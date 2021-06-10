import discord
import asyncio
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
from utils import log

guild_id = [791160100567384094]

class devthings(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        await log.online(self)
        db.connect("./data/database.db")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild == guild_id:
            
            role = member.guild.get_role(846972672402915348)
            await member.add_roles(role)

        else:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = 815307066473578516

        if payload.message_id == message_id:
            member = payload.member
            guild = member.guild
            emoji = payload.emoji.name

            if emoji == "javascript":
                role = member.guild.get_role(811690417912807474)
                await member.add_roles(role)

            if emoji == "python":
                role = member.guild.get_role(811689718826795019)
                await member.add_roles(role)

            if emoji == "java":
                role = member.guild.get_role(811690475865374731)
                await member.add_roles(role)

            if emoji == "ruby":
                role = member.guild.get_role(815301345493516308)
                await member.add_roles(role)

            if emoji == "php":
                role = member.guild.get_role(815300280324194325)
                await member.add_roles(role)

            if emoji == "cplusplus":
                role = member.guild.get_role(815302655579914300)
                await member.add_roles(role)

            if emoji == "csharp":
                role = member.guild.get_role(815301348865998920)
                await member.add_roles(role)

            if emoji == "justc":
                role = member.guild.get_role(815300912292691979)
                await member.add_roles(role)

            if emoji == "typescript":
                role = member.guild.get_role(815301223623426069)
                await member.add_roles(role)

            #figure out a simple elif to remove emoji on raw_reaction_remove if possible here...

            else:
                return

        else:
            return

def setup(client):
    client.add_cog(devthings(client))

    