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
import json
from glob import glob
from db import db
from discord.utils import get
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart, redirect, url_for, render_template, request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
from discord.ext import commands, tasks, ipc
from utils import log
from discord_slash import SlashCommand
import statcord

#version
__VERSION__ = "1.2.8"

#global runtime process
start_time = time.time()

#loading bot config
with open("config.json") as file:
    config = json.load(file)
    Token = config["client_token"]
    Statcord_Token = config["statcord_token"]

#logo
log.logo()

#discord.log
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="./data/logs/discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)  

async def get_prefix(client, context):
    prefix = await db.record(f"SELECT Prefix FROM guilds WHERE GuildID = {context.guild.id}")
    return prefix[0]

async def get_uptime():
    current_time = time.time()
    difference = int(round(current_time - start_time))
    uptime = str(timedelta(seconds=difference))
    return uptime

async def get_version():
    version == __VERSION__
    return version

async def get_latency():
    before = time.monotonic()
    before_ws = int(round(self.client.latency * 1000, 1))
    latency = (time.monotonic() - before) * 1000
    return latency

async def get_ram_usage():
    ram_usage = self.client.process.memory_full_info().rss / 1024**2
    return ram_usage

async def is_owner(context):
    global config
    return context.message.author.id in config["owner_ids"]

async def get_user_count():
    users = len(self.client.users)
    return users

async def update_users_table(self):
    await db.multiexec(
        "INSERT OR IGNORE INTO users (GuildID, UserID) VALUES (?, ?)",
        (
            (member.guild.id, member.id,)
            for guild in self.guilds
            for member in guild.members
            if not member.bot
        ),
    )
    await db.commit()

async def update_guilds_table(self):
    await db.multiexec(
        "INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
        ((guild.id,) for guild in self.guilds),
    )
    await db.commit()

async def update_guildconfig_table(self):
    await db.multiexec(
        "INSERT OR IGNORE INTO guildconfig (GuildID) VALUES (?)",
        ((guild.id,) for guild in self.guilds),
    )
    await db.commit()

class OneCoolBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        await update_users_table(self)
        await update_guilds_table(self)
        await update_guildconfig_table(self)
    
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
client.config = config
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
@client.command(hidden=True, pass_context=True, aliases=["ld", "l"])
@commands.check(is_owner)
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
@client.command(hidden=True, pass_context=True, aliases=["ul", "u"])
@commands.check(is_owner)
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
@client.command(hidden=True, pass_context=True, aliases=["rl", "r"])
@commands.check(is_owner)
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
@client.command(hidden=True, pass_context=True, aliases=["ldc", "lc"])
@commands.check(is_owner)
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
@client.command(hidden=True, pass_context=True, aliases=["ulc", "uc"])
@commands.check(is_owner)
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
@client.command(hidden=True, pass_context=True, aliases=["rlc", "rc"])
@commands.check(is_owner)
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
@client.command(hidden=True, pass_context=True, aliases=["sh"])
@commands.check(is_owner)
async def shutdown(context):
    await context.reply("Your wish is my command | Shutting down.", mention_author=False)
    await log.client_close()
    await client.close()
    
client.loop.create_task(change_presence())
client.run(Token, reconnect=True)