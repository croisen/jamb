from concurrent.futures import ProcessPoolExecutor
from typing import Any, Dict, Self
from urllib.parse import parse_qs, urlparse
import asyncio
import functools
import logging
import time

from yt_dlp import YoutubeDL


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

        # Welp the raw link expires too if I am still using yt
        self.expire = int(parse_qs(urlparse(self.url).query)["expire"][0])

    async def renew(self) -> Self:
        # Checking if it ain't enough to play the whole duration as well
        # since ffmpeg would error out with:
        # The specified session has been invalidated for some reason
        if time.time() >= (self.expire - self.duration):
            return await a_search(self.ffmpeg, self.web_url)
        else:
            return self


def search(ffmpeg: str, search_term: str) -> Video:
    vid = None
    params = {
        "default_search": "ytsearch1",
        "ffmpeg_location": ffmpeg,
        "format": "bestaudio",
        "logger": _logger,
        "noplaylist": True,
    }

    with YoutubeDL(params) as ydl:
        vid = ydl.sanitize_info(ydl.extract_info(search_term, download=False))
        if urlparse(search_term).scheme not in ("http", "https"):
            vid = ydl.sanitize_info(ydl.extract_info(search_term, download=False))["entries"][0]

        return Video(vid, ffmpeg)


async def a_search(ffmpeg: str, search_term: str) -> Video:
    loop = asyncio.get_running_loop()
    f = functools.partial(search, ffmpeg, search_term)
    with ProcessPoolExecutor() as exc:
        return await loop.run_in_executor(exc, f)
