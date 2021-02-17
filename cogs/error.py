import discord
import traceback
import lavalink
import sys
import aiohttp
from discord.ext import commands
from termcolor import colored

class errorhandler(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[error]: online...", "red"))

    # @commands.Cog.listener()
    # async def on_command_error(self, context, error):
    #     #gets original error
    #     error = getattr(error, 'original', error)
    #
    #     #if a local error handler exists...
    #     if hasattr(context.command, 'on_error'):
    #         return
    #
    #     #command_not_found
    #     if isinstance(error, commands.CommandNotFound):
    #         print(colored("[error]: An invalid command was sent, ignoring...", "red"))
    #         return
    #
    #     #disabled_command
    #     if isinstance(error, commands.DisabledCommand):
    #         print(colored("[error]: A disabled command was sent, ignoring...", "red"))
    #         return
    #
    #     #missing_permissions
    #     if isinstance(error, commands.MissingPermissions):
    #         print(colored("[error]: User was missing permissions, ignoring...", "red"))
    #         return
    #
    #     else:
    #         pass

def setup(client):
    client.add_cog(errorhandler(client))
