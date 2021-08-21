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

#DevelopingThings GuildID
devthings_guild_id = (791160100567384094)

class Events(commands.Cog):
    def __init__(self, client, *args, **kwargs):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)
    
    #ON_MEMBER_JOIN
    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        #this is just so my server works atm, anything and everything like this that is static will be rewritten really sooon
        message = self.client.get_channel(791160100567384098)
        await asyncio.sleep(1)
        await message.send(f"Hi there {member.mention} :wave: Thank You for joining the server! If you have any questions, just ask me a question.")
        if member.guild.id == devthings_guild_id:    
            role = member.guild.get_role(846972672402915348)
            await member.add_roles(role)

        else:
            pass

        try:
            db.execute("INSERT INTO users (UserID, GuildID) VALUES (?, ?)", member.id, member.guild.id)
            db.commit()
            await log.member_add_db(self, member)   
        
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

   
    #EMOJI TO ROLE LISTENER
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

            elif emoji == "python":
                role = member.guild.get_role(811689718826795019)
                await member.add_roles(role)

            elif emoji == "java":
                role = member.guild.get_role(811690475865374731)
                await member.add_roles(role)

            elif emoji == "ruby":
                role = member.guild.get_role(815301345493516308)
                await member.add_roles(role)

            elif emoji == "php":
                role = member.guild.get_role(815300280324194325)
                await member.add_roles(role)

            elif emoji == "cplusplus":
                role = member.guild.get_role(815302655579914300)
                await member.add_roles(role)

            elif emoji == "csharp":
                role = member.guild.get_role(815301348865998920)
                await member.add_roles(role)

            elif emoji == "justc":
                role = member.guild.get_role(815300912292691979)
                await member.add_roles(role)

            elif emoji == "typescript":
                role = member.guild.get_role(815301223623426069)
                await member.add_roles(role)

            else:
                return

        else:
            return

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
