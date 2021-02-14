import discord
import asyncio
import random
import sqlite3
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

def setup(client):
    client.add_cog(economy(client))
