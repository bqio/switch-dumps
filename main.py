import xml.etree.ElementTree as ET
import json
import argparse

context = None
output = []

parser = argparse.ArgumentParser(description="Rutracker parser by bqio")

parser.add_argument("-f", dest="file", required=True, type=str, help="rutracker dump file")
parser.add_argument("-i", dest="forumid", required=True, type=int, help="rutracker forum id")

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
  json.dump(output, f)