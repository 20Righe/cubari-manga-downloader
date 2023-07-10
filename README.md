# Cubari Manga Downloader

This script allows you to download manga from Cubari, a website that was popular as an alternative when MangaDex was down. While Cubari may not be actively used anymore, the content uploaded there may still be accessible, making this script potentially useful.

The script provides two main commands:
1. List available chapters of a manga.
2. Download selected chapters of a manga.

## Usage
`cubari-manga-downloader.py [link] [--chapters-list] [--chapters CHAPTERS [CHAPTERS ...]]`

### Positional Arguments
- `link`: Manga page link.

### Optional Arguments
- `-h, --help`: Show the help message and exit.
- `--chapters-list, --C`: List available chapters.
- `--chapters CHAPTERS [CHAPTERS ...], -c CHAPTERS [CHAPTERS ...]`: Specify chapters to download. If omitted, all chapters will be downloaded.

## Examples
**List available chapters of a manga:**

`cubari-manga-downloader.py [link] --C`

**Download specific chapters of a manga:**

`cubari-manga-downloader.py [link] --c 1 2 n`

Please note that the `[link]` placeholder should be replaced with the actual manga page link when running the commands.
