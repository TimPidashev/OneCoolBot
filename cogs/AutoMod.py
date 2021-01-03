import discord
import asyncio
from discord.ext import commands

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("cog AutoMod online...")

    #bad words
    @commands.Cog.listener()
    async def on_message(self, message):
        bad_words = ["fick", "arsch", "Arschgesicht", "arschgesicht", "Arschloch", "Asshole", "asshole", "Fotze", "fotze", "Miststück", "miststück", "Bitch", "bitch", "Schlampe", "schlampe", "Sheisse", "sheisse",  "Shit", "shit", "Fick", "huren", "Verpiss", "verpiss", "masturbiert", "Idiot", "idiot", "depp", "Depp", "Dumm", "dumm", "jude", "Bastard", "bastard", "Wichser", "wichser", "wixxer", "Wixxer", "Hurensohn" "Wixer", "Pisser", "Arschgesicht", "huso", "hure", "Hure", "verreck" "Verreck", "fehlgeburt", "Fehlgeburt", "ficken", "adhs", "ADHS", "Btch", "faggot", "fck", "f4ck", "nigga", "Nutted", "flaschengeburt", "penis", "pusse", "pusse", "pussy", "pussys", "nigger", "kacke", "fuucker", "fuck"]
        advertising = ["https://discord.gg", "http://discord.gg"]
        for word in bad_words:
            if message.content.count(word) > 0:
                await message.channel.purge(limit=1)
                await message.channel.send(f"Cussing is not allowed! {message.author.mention}")
                print(f"{message.author} said {message.content} and was moderated...")
        for word in advertising:
            if message.content.count(word) > 0:
                await message.channel.purge(limit=1)
                await message.channel.send(f"Advertising is not allowed! {message.author.mention}")
                print(f"{message.author} said {message.content} and was moderated...")

def setup(client):
    client.add_cog(AutoMod(client))
