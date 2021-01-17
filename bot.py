#import stuff
import discord
import os
import time
import asyncio
from pyfiglet import Figlet
from termcolor import colored, cprint
from dotenv import load_dotenv
from discord.ext import commands
import logging
intents = discord.Intents.default()
intents.members = True
load_dotenv()
Token = os.getenv('BOT_TOKEN')

#prefix/remove default help command/shard bot
client = commands.AutoShardedBot(commands.when_mentioned_or("."), intents=intents)
client.remove_command("help")

#ASCII art
cool_logo = Figlet(font="graffiti")
print(colored(cool_logo.renderText("OneCoolBot"), "magenta"))

#discord.log
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

#cogs related
@client.command()
@commands.has_permissions(administrator=True)
async def load(context, extension):
    client.load_extension(f'cogs.{extension}')
    print(colored("loaded "f'cogs.{extension}' + "...", "yellow"))

@client.command()
@commands.has_permissions(administrator=True)
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')
    print(colored("unloaded "f'cogs.{extension}' + "...", "yellow"))

@client.command()
@commands.has_permissions(administrator=True)
async def reload(context, extension):
    client.reload_extension(f'cogs.{extension}')
    print(colored("reloaded "f'cogs.{extension}' + "...", "yellow"))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#on_shard_ready
@client.event
async def on_shard_ready(shard_id):
    print(colored(f"Shard {shard_id} is ready...", "green"))

#on_ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=".help"))
    print(colored("Bot is back up...", "green"))

client.run(Token, reconnect=True)
