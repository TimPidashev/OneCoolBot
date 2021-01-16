import discord
import os
import asyncio
import time
from discord.ext import commands
from termcolor import colored

class dms(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("cog dms online...", "green"))

    @commands.command()
    async def chat(self, context):
        await context.channel.send(f"{context.author}, my A.I. is not yet functional, go bug Timmy to update me!")

def setup(client):
    client.add_cog(dms(client))
