# switch-dumps

![Github All Releases](https://img.shields.io/github/downloads/bqio/switch-dumps/total.svg)

Nintendo Switch rutracker forum dump

## Schema

```python
class Entry:
    title: str # Game title
    hash: str # Magnet hash
    tracker: str # Tracker URL
    poster: str # Poster URL
    size: int # Size (in bytes)
    published_date: int # Unix epoch
```

## Run

```bash
py main.py rutracker.xml 1605
```

## API

https://api.github.com/repos/bqio/switch-dumps/releases/latest

## Thanks

https://rutracker.org/forum/viewtopic.php?t=5591249
