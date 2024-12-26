__title__ = "bot_music_commands"
__author__ = "croisen"
__license__ = "MIT"
__copyright__ = "Copyright 2024-present croisen"
__version__ = "0.0.1"

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from typing import Dict, Optional
import asyncio
import datetime
import logging

from discord.embeds import Embed
from discord.ext.commands import Cog, Context
from discord.ext.commands import guild_only, hybrid_command

from utils.bot_config import CroiBot
from utils.yt_vid import search

from .queue import Queue
from .music_loop import music_loop


class Music(Cog):
    def __init__(self, bot: CroiBot):
        self.bot: CroiBot = bot
        self.logger = logging.getLogger(__name__)
        self.queues: Dict[int, Queue] = {}

    def get_queue(self) -> Dict[int, Queue]:
        return self.queues

    async def check_vc_get_queue(self, ctx: Context) -> Optional[Queue]:
        q = self.queues.get(ctx.guild.id)
        av = ctx.author.voice
        if not av:
            await ctx.reply("You are not in a voice channel")
            return None

        return q

    @hybrid_command()
    @guild_only()
    async def play(self, ctx: Context, music: str) -> None:
        q = await self.check_vc_get_queue(ctx)
        if not q:
            vc = await ctx.author.voice.channel.connect()
            q = Queue(self.bot, ctx.guild.id, ctx.channel.id, vc)
            self.queues.update({id: q})

        msg = await ctx.reply("Searching")
        vid = await search(music)
        await msg.delete()
        await q.add(vid)

    @hybrid_command()
    @guild_only()
    async def stop(self, ctx: Context) -> None:
        q = await self.check_vc_get_queue(ctx)
        if not q:  # Uh oh moment if this is the case
            for vc in self.bot.voice_clients:
                if ctx.guild.id == vc.guild.id:
                    await ctx.reply("Stopping music")
                    await vc.disconnect()
                    return

            await ctx.reply(
                "Voice channel state cannot be found in this guild, try to message one of this bot's owners or croisen#5695"
            )
            return

        await ctx.reply("Stopping music")
        self.queues.pop(ctx.guild.id)
        await q.voice_client.disconnect()

    @hybrid_command()
    @guild_only()
    async def queue(self, ctx: Context) -> None:
        q = await self.check_vc_get_queue(ctx)
        if not q:
            await ctx.reply("No queue found for this guild")
            return

        embed = Embed()
        embed.title = f"Music Queue for {ctx.guild.name}"
        embed.description = f"Currently playing: {q.currently_playing}"
        embed.timestamp = datetime.datetime.utcnow()
        for i, music in enumerate(q.queue, start=1):
            embed = embed.add_field(name=f"#{i:3}: {music.title}")

        await ctx.reply(embed=embed)


async def setup(bot: CroiBot) -> None:
    bot.logger.info("Loading extension Music")
    m = Music(bot)
    await bot.add_cog(m)

    e = asyncio.get_event_loop()
    bot.mloop = e.create_task(music_loop(bot, m))
