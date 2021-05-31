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
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

#loading and identifying client token
load_dotenv()
Token = os.getenv("BOT_TOKEN")

#start_time
global start_time
start_time = time.time()

#logo and connect to database
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

class OneCoolBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        DiscordComponents(self)
        await data.update_users_table(self)
        await data.update_guilds_table(self)
        await data.update_guildconfig_table(self)
    
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



"""Client/general commands below"""

#owner commands
@client.group(pass_context=True, invoke_without_command=True, aliases=["ownr", "o"])
async def owner(context):
    return

#load
@owner.command(aliases=["ld", "l"])
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

#unload
@owner.command(aliases=["ul", "u"])
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

#reload
@owner.command(aliases=["rl", "r"])
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

#shutdown
@owner.command(aliases=["sh", "s"])
@commands.is_owner()
async def shutdown(context):
    await context.reply("Your wish is my command | Shutting down.", mention_author=False)
    await log.client_close()
    await client.close()

#prefix
@client.group(pass_context=True, invoke_without_command=True, aliases=["prfx", "prf", "pr", "p"])
async def prefix(context):
    await log.client_command(context)
    prefix = await data.get_prefix(context)
    await context.reply(f"The current prefix is `{prefix}`", mention_author=False)

@prefix.command(aliases=["alias", "als", "a"])
async def aliases(context):
    await log.client_command(context)
    await context.reply("**prefix** aliases: `prfx` `prf` `pr` `p`", mention_author=False)

@prefix.command(aliases=["hlp", "h"])
async def help(context):
    await log.client_command(context)
    await context.reply(f"Shows server prefix.", mention_author=False)

#info
@client.group(pass_context=True, invoke_without_command=True, aliases=["inf", "i"])
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

@info.command(aliases=["alias", "als", "a"])
async def aliases(context):
    await log.client_command(context)
    await context.reply("**info** aliases: `inf` `i`", mention_author=False)

@info.command(aliases=["hlp", "h"])
async def help(context):
    await log.client_command(context)
    await context.reply(f"Shows bot info", mention_author=False)

#serverinfo
@client.group(pass_context=True, invoke_without_command=True, aliases=["srvrinf", "si"])
async def serverinfo(context):
    await log.client_command(context)
    await context.reply(embed=await embed.serverinfo(context), mention_author=False)

@serverinfo.command(aliases=["alias", "als", "a"])
async def aliases(context):
    await log.client_command(context)
    await context.reply("**serverinfo** aliases: `srvrinf` `si`", mention_author=False)

@serverinfo.command(aliases=["hlp", "h"])
async def help(context):
    await log.client_command(context)
    await context.reply("Shows server info.")

#userinfo
@client.group(pass_context=True, invoke_without_command=True, aliases=["usrinf", "ui"])
async def userinfo(context, user: discord.Member = None):
    await log.client_command(context)
    await context.reply(embed=await embed.userinfo(context, user), mention_author=False)

@userinfo.command(aliases=["alias", "als", "a"])
async def aliases(context):
    await log.client_command(context)
    await context.reply("**userinfo** aliases: `usrinf` `ui`", mention_author=False)

@userinfo.command(aliases=["hlp", "h"])
async def help(context):
    await log.client_command(context)
    await context.reply("Shows user info.", mention_author=False)

@client.command(aliases=["btns", "bs"])
async def buttons(message):
    embed = discord.Embed(
        colour=0x9b59b6
    )
    embed.add_field(name="Buttons", value="Here are some buttons!", inline=False)
    await message.reply(embed=embed, 
        components=[[
            Button(style=ButtonStyle.blue, label="blue"),
            Button(style=ButtonStyle.green, label="red"),
            Button(style=ButtonStyle.grey, label="grey"),
            Button(style=ButtonStyle.red, label="red"),
            Button(style=ButtonStyle.URL, label="url", url="https://onecoolbot.xyz")
            # Button(style=ButtonStyle.emoji, label="emoji", emoji=discord.PartialEmoji(name="joy", animated=False, id=None))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    ")
        ]], mention_author=False
    )

