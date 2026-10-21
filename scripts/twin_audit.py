#!/usr/bin/env python3
"""Audit a Chinese file against its English twin, line by line (stdlib only).

    python3 twin_audit.py <file> [<file> ...]            # report ERROR / WARN / REVIEW
    python3 twin_audit.py --sync-fences <file> [...]     # first copy non-CJK fence lines zh -> en

Either file of a pair may be named. Pairs are named by pair_of():
    notes, ideas, news    X.md (Chinese)          <->  X_en.md (English)
    READMEs (any dir)     README_zh.md (Chinese)  <->  README.md (English, GitHub's default)

ai-garden keeps every note and index in Chinese and English, written line for line:
line i of the English file translates line i of the Chinese one. Paragraphs are single
lines in this repo, so that is always possible, and it makes drift mechanical to catch:

ERROR   line counts differ; a line's kind differs (blank, heading level, list marker and
        indent, table pipe count or delimiter row, blockquote, footnote id, fence);
        a code-fence line with no CJK differs from the Chinese one; in a code line WITH
        Chinese (a comment or string), the code before the first / after the last Chinese
        character changed (prose fences - text, md, none - are exempt); the URLs, image
        targets or footnote refs on a line differ; either file lacks the
        language-switcher link to its twin
WARN    inline code spans without CJK differ; local link targets differ once both are
        mapped to the Chinese side; Chinese is left in the English file outside the switcher
REVIEW  the numbers on a line differ after unit normalisation (100 万 = 1M = 1,000,000):
        usually a deliberate rewording (2.5 折 -> 75% off), sometimes a typo

--sync-fences copies every code-fence line without CJK from the Chinese file into the
English one, so code is copied rather than retyped; only comment/string lines holding
Chinese get translated. scripts/check.py calls pair_of() and audit_pair(): ERROR fails the
push, WARN is printed, REVIEW is shown only by this CLI.
"""
import os
import re
import sys
from collections import Counter

EN = "_en.md"
ZH_README = "README_zh.md"
CJK_RE = re.compile(r"[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef]")
URL_RE = re.compile(r"https?://[^\s)>\]`\"'<|]+")
CODE_RE = re.compile(r"`([^`\n]+)`")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
FN_REF_RE = re.compile(r"\[\^([^\]]+)\](?!:)")
SWITCHER_ZH_RE = re.compile(r"^中文 \| \[English\]\((\./[^)\s]+\.md)\)$")
SWITCHER_EN_RE = re.compile(r"^\[中文\]\((\./[^)\s]+\.md)\) \| English$")
NUM_RE = re.compile(r"(\d+(?:,\d{3})*(?:\.\d+)?)\s*(万|亿|thousand|million|billion|[KMB](?![A-Za-z]))?")
SCALE = {"万": 1e4, "亿": 1e8, "K": 1e3, "M": 1e6, "B": 1e9,
         "thousand": 1e3, "million": 1e6, "billion": 1e9, None: 1.0}
# Fences holding prose (dialogue, diagrams): their Chinese lines are translated freely.
PROSE_FENCES = {"", "text", "txt", "plain", "markdown", "md"}


def pair_of(path):
    """(chinese_path, english_path) for either file of a pair.

    READMEs are English by default (README.md, what GitHub renders) with the Chinese in
    README_zh.md; every other file is Chinese as X.md with the English in X_en.md.
    """
    d, base = os.path.split(path)
    if base in ("README.md", ZH_README, "README" + EN):
        return os.path.join(d, ZH_README), os.path.join(d, "README.md")
    if base.endswith(EN):
        return os.path.join(d, base[: -len(EN)] + ".md"), path
    return path, os.path.join(d, base[:-3] + EN)


def is_english(path):
    return pair_of(path)[1] == path


def twin_of(path):
    zh, en = pair_of(path)
    return zh if path == en else en


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    return lines[:-1] if lines and lines[-1] == "" else lines


def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def clean_url(u):
    return CJK_RE.split(u)[0].rstrip(".,;:")


def is_local(t):
    return not re.match(r"^(https?:|mailto:|#|data:)", t)


