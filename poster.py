import re
from pathlib import Path
import urllib.request
import logging

IMG_REGEXP = r"\[img=right\](https?://\S+\.(?:png|jpe?g))\[/img\]"


def from_content(content: str) -> str:
    return re.findall(IMG_REGEXP, content, re.IGNORECASE)[0]


def load_into_dir(hash: str, url: str, dir: Path | str) -> Path:
    url_p = Path(url)
    ext = url_p.suffix
    dir = Path(dir)
    dir.mkdir(exist_ok=True)
    try:
        local = dir / f"{hash}{ext}"
        if local.exists():
            return local
        urllib.request.urlretrieve(url, local)
        logging.info(f"Image downloaded successfully to {local}")
        return local
    except Exception as e:
        logging.info(f"Error downloading image: {e}")
