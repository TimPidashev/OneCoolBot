import discord
import psutil
import os
import time
import random
import asyncio
import logging
import sqlite3
from glob import glob
from db import db
from discord.utils import get
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from quart import Quart, redirect, url_for, render_template, request
from dotenv import load_dotenv
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
from discord.ext import commands, tasks, ipc
from utils import data, embed, log

#loading and identifying client token
load_dotenv()
Token = os.getenv("BOT_TOKEN")

#timestamping start_time
start_time = time.time()

#logging logo and connecting to database
log.logo()
data.connect()

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

#ipc_class
class OneCoolBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.ipc = ipc.Server(self, secret_key="my_secret_key")

    async def on_ipc_ready(self):
        print("Ipc is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

#client setup
client = OneCoolBot(command_prefix=get_prefix, intents=discord.Intents.all())
client.process = psutil.Process(os.getpid())
client.remove_command("help")  

#change presence
async def change_presence():
        await client.wait_until_ready()
        statuses = [f"{len(client.guilds)} servers", f"{len(client.users)} members"]
        while not client.is_closed():
            status = random.choice(statuses)
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=status))
            await asyncio.sleep(10)  

#load cogs forloop
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

#commands group: bot
@client.group(pass_context=True, invoke_without_command=True, aliases=["bt", "b"])
async def bot(context): 
    await log.client_command(context)
    message = context.message  
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]

    if message.content == f"{prefix}bot" or f"{prefix}bt" or f"{prefix}b":
        await context.reply(embed=await embed.bot(context, prefix), mention_author=False)

    else:
        await context.reply("**Error :(**\nThis is not a valid command. Use this handy command `{prefix}bot help` to help you out.", mention_author=False)
    
@bot.command(aliases=["ld", "l"])
@commands.is_owner()
async def load(context, extension):
    await client.load_extension(f'cogs.{extension}')
    log.client_command(context)
    await context.reply(f"Your wish is my command | Loaded cogs.**{extension}**", mention_author=False)

@bot.command(aliases=["ul", "u"])
@commands.is_owner()
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')
    await log.client_command(context)
    await context.reply(f"Your wish is my command | Unloaded cogs.**{extension}**", mention_author=False)

@bot.command(aliases=["rl", "r"])
@commands.is_owner()
async def reload(context, extension):
    client.reload_extension(f'cogs.{extension}')
    await log.client_command(context)
    await context.reply(f"Your wish is my command | Reloaded cogs.**{extension}**", mention_author=False)

@bot.command(aliases=["hlp", "h"])
async def help(context):
    await log.client_command(context)

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
async def userinfo(context, user: discord.User = None):
    await log.client_command(context)
    await context.reply(embed=await embed.userinfo(context, user), mention_author=False)

client.loop.create_task(change_presence())
client.run(Token, reconnect=True)