def norm_local(t, base_dir):
    """A local link target mapped to the Chinese side of its pair, for comparing link sets."""
    t = t.split("#", 1)[0]
    if not t or t.endswith("/"):
        t += "README.md"
    zh, _ = pair_of(os.path.normpath(os.path.join(base_dir, t)))
    return zh


def kind(line):
    s = line.strip()
    if not s:
        return ("blank",)
    if s.startswith("```"):
        return ("fence", s)
    m = re.match(r"(#{1,6})\s", line)
    if m:
        return ("heading", len(m.group(1)))
    if s.startswith("|"):
        if re.fullmatch(r"\|(?:\s*:?-{3,}:?\s*\|)+", s):
            return ("table delimiter", s)
        return ("table row", len(re.findall(r"(?<!\\)\|", CODE_RE.sub("", s))))
    m = re.match(r"(\s*)([-*+]|\d+\.)\s", line)
    if m:
        marker = m.group(2)
        return ("list item", len(m.group(1)), "-" if marker in "-*+" else marker)
    if s.startswith(">"):
        return ("blockquote",)
    m = re.match(r"\[\^([^\]]+)\]:", s)
    if m:
        return ("footnote", m.group(1))
    return ("text",)


def fmt(k):
    if k[0] == "heading":
        return f"a level-{k[1]} heading"
    if k[0] == "list item":
        return f"a list item (indent {k[1]}, marker {k[2]!r})"
    if k[0] == "table row":
        return f"a table row with {k[1]} pipes"
    if len(k) > 1:
        return f"{k[0]} {k[1]!r}"
    return f"a {k[0]} line"


def short(s):
    return repr(s.strip()[:70])


def prose(line):
    """The line minus code, link targets, URLs, footnote markers and list markers."""
    t = CODE_RE.sub(" ", line)
    t = re.sub(r"\]\([^)\s]*\)", "]", t)
    t = URL_RE.sub(" ", t)
    t = re.sub(r"\[\^[^\]]+\]:?", " ", t)
    return re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", t)


def numbers(text):
    return Counter(round(float(m.group(1).replace(",", "")) * SCALE[m.group(2)], 6)
                   for m in NUM_RE.finditer(text))


def diff(xs, ys):
    a, b = Counter(xs), Counter(ys)
    return f"only zh {sorted(map(str, (a - b).elements()))[:4]}, only en {sorted(map(str, (b - a).elements()))[:4]}"


def switcher_target(lines, rx):
    for line in lines[:8]:
        m = rx.match(line.strip())
        if m:
            return os.path.basename(m.group(1))
    return None


