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
from termcolor import colored
from discord.ext import commands
from db import db

class level(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[level]: cog level online...", "cyan"))

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

                    # elif lvl == 5:
                    #     role = message.author.guild.get_role(791161672957558834)
                    #     await message.author.add_roles(role)
                    #     print(colored("[level]: Added '{}' to {}".format(role.name, message.author.name) + "...", "cyan"))
                    #
                    # elif lvl == 10:
                    #     yellow_belt = message.author.guild.get_role(791161670080004126)
                    #     await message.author.add_roles(yellow_belt)
                    #     #print(colored("[level]: Added '{}' to {}".format(role.name, member.name) + "...", "cyan"))

                else:
                    pass

            else:
                print(colored(f"[level]: {message.author}#{message.author.discriminator} is not in the db...", "cyan"))
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
            #async with context.typing():
                #await asyncio.sleep(1)
            await context.channel.send("You are not in the database :(")

    # @command(
    #     name="leaderboard",
    #     aliases=["lb", "xplb"],
    #     brief="Show who's on top of the Doob GlobalXP Leaderboard!",
    # )
    # async def display_leaderboard(self, ctx):
    #     """Displays the Global XP Leaderboard for Doob."""
    #     records = db.records("SELECT UserID, XP, Level FROM users ORDER BY XP DESC")
    #
    #     menu = MenuPages(
    #         source=Menu(ctx, records), clear_reactions_after=True, timeout=100.0
    #     )
    #     await menu.start(ctx)
    #
    # @command(
    #     name="serverleaderboard",
    #     aliases=["serverlb", "serverxplb", "svxp", "svxplb"],
    #     brief="Show who's on top of the Doob ServerXP Leaderboard!",
    # )
    # async def display_serverxp_leaderboard(self, ctx):
    #     """Displays the Server XP Leaderboard for Doob."""
    #     records = db.records(
    #         "SELECT UserID, XP, Level FROM guildexp WHERE GuildID = ? ORDER BY XP DESC",
    #         ctx.guild.id,
    #     )
    #
    #     menu = MenuPages(
    #         source=ServerMenu(ctx, records), clear_reactions_after=True, timeout=100.0
    #     )
    #     await menu.start(ctx)
    #
    # @Cog.listener()
    # async def on_ready(self):
    #     if not self.bot.ready:
    #         self.bot.cogs_ready.ready_up("exp")
    #
    # @Cog.listener()
    # async def on_message(self, message):
    #     if not message.author.bot:
    #         await self.process_xp(message)

def setup(client):
    client.add_cog(level(client))
