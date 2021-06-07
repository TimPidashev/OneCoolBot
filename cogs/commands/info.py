import discord
import time
import asyncio
import psutil
from discord.ext import commands
from utils import data, embed, log
from datetime import datetime, timedelta

#global runtime process
start_time = time.time()

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        await log.on_command_ready(self)
        #doesnt work

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["inf", "i"])
    async def info(self, context):
        await log.cog_command(self, context)

        before = time.monotonic()
        before_ws = int(round(self.client.latency * 1000, 1))
        ping = (time.monotonic() - before) * 1000
        ramUsage = self.client.process.memory_full_info().rss / 1024**2
        current_time = time.time()
        difference = int(round(current_time - start_time))
        uptime = str(timedelta(seconds=difference))
        users = len(self.client.users)

        await context.reply(embed=await embed.info(context, users, before_ws, ramUsage, uptime), mention_author=False)

    @info.command(aliases=["alias", "als", "a"])
    async def aliases(self, context):
        await log.cog_command(self, context)
        await context.reply("**info** aliases: `inf` `i`", mention_author=False)

    @info.command(aliases=["hlp", "h"])
    async def help(self, context):
        await log.cog_command(self, context)
        await context.reply(f"Shows bot info", mention_author=False)

def setup(client):
    client.add_cog(info(client))