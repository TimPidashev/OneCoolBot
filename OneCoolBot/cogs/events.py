"""
MIT License

Copyright (c) 2021 Timothy Pidashev
"""


import discord
import asyncio
from discord import Member, Embed
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Cog
from discord import Embed, Emoji, Embed
from utils import db, log

class Events(commands.Cog):
    def __init__(self, client, *args, **kwargs):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)
    
    #ON_MEMBER_JOIN
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            db.execute("INSERT INTO users (UserID, GuildID) VALUES (?, ?)", member.id, member.guild.id)
            db.commit()
            await log.member_add_db(self, member)   

            channel = self.client.get_channel(791160100567384098)
            await asyncio.sleep(1)
            await channel.send(f"Hi there {member.mention} :wave: Thank You for joining the server! If you have any questions, just ask me a question.")

            role = member.guild.get_role(846972672402915348)
            await member.add_roles(role)
        
        except Exception as error:
            await log.member_add_db_error(self, member)
    
    #ON_MEMBER_LEAVE
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            db.execute("DELETE FROM users WHERE (UserID = ?)", member.id)
            db.commit()
            await log.member_remove_db(self, member)

        except Exception as error:
            await log.member_remove_db_error(self, member)

    @commands.Cog.listener()
    async def on_message(self, message):
         if not message.author.bot:
            context = await self.client.get_context(message)

            if context.command:
                return

            message = 1
            db.execute(f"UPDATE users SET GlobalMessageCount = GlobalMessageCount + ? WHERE UserID = {context.author.id}",
                message
            )
            db.commit()

def setup(client):
    client.add_cog(Events(client))
