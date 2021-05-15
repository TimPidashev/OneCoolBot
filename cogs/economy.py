import discord
import asyncio
import random
import sqlite3
import time
import os
from utils import embed, log
from db import db
from os.path import isfile
from typing import Optional
from termcolor import colored, cprint
from discord.ext import commands
from discord import Member, Embed
from datetime import datetime
from discord.ext.menus import MenuPages, ListPageSource
from discord.utils import get
from random import choice
from discord.ext.commands import Cog
from discord import Embed, Emoji

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)
        db.connect("./data/database.db")

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["eco", "e"])
    async def economy(self, context):
        await log.cog_command(self, context)
        message = context.message  
        prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
            context.guild.id,
        )[0]

        if message.content == f"{prefix}economy" or f"{prefix}eco" or f"{prefix}e":
            embed = discord.Embed(
                title=f"{prefix}economy <?>", 
                description="You have found a *super command!* With this command you can do anything your heart desires, well almost...", 
                colour=0x9b59b6
            )   
            embed.set_footer(
                text=f"For more information on what this command does, type {prefix}economy help"
            )
            await context.reply(embed=embed, mention_author=False)
        
        else:
            embed = discord.Embed(
                colour=0x9b59b6
            )
            embed.add_field(
                name="**Error :(**", 
                value=f"This is not a valid command. Try running `{prefix}economy help` for help with game commands...", 
                inline=False
            )

            if context.author == context.guild.owner:
                embed.set_footer(
                    text=f"To disable error messages, type: {prefix}bot error_notifs off"
                )

            await context.message.reply(embed=embed, mention_author=False)

    @economy.command()
    async def wallet(self, context, target: Optional[Member]):
        await log.cog_command(self, context)
        target = target or context.author
        ids = db.column("SELECT UserID FROM users ORDER BY Coins DESC")
        coins = db.record("SELECT Coins FROM users WHERE UserID = ?", target.id)
        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.add_field(
            name=f"**Wallet:**",
            value=f"**{target.display_name}** has :coin: **{coins[0]}** coins and is rank **{ids.index(target.id)+1}** of {len(ids):} users globally.",
            inline=False
        )
        await context.reply(embed=embed, mention_author=False)

    @economy.command()
    async def cap(self, context):
        await log.cog_command(self, context)
        cap = db.record("SELECT sum(Coins) FROM users")
        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.add_field(
            name=f"**Current Market Cap:**", 
            value=f"There are currently :coin: **{cap[0]}** coins widespread globally"
        )
        await context.reply(embed=embed, mention_author=False)

    @economy.command()
    async def market(self, context):
        await log.cog_command(self, context)
        embed = discord.Embed(
            title="**Market:**", 
            colour=0x9b59b6
        )
        embed.set_footer(
            text="See whats for sale!"
        )
        await context.reply(embed=embed, mention_author=False)


    @economy.command()
    async def help(self, context):
        await log.cog_command(self, context)
        prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
            context.guild.id,
        )[0]
        #page 1
        page_1 = discord.Embed(
            title="Economy",
            description="The home page of the economy super-command!", 
            colour=0x9b59b6
        )
        page_1.add_field(
            name="`Under Construction`",
            value="This command is still under construction! Shhhh, 𝓣𝓲𝓶𝓶𝔂 has a headache!",
            inline=False
        )
        page_1.set_footer(
            text="To scroll through pages, react to the arrows below."
        )

        message = await context.reply(embed=page_1, mention_author=False)
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("❌")
        pages = 1
        current_page = 1

        def check(reaction, user):
            return user == context.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]

        while True:
            try:
                reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" and current_page != pages:
                    current_page += 1

                    if current_page == 2:
                        await message.edit(embed=page_1)
                        await message.remove_reaction(reaction, user)
                
                if str(reaction.emoji) == "◀️" and current_page > 1:
                    current_page -= 1
                    
                    if current_page == 1:
                        await message.edit(embed=page_1)
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

def setup(client):
    client.add_cog(economy(client))
