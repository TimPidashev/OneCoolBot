import discord
import json
import random
import os
from discord.ext import commands

class level(commands.Cog):
    def __init__(self, client):
        self.bot = client


def setup(client):
    client.add_cog(level(client))
