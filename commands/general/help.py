from typing import Optional
import datetime
from discord.embeds import Embed
from discord.ext.commands import Context


async def help(ctx: Context, cmd_or_cat: Optional[str]) -> None:
    embed = Embed()
    embed.title = f"Help for {ctx.bot.user.name}"
    embed.url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    embed.timestamp = datetime.datetime.utcnow()
    embed = embed.set_thumbnail(url=ctx.bot.user.avatar.url)

    if not cmd_or_cat:
        for cogs in ctx.bot.cogs.values():
            cmds = cogs.get_commands()
            if len(cmds) == 0:
                continue

            cc = []
            for cmd in cmds:
                if cmd.description:
                    cc.append(f"> {cmd.name} - {cmd.description}")
                else:
                    cc.append(f"> {cmd.name}")

            embed = embed.add_field(
                name=cogs.__cog_name__, value="\n".join(cc), inline=False
            )
    else:
        cmd_found = False
        for cogs in ctx.bot.cogs.values():
            cmds = cogs.get_commands()

            if cogs.__cog_name__.lower() == cmd_or_cat.lower():
                if len(cmds) == 0:
                    continue

                cc = []
                for cmd in cmds:
                    if cmd.description:
                        cc.append(f"> {cmd.name} - {cmd.description}")
                    else:
                        cc.append(f"> {cmd.name}")

                cmd_found = True
                embed = embed.add_field(
                    name=cogs.__cog_name__, value="\n".join(cc), inline=False
                )

                break

        for cmd in ctx.bot.all_commands.values():
            if cmd_or_cat.lower() == cmd.name.lower():
                cmd_found = True
                embed = embed.add_field(
                    name=cmd.name,
                    value=f"Description: {cmd.description}\nUsage Sample: {cmd.usage}",
                    inline=False,
                )

        if not cmd_found:
            embed = embed.add_field(
                name="Command not found", value="sed :(", inline=False
            )

    await ctx.send(embed=embed)
