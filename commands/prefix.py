import discord
import asyncio
from discord.ext import commands
from utils import checks, log
from db import db

class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass
#dynamic helper function per user???? Where user gets the help output if they are new to the command or have never used it before
    @commands.group(pass_context=True, invoke_without_command=True, aliases=["prfx", "prf", "pr", "p"])
    async def prefix(self, context):
        await log.cog_command(self, context)
        prefix = db.record(f"SELECT Prefix FROM guilds WHERE GuildID = {context.guild.id}")[0]
        await context.reply(f"The current prefix is `{prefix}`", mention_author=False)

    @prefix.command(aliases=["hlp", "h"])
    async def help(self, context):
        await log.cog_command(self, context)
        embed = discord.Embed(colour=0x9b59b6)

        fields=[("***Command:***", "`prefix`", True),
                ("***Options:***", "`help` `aliases` `change`", True),
                ("`change`:", "Changes server prefix.", False),
                ("`aliases`:", "Shows command aliases.", False),
                ("`help`:", "Shows this message.", False)]

        embed.set_footer(text="Use this command to change my prefix!")

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)    

        await context.reply(embed=embed, mention_author=False)

    @prefix.command(aliases=["alias", "als", "a"])
    async def aliases(self, context, arg=None):
        await log.cog_command(self, context)
        embed = discord.Embed(colour=0x9b59b6)
        embed.add_field(
            name="***Command:*** prefix",
            value="***Aliases:*** `prfx` `prf` `pr` `p`",
            inline=False
        )
        await context.reply(embed=embed, mention_author=False)

    @prefix.command(aliases=["chng", "c"])
    @commands.is_owner()
    async def change(self, context, arg=None):
        await log.cog_command(self, context)

        if arg is None:
            await context.reply("**:| oops**\nMake sure to type your new prefix after the command.", mention_author=False)

        if arg is not None:
            try:
                db.execute(f"UPDATE guilds SET Prefix = ? WHERE GuildID = {context.guild.id}", arg)
                db.commit()
                await context.reply(f"**:) success**\nPrefix was changed to `{arg}`", mention_author=False)

            except:
                await context.reply("**:( error**\nAn internal error occured. How about giving that command another go?", mention_author=False)

def setup(client):
    client.add_cog(prefix(client))