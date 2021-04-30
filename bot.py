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
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.group(pass_context=True, invoke_without_command=True)
async def bot(context):   
    if context.invoked_subcommand is None:
        async with context.typing():
            await asyncio.sleep(1)
            embed = discord.Embed(
                title=".bot <?>", 
                description="You have found a *super command!* With this command you can do anything your heart desires, well almost...", 
                colour=0x9b59b6
            )   
            embed.set_footer(
                text="For more information on what this command does, type `bot .help`"
            )
            await context.reply(embed=embed, mention_author=False)
            
#    elif context.invoke_without_command:
#         print("test")
        

@bot.command()
@commands.is_owner()
async def load(context, extension):
    client.load_extension(f'cogs.{extension}')
    print(colored("[main]:", "magenta"), colored(f"Loaded cogs.{extension}...", "green"))
    embed = discord.Embed(
        title="Your wish is my command",
        description=f"Loaded cogs.{extension}",
        colour=0x9b59b6
    )
    embed.set_footer(
        text=".bot owner_notifs off to turn off notifs."
    )
    await context.reply(embed=embed, mention_author=False)

@bot.command()
@commands.is_owner()
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')
    print(colored("[main]:", "magenta"), colored(f"Unloaded cogs.{extension}...", "green"))
    embed = discord.Embed(
        title="Your wish is my command",
        description=f"Unloaded cogs.{extension}",
        colour=0x9b59b6
    )
    embed.set_footer(
        text=".bot owner_notifs off to turn off notifs."
    )
    await context.reply(embed=embed, mention_author=False)

@bot.command()
@commands.is_owner()
async def reload(context, extension):
    client.reload_extension(f'cogs.{extension}')
    print(colored("[main]:", "magenta"), colored(f"Reloaded cogs.{extension}...", "green"))
    embed = discord.Embed(
        title="Your wish is my command",
        description=f"Reloaded cogs.{extension}",
        colour=0x9b59b6
    )
    embed.set_footer(
        text=".bot owner_notifs off to turn off notifs."
    )
    await context.reply(embed=embed, mention_author=False)

@bot.command()
@commands.is_owner()
async def shutdown(context):
    await context.bot.logout()

