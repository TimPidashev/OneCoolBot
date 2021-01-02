import discord
import asyncio
from discord.ext import commands, tasks
from discord.utils import get

#roles
moderator = (791161649901207572)
owner = (791163340323815435)

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("cog commands online...")

    #info
    @commands.command()
    async def info(self, context):
        print("command(info) used...")
        await context.message.channel.send("<@790701838164557854> is a discord bot written in Discord.py, owned and maintained by <@598625004279693460>")

    #changelog
    @commands.command()
    async def changelog(self, context):
        print("command(changelog) used...")
        changelogEmbed = discord.Embed(title="Changelog", description="Bot Changelog", color=2105637)
        changelogEmbed.add_field(name="Version 0.0.4(In Development)", value="Implement Database, autoshard bot, and other misc upgrades... ", inline=False)
        changelogEmbed.add_field(name="Version 0.0.3(Current)", value="Added CommandErrorHandler cog | Added moderation(ban, unban, kick, clear) | Added xp cog(levels) | Changed bot profile | Minor bug fixes", inline=False)
        changelogEmbed.add_field(name="Version 0.0.2", value="Added cogs functionality | Added 2 cogs(commands, onMemberJoin)", inline=False)
        changelogEmbed.add_field(name="Version 0.0.1", value="Added a terminal output for all the bot interactions | Added a join message | added bot status(playing .help)", inline=False)
        changelogEmbed.add_field(name="Version 0.0.0", value="Created the bot! | added an event(Bot Startup) | added a command(version)", inline=False)
        await context.message.channel.send(embed=changelogEmbed)

    #code i dont want to get rid of for reference...
    @commands.command()
    async def pages(self, context):
        contents = ["This is page 1!", "This is page 2!", "This is page 3!", "This is page 4!"]
        pages = 4
        cur_page = 1
        message = await context.send(f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        def check(reaction, user):
            return user == context.author and str(reaction.emoji) in ["◀️", "▶️"]
        while True:
            try:
                reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)
                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                    await message.remove_reaction(reaction, user)
                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

    #version
    @commands.command()
    async def version(self, context):
        print("command(version) used...")
        versionEmbed = discord.Embed(title="Current Version", description="The bot is in version 0.0.3", color=2105637)
        versionEmbed.add_field(name="Version Code:", value="v0.0.3", inline=False)
        versionEmbed.add_field(name="Date Released:", value="December 23, 2020", inline=False)
        await context.message.channel.send(embed=versionEmbed)

    #help
    @commands.command()
    async def help(self, context):
        print('command(help) used...')
        helpEmbed = discord.Embed(title="Help", color=2105637)
        helpEmbed.add_field(name="Bot Related", value="info, version, help, changelog")
        helpEmbed.add_field(name="AutoRole/Level/XP System(Coming Soon!)", value="rank, leaderboard", inline=False)
        helpEmbed.add_field(name="Economy(Coming Soon!)", value="bank, market, inventory", inline=False)
        helpEmbed.add_field(name="Mod Commands(requires moderator role)", value="kick, mute, ban, unban(Doesn't exactly work yet...), clear", inline=False)
        await context.message.channel.send(embed=helpEmbed)

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
                await context.channel.send(embed=unbanServerEmbed)
                print(f"{context.author} unbanned {user.name}#{user.discriminator}...")
                return
            else:
                print(f"{context.author} tried to unban/unbanned {user.name}#{user.discriminator}, but internal error occured...")

def setup(client):
    client.add_cog(Commands(client))
