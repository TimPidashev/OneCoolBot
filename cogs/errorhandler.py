import discord
import os
import time
import asyncio
from discord.ext import commands

class errorhandler(commands.Cog):
    def __init__(self, client):
        self.bot = client
    

def setup(client):
    client.add_cog(errorhandler(client))
