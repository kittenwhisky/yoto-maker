# Build Plan: Yoto Card Maker

## Phase 1 — Scaffold project

- Create `pyproject.toml` with metadata, dependencies (`yt-dlp`, `InquirerPy`), and `[project.scripts]` entry point (`yoto-maker`)
- Create `src/yoto_card_maker/` package with `__init__.py`
- Create `.gitignore` (Python template)

## Phase 2 — Implement catalog module

- `src/yoto_card_maker/catalog.py`
- Use `yt-dlp` Python API to extract playlist metadata (title, URL per video) without downloading
- Write results to CSV with columns: `track_number`, `title`, `url`

## Phase 3 — Implement download module

- `src/yoto_card_maker/download.py`
- Read validated CSV
- For each row: download audio via `yt-dlp`, convert to MP3, save as `{title}.mp3` in output directory
- Show progress (e.g. `[1/50] Mr. Happy ✓`)

## Phase 4 — Implement interactive CLI menu

- `src/yoto_card_maker/cli.py`
- Entry point: `yoto-maker` launches interactive menu via `InquirerPy`
- Option 1: Catalog — prompts for playlist URL and output CSV path
- Option 2: Download — prompts for CSV path and output directory
- Wire menu choices to catalog and download modules

## Phase 5 — Test with Mr. Men playlist

- Run `pip install -e .`
- Run `yoto-maker`, select catalog, paste playlist URL
- Validate generated CSV
- Run `yoto-maker`, select download, test with first 2 tracks
- Verify MP3 files exist with correct names

## Phase 6 — Documentation, Git & GitHub

### GitHub setup (one-time, during Phase 1 scaffold)
- Create GitHub repo via `gh repo create yoto-card-maker --private --source . --remote origin`
- Git remote URL is stored in `.git/config` automatically — no `.env` needed

### Git strategy
- Commit to `main` after each phase passes tests & review
- Tag milestones: `git tag phase-N-description`
- Push to GitHub after each phase commit

### README.md (extensive — for humans & GitHub)
- Project description and purpose
- Installation instructions (Python, ffmpeg, pip install)
- Usage guide with full CLI walkthrough (catalog → validate → download)
- CSV format specification
- Examples with sample output
- Tech stack and dependencies
- Future roadmap (Yoto API upload)

### CLAUDE.md (succinct — for future Claude Code sessions)
- Build/run commands only (`pip install -e .`, `yoto-maker`, `pytest`)
- Module responsibility map (one line per module)
- Key conventions (e.g., CSV column names, naming patterns)
