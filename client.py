import discord
import psutil
import os
import time
import random
import asyncio
import logging
import sqlite3
import traceback
import sys
import aiml
from glob import glob
# from ai import train
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
from utils import data, embed, log

#test channel for ai
channel_name = "timmy-testin" # default channel name

#loading and identifying client token
load_dotenv()
Token = os.getenv("BOT_TOKEN")

#timestamping start_time
start_time = time.time()

#logging logo and connecting to database
log.logo()
data.connect()

# AIML startup
# kernel = aiml.Kernel()
# kernel.learn("std-startup.xml")
# kernel.respond("LOAD AIML B")

#discord.log
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="./data/logs/discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)  

#get_prefix
async def get_prefix(client, context):
    prefix = db.record(f"SELECT Prefix FROM guilds WHERE GuildID = {context.guild.id}")[0]
    return prefix

class OneCoolBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        await data.update_users_table(self)
        await data.update_guilds_table(self)
        await data.update_guildconfig_table(self)
    
    async def on_connect(self):
        await log.client_connect(self)

    async def on_disconnect(self):
        await log.client_disconnect(self)

    async def on_shard_ready(self, shard_id):
        await log.on_shard_ready(self, shard_id)

    async def on_ipc_ready(self):
        pass

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

#client setup
client = OneCoolBot(command_prefix=get_prefix, intents=discord.Intents.all(), case_insensitive=True)
client.process = psutil.Process(os.getpid())
client.remove_command("help")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

#change presence
async def change_presence():
        await client.wait_until_ready()
        statuses = [f"{len(client.guilds)} servers", f"{len(client.users)} members", "Evolving AI"]
        while not client.is_closed():
            status = random.choice(statuses)
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=status))
            await asyncio.sleep(10)  

#AIML HANDLER
# @client.event
# async def on_message(message):
#     channel = message.channel

#     if message.author.bot or str(message.channel) != channel_name:
#         return
    
#     if message.author == client.user:
#         return

#     if message.content is None:
#         return

#     if "https://" in message.content.lower() or "www." in message.content.lower():
#         return

#     if message.content == "<@547321575993769984>":
#         await mesage.reply(f"{mesage.author.mention}")
#         return
        
#     else:
#         response = kernel.respond(message.content)
#         await asyncio.sleep(random.randint(0,2))
#         await channel.send(response)

#commands group: bot
@client.group(pass_context=True, invoke_without_command=True, aliases=["bt", "b"])
async def bot(context, arg=None): 
    await log.client_command(context)
    prefix = await data.get_prefix(context)
    
    if arg is not None:
        if arg == "aliases" or arg == "alias" or arg == "als" or arg == "a": 
            await context.reply(f"**{prefix}bot** aliases: `bt` `b`", mention_author=False)

        if arg == "prefix" or arg == "prfx" or arg == "prf" or arg == "pr" or arg == "p":
            await context.reply(f"The current prefix is `{prefix}`", mention_author=False)

        else:
            return

    elif arg is None:
        return

@bot.command(aliases=["ld", "l"])
@commands.is_owner()
async def load(context, extension=None):
    if extension is not None:
        try:
            client.load_extension(f'cogs.{extension}')
            await log.client_command(context)
            await context.reply(f"Your wish is my command | Loaded cogs.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```{error}```", mention_author=False)
    
    elif extension is None:
        await context.reply("**oops :|**\n Please provide me with more context.", mention_author=False)

    else:
        return

@bot.command(aliases=["ul", "u"])
@commands.is_owner()
async def unload(context, extension=None):
    if extension is not None:
        try:
            client.unload_extension(f'cogs.{extension}')
            await log.client_command(context)
            await context.reply(f"Your wish is my command | Unloaded cogs.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```{error}```", mention_author=False)
    
    elif extension is None:
        await context.reply("**oops :|**\n Please provide me with more context.", mention_author=False)

    else:
        return

@bot.command(aliases=["rl", "r"])
@commands.is_owner()
async def reload(context, extension=None):
    if extension is not None:
        try:
            client.reload_extension(f'cogs.{extension}')
            await log.client_command(context)
            await context.reply(f"Your wish is my command | Reloaded cogs.**{extension}**", mention_author=False)

        except Exception as error:
            await context.reply(f"**error :(**\n```{error}```", mention_author=False)

    elif extension is None:
        await context.reply("**oops :|**\n Please provide me with more context.", mention_author=False)

    else:
        return

@bot.command(aliases=["hlp", "h"])
async def help(context, arg=None):
    await log.client_command(context)
    if arg is None:
        message = await context.reply(embed=await embed.help_page_1(context), mention_author=False)
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("❌")
        pages = 6
        current_page = 1

        def check(reaction, user):
            return user == context.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]

        while True:
            try:
                reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" and current_page != pages:
                    current_page += 1

                    if current_page == 2:
                        await message.edit(embed=await embed.help_page_2(context))
                        await message.remove_reaction(reaction, user)
                    
                    elif current_page == 3:
                        await message.edit(embed=await embed.help_page_3(context))
                        await message.remove_reaction(reaction, user)

                    elif current_page == 4:
                        await message.edit(embed=await embed.help_page_4(context))
                        await message.remove_reaction(reaction, user)

                    elif current_page == 5:
                        await message.edit(embed=await embed.help_page_5(context))
                        await message.remove_reaction(reaction, user)

                    elif current_page == 6:
                        await message.edit(embed=await embed.help_page_6(context))
                        await message.remove_reaction(reaction, user)
                
                if str(reaction.emoji) == "◀️" and current_page > 1:
                    current_page -= 1
                    
                    if current_page == 1:
                        await message.edit(embed=await embed.help_page_1(context))
                        await message.remove_reaction(reaction, user)

                    elif current_page == 2:
                        await message.edit(embed=await embed.help_page_2(context))
                        await message.remove_reaction(reaction, user)
                    
                    elif current_page == 3:
                        await message.edit(embed=await embed.help_page_3(context))
                        await message.remove_reaction(reaction, user)

                    elif current_page == 4:
                        await message.edit(embed=await embed.help_page_4(context))
                        await message.remove_reaction(reaction, user)

                    elif current_page == 5:
                        await message.edit(embed=await embed.   help_page_5(context))
                        await message.remove_reaction(reaction, user)

                if str(reaction.emoji) == "❌":
                    await message.delete()
                    await context.message.delete()
                    break

                else:
                    await message.remove_reaction(reaction, user)
                    
            except asyncio.TimeoutError:
                await message.delete()
                await context.message.delete()
                break

@bot.command(aliases=["inf", "i"])
async def info(context):
    await log.client_command(context)

    before = time.monotonic()
    before_ws = int(round(client.latency * 1000, 1))
    ping = (time.monotonic() - before) * 1000
    ramUsage = client.process.memory_full_info().rss / 1024**2
    current_time = time.time()
    difference = int(round(current_time - start_time))
    uptime = str(timedelta(seconds=difference))
    users = len(client.users)

    await context.reply(embed=await embed.info(context, users, before_ws, ramUsage, uptime), mention_author=False)

@bot.command(aliases=["srvrinf", "si"])
async def serverinfo(context):
    await log.client_command(context)
    await context.reply(embed=await embed.serverinfo(context), mention_author=False)

@bot.command(aliases=["usrinf", "ui"])
async def userinfo(context, user: discord.Member = None):
    await log.client_command(context)
    await context.reply(embed=await embed.userinfo(context, user), mention_author=False)

client.loop.create_task(change_presence())
client.run(Token, reconnect=True)
