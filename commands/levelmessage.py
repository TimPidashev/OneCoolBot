import discord
from discord.ext import commands
import asyncio
from db import db
from utils import log

class levelmessages(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass


    @commands.group(pass_context=True, invoke_without_command=True, aliases=["lvlmsgs", "lvlms", "lmsg", "lm"])
    async def levelmessage(self, context, arg=None):
        await log.cog_command(self, context)
        level_message_check, level_message, level_message_channel = db.record(
            f"SELECT LevelMessages, LevelMessage, LevelMessageChannel FROM guildconfig WHERE GuildID = {context.guild.id}"
        )[0]

        await context.reply("Coming soon!", mention_author=False)


def setup(client):
    client.add_cog(levelmessages(client))