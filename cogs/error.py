import discord
import traceback
import wavelink
import sys
import aiohttp
from discord.ext import commands
from termcolor import colored, cprint
from discord import Member, Embed
from discord.utils import get
import asyncio
import sqlite3
from db import db
from utils import embed, log

class error(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass
        
def setup(client):
    client.add_cog(error(client))
