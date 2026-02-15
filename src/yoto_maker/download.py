"""Batch download tracks from a validated CSV catalog as MP3 files."""

import csv
import glob
import os

import yt_dlp


def download_tracks(csv_path: str, output_dir: str) -> None:
    """Download all tracks listed in a CSV catalog as MP3 files.

    Reads the CSV (columns: track_number, title, url), downloads audio for each
    row via yt-dlp, converts to MP3 using ffmpeg, and saves as {title}.mp3 in
    the output directory. Individual failures are printed and skipped.

    After all tracks are attempted, prints an error report and writes an error
    CSV containing only the failed rows.

    Args:
        csv_path: Path to the validated CSV catalog file.
        output_dir: Directory where MP3 files will be saved (created if needed).
    """
    os.makedirs(output_dir, exist_ok=True)

    tracks = _read_catalog(csv_path)
    total = len(tracks)
    failures = []

    print(f"Downloading {total} tracks...")

    for i, track in enumerate(tracks, start=1):
        title = track["title"]
        url = track["url"]

        try:
            _download_single(url, title, output_dir)
            print(f"  [{i}/{total}] {title} \u2713")
        except Exception as exc:
            print(f"  [{i}/{total}] {title} \u2717 {exc}")
            _cleanup_partial_files(output_dir, title)
            failures.append((track, str(exc)))

    if failures:
        _print_error_report(failures, total)
        _write_error_csv(csv_path, failures)
    else:
        print(f"\nAll {total} tracks downloaded successfully!")


def _cleanup_partial_files(output_dir: str, title: str) -> None:
    """Remove any leftover partial/temp files for a failed download."""
    pattern = os.path.join(output_dir, glob.escape(title) + ".*")
    for path in glob.glob(pattern):
        if not path.endswith(".mp3"):
            try:
                os.remove(path)
            except OSError:
                pass


def _print_error_report(failures: list[tuple[dict, str]], total: int) -> None:
    """Print a summary of failed downloads to the terminal."""
    print(f"\n--- Error Report ---")
    print(f"{len(failures)} of {total} tracks failed:\n")
    for track, error in failures:
        print(f"  {track['title']}")
        print(f"    URL:   {track['url']}")
        print(f"    Error: {error}\n")


def _write_error_csv(
    original_csv_path: str, failures: list[tuple[dict, str]]
) -> None:
    """Write a CSV containing only the failed tracks.

    The file is saved next to the original CSV with ' - error report' appended
    to the stem.
    """
    stem, _ = os.path.splitext(original_csv_path)
    error_csv_path = f"{stem} - error report.csv"

    fieldnames = list(failures[0][0].keys())

    with open(error_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for track, _ in failures:
            writer.writerow(track)

    print(f"Error CSV saved to: {error_csv_path}")


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
