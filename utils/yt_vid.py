from typing import Any, Dict, Self
from urllib.parse import parse_qs, urlparse
import logging
import time

from yt_dlp import YoutubeDL


_logger = logging.getLogger(__name__)


class Video:
    def __init__(self, yt_res: Dict[str, Any]) -> Self:
        self.url = yt_res["url"]
        self.web_url = yt_res["webpage_url"]
        self.thumbnail = yt_res["thumbnail"]

        self.title = yt_res["title"]
        self.uploader_url = yt_res["uploader_url"]
        self.uploader = yt_res["uploader"]
        self.duration = yt_res["duration"]
        self.duration_str = yt_res["duration_string"]

        # Welp the raw link expires too
        self.expire = int(parse_qs(urlparse(self.url).query)["expire"][0])

    async def renew(self) -> Self:
        if self.expire <= time.time():
            return await search(self.web_url)
        else:
            return self


async def search(search: str) -> Video:
    vid = None
    with YoutubeDL(
        {"format": "bestaudio", "noplaylist": "True", "logger": _logger}
    ) as ydl:
        if urlparse(search).scheme in ("http", "https"):
            vid = ydl.extract_info(f"ytsearch:{search}", download=False)["entries"][0]
        else:
            vid = ydl.extract_info(f"ytsearch:{search}", download=False)["entries"][0]

        return Video(vid)
