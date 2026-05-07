# switch-dumps

![Github All Releases](https://img.shields.io/github/downloads/bqio/switch-dumps/total.svg)

Nintendo Switch rutracker forum dump

## Schema

```python
class Entry:
    title: str # Game title
    magnetURI: str # Magnet uri
    poster: str # Poster URL
    size: int # Size (in bytes)
    published_date: int # Unix epoch
    screenshots: list[str] # Screenshots links (if available)
```

## Usage

```bash
usage: dump.py [-h] [--posters] [--screenshots] xml_path forum_id output

Nintendo Switch rutracker forum dumper script, by bqio

positional arguments:
  xml_path           path to the XML dump file (Path)
  forum_id           rutracker forum id (int)
  output             output json file path (Path)

options:
  -h, --help         show this help message and exit
  --posters, -p      download posters locally (bool)
  --screenshots, -s  add screenshots (if available) to the json dump (bool)
```

## API

https://api.github.com/repos/bqio/switch-dumps/releases/latest

## Thanks

https://rutracker.org/forum/viewtopic.php?t=5591249