#help
@client.command(aliases=["hlp", "h"])
async def help(context, arg=None):
    await log.client_command(context)

    if arg is None:
        message = await context.reply(embed=await embed.help_page_1(context),
            components=[[
                Button(style=ButtonStyle.grey, label="back", emoji="◀️"),
                Button(style=ButtonStyle.grey, label="forward", emoji="▶️"),
                Button(style=ButtonStyle.grey, label="quit", emoji="❌")
            ]], mention_author=False
        )

        pages = 6
        current_page = 1
        timeout = False

        while timeout != True:
            try:
                response = await client.wait_for("button_click", timeout=60)

                if response.component.label == "forward" and current_page != pages:
                    current_page += 1
                   
                    if current_page == 2:
                        await message.edit(type=7, embed=await embed.help_page_2(context),
                            components=[[
                                Button(style=ButtonStyle.grey, label="back", emoji="◀️"),
                                Button(style=ButtonStyle.grey, label="forward", emoji="▶️"),
                                Button(style=ButtonStyle.grey, label="quit", emoji="❌")
                            ]], mention_author=False
                        )
                    
                    elif current_page == 3:
                        await message.edit(type=7, embed=await embed.help_page_3(context),
                            components=[[
                                Button(style=ButtonStyle.grey, label="back", emoji="◀️"),
                                Button(style=ButtonStyle.grey, label="forward", emoji="▶️"),
                                Button(style=ButtonStyle.grey, label="quit", emoji="❌")
                            ]], mention_author=False
                        )

                    elif current_page == 4:
                        await message.edit(type=7, embed=await embed.help_page_4(context),
                            components=[[
                                Button(style=ButtonStyle.grey, label="back", emoji="◀️"),
                                Button(style=ButtonStyle.grey, label="forward", emoji="▶️"),
                                Button(style=ButtonStyle.grey, label="quit", emoji="❌")
                            ]], mention_author=False
                        )

                    elif current_page == 5:
                        await message.edit(type=7, embed=await embed.help_page_5(context),
                            components=[[
                                Button(style=ButtonStyle.grey, label="back", emoji="◀️"),
                                Button(style=ButtonStyle.grey, label="forward", emoji="▶️"),
                                Button(style=ButtonStyle.grey, label="quit", emoji="❌")
                            ]], mention_author=False
                        )
                    
                    elif current_page == 6:
                        await message.edit(type=7, embed=await embed.help_page_6(context),
                            components=[[
                                Button(style=ButtonStyle.grey, label="back", emoji="◀️"),
                                Button(style=ButtonStyle.grey, label="forward", emoji="▶️"),
                                Button(style=ButtonStyle.grey, label="quit", emoji="❌")
                            ]], mention_author=False
                        )

                elif response.component.label == "back" and current_page > 1:
                    current_page -= 1

                    if current_page == 1:
                        await message.edit(type=7, embed=await embed.help_page_1(context),
                            components=[[
                                Button(style=ButtonStyle.grey, label="back", emoji="◀️"),
                                Button(style=ButtonStyle.grey, label="forward", emoji="▶️"),
                                Button(style=ButtonStyle.grey, label="quit", emoji="❌")
                            ]], mention_author=False
                        )

                    elif current_page == 2:
                        await message.edit(type=7, embed=await embed.help_page_2(context),
                            components=[[
                                Button(style=ButtonStyle.grey, label="back", emoji="◀️"),
                                Button(style=ButtonStyle.grey, label="forward", emoji="▶️"),
                                Button(style=ButtonStyle.grey, label="quit", emoji="❌")
                            ]], mention_author=False
                        )

                    elif current_page == 3:
                        await message.edit(type=7, embed=await embed.help_page_3(context),
                            components=[[
                                Button(style=ButtonStyle.grey, label="back", emoji="◀️"),
                                Button(style=ButtonStyle.grey, label="forward", emoji="▶️"),
                                Button(style=ButtonStyle.grey, label="quit", emoji="❌")
                            ]], mention_author=False
                        )

                    elif current_page == 4:
                        await message.edit(type=7, embed=await embed.help_page_4(context),
                            components=[[
                                Button(style=ButtonStyle.grey, label="back", emoji="◀️"),
                                Button(style=ButtonStyle.grey, label="forward", emoji="▶️"),
                                Button(style=ButtonStyle.grey, label="quit", emoji="❌")
                            ]], mention_author=False
                        )
                    elif current_page == 5:
                        await message.edit(type=7, embed=await embed.help_page_5(context),
                                components=[[
                                    Button(style=ButtonStyle.grey, label="back", emoji="◀️"),
                                    Button(style=ButtonStyle.grey, label="forward", emoji="▶️"),
                                    Button(style=ButtonStyle.grey, label="quit", emoji="❌")
                                ]], mention_author=False
                            )

                elif response.component.label == "quit":
                    await message.delete()
                    await context.message.delete()
                    break

                else:
                    pass
                
            except asyncio.TimeoutError:
                await message.delete()
                await context.message.delete()
                break
    
    elif arg is not None:
        if arg == "aliases" or arg == "alias" or arg == "als" or arg == "a":
            await log.client_command(context)
            await context.reply("**help** aliases: `hlp` `h`", mention_author=False)

        else:
            return

client.loop.create_task(change_presence())
client.run(Token, reconnect=True)
