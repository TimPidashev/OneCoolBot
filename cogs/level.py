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

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            result = db.record("SELECT UserID FROM users WHERE UserID = (?)", message.author.id)
            if result is not None:
                xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM users WHERE UserID = ?", message.author.id)
                if datetime.utcnow() > datetime.fromisoformat(xplock):

                    xp_to_add = random.randint(10, 20)
                    new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)
                    coins_on_xp = random.randint(1, 10)
                    db.execute("UPDATE users SET XP = XP + ?, Level = ?, Coins = Coins + ?, XPLock = ? WHERE UserID = ?",
                        xp_to_add,
                        new_lvl,
                        coins_on_xp,
                        (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
                        message.author.id
                    )

                    db.commit()
                    print(colored(f"[level]: Added {xp_to_add} xp to {message.author}...", "cyan"))
                    print(colored(f"[economy]: Added {coins_on_xp} coins to {message.author}...", "blue"))

                    if new_lvl > lvl:
                        await message.channel.send(f":partying_face: {message.author.mention} is now level **{new_lvl:,}**!")
                        print(colored(f"[level]: {message.author} has leveled up to {new_lvl:,}...", "cyan"))

                        coins = db.record("SELECT Coins FROM users WHERE UserID = ?", message.author.id)

                        coins_to_add = random.randint(10, 1000)

                        db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                            coins_to_add,
                            message.author.id
                        )

                        db.commit()
                        print(colored(f"[economy]: Added {coins_to_add} coins to {message.author} on level up...", "blue"))

                        if new_lvl == 5:
                            new_here = message.guild.get_role(791162885002100793)
                            await message.author.remove_roles(new_here)
                            print(colored(f"[level]: Removed {new_here.name} from {message.author}...", "cyan"))

                            white_belt = message.guild.get_role(791161672957558834)
                            await message.author.add_roles(white_belt)
                            print(colored(f"[level]: Added {white_belt.name} to {message.author}...", "cyan"))

                            coins1 = db.record("SELECT Coins FROM users WHERE UserID = ?", message.author.id)

                            coins1_to_add = random.randint(1000, 5000)

                            db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                                coins1_to_add,
                                message.author.id
                            )

                            db.commit()
                            print(colored(f"[economy]: Added {coins1_to_add} coins to {message.author} due to major level up...", "blue"))

                            embed = discord.Embed(
                                colour = discord.Colour.green(),
                                title = f":partying_face: Hooray, you have gotten the {white_belt.name} role!",
                                description = f"You recieved :coin: {coins1_to_add} coins!"
                            )
                            await message.author.send(embed=embed)

                        elif new_lvl == 10:
                            yellow_belt = message.guild.get_role(791161670080004126)
                            await message.author.add_roles(yellow_belt)
                            print(colored(f"[level]: Added {yellow_belt.name} to {message.author}...", "cyan"))

                            coins2 = db.record("SELECT Coins FROM users WHERE UserID = ?", message.author.id)

                            coins2_to_add = random.randint(5000, 10000)

                            db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                                coins2_to_add,
                                message.author.id
                            )

                            db.commit()
                            print(colored(f"[economy]: Added {coins2_to_add} coins to {message.author} due to major level up...", "blue"))

                            embed = discord.Embed(
                                colour = discord.Colour.green(),
                                title = f":partying_face: Hooray, you have gotten the {yellow_belt.name} role!",
                                description = f"You recieved :coin: {coins2_to_add} coins!"
                            )
                            await message.author.send(embed=embed)

                        elif new_lvl == 20:
                            orange_belt = message.guild.get_role(791161667148840970)
                            await message.author.add_roles(orange_belt)
                            print(colored(f"[level]: Added {orange_belt.name} to {message.author}...", "cyan"))

                            coins3 = db.record("SELECT Coins FROM users WHERE UserID = ?", message.author.id)

                            coins3_to_add = random.randint(10000, 20000)

                            db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                                coins3_to_add,
                                message.author.id
                            )

                            db.commit()
                            print(colored(f"[economy]: Added {coins3_to_add} coins to {message.author} due to major level up...", "blue"))

                            embed = discord.Embed(
                                colour = discord.Colour.green(),
                                title = f":partying_face: Hooray, you have gotten the {orange_belt.name} role!",
                                description = f"You recieved :coin: {coins3_to_add} coins!"
                            )
                            await message.author.send(embed=embed)

                        elif new_lvl == 30:
                            green_belt = message.guild.get_role(791161664296058890)
                            await message.author.add_roles(green_belt)
                            print(colored(f"[level]: Added {green_belt.name} to {message.author}...", "cyan"))

                            coins4 = db.record("SELECT Coins FROM users WHERE UserID = ?", message.author.id)

                            coins4_to_add = random.randint(20000, 30000)

                            db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                                coins4_to_add,
                                message.author.id
                            )

                            db.commit()
                            print(colored(f"[economy]: Added {coins4_to_add} coins to {message.author} due to major level up...", "blue"))

                            embed = discord.Embed(
                                colour = discord.Colour.green(),
                                title = f":partying_face: Hooray, you have gotten the {green_belt.name} role!",
                                description = f"You recieved :coin: {coins4_to_add} coins!"
                            )
                            await message.author.send(embed=embed)

                        elif new_lvl == 40:
                            blue_belt = message.guild.get_role(791161661293330432)
                            await message.author.add_roles(blue_belt)
                            print(colored(f"[level]: Added {blue_belt.name} to {message.author}...", "cyan"))

                            coins5 = db.record("SELECT Coins FROM users WHERE UserID = ?", message.author.id)

                            coins5_to_add = random.randint(30000, 40000)

                            db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                                coins5_to_add,
                                message.author.id
                            )

                            db.commit()
                            print(colored(f"[economy]: Added {coins5_to_add} coins to {message.author} due to major level up...", "blue"))

                            embed = discord.Embed(
                                colour = discord.Colour.green(),
                                title = f":partying_face: Hooray, you have gotten the {blue_belt.name} role!",
                                description = f"You recieved :coin: {coins5_to_add} coins!"
                            )
                            await message.author.send(embed=embed)

                        elif new_lvl == 50:
                            purple_belt = message.guild.get_role(791161658406993940)
                            await message.author.add_roles(purple_belt)
                            print(colored(f"[level]: Added {purple_belt.name} to {message.author}...", "cyan"))

                            coins6 = db.record("SELECT Coins FROM users WHERE UserID = ?", message.author.id)

                            coins6_to_add = random.randint(40000, 50000)

                            db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                                coins6_to_add,
                                message.author.id
                            )

                            db.commit()
                            print(colored(f"[economy]: Added {coins6_to_add} coins to {message.author} due to major level up...", "blue"))

                            embed = discord.Embed(
                                colour = discord.Colour.green(),
                                title = f":partying_face: Hooray, you have gotten the {purple_belt.name} role!",
                                description = f"You recieved :coin: {coins6_to_add} coins!"
                            )
                            await message.author.send(embed=embed)

                        elif new_lvl == 75:
                            black_belt = message.guild.get_role(791161652971962378)
                            await message.author.add_roles(black_belt)
                            print(colored(f"[level]: Added {black_belt.name} to {message.author}...", "cyan"))

                            coins7 = db.record("SELECT Coins FROM users WHERE UserID = ?", message.author.id)

                            coins7_to_add = random.randint(50000, 75000)

                            db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                                coins7_to_add,
                                message.author.id
                            )

                            db.commit()
                            print(colored(f"[economy]: Added {coins7_to_add} coins to {message.author} due to major level up...", "blue"))

                            embed = discord.Embed(
                                colour = discord.Colour.green(),
                                title = f":partying_face: Hooray, you have gotten the {black_belt.name} role!",
                                description = f"You recieved :coin: {coins7_to_add} coins!"
                            )
                            await message.author.send(embed=embed)

                        elif new_lvl == 100:
                            moderator = message.guild.get_role(791161649901207572)
                            await message.author.add_roles(moderator)
                            print(colored(f"[level]: Added {moderator.name} to {message.author}...", "cyan"))

                            coins8 = db.record("SELECT Coins FROM users WHERE UserID = ?", message.author.id)

                            coins8_to_add = random.randint(75000, 100000)

                            db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                                coins8_to_add,
                                message.author.id
                            )

                            db.commit()
                            print(colored(f"[economy]: Added {coins8_to_add} coins to {message.author} due to major level up...", "blue"))

                            embed = discord.Embed(
                                colour = discord.Colour.green(),
                                title = f":partying_face: Hooray, you have gotten the {moderator.name} role!",
                                description = f"You recieved :coin: {coins8_to_add} coins!"
                            )
                            await message.author.send(embed=embed)
                            await message.author.send(f":partying_face: Hooray, you have gotten the {moderator.name} role!")

                else:
                    pass

            else:
                db.execute("INSERT OR IGNORE INTO users (UserID) VALUES (?)", message.author.id)
                db.commit()
                print(colored(f"[level]: {message.author}#{message.author.discriminator} was added to lebel db...", "cyan"))


    @commands.command()
    async def rank(self, context, target: Optional[Member]):
        print(colored(f"[level]: {context.author} accessed rank...", "cyan"))
        target = target or context.author

        result = db.record(f"SELECT XP, Level FROM users WHERE UserID = {target.id}")

        if result is not None:
            async with context.typing():
                await asyncio.sleep(1)

                img = Image.open("./data/rank.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("./data/Quotable.otf", 35)
                font1 = ImageFont.truetype("./data/Quotable.otf", 24)
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(context.author.avatar_url)) as response:
                        image = await response.read()
                icon = Image.open(BytesIO(image)).convert("RGBA")
                img.paste(icon.resize((156, 156)), (50, 60))
                draw.text((242, 100), f"{str(result[1])}", (140, 86, 214), font=font)
                draw.text((242, 180), f"{str(result[0])}", (140, 86, 214), font=font)
                draw.text((50,220), f"{context.author.name}", (140, 86, 214), font=font1)
                draw.text((50,240), f"#{context.author.discriminator}", (255, 255, 255), font=font1)
                img.save("./data/infoimg2.png")
                ffile = discord.File("./data/infoimg2.png")
                await context.send(file=ffile)

        else:
            async with context.typing():
                await asyncio.sleep(1)
                await context.channel.send("You are not in the database :(")

    @commands.command()
    async def leaderboard(self, context):
        print(colored(f"[level]: {context.author} accessed leaderboard...", "cyan"))
        async with context.typing():
            await asyncio.sleep(1)
            records = db.records("SELECT UserID, XP FROM users ORDER BY XP DESC")
            menu = MenuPages(source=Menu(context, records), clear_reactions_after=True, timeout=100.0)
            await menu.start(context)

def setup(client):
    client.add_cog(level(client))
