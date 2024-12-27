import xml.etree.ElementTree as ET
import sys
import json
import poster

from typing import Iterator


def iterparse(xml_path: str) -> Iterator[tuple[str, ET.Element]]:
    return ET.iterparse(xml_path, events=("start", "end"))


def to_tracker_url(id: int) -> str:
    if id == 1:
        return "http://bt.t-ru.org/ann?magnet"
    else:
        return f"http://bt{id}.t-ru.org/ann?magnet"


if len(sys.argv) != 3:
    print("Usage: main.py xml_path forum_id")
    exit(0)

dest = []
context = iterparse(sys.argv[1])
context = iter(context)

event, root = context.__next__()

for event, elem in context:
    if event == "end" and elem.tag == "torrent":
        title_elem = elem.find("title")
        forum_elem = elem.find("forum")
        torrent_elem = elem.find("torrent")
        del_elem = elem.find("del")
        content_elem = elem.find("content")

        if (
            title_elem != None
            and forum_elem != None
            and torrent_elem != None
            and del_elem == None
        ):
            forum_id = forum_elem.attrib.get("id")
            title = title_elem.text
            hash = torrent_elem.attrib.get("hash")
            tracker = to_tracker_url(int(torrent_elem.attrib.get("tracker_id")))

            if forum_id == sys.argv[2]:
                entry = {
                    "title": title,
                    "hash": hash,
                    "tracker": tracker,
                    "poster": poster.from_content(content_elem.text),
                }
                dest.append(entry)
                print(entry)

        root.clear()

with open(f"forum_{sys.argv[2]}.json", "w", encoding="utf-8") as fp:
    json.dump(dest, fp)
