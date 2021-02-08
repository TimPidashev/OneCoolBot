import discord
import asyncio
import json
from db import db
from datetime import datetime
from discord.ext import commands
from termcolor import colored

class joinleave(commands.Cog):
    def __init__(self, client):
        self.bot = client

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[joinleave]: cog joinleave online...", "green"))

    #on_member_join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(colored(f"[joinleave]: {member.name}#{member.discriminator} joined at {member.joined_at}" + "...", "green"))

        #adding user to database
        try:
            db.execute("INSERT INTO users (UserID) VALUES (?)", member.id)
            print(colored(f"[joinleave]: {member.name}#{member.discriminator} (member/user) have been added into the users DB...", "green"))
            db.commit()

        except:
            print(colored(f"[joinleave]: Internal error occurred when adding {member.name}#{member.discriminator} to users db...", "red"))

        #dm welcome message to new member
        userJoinPrivateEmbed = discord.Embed(
            colour = discord.Colour.green(),
            title = "Welcome "+member.name+"!",
            description = "We're so glad you're here!"
        )

        try:
            await member.send(embed=userJoinPrivateEmbed)
            print(colored(f"[joinleave]: successfully sent welcome message to {member.name}#{member.discriminator}...", "green"))

        except:
            print(colored(f"[joinleave]: couldn't send welcome message to {member.name}#{member.discriminator}...", "red"))

        #add role 'new here' to user
        role = member.guild.get_role(791162885002100793)

        try:
            await member.add_roles(role)
            print(colored("[joinleave]: Added '{}' to {}".format(role.name, member.name) + "...", "green"))

        except:
            print(colored("[joinleave]: Couldn't add role '{}' to {}".format(role.name, member.name) + "...", "red"))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(colored(f"[joinleave]: {member.name}#{member.discriminator} left at " + current_time + "...", "green"))

        #deleting user from databases
        try:
            db.execute("DELETE FROM users WHERE (UserID = ?)", member.id)
            db.commit()
            print(colored(f"[joinleave]: Successfully removed {member.name}#{member.discriminator} from users db...", "green"))

        except:
            print(colored(f"[joinleave]: Internal error occurred when removing {member.id}#{member.discriminator} from users db...", "red"))



def setup(client):
    client.add_cog(joinleave(client))
