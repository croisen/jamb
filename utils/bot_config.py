from typing import Any, Dict, Optional
from pathlib import Path
import asyncio
import json
import logging

from discord import Intents, Status, FFmpegOpusAudio
from discord.ext.commands import AutoShardedBot


class CroiBot(AutoShardedBot):
    mloop: asyncio.Task

    def __init__(self, config_file: Path, ffmpeg_path: Path):
        self.config: Optional[Dict[str, Any]] = None
        self.config_file: Path = config_file
        self.get_config(self.config_file)

        self.logger = logging.getLogger(__name__ + "(Bot Instance)")
        self.ffmpeg: Path = ffmpeg_path

        super().__init__(
            command_prefix=self.config["command-prefix"],
            case_insensitive=True,
            status=Status.idle,
            strip_after_prefix=True,
            help_command=None,
            intents=Intents.all(),
        )

    def get_config(self, config_file: Path):
        try:
            with open(config_file) as c:
                self.config = json.loads(c.read())
        except FileNotFoundError as e:
            print("Default config file: config.json not found next to main.py")
            raise e

    def get_song_from_url(self, url: str) -> FFmpegOpusAudio:
        return FFmpegOpusAudio(url, executable=str(self.ffmpeg))

    async def start_bot(self) -> None:
        if not self.config:
            self.config(self.config_file)

        self.logger.info(self.ffmpeg)
        await self.load_extension("commands.admin")
        await self.load_extension("commands.general")
        await self.load_extension("commands.music")
        await self.start(self.config["bot-token"])
