import re

IMG_REGEXP = r"\[img.*\](.*)\["


def from_content(content: str) -> str:
    return re.findall(IMG_REGEXP, content, re.IGNORECASE)[0]
