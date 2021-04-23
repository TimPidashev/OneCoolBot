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
        if arg == "count":
            await context.reply("success")
        
        else:
            await context.reply("game does not exist!")

def setup(client):
    client.add_cog(games(client))