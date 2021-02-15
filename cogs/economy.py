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
        self.bot = client

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
            await context.channel.send(f"`Wallet`\n{target.display_name} has :coin: {coins[0]} coins and is rank {ids.index(target.id)+1} of {len(ids):} users globally.")

    @commands.command()
    async def market(self, context):
        print(f"[economy]: user {context.author} accessed the global market...", "blue"))

        async with context.typing():
            await asyncio.sleep(1)
            await context.channel.send(f"`Market`\nIn development!")

def setup(client):
    client.add_cog(economy(client))