def audit_pair(zh_path, en_path, rel=None):
    """Return (errors, warns, reviews) for one zh/en pair; `rel` turns a path into a display name."""
    rel = rel or (lambda p: p)
    zr, er = rel(zh_path), rel(en_path)
    errors, warns, reviews = [], [], []
    zh, en = read_lines(zh_path), read_lines(en_path)

    if switcher_target(zh, SWITCHER_ZH_RE) != os.path.basename(en_path):
        errors.append(f"{zr}: put `中文 | [English](./{os.path.basename(en_path)})` under the title")
    if switcher_target(en, SWITCHER_EN_RE) != os.path.basename(zh_path):
        errors.append(f"{er}: put `[中文](./{os.path.basename(zh_path)}) | English` under the title")
    if len(zh) != len(en):
        errors.append(f"{er}: {len(en)} lines but {zr} has {len(zh)} - translate line for line")
        return errors, warns, reviews

    in_fence, lang = False, ""
    for i, (a, b) in enumerate(zip(zh, en), 1):
        ka, kb = kind(a), kind(b)
        if in_fence and ka[0] != "fence":
            if not CJK_RE.search(a):
                if a != b:
                    errors.append(f"{er}:{i}: code must match {zr} exactly: {short(a)} vs {short(b)}")
                continue
            if lang not in PROSE_FENCES:
                # Only the Chinese span (a comment or a string) may change; the code around it may not.
                spans = [m.span() for m in CJK_RE.finditer(a)]
                pre, suf = a[:spans[0][0]], a[spans[-1][1]:]
                if not (b.startswith(pre) and b.endswith(suf) and len(b) >= len(pre) + len(suf)):
                    errors.append(f"{er}:{i}: only the Chinese part of this code line may change - "
                                  f"keep {pre.strip()!r} before it and {suf.strip()!r} after it: {short(b)}")
            if CJK_RE.search(b):
                warns.append(f"{er}:{i}: Chinese left in code: {short(b)}")
            continue
        if ka != kb:
            errors.append(f"{er}:{i}: {fmt(kb)} where {zr} has {fmt(ka)}")
        if ka[0] == "fence":
            in_fence = not in_fence
            lang = ka[1][3:].strip().lower() if in_fence else ""
            if a != b:
                errors.append(f"{er}:{i}: fence must match {zr} exactly: {short(a)} vs {short(b)}")
            continue

        a_nc, b_nc = CODE_RE.sub("", a), CODE_RE.sub("", b)
        for label, xs, ys, bucket in (
            ("footnote refs", FN_REF_RE.findall(a_nc), FN_REF_RE.findall(b_nc), errors),
            ("image targets", IMG_RE.findall(a), IMG_RE.findall(b), errors),
            ("URLs", [clean_url(u) for u in URL_RE.findall(a)], [clean_url(u) for u in URL_RE.findall(b)], errors),
            ("inline code", [c for c in CODE_RE.findall(a) if not CJK_RE.search(c)],
             [c for c in CODE_RE.findall(b) if not CJK_RE.search(c)], warns),
        ):
            if Counter(xs) != Counter(ys):
                bucket.append(f"{er}:{i}: {label} differ from {zr} - {diff(xs, ys)}")

        if not (SWITCHER_ZH_RE.match(a.strip()) or SWITCHER_EN_RE.match(b.strip())):
            za, zb = os.path.dirname(zh_path), os.path.dirname(en_path)
            la = [norm_local(t, za) for t in LINK_RE.findall(a) if is_local(t)]
            lb = [norm_local(t, zb) for t in LINK_RE.findall(b) if is_local(t)]
            if Counter(la) != Counter(lb):
                warns.append(f"{er}:{i}: local links differ from {zr} - {diff(la, lb)}")
            m = CJK_RE.search(b_nc)
            if m:
                warns.append(f"{er}:{i}: Chinese left: ...{b_nc[max(0, m.start() - 25):m.end() + 25]}...")

        if ka[0] != "heading":
            na, nb = numbers(prose(a)), numbers(prose(b))
            if na != nb:
                reviews.append(f"{er}:{i}: numbers differ - {diff(list(na.elements()), list(nb.elements()))}"
                               f"\n      zh: {a.strip()[:110]}\n      en: {b.strip()[:110]}")
    return errors, warns, reviews


def sync_fences(zh_path, en_path):
    """Copy code-fence lines without CJK from zh into en. Returns how many lines changed."""
    zh, en = read_lines(zh_path), read_lines(en_path)
    if len(zh) != len(en):
        raise SystemExit(f"{en_path}: {len(en)} lines vs {len(zh)} - align the files before syncing fences")
    in_fence, changed = False, 0
    for i, a in enumerate(zh):
        is_fence = kind(a)[0] == "fence"
        if (in_fence or is_fence) and not CJK_RE.search(a) and en[i] != a:
            en[i] = a
            changed += 1
        if is_fence:
            in_fence = not in_fence
    if changed:
        write_lines(en_path, en)
    return changed


def main():
    args = sys.argv[1:]
    sync = "--sync-fences" in args
    paths = [p for p in args if not p.startswith("--")]
    if not paths:
        print(__doc__)
        sys.exit(2)
    failed = False
    for p in paths:
        zh, en = pair_of(p)
        if sync:
            print(f"{en}: synced {sync_fences(zh, en)} code line(s) from {zh}")
        errors, warns, reviews = audit_pair(zh, en)
        print(f"== {zh} <-> {en}: {len(errors)} error(s), {len(warns)} warning(s), {len(reviews)} to review")
        for tag, items in (("ERROR", errors), ("WARN", warns), ("REVIEW", reviews)):
            for item in items:
                print(f"{tag}: {item}")
        failed |= bool(errors)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
