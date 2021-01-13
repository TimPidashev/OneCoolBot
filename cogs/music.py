import discord
import wavelink
import os
import asyncio
from discord.ext import commands

class music(commands.Cog):
    def __init__(self, client):
        self.bot = client

def setup(client):
    client.add_cog(music(client))
