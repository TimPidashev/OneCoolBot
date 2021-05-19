import discord
import asyncio
import random
import sqlite3
import time
import os
from utils import data, embed, log
from db import db
from os.path import isfile
from typing import Optional
from termcolor import colored, cprint
from discord.ext import commands
from discord import Member, Embed
from datetime import datetime
from discord.ext.menus import MenuPages, ListPageSource
from discord.utils import get
from random import choice
from discord.ext.commands import Cog
from discord import Embed, Emoji

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)
        data.connect()

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["eco", "e"])
    async def economy(self, context):
        await log.cog_command(self, context)
        message = context.message  
        prefix = await data.get_prefix(context)

        if message.content == f"{prefix}economy" or f"{prefix}eco" or f"{prefix}e":
            await context.reply(embed=await data.economy(context, prefix), mention_author=False)
        
        else:
            await context.reply("**Error :(**\nThis is not a valid command. Use this handy command `{prefix}economy help` to help you out.", mention_author=False)

    @economy.command(aliases=["wllt", "wt", "w"])
    async def wallet(self, context, target: Optional[Member]):
        await log.cog_command(self, context)
        await context.reply(embed=await embed.wallet(context, target), mention_author=False)

    @economy.command(aliases=["cp", "c"])
    async def cap(self, context):
        await log.cog_command(self, context)
        await context.reply(embed=await embed.cap(context), mention_author=False)

    @economy.command(aliases=["mrkt", "mrk", "mk", "m"])
    async def market(self, context):
        await log.cog_command(self, context)
        await context.reply(embed=await embed.market(context), mention_author=False)

    @economy.command(aliases=["hlp", "h"])
    async def help(self, context):
        await log.cog_command(self, context)
        message = await context.reply(embed=await embed.economy_help_page_1(context), mention_author=False)
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("❌")
        pages = 1
        current_page = 1

        def check(reaction, user):
            return user == context.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]

        while True:
            try:
                reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" and current_page != pages:
                    current_page += 1

                    if current_page == 2:
                        await message.edit(embed=page_1)
                        await message.remove_reaction(reaction, user)
                
                if str(reaction.emoji) == "◀️" and current_page > 1:
                    current_page -= 1
                    
                    if current_page == 1:
                        await message.edit(embed=page_1)
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

def setup(client):
    client.add_cog(economy(client))
