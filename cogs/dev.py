import discord
from discord.ext import commands
from db import db
from utils import checks, log

class dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass

    @commands.command(hidden=True, pass_context=True)
    @commands.check(checks.is_owner)
    async def test(self, context):
        await context.reply("WOW! Much nothing here!", mention_author=False)




def setup(client):
    client.add_cog(dev(client))