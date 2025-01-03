from typing import Optional, List, Self
import datetime
import random
import time

from discord import Embed, VoiceClient

from utils.bot_config import CroiBot
from utils.yt_vid import Video


class Queue:
    LS_NORMAL = 1
    LS_LOOP_1 = 2
    LS_LOOP_A = 3

    def __init__(
        self, bot: CroiBot, guild_id: int, channel_id: int, vc: VoiceClient
    ) -> Self:
        self.bot = bot
        self.guild_id: int = guild_id
        self.channel_id: int = channel_id
        self.voice_client = vc
        self.last_play_time: int = time.time()
        self.searching: bool = False

        self.currently_playing: Optional[Video] = None
        self.queue: List[Video] = []
        self.loop_state: int = self.LS_NORMAL

    def shuffle(self) -> None:
        random.shuffle(self.queue)

    async def next(self, skip: bool) -> None:
        if self.searching:
            return

        if self.loop_state == self.LS_NORMAL:
            if len(self.queue) >= 1:
                self.currently_playing = self.queue.pop(0)
            else:
                self.currently_playing = None
                return
        elif self.loop_state == self.LS_LOOP_1:
            pass
        elif self.loop_state == self.LS_LOOP_A:
            self.queue.append(self.currently_playing)
            self.currently_playing = self.queue.pop(0)

        if not skip and self.currently_playing:
            self.searching = True
            self.currently_playing = await self.currently_playing.renew()
            self.searching = False
            await self.play()

    async def add(self, vid: Video) -> None:
        channel = self.bot.get_channel(self.channel_id)
        self.queue.append(vid)

        if not self.currently_playing:
            await self.next(False)
        else:
            embed = Embed()
            embed.title = "Added song:"
            embed.url = vid.web_url
            embed.timestamp = datetime.datetime.utcnow()
            embed = embed.set_image(url=vid.thumbnail)
            embed = embed.add_field(
                name=vid.title,
                value=f"Duration: {vid.duration_str}\nBy: {vid.uploader}",
                inline=False,
            )

            await channel.send(embed=embed)

    async def play(self) -> None:
        if not self.currently_playing:
            return

        self.last_play_time = time.time() + self.currently_playing.duration
        channel = self.bot.get_channel(self.channel_id)
        embed = Embed()
        embed.title = "Now playing"
        embed.url = self.currently_playing.web_url
        embed.timestamp = datetime.datetime.utcnow()
        embed = embed.set_image(url=self.currently_playing.thumbnail)
        embed = embed.add_field(
            name=self.currently_playing.title,
            value=f"Duration: {self.currently_playing.duration_str}\nBy: {self.currently_playing.uploader}",
            inline=False,
        )

        await channel.send(embed=embed)
        self.voice_client.play(self.bot.get_song_from_url(self.currently_playing.url))
