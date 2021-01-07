import discord
import asyncio
import json
from datetime import datetime
from discord.ext import commands

class joinleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("cog joinleave online...")

    #on_member_join
    @commands.Cog.listener()
    async def on_member_join(self, member):

        print(f"{member.name}#{member.discriminator} joined at {member.joined_at}" + "...")
        general = await self.bot.fetch_channel(791160100567384098)

        userJoinPrivateEmbed = discord.Embed(
            colour = discord.Colour.green(),
            title = "Welcome "+member.name+"!",
            description = "We're so glad you're here!"
        )

        userJoinServerEmbed = discord.Embed(
            colour = discord.Colour.green(),
            title = "Welcome "+member.name+"!",
            description = "We're so glad you're here!"
        )

        try:
            await member.send(embed=userJoinPrivateEmbed)
            await general.send(embed=userJoinServerEmbed)
            print("successfully sent welcome message to " + member.name + "...")

        except:
            print("couldn't send welcome message to " + member.name + "...")

        role = member.guild.get_role(791162885002100793)

        try:
            await member.add_roles(role)
            print("Added '{}' to {}".format(role.name, member.name + "..."))

        except:
            print("Couldn't add role '{}' to {}".format(role.name, member.name) + "...")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"{member.name}#{member.discriminator} left at " + current_time + "...")


def setup(client):
    client.add_cog(joinleave(client))
