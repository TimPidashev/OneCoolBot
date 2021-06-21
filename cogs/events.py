import discord
import asyncio
from discord import Member, Embed
from discord.ext import commands
from utils import log
from db import db

class events(commands.Cog):
    def __init__(self, client, *args, **kwargs):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            db.execute("INSERT INTO users (UserID, GuildID) VALUES (?, ?)", member.id, member.guild.id)
            db.commit()
            await log.member_add_db(self, member)

        except Exception as error:
            await log.member_add_db_error(self, member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            db.execute("DELETE FROM users WHERE (UserID = ?)", member.id)
            db.commit()
            await log.member_remove_db(self, member)

        except Exception as error:
            await log.member_remove_db_error(self, member)

    @commands.Cog.listener()
    async def on_guild_join(self, member):
        try:
            db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)
            db.commit()
            await log.guild_add_db(self, guild)

            try:
                db.execute("INSERT INTO guildconfig (GuildID) VALUES (?)", guild.id)
                db.commit()
                await log.guildconfig_add_db(self, guild)

            except Exception as error:
                await log.guild_config_add_db_error(self, guild)

        except Exception as error:
            await log.guild_add_db_error(self, guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, member):
        try:
            db.execute("DELETE FROM guilds WHERE (GuildID = ?)", guild.id)
            db.commit()
            await log.on_guild_remove_db(self, guild)

            try:
                db.execute("DELETE FROM guildconfig WHERE (GuildID = ?)", guild.id)
                db.commit()
                await log.on_guild_remove_guildconfig(self, guild)

            except:
                await log.on_guild_remove_guildcofig_error(self, guild)

        except Exception as error:
            await log.guild_remove_db_error(self, guild)    


def setup(client):
    client.add_cog(events(client))
