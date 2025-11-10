import xml.etree.ElementTree as ET
import sys
import json
import poster
import datetime
import re
import logging

from typing import Iterator
from ignore import IGNORED_TOPIC_ID
from pathlib import Path

_LOG_FORMAT = "%(levelname)s :: %(message)s"
_POSTERS_DIR = Path("posters")


def iterparse(xml_path: str) -> Iterator[tuple[str, ET.Element]]:
    return ET.iterparse(xml_path, events=("start", "end"))


def to_tracker_url(id: int) -> str:
    if id == 1:
        return "http://bt.t-ru.org/ann?magnet"
    else:
        return f"http://bt{id}.t-ru.org/ann?magnet"


def dump(xml_path: str, forum_id: int, with_posters: bool = False) -> list[dict]:
    dest: list[dict] = []
    context = iterparse(xml_path)
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
                    topic_forum_id = forum_elem.attrib.get("id")
                    title = re.sub(r"\[.*?\]", "", title_elem.text).strip()
                    hash = torrent_elem.attrib.get("hash")
                    tracker = to_tracker_url(int(torrent_elem.attrib.get("tracker_id")))

                    if forum_id == int(topic_forum_id):
                        try:
                            _poster = poster.from_content(content_elem.text)
                            if with_posters:
                                _poster = poster.load_into_dir(
                                    hash, _poster, _POSTERS_DIR
                                )
                        except Exception as e:
                            logging.error(f"Error {topic_id}: {e}")
                            _poster = ""
                        entry = {
                            "title": title,
                            "hash": hash,
                            "tracker": tracker,
                            "poster": str(_poster),
                            "size": size,
                            "published_date": published_date,
                        }
                        dest.append(entry)
                        logging.info(f"Add {topic_id}: {entry}")
                else:
                    logging.info(f"Ignore {topic_id}")

            root.clear()
    return dest


def save_json(dest: list[dict], output_name: str) -> None:
    with open(f"{output_name}.json", "w", encoding="utf-8") as fp:
        json.dump(dest, fp)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} xml_path forum_id output_name")
        exit(0)
    logging.basicConfig(
        level=logging.INFO,
        filename="log.txt",
        filemode="w",
        encoding="utf-8",
        format=_LOG_FORMAT,
    )
    xml_path = sys.argv[1]
    forum_id = int(sys.argv[2])
    output_name = sys.argv[3]
    with_posters = len(sys.argv) == 5 and sys.argv[4] == "--with-posters"
    dump_data = dump(xml_path, forum_id, with_posters)
    save_json(dump_data, output_name)
