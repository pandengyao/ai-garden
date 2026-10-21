# AGENTS.md

Rules for AI coding agents (Codex, Claude Code, Cursor, Copilot, Hermes and others) working in this repo. For humans, the overview is [README.md](./README.md).

**This repo is public.** Anything committed is world-readable and stays in git history, even after a later commit deletes it.

## What this repo is

A personal digital garden of AI notes: research, reading and thinking about AI, written up one note at a time. It is not a software project. The only code is the checker in `scripts/`.

## Layout

| Path | Contents |
| --- | --- |
| `notes/<topic>/X.md`, `X_en.md` | Notes on articles, papers and reports, and original research. Topic folders are `snake_case`: `agent`, `inference`, `llm_api`, `multimodal` so far |
| `notes/<topic>/img/` | Images for that topic. Name new ones `<File>-<what>.<ext>` |
| `ideas/YYYY-MM-DD-<slug>.md`, `_en.md` | Short original ideas |
| `news/YYYY-MM.md`, `_en.md` | AI news, one file per month, newest entry first |
| `README.md`, `README_zh.md` | The English index (GitHub's front page) and the Chinese index |
| `ideas/README*.md`, `news/README*.md` | Indexes for those sections, split the same way |
| `scripts/check.py`, `scripts/twin_audit.py` | The checker. Run it before every commit |
| `scripts/private-patterns.txt` | Extra patterns for the checker. Local only and git-ignored, so never commit it |

## Two languages for every note

Every note and index exists in Chinese and in English.

- **Notes are Chinese-first**: `X.md` is the Chinese original and `X_en.md` its English translation, in the same folder.
- **READMEs are the other way round**: `README.md` is English and `README_zh.md` is Chinese. There is no `README_en.md`.
- **Indexes**: list each Chinese note in `README_zh.md` and its English twin in `README.md`, in the same section and position.
- **Language switcher**: the line right under each title is `中文 | [English](./<English file>)` in the Chinese file and `[中文](./<Chinese file>) | English` in the English one.
- **Line for line**: line N of the English file translates line N of the Chinese one. Keep every blank line, heading level, list marker and indent, table shape, footnote id, URL and image path. Paragraphs are single lines, so this always works.
- **Copy code, don't retype it**: a code line without Chinese is byte-identical in both files. In a line with Chinese, translate only the comment or string. `python3 scripts/twin_audit.py --sync-fences <file>` copies the Chinese-free code lines for you. Without the flag, it audits a pair.
- **Translate faithfully**: never add, cut or update a fact in one language only. Use English brand names for Chinese companies, such as Zhipu, Alibaba Bailian, Volcano Ark, StepFun and Moonshot AI (Kimi). Turn Chinese discounts into percentages (2.5 折 = 75% off, 五折 = 50% off), and 万 / 亿 into thousand, million or billion.
- **Change both files in the same commit.** The checker fails when a pair is missing a file or the two have drifted apart.

`AGENTS.md` and `CLAUDE.md` are for agents and stay English only.

## Writing a note

- Notes are Markdown only. Turn an HTML, PDF, Word or slide source into a Markdown note, and link the original instead of committing it.
- Under the switcher line, start with a metadata list: the source (`原文链接` / `Source`, or `官方发布` / `Official announcement`) and one date (`发布日期` / `Published` for a source; `调研日期` / `Research date` or `整理日期` / `Compiled` for original work). `论文` / `Paper`, `官方资料` / `Official resources`, `实测环境` / `Test environment` and `范围` / `Scope` are optional.
- Never add a `成熟度`, `类型` or `作者` (Maturity, Type, Author) line, and never start an index entry with 🌱, 🌿 or 🌳. The checker rejects both.
- Explain in your own words and quote only short passages. Never paste a source wholesale.
- Every number, name and date comes from the source. Check release dates against the vendor's own announcement, and run every code example before you publish it.
- Index entries go newest first within their section, as `- [Title: subtitle](./notes/<topic>/<File>.md) · YYYY-MM-DD` followed by an indented one-line summary of the conclusion. The date is the source's publication date. Sections are sorted by their English names.

## Markdown style

markdownlint enforces most of this.

- Leave a blank line before and after every heading, list, table, code block, image and caption.
- Use `-` for bullets and `1.` for numbered lists, with one space after the marker. Indent nested items 2 spaces under `-` and 3 under `1.`.
- Write one paragraph per line, with no hard wraps. Don't skip heading levels.
- No raw HTML. Put identifiers and anything with angle brackets in backticks.
- Table delimiter rows have spaces: `| --- | --- |`.
- An image is `![alt](./img/x.png)`, then a blank line, then an italic caption that ends with punctuation.
- No YAML frontmatter. GitHub shows it on the page, so metadata goes in the list at the top.

## Never

- Commit employer-internal material: intranet links, internal documents or reports, colleagues' names or email addresses, internal tools, unreleased metrics. That includes raw HTML or PDF exports of a public page, which can carry hidden metadata. If you are not sure something is public, stop and ask the owner.
- Commit secrets such as API keys or tokens. Example commands read them from environment variables like `$NVIDIA_API_KEY`.
- Use a work email as the commit author. Commits go out under the owner's personal GitHub identity, which this clone's git config already sets.
- Force-push or rewrite history unless the owner explicitly asks.
- Stage with `git add -A` or `git add .`. Several agents may work in this clone at once, and another one's unfinished files (say, a Chinese note whose English twin isn't written yet) may be in the tree. Leave files you didn't create alone.

## Before every commit

```bash
git add <your files>
python3 scripts/check.py --staged      # add --all after a restructure
git commit -m "<message>" -- <your files>
```

The check must end with `OK`. It runs on exactly what the commit will contain, and covers indexes, links, the language pairs, metadata, secrets and markdownlint (via `npx`, so it needs Node.js). Fix every `ERROR` and read every `WARN`. A `WARN` on a quote from a vendor's terms of service is fine. Without `--staged`, it checks the whole working tree, including other agents' unfinished files. Naming the paths in `git commit` keeps anything another agent staged out of your commit.

Commit messages follow Conventional Commits, such as `docs: add <topic> note` or `docs(news): add 2026-10 items`. When the owner changes a convention, update this file in the same commit, and `scripts/check.py` too if it enforces the rule.
