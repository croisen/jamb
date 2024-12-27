from typing import Any, Dict, Self
from urllib.parse import parse_qs, urlparse
import logging
import time

from yt_dlp import YoutubeDL

from utils.to_thread import to_thread


_logger = logging.getLogger(__name__)


class Video:
    def __init__(self, yt_res: Dict[str, Any], ffmpeg: str) -> Self:
        self.url = yt_res["url"]
        self.web_url = yt_res["webpage_url"]
        self.thumbnail = yt_res["thumbnail"]
        self.ffmpeg = ffmpeg

        self.title = yt_res["title"]
        self.uploader_url = yt_res["uploader_url"]
        self.description = yt_res["description"]
        self.uploader = yt_res["uploader"]
        self.duration = yt_res["duration"]
        self.duration_str = yt_res["duration_string"]

        # Welp the raw link expires too
        self.expire = int(parse_qs(urlparse(self.url).query)["expire"][0])

    async def renew(self) -> Self:
        if self.expire <= time.time():
            return await search(self.ffmpeg, self.web_url)
        else:
            return self


@to_thread
def search(ffmpeg: str, search: str) -> Video:
    vid = None
    params = {
        "ffmpeg_location": ffmpeg,
        "format": "opus/bestaudio",
        "logger": _logger,
        "noplaylist": "True",
    }

    with YoutubeDL(params) as ydl:
        if urlparse(search).scheme in ("http", "https"):
            vid = ydl.extract_info(search, download=False)["entries"][0]
        else:
            vid = ydl.extract_info(f"ytsearch:{search}", download=False)["entries"][0]

        return Video(vid, ffmpeg)
