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

## Naming

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Project name | `yoto-maker` (renaming from `yoto-card-maker`) | Shorter. Rename pending — do it before any code is written. |
| CLI entry point | `yoto-maker` | Matches project name. |
| Python package | `yoto_card_maker` → will become `yoto_maker` | Update after directory rename. |
