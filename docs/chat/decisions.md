# Decisions Log

Key decisions made during project planning. Future Claude sessions should append new decisions here.

## Language & Framework

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python | `yt-dlp` is a native Python library — core dependency for YouTube download. Also has existing `yoto-api` Python library for future Yoto upload feature. |
| CLI UX | Interactive menu (InquirerPy) | User prefers guided prompts over subcommands. Run `yoto-maker` → pick action → enter inputs one by one. |
| CLI framework | InquirerPy (not Typer) | Driven by interactive menu requirement. Typer is subcommand-oriented. |

## Scope

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Bell chimes | Descoped | Originally planned to add page-turn chimes synced to ebook text. User simplified scope to just downloading audio from YouTube. |
| Yoto API upload | Future — not in v1 | Keep modules separate so `upload.py` and `auth.py` can be added later without touching existing code. |
| First use case | Mr. Men audiobook series (~50 books) | YouTube playlist: `https://www.youtube.com/playlist?list=PL3LDD1LouE8hghr2vbI3_B64SGGbU8Je8` |

## Architecture

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Module structure | Separate files: `catalog.py`, `download.py`, `cli.py` | Modularity for future extensibility (upload module). No cross-dependencies between catalog and download. |
| CSV as intermediate format | `track_number`, `title`, `url` columns | User validates/edits CSV manually between catalog and download steps. Human-in-the-loop by design. |

## Workflow & Tooling

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Git strategy | Commit to `main` after each phase passes | Solo project — PRs and worktrees are unnecessary overhead. Tag each phase milestone. |
| Subagent workflow | 3-agent loop per phase (Coder → Tester → Reviewer) | Coder writes code, Tester validates, Reviewer checks against PRD/plan and creates debug plan if needed. Loop until pass. |
| Parallel phases | Phases 2, 3, 4 run in parallel | catalog.py, download.py, cli.py have no write-time dependencies. |
| Documentation | README.md (extensive, for humans) + CLAUDE.md (succinct, for AI) | Different audiences, different detail levels. CLAUDE.md kept short for token efficiency. |

## Bugfixes & Robustness (2026-02-15)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CLI path quoting | Strip `"` and `'` from all path inputs in `cli.py` | Users paste paths with surrounding quotes from Windows Explorer / terminal. `.strip()` alone only removes whitespace. |
| CSV encoding | `utf-8-sig` instead of `utf-8` in `download.py` | CSV files saved from Excel or other tools often include a UTF-8 BOM (`\xef\xbb\xbf`), which corrupts the first column name for `DictReader`. `utf-8-sig` strips it automatically. |
| CSV header whitespace | Strip whitespace from `DictReader.fieldnames` | Defensive measure against headers with trailing/leading spaces. |
| CSV column validation | Validate required columns exist before processing | Provides a clear error message with actual vs expected column names instead of a cryptic `KeyError`. |
| yt-dlp JS runtime | Node.js via `js_runtimes: {"node": {}}` | YouTube now requires a JavaScript runtime for player challenge solving. Node.js is already installed on the dev machine. yt-dlp only enables `deno` by default. |
| yt-dlp EJS solver | `remote_components: {"ejs:github"}` | yt-dlp needs the EJS challenge solver script to extract YouTube formats. This option auto-downloads it from GitHub on first use. |

## CLI UX Enhancements (2026-02-15)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Menu prompt type | `inquirer.rawlist` instead of `inquirer.select` | Prepends numbered labels (`1)`, `2)`) to menu options and lets users type a number or use arrow keys to select. Matches the numbered menu UX shown in the PRD. |

## Naming

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Project name | `yoto-maker` (renaming from `yoto-card-maker`) | Shorter. Rename pending — do it before any code is written. |
| CLI entry point | `yoto-maker` | Matches project name. |
| Python package | `yoto_card_maker` → will become `yoto_maker` | Update after directory rename. |
