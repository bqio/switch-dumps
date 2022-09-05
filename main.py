import xml.etree.ElementTree as ET
import json

FORUM_ID = 1605

context = None
output = []

for event, elem in ET.iterparse("rutracker-20220528.xml", events=("start", "end")):
  if event == "start":
    if elem.tag == "torrent" and context == None:
      context = elem
  if event == "end":
    if elem == context:
      forum_id = elem[2].attrib.get("id")
      if int(forum_id) == FORUM_ID:
        title = elem[0].text
        hash = elem[1].attrib.get("hash")
        output.append({
          "title": title,
          "hash": hash,
        })
      context = None
      elem.clear()
      #files = []
      #for file in elem.iter("file"):
        #files.append(file.attrib.get("name"))
with open("data.json", "w") as f:
  json.dump(output, f)