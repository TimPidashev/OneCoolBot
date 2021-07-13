import discord
from discord.ext import commands
from db import db
from utils import checks, colours, log
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, wait_for_component
from discord_slash.utils import manage_components
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
import time
from datetime import datetime, timedelta
import asyncio
import psutil
import json
from PIL import Image, ImageDraw, ImageFont, ImageFile, ImageFilter, ImagePath
import aiohttp
from typing import Optional
from io import BytesIO

guild_ids = [791160100567384094]

#loading bot config
with open("config.json") as file:
    config = json.load(file)

#LEADERBOARD GENERATOR
class Menu(ListPageSource):
    def __init__(self, context, data):
        self.context = context

        super().__init__(data, per_page=10)

    async def write_page(self, menu, offset, fields=[]):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(
            title="Leaderboard",
            colour=await colours.colour(self.context),
        )

        embed.set_thumbnail(url=self.context.guild.icon_url)
        embed.set_footer(
            text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} members."
        )

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        fields = []
        table = "\n".join(
            f"{idx+offset}. **{self.context.guild.get_member(entry[0]).name}** ~ `{entry[1]}`"
            for idx, entry in enumerate(entries)
        )

        fields.append(("Top members:", table))

        return await self.write_page(menu, offset, fields)

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        await log.online(self)

    #HELP 
    @cog_ext.cog_slash(
        name="help",
        description="A complete manual of help for the helpless!",
        guild_ids=guild_ids
    )
    async def help(self, context: SlashContext):
        await log.slash_command(self, context)
        page_1 = discord.Embed(
            title="Index",
            description="The home page of the help command!", 
            colour=await colours.colour(context)
        )
        fields = [("`General`", "**The basic commands for day-to-day tasks.", False),
                ("`Economy`", "A global market and trading system, complete with its own currency!", False),
                ("`Games`", "Play with friends, compete with strangers, and make some extra coins while having fun!", False),
                ("`Music`", "Listen to low-latency music streams for studying and hanging with friends in voice-chat!", False),
                ("`Moderation`", "Make sure your server is always under control, with an advanced toolset for your moderators, and auto-moderation for the tech-savvy!", False),
                ("`Settings`", "Configure OneCoolBot with ease right in discord, with a dashboard coming later.", False)]

        page_1.set_footer(
            text="To scroll through pages, react to the arrows below."
        )

        for name, value, inline in fields:
            page_1.add_field(name=name, value=value, inline=inline)

        page_2 = discord.Embed(
            title="General", 
            description="The overview of the general commands.", 
            colour=await colours.colour(context)
        )
        fields = [("`help`", "Your looking at this command.\n**subcommands:** `aliases`", False),
                ("`info`", "Displays bot status, ping, and other miscellaneous content.\n**subcommands:** `aliases` `help`", False),
                ("`serverinfo`", "Displays server info, such as user count.\n**subcommands:** `aliases` `help`", False),
                ("`userinfo`", "Displays user info, discord stats, and the like.\n**subcommands:** `aliases` `help`", False)]

        page_2.set_footer(
            text=f"Handy tip! To see what a command can do, use the `help` subcommand."
        )

        for name, value, inline in fields:
            page_2.add_field(name=name, value=value, inline=inline)

        page_3 = discord.Embed(
            title="Economy", 
            description="A global market and trading system, complete with its own currency!", 
            colour=await colours.colour(context)
        )
        fields = [("Under Construction!", "Economy is currently being polished and completely refactored. Should be complete in a weeek or two.", False)]

        for name, value, inline in fields:
            page_3.add_field(name=name, value=value, inline=inline)

        page_4 = discord.Embed(
            title="Games", 
            description="Play with friends, compete with strangers, and make some extra coins all while having fun!", 
            colour=await colours.colour(context)
        )
        fields = [("Under Construction!", "Games are currently being polished and completely refactored. ETA not known yet, be patient!", False)]

        for name, value, inline in fields:
            page_4.add_field(name=name, value=value, inline=inline)

        page_5 = discord.Embed(
            title="Music",
            description="Listen to low-latency music streams for studying and hanging with friends in voice-chat!",
            colour=await colours.colour(context)
        )
        fields = [("Commands", "`connect` connect bot to voice chat\n`play` <search song to play>\n`pause` pause player\n`resume` resume player\n`skip` skip current song\n`stop`\n`volume` change volume\n`shuffle` shuffle queue\n`equalizer` change equalizer\n`queue` see songs queue\n`current` see currently played song\n`swap` swap song\n`music` see music status\n`spotify` see spotify rich presence", False)]

        for name, value, inline in fields:
            page_5.add_field(name=name, value=value, inline=inline)

        page_5.set_footer(
            text=f"Music is stable, but will be refactored to use new discord features and spotify integration, including playlists!"
        )

        page_6 = discord.Embed(
            title="Moderation", 
            description="Make sure your server is always under control, with an advanced toolset for your moderators, and auto-moderation for the tech-savvy!", 
            colour=await colours.colour(context)
        )
        fields = [(f"`clear` <message_amount>", "Clear messages from a channel.", False),
                (f"`kick` <@member> <reason>", "Kick mentioned member from server.", False),
                (f"`ban` <@member> <reason>", "Ban mentioned member from server.", False),
                (f"`unban` <@member> <reason>", "Unbans mentioned member from server.", False)]

        for name, value, inline in fields:
            page_6.add_field(name=name, value=value, inline=inline)

        page_6.set_footer(
            text="Is being refactored, as is most of the bot lol. Will be complete and shiny with ai moderation soon!"
        )

        message = await context.send(embed=page_1)
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
                break

    #INFO
    @commands.command(aliases=["inf", "i"])
    async def info(self, context):
        await log.cog_command(self, context)

        before = time.monotonic()
        before_ws = int(round(self.client.latency * 1000, 1))
        ping = (time.monotonic() - before) * 1000
        ramUsage = self.client.process.memory_full_info().rss / 1024**2
        current_time = time.time()
        difference = int(round(current_time - self.client.start_time))
        uptime = str(timedelta(seconds=difference))
        users = len(self.client.users)

        info = discord.Embed(
        title="Bot Info",
        description="Everything about me!",
        colour=0x9b59b6
        )
        info.set_thumbnail(
            url=context.bot.user.avatar_url
        )
        fields = [("Developer", "𝓣𝓲𝓶𝓶𝔂#6955", True), 
                ("Users", f"{users}", True),
                ("Latency", f"{before_ws}ms", True),
                ("RAM Usage", f"{ramUsage:.2f} MB", True), 
                ("Uptime", uptime, True), 
                ("Version", self.client.version, True)]

        info.set_footer(
            text="Fix backend for the most part."
        )

        for name, value, inline in fields:
            info.add_field(name=name, value=value, inline=inline)

        await context.reply(embed=info, mention_author=False)

    
    #USER
    @commands.command(aliases=["usrinf", "ui"])
    async def userinfo(self, context, user: discord.Member = None):
        await log.cog_command(self, context)

        if isinstance(context.channel, discord.DMChannel):
            return

        if user is None:
            user = context.author 

        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.set_author(
            name=str(user), 
            icon_url=user.avatar_url
        )
        
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        members = sorted(context.guild.members, key=lambda m: m.joined_at)
        date_format = "%a, %d %b %Y at %I:%M %p"

        top_role = user.top_role
        
        fields = [("Joined this server at", user.joined_at.strftime(date_format), True),
                  ("Registered this account at", user.created_at.strftime(date_format), False),
                  ("Server join position", str(members.index(user)+1), True),
                  ("Roles [{}]".format(len(user.roles)-1), top_role.mention, True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(
            text="ID: " + str(user.id)
        )
        await context.reply(embed=embed, mention_author=False)

    #LEADERBOARD
    @commands.command(aliases=["lb"])
    async def leaderboard(self, context):
        await log.cog_command(self, context)
        records = db.records("SELECT UserID, XP FROM users ORDER BY XP DESC")
        menu = MenuPages(source=Menu(context, records), clear_reactions_after=True, timeout=100.0)
        await menu.start(context)


    #COLORTHEME
    @cog_ext.cog_slash(
        name="colortheme", 
        description="Per-user color customizability!", 
        guild_ids=guild_ids,
        options=[
            create_option(
                name="colortheme",
                description="Change my color theme!",
                required=False,
                option_type=3,
                choices=[
                    create_choice(
                        name="black",
                        value="black,0"
                    ),
                    create_choice(
                        name="teal",
                        value="teal,0x1abc9c"
                    ),
                    create_choice(
                        name="dark teal",
                        value="dark teal,0x11806a"
                    ),
                    create_choice(
                        name="green",
                        value="green,0x2ecc71"
                    ),
                    create_choice(
                        name="dark green",
                        value="dark green,0x1f8b4c"
                    ),
                    create_choice(
                        name="blue",
                        value="blue,0x3498db"
                    ),
                    create_choice(
                        name="dark blue",
                        value="dark blue,0x206694"
                    ),
                    create_choice(
                        name="purple",
                        value="purple,0x9b59b6"
                    ),
                    create_choice(
                        name="dark purple",
                        value="dark purple,0x71368a"
                    ),
                    create_choice(
                        name="magenta",
                        value="magenta,0xe91e63"
                    ),
                    create_choice(
                        name="dark magenta",
                        value="dark magenta,0xad1457"
                    ),
                    create_choice(
                        name="gold",
                        value="gold,0xf1c40f"
                    ),
                    create_choice(
                        name="dark gold",
                        value="dark gold,0xc27c0e"
                    ),
                    create_choice(
                        name="orange",
                        value="orange,0xe67e22"
                    ),
                    create_choice(
                        name="dark orange",
                        value="dark orange,0xa84300"
                    ),
                    create_choice(
                        name="red",
                        value="red,0xe74c3c"
                    ),
                    create_choice(
                        name="dark red",
                        value="dark red,0x992d22"
                    ),
                    create_choice(
                        name="lighter grey",
                        value="lighter grey,0x95a5a6s"
                    ),
                    create_choice(
                        name="light grey",
                        value="light grey,0x979c9f"
                    ),
                    create_choice(
                        name="dark grey",
                        value="dark grey,0x607d8b"
                    ),
                    create_choice(
                        name="darker grey",
                        value="darker grey,0x546e7a"
                    ),
                    create_choice(
                        name="greyple",
                        value="greyple,0x99aab5"
                    ),
                    create_choice(
                        name="blurple",
                        value="blurple,0x7289da"
                    )

                ]
    
            )
        ],
        connector={
            "colortheme": "colortheme"
        }
    )

    async def settings(self, context: SlashContext, colortheme: str):
        await log.slash_command(self, context)
        if colortheme:
            #add rainbow and custom colorthemes as purchases in economy later!
            color, value = colortheme.split(",")
            await colours.change_colour(context, value)
            embed = discord.Embed(colour=await colours.colour(context))
            embed.add_field(
                name="Color Theme",
                value=f"Color theme changed to `{color}`",
                inline=True
            )
            await context.send(embed=embed)
        
        else:
            return

    #RANK
    @commands.command(aliases=["rnk"])
    async def rank(self, context, target: Optional[Member]):
        await log.cog_command(self, context)
        target = target or context.author
        if target is not None:
            exp, level = db.record(f"SELECT XP, Level FROM users WHERE (guildID, UserID) = (?, ?)",
                target.guild.id,
                target.id
            )
            ids = db.column(f"SELECT UserID FROM users WHERE GuildID = {target.guild.id} ORDER BY XP DESC")
            message_count = db.record(f"SELECT GlobalMessageCount FROM users WHERE UserID = {context.author.id} and GuildID = {context.guild.id}")[0]

        if exp or level is not None:
            rank = f"{ids.index(target.id)+1}"
            xp = exp
            user_name = str(target.nick or target.display_name)
            discriminator = f"#{target.discriminator}"

            final_xp_calc = int((level + 1) ** (20 / 11) * 42)
            final_xp = final_xp_calc + xp  
            
            rank_background = db.record(f"SELECT RankBackground FROM usersettings WHERE UserID = {target.id}")[0]

            if rank_background == "None":
                background = Image.new("RGB", (1000, 240))

            else:
                with Image.open(rank_background, "r") as f:
                    background = f.convert("RGB")
                
    
            async with aiohttp.ClientSession() as session:
                async with session.get(str(target.avatar_url)) as response:
                    image = await response.read()
                    icon = Image.open(BytesIO(image)).convert("RGBA").resize((200, 200))
                    bigsize = (icon.size[0] * 3, icon.size[1] * 3)
                    mask = Image.new("L", bigsize, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0) + bigsize, 255)
                    mask = mask.resize(icon.size, Image.ANTIALIAS)
                    icon.putalpha(mask)
                    background.paste(icon, (20, 20), mask=icon)
                    draw = ImageDraw.Draw(background, "RGB")
                    big_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 60, encoding="utf-8")
                    medium_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 40, encoding="utf-8")
                    small_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 30, encoding="utf-8")

                    text_size = draw.textsize(str(level), font=big_font)
                    offset_x = 1000 - 15 - text_size[0]
                    offset_y = 10
                    draw.text((offset_x, offset_y), str(level), font=big_font, fill=await colours.colour_hex(context, target))
                    text_size = draw.textsize("LEVEL", font=small_font)
                    offset_x -= text_size[0] + 5
                    draw.text((offset_x, offset_y + 27), "LEVEL", font=small_font, fill="#fff")

                    text_size = draw.textsize(f"#{rank}", font=big_font)
                    offset_x -= text_size[0] + 15
                    draw.text((offset_x, offset_y), f"{rank}", font=big_font, fill=await colours.colour_hex(context, target))
                    text_size = draw.textsize("RANK", font=small_font)
                    offset_x -= text_size[0] + 5
                    draw.text((offset_x, offset_y + 27), "RANK", font=small_font, fill="#fff")
                    
                    text_size = draw.textsize(f"{message_count}", font=big_font)
                    offset_x -= text_size[0] + 50
                    draw.text((offset_x, offset_y), f"{message_count}", font=big_font, fill=await colours.colour_hex(context, target))
                    text_size = draw.textsize("KARMA", font=small_font)
                    offset_x -= text_size[0] + 10
                    draw.text((offset_x, offset_y + 27), "KARMA", font=small_font, fill="#fff")

                    bar_offset_x = 320
                    bar_offset_y = 160
                    bar_offset_x_1 = 950
                    bar_offset_y_1 = 200
                    circle_size = bar_offset_y_1 - bar_offset_y
                    draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")
                    draw.ellipse(
                        (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill=await colours.colour_hex(context, target)
                    )
                    draw.ellipse(
                        (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#727175"
                    )
                    bar_length = bar_offset_x_1 - bar_offset_x
                    progress = (final_xp - xp) * 100 / final_xp
                    progress = 100 - progress
                    progress_bar_length = round(bar_length * progress / 100)
                    bar_offset_x_1 = bar_offset_x + progress_bar_length
                    draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill=await colours.colour_hex(context, target))
                    draw.ellipse(
                        (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill=await colours.colour_hex(context, target)
                    )
                    draw.ellipse(
                        (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill=await colours.colour_hex(context, target)
                    )
                    text_size = draw.textsize(f"/ {final_xp} XP", font=small_font)
                    offset_x = 950 - text_size[0]
                    offset_y = bar_offset_y - text_size[1] - 10
                    draw.text((offset_x, offset_y), f"/ {final_xp:,} XP", font=small_font, fill="#727175")
                    text_size = draw.textsize(f"{xp:,}", font=small_font)
                    offset_x -= text_size[0] + 8
                    draw.text((offset_x, offset_y), f"{xp:,}", font=small_font, fill="#fff")
                    text_size = draw.textsize(user_name, font=medium_font)
                    offset_x = bar_offset_x
                    offset_y = bar_offset_y - text_size[1] - 5
                    draw.text((offset_x, offset_y), user_name, font=medium_font, fill="#fff")
                    offset_x += text_size[0] + 5
                    offset_y += 10
                    draw.text((offset_x, offset_y), discriminator, font=small_font, fill="#727175")
                    background.show()

                    background.save("./data/img/imgswap.png")
                    ffile = discord.File("./data/img/imgswap.png")
                    await context.reply(file=ffile, mention_author=False)
                       
        else:
            await context.reply("You are not in the database :(\nDon't worry though, you were just added! Try running the command again.", mention_author=False)

    #test rank_background
    @commands.command()
    @commands.check(checks.is_owner)
    async def rb(self, context, arg, target: Optional[Member]):
        target = target or context.author

        db.execute(f"UPDATE usersettings SET RankBackground = ? WHERE UserID = ?",
            arg,
            target.id
        )

    @commands.command(aliases=["atm"])
    @commands.check(checks.is_owner)
    async def add_to_market(self, context, name, category, quantity, price):
        embed = discord.Embed(colour=await colours.colour(context))

        db.execute(f"INSERT INTO globalmarket (ItemName, Category, QuantityAvailable, QuantityLimit, Price) VALUES (?, ?, ?, ?, ?)", 
            name, 
            category, 
            quantity, 
            quantity,
            price
        )
        db.commit()
         
        fields = [("`Market`", f"New item added by {context.author.name}", True),
                  ("`Name`", name, False),
                  ("`category`", category, True),
                  ("`quantity`", quantity, True),
                  ("`price`", f":coin: {price}", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await context.reply(embed=embed, mention_author=False)

    #TICKETS
    @cog_ext.cog_slash(
        name="ticket",
        description="Send an request to become a @project maintainer",
        guild_ids=guild_ids,
        options=[
            create_option(
                name="name",
                description="What is the name of the project you would like to share?",
                required=True,
                option_type=3
            ),
            create_option(
                name="description",
                description="What is the description of the project you would like to share?",
                required=True,
                option_type=3
            )
        ]
    )
    async def ticket(self, context: SlashContext, name: str, description: str):
        await log.slash_command(self, context)
        db.execute(f"INSERT INTO tickets (UserID, ProjectName, ProjectDescription) VALUES (?, ?, ?)",
            context.author.id,
            name,
            description
        )
        db.commit()

        await context.send("Your ticket has been sent! You will be notified when an admin responds to your ticket.")

        embed = discord.Embed(colour=await colours.colour(context))
        embed.add_field(name=f"Ticket for a project", value=f"**Name:** `{name}`\n**Description:**\n{description}", inline=False)
        embed.set_author(name=f"Requested by: {context.author.name}", icon_url=context.author.avatar_url)
        embed.set_footer(text=f"Vote if this project will become a part of the DevelopingThings watchlist.")
        
        admins = self.client.get_channel(863918584366104627)

        message = await admins.send(embed=embed)
        await message.add_reaction("✔️")
        await message.add_reaction("❌")

        def check(reaction, user):
            return user in config["owner_ids"] and str(reaction.emoji) in ["✔️", "❌"]

        while True:
            try:
                reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "✔️":
                    pass

                if str(reaction.emoji) == "❌":
                    pass

                else:
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                break
        

        
def setup(client):
    client.add_cog(Commands(client))