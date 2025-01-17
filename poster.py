import re

IMG_REGEXP = r"\[img=right\](https?://\S+\.(?:png|jpe?g))\[/img\]"


def from_content(content: str) -> str:
    return re.findall(IMG_REGEXP, content, re.IGNORECASE)[0]
