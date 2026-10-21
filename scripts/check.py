#!/usr/bin/env python3
"""Pre-commit checks for ai-garden (stdlib only; markdownlint runs through npx when available).

    python3 scripts/check.py             # the working tree, as it is on disk
    python3 scripts/check.py --staged    # exactly what `git commit` would record
    python3 scripts/check.py --all       # scan every tracked file, not only the changed ones

--staged checks the index, ignoring untracked files and unstaged edits; it is the check to run
before a commit. Stage only your own files first (`git add <paths>`), so another agent's
unfinished files neither block the check nor slip into the commit. The flags combine.
Exit 1 on any ERROR. WARN lines need a human look but do not fail.

Whole-tree checks:
1. Index links resolve, and every note is listed in the index of its own language:
   notes/**/X.md in README_zh.md, notes/**/X_en.md in README.md; ideas/ and news/ notes in
   that section's README_zh.md / README.md. README.md is the English index (GitHub's default
   page), so a README_en.md is stale.
2. Relative links and images inside notes resolve.
3. No note carries a 成熟度 / 类型 / 作者 (Maturity / Type / Author) metadata line, and no index
   entry starts with a maturity emoji (🌱 / 🌿 / 🌳).
4. Bilingual twins: every note and index has its twin (twin_audit.pair_of) and the pair passes
   twin_audit.audit_pair: line for line, identical code, same URLs and footnotes, and a
   language-switcher line under each title.

Checks on files changed vs origin/main (--all: every tracked file):
5. Notes are Markdown only: no .html / .htm / .pdf / .doc / .docx / .pptx under notes/, ideas/, news/.
6. Text files hold no API keys, tokens or private keys (ERROR) and no confidentiality wording
   (WARN), plus the patterns in scripts/private-patterns.txt: a local, git-ignored file, one
   `ERROR|WARN <tab> regex <tab> label` per line, for markers that must never be published but
   are too private to commit themselves. A missing file is a WARN, so a fresh clone still works.
7. Files over 5 MB get a WARN (changed files only).
8. markdownlint, configured by .markdownlint-cli2.jsonc, passes on the .md files.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)  # the git repository
ROOT = REPO                   # the tree under check: REPO, or an export of the index (--staged)
sys.path.insert(0, HERE)
from twin_audit import audit_pair, is_english, pair_of  # noqa: E402

SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9_-]{20,}", "API key (sk-...)"),
    (r"gh[pousr]_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"nvapi-[A-Za-z0-9_-]{20,}", "NVIDIA API key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
]
WARN_PATTERNS = [
    (r"内部资料|内部文档|内部数据|仅限内部|请勿外传|机密|保密", "confidentiality wording"),
    (r"(?i)\bconfidential\b|internal use only|do not distribute", "confidentiality wording"),
]
PRIVATE_PATTERNS = os.path.join(HERE, "private-patterns.txt")
NOT_SCANNED = {"scripts/check.py"}  # it holds the patterns themselves
TEXT_EXT = {".md", ".html", ".htm", ".txt", ".json", ".csv", ".yaml", ".yml", ".py", ".ipynb", ".svg", ".tex"}
LINK_RE = re.compile(r'\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
BIG = 5 * 1024 * 1024
NON_MD_DOCS = (".html", ".htm", ".pdf", ".docx", ".doc", ".pptx")
NOTE_DIRS = ("notes/", "ideas/", "news/")
EN = "_en.md"
INDEX_FILES = ("README.md", "README_zh.md", "ideas/README.md", "ideas/README_zh.md",
               "news/README.md", "news/README_zh.md")
STALE_FILES = ("README_en.md", "ideas/README_en.md", "news/README_en.md")
BANNED_META_RE = re.compile(r"(?m)^[-*]\s+\*\*(成熟度|类型|作者|Maturity|Type|Author)\*\*\s*[:：]")
INDEX_EMOJI_RE = re.compile(r"(?m)^\s*[-*]\s+(🌱|🌿|🌳)\s*\[")
LINT_CFG = os.path.join(REPO, ".markdownlint-cli2.jsonc")
USAGE = "usage: python3 scripts/check.py [--staged] [--all]"


def load_private_patterns():
    """(error_patterns, warn_patterns, note) from the local, git-ignored patterns file."""
    if not os.path.exists(PRIVATE_PATTERNS):
        return [], [], f"{os.path.relpath(PRIVATE_PATTERNS, REPO)} not found - only the built-in patterns ran"
    errors, warns = [], []
    with open(PRIVATE_PATTERNS, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != 3 or parts[0] not in ("ERROR", "WARN"):
                raise SystemExit(f"{PRIVATE_PATTERNS}:{n}: expected 'ERROR|WARN<TAB>regex<TAB>label'")
            (errors if parts[0] == "ERROR" else warns).append((parts[1], parts[2]))
    return errors, warns, None


def markdownlint(md_files):
    if not md_files:
        return [], []
    if not shutil.which("npx"):
        return [], ["markdownlint skipped: npx not found"]
    cmd = ["npx", "--yes", "markdownlint-cli2", "--config", LINT_CFG] + [":" + f for f in md_files]
    try:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return [], ["markdownlint skipped: timed out"]
    issues = [ln for ln in (r.stdout + r.stderr).splitlines()
              if re.search(r":\d+(?::\d+)? (?:error|warning) MD\d{3}", ln)]
    if r.returncode != 0 and not issues:
        return [], [f"markdownlint did not run cleanly (exit {r.returncode}): {(r.stderr or r.stdout).strip()[:200]}"]
    return [f"markdownlint: {ln}" for ln in issues], []


def git(*args):
    r = subprocess.run(["git", "-C", REPO, "-c", "core.quotePath=false", *args],
                       capture_output=True, text=True)
    return [line for line in r.stdout.splitlines() if line.strip()]


def export_index():
    """Write the index - what `git commit` would record - to a temp dir and return its path."""
    dst = tempfile.mkdtemp(prefix="ai-garden-staged-")
    subprocess.run(["git", "-C", REPO, "checkout-index", "--all", "--force", f"--prefix={dst}/"],
                   check=True, capture_output=True)
    return dst


def changed_files(scan_all, staged):
    """Repo-relative paths for the file checks (5-8)."""
    if scan_all:
        files = set(git("ls-files"))
        if not staged:
            files.update(git("ls-files", "--others", "--exclude-standard"))
        return files
    base = "origin/main" if git("rev-parse", "--verify", "--quiet", "origin/main") else None
    if staged:
        return set(git("diff", "--cached", "--name-only", base) if base else git("ls-files"))
    files = set(git("diff", "--name-only", f"{base}...HEAD")) if base else set()
    files.update(git("diff", "--name-only", "HEAD"))
    files.update(git("diff", "--name-only", "--cached"))
    files.update(git("ls-files", "--others", "--exclude-standard"))
    return files


def is_local(target):
    return not re.match(r"^(https?:|mailto:|#|data:)", target)


def resolve(base_dir, target):
    target = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
    return os.path.normpath(os.path.join(base_dir, target))


def index_for(rel):
    """The index that must list note `rel`: the one in the note's own language."""
    top = rel.split("/", 1)[0]
    d = top if top in ("ideas", "news") else ""
    zh, en = pair_of(os.path.join(d, "README.md"))
    return en if rel.endswith(EN) else zh


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def local_links(rel, body):
    base = os.path.dirname(os.path.join(ROOT, rel))
    return [(t, resolve(base, t)) for t in LINK_RE.findall(body) if is_local(t)]


