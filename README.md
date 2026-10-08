# Playlist Cleaner

A small Python utility for converting a Spotify playlist CSV export into a readable `.txt` file.

By default, it converts each song into:

```text
Track Name — Artist Name(s)
```

You can select specific columns, sort the playlist, limit the number of songs, or combine all of these operations.

## Requirements

* Python 3
* No external dependencies

## Usage

Place your Spotify playlist export in the same directory as the script and name it:

```text
playlist.csv
```

Then run:

```bash
python clean.py
```

The output is written to:

```text
playlist.txt
```

## Processing Order

The script always processes the playlist in this order:

```text
CSV
 ↓
Columns
 ↓
Sort
 ↓
Amount
 ↓
Output
```

This means `--amount` is applied **after** sorting.

For example:

```bash
python clean.py --sort artist --amount first 10
```

sorts the entire playlist by artist first, then keeps the first 10 songs from that sorted result.

The order in which functions are written in the command does not matter.

## Default Behavior

Running the script without any arguments exports the track name and artist name:

```bash
python clean.py
```

Output:

```text
Track Name — Artist Name(s)
```

## Options

### Columns

| Short  | Full                 | Description               |
| ------ | -------------------- | ------------------------- |
| `-tu`  | `--track-uri`        | Show Track URI            |
| `-t`   | `--track`            | Show Track Name           |
| `-au`  | `--artist-uri`       | Show Artist URI(s)        |
| `-a`   | `--artist`           | Show Artist Name(s)       |
| `-alu` | `--album-uri`        | Show Album URI            |
| `-al`  | `--album`            | Show Album Name           |
| `-aau` | `--album-artist-uri` | Show Album Artist URI(s)  |
| `-aa`  | `--album-artist`     | Show Album Artist Name(s) |
| `-r`   | `--release-date`     | Show Album Release Date   |
| `-i`   | `--image`            | Show Album Image URL      |
| `-d`   | `--disc`             | Show Disc Number          |
| `-tn`  | `--track-number`     | Show Track Number         |
| `-du`  | `--duration`         | Show Track Duration (ms)  |
| `-p`   | `--preview`          | Show Track Preview URL    |
| `-e`   | `--explicit`         | Show Explicit             |
| `-po`  | `--popularity`       | Show Popularity           |
| `-is`  | `--isrc`             | Show ISRC                 |
| `-ab`  | `--added-by`         | Show Added By             |
| `-at`  | `--added-at`         | Show Added At             |
| `-all` | `--all`              | Show every column         |

### Sorting

```text
-s, --sort COLUMN [COLUMN ...]
```

Sort by one or two columns.

The first column is the primary sort key. The second column is the secondary sort key.

Examples:

```bash
python clean.py --sort artist
```

Sort by artist.

```bash
python clean.py --sort artist track
```

Sort by artist first, then track name.

Available sort columns:

```text
track-uri
track
artist-uri
artist
album-uri
album
album-artist-uri
album-artist
release-date
image
disc
track-number
duration
preview
explicit
popularity
isrc
added-by
added-at
```

Sorting is case-insensitive.

### Amount

```text
-am, --amount POSITION NUMBER
```

Select a number of songs from the processed playlist.

`POSITION` can be:

* `first`
* `last`

Examples:

```bash
python clean.py --amount first 10
```

Keep the first 10 songs.

```bash
python clean.py --amount last 20
```

Keep the last 20 songs.

When combined with sorting, the amount is applied after sorting:

```bash
python clean.py --sort popularity --amount first 10
```

This sorts the entire playlist by popularity and then keeps the first 10 songs.

## Examples

### Track and Artist

```bash
python clean.py -t -a
```

or:

```bash
python clean.py --track --artist
```

Output:

```text
Song Name — Artist Name
Another Song — Another Artist
```

### Track, Artist, and Album

```bash
python clean.py -t -a -al
```

or:

```bash
python clean.py --track --artist --album
```

Output:

```text
Song Name — Artist Name — Album Name
```

### Sort by Artist

```bash
python clean.py --track --artist --sort artist
```

### Sort by Artist and Track

```bash
python clean.py --track --artist --sort artist track
```

### First 20 Songs by Artist

```bash
python clean.py --track --artist --sort artist --amount first 20
```

### Last 20 Songs by Popularity

```bash
python clean.py --track --artist --sort popularity --amount last 20
```

### Everything

```bash
python clean.py --all
```

or:

```bash
python clean.py -all
```

### Combined Functions

Functions can be written in any order.

For example, these are equivalent:

```bash
python clean.py --track --artist --sort artist --amount first 20
```

```bash
python clean.py --amount first 20 --sort artist --artist --track
```

```bash
python clean.py --sort artist --amount first 20 --artist --track
```

All three follow the same internal processing order:

```text
Columns → Sort → Amount → Output
```

## Help

Run:

```bash
python clean.py --help
```

The complete help output is:

```text
usage: clean.py [-h] [-tu] [-t] [-au] [-a] [-alu] [-al] [-aau] [-aa]
                [-r] [-i] [-d] [-tn] [-du] [-p] [-e] [-po] [-is] [-ab]
                [-at] [-all] [-s COLUMN [COLUMN ...]]
                [-am POSITION NUMBER]

Clean and export Spotify playlist CSV data.

options:
  -h, --help            show this help message and exit
  -s COLUMN [COLUMN ...], --sort COLUMN [COLUMN ...]
                        Sort by one or two columns. The first column is
                        primary and the second is secondary.
  -am POSITION NUMBER, --amount POSITION NUMBER
                        Select an amount of songs. POSITION must be 'first'
                        or 'last'.

Columns:
  -tu, --track-uri      Show Track URI
  -t, --track           Show Track Name
  -au, --artist-uri     Show Artist URI(s)
  -a, --artist          Show Artist Name(s)
  -alu, --album-uri     Show Album URI
  -al, --album          Show Album Name
  -aau, --album-artist-uri
                        Show Album Artist URI(s)
  -aa, --album-artist   Show Album Artist Name(s)
  -r, --release-date    Show Album Release Date
  -i, --image           Show Album Image URL
  -d, --disc            Show Disc Number
  -tn, --track-number   Show Track Number
  -du, --duration       Show Track Duration (ms)
  -p, --preview         Show Track Preview URL
  -e, --explicit        Show Explicit
  -po, --popularity     Show Popularity
  -is, --isrc           Show ISRC
  -ab, --added-by       Show Added By
  -at, --added-at       Show Added At
  -all, --all           Show every column
```

## Files

The script expects:

```text
playlist.csv
```

and generates:

```text
playlist.txt
```

These files are excluded from Git because the CSV contains personal playlist data and the TXT file is generated output.

## License

Use, modify, and adapt it however you want.