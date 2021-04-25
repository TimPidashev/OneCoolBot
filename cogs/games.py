import discord
import asyncio
import json
import os
from db import db
from os.path import isfile
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from termcolor import colored
from typing import Optional
from random import choice
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
from discord.ext.commands import Cog
from discord import Embed, Emoji
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
            await context.reply(embed=embed, mention_author=False)

        elif arg == "count":
            game_channel = self.client.channel()
            emoji = self.client.get_emoji(823934633116303431)
            start_timer = int(60)
            timer = 60
            embed = discord.Embed(colour=0x9b59b6)
            embed.add_field(name="**Count**", value="Count as high as you can!", inline=False)
            embed.insert_field_at(
            index=1,
            name=":trophy:React below to join the match.",
            value=f":stopwatch:Match starts in: {start_timer}'s",
            inline=False
        )
            embed.set_footer(text="Winner gets 1000 coins!")
            message = await context.reply(embed=embed, mention_author=False)
            await message.add_reaction(emoji)

            while timer != 0:
                timer = timer - 1
                embed.remove_field(index=1)
                embed.insert_field_at(
                    index=1,
                    name=":trophy:React below to join the match.",
                    value=f":stopwatch:Match starts in: {timer}'s",
                    inline=False
                )
                await message.edit(embed=embed)
                time.sleep(1)

                if timer == 0:
                    embed.remove_field(index=1)
                    embed.insert_field_at(
                        index=1,
                        name=":trophy:The match has started!",
                        value=f"Commence typing!",
                        inline=False
                    )
                    await message.edit(embed=embed)

                    fetch_message = await context.channel.fetch_message(message.id)
                    users = await fetch_message.reactions[0].users().flatten()
                    users.pop(users.index(self.client.user))


                    start_game = True
                    count = 0

                    # while start_game != False:
                    #     commands.Cog.listener()
                    #     async def on_message(self, message):
                    #         if not message.author.bot() and message.channel = game_channel:
                    #             if message.content.startswith("1"):
                    #                 count = count += 1
                    #                 print(count)
                    #                 break
                                    
                        





                    # await context.reply(users, mention_author=False)
        
        else:
            embed = discord.Embed(colour=0x9b59b6)
            embed.add_field(name="**Error :(**", value=f"Game: {arg} does not exist. Try running ***.game help*** for help  with game command...", inline=False)
            await context.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(games(client))