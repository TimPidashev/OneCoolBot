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
import asyncpg
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
        try:
            await db.execute("INSERT INTO users (UserID, GuildID) VALUES (?, ?)", member.id, member.guild.id)
            await db.commit()
            await log.member_add_db(self, member)

        except Exception as error:
            await log.member_add_db_error(self, member)

    @commands.Cog.listener(self, member):
    async def on_member_remove(self, member):
        try:
            await db.execute("DELETE FROM users WHERE (UserID = ?)", member.id)
            await db.commit()
            await log.member_remove_db(self, member)

        except Exception as error:
            await log.member_remove_db_error(self, member)

    @commands.Cog.listener(self, member):
    async def on_guild_join(self, member):
        try:
            await db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)
            await db.commit()
            await log.guild_add_db(self, guild)

            try:
                await db.execute("INSERT INTO guildconfig (GuildID) VALUES (?)", guild.id)
                await db.commit()
                await log.guildconfig_add_db(self, guild)

            except Exception as error:
                await log.guild_config_add_db_error(self, guild)

        except Exception as error:
            await log.guild_add_db_error(self, guild)


    @commands.Cog.listener(self, member):
    async def on_guild_remove(self, member):
        try:
            await db.execute("DELETE FROM guilds WHERE (GuildID = ?)", guild.id)
            await db.commit()
            await log.on_guild_remove_db(self, guild)

            try:
                await db.execute("DELETE FROM guildconfig WHERE (GuildID = ?)", guild.id)
                await db.commit()
                await log.on_guild_remove_guildconfig(self, guild)

            except:
                await log.on_guild_remove_guildcofig_error(self, guild)

        except Exception as error:
            await log.guild_remove_db_error(self, guild)    



def setup(client):
    client.add_cog(events(client))
