import discord
from discord.ext import commands, tasks
from utils import embed, log

class admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)

def setup(client):
    client.add_cog(admin(client))