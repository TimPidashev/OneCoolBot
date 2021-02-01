import discord
import random
import time
import asyncio
from termcolor import colored
from discord.ext import commands

class level(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[level]: cog level online...", "cyan"))

def setup(client):
    client.add_cog(level(client))
