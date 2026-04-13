import re
import random
import os

IMG_REGEXP = r"\[URL=(.*?)\]\[IMG\](.*?)\[/IMG\]\[/URL\]"


def fastpic_thumb_to_big(url: str, img: str) -> str | None:
    if ".html" in url:
        url = url[:-5]
    if "_" in url:
        return None
    extension = os.path.splitext(url)[1]
    dist = img.replace("thumb", "big").replace(".jpeg", extension)
    return dist


def from_content(content: str):
    matches = re.findall(IMG_REGEXP, content)
    urls = []
    for url, img in matches:
        screenshot = fastpic_thumb_to_big(url, img)
        if screenshot:
            urls.append(screenshot)
    return random.sample(urls[1:], min(3, len(urls) - 1)) if len(urls) > 1 else []
