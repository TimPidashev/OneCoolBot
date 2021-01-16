import discord
import asyncio
import re
from discord.ext import commands
from termcolor import colored

class automoderation(commands.Cog):
    def __init__(self, client):
        self.bot = client

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("cog automoderation online...", "green"))

    #bad words
    @commands.Cog.listener()
    async def on_message(self, message):
        bad_words = ["fick", "arsch", "Arschgesicht", "arschgesicht", "Arschloch", "Asshole", "asshole", "Fotze", "fotze", "Miststück", "miststück", "Bitch", "bitch", "Schlampe", "schlampe", "Sheisse", "sheisse",  "Shit", "shit", "Fick", "huren", "Verpiss", "verpiss", "masturbiert", "Idiot", "idiot", "depp", "Depp", "Dumm", "dumm", "jude", "Bastard", "bastard", "Wichser", "wichser", "wixxer", "Wixxer", "Hurensohn" "Wixer", "Pisser", "Arschgesicht", "huso", "hure", "Hure", "verreck" "Verreck", "fehlgeburt", "Fehlgeburt", "ficken", "adhs", "ADHS", "Btch", "faggot", "fck", "f4ck", "nigga", "Nutted", "flaschengeburt", "penis", "pusse", "pusse", "pussy", "pussys", "nigger", "kacke", "fuucker", "fuck"]
        for word in bad_words:
            if message.content.count(word) > 0:
                await message.channel.purge(limit=1)
                await message.channel.send(f"Cussing is not allowed! {message.author.mention}")
                print(colored(f"{message.author} said {message.content} and was moderated...", "orange"))

    @commands.Cog.listener()
    async def on_message(self, message):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',message.content.lower())
        if urls is not None and message.content.startswith('https://discord.gg' or 'http://discord.gg'):
            await message.channel.purge(limit=1)
            await message.channel.send("Links are not allowed!")
            print(colored(f"{message.author} tried to advertise link {message.content} but was stopped...", "orange"))
            return


def setup(client):
    client.add_cog(automoderation(client))
