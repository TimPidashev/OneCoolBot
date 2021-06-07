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

        info = discord.Embed(
        title="Bot Info",
        description="Everything about me!",
        colour=0x9b59b6
        )
        info.set_thumbnail(
            url=context.bot.user.avatar_url
        )
        fields = [("Developer", "𝓣𝓲𝓶𝓶𝔂#6955", True), 
                ("Users", f"{users}", True),
                ("Latency", f"{before_ws}ms", True),
                ("RAM Usage", f"{ramUsage:.2f} MB", True), 
                ("Uptime", uptime, True), 
                ("Version", "Ver 1.2.7", True)]

        info.set_footer(
            text="Most recent changes: Command revamp, prep for asyncpg"
        )

        for name, value, inline in fields:
            info.add_field(name=name, value=value, inline=inline)

        await context.reply(embed=info, mention_author=False)

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