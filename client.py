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
import log
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
log.logo()

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
        handler = logging.FileHandler(filename="./data/discord.log", encoding="utf-8", mode="w")
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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.group(pass_context=True, invoke_without_command=True)
async def bot(context): 
    await log.client_command(context)
    message = context.message  
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]

    if message.content == f"{prefix}bot":
        embed = discord.Embed(
            title=f"{prefix}bot <?>", 
            description="You have found a *super command!* With this command you can do anything your heart desires, well almost...", 
            colour=0x9b59b6
        )   
        embed.set_footer(
            text=f"For more information on what this command does, type {prefix}bot help"
        )
        await context.reply(embed=embed, mention_author=False)

    else:
        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.add_field(
            name="**Error :(**", 
            value=f"This is not a valid command. Try running `{prefix}bot help` for help with bot commands...", 
            inline=False
        )

        if context.author == context.guild.owner:
            embed.set_footer(
                text=f"To disable error messages, type: {prefix}bot error_notifs off"
            )

        await context.reply(embed=embed, mention_author=False)

@bot.command()
@commands.is_owner()
async def load(context, extension):
    await client.load_extension(f'cogs.{extension}')
    log.client_command(context)
    embed = discord.Embed(
        title="Your wish is my command",
        description=f"Loaded cogs.{extension}",
        colour=0x9b59b6
    )
    await context.reply(embed=embed, mention_author=False)

@bot.command()
@commands.is_owner()
async def unload(context, extension):
    client.unload_extension(f'cogs.{extension}')
    await log.client_command(context)
    embed = discord.Embed(
        title="Your wish is my command",
        description=f"Unloaded cogs.{extension}",
        colour=0x9b59b6
    )
    await context.reply(embed=embed, mention_author=False)

@bot.command()
@commands.is_owner()
async def reload(context, extension):
    client.reload_extension(f'cogs.{extension}')
    await log.client_command(context)
    embed = discord.Embed(
        title="Your wish is my command",
        description=f"Reloaded cogs.{extension}",
        colour=0x9b59b6
    )
    await context.reply(embed=embed, mention_author=False)

@bot.command()
async def help(context):
    await log.client_command(context)
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]
    
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
        name="`Music`",
        value="Listen to low-latency music streams for studying and hanging with friends in voice-chat!",
        inline=False
    )
    page_1.add_field(
        name="`Moderation`",
        value="Make sure your server is always under control, with an advanced toolset for your moderators, and auto-moderation for the tech-savvy!", 
        inline=False
    )
    page_1.add_field(
        name="`Settings`",
        value="Configure OneCoolBot with ease right in discord, with a dashboard coming later.",
        inline = False
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
        name="`userinfo`", 
        value="Displays user info, such as xp, statistics, and rank.",
        inline=False
    )
    page_2.set_footer(
        text=f"To use these commands, type {prefix}bot <command_name>"
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
        text=f"To use these commands, type {prefix}eco <command_name>"
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
        text=f"To use these commands, type {prefix}game <command_name>. For more help on game commands, type {prefix}game help"
    )
    
    #page 5
    page_5 = discord.Embed(
        title="Music",
        description="Listen to low-latency music streams for studying and hanging with friends in voice-chat!",
        colour=0x9b59b6
    )
    page_5.add_field(
        name="Commands",
        value="`connect` connect bot to voice chat\n`play` <search song to play>\n`pause` pause player\n`resume` resume player\n`skip` skip current song\n`stop`\n`volume` change volume\n`shuffle` shuffle queue\n`equalizer` change equalizer\n`queue` see songs queue\n`current` see currently played song\n`swap` swap song\n`music` see music status\n`spotify` see spotify rich presence",
        inline=False
    )
    page_5.set_footer(
        text=f"confused? use this handy command: {prefix}bot music help"
    )

    #page 6
    page_6 = discord.Embed(
        title="Moderation", 
        description="Make sure your server is always under control, with an advanced toolset for your moderators, and auto-moderation for the tech-savvy!", 
        colour=0x9b59b6
    )
    page_6.add_field(
        name=f"`{prefix}clear` <message_amount>",
        value="Clear messages from a channel.",
        inline=False
    )
    page_6.add_field(
        name=f"`{prefix}kick` <@member> <reason>",
        value="Kick mentioned member from server.",
        inline=False
    )
    page_6.add_field(
        name=f"`{prefix}ban` <@member> <reason>",
        value="Ban mentioned member from server.",
        inline=False
    )
    page_6.add_field(
        name=f"`{prefix}unban` <@member> <reason>",
        value="Unbans mentioned member from server.",
        inline=False
    )
    page_6.set_footer(
        text="Moderation commands are not args, and can be used as shown above."
    )

    message = await context.reply(embed=page_1, mention_author=False)
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

                elif current_page == 6:
                    await message.edit(embed=page_6)
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

                elif current_page == 5:
                    await message.edit(embed=page_5)
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
    await log.client_command(context)

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
        value="Ver 1.2.4"
    )
    embed.set_footer(
        text="Most recent changes: Added super-command(game)"
    )

    message = await context.message.reply(embed=embed, mention_author=False)

