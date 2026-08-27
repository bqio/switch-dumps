import argparse
import html
import urllib.request
import xml.etree.ElementTree as ET


ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def get_magnet_from_feed(feed_url: str, topic_id: int) -> str | None:
    request = urllib.request.Request(
        feed_url,
        headers={
            "User-Agent": "Mozilla/5.0",
        },
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        content = response.read()

    root = ET.fromstring(content)

    target = f"/t/{topic_id}"

    for entry in root.findall("atom:entry", ATOM_NS):
        entry_id = entry.findtext("atom:id", namespaces=ATOM_NS)

        if not entry_id or not entry_id.endswith(target):
            continue

        for link in entry.findall("atom:link", ATOM_NS):
            if link.get("rel") == "enclosure":
                href = link.get("href")

                if href:
                    return html.unescape(href)

        return None

    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Get magnet link from an Atom feed."
    )

    parser.add_argument(
        "--feed-url",
        required=True,
        help="Atom feed URL",
    )

    parser.add_argument(
        "--topic-id",
        required=True,
        type=int,
        help="Topic ID",
    )

    args = parser.parse_args()

    magnet_link = get_magnet_from_feed(
        feed_url=args.feed_url,
        topic_id=args.topic_id,
    )

    if not magnet_link:
        parser.error(f"Magnet link not found for topic {args.topic_id}")

    with open("magnet.txt", "w", encoding="utf-8") as file:
        file.write(magnet_link)

    print(f"Magnet link for topic {args.topic_id} saved to magnet.txt")


if __name__ == "__main__":
    main()