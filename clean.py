import argparse
import csv

INPUT_FILE = "playlist.csv"
OUTPUT_FILE = "playlist.txt"

COLUMNS = {
    "track_uri": ("Track URI", "-tu", "--track-uri"),
    "track": ("Track Name", "-t", "--track"),
    "artist_uri": ("Artist URI(s)", "-au", "--artist-uri"),
    "artist": ("Artist Name(s)", "-a", "--artist"),
    "album_uri": ("Album URI", "-alu", "--album-uri"),
    "album": ("Album Name", "-al", "--album"),
    "album_artist_uri": ("Album Artist URI(s)", "-aau", "--album-artist-uri"),
    "album_artist": ("Album Artist Name(s)", "-aa", "--album-artist"),
    "release_date": ("Album Release Date", "-r", "--release-date"),
    "image": ("Album Image URL", "-i", "--image"),
    "disc": ("Disc Number", "-d", "--disc"),
    "track_number": ("Track Number", "-tn", "--track-number"),
    "duration": ("Track Duration (ms)", "-du", "--duration"),
    "preview": ("Track Preview URL", "-p", "--preview"),
    "explicit": ("Explicit", "-e", "--explicit"),
    "popularity": ("Popularity", "-po", "--popularity"),
    "isrc": ("ISRC", "-is", "--isrc"),
    "added_by": ("Added By", "-ab", "--added-by"),
    "added_at": ("Added At", "-at", "--added-at"),
}


def main():
    parser = argparse.ArgumentParser(
        description="Clean and export Spotify playlist CSV data."
    )

    for key, (column, short, long) in COLUMNS.items():
        parser.add_argument(
            short,
            long,
            action="store_true",
            help=f"Show {column}"
        )

    parser.add_argument(
        "-all",
        "--all",
        action="store_true",
        help="Show every column"
    )

    args = parser.parse_args()

    # Check which options were selected
    selected = [
        key for key in COLUMNS
        if getattr(args, key)
    ]

    # Default behavior
    if not selected and not args.all:
        selected = ["track", "artist"]

    # --all / -all
    if args.all:
        selected = list(COLUMNS.keys())

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as csv_file:

        reader = csv.DictReader(csv_file)

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as txt_file:

            count = 0

            for row in reader:
                values = []

                for key in selected:
                    column = COLUMNS[key][0]
                    value = row[column].strip()
                    values.append(value)

                if any(values):
                    txt_file.write(" — ".join(values) + "\n")
                    count += 1

    print(
        f"Done! Exported {count} songs to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()