# Yoto Maker

Download audio from a YouTube playlist as MP3 files. Designed for creating custom Yoto card content.

## How It Works

1. **Catalog** — Provide a YouTube playlist URL. The tool extracts track metadata into a CSV file.
2. **Validate** — Open the CSV, remove unwanted tracks, fix titles, reorder as needed. (Manual step.)
3. **Download** — Feed the validated CSV back in. The tool batch-downloads each track as an MP3.

## Prerequisites

- **Python 3.12+**
- **ffmpeg** — required by yt-dlp for audio conversion. Install via your package manager:
  - Windows: `scoop install ffmpeg` or `choco install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

## Installation

```bash
git clone https://github.com/kittenwhisky/yoto-maker.git
cd yoto-maker
pip install -e .
```

## Usage

Run the interactive menu:

```bash
yoto-maker
```

### Option 1: Catalog a YouTube playlist

```
Welcome to Yoto Card Maker!

What would you like to do?
> Catalog a YouTube playlist

Enter YouTube playlist URL: https://www.youtube.com/playlist?list=PL3LDD1...
Output CSV path [tracks.csv]: mr-men-tracks.csv

✓ Saved 52 tracks to mr-men-tracks.csv
```

### Option 2: Download tracks from a catalog

```
What would you like to do?
> Download tracks from a catalog

Path to catalog CSV: mr-men-tracks.csv
Output directory [./output]: ./mr-men-audiobooks

Downloading 50 tracks...
  [1/50] Mr. Happy ✓
  [2/50] Mr. Grumpy ✓
  ...
```

## CSV Format

The catalog CSV has three columns:

| Column | Description |
|--------|-------------|
| `track_number` | 1-indexed integer |
| `title` | Video title (becomes the MP3 filename) |
| `url` | Full YouTube video URL |

Edit this file between the catalog and download steps to remove unwanted tracks or fix titles.

## Tech Stack

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube metadata extraction and audio download
- [InquirerPy](https://github.com/kazhala/InquirerPy) — Interactive CLI prompts
- [ffmpeg](https://ffmpeg.org/) — Audio format conversion (used by yt-dlp)

## Future Roadmap

- Upload MP3s directly to Yoto as MYO card playlists via the [Yoto API](https://yoto.dev/api/)
