# Playlist Cleaner

A small Python utility for converting a Spotify playlist CSV export into a readable `.txt` file.

## Requirements

* Python 3

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

## Default Behavior

Running the script without any arguments exports the track name and artist name:

```text
Track Name — Artist Name(s)
```

Example:

```bash
python clean.py
```

## Options

Every column can be selected using either a short flag or its full name.

| Short  | Full                 | Description          |
| ------ | -------------------- | -------------------- |
| `-tu`  | `--track-uri`        | Track URI            |
| `-t`   | `--track`            | Track Name           |
| `-au`  | `--artist-uri`       | Artist URI(s)        |
| `-a`   | `--artist`           | Artist Name(s)       |
| `-alu` | `--album-uri`        | Album URI            |
| `-al`  | `--album`            | Album Name           |
| `-aau` | `--album-artist-uri` | Album Artist URI(s)  |
| `-aa`  | `--album-artist`     | Album Artist Name(s) |
| `-r`   | `--release-date`     | Album Release Date   |
| `-i`   | `--image`            | Album Image URL      |
| `-d`   | `--disc`             | Disc Number          |
| `-tn`  | `--track-number`     | Track Number         |
| `-du`  | `--duration`         | Track Duration (ms)  |
| `-p`   | `--preview`          | Track Preview URL    |
| `-e`   | `--explicit`         | Explicit             |
| `-po`  | `--popularity`       | Popularity           |
| `-is`  | `--isrc`             | ISRC                 |
| `-ab`  | `--added-by`         | Added By             |
| `-at`  | `--added-at`         | Added At             |
| `-all` | `--all`              | Show every column    |

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

### Select Other Columns

```bash
python clean.py --duration --popularity
```

Output:

```text
243000 — 85
198000 — 72
```

### Everything

```bash
python clean.py --all
```

or:

```bash
python clean.py -all
```

This exports every column from the Spotify CSV.

### Help

```bash
python clean.py --help
```

This displays all available options and their descriptions.

## Column Order

When multiple options are selected, the output follows the original Spotify CSV column order rather than the order in which the flags were entered.

For example:

```bash
python clean.py --album --artist --track
```

still produces:

```text
Track Name — Artist Name(s) — Album Name
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

## License

Use, modify, and adapt it however you want.
