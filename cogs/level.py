import discord
import json
import asyncio
import time
import random
from discord.ext import commands

class level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("cog level online...")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("users.json", "r") as f:
            users = json.load(f)

        await update_data(users, member)

        with open("users.json", "w") as f:
            json.dump(users, f)

    async def update_data(self, users, user):
        if not user.id in users:
            users[user.id] - {}

def setup(client):
    client.add_cog(level(client))
