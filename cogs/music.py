import discord
import youtube_dl
import os
from discord.ext import commands
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
class music(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("cog music online...")

    @commands.command()
    async def play(self, context):
        if not context.message.author.voice:
            await context.send("You are not connected to a voice channel.")
        else:
            channel = context.message.author.voice.channel
            await channel.connect()


def setup(client):
    client.add_cog(music(client))
