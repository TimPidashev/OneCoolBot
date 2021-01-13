#import stuff
import discord
import os
import asyncio
from pyfiglet import Figlet
from termcolor import colored
from dotenv import load_dotenv
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
load_dotenv()
Token = os.getenv('BOT_TOKEN')

#prefix/remove default help command/shard bot
client = commands.Bot(command_prefix = '.', intents=intents)
client.remove_command("help")

cool_logo = Figlet(font='graffiti')
print(colored(cool_logo.renderText('OneCoolBot'), 'magenta'))

#cogs related
@client.command()
@commands.has_permissions(administrator=True)
async def load(context, extension):
    client.load_extension(f'cogs.{extension}')
    print("loaded "f'cogs.{extension}' + "...")

@client.command()
@commands.has_permissions(administrator=True)
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')
    print("unloaded "f'cogs.{extension}' + "...")

@client.command()
@commands.has_permissions(administrator=True)
async def reload(context, extension):
    client.reload_extension(f'cogs.{extension}')
    print("reloaded "f'cogs.{extension}' + "...")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#on_ready
@client.event
async def on_ready():

    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=".help"))

    general = await client.fetch_channel(791160100567384098)
    print("Bot is back up...")

client.run(Token, reconnect=True)
