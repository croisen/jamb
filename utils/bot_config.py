from typing import Any, Dict, Optional
from pathlib import Path
import json
import logging
import sys

from discord import Intents, Status
from discord.ext.commands import AutoShardedBot


class CroiBot(AutoShardedBot):
    config: Optional[Dict[str, Any]] = None
    config_file: Path

    def __init__(self, config_file: Path, ffmpeg_path: Path):
        self.config_file = config_file
        self.get_config(self.config_file)
        self.logger = logging.getLogger(__name__ + "(Bot Instance)")
        self.ffmpeg = ffmpeg_path

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
        except FileNotFoundError:
            print("Default config file: config.json not found next to main.py")
            sys.exit(1)

    async def start_bot(self) -> None:
        if not self.config:
            self.config(self.config_file)

        await self.load_extension("commands.admin")
        await self.load_extension("commands.general")
        await self.start(self.config["bot-token"])
