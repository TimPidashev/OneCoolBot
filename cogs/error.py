"""
MIT License

Copyright (c) 2021 Timothy Pidashev
"""


import discord
from discord.ext import commands
from utils import log

class Error(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)

    @commands.Cog.listener()
    async def on_command_error(self, context, error):

        if isinstance(error, commands.CheckFailure):
            await context.reply(f"**oops :|**\nYou are not priveleged enough to use this command.", mention_author=False)
            await log.is_owner_false(self, context, error)

        #error handler is atm pretty pointless...

        else:
            pass

def setup(client):
    client.add_cog(Error(client))
