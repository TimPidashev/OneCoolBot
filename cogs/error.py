import discord
import traceback
import sys
import aiohttp
from discord.ext import commands
from termcolor import colored, cprint
from discord import Member, Embed
from discord.utils import get
import asyncio
import sqlite3
from db import db

class errorhandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[error]:", "magenta"), colored("online...", "green"))

    @commands.command()
    async def help(self, context):
        print(colored("[error]:", "magenta"), colored(f"{context.author.name}#{context.author.discriminator} was redirected  to help command in guild: {context.guild.name} | channel: {context.channel.name}...", "green"))
        prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
            context.guild.id,
        )[0]
        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.add_field(
            name="**Error :(**", 
            value=f"Commands are categorized in sections. For more info, type `{prefix}bot help`",
            inline=False
        )
        if context.author == context.guild.owner:
            embed.set_footer(
                text=f"To disable error messages, type: {prefix}bot error_notifs off"
            )
        await context.reply(embed=embed, mention_author=False)

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
