import discord
from discord.ext import commands
import asyncio
from db import db
from utils import checks, log

class levelmessages(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["lmsg", "lm"])
    @commands.check(checks.is_owner)
    async def levelmessage(self, context, arg=None):
        await log.cog_command(self, context)
        if arg is not None:
            pass


        if arg is not None:
            pass



        

def setup(client):
    client.add_cog(levelmessages(client))