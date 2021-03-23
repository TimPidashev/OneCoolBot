import discord
import sqlite3
import time
import os
from discord.ext import commands
from termcolor import colored

class owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[owner]: online...", "white"))
    
def setup(client):
    client.add_cog(owner(client))