@bot.command()
async def help(context):
    print(colored("[main]:", "magenta"), colored("command(help) used...", "green"))
    
    #page 1
    page_1 = discord.Embed(
        title="Index",
        description="The home page of the help command!", 
        colour=0x9b59b6
    )
    page_1.add_field(
        name="`General`",
        value="**The basic commands for day-to-day tasks.",
        inline=False
    )
    page_1.add_field(
        name="`Economy`", 
        value="A global market and trading system, complete with its own currency!",
        inline=False
    )
    page_1.add_field(
        name="`Games`", 
        value="Play with friends, compete with strangers, and make some extra :coin: while having fun!",
        inline=False
    )
    page_1.add_field(
        name="`Moderation`",
        value="Make sure your server is always under control, with an advanced toolset for your moderators, and auto-moderation for the tech-savvy!", 
        inline=False
    )
    page_1.set_footer(
        text="To scroll through pages, react to the arrows below."
    )

    #page 2
    page_2 = discord.Embed(
        title="General", 
        description="The overview of the general commands.", 
        colour=0x9b59b6
    )
    page_2.add_field(
        name="`help`", 
        value="If your reading this, you know what this command does :smile:",
        inline=False
    )
    page_2.add_field(
        name="`info`", 
        value="Displays bot status, ping, and other miscellaneous content.",
        inline=False
    )
    page_2.add_field(
        name="`serverinfo`",
        value="Displays server info, such as user count.",
        inline=False
    )
    page_2.add_field(
        name="`userinfo`,",
        value="Displays user info, such as xp, statistics, and rank.",
        inline=False
    )
    page_2.set_footer(
        text="To use these commands, type .bot <command_name>"
    )
    
    #page 3
    page_3 = discord.Embed(
        title="Economy", 
        description="A global market and trading system, complete with its own :coin:currency!", 
        colour=0x9b59b6
    )
    page_3.add_field(
        name="`wallet`",
        value="Check how many coins you own.",
        inline=False
    )
    page_3.add_field(
        name="`market`",
        value="See whats for sale, sell, and trade in a global market.",
        inline=False
    )
    page_3.add_field(
        name="`cap`",
        value="Check the current global/local market cap.",
        inline=False
    )
    page_3.set_footer(
        text="To use these commands, type .eco <command_name>"
    )

    page_4 = discord.Embed(
        title="Games", 
        description="Play with friends, compete with strangers, and make some extra coins all while having fun!", 
        colour=0x9b59b6
    )
    page_4.add_field(
        name="`count`",
        value="A counting game with multiple people and different modes for different occasions. More detail found in `game` help menu.",
        inline=False
    )
    page_4.add_field(
        name="`chess`",
        value="Match up with people and play for coins, or challenge @OneCoolBot for a very special prize!",
        inline=False
    )
    page_4.add_field(
        name="`roll`",
        value="Roll the die with friends to decide your fate, or for coins.",
        inline=False
    )
    
    page_4.add_field(
        name="`cave`",
        value="Play the collosal-cave-adventure terminal classic within discord!",
        inline=False
    )
    page_4.set_footer(
        text="To use these commands, type .game <command_name>. For more help on game commands, type .game help"
    )

    #page 5
    page_5 = discord.Embed(
        title="Moderation", 
        description="Make sure your server is always under control, with an advanced toolset for your moderators, and auto-moderation for the tech-savvy!", 
        colour=0x9b59b6
    )
    page_5.add_field(
        name="`clear` <message_amount>",
        value="Clear messages from a channel.",
        inline=False
    )
    page_5.add_field(
        name="`kick` <@member> <reason>",
        value="Kick mentioned member from server.",
        inline=False
    )
    page_5.add_field(
        name="`ban` <@member> <reason>",
        value="Ban mentioned member from server.",
        inline=False
    )
    page_5.add_field(
        name="`unban` <@member> <reason>",
        value="Unbans mentioned member from server.",
        inline=False
    )
    page_5.set_footer(
        text="Moderation commands are not args, and can be used as shown above."
    )

    message = await context.reply(embed=page_1, mention_author=False)
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    await message.add_reaction("❌")
    pages = 5
    current_page = 1

    def check(reaction, user):
        return user == context.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]

    while True:
        try:
            reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

            if str(reaction.emoji) == "▶️" and current_page != pages:
                current_page += 1

                if current_page == 2:
                    await message.edit(embed=page_2)
                    await message.remove_reaction(reaction, user)
                
                elif current_page == 3:
                    await message.edit(embed=page_3)
                    await message.remove_reaction(reaction, user)

                elif current_page == 4:
                    await message.edit(embed=page_4)
                    await message.remove_reaction(reaction, user)

                elif current_page == 5:
                    await message.edit(embed=page_5)
                    await message.remove_reaction(reaction, user)
            
            if str(reaction.emoji) == "◀️" and current_page > 1:
                current_page -= 1
                
                if current_page == 1:
                    await message.edit(embed=page_1)
                    await message.remove_reaction(reaction, user)

                elif current_page == 2:
                    await message.edit(embed=page_2)
                    await message.remove_reaction(reaction, user)
                
                elif current_page == 3:
                    await message.edit(embed=page_3)
                    await message.remove_reaction(reaction, user)

                elif current_page == 4:
                    await message.edit(embed=page_4)
                    await message.remove_reaction(reaction, user)

            if str(reaction.emoji) == "❌":
                await message.delete()
                break

            else:
                await message.remove_reaction(reaction, user)
                
        except asyncio.TimeoutError:
            await message.delete()
            #add context message delete here
            break

@bot.command()
async def info(context):
    print(colored("[main]:", "magenta"), colored("command(info) used...", "green"))
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

        embed = discord.Embed(
            title="Bot Info",
            description="Everything about me!",
            colour=0x9b59b6
        )
        embed.set_thumbnail(
            url=context.bot.user.avatar_url
        )
        embed.add_field(
            name="Developer",
            value="𝓣𝓲𝓶𝓶𝔂#6955"
        )
        embed.add_field(
            name="Users", 
            value=f"{len(context.guild.members)}", 
            inline=True
        )
        embed.add_field(
            name="Ping", 
            value=f"{before_ws}ms"
        )
        embed.add_field(
            name="RAM Usage", 
            value=f"{ramUsage:.2f} MB", 
            inline=True
        )
        embed.add_field(
            name="Uptime", 
            value=text, 
            inline=True
        )
        embed.add_field(
            name="Version", 
            value="Ver 0.1.4"
        )
        embed.set_footer(
            text="Most recent changes(rewrite): more args!"
        )

        message = await context.message.reply(embed=embed, mention_author=False)

# @client.command()
# async def help(context):
#     async with context.typing():
#         await asyncio.sleep(1)
#         embed = discord.Embed(colour=0x9b59b6)
#         embed.add_field(name="**Error :(**", value="Commands are categorized in sections. For help command, type **.bot help**")
#         await context.reply(embed=embed, mention_author=False)

client.run(Token, reconnect=True)
