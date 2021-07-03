import discord
from discord.ext import commands
from db import db
from utils import checks, colours, log
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, create_choice

guild_ids = [791160100567384094, 788629323044093973]

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @cog_ext.cog_slash(
        name="economy",
        description="A global market and trading system, complete with its own currency!",
        guild_ids=guild_ids
    )
    async def economy(self, context: SlashContext):
        await context.send("Coming soon!")

def setup(client):
    client.add_cog(economy(client))
