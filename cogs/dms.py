import discord
import os
import asyncio
import time
from discord import DMChannel
from discord.ext import commands
from termcolor import colored
from datetime import datetime

class dms(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[dms]: cog dms online...", "grey"))

    #currently broken
    
    #@commands.command()
    #async def report(self, message):
        #if not message.author.bot:
            #if isinstance(message.channel, DMChannel):
                #if len(message.content) < 50:
                    #await context.send("Your message should be at leas 50 characters in length.")
                #else:
                    #await context.send("Your message has been accepted...")


        #else:
            #await self.process_commands(message)





    #modmail system in the works
    #@commands.Cog.listener()
    #async def on_message(self, message):
        #if not message.author.bot:
            #if isinstance(message.channel, DMChannel):
                #if len(message.content) < 50:
                    #await context.send("Your message should be at leas 50 characters in length.")

        #else:
            #await self.process commands(message)


def setup(client):
    client.add_cog(dms(client))
