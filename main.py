import xml.etree.ElementTree as ET
import sys
import json
import poster
import datetime
import re
import logging

from typing import Iterator
from ignore import IGNORED_TOPIC_ID

_LOG_FORMAT = "%(levelname)s :: %(message)s"

logging.basicConfig(
    level=logging.INFO,
    filename="log.txt",
    filemode="w",
    encoding="utf-8",
    format=_LOG_FORMAT,
)


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
            topic_id = int(elem.attrib.get("id"))
            if topic_id not in IGNORED_TOPIC_ID:
                size = int(elem.attrib.get("size"))
                published_date = int(
                    datetime.datetime.strptime(
                        elem.attrib.get("registred_at"), "%Y.%m.%d %H:%M:%S"
                    ).timestamp()
                )
                forum_id = forum_elem.attrib.get("id")
                title = re.sub(r"\[.*?\]", "", title_elem.text).strip()
                hash = torrent_elem.attrib.get("hash")
                tracker = to_tracker_url(int(torrent_elem.attrib.get("tracker_id")))

                if forum_id == sys.argv[2]:
                    try:
                        _poster = poster.from_content(content_elem.text)
                    except Exception as e:
                        logging.error(f"Error {topic_id}: {e}")
                        _poster = ""
                    entry = {
                        "title": title,
                        "hash": hash,
                        "tracker": tracker,
                        "poster": _poster,
                        "size": size,
                        "published_date": published_date,
                    }
                    dest.append(entry)
                    logging.info(f"Add {topic_id}: {entry}")
            else:
                logging.info(f"Ignore {topic_id}")

        root.clear()

with open(f"forum_{sys.argv[2]}.json", "w", encoding="utf-8") as fp:
    json.dump(dest, fp)