@bot.group(pass_context=True, invoke_without_command=True)
async def settings(context):
    await log.client_command(context)
    message = context.message  
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]

    if message.content == f"{prefix}bot settings":
        embed = discord.Embed(
            title=f"{prefix}settings <?>", 
            description="You have found a *sub command!* With this command you can do anything your heart desires, well almost...", 
            colour=0x9b59b6
        )   
        embed.set_footer(
            text=f"For more information on what this command does, type {prefix}bot settings help"
        )
        await context.reply(embed=embed, mention_author=False)

    else:
        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.add_field(
            name="**Error :(**", 
            value=f"This is not a valid command. Try running `{prefix}bot settings help` for help with settings commands...", 
            inline=False
        )

        if context.author == context.guild.owner:
            embed.set_footer(
                text=f"To disable error messages, type: {prefix}bot error_notifs off"
            )

        await context.reply(embed=embed, mention_author=False)

@settings.command()
async def help(context):
    await log.client_command(context)
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]
    
    #page 1
    page_1 = discord.Embed(
        title="Index",
        description="The home page of the settings sub-command!", 
        colour=0x9b59b6
    )
    page_1.add_field(
        name="`config`",
        value="Use this command to go through an easy setup of OneCoolBot",
        inline=False
    )
    page_1.add_field(
        name="`prefix`",
        value="Use this command to change my prefix!",
        inline=False
    )
    page_1.add_field(
        name="`level`", 
        value="Use this command to turn off levels, change level messages, and change where the level messages will be sent.",
        inline=False
    )
    page_1.set_footer(
        text="To scroll through pages, react to the arrows below."
    )

    #page 2
    page_2 = discord.Embed(
        title="General", 
        description="The overview of the commands.", 
        colour=0x9b59b6
    )
    page_2.add_field(
        name="`prefix`", 
        value=f"This command changes the prefix. Example: `{prefix}bot settings prefix <new_prefix>`",
        inline=False
    )
    page_2.add_field(
        name="`levels`", 
        value="Toggles level functionality on and off.",
        inline=False
    )
    page_2.add_field(
        name="`levelmessages`",
        value="Enables or disables level-messages.",
        inline=False
    )
    page_2.set_footer(
        text=f"To use these commands, type {prefix}bot settings <command_name> <args>"
    )

    message = await context.reply(embed=page_1, mention_author=False)
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
                    await message.edit(embed=page_2)
                    await message.remove_reaction(reaction, user)
            
            if str(reaction.emoji) == "◀️" and current_page > 1:
                current_page -= 1
                
                if current_page == 1:
                    await message.edit(embed=page_1)
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

