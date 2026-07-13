import sys
import xml.etree.ElementTree as ET
import argparse
import json
import poster
import datetime
import re
import logging
import screens

from typing import Iterator, BinaryIO, TextIO
from ignore import IGNORED_TOPIC_ID
from pathlib import Path

_LOG_FORMAT = "%(levelname)s :: %(message)s"
_POSTERS_DIR = Path("posters")


def iterparse(xml_source: str | BinaryIO) -> Iterator[tuple[str, ET.Element]]:
    return ET.iterparse(xml_source, events=("start", "end"))


def to_tracker_url(id: int) -> str:
    if id == 1:
        return "http://bt.t-ru.org/ann?magnet"
    else:
        return f"http://bt{id}.t-ru.org/ann?magnet"


def make_magnet_uri(info_hash: str, tracker: str) -> str:
    return f"magnet:?xt=urn:btih:{info_hash}&tr={tracker}"


def dump(
    xml_source: str | BinaryIO,
    forum_id: int,
    with_posters: bool,
    with_screenshots: bool,
    out_fp: TextIO,
) -> None:
    context = iterparse(xml_source)
    context = iter(context)
    event, root = context.__next__()

    out_fp.write("[\n")
    is_first = True

    for event, elem in context:
        if event == "end" and elem.tag == "torrent":
            title_elem = elem.find("title")
            forum_elem = elem.find("forum")
            torrent_elem = elem.find("torrent")
            del_elem = elem.find("del")
            content_elem = elem.find("content")

            if (
                title_elem is not None
                and forum_elem is not None
                and torrent_elem is not None
                and content_elem is not None
                and del_elem is None
            ):
                # check topic id
                topic_id = elem.attrib.get("id")
                if topic_id is None:
                    raise ValueError("elem.attrib.id is None")
                topic_id = int(topic_id)

                if topic_id not in IGNORED_TOPIC_ID:
                    # check torrent size
                    size = elem.attrib.get("size")
                    if size is None:
                        raise ValueError("elem.attrib.size is None")
                    size = int(size)

                    # check topic registred_at
                    registred_at = elem.attrib.get("registred_at")
                    if registred_at is None:
                        raise ValueError("elem.attrib.registred_at is None")
                    published_date = int(
                        datetime.datetime.strptime(
                            registred_at, "%Y.%m.%d %H:%M:%S"
                        ).timestamp()
                    )

                    # check forum id
                    _forum_id = forum_elem.attrib.get("id")
                    if _forum_id is None:
                        raise ValueError("forum_elem.attrib.id is None")
                    _forum_id = int(_forum_id)

                    # check topic title text
                    title_text = title_elem.text
                    if title_text is None:
                        raise ValueError("title_elem.text is None")
                    title_text = re.sub(r"\[.*?\]", "", title_text).strip()

                    # check torrent hash
                    torrent_hash = torrent_elem.attrib.get("hash")
                    if torrent_hash is None:
                        raise ValueError("torrent_elem.attrib.hash is None")

                    # check torrent tracker id
                    tracker_id = torrent_elem.attrib.get("tracker_id")
                    if tracker_id is None:
                        raise ValueError("torrent_elem.attrib.tracker_id is None")
                    tracker_id = int(tracker_id)
                    tracker = to_tracker_url(tracker_id)

                    if forum_id == _forum_id:
                        _poster = ""
                        try:
                            # check topic content text
                            content_text = content_elem.text
                            if content_text is None:
                                raise ValueError("content_elem.text is None")

                            # check topic poster
                            _poster = poster.from_content(content_text)
                            screenshots = []
                            if with_screenshots:
                                screenshots = screens.from_content(content_text)
                            if with_posters:
                                _poster = poster.load_into_dir(
                                    torrent_hash, _poster, _POSTERS_DIR
                                )
                        except Exception as e:
                            logging.error(f"Error {topic_id}: {e}")

                        entry = {
                            "title": title_text,
                            "magnetURI": make_magnet_uri(torrent_hash, tracker),
                            "poster": _poster,
                            "size": size,
                            "published_date": published_date,
                            "screenshots": screenshots,
                        }

                        if not is_first:
                            out_fp.write(",\n")
                        is_first = False
                        json.dump(entry, out_fp, ensure_ascii=False)

                        logging.info(f"Add {topic_id}: {entry}")
                else:
                    logging.info(f"Ignore {topic_id}")

            root.clear()

    out_fp.write("\n]\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Nintendo Switch rutracker forum dumper script, by bqio"
    )

    parser.add_argument(
        "xml_path", type=str, help="path to the XML dump file or '-' for stdin"
    )
    parser.add_argument("forum_id", type=int, help="rutracker forum id (int)")
    parser.add_argument("output", type=Path, help="output json file path (Path)")

    parser.add_argument(
        "--posters", "-p", action="store_true", help="download posters locally (bool)"
    )
    parser.add_argument(
        "--screenshots",
        "-s",
        action="store_true",
        help="add screenshots (if available) to the json dump (bool)",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        filename="log.txt",
        filemode="w",
        encoding="utf-8",
        format=_LOG_FORMAT,
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(_LOG_FORMAT)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    logging.info("Script starting...")

    if args.xml_path == "-":
        xml_source = sys.stdin.buffer
        logging.info("Reading XML from stdin stream...")
    else:
        xml_source = args.xml_path
        logging.info(f"Reading XML from file: {xml_source}")

    with open(args.output, "w", encoding="utf-8") as out_fp:
        dump(xml_source, args.forum_id, args.posters, args.screenshots, out_fp)

    logging.info("Script finished successfully.")
