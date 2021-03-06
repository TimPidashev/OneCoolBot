import discord
import tensorflow
import random
import json
import os

class ai(commands.Cog):
    async def on_ready(self):
        print(colored("[AI]: online...", "white"))

        with open("./data/intents.json") as file:
            data = json.load(file)



def setup(client):
    client.add_cog(ai(client))
