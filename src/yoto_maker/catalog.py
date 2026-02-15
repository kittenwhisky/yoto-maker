"""Catalog module — extract YouTube playlist metadata into a CSV file."""

import csv

import yt_dlp


def generate_catalog(playlist_url: str, output_path: str) -> int:
    """Extract video titles and URLs from a YouTube playlist and save to CSV.

    Uses yt-dlp to fetch playlist metadata without downloading any media.

    Args:
        playlist_url: Full YouTube playlist URL.
        output_path: File path for the output CSV.

    Returns:
        Number of tracks written to the CSV.
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": "in_playlist",
        "js_runtimes": {"node": {}},
        "remote_components": {"ejs:github"},
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

    entries = info.get("entries", [])

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(["track_number", "title", "url"])

        for index, entry in enumerate(entries, start=1):
            video_url = entry.get("url") or entry.get("webpage_url", "")
            # Ensure the URL is a full YouTube URL
            if video_url and not video_url.startswith("http"):
                video_url = f"https://www.youtube.com/watch?v={video_url}"
            title = entry.get("title", "Untitled")
            writer.writerow([index, title, video_url])

    count = len(entries)
    print(f"\u2713 Saved {count} tracks to {output_path}")
    return count
