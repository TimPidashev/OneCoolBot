import discord
import time
import sqlite3
import asyncio
import random
import os
from discord import Member, Embed
from discord.ext.commands import Cog
from typing import Optional
from os.path import isfile
from datetime import datetime, timedelta
from discord.ext.menus import MenuPages, ListPageSource
from termcolor import colored
from discord.ext import commands
from db import db

class level(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[level]: level online...", "cyan"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            db.connect("./data/database.db")
            result = db.record("SELECT UserID FROM users WHERE UserID = (?)", message.author.id)
            if result is not None:
                xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM users WHERE UserID = ?", message.author.id)
                if datetime.utcnow() > datetime.fromisoformat(xplock):

                    xp_to_add = random.randint(10, 20)
                    new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)

                    db.execute("UPDATE users SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?",
                        xp_to_add,
                        new_lvl,
                        (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
                        message.author.id,
                    )
                    db.commit()
                    print(colored(f"[level]: added {xp_to_add} xp to {message.author}...", "cyan"))

                    if new_lvl > lvl:
                        await message.channel.send(f":partying_face: {message.author.mention} has leveled up to {new_lvl:,}!")
                        if new_lvl == 5:
                            new_here = message.guild.get_role(791162885002100793)
                            await message.author.remove_role(new_here)
                            white_belt = message.guild.get_role(791161672957558834)
                            await message.author.add_roles(white_belt)
                            print(colored(f"[level]: Added {white_belt.name} to {message.author.name}...", "cyan"))
                            await message.author.send(f":partying_face: Hooray, you have gotten the {white_belt.name} role!")

                        elif new_lvl == 10:
                            yellow_belt = message.guild.get_role(791161670080004126)
                            await message.author.add_roles(yellow_belt)
                            print(colored(f"[level]: Added {yellow_belt.name} to {message.author.name}...", "cyan"))
                            await message.author.send(f":partying_face: Hooray, you have gotten the {yellow_belt.name} role!")

                        elif new_lvl == 20:
                            orange_belt = message.guild.get_role(791161667148840970)
                            await message.author.add_roles(orange_belt)
                            print(colored(f"[level]: Added {orange_belt.name} to {message.author.name}...", "cyan"))
                            await message.author.send(f":partying_face: Hooray, you have gotten the {orange_level.name} role!")

                        elif new_lvl == 30:
                            green_belt = message.guild.get_role(791161664296058890)
                            await message.author.add_roles(green_belt)
                            print(colored(f"[level]: Added {green_belt.name} to {green_belt.author.name}...", "cyan"))
                            await message.author.send(f":partying_face: Hooray, you have gotten the {green_belt.name} role!")

                        elif new_lvl == 40:
                            blue_belt = message.guild.get_role(791161661293330432)
                            await message.author.add_roles(blue_belt)
                            print(colored(f"[level]: Added {blue_belt.name} to {blue_belt.author.name}...", "cyan"))
                            await message.author.send(f":partying_face: Hooray, you have gotten the {blue_belt.name} role!")

                        elif new_lvl == 50:
                            purple_belt = message.guild.get_role(791161658406993940)
                            await message.author.add_roles(purple_belt)
                            print(colored(f"[level]: Added {purple_belt.name} to {purple_belt.author.name}...", "cyan"))
                            await message.author.send(f":partying_face: Hooray, you have gotten the {purple_belt.name} role!")

                        elif new_lvl == 75:
                            black_belt = message.guild.get_role(791161652971962378)
                            await message.author.add_roles(black_belt)
                            print(colored(f"[level]: Added {black_belt.name} to {black_belt.author.name}...", "cyan"))
                            await message.author.send(f":partying_face: Hooray, you have gotten the {black_belt.name} role!")

                        elif new_lvl == 100:
                            moderator = message.guild.get_role(791161649901207572)
                            await message.author.add_roles(moderator)
                            print(colored(f"[level]: Added {moderator.name} to {moderator.author.name}...", "cyan"))
                            await message.author.send(f":partying_face: Hooray, you have gotten the {moderator.name} role!")

                else:
                    pass

            else:
                print(colored(f"[level]: {message.author}#{message.author.discriminator} was added to db...", "cyan"))
                db.execute("INSERT OR IGNORE INTO users (UserID) VALUES (?)", message.author.id)
                db.commit()

    @commands.guild_only()
    @commands.command()
    async def rank(self, context, target: Optional[Member]):
        target = target or context.author
        ids = db.column("SELECT UserID FROM users ORDER BY XP DESC")

        xp, lvl = db.record(
            "SELECT XP, Level FROM users WHERE UserID = ?", target.id
        ) or (None, None)

        if lvl is not None:
            async with context.typing():
                await asyncio.sleep(1)
                await context.channel.send(f"`Global Rank:`\n{target.display_name} is level {lvl:,} with {xp:,} xp and is rank {ids.index(target.id)+1} of {len(ids):,} users globally.")

        else:
            async with context.typing():
                await asyncio.sleep(1)
                await context.channel.send("You are not in the database :(")

    @commands.guild_only()
    @commands.command()
    async def leaderboard(self, context):
        records = db.records("SELECT UserID, XP, Level FROM users ORDER BY XP DESC")
        await context.channel.send("Leaderboard coming Soon!")

def setup(client):
    client.add_cog(level(client))
