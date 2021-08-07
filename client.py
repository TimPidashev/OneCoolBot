"""
MIT License

Copyright (c) 2021 Timothy Pidashev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""



import discord
import psutil
import os
import time
import random
import asyncio
import logging
import traceback
import sys
import json
from glob import glob
from discord.utils import get
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart, redirect, url_for, render_template, request
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
from discord.ext import commands, tasks, ipc
from utils import checks, log
from discord_slash import SlashCommand
import statcord
import ez_db as db

#setup db
db = db.AsyncDB(db_path="./data/database/database.db", build_path="./data/database/build.sql")

#loading bot config
with open("config.json") as file:
    config = json.load(file)
    Token = config["client_token"]
    Statcord_Token = config["statcord_token"]

# logo
log.logo()

#discord.log
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="./data/logs/discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)  

async def build_db():
    await db.build()

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

async def update_usersettings_table(self):
    await db.multiexec(
        "INSERT OR IGNORE INTO usersettings (UserID) VALUES (?)",
        (
            (member.id,)
            for guild in self.guilds
            for member in guild.members
            if not member.bot
        ),
    )
    await db.commit()

class OneCoolBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = "1.3.0"
        self.start_time = time.time()
        self.maintenance = False

    async def on_ready(self):
        await build_db()
        await update_users_table(self)
        await update_usersettings_table(self)

    async def on_connect(self):
        await log.client_connect(self)

    async def on_disconnect(self):
        pass

    async def on_reconnect(self):
        await log.client_reconnect(self)

    async def on_shard_ready(self, shard_id):
        await log.on_shard_ready(self, shard_id)

#client setup
client = OneCoolBot(command_prefix=".", intents=discord.Intents.all(), case_insensitive=True, help_command=None)
client.process = psutil.Process(os.getpid())
client.config = config

#slash client
slash = SlashCommand(client, sync_commands=True)

api = statcord.Client(client, Statcord_Token)
api.start_loop()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

#change presence
async def change_presence():
        await client.wait_until_ready()

        while not client.is_closed():
            if client.maintenance == False:
                status = "/help"
                await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=status))
                await asyncio.sleep(10)  

            if client.maintenance == True:
                status = "Undergoing maintenance"
                await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=status))
                await asyncio.sleep(10)  

#statcord handling
@client.event
async def on_command(context):
    api.command_run(context)

@client.event
async def on_fatal_error(event):
    sys.exit()

"""Admin commands below"""
@client.command(hidden=True, pass_context=True, aliases=["ld"])
@commands.check(checks.is_owner)
async def load(context, extension=None):
    if extension is not None:
        try:
            client.load_extension(f"cogs.{extension}")
            await log.client_command(context)
            await log.load_cog(extension)
            await context.reply(f"Your wish is my command | Loaded cogs.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```diff\n- {error}```", mention_author=False)
    
    elif extension is None:
        await context.reply("**oops :|**\nPlease provide me with more context.", mention_author=False)

    else:
        return

#unload cog
@client.command(hidden=True, pass_context=True, aliases=["ul", "u"])
@commands.check(checks.is_owner)
async def unload(context, extension=None):
    if extension is not None:
        try:
            client.unload_extension(f"cogs.{extension}")
            await log.client_command(context)
            await log.unload_cog(extension)
            await context.reply(f"Your wish is my command | Unloaded cogs.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```diff\n- {error}```", mention_author=False)
    
    elif extension is None:
        await context.reply("**oops :|**\nPlease provide me with more context.", mention_author=False)

    else:
        return

#reload cog
@client.command(hidden=True, pass_context=True, aliases=["rl", "r"])
@commands.check(checks.is_owner)
async def reload(context, extension=None):
    if extension is not None:
        try:
            client.reload_extension(f"cogs.{extension}")
            await log.client_command(context)
            await log.reload_cog(extension)
            await context.reply(f"Your wish is my command | Reloaded cogs.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```diff\n- {error}```", mention_author=False)

    elif extension is None:
        await context.reply("**oops :|**\nPlease provide me with more context.", mention_author=False)

    else:
        return

#shutdown
@client.command(hidden=True, pass_context=True, aliases=["sh"])
@commands.check(checks.is_owner)
async def shutdown(context):
    try:
        await context.reply("Your wish is my command | Shutting down.", mention_author=False)
        await log.client_close(context)
        await client.close()
        sys.exit() #very lazy shutdown, clean up later

    except Exception as error:
        await context.reply(f"**error :(**\n```diff\n- {error}```", mention_author=False)

#restart
@client.command(hidden=True, pass_context=True, aliases=["re", "rst"])
@commands.check(checks.is_owner)
async def restart(context):
    try:
        await context.reply("Your wish is my command | Restarting.", mention_author=False)
        await log.client_restart(context)
        await client.close()
        os.execl(sys.executable, sys.executable, *sys.argv)

    except Exception as error:
        await context.reply(f"**error :(**\n```diff\n- {error}```", mention_author=False)

@client.command(hidden=True, pass_context=True, aliases=["m"])
@commands.check(checks.is_owner)
async def maintenance(context, arg):
    if arg == "on" and client.maintenance == False:
        try:
            client.maintenance = True
            await context.reply("Your wish is my command | Going into maintenance mode", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```diff\n- {error}```", mention_author=False)

    if arg == "off" and client.maintenance == True:
        try:
            client.maintenance = False
            await context.reply("Your wish is my command | Updating and exiting maintenance mode", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```diff\n- {error}```", mention_author=False)

    else:
        pass

client.loop.create_task(change_presence())
client.run(Token, reconnect=True)
