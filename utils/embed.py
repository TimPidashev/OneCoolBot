from db import db
import discord
import asyncio
import sqlite3
import json
import os

db.connect("./data/database.db")

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

