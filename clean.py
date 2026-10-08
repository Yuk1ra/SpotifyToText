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
    "album_artist_uri": (
        "Album Artist URI(s)",
        "-aau",
        "--album-artist-uri",
    ),
    "album_artist": (
        "Album Artist Name(s)",
        "-aa",
        "--album-artist",
    ),
    "release_date": (
        "Album Release Date",
        "-r",
        "--release-date",
    ),
    "image": ("Album Image URL", "-i", "--image"),
    "disc": ("Disc Number", "-d", "--disc"),
    "track_number": (
        "Track Number",
        "-tn",
        "--track-number",
    ),
    "duration": (
        "Track Duration (ms)",
        "-du",
        "--duration",
    ),
    "preview": (
        "Track Preview URL",
        "-p",
        "--preview",
    ),
    "explicit": ("Explicit", "-e", "--explicit"),
    "popularity": (
        "Popularity",
        "-po",
        "--popularity",
    ),
    "isrc": ("ISRC", "-is", "--isrc"),
    "added_by": ("Added By", "-ab", "--added-by"),
    "added_at": ("Added At", "-at", "--added-at"),
}


def normalize(value):
    """Return a case-insensitive value suitable for sorting."""
    return value.strip().casefold()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Clean and export Spotify playlist CSV data."
    )

    # Column options
    columns_group = parser.add_argument_group("Columns")

    for key, (column, short, long) in COLUMNS.items():
        columns_group.add_argument(
            short,
            long,
            action="store_true",
            help=f"Show {column}",
        )

    columns_group.add_argument(
        "-all",
        "--all",
        action="store_true",
        help="Show every column",
    )

    # Sort function
    parser.add_argument(
        "-s",
        "--sort",
        nargs="+",
        metavar="COLUMN",
        help=(
            "Sort by one or two columns. "
            "The first column is primary and the second is secondary."
        ),
    )

    # Amount function
    parser.add_argument(
        "-am",
        "--amount",
        nargs=2,
        metavar=("POSITION", "NUMBER"),
        help=(
            "Select an amount of songs. "
            "POSITION must be 'first' or 'last'."
        ),
    )

    return parser


def get_selected_columns(args):
    """Determine which columns should appear in the output."""

    if args.all:
        return list(COLUMNS.keys())

    selected = [
        key
        for key in COLUMNS
        if getattr(args, key)
    ]

    # Original behavior
    if not selected:
        return ["track", "artist"]

    return selected


def get_sort_columns(args):
    """Validate and return requested sort columns."""

    if not args.sort:
        return []

    if len(args.sort) > 2:
        raise ValueError(
            "Sort accepts a maximum of two columns."
        )

    valid_columns = set(COLUMNS.keys())

    # Allow long names and a few natural aliases.
    aliases = {
        "track-uri": "track_uri",
        "track": "track",
        "artist-uri": "artist_uri",
        "artist": "artist",
        "album-uri": "album_uri",
        "album": "album",
        "album-artist-uri": "album_artist_uri",
        "album-artist": "album_artist",
        "release-date": "release_date",
        "image": "image",
        "disc": "disc",
        "track-number": "track_number",
        "duration": "duration",
        "preview": "preview",
        "explicit": "explicit",
        "popularity": "popularity",
        "isrc": "isrc",
        "added-by": "added_by",
        "added-at": "added_at",
    }

    result = []

    for column in args.sort:
        key = aliases.get(column)

        if key is None or key not in valid_columns:
            raise ValueError(
                f"Invalid sort column: '{column}'"
            )

        result.append(key)

    return result


def get_amount(args):
    """Validate and return amount settings."""

    if not args.amount:
        return None

    position, number = args.amount

    position = position.lower()

    if position not in ("first", "last"):
        raise ValueError(
            "Amount position must be 'first' or 'last'."
        )

    try:
        number = int(number)
    except ValueError:
        raise ValueError(
            "Amount must be a whole number."
        )

    if number < 0:
        raise ValueError(
            "Amount cannot be negative."
        )

    return position, number


def sort_rows(rows, sort_columns):
    """Sort rows using primary and optional secondary columns."""

    if not sort_columns:
        return rows

    # Stable sorting lets us apply the secondary key first,
    # then the primary key.
    for column in reversed(sort_columns):
        csv_column = COLUMNS[column][0]

        rows.sort(
            key=lambda row: normalize(row[csv_column])
        )

    return rows


def apply_amount(rows, amount):
    """Take the requested first or last number of rows."""

    if amount is None:
        return rows

    position, number = amount

    if position == "first":
        return rows[:number]

    return rows[-number:] if number else []


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        selected_columns = get_selected_columns(args)
        sort_columns = get_sort_columns(args)
        amount = get_amount(args)

    except ValueError as error:
        parser.error(str(error))

    # ---------------------------------------------------------
    # 1. Read CSV
    # ---------------------------------------------------------

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:

        reader = csv.DictReader(csv_file)
        rows = list(reader)

    # ---------------------------------------------------------
    # 2. Sort
    # ---------------------------------------------------------

    rows = sort_rows(rows, sort_columns)

    # ---------------------------------------------------------
    # 3. Amount
    # ---------------------------------------------------------

    rows = apply_amount(rows, amount)

    # ---------------------------------------------------------
    # 4. Write output
    # ---------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as txt_file:

        count = 0

        for row in rows:
            values = []

            for key in selected_columns:
                csv_column = COLUMNS[key][0]
                value = row[csv_column].strip()
                values.append(value)

            if any(values):
                txt_file.write(
                    " — ".join(values) + "\n"
                )
                count += 1

    print(
        f"Done! Exported {count} songs to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
