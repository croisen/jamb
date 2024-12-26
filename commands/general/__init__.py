__title__ = "bot_general_commands"
__author__ = "croisen"
__license__ = "MIT"
__copyright__ = "Copyright 2024-present croisen"
__version__ = "0.0.1"

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from typing import Optional
import logging

from discord.ext.commands import Cog, Context
from discord.ext.commands import guild_only, hybrid_command

from utils.bot_config import CroiBot

from . import help


class General(Cog):
    def __init__(self, bot: CroiBot):
        self.bot: CroiBot = bot
        self.logger = logging.getLogger(__name__)

    @hybrid_command(description="Shows this message")
    @guild_only()
    async def help(self, ctx: Context, cmd_or_cat: Optional[str] = None) -> None:
        await help.help(ctx, cmd_or_cat)


async def setup(bot: CroiBot) -> None:
    bot.logger.info("Loading extension General")
    await bot.add_cog(General(bot))
