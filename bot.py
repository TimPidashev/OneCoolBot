import discord
import psutil
import os
import time
import asyncio
import logging
import sqlite3
from glob import glob
from pyfiglet import Figlet
from db import db
from discord.utils import get
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart, redirect, url_for, render_template, request
from termcolor import colored, cprint
from dotenv import load_dotenv
from discord.ext import commands, tasks, ipc

load_dotenv()
Token = os.getenv("BOT_TOKEN")

start_time = time.time()

logo = Figlet(font="graffiti")
print(colored(logo.renderText("OneCoolBot"), "magenta"))

class OneCoolBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.ipc = ipc.Server(self, secret_key="my_secret_key")
    
    async def on_ready(self):
        print(colored("[main]:", "magenta"), colored("Bot is back up...", "green"))

        await self.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=".help"))

        logger = logging.getLogger("discord")
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
        handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
        logger.addHandler(handler)


    async def on_ipc_ready(self):
        print("Ipc is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

client = OneCoolBot(command_prefix=".", intents=discord.Intents.all())
client.process = psutil.Process(os.getpid())
client.remove_command("help")

@client.command()
@commands.has_permissions(administrator=True)
async def load(context, extension):
    client.load_extension(f'cogs.{extension}')
    print(colored("[main]: loaded "f'cogs.{extension}' + "...", "magenta"))

@client.command()
@commands.has_permissions(administrator=True)
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')
    print(colored("[main]: unloaded "f'cogs.{extension}' + "...", "magenta"))

@client.command()
@commands.has_permissions(administrator=True)
async def reload(context, extension):
    client.reload_extension(f'cogs.{extension}')
    print(colored("[main]: reloaded "f'cogs.{extension}' + "...", "magenta"))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def info(context):
    print(colored("[main]: command(info) used...", "magenta"))
    async with context.typing():
        await asyncio.sleep(1)
        before = time.monotonic()
        before_ws = int(round(client.latency * 1000, 1))
        ping = (time.monotonic() - before) * 1000
        ramUsage = client.process.memory_full_info().rss / 1024**2
        avgmembers = round(len(client.users) / len(client.guilds))
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(timedelta(seconds=difference))
        embed = discord.Embed(colour=0x9b59b6)
        embed.set_thumbnail(url=context.bot.user.avatar_url)
        embed.add_field(name="Developer", value="𝓣𝓲𝓶𝓶𝔂#6955")
        embed.add_field(name="Users", value=f"{len(context.guild.members)}", inline=True)
        embed.add_field(name="Ping", value=f"{before_ws}ms")
        embed.add_field(name="RAM Usage", value=f"{ramUsage:.2f} MB", inline=True)
        embed.add_field(name="Uptime", value=text, inline=True)
        embed.add_field(name="Version", value="Ver 1.1.8")
        embed.set_footer(text="Most recent changes: Added giveaway command(beta)")
        await context.message.channel.send(embed=embed)

client.run(Token, reconnect=True)