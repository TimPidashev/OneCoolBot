import discord
import traceback
import sys
import aiohttp
from discord.ext import commands
from termcolor import colored, cprint
from discord import Member, Embed
from discord.utils import get

class errorhandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[error]:", "magenta"), colored("online...", "green"))

    # @commands.Cog.listener()
    # async def on_command_error(self, context, error):
    #     #gets original error
    #     error = getattr(error, 'original', error)
    
    #     #if a local error handler exists...
    #     if hasattr(context.command, 'on_error'):
    #         return
    
    #     #command_not_found
    #     if isinstance(error, commands.CommandNotFound):
    #         print(colored("[error]:", "magenta"), colored("An invalid command was sent, ignoring...", "red"))
            # embed = discord.Embed(
            #     colour=0x9b59b6
            # )
            # embed.add_field(
            #     name="**Error :(**", 
            #     value=f"Command: {arg} does not exist. Try running ***.bot help*** for help  with bot commands...", 
            #     inline=False
            # )
            # embed.set_footer(
            #     text="To disable error commands, type: .bot error_notifs off"
            # )
            # await context.message.reply(embed=embed, mention_author=False)
            # return
    
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
    client.add_cog(errorhandler(client))
