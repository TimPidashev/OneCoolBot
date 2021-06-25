import discord
import asyncio
from discord.ext import commands
from utils import log
from db import db

# db.connect("./data/database.db")

class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["prfx", "prf", "pr", "p"])
    async def prefix(self, context):
        await log.cog_command(self, context)
        prefix = db.record(f"SELECT Prefix FROM guilds WHERE GuildID = {context.guild.id}")[0]
        await context.reply(f"The current prefix is `{prefix}`", mention_author=False)

    @prefix.command(aliases=["alias", "als", "a"])
    async def aliases(self, context):
        await log.cog_command(self, context)
        await context.reply("**prefix** aliases: `prfx` `prf` `pr` `p`", mention_author=False)

    @prefix.command(aliases=["hlp", "h"])
    async def help(self, context):
        await log.cog_command(self, context)
        await context.reply(f"Shows server prefix.", mention_author=False)

def setup(client):
    client.add_cog(prefix(client))