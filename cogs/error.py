import discord
from discord.ext import commands
from utils import log

class error(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_command_error(self, context, error):

        if isinstance(error, commands.CheckFailure):
            await context.reply(f"**oops :|**\nYou are not priveleged enough to use this command.", mention_author=False)
            await log.is_owner_false(self, context, error)

def setup(client):
    client.add_cog(error(client))
