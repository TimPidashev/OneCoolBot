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
import sqlite3

class misc(commands.Cog):
    def __init__(self, client):
        self.client = client

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
        print(colored(f"[misc]: {member.name}#{member.discriminator} joined at {member.joined_at}" + "...", "green"))

        #adding user to database
        try:
            db.execute("INSERT INTO users (UserID) VALUES (?)", member.id)
            db.commit()
            print(colored(f"[misc]: {member.name}#{member.discriminator} (member/user) have been added into the users DB...", "green"))

        except:
            print(colored(f"[misc]: Internal error occurred when adding {member.name}#{member.discriminator} to databases...", "red"))

        #dm welcome message to new member
        userJoinPrivateEmbed = discord.Embed(
            colour = discord.Colour.green(),
            title = "Welcome "+member.name+"!",
            description = "I'm still in early development, so if you have any ideas as to what i should say here, let me know!"
        )

        try:
            await member.send(embed=userJoinPrivateEmbed)
            print(colored(f"[misc]: successfully sent welcome message to {member.name}#{member.discriminator}...", "green"))

        except:
            print(colored(f"[misc]: couldn't send welcome message to {member.name}#{member.discriminator}...", "red"))

        #add role 'new here' to user
        role = member.guild.get_role(791162885002100793)

        try:
            await member.add_roles(role)
            print(colored("[misc]: Added '{}' to {}".format(role.name, member.name) + "...", "green"))

        except:
            print(colored("[misc]: Couldn't add role '{}' to {}".format(role.name, member.name) + "...", "red"))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(colored(f"[misc]: {member.name}#{member.discriminator} left at " + current_time + "...", "green"))

        #deleting user from databases
        try:
            db.execute("DELETE FROM users WHERE (UserID = ?)", member.id)
            db.commit()
            print(colored(f"[misc]: Successfully removed {member.name}#{member.discriminator} from users db...", "green"))

        except:
            print(colored(f"[misc]: Internal error occurred when removing {member.id}#{member.discriminator} from users db...", "red"))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        #Python
        if payload.emoji.name == "⭐":
            message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if payload.channel_id == 810324712180940821:
                if not message.author.bot and payload.user_id != message.author.id:
                    user = db.record("SELECT UserID FROM starboard WHERE UserID = (?)", message.author.id)
                    if user is not None:
                        star = 1
                        python_star = 1
                        db.execute("UPDATE starboard SET Stars = Stars + ?, Python = Python + ? WHERE UserID = ?",
                            star,
                            python_star,
                            message.author.id
                        )
                        db.commit()
                        print(colored(f"[misc]: Added a star to {message.author} who helped someone in python channel...", "green"))

                    else:
                        db.execute("INSERT OR IGNORE INTO starboard (UserID) VALUES (?)", message.author.id)
                        db.commit()
                        print(colored(f"[misc]: Added {message.author} to starboard db...", "green"))

                else:
                    print(colored("[misc]: Somebody tried adding themself a star but was stopped...", "green"))

        #Javascript
        if payload.emoji.name == "⭐":
            message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if payload.channel_id == 810324738743205898:
                if not message.author.bot and payload.user_id != message.author.id:
                    user = db.record("SELECT UserID FROM starboard WHERE UserID = (?)", message.author.id)
                    if user is not None:
                        star = 1
                        javascript_star = 1
                        db.execute("UPDATE starboard SET Stars = Stars + ?, Javascript = Javascript + ? WHERE UserID = ?",
                            star,
                            javascript_star,
                            message.author.id
                        )
                        db.commit()
                        print(colored(f"[misc]: Added a star to {message.author} who helped someone in javascript channel...", "green"))

                    else:
                        db.execute("INSERT OR IGNORE INTO starboard (UserID) VALUES (?)", message.author.id)
                        db.commit()
                        print(colored(f"[misc]: Added {message.author} to starboard db...", "green"))

                else:
                    print(colored("[misc]: Somebody tried adding themself a star but was stopped...", "green"))

        #Java
        if payload.emoji.name == "⭐":
            message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if payload.channel_id == 810324756137115688:
                if not message.author.bot and payload.user_id != message.author.id:
                    user = db.record("SELECT UserID FROM starboard WHERE UserID = (?)", message.author.id)
                    if user is not None:
                        star = 1
                        java_star = 1
                        db.execute("UPDATE starboard SET Stars = Stars + ?, Java = Java + ? WHERE UserID = ?",
                            star,
                            java_star,
                            message.author.id
                        )
                        db.commit()
                        print(colored(f"[misc]: Added a star to {message.author} who helped someone in java channel...", "green"))

                    else:
                        db.execute("INSERT OR IGNORE INTO starboard (UserID) VALUES (?)", message.author.id)
                        db.commit()
                        print(colored(f"[misc]: Added {message.author} to starboard db...", "green"))

                else:
                    print(colored("[misc]: Somebody tried adding themself a star but was stopped...", "green"))

        else:
            return

def setup(client):
    client.add_cog(misc(client))
