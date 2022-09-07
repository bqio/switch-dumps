import xml.etree.ElementTree as ET
import json
import argparse
from format import remove_thread_title_tags, remove_removed_threads

context = None
output = []

parser = argparse.ArgumentParser(description="Rutracker parser by bqio")

parser.add_argument("-f", dest="file", required=True, type=str, help="rutracker dump file")
parser.add_argument("-i", dest="forumid", required=True, type=int, help="rutracker forum id")
parser.add_argument("--remove-title-tags", dest="rtt", required=False, default=False, action='store_true', help="remove title tags")
parser.add_argument("--remove-removed-threads", dest="rrt", required=False, default=False, action='store_true', help="remove removed threads")

args = parser.parse_args()

for event, elem in ET.iterparse(args.file, events=("start", "end")):
  if event == "start":
    if elem.tag == "torrent" and context == None:
      context = elem
  if event == "end":
    if elem == context:
      forum_id = elem[2].attrib.get("id")
      if int(forum_id) == args.forumid:
        title = elem[0].text
        hash = elem[1].attrib.get("hash")
        output.append({
          "title": title,
          "hash": hash,
        })
        print(title)
      context = None
      elem.clear()
with open("f{}.json".format(args.forumid), "w") as f:
  if args.rrt:
    output = remove_removed_threads(output)
  if args.rtt:
    output = remove_thread_title_tags(output)
  json.dump(output, f)