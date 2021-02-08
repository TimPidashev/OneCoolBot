import discord
import asyncio
import re
from discord.ext import commands, tasks
from discord.utils import get
from termcolor import colored

class moderation(commands.Cog):
    def __init__(self, client):
        self.bot = client

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[moderation]: cog moderation online...", "yellow"))

    #clear
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, context, amount=10):
        await context.channel.purge(limit=amount)
        print(colored(f"[moderation]: removed {amount} messages...", "yellow"))

    #kick
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member, *, reason=None):
        kickServerEmbed = discord.Embed(
            colour = discord.Colour.red(),
            title = f"{context.author} kicked {member.name}!",
            description = f"**Reason:** {reason}\n**By:** {context.author.mention}",
        )
        kickPrivateEmbed = discord.Embed(
            colour = discord.Colour.red(),
            title = f"Oh no! You were kicked by {context.author}!",
            description = f"**Reason:** {reason}\n"
        )
        try:
            await context.channel.send(embed=kickServerEmbed)
            await member.send(embed=kickPrivateEmbed)
            await member.kick(reason=reason)
            print(colored(f"[moderation]: {context.author} kicked {member}...", "yellow"))
        except:
            print(colored(f"[moderation]: an error occured while {context.author} was trying to kick/kicked {member}...", "red"))

    #ban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *, reason=None):
       banServerEmbed = discord.Embed(
            colour = discord.Colour.red(),
            title = f"{context.author} banned {member.name}!",
            description = f"**Reason:** {reason}\n**By:** {context.author.mention}",
       )
       banPrivateEmbed = discord.Embed(
            colour = discord.Colour.red(),
            title = f"Oh no! You were banned by {context.author}!",
            description = f"**Reason:** {reason}\n"
       )
       try:
           await context.channel.send(embed=banServerEmbed)
           await member.send(embed=banPrivateEmbed)
           await member.ban(reason=reason)
           print(colored(f"[moderation]: {context.author} banned {member}...", "yellow"))
       except:
            print(colored(f"[moderation]: an error occured while {context.author} was trying to ban/banned {member}...", "red"))

    #unban(works, but needs help)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, context, *, member):
        banned_users = await context.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await context.guild.unban(user)
                unbanServerEmbed = discord.Embed(
                    colour = discord.Colour.green(),
                    title = f"{context.author} unbanned {user.name}#{user.discriminator}!",
                    description = f"**Reason:** Good Behavior **By:** {context.author.mention}",
                )
                await context.channel.send(embed=unbanServerEmbed)
                print(colored(f"[moderation]:  {context.author} unbanned {user.name}#{user.discriminator}...", "yellow"))
                return
            else:
                print(colored(f"[moderation]: {context.author} tried to unban/unbanned {user.name}#{user.discriminator}, but internal error occured...", "red"))

    #automoderation section below
    @commands.Cog.listener()
    async def on_message(self, message):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',message.content.lower())
        if urls is not None and message.content.startswith('https://discord.gg' or 'http://discord.gg'):
            await message.channel.purge(limit=1)
            await message.channel.send("Links are not allowed!")
            print(colored(f"[automoderation]: {message.author} tried to advertise link {message.content} but was stopped...", "yellow"))
            return

def setup(client):
    client.add_cog(moderation(client))
