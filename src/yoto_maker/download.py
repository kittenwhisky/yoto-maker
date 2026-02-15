"""Batch download tracks from a validated CSV catalog as MP3 files."""

import csv
import os

import yt_dlp


def download_tracks(csv_path: str, output_dir: str) -> None:
    """Download all tracks listed in a CSV catalog as MP3 files.

    Reads the CSV (columns: track_number, title, url), downloads audio for each
    row via yt-dlp, converts to MP3 using ffmpeg, and saves as {title}.mp3 in
    the output directory. Individual failures are printed and skipped.

    Args:
        csv_path: Path to the validated CSV catalog file.
        output_dir: Directory where MP3 files will be saved (created if needed).
    """
    os.makedirs(output_dir, exist_ok=True)

    tracks = _read_catalog(csv_path)
    total = len(tracks)

    print(f"Downloading {total} tracks...")

    for i, track in enumerate(tracks, start=1):
        title = track["title"]
        url = track["url"]

        try:
            _download_single(url, title, output_dir)
            print(f"  [{i}/{total}] {title} \u2713")
        except Exception as exc:
            print(f"  [{i}/{total}] {title} \u2717 {exc}")


def _read_catalog(csv_path: str) -> list[dict[str, str]]:
    """Read the CSV catalog and return a list of track dicts.

    Args:
        csv_path: Path to CSV with columns track_number, title, url.

    Returns:
        List of dicts with keys: track_number, title, url.
    """
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        tracks = list(reader)

    if not tracks:
        raise SystemExit(f"No tracks found in {csv_path}")

    required = {"title", "url"}
    actual = set(tracks[0].keys())
    missing = required - actual
    if missing:
        raise SystemExit(
            f"CSV is missing columns: {missing}. Found columns: {sorted(actual)}"
        )

    return tracks


def _download_single(url: str, title: str, output_dir: str) -> None:
    """Download a single track as MP3.

    Args:
        url: YouTube video URL.
        title: Track title used for the output filename.
        output_dir: Directory where the MP3 will be saved.
    """
    outtmpl = os.path.join(output_dir, f"{title}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
        "js_runtimes": {"node": {}},
        "remote_components": {"ejs:github"},
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
