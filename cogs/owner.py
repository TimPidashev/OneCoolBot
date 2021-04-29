import discord
from discord.ext import commands, tasks
from termcolor import colored
from db import db

class owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[owner]:", "magenta"), colored("online...", "green"))
        db.connect("./data/database.db")


    

def setup(client):
    client.add_cog(owner(client))