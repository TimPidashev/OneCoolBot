import discord
import asyncio
import random
import sqlite3
import time
import os
from db import db
from os.path import isfile
from typing import Optional
from termcolor import colored, cprint
from discord.ext import commands
from discord import Member, Embed
from datetime import datetime
from discord.ext.menus import MenuPages, ListPageSource

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[economy]:", "magenta"), colored("online...", "green"))
        db.connect("./data/database.db")

    
    
def setup(client):
    client.add_cog(economy(client))
