import discord
import asyncio
import json
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
        general = await self.bot.fetch_channel(791160100567384098)

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
        print(colored(f"[joinleave]: {member.name}#{member.discriminator} left at " + current_time + "...", "red"))


def setup(client):
    client.add_cog(joinleave(client))
