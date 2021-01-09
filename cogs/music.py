import discord
from discord.ext import commands

class music(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("cog music online...")

    @commands.command()
    async def connect(self, context):
        voiceChannel = discord.utils.get(context.guild.voice_channels, name="Music")
        voice = discord.utils.get(client.voice_clients, guild=context.guild)
        await voiceChannel.connect()


def setup(client):
    client.add_cog(music(client))