def run_checks(scan_all, staged):
    errors, warns = [], []

    indexes = {rel: read(rel) for rel in INDEX_FILES if os.path.exists(os.path.join(ROOT, rel))}
    for rel in STALE_FILES:
        if os.path.exists(os.path.join(ROOT, rel)):
            errors.append(f"{rel}: stale - README.md is the English index (Chinese: README_zh.md)")
    linked_from = {}
    for rel, body in indexes.items():
        for m in INDEX_EMOJI_RE.finditer(body):
            errors.append(f"{rel}: index entry starts with maturity emoji {m.group(1)} - drop it")
        targets = set()
        for t, p in local_links(rel, body):
            targets.add(p)
            if not os.path.exists(p):
                errors.append(f"{rel} link does not resolve: {t}")
        linked_from[rel] = targets

    found = set(glob.glob(os.path.join(ROOT, "notes", "**", "*.md"), recursive=True)
                + glob.glob(os.path.join(ROOT, "ideas", "*.md"))
                + glob.glob(os.path.join(ROOT, "news", "*.md")))
    notes = sorted(r for r in (os.path.relpath(p, ROOT) for p in found)
                   if r not in INDEX_FILES and r not in STALE_FILES)
    bodies = dict(indexes)
    for rel in notes:
        body = bodies[rel] = read(rel)
        idx = index_for(rel)
        if os.path.normpath(os.path.join(ROOT, rel)) not in linked_from.get(idx, set()):
            errors.append(f"note not listed in {idx}: {rel}")
        for m in BANNED_META_RE.finditer(body):
            errors.append(f"{rel}: remove the '{m.group(1)}' metadata line")
        for t, p in local_links(rel, body):
            if not os.path.exists(p):
                errors.append(f"{rel}: broken relative link {t}")

    pairs = 0
    for rel in sorted(bodies):
        zh, en = pair_of(rel)
        twin = zh if rel == en else en
        if not os.path.exists(os.path.join(ROOT, twin)):
            errors.append(f"{rel}: missing its {'Chinese' if is_english(rel) else 'English'} twin {twin}")
            continue
        if rel == en:
            continue
        pairs += 1
        p_errors, p_warns, _ = audit_pair(os.path.join(ROOT, zh), os.path.join(ROOT, en),
                                          rel=lambda p: os.path.relpath(p, ROOT))
        errors += p_errors
        warns += p_warns

    files = sorted(f for f in changed_files(scan_all, staged) if os.path.isfile(os.path.join(ROOT, f)))
    for f in files:
        if f.startswith(NOTE_DIRS) and f.lower().endswith(NON_MD_DOCS):
            errors.append(f"{f}: notes are Markdown only - convert to .md (or link the original)")

    lint_targets = [f for f in files if f.lower().endswith(".md")]
    lint_errors, lint_warns = markdownlint(lint_targets)
    errors += lint_errors
    warns += lint_warns

    priv_errors, priv_warns, note = load_private_patterns()
    if note:
        warns.append(note)
    for f in files:
        full = os.path.join(ROOT, f)
        if not scan_all and os.path.getsize(full) > BIG:
            warns.append(f"{f}: {os.path.getsize(full) / 2**20:.1f} MB - compress or link instead?")
        if f in NOT_SCANNED or os.path.splitext(f)[1].lower() not in TEXT_EXT:
            continue
        body = open(full, encoding="utf-8", errors="ignore").read()
        for pats, bucket in ((SECRET_PATTERNS + priv_errors, errors), (WARN_PATTERNS + priv_warns, warns)):
            for pat, label in pats:
                hits = list(re.finditer(pat, body))
                if hits:
                    ctx = re.sub(r"\s+", " ", body[max(0, hits[0].start() - 40):hits[0].end() + 40])
                    bucket.append(f"{f}: {label} x{len(hits)} e.g. ...{ctx}...")

    tree = "staged tree" if staged else "working tree"
    scope = "all tracked files" if scan_all else f"{len(files)} changed file(s)"
    print(f"{tree}: {len(indexes)} index file(s), {len(notes)} notes, {pairs} zh/en pair(s); "
          f"scanned {scope}; markdownlint on {len(lint_targets)} file(s)")
    for w in warns:
        print("WARN:", w)
    for e in errors:
        print("ERROR:", e)
    if errors and not staged:
        untracked = git("ls-files", "--others", "--exclude-standard")
        named = [f for f in untracked if any(f in e for e in errors)]
        if named:
            print("HINT: errors name untracked file(s): " + ", ".join(named) + ". If you did not "
                  "create them, another agent may still be writing them. Leave them alone, "
                  "`git add` only your own files and re-run with --staged.")
    print("FAILED" if errors else "OK")
    return 1 if errors else 0


def main():
    global ROOT
    args = sys.argv[1:]
    if args in (["-h"], ["--help"]):
        print(__doc__)
        return 0
    if any(a not in ("--all", "--staged") for a in args):
        raise SystemExit(USAGE)
    scan_all, staged = "--all" in args, "--staged" in args
    if staged:
        ROOT = export_index()
    try:
        return run_checks(scan_all, staged)
    finally:
        if staged:
            shutil.rmtree(ROOT, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
