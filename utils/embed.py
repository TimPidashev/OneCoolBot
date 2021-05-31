from db import db
import discord
import asyncio
import sqlite3
import json
import os

db.connect("./data/database.db")

#info
async def info(context, users, before_ws, ramUsage, uptime):
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
              ("Version", "Ver 1.2.6", True)]

    info.set_footer(
        text="Most recent changes: AI now works!"
    )

    for name, value, inline in fields:
        info.add_field(name=name, value=value, inline=inline)
    
    return info

#userinfo
async def userinfo(context, user):
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
    date_format = "%a, %d %b %Y %I:%M %p"

    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
    
    fields = [("Joined", user.joined_at.strftime(date_format), False),
              ("Join position", str(members.index(user)+1), True),
              ("Registered", user.created_at.strftime(date_format), True),
              ("Roles [{}]".format(len(user.roles)-1), role_string, False)]
            #   ("Guild permissions", perm_string, False)
    
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    embed.set_footer(
        text="ID: " + str(user.id)
    )

    return embed

#help
async def help_page_1(context):
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]
    
    page_1 = discord.Embed(
        title="Index",
        description="The home page of the help command!", 
        colour=0x9b59b6
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

    return page_1

async def help_page_2(context):
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]

    page_2 = discord.Embed(
        title="General", 
        description="The overview of the general commands.", 
        colour=0x9b59b6
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
    
    return page_2

async def help_page_3(context):
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]

    page_3 = discord.Embed(
        title="Economy", 
        description="A global market and trading system, complete with its own currency!", 
        colour=0x9b59b6
    )
    fields = [("Under Construction!", "Economy is currently being polished and completely refactored. Should be complete in a weeek or two.", False)]

    for name, value, inline in fields:
        page_3.add_field(name=name, value=value, inline=inline)

    return page_3

async def help_page_4(context):
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]

    page_4 = discord.Embed(
        title="Games", 
        description="Play with friends, compete with strangers, and make some extra coins all while having fun!", 
        colour=0x9b59b6
    )
    fields = [("Under Construction!", "Games are currently being polished and completely refactored. ETA not known yet, be patient!", False)]

    for name, value, inline in fields:
        page_4.add_field(name=name, value=value, inline=inline)

    return page_4

async def help_page_5(context):
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]

    page_5 = discord.Embed(
        title="Music",
        description="Listen to low-latency music streams for studying and hanging with friends in voice-chat!",
        colour=0x9b59b6
    )
    fields = [("Commands", "`connect` connect bot to voice chat\n`play` <search song to play>\n`pause` pause player\n`resume` resume player\n`skip` skip current song\n`stop`\n`volume` change volume\n`shuffle` shuffle queue\n`equalizer` change equalizer\n`queue` see songs queue\n`current` see currently played song\n`swap` swap song\n`music` see music status\n`spotify` see spotify rich presence", False)]
    
    for name, value, inline in fields:
        page_5.add_field(name=name, value=value, inline=inline)

    page_5.set_footer(
        text=f"Music is stable, but will be refactored to use new discord features and spotify integration, including playlists!"
    )

    return page_5

async def help_page_6(context):
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]

    page_6 = discord.Embed(
        title="Moderation", 
        description="Make sure your server is always under control, with an advanced toolset for your moderators, and auto-moderation for the tech-savvy!", 
        colour=0x9b59b6
    )
    fields = [(f"`{prefix}clear` <message_amount>", "Clear messages from a channel.", False),
              (f"`{prefix}kick` <@member> <reason>", "Kick mentioned member from server.", False),
              (f"`{prefix}ban` <@member> <reason>", "Ban mentioned member from server.", False),
              (f"`{prefix}unban` <@member> <reason>", "Unbans mentioned member from server.", False)]

    for name, value, inline in fields:
        page_6.add_field(name=name, value=value, inline=inline)

    page_6.set_footer(
        text="Is being refactored, as is most of the bot lol. Will be complete and shiny with ai moderation soon!"
    )

    return page_6

async def serverinfo(context):
    embed = discord.Embed(
        title="Server Info",
        colour=0x9b59b6
    )
    embed.set_thumbnail(
        url=context.guild.icon_url
    )

    fields = [("Owner", context.guild.owner, False),
              ("Region", context.guild.region, False),
              ("Created At", context.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
              ("Members", len(context.guild.members), False)]

    for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

    return embed

async def settings(context, prefix):
    embed = discord.Embed(
        title=f"{prefix}settings <?>", 
        description="You have found a *sub command!* With this command you can do anything your heart desires, well almost...", 
        colour=0x9b59b6
    )   
    embed.set_footer(
        text=f"For more information on what this command does, type {prefix}settings help"
    )
    
    return embed

async def settings_help_page_1(context):
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]
    
    page_1 = discord.Embed(
        title="Index",
        description="The home page of the settings sub-command!", 
        colour=0x9b59b6
    )
    fields = [("`config`", "Use this command to go through an easy setup of OneCoolBot", False),
              ("`prefix`", "Use this command to change my prefix!", False),
              ("`level`", "Use this command to turn off levels, change level messages, and change where the level messages will be sent.", False)]

    page_1.set_footer(
        text="To scroll through pages, react to the arrows below."
    )

    return page_1

async def settings_help_page_2(context):
    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
        context.guild.id,
    )[0]
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

    return page_2

async def economy(context, prefix):
    embed = discord.Embed(
        title=f"{prefix}economy <?>", 
        description="You have found a *super command!* With this command you can do anything your heart desires, well almost...", 
        colour=0x9b59b6
    )   
    embed.set_footer(
        text=f"For more information on what this command does, type {prefix}economy help"
    )
    return embed

async def wallet(context, target):
    target = target or context.author
    ids = db.column("SELECT UserID FROM users ORDER BY Coins DESC")
    coins = db.record("SELECT Coins FROM users WHERE UserID = ?", target.id)
    embed = discord.Embed(
        colour=0x9b59b6
    )
    embed.add_field(
        name=f"**Wallet:**",
        value=f"**{target.display_name}** has :coin: **{coins[0]}** coins and is rank **{ids.index(target.id)+1}** of {len(ids):} users globally.",
        inline=False
    )
    
    return embed

async def cap(context):
    cap = db.record("SELECT sum(Coins) FROM users")
    embed = discord.Embed(
        colour=0x9b59b6
    )
    embed.add_field(
        name=f"**Current Market Cap:**", 
        value=f"There are currently :coin: **{cap[0]}** coins widespread globally"
    )
    
    return embed

async def market(context):
    embed = discord.Embed(
        title="**Market:**", 
        colour=0x9b59b6
    )
    embed.set_footer(
        text="See whats for sale!"
    )

    return embed

async def economy_help_page_1(context):
    #page 1
    page_1 = discord.Embed(
        title="Economy",
        description="The home page of the economy super-command!", 
        colour=0x9b59b6
    )
    page_1.add_field(
        name="`Under Construction`",
        value="This command is still under construction! Shhhh, 𝓣𝓲𝓶𝓶𝔂 has a headache!",
        inline=False
    )
    page_1.set_footer(
        text="To scroll through pages, react to the arrows below."
    )

    return page_1