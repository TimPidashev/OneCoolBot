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
from utils import log

class games(commands.Cog):
    def __init__(self, client, *args, **kwargs):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)
        db.connect("./data/database.db")

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["g"])
    async def game(self, context):
        await log.cog_command(self, context)
        message = context.message  
        prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
            context.guild.id,
        )[0]

        if message.content == f"{prefix}game" or f"{prefix}g":
            embed = discord.Embed(
                title=f"{prefix}game <?>", 
                description="You have found a *super command!* With this command you can do anything your heart desires, well almost...", 
                colour=0x9b59b6
            )   
            embed.set_footer(
                text=f"For more information on what this command does, type {prefix}game help"
            )
            await context.reply(embed=embed, mention_author=False)
        
        else:
            embed = discord.Embed(
                colour=0x9b59b6
            )
            embed.add_field(
                name="**Error :(**", 
                value=f"This is not a valid command. Try running `{prefix}game help` for help with game commands...", 
                inline=False
            )

            if context.author == context.guild.owner:
                embed.set_footer(
                    text=f"To disable error messages, type: {prefix}bot error_notifs off"
                )

            await context.message.reply(embed=embed, mention_author=False)

    @game.command()
    async def help(self, context):
        await log.cog_command(self, context)
        prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
            context.guild.id,
        )[0]
        #page 1
        page_1 = discord.Embed(
            title="Index",
            description="The home page of the game super-command!", 
            colour=0x9b59b6
        )
        page_1.add_field(
            name="`Counting`",
            value="A counting game with multiple people and different modes for different occasions.",
            inline=False
        )
        page_1.add_field(
            name="`Chess`", 
            value="Match up with people and play for coins, or challenge @OneCoolBot for a very special prize!",
            inline=False
        )
        page_1.add_field(
            name="`Cave Adventure`", 
            value="Play the collosal-cave-adventure terminal classic within discord!",
            inline=False
        )
        page_1.add_field(
            name="`Roll the Dice`",
            value="Roll the dice with friends to decide your fate, or for coins.", 
            inline=False
        )
        page_1.set_footer(
            text="To scroll through pages, react to the arrows below."
        )

        #page 2
        page_2 = discord.Embed(
            title="Counting", 
            colour=0x9b59b6
        )
        page_2.add_field(
            name="Commands", 
            value="`count` Specifies game context.",
            inline=False
        )
        page_2.add_field(
            name="Argument 1",
            value=f"_Modes_:\n`default` The default game mode.\n`deathmatch` Become the last man standing!\n`duel` 1v1 a friend or foe in an epic fight!\n`endless` Play against OneCoolBot in an endless fight!",
            inline=False
        )
        page_2.add_field(
            name="Argument 2",
            value=f"_Conditions:_\n**default** `no secondary args.`\n**deathmatch** `@member` `@OneCoolBot`\n**duel** `@member` `@OneCoolBot`\n**endless** `no secondary args.`",
            inline=False
        )
        page_2.set_footer(
            text=f"For complete reference with counting, do: {prefix}game count help"
        )
        
        #page 3
        page_3 = discord.Embed(
            title="Chess", 
            colour=0x9b59b6
        )
        page_3.add_field(
            name="Commands",
            value="`chess` specifies game context.",
            inline=False
        )
        page_3.add_field(
            name="Argument 1",
            value="_Modes:_\n`default` The default game mode.\n`losers` Get rid of your pieces before your opponent!",
            inline=False
        )
        page_3.add_field(
            name="Argument 2",
            value="_Conditions:_\n**default** `wager` `@member` `@OneCoolBot`\n**losers** `wager` `@member` `@OneCoolBot`",
            inline=False
        )
        page_3.set_footer(
            text=f"For complete reference with chess, do: {prefix}game chess help"
        )
        
        #page 4
        page_4 = discord.Embed(
            title="Cave Adventure", 
            colour=0x9b59b6
        )
        page_4.add_field(
            name="Commands",
            value="`cave` specifies game context.",
            inline=False
        )
        page_4.add_field(
            name="Argument 1",
            value="_Options:_",
            inline=False
        )
        page_4.add_field(
            name="Argument 2",
            value="_Actions:_",
            inline=False
        )
        page_4.add_field(
            name="Argument 3",
            value="_Settings:_"
        )
        page_4.set_footer(
            text=f"For complete reference with chess, do: {prefix}game cave help"
        )

        #page 5
        page_5 = discord.Embed(
            title="Roll the Dice", 
            colour=0x9b59b6
        )
        page_5.add_field(
            name="Commands",
            value="`roll` specifies game context.",
            inline=False
        )
        page_5.add_field(
            name="Argument 1",
            value="_Modes:_",
            inline=False
        )
        page_5.add_field(
            name="Argument 2",
            value="_Actions:_",
            inline=False
        )
        page_5.set_footer(
            text="For complete reference with chess, do: {prefix}game roll help"
        )

        message = await context.reply(embed=page_1, mention_author=False)
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("❌")
        pages = 5
        current_page = 1

        def check(reaction, user):
            return user == context.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]

        while True:
            try:
                reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" and current_page != pages:
                    current_page += 1

                    if current_page == 2:
                        await message.edit(embed=page_2)
                        await message.remove_reaction(reaction, user)
                    
                    elif current_page == 3:
                        await message.edit(embed=page_3)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 4:
                        await message.edit(embed=page_4)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 5:
                        await message.edit(embed=page_5)
                        await message.remove_reaction(reaction, user)
                
                if str(reaction.emoji) == "◀️" and current_page > 1:
                    current_page -= 1
                    
                    if current_page == 1:
                        await message.edit(embed=page_1)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 2:
                        await message.edit(embed=page_2)
                        await message.remove_reaction(reaction, user)
                    
                    elif current_page == 3:
                        await message.edit(embed=page_3)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 4:
                        await message.edit(embed=page_4)
                        await message.remove_reaction(reaction, user)

                if str(reaction.emoji) == "❌":
                    await message.delete()
                    break

                else:
                    await message.remove_reaction(reaction, user)
                    
            except asyncio.TimeoutError:
                await message.delete()
                #add context message delete here
                break


    @game.command()
    async def count(self, context):
        await log.cog_command(self, context)
        emoji = self.client.get_emoji(823934633116303431)
        start_timer = int(60)
        timer = 60

        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.add_field(
            name="**Count**",
            value="Count as high as you can!",
            inline=False
        )
        embed.insert_field_at(
            index=1,
            name=":trophy:React below to join the match.",
            value=f":stopwatch:Match starts in: {start_timer}'s",
            inline=False
        )
        embed.set_footer(
            text="Winner gets 1000 coins!"
        )
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





        # if arg == "help":
        #     embed = discord.Embed(colour=0x9b59b6)
        #     embed.add_field(name="**Help with games**", value="A reference to all the commands and minigames.", inline=False)
        #     embed.set_footer(text="To suggest more minigames, dm 𝓣𝓲𝓶𝓶𝔂#6955")
        #     await context.reply(embed=embed, mention_author=False)

        # elif arg == "count":
        #     emoji = self.client.get_emoji(823934633116303431)
        #     start_timer = int(60)
        #     timer = 60
        #     embed = discord.Embed(colour=0x9b59b6)
        #     embed.add_field(name="**Count**", value="Count as high as you can!", inline=False)
        #     embed.insert_field_at(
        #     index=1,
        #     name=":trophy:React below to join the match.",
        #     value=f":stopwatch:Match starts in: {start_timer}'s",
        #     inline=False
        # )
        #     embed.set_footer(text="Winner gets 1000 coins!")
        #     message = await context.reply(embed=embed, mention_author=False)
        #     await message.add_reaction(emoji)

        #     while timer != 0:
        #         timer = timer - 1
        #         embed.remove_field(index=1)
        #         embed.insert_field_at(
        #             index=1,
        #             name=":trophy:React below to join the match.",
        #             value=f":stopwatch:Match starts in: {timer}'s",
        #             inline=False
        #         )
        #         await message.edit(embed=embed)
        #         time.sleep(1)

        #         if timer == 0:
        #             embed.remove_field(index=1)
        #             embed.insert_field_at(
        #                 index=1,
        #                 name=":trophy:The match has started!",
        #                 value=f"Commence typing!",
        #                 inline=False
        #             )
        #             await message.edit(embed=embed)

        #             fetch_message = await context.channel.fetch_message(message.id)
        #             users = await fetch_message.reactions[0].users().flatten()
        #             users.pop(users.index(self.client.user))

        #             start_game = True
        #             count = 0

        #             while start_game != False:
        #                 commands.Cog.listener()
        #                 async def on_message(self, message):
        #                     if not message.author.bot() and message.channel = game_channel:
        #                         if message.content.startswith("1"):
        #                             count = count += 1
        #                             print(count)
        #                             break
                                    
                        





                    # await context.reply(users, mention_author=False)
        
        

def setup(client):
    client.add_cog(games(client))