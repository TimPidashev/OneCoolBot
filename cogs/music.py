import discord
from wavelink
from discord.ext import commands, tasks

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("cog musicbot online...")

    #musicbot
    

def setup(client):
    client.add_cog(music(client))
