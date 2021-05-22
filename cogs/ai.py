import discord
from discord.ext import commands
from utils import data, embed, log
from datetime import datetime


class ai(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        await log.cog_command(self)


    @commands.Cog.listener()
    async def on_message(self, message):
        pass

def setup(client):
    client.add_cog(ai(client))