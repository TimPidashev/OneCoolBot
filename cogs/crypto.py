import discord
import requests
import json
import asyncio
from discord.ext import commands

class crypto(commands.Cog):
    def __init__(self, client):
        self.bot = client


def setup(client):
    client.add_cog(crypto(client))
