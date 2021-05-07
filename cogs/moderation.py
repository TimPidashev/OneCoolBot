import discord
import asyncio
import re
import sqlite3
import log
from better_profanity import profanity
from discord.ext import commands, tasks
from discord.utils import get
from termcolor import colored

profanity.load_censor_words_from_file("./data/profanity.txt")

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
       await log.online(self)

    #clear
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, context, amount=10):
        await context.channel.purge(limit=amount+1)
        print(colored("[moderation]:", "magenta"), colored(f"removed {amount} messages...", "yellow"))

    #kick
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member, *, reason=None):
        embed1 = discord.Embed(
            colour = discord.Colour.red(),
            title = f"{context.author} kicked {member.name}!",
            description = f"**Reason:** {reason}\n**By:** {context.author.mention}",
        )
        embed2 = discord.Embed(
            colour = discord.Colour.red(),
            title = f"Oh no! You were kicked by {context.author}!",
            description = f"**Reason:** {reason}\n"
        )
        try:
            await context.channel.send(embed=embed1)
            await member.send(embed=embed2)
            await member.kick(reason=reason)
            print(colored("[moderation]:", "magenta"), colored(f"{context.author} kicked {member}...", "yellow"))
        except:
            print(colored("[moderation]:", "magenta"), colored(f"an error occured while {context.author} was trying to kick/kicked {member}...", "red"))

    #ban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *, reason=None):
       embed1 = discord.Embed(
            colour = discord.Colour.red(),
            title = f"{context.author} banned {member.name}!",
            description = f"**Reason:** {reason}\n**By:** {context.author.mention}",
       )
       embed2 = discord.Embed(
            colour = discord.Colour.red(),
            title = f"Oh no! You were banned by {context.author}!",
            description = f"**Reason:** {reason}\n"
       )
       try:
           await context.channel.send(embed=embed1)
           await member.send(embed=embed2)
           await member.ban(reason=reason)
           print(colored("[moderation]:", "magenta"), colored(f"{context.author} banned {member}...", "yellow"))
       except:
            print(colored("[moderation]:", "magenta"), colored(f"an error occured while {context.author} was trying to ban/banned {member}...", "red"))

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
                embed = discord.Embed(
                    colour = discord.Colour.green(),
                    title = f"{context.author} unbanned {user.name}#{user.discriminator}!",
                    description = f"**Reason:** Good Behavior **By:** {context.author.mention}",
                )
                await context.channel.send(embed=unban)
                print(colored("[moderation]:", "magenta"), colored(f"{context.author} unbanned {user.name}#{user.discriminator}...", "yellow"))

            else:
                print(colored("[moderation]:", "magenta"), colored(f"{context.author} tried to unban/unbanned {user.name}#{user.discriminator}, but internal error occured...", "red"))

    #automoderation section below
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',message.content.lower())
            if urls is not None and message.content.startswith('https://discord.gg' or 'http://discord.gg'):
                await message.delete()
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = f"**Warning**",
                    description = "Discord invite links are not allowed!"
                )
                await message.author.send(embed=embed)
                print(colored("[moderation]:", "magenta"), colored(f"{message.author} tried to advertise: {message.content}...", "yellow"))

            elif profanity.contains_profanity(message.content):
                await message.delete()
                embed = discord.Embed(
                    colour = discord.Colour.red(),
                    title = f"**Warning**",
                    description = "Profanity is not allowed on this server!"
                )
                await message.author.send(embed=embed)
                print(colored("[moderation]:", "magenta"), colored(f"{message.author}'s message({message.content}) was deleted...", "yellow"))

        else:
            pass


def setup(client):
    client.add_cog(moderation(client))
