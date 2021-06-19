import discord
import psutil
import os
import time
import random
import asyncio
import logging
import aiosqlite
import sqlite3
import traceback
import sys
from glob import glob
from db import db
from discord.utils import get
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart, redirect, url_for, render_template, request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
from discord.ext import commands, tasks, ipc
from utils import log
from discord_slash import SlashCommand
import statcord

#loading and identifying client token
load_dotenv()
Token = os.getenv("BOT_TOKEN")
Statcord_Token = os.getenv("STATCORD")

#logo
log.logo()

#discord.log
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="./data/logs/discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)  

#get_prefix
async def get_prefix(client, context):
    prefix = await db.record(f"SELECT Prefix FROM guilds WHERE GuildID = {context.guild.id}")
    return prefix[0]

class OneCoolBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        pass
    
    async def on_connect(self):
        await log.client_connect(self)

    async def on_disconnect(self):
        await log.client_disconnect(self)

    async def on_reconnect(self):
        await log.client_reconnect(self)

    async def on_shard_ready(self, shard_id):
        await log.on_shard_ready(self, shard_id)

#client setup
client = OneCoolBot(command_prefix=get_prefix, intents=discord.Intents.all(), case_insensitive=True)
client.process = psutil.Process(os.getpid())
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)
client.remove_command("help")
api = statcord.Client(client, Statcord_Token)
api.start_loop()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        client.load_extension(f"commands.{filename[:-3]}")

#change presence
async def change_presence():
        await client.wait_until_ready()
        statuses = [f"{len(client.guilds)} servers", f"{len(client.users)} members", "Evolving AI"]
        while not client.is_closed():
            status = random.choice(statuses)
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=status))
            await asyncio.sleep(10)  

"""Client/general commands below"""

#statcord handling
@client.event
async def on_command(context):
    api.command_run(context)

#load
@client.command(aliases=["ld", "l"])
@commands.is_owner()
async def load(context, extension=None):
    if extension is not None:
        try:
            client.load_extension(f"cogs.{extension}")
            await log.client_command(context)
            await context.reply(f"Your wish is my command | Loaded cogs.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```{error}```", mention_author=False)
    
    elif extension is None:
        await context.reply("**oops :|**\nPlease provide me with more context.", mention_author=False)

    else:
        return

#unload
@client.command(aliases=["ul", "u"])
@commands.is_owner()
async def unload(context, extension=None):
    if extension is not None:
        try:
            client.unload_extension(f"cogs.{extension}")
            await log.client_command(context)
            await context.reply(f"Your wish is my command | Unloaded cogs.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```{error}```", mention_author=False)
    
    elif extension is None:
        await context.reply("**oops :|**\nPlease provide me with more context.", mention_author=False)

    else:
        return

#reload
@client.command(aliases=["rl", "r"])
@commands.is_owner()
async def reload(context, extension=None):
    if extension is not None:
        try:
            client.reload_extension(f"cogs.{extension}")
            await log.client_command(context)
            await context.reply(f"Your wish is my command | Reloaded cogs.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```{error}```", mention_author=False)

    elif extension is None:
        await context.reply("**oops :|**\nPlease provide me with more context.", mention_author=False)

    else:
        return

#load command
@client.command(aliases=["ldc", "lc"])
@commands.is_owner()
async def loadcommand(context, extension=None):
    if extension is not None:
        try:
            client.load_extension(f"commands.{extension}")
            await log.client_command(context)
            await context.reply(f"Your wish is my command | Loaded commands.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```{error}```", mention_author=False)
    
    elif extension is None:
        await context.reply("**oops :|**\nPlease provide me with more context.", mention_author=False)

    else:
        return

#unload command
@client.command(aliases=["ulc", "uc"])
@commands.is_owner()
async def unloadcommmand(context, extension=None):
    if extension is not None:
        try:
            client.unload_extension(f"commands{extension}")
            await log.client_command(context)
            await context.reply(f"Your wish is my command | Unloaded commands.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```{error}```", mention_author=False)
    
    elif extension is None:
        await context.reply("**oops :|**\nPlease provide me with more context.", mention_author=False)

    else:
        return

#reload command
@client.command(aliases=["rlc", "rc"])
@commands.is_owner()
async def reloadcommand(context, extension=None):
    if extension is not None:
        try:
            client.reload_extension(f"commands.{extension}")
            await log.client_command(context)
            await context.reply(f"Your wish is my command | Reloaded commands.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```{error}```", mention_author=False)

    elif extension is None:
        await context.reply("**oops :|**\nPlease provide me with more context.", mention_author=False)

    else:
        return

#shutdown
@client.command(aliases=["sh"])
@commands.is_owner()
async def shutdown(context):
    await context.reply("Your wish is my command | Shutting down.", mention_author=False)
    await log.client_close()
    await client.close()

# @client.event
# async def on_message(context):
#     await db.execute("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)", context.guild.id)
#     await db.commit()
#     await context.reply(f"{context.guild.name} inserted into database!!!!! woooooohooooo im back!!!!!!!!!!!! thx Timmy!!!!!!!!", mention_author=False)

client.loop.create_task(change_presence())

try:
    client.run(Token, reconnect=True)

except KeyboardInterrupt:
    client.close()
