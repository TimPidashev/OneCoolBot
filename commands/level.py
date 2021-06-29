import discord
from discord.ext import commands
from db import db
from utils import checks, log

class level(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def on_ready(self):
        await log.cog_command(self, context)

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["lvl", "l"])
    async def level(self, context, arg=None):
        if arg is not None:
            pass

        if arg is None:
            pass



def setup(client):
    client.add_cog(level(client))