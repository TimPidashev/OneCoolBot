import discord
from discord.ext import commands

class music(commands.Cog):
    def __init__(self, bot):
        self.bot  = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog music ready...")

def setup(client):
    client.add_cog(music(client))
