from typing import Any
import asyncio
import logging
import time

from utils.bot_config import CroiBot

from .queue import Queue


_logger = logging.getLogger(__name__)


async def music_loop(b: CroiBot, m: Any) -> None:
    """
    m is typed as Any to avoid import loops but it takes a Music cog
    """

    _logger.info("Music loop started")
    while not b.is_closed():
        for vc in b.voice_clients:
            q: Queue = m.get_queue().get(vc.guild.id)
            if not q:
                continue

            _logger.debug(f"Checking {vc.guild.name}")
            if not vc.is_playing():
                g = q.guild_id
                _logger.debug(
                    f"{vc.guild.name}: {len(q.queue)} {time.time() - q.last_play_time}"
                )

                if len(q.queue) == 0 and (time.time() - q.last_play_time) >= 600:
                    c = b.get_channel(q.channel_id)
                    _logger.info(
                        f"Disconnecting from {vc.guild.name} due to inactivity"
                    )

                    await c.send("Disconnecing due to inactivity")
                    await vc.disconnect()
                    m.get_queue().pop(g)
                else:
                    await q.next()

        _logger.debug("Now sleeping")
        await asyncio.sleep(5)

    _logger.info("Music loop done")
