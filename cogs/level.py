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
    async def on_message(self, message):
        with open("users.json", "r") as f:
            users = json.load(f)

            if message.author.bot:
                return

            if message.channel.is_private:
                return

            else:
                await update_data(users, message.author)
                number = random.randint(1,10)
                await add_experience(users, message.author, number)
                await level_up(users, message.author, message.channel)

            with open(users.json, "w") as f:
                json.dump(users, f)
            await bot.process_commands(message)

def setup(client):
    client.add_cog(level(client))
