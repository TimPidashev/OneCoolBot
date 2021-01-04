import discord
from discord.ext import commands, tasks
import youtube_dl

#figure out what this line means...
youtube_dl.utils.bug_reports_message = Lambda: ''

class musicbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("cog musicbot online...")

    #musicbot
    

def setup(client):
    client.add_cog(musicbot(client))
