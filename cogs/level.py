import discord
import time
import sqlite3
import asyncio
import random
from datetime import datetime, timedelta
from termcolor import colored
from discord.ext import commands
from db import db

class level(commands.Cog):
    def __init__(self, client):
        self.bot = client

    async def process_xp(self, message):
        xp, lvl, xplock = db.record(
            "SELECT XP, Level, XPLock FROM users WHERE UserID = ?", message.author.id
        )

        if datetime.utcnow() > datetime.fromisoformat(xplock):
            await self.add_xp(message, xp, lvl)

    async def add_xp(self, message, xp, lvl):
        xp_to_add = random.randint(10, 20)

        new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)

        db.execute(
            "UPDATE users SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?",
            xp_to_add,
            new_lvl,
            (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
            message.author.id,
        )

        if new_lvl > lvl:
            #if level_up_messages == "('yes',)" or level_up_messages == "('Yes',)":
            await message.channel.send(
                f"{message.author.mention} leveled up to {new_lvl:,}!",
                delete_after=10,
            )

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[level]: cog level online...", "cyan"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            db.execute("INSERT OR IGNORE INTO users (UserID) VALUES (?)", message.author.id)
            db.commit()

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if not message.author.bot:
    #         await self.process_xp(message)

    # @command(name="level", aliases=["rank", "lvl"], brief="Shows your level, and rank.")
    # async def display_level(self, ctx, target: Optional[Member]):
    #     """Shows your Global+Server Doob level, rank and XP!"""
    #     target = target or ctx.author
    #
    #     ids = db.column("SELECT UserID FROM users ORDER BY XP DESC")
    #     # ids_g = db.column("SELECT UserID FROM users ORDER BY XP DESC WHERE GuildID = ?", ctx.guild.id)
    #     xp, lvl = db.record(
    #         "SELECT XP, Level FROM users WHERE UserID = ?", target.id
    #     ) or (None, None)
    #     xp_g, lvl_g = (
    #         db.record(
    #             "SELECT XP, Level FROM guildexp WHERE (UserID, GuildID) = (?, ?)",
    #             target.id,
    #             ctx.guild.id,
    #         )
    #         or (None, None)
    #     )
    #
    #     if lvl is not None:
    #         await ctx.reply(
    #             f"`Global Rank:`\n{target.display_name} is level {lvl:,} with {xp:,} xp and is rank {ids.index(target.id)+1} of {len(ids):,} users globally.\n`Server Rank:`\n{target.display_name} is server level {lvl_g:,} with {xp_g:,} server xp."
    #         )
    #
    #     else:
    #         ctx.reply("That member is not in the XP Database.")
    #
    # @command(
    #     name="levelmessages",
    #     aliases=["slm", "lm", "setlevelmessages"],
    #     brief="Set the server's level messages",
    # )
    # @has_permissions(manage_guild=True)
    # async def set_level_messages(self, ctx, *, yes_or_no: Optional[str]):
    #     """PLEASE, put 'yes' if you DO want level messages\n`Manage Server` permission required."""
    #     levelmessages = db.records(
    #         "SELECT LevelMessages FROM guilds WHERE GuildID = ?", ctx.guild.id
    #     ) or (None)
    #     prefix = db.records("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)
    #
    #     if (
    #         yes_or_no == "Yes"
    #         or yes_or_no == "yes"
    #         or yes_or_no == "no"
    #         or yes_or_no == "No"
    #     ):
    #         db.execute(
    #             "UPDATE guilds SET LevelMessages = ? WHERE GuildID = ?",
    #             yes_or_no,
    #             ctx.guild.id,
    #         )
    #         db.commit()
    #         await ctx.reply(f"Level messages set to `{yes_or_no}`.")
    #
    #     else:
    #         await ctx.reply(
    #             f"The current setting for Level Messages is: `{levelmessages[0][0]}`\nTo change it, type `{prefix[0][0]}levelmessages (yes or no)`"
    #         )
    #
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