@settings.command()
async def prefix(context, arg=None):
    await log.client_command(context)
    
    if arg is not None and context.author == context.guild.owner:

        db.execute(f"UPDATE guilds SET Prefix = ? WHERE GuildID = {context.guild.id}",
            arg
        )
        db.commit()

        prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
            context.guild.id,
        )[0]

        embed = discord.Embed(
            name="New Bot Prefix",
            colour=0x9b59b6
        )
        embed.add_field(
            name="Prefix Changed",
            value=f"The prefix was changed to `{prefix}`"
        )
        await context.reply(embed=embed, mention_author=False)
    
    if arg is None:
        prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
            context.guild.id,
        )[0]

        embed = discord.Embed(
            name="Bot Prefix",
            colour=0x9b59b6
        )
        embed.add_field(
            name="Current Prefix",
            value=f"The current prefix is `{prefix}`",
            inline=False
        )
        if context.author == context.guild.owner:
                embed.set_footer(
                    text=f"To change the prefix, use command: {prefix}bot prefix <new_prefix>"
                )
            
        await context.reply(embed=embed, mention_author=False)

@settings.command()
async def configuration(context):
    await log.client_command(context)
    if context.author == context.guild.owner:
        
        #page 1
        page_1 = discord.Embed(
            title="Bot Configuration",
            description="This one command will help you tell me how to power your server!", 
            colour=0x9b59b6
        )
        page_1.add_field(
            name="`How to use:`",
            value="Simply react to the specified reactions below to setup the bot!",
            inline=False
        )
        page_1.set_footer(
            text="To continue with setup, react with the checkmark!"
        )

        #page 2
        page_2 = discord.Embed(
            title="Prefix",
            description="Let's setup my prefix! This is what you will use to define my commands.",
            colour=0x9b59b6
        )
        page_2.set_footer(
            text="To pick a prefix, react to the specified prefix. These can ablways be changed later to prefixes not on this list!"
        )

        #page3
        page_3 = discord.Embed(
            title="Levels",
            description="Let's setup Levels!",
            colour=0x9b59b6
        )
        page_3.add_field(
            name="Firstly, do you want levels to be active on your server?",
            value="React below to continue",
            inline=False
        )

        page_4 = discord.Embed(
            title="Level Messages",
            description="Let's setup level messages!",
            colour=0x9b59b6
        )
        page_4.add_field(
            name="Do you want level messages anywhere in your server?",
            value="You can tell me to either dm the member, send to a specific level messages channel, or reply to the member!",
            inline=False
        )
        page_4.add_field(
            name="React to one of these reactions to choose your option!",
            value="1️⃣ `level messages in dms`\n2️⃣ `level messages replied in chat`\n3️⃣ `level messages in a setup channel`\n✖️ `level messages off`",
            inline=False
        )
        page_4.set_footer(
            text="React below to continue"
        )

        #page 5 
        page_5 = discord.Embed(
            title="Level Message",
            description="Setup a custom level message to send to your members!",
            colour=0x9b59b6
        )
        page_5.add_field(
            name="Default",
            value=f"The default level message is: :partying_face: {context.author.mention} is now level **5**!",
            inline=False
        )
        page_5.add_field(
            name="Options",
            value="✔️ `keep default`\n❕ `setup your own`",
            inline=False
        )
        page_5.set_footer(
            text="React below to continue"
        )

        #add update message

        message = await context.reply(embed=page_1, mention_author=False)
        await message.add_reaction("▶️")
        await message.add_reaction("❌")
        pages = 5
        current_page = 1

        def check(reaction, user):
            return user == context.author and str(reaction.emoji) in ["▶️", "❌", "🔘", "💲", "❔", "❕", "➕", "➖"]

        while True:
            try:
                reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" and current_page != pages:
                    current_page += 1

                    if current_page == 2:
                        await message.edit(embed=page_2)
                        await message.remove_reaction(reaction, user)
                        await message.remove_reaction("▶️")
                        await message.remove_reaction("❌")

                        await message.add_reaction("🔘")
                        await message.add_reaction("💲")
                        await message.add_reaction("❔")
                        await message.add_reaction("❕")
                        await message.add_reaction("➕")
                        await message.add_reaction("➖")

                    
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

                    elif current_page == 5:
                        await message.edit(embed=page_5)
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

    else:
        await context.reply("You are not the owner of this server!", mention_author=False)

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
            await context.reply("Levels are currently off.", mention_author=False)
            
        if levels == "ON":
            await context.reply("Levels are currently on.", mention_author=False)

client.loop.create_task(change_presence())
client.run(Token, reconnect=True)
