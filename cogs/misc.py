import discord
import asyncio
import json
from db import db
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from termcolor import colored

class misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[misc]: online...", "green"))

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
            print(colored(f"[misc]: {member.name}#{member.discriminator} (member/user) have been added into the users DB...", "green"))
            db.commit()

        except:
            print(colored(f"[misc]: Internal error occurred when adding {member.name}#{member.discriminator} to users db...", "red"))

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

def setup(client):
    client.add_cog(misc(client))
