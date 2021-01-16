import discord
import asyncio
import asyncpg
from discord.ext import commands

class level(commands.Cog):
    def __init__(self, client):
        self.bot = client


def setup(client):
    client.add_cog(level(client))
