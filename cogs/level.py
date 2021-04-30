import discord
import time
import sqlite3
import asyncio
import random
import os
import aiohttp
import io
from io import BytesIO
from discord import Member, Embed
from discord.ext.commands import Cog
from typing import Optional
from os.path import isfile
from datetime import datetime, timedelta
from discord.ext.menus import MenuPages, ListPageSource
from termcolor import colored, cprint
from discord.ext import commands
from db import db
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class Menu(ListPageSource):
    def __init__(self, context, data):
        self.context = context

        super().__init__(data, per_page=10)

    async def write_page(self, menu, offset, fields=[]):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(
            title="Leaderboard",
            colour=self.context.author.colour,
        )

        embed.set_thumbnail(url=self.context.guild.me.avatar_url)
        embed.set_footer(
            text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} members."
        )

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        fields = []
        table = "\n".join(
            f"{idx+offset}. **{self.context.guild.get_member(entry[0]).name}** ~ `{entry[1]}`"
            for idx, entry in enumerate(entries)
        )

        fields.append(("Top members:", table))

        return await self.write_page(menu, offset, fields)

class level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        db.connect("./data/database.db")
        print(colored("[level]:", "magenta"), colored("online...", "green"))

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if not message.author.bot:
    #         result = db.record("SELECT GuildID, UserID FROM users WHERE (GuildID, UserId) = (?, ?)",
    #             message.guild.id,
    #             message.author.id
    #         )
    #         if result is not None:
    #             xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM users WHERE (GuildID, UserID) = (?, ?)", 
    #                 message.guild.id, 
    #                 message.author.id
    #             )
                
    #             if datetime.utcnow() > datetime.fromisoformat(xplock):

    #                 xp_to_add = random.randint(10, 20)
    #                 new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)
    #                 coins_on_xp = random.randint(1, 10)

    #                 db.execute(f"UPDATE users SET XP = XP + ?, Level = ?, Coins = Coins + ?, XPLock = ? WHERE GuildID = {message.guild.id} AND UserID = {message.author.id}",
    #                     xp_to_add,
    #                     new_lvl,
    #                     coins_on_xp,
    #                     (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
    #                 )

    #                 db.commit()
    #                 print(colored("[level]:", "magenta"), colored(f"Added {xp_to_add} xp to {message.author} in guild: {message.guild.name}...", "cyan"))
    #                 print(colored("[economy]:", "magenta"), colored(f"Added {coins_on_xp} coins to {message.author} in guild: {message.guild.name}...", "blue"))

    #                 if new_lvl > lvl:
    #                     await message.channel.send(f":partying_face: {message.author.mention} is now level **{new_lvl:,}**!")
    #                     print(colored("[level]:", "magenta"), colored(f"{message.author} has leveled up to {new_lvl:,} in guild {message.guild.name}...", "cyan"))

    #             else:
    #                 pass

    #         else:
                
    #             db.execute("INSERT OR IGNORE INTO users (GuildID, UserID) VALUES (?, ?)",
    #                 message.guild.id,
    #                 message.author.id
    #             )
    #             db.commit()
    #             print(colored("[level]:", "magenta"), colored(f"{message.author}#{message.author.discriminator} in guild: {message.guild.name} was added to users table...", "cyan"))

    # @commands.command()
    # async def rank(self, message):
    #     print(colored("[level]:", "magenta"), colored(f"{message.author} accessed rank in guild: {message.guild.name}...", "cyan"))

    #     result = db.record("SELECT XP, Level FROM users WHERE (GuildID, UserID) = (?, ?)",
    #         message.guild.id,
    #         message.author.id
    #     )

    #     if result is not None:
    #         async with message.typing():
    #             await asyncio.sleep(1)

    #             img = Image.open("./data/rank.png")
    #             draw = ImageDraw.Draw(img)
    #             font = ImageFont.truetype("./data/Quotable.otf", 35)
    #             font1 = ImageFont.truetype("./data/Quotable.otf", 24)
    #             async with aiohttp.ClientSession() as session:
    #                 async with session.get(str(message.author.avatar_url)) as response:
    #                     image = await response.read()
    #             icon = Image.open(BytesIO(image)).convert("RGBA")
    #             img.paste(icon.resize((156, 156)), (50, 60))
    #             draw.text((242, 100), f"{str(result[1])}", (140, 86, 214), font=font)
    #             draw.text((242, 180), f"{str(result[0])}", (140, 86, 214), font=font)
    #             draw.text((50,220), f"{message.author.name}", (140, 86, 214), font=font1)
    #             draw.text((50,240), f"#{message.author.discriminator}", (255, 255, 255), font=font1)
    #             img.save("./data/infoimg2.png")
    #             ffile = discord.File("./data/infoimg2.png")
    #             await message.reply(file=ffile, mention_author=False)

    #     else:
    #         async with message.typing():
    #             await asyncio.sleep(1)
    #             await message.reply("You are not in the database :(", mention_author=False)

    # @commands.command()
    # async def leaderboard(self, context):
    #     print(colored(f"[level]: {context.author} accessed leaderboard...", "cyan"))
    #     async with context.typing():
    #         await asyncio.sleep(1)
    #         records = db.records("SELECT UserID, XP FROM users ORDER BY XP DESC")
    #         menu = MenuPages(source=Menu(context, records), clear_reactions_after=True, timeout=100.0)
    #         await menu.start(context)

def setup(client):
    client.add_cog(level(client))
