import discord
import json
import random
import os
from discord.ext import commands

class level(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("cog level online...")

    @commands.Cog.listener()
    async def on_message(self, message):
        with open("users.json", "r", encoding="utf8") as f:
            user = json.load(f)
        try:
            with open("users.json", "w", encoding="utf8") as f:
                user[str(message.author.id)]["xp"] = user[str(message.author.id)]["xp"]+1#make into random int from 1 to 10 later...
                lvl_start = user[str(message.author.id)]["level"]
                lvl_end = user[str(message.author.id)]["exp"] ** (1.5/4)
                if lvl_start < lvl_end:
                    user[str(message.author.id)]["level"] = user[str(message.author.id)]["level"]+1
                    lvl = user[str(message.author.id)]["level"]
                    await message.channel.send(f"{message.author.name} has leveled up to {lvl}!")
                    json.dump(user,f,sort_keys=True,indent=4,ensure_ascii=False)
                    return
                json.dump(user,f,sort_keys=True,indent=4,ensure_ascii=False)
        except:
            with open("users.json", "w", encoding="utf8") as f:
                user = {}
                user[str(message.author.id)] = {}
                user[str(message.author.id)]["level"] = 0
                user[str(message.author.id)]["xp"] = 0
                json.dump(user,f,sort_keys=True,indent=4,ensure_ascii=False)

def setup(client):
    client.add_cog(level(client))
