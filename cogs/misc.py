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
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed
from discord.ext.commands import Cog
import sqlite3

class Menu(ListPageSource):
    def __init__(self, context, data):
        self.context = context

        super().__init__(data, per_page=10)

    async def write_page(self, menu, offset, fields=[]):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(
            title="Starboard",
            colour=self.context.author.colour,
        )

        embed.set_thumbnail(url=self.context.guild.me.avatar_url)
        embed.set_footer(
            text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} members."
        )

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        fields = []
        table = "\n".join(
            f"{idx+offset}. **{self.context.guild.get_member(entry[0]).name}** ~ ⭐`{entry[1]}`"
            for idx, entry in enumerate(entries)
        )

        fields.append(("Top members:", table))

        return await self.write_page(menu, offset, fields)

class misc(commands.Cog):
    def __init__(self, client, *args, **kwargs):
        self.client = client
        self.role_message_id = 815307066473578516
        self.emoji_to_role = {
            "<:javascript:815332173640761344>": 811690417912807474,
            "<:python:815331845280497726>": 811689718826795019
        }

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[misc]: online...", "green"))
        db.connect("./data/database.db")

    #help command
    @commands.command()
    async def help(self, context):
        print(colored("[main]: command(help) used...", "magenta"))
        async with context.typing():
            await asyncio.sleep(1)
            embed = discord.Embed(title="Help", color=2105637)
            embed.add_field(name="Bot Related", value="`info, help`")
            embed.add_field(name="AutoRole/Level/XP System", value="`rank, leaderboard`", inline=False)
            embed.add_field(name="Economy", value="`wallet, market, give, me`", inline=False)
            embed.add_field(name="Moderator", value="`kick, mute, ban, unban, clear`", inline=False)
            embed.add_field(name="Music", value="`connect, play, pause, resume, skip, stop, volume, shuffle, equalizer, queue, current, swap, music, spotify`")
            await context.message.channel.send(embed=embed)

    #on_member_join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(colored(f"[misc]: {member.name}#{member.discriminator} joined at {current_time}" + "...", "green"))

        #adding user to database
        try:
            db.execute("INSERT INTO users (UserID) VALUES (?)", member.id)
            db.commit()
            print(colored(f"[misc]: {member.name}#{member.discriminator} has been added into the users DB...", "green"))

        except:
            print(colored(f"[misc]: Internal error occurred when adding {member.name}#{member.discriminator} to databases...", "red"))

        #dm welcome message to new member
        userJoinPrivateEmbed = discord.Embed(
            colour = discord.Colour.green(),
            title = "Welcome "+member.name+"!",
            description = "Thank you for joining this help server! If you have any questions dm my owner Timmy!"
        )

        try:
            await member.send(embed=userJoinPrivateEmbed)
            print(colored(f"[misc]: successfully sent welcome message to {member.name}#{member.discriminator}...", "green"))

        except:
            print(colored(f"[misc]: couldn't send welcome message to {member.name}#{member.discriminator}...", "red"))

        #add role 'new here' to user
        new_here = member.guild.get_role(791162885002100793)

        try:
            await member.add_roles(new_here)
            print(colored("[misc]: Added '{}' to {}".format(new_here.name, member.name) + "...", "green"))

        except:
            print(colored("[misc]: Couldn't add role '{}' to {}".format(new_here.name, member.name) + "...", "red"))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(colored(f"[misc]: {member.name}#{member.discriminator} left at {current_time}...", "green"))

        #deleting user from databases
        try:
            db.execute("DELETE FROM users WHERE (UserID = ?)", member.id)
            db.commit()
            print(colored(f"[misc]: Successfully removed {member.name}#{member.discriminator} from users db...", "green"))

        except:
            print(colored(f"[misc]: Internal error occurred when removing {member.id}#{member.discriminator} from users db...", "red"))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self.role_message_id:
            return

        role_id = self.emoji_to_role[payload.emoji]
        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            print("not in guild")
            return

        await payload.member.add_roles(role)
        print("sucessfull")

    # #starboard
    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #     if payload.emoji.name == "⭐":
    #         message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    #         if payload.channel_id == 814897487370125353:
    #             if not message.author.bot and payload.user_id != message.author.id:
    #                 user = db.record("SELECT UserID FROM starboard WHERE UserID = (?)", message.author.id)
    #                 if user is not None:
    #                     star = 1
    #                     db.execute("UPDATE starboard SET Stars = Stars + ? WHERE UserID = ?",
    #                         star,
    #                         message.author.id
    #                     )
    #                     db.commit()
    #                     print(colored(f"[misc]: Added a star to {message.author} who helped someone in python channel...", "green"))
    #
    #                 else:
    #                     db.execute("INSERT OR IGNORE INTO starboard (UserID) VALUES (?)", message.author.id)
    #                     db.commit()
    #                     print(colored(f"[misc]: Added {message.author} to starboard db...", "green"))
    #
    #             else:
    #                 user = db.record("SELECT UserID FROM starboard WHERE UserID = (?)", message.author.id)
    #                 star = 3
    #                 db.execute("UPDATE starboard SET Stars = Stars - ? WHERE UserID = ?",
    #                     star,
    #                     message.author.id
    #                 )
    #                 db.commit()
    #                 print(colored(f"[misc]: {message.author} tried to cheat the starboard...", "green"))
    #
    #         else:
    #             pass
    #
    #     else:
    #         return
    #
    #
    # @commands.command()
    # async def starboard(self, context):
    #     print(colored(f"[misc]: {context.author} accessed starboard...", "green"))
    #     async with context.typing():
    #         await asyncio.sleep(1)
    #         records = db.records("SELECT UserID, Stars FROM starboard ORDER BY Stars DESC")
    #         menu = MenuPages(source=Menu(context, records), clear_reactions_after=True, timeout=100.0)
    #         await menu.start(context)
    #
    #
    # @commands.command()
    # async def stars(self, context, target: Optional[Member]):
    #     print(colored(f"[misc]: {context.author} accessed stars...", "green"))
    #     target = target or context.author
    #     ids = db.column("SELECT UserID FROM starboard ORDER BY Stars DESC")
    #
    #     python, javascript, java = db.record(
    #         "SELECT Python, Javascript, Java FROM Starboard WHERE UserID = ?", target.id
    #     ) or (None, None, None)
    #
    #     if stars is not None:
    #         async with context.typing():
    #             await asyncio.sleep(1)
    #             embedColour = discord.Embed.Empty
    #             if hasattr(context, 'guild') and context.guild is not None:
    #                 embedColour = context.me.top_role.colour
    #             embed = discord.Embed(colour=embedColour)
    #             embed.add_field(name=f"**Stars**", value=f"**{target.display_name}** has **{python:,}** python, **{javascript:,}** javascript, and is rank **{ids.index(target.id)+1}** of {len(ids):,} users globally.")
    #             await context.message.channel.send(embed=embed)
    #     else:
    #         async with context.typing():
    #             await asyncio.sleep(1)
    #             await context.channel.send("You haven't helped anybody yet :(")




def setup(client):
    client.add_cog(misc(client))
