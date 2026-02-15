"""CLI module — interactive menu entry point for yoto-maker."""

from InquirerPy import inquirer

from yoto_maker.catalog import generate_catalog
from yoto_maker.download import download_tracks


def main() -> None:
    """Launch the interactive yoto-maker menu."""
    print("\nWelcome to Yoto Card Maker!\n")

    action = inquirer.rawlist(
        message="What would you like to do?",
        choices=[
            {"name": "Catalog a YouTube playlist", "value": "catalog"},
            {"name": "Download tracks from a catalog", "value": "download"},
        ],
    ).execute()

    if action == "catalog":
        _catalog_flow()
    elif action == "download":
        _download_flow()


def _catalog_flow() -> None:
    """Prompt for playlist URL and output path, then generate the catalog CSV."""
    playlist_url = inquirer.text(
        message="Enter YouTube playlist URL:",
        validate=lambda val: len(val.strip()) > 0,
        invalid_message="URL cannot be empty.",
    ).execute()

    output_path = inquirer.text(
        message="Output CSV path:",
        default="tracks.csv",
    ).execute()

    generate_catalog(playlist_url.strip().strip("\"'"), output_path.strip().strip("\"'"))


def _download_flow() -> None:
    """Prompt for CSV path and output directory, then download tracks."""
    csv_path = inquirer.text(
        message="Path to catalog CSV:",
        validate=lambda val: len(val.strip()) > 0,
        invalid_message="CSV path cannot be empty.",
    ).execute()

    output_dir = inquirer.text(
        message="Output directory:",
        default="./output",
    ).execute()

    download_tracks(csv_path.strip().strip("\"'"), output_dir.strip().strip("\"'"))


if __name__ == "__main__":
    main()
