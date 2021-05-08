import discord
import asyncio
import json
import os
from db import db
from os.path import isfile
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from termcolor import colored, cprint
from typing import Optional
from random import choice
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
from discord.ext.commands import Cog
from discord import Embed, Emoji
import sqlite3
import time
import log

class events(commands.Cog):
    def __init__(self, client, *args, **kwargs):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)
        db.connect("./data/database.db")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await log.on_member_join(self, member)

        try:
            db.execute("INSERT INTO users (UserID, GuildID) VALUES (?, ?)", member.id, member.guild.id)
            db.commit()
            await log.member_add_db(self, member)

        except Exception as error:
            await log.member_add_db_error(self, member)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await log.on_guild_join(self, guild)

        try:
            db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)
            db.commit()
            await log.guild_add_db(self, guild)

        except Exception as error:
            await log.guild_add_db_error(self, guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await log.on_member_remove(self, member)

        try:
            db.execute("DELETE FROM users WHERE (UserID = ?)", member.id)
            db.commit()
            await log.member_remove_db(self, member)

        except Exception as error:
            await log.member_remove_db_error(self, member)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await log.on_guild_remove(self, guild)

        try:
            db.execute("DELETE FROM guilds WHERE (GuildID = ?)", guild.id)
            db.commit()
            await log.on_guild_remove_db(self, guild)

        except Exception as error:
            await log.guild_remove_db_error(self, guild)

def setup(client):
    client.add_cog(events(client))
