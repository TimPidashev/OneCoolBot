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
from termcolor import colored, cprint
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

async def get_prefix(client, context):
        prefix = db.record(f"SELECT Prefix FROM guilds WHERE GuildID = {context.guild.id}")
        return prefix

class OneCoolBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.ipc = ipc.Server(self, secret_key="my_secret_key")

    async def on_ready(self):
        db.connect("./data/database.db")

        logger = logging.getLogger("discord")
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename="./data/logs/discord.log", encoding="utf-8", mode="w")
        handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
        logger.addHandler(handler)  

    async def on_ipc_ready(self):
        print("Ipc is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

client = OneCoolBot(command_prefix=get_prefix, intents=discord.Intents.all())
client.process = psutil.Process(os.getpid())
client.remove_command("help")  

async def change_presence():
        await client.wait_until_ready()
        statuses = [f"{len(client.guilds)} servers", f"{len(client.users)} members"]
        while not client.is_closed():
            status = random.choice(statuses)
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=status))
            await asyncio.sleep(10)  

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

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
    await context.reply(f"Your wish is my command | Loaded cogs.{extension}", mention_author=False)

@bot.command(aliases=["ul", "u"])
@commands.is_owner()
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')
    await log.client_command(context)
    await context.reply(f"Your wish is my command | Unloaded cogs.{extension}", mention_author=False)

@bot.command(aliases=["rl", "r"])
@commands.is_owner()
async def reload(context, extension):
    client.reload_extension(f'cogs.{extension}')
    await log.client_command(context)
    await context.reply(f"Your wish is my command | Reloaded cogs.{extension}", mention_author=False)

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

@bot.group(pass_context=True, invoke_without_command=True, aliases=["st", "s"])
async def settings(context):
    await log.client_command(context)
    message = context.message  
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]

    if message.content == f"{prefix}bot settings" or f"{prefix}bt settings" or f"{prefix}b settings" f"{prefix}bot st" f"{prefix}b s":
        await context.reply(embed=await embed.settings(context, prefix), mention_author=False)

    else:
        await context.reply("**Error :(**\nThis is not a valid command. Use this handy command `{prefix}bot help` to help you out.", mention_author=False)
    

@settings.command(aliases=["hlp", "h"])
async def help(context):
    await log.client_command(context)
    message = await context.reply(embed=await embed.settings_help_page_1(context), mention_author=False)

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    await message.add_reaction("❌")
    pages = 2
    current_page = 1

    def check(reaction, user):
        return user == context.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]

    while True:
        try:
            reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

            if str(reaction.emoji) == "▶️" and current_page != pages:
                current_page += 1

                if current_page == 2:
                    await message.edit(embed=await embed.settings_help_page_2(context))
                    await message.remove_reaction(reaction, user)
            
            if str(reaction.emoji) == "◀️" and current_page > 1:
                current_page -= 1
                
                if current_page == 1:
                    await message.edit(embed=await embed.settings_help_page_1(context))
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

@settings.command(aliases=["prfx", "p"])
async def prefix(context, arg=None):
    await log.client_command(context)
    
    if arg is not None and context.author == context.guild.owner:

        db.execute(f"UPDATE guilds SET Prefix = ? WHERE GuildID = {context.guild.id}", arg)
        db.commit()

        prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?", context.guild.id)[0]

        await context.reply(f"The prefix was changed to `{prefix}`", mention_author=False)
    
    if arg is None:
        prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?", context.guild.id)[0]

        if context.author == context.guild.owner:
            await context.reply(f"The current prefix is `{prefix}`\nTo change the prefix, use this handy command: `{prefix}bot prefix <prefix>`", mention_author=False)

        else:
            await context.reply(f"The current prefix is `{prefix}`", mention_autho=False)

@settings.command()
async def levels(context, arg=None):
    await log.client_command(context)
    levels = db.record(f"SELECT Levels FROM guildconfig WHERE GuildID = {context.guild.id}")[0]

    if arg == "on" and context.author == context.guild.owner:
        levels = "ON"
        db.execute(f"UPDATE guildconfig SET Levels = ? WHERE GuildID = {context.guild.id}",
            levels
        )
        db.commit()

        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.add_field(
            name="Current Settings",
            value="Levels were turned on!",
            inline=False
        )
    
        await context.reply(embed=embed, mention_author=False)

    if arg == "off" and context.author == context.guild.owner:
        levels = "OFF"
        db.execute(f"UPDATE guildconfig SET Levels = ? WHERE GuildID = {context.guild.id}",
            levels
        )
        db.commit()

        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.add_field(
            name="Current Settings",
            value="Levels were turned off!",
            inline=False
        )
    
        await context.reply(embed=embed, mention_author=False)

    if arg is None:
        levels = db.record(f"SELECT Levels from guildconfig WHERE GuildID = {context.guild.id}")[0]

        if levels == "OFF":
            await context.reply("**Levels** are currently off.", mention_author=False)
            
        if levels == "ON":
            await context.reply("**Levels** are currently on.", mention_author=False)

@settings.command()
async def levelmessages(context, arg=None):
    await log.client_command(context)
    levelmessage = db.record(f"SELECT LevelMessages FROM guildconfig WHERE GuildID = {context.guild.id}")[0]

    if arg == "on" and context.author == context.guild.owner:
        levelmessage = "ON"
        db.execute(f"UPDATE guildconfig SET LevelMessages = ? WHERE GuildID = {context.guild.id}",
            levelmessage
        )
        db.commit()

        message = db.record(f"SELECT LevelMessage FROM guildconfig WHERE GuildID = {context.guild.id}")[0]
        
        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.add_field(
            name="Current Settings",
            value="Level message turned on!",
            inline=False
        )
        embed.add_field(
            name="Current Level Message",
            value=f"{message}",
            inline=False
        )
        # if channel == "0":
        #     embed.add_field(
        #         name="Current Level Message Channel",
        #         value="None, level messages will be sent to the member in chat.",
        #         inline=False
        #     )
        
        # if channel != "0":
            
        #     embed.add_field(
        #         name="Current Level Message Channel",
        #         value=f"{channel}",
        #         inline=False
        #     )
    
        await context.reply(embed=embed, mention_author=False)

    if arg == "off" and context.author == context.guild.owner:
        levelmessage = "OFF"
        db.execute(f"UPDATE guildconfig SET LevelMessage = ? WHERE GuildID = {context.guild.id}",
            levelmessage
        )
        db.commit()

        await context.reply("**Level messages** were turned off.", mention_author=False)

    if arg is None:
        levelmessages = db.record(f"SELECT LevelMessages FROM guildconfig WHERE GuildID = {context.guild.id}")[0]

        if levelmessages == "OFF":
            await context.reply("**Level messages** are currently off.", mention_author=False)

        if levelmessages == "ON":
            await context.reply("**Level messages** are currently on", mention_author=Falses)

        if levelmessages == "NONE":
            db.execute("INSERT INTO guildconfig (GuildID) VALUES (?)", context.guild.id)
            db.commit()
    
    if arg == "help":
        await context.reply("Under construction.", mention_author=False)

client.loop.create_task(change_presence())
client.run(Token, reconnect=True)
