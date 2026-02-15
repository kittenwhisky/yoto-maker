# PRD: Yoto Card Maker — YouTube Playlist to MP3 Downloader

## Goal

A Python CLI tool that takes a YouTube playlist, generates a CSV for the user to validate, then batch-downloads each track as an MP3 file with clean filenames.

## Workflow

```
Phase 1: Catalog          Phase 2: Validate        Phase 3: Download
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ YouTube playlist │ ──▶ │ CSV with #,       │ ──▶ │ Download MP3s    │
│ URL as input     │     │ title, URL        │     │ to output folder │
└──────────────────┘     │ User edits CSV    │     └──────────────────┘
                         └──────────────────┘
```

### Phase 1 — Catalog generation
- Input: YouTube playlist URL
- Output: CSV file with columns: `track_number`, `title`, `url`
- Tool: `yt-dlp` (extract playlist metadata without downloading)

### Phase 2 — User validation
- User opens CSV, removes unwanted tracks, corrects titles, reorders track numbers
- This is a manual step outside the tool

### Phase 3 — Batch download
- Input: Validated CSV + output folder path
- For each row: download audio from URL, convert to MP3, save as `{title}.mp3`
- Tool: `yt-dlp` with ffmpeg for MP3 conversion

## CLI UX

Run `yoto-maker` to launch an interactive menu:

```
$ yoto-maker

Welcome to Yoto Card Maker!

What would you like to do?
  1) Catalog a YouTube playlist
  2) Download tracks from a catalog

> 1

Enter YouTube playlist URL: https://www.youtube.com/playlist?list=PL3LDD1...
Output CSV path [tracks.csv]: mr-men-tracks.csv

✓ Saved 52 tracks to mr-men-tracks.csv
```

```
$ yoto-maker

What would you like to do?
  1) Catalog a YouTube playlist
  2) Download tracks from a catalog

> 2

Path to catalog CSV: mr-men-tracks.csv
Output directory [./output]: ./mr-men-audiobooks

Downloading 50 tracks...
  [1/50] Mr. Happy ✓
  [2/50] Mr. Grumpy ✓
  ...
```

Library: **`inquirerpy`** (or **`rich` prompts**) for the interactive menu and input prompts.

## Tech Stack

- **Python 3.12+**
- **InquirerPy** — interactive menu prompts and user input
- **yt-dlp** — YouTube metadata extraction & audio download
- **ffmpeg** — audio conversion (yt-dlp uses it under the hood)
- **csv** — stdlib, for reading/writing the catalog

## Future: Yoto Upload (not in scope now)

A future `yoto upload` command will upload processed MP3s to Yoto as MYO card playlists via the [Yoto Developer API](https://yoto.dev/api/). This informs the modular design below — the CLI, catalog, and download modules are kept separate so an `upload.py` module can be added later without touching existing code.

## File Structure

```
yoto-card-maker/
├── pyproject.toml
├── src/
│   └── yoto_card_maker/
│       ├── __init__.py
│       ├── cli.py          # Interactive menu entry point
│       ├── catalog.py      # Playlist → CSV extraction
│       └── download.py     # CSV → MP3 batch download
│       # future: upload.py — Yoto API upload
│       # future: auth.py   — Yoto OAuth device flow
├── .gitignore
└── CLAUDE.md
```

## Implementation Steps

1. **Scaffold project** — pyproject.toml, package structure, .gitignore
2. **Implement `catalog` command** — use yt-dlp Python API to extract playlist metadata, write CSV
3. **Implement `download` command** — read CSV, download each track as MP3 with yt-dlp
4. **Test with the Mr. Men playlist** — generate CSV, user validates, download first 2 tracks to verify
5. **Create CLAUDE.md** — document commands and project conventions

## Verification

```bash
pip install -e .
yoto-maker
# Select option 1, paste playlist URL, verify CSV output
# Edit CSV manually
# Run yoto-maker again, select option 2, provide CSV path and output dir
# Verify MP3 files exist with correct names
```
