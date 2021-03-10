import discord
import asyncio
import random
import sqlite3
import time
import os
from db import db
from os.path import isfile
from typing import Optional
from termcolor import colored
from discord.ext import commands
from discord import Member, Embed
from datetime import datetime, timedelta
from discord.ext.menus import MenuPages, ListPageSource

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[economy]: online...", "blue"))
        db.connect("./data/database.db")

    @commands.command()
    async def wallet(self, context, target: Optional[Member]):
        print(colored(f"[economy]: user {context.author} checked his wallet...", "blue"))

        target = target or context.author
        ids = db.column("SELECT UserID FROM users ORDER BY Coins DESC")

        coins = db.record("SELECT Coins FROM users WHERE UserID = ?", target.id)

        async with context.typing():
            await asyncio.sleep(1)
            embedColour = discord.Embed.Empty
            if hasattr(context, 'guild') and context.guild is not None:
                embedColour = context.me.top_role.colour
            embed = discord.Embed(colour=embedColour)
            embed.add_field(name=f"**Wallet:**", value=f"**{target.display_name}** has :coin: **{coins[0]}** coins and is rank **{ids.index(target.id)+1}** of {len(ids):} users globally.")
            await context.message.channel.send(embed=embed)

    @commands.command()
    async def cap(self, context):
        print(colored(f"[economy]: user {context.author} accessed cap...", "blue"))

        cap = db.record("SELECT sum(Coins) FROM users")
        #await context.channel.send(f"There are currently :coin: **{cap[0]}** coins widespread globally.")

        async with context.typing():
            await asyncio.sleep(1)

            embedColour = discord.Embed.Empty
            if hasattr(context, 'guild') and context.guild is not None:
                embedColour = context.me.top_role.colour

            embed = discord.Embed(colour=embedColour)
            embed.add_field(name=f"**Current Market Cap:**", value=f"There are currently :coin: **{cap[0]}** coins widespread globally")
            await context.message.channel.send(embed=embed)

    @commands.command()
    async def market(self, context):
        print(colored(f"[economy]: user {context.author} accessed the global market...", "blue"))

        async with context.typing():
            await asyncio.sleep(1)
            await context.channel.send(f"`Market`\nIn development!")

    @commands.command()
    async def give(self, context):
        print(colored("[economy]: Command give was used..", "blue"))
        async with context.typing():
            await asyncio.sleep(1)
            await context.channel.send("This command is still in development, go bug 𝓣𝓲𝓶𝓶𝔂 to update!")

    @commands.command()
    async def me(self, context):
        print(colored("[economy]: Command me was used..", "blue"))
        async with context.typing():
            await asyncio.sleep(1)
            await context.channel.send("This command is still in development, go bug 𝓣𝓲𝓶𝓶𝔂 to update!")

    @commands.command()
    async def sell(self, context):
        print(colored("[economy]: Command sell was used...", "blue"))
        async with context.typing():
            await asyncio.sleep(1)
            await context.channel.send("This command is still in development, go bug 𝓣𝓲𝓶𝓶𝔂 to update!")

def setup(client):
    client.add_cog(economy(client))
