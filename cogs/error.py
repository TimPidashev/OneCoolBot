import discord
import traceback
import wavelink
import sys
import aiohttp
from discord.ext import commands
from termcolor import colored, cprint
from discord import Member, Embed
from discord.utils import get
import asyncio
import sqlite3
from db import db
from utils import embed, log

class error(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)
        
    # @commands.Cog.listener()
    # async def on_command_error(self, context, error):
    #     #gets original error
    #     error = getattr(error, 'original', error)
    
        # if a local error handler exists...
        # if hasattr(context.command, 'on_error'):
        #     return
    
        # command_not_found
        # if isinstance(error, commands.CommandNotFound):
        #     pass
    
    #disabled_command
    # if isinstance(error, commands.DisabledCommand):
    #     print(colored("[error]:", "magenta"), colored("A disabled command was sent, ignoring...", "red"))
    #     return

    # #missing_permissions
    # if isinstance(error, commands.MissingPermissions):
    #     print(colored("[error]:", "magenta"), colored("User was missing permissions, ignoring...", "red"))
    #     return

    # else:
    #     pass

def setup(client):
    client.add_cog(error(client))
