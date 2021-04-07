import discord
import asyncio
import json
import os
from db import db
from os.path import isfile
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from termcolor import colored
from typing import Optional
from random import choice
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
from discord.ext.commands import Cog
from discord import Embed, Emoji
import sqlite3
import time

class misc(commands.Cog):
    def __init__(self, client, *args, **kwargs):
        self.client = client

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[misc]: online...", "green"))
        db.connect("./data/database.db")

    #on_member_join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(colored(f"[misc]: {member.name}#{member.discriminator} joined {member.guild}#{member.guild.id} at {current_time}...", "green"))

        try:
            db.execute("INSERT INTO users (UserID) VALUES (?)", member.id)
            db.commit()
            print(colored(f"[misc]: {member.name}#{member.discriminator} was added into the users table...", "green"))

        except:
            print(colored(f"[misc]: Error occurred when adding {member.name}#{member.discriminator} to users table...", "red"))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(colored(f"[misc]: Joined guild: {guild.name}#{guild.id}", "green"))

        try:
            db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)
            db.commit()
            print(colored(f"[misc]: {guild.name}#{guild.id} was added into the guilds table", "green"))

        except:
            print(colored(f"[misc]: Error occured when adding {guild.name}#{guild.id} to guilds table...", "red"))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(colored(f"[misc]: {member.name}#{member.discriminator} left from {member.guild}#{member.guild.id} at {current_time}...", "yellow"))

        try:
            db.execute("DELETE FROM users WHERE (UserID = ?)", member.id)
            db.commit()
            print(colored(f"[misc]: Removed {member.name}#{member.discriminator} from users table...", "yellow"))

        except:
            print(colored(f"[misc]: Error occurred when removing {member.id}#{member.discriminator} from users table...", "red"))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(colored(f"[misc]: Left guild: {guild.name}#{guild.id} at {current_time}..." "yellow"))

        try:
            db.execute("DELETE FROM guilds WHERE (GuildID = ?)", guild.id)
            db.commit()
            print(colored(f"[misc]: Removed {guild.name}#{guild.id} from guilds table...", "yellow"))

        except:
            print(colored(f"[misc]: Error occured when removing guild: {guild.name}#{guild.id} from guilds table...", "red"))







def setup(client):
    client.add_cog(misc(client))
