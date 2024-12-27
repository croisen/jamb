__title__ = "bot_music_commands"
__author__ = "croisen"
__license__ = "MIT"
__copyright__ = "Copyright 2024-present croisen"
__version__ = "0.0.1"

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from typing import Dict, List, Optional
import datetime
import logging
import time

from discord.embeds import Embed
from discord.ext.tasks import loop
from discord.ext.commands import Cog, Context
from discord.ext.commands import guild_only, hybrid_command

from utils.bot_config import CroiBot
from utils.yt_vid import search

from .queue import Queue


class Music(Cog):
    def __init__(self, bot: CroiBot):
        self.bot: CroiBot = bot
        self.logger = logging.getLogger(__name__)
        self.queues: Dict[int, Queue] = {}
        self.mloop.start()

    async def check_vc_get_queue(self, ctx: Context) -> Optional[Queue]:
        q = self.queues.get(ctx.guild.id)
        av = ctx.author.voice
        if not av:
            await ctx.reply("You are not in a voice channel")
            return None

        return q

    @loop(seconds=5.0)
    async def mloop(self):
        for vc in self.bot.voice_clients:
            q = self.queues.get(vc.guild.id)
            if not q:
                continue

            self.logger.debug(f"Checking {vc.guild.name}")
            if not vc.is_playing():
                g = q.guild_id
                self.logger.debug(
                    f"{vc.guild.name}: {len(q.queue)} {time.time() - q.last_play_time}"
                )

                if len(q.queue) == 0 and (time.time() - q.last_play_time) >= 600:
                    c = self.bot.get_channel(q.channel_id)
                    self.logger.info(
                        f"Disconnecting from {vc.guild.name} due to inactivity"
                    )

                    await c.send("Disconnecing due to inactivity")
                    await vc.disconnect()
                    self.queues.pop(g)
                else:
                    await q.next(False)

    @hybrid_command()
    @guild_only()
    async def play(self, ctx: Context, *, music: str) -> None:
        q = await self.check_vc_get_queue(ctx)
        if not ctx.author.voice:
            return

        if not q:
            vc = await ctx.author.voice.channel.connect(self_deaf=True)
            q = Queue(self.bot, ctx.guild.id, ctx.channel.id, vc)
            # It wasn't even raising an error when the key was just id a
            # variable that did not exist here, thus every check queue returned
            # none
            self.queues.update({ctx.guild.id: q})

        msg = await ctx.reply("Searching")
        vid = await search(str(self.bot.ffmpeg), music)
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

        current = ""
        embed = Embed()
        if not q.currently_playing:
            current = "None"
        else:
            current = q.currently_playing.title
            embed.url = q.currently_playing.url

        embed.title = f"Music Queue for {ctx.guild.name}"
        embed.description = f"Currently playing: {current}"
        embed.timestamp = datetime.datetime.utcnow()

        if len(q.queue) > 0:
            for i, music in enumerate(q.queue, start=1):
                embed = embed.add_field(
                    name=f"#{i:3}: {music.title}",
                    value="",
                    inline=False,
                )
        else:
            embed = embed.add_field(
                name="Nothing in queue",
                value="",
                inline=False,
            )

        await ctx.reply(embed=embed)

    @hybrid_command()
    @guild_only()
    async def skip(self, ctx: Context, count: int = 1) -> None:
        q = await self.check_vc_get_queue(ctx)
        if not q:
            return

        skipped: List[str] = []
        q.voice_client.stop()
        for i in range(0, count, 1):
            skipped.append(q.currently_playing.title)
            await q.next(True)

        s = "\n".join(skipped)
        await ctx.reply(f"{s}\nSkipped {len(skipped)} song(s)")
        await q.play()


async def setup(bot: CroiBot) -> None:
    bot.logger.info("Loading extension Music")
    m = Music(bot)
    await bot.add_cog(m)
