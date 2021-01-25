import discord
import asyncio
from discord.ext import commands
from dhooks import Webhook, Embed
from termcolor import colored

Minecraft = Webhook("https://discord.com/api/webhooks/803034440741552168/-yavbPRjS6kZhiObh9JB7nvBRjObiQvS-yNjXtire1MreORJC2CPYgxbuthLj98Mmd0t")

class webhooks(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[webhooks]: cog webhooks online...", "grey"))

    @commands.guild_only()
    @commands.commmand()
    async def minecraft(self):

def setup(client):
    client.add_cogs(webhooks)
