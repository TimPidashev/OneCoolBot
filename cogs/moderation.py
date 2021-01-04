import discord
import asyncio
from discord.ext import commands, tasks
from discord.utils import get

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("cog moderation online...")

    #clear
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, context, amount=10):
        await context.channel.purge(limit=amount)
        print(f"removed {amount} messages...")

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
            print(f"{context.author} kicked {member}...")
        except:
            print(f"an error occured while {context.author} was trying to kick/kicked {member}...")

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
           print(f"{context.author} banned {member}...")
       except:
            print(f"an error occured while {context.author} was trying to ban/banned {member}...")

    #unban(doesn't work)
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, context, *, member):
        unbanServerEmbed = discord.Embed(
            colour = discord.Colour.green(),
            title = f"{context.author} unbanned {user.name}#{user.discriminator}!",
            description = f"**Reason:** Good Behavior **By:** {context.author.mention}",
        )
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
                print(f"{context.author} unbanned {user.name}#{user.discriminator}...")
                return
            else:
                print(f"{context.author} tried to unban/unbanned {user.name}#{user.discriminator}, but internal error occured...")

def setup(client):
    client.add_cog(moderation(client))
