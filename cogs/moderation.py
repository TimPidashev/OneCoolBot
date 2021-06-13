import discord
import asyncio
from utils import log
from discord.ext import commands, tasks

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
       pass

    #clear for development
    @commands.command()
    @commands.is_owner()
    async def clear(self, context, amount=10):
        await context.channel.purge(limit=amount+1)
        await log.clear_messages(self, context, amount)

def setup(client):
    client.add_cog(moderation(client))
