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
    async def prefix(self, context, arg=None):
        if arg is not None:
            try:
                db.execute(f"UPDATE guilds SET Prefix = ? WHERE GuildID = {context.guild.id}", arg)
                db.commit()
                embed = discord.Embed(colour=0x9b59b6)
                embed.add_field(
                    name="**:) success**",
                    value=f"Prefix was changed to `{arg}`",
                    inline=True
                )
                await context.reply(embed=embed, mention_author=False)

            except:
                embed = discord.Embed(colour=0x9b59b6)
                embed.add_field(
                    name="**:( error**",
                    value=f"An internal error occured, how about giving that command another go?"
                )
                await context.reply(embed=embed, mention_author=False)

        if arg is None:        
            await log.cog_command(self, context)
            prefix = db.record(f"SELECT Prefix FROM guilds WHERE GuildID = {context.guild.id}")[0]
            await context.reply(f"The current prefix is `{prefix}`", mention_author=False)

    @prefix.command(aliases=["hlp", "h"])
    async def help(self, context):
        await log.cog_command(self, context)
        embed = discord.Embed(colour=0x9b59b6)

        fields=[("***Command***", "`prefix`", True),
                ("***Options***", "`change` `help`", True),
                ("***Aliases***", "`prfx` `prf` `pr` `p`", True),
                ("`change`", "To change prefix, just type a new prefix after `prefix`", False)]

        embed.set_footer(text="Use this command to change my prefix!")

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)    

        await context.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(prefix(client))