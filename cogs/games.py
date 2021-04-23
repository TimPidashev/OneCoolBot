import discord
from discord.ext import commands
from termcolor import colored
from db import db
import sqlite3
import time

class games(commands.Cog):
    def __init__(self, client, *args, **kwargs):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[games]:", "magenta"), colored("online...", "green"))
        db.connect("./data/database.db")

    @commands.command()
    async def game(self, context, arg):
        if arg == "help":
            embed = discord.Embed(colour=0x9b59b6)
            embed.add_field(name="**Help with games**", value="A reference to all the commands and minigames.", inline=False)
            embed.set_footer(text="To suggest more minigames, dm 𝓣𝓲𝓶𝓶𝔂#6955")

        if arg == "count":
            embed = discord.Embed(colour=0x9b59b6)
            embed.add_field(name="**Count**", value="Count as high as you can!", inline=False)
            embed.set_footer(text="Winner gets 1000 coins!")
            await context.reply(embed=embed, mention_author=False)
        
        else:
            embed = discord.Embed(colour=0x9b59b6)
            embed.add_field(name="**Error :(**", value=f"Game: {arg} does not exist. Try running ***.game help*** for help  with game command...", inline=False)
            await context.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(games(client))