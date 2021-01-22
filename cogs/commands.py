import discord
import asyncio
import psutil
import time
import os
from termcolor import colored
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime, timedelta

#uptime
start_time = time.time()

#roles
moderator = (791161649901207572)
owner = (791163340323815435)

class commands(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.process = psutil.Process(os.getpid())

    #on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[commands]: cog commands online...", "white"))

    #info
    @commands.guild_only()
    @commands.command()
    async def info(self, context):
        print(colored("[commands]: command(info) used...", "white"))

        """ About the bot """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        ping = (time.monotonic() - before) * 1000
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))
        embedColour = discord.Embed.Empty
        if hasattr(context, 'guild') and context.guild is not None:
            embedColour = context.me.top_role.colour
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(timedelta(seconds=difference))
        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=context.bot.user.avatar_url)
        embed.add_field(name="Developer", value="𝓣𝓲𝓶𝓶𝔂#6955")
        embed.add_field(name="Servers", value=f"{len(context.bot.guilds)}", inline=True)
        embed.add_field(name="Ping", value=f"{before_ws}ms")
        embed.add_field(name="RAM Usage", value=f"{ramUsage:.2f} MB", inline=True)
        embed.add_field(name="Uptime", value=text, inline=True)
        embed.add_field(name="Version", value="Ver 0.0.7")
        embed.set_footer(text="Copyright © 2021 - All Rights Reserved.")
        await context.message.channel.send(embed=embed)

    #help
    @commands.guild_only()
    @commands.command()
    async def help(self, context):
        print(colored("[commands]: command(help) used...", "white"))
        embed = discord.Embed(title="Help", color=2105637)
        embed.add_field(name="Bot Related", value="info, help")
        embed.add_field(name="AutoRole/Level/XP System(Coming Soon!)", value="rank, leaderboard", inline=False)
        embed.add_field(name="Economy(Coming Soon!)", value="bank, market, inventory", inline=False)
        embed.add_field(name="Mod Commands(requires moderator role)", value="kick, mute, ban, unban, clear", inline=False)
        embed.add_field(name="Music", value="connect, play, pause, resume, skip, stop, volume, shuffle, equalizer, queue, current, swap, music, spotify")
        await context.message.channel.send(embed=embed)

    #code i dont want to get rid of for reference...
    @commands.guild_only()
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

def setup(client):
    client.add_cog(commands(client))
