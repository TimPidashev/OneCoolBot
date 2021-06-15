import discord
import asyncio
import os
from db import db
from os.path import isfile
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from typing import Optional
from random import choice
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
from discord.ext.commands import Cog
from discord import Embed, Emoji
from discord.ext import commands, tasks
import asyncio
import sqlite3
import time
from db import db
from utils import log

class events(commands.Cog):
    def __init__(self, client, *args, **kwargs):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await log.on_member_join(self, member)
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await log.on_member_remove(self, member)
        pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await log.on_guild_join(self, guild)
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await log.on_guild_remove(self, guild)
        pass

def setup(client):
    client.add_cog(events(client))
