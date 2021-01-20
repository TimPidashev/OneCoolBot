import discord
import asyncio
import asyncpg
from discord.ext import commands
from termcolor import colored

class level(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("cog level online...", "green"))

def setup(client):
    client.add_cog(level(client))
