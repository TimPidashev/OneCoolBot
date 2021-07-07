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

guild_ids = [791160100567384094]

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
            colour=self.context.author.colour,
        )

        embed.set_thumbnail(url=self.context.guild.me.avatar_url)
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
        pass

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
        async with context.typing():
            await asyncio.sleep(1)
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



def setup(client):
    client.add_cog(Commands(client))