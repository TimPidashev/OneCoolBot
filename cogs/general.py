import discord
from discord.ext import commands
from db import db
from utils import checks, colours, log
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, create_choice

guild_ids = [791160100567384094]

class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass


def setup(client):
    client.add_cog(General(client))