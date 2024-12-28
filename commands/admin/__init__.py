__title__ = "bot_admin_commands"
__author__ = "croisen"
__license__ = "MIT"
__copyright__ = "Copyright 2024-present croisen"
__version__ = "0.0.1"

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

import logging

from discord.ext.commands import Cog, Context
from discord.ext.commands import guild_only, hybrid_command

from utils.bot_config import CroiBot


class Admin(Cog):
    def __init__(self, bot: CroiBot):
        self.bot: CroiBot = bot
        self.logger = logging.getLogger(__name__)
        self.extensions = []

    def add_extensions(self) -> None:
        for extension in self.bot.extensions.keys():
            self.extensions.append(extension)

    @hybrid_command()
    @guild_only()
    async def logout(self, ctx: Context) -> None:
        if not await self.bot.is_owner(ctx.author):
            await ctx.reply("You can't make me logout")

        self.logger.warning(f"Now logging out (Invoked by: {ctx.author.name})")
        await ctx.reply("Now logging out")

        for vc in self.bot.voice_clients:
            await vc.disconnect()

        for shard in self.bot.shards.values():
            await shard.disconnect()

        await (
            self.bot.http.close()
        )  # Dunno why the shard disconnect and this is not on the main close below
        await self.bot.close()

    @hybrid_command()
    @guild_only()
    async def register(self, ctx: Context, reg_global: bool = False) -> None:
        if not await self.bot.is_owner(ctx.author):
            await ctx.reply("You can't make me re-register my commands")

        if reg_global:
            await ctx.reply("Now registering commands globally")
            await self.bot.tree.sync()
        else:
            await ctx.reply("Now registering commands for the current guild")
            await self.bot.tree.sync(guild=ctx.guild)

    @hybrid_command()
    @guild_only()
    async def reload(self, ctx: Context) -> None:
        if not await self.bot.is_owner(ctx.author):
            await ctx.reply("I'm not reloading my modules")

        await ctx.reply("Reloading modules...")
        self.logger.info(f"Reloading extensions (Invoked by: {ctx.author.name})")

        if len(self.extensions) != len(self.bot.extensions):
            self.add_extensions()
            self.extensions = sorted(set(self.extensions))

        for extension in self.extensions:
            await ctx.bot.reload_extension(extension)


async def setup(bot: CroiBot) -> None:
    bot.logger.info("Loading extension Admin")
    await bot.add_cog(Admin(bot))
