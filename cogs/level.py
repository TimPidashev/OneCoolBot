import discord
import time
import sqlite3
import asyncio
import random
import os
import aiohttp
import io
import numpy
from utils import embed, log
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
from PIL import Image, ImageDraw, ImageFont
from utils import data, embed, log

class level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        db.connect("./data/database.db")
        await log.online(self)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            context = await self.client.get_context(message)
            if context.command:
                return

            level_check = await data.level_check(message)

            if level_check == "OFF":
                result = await data.find_record(message)
                
                if result is not None:
                    xp, lvl, xplock = await data.fetch_record(message)
                    if datetime.utcnow() > datetime.fromisoformat(xplock):
                        coins_on_xp = random.randint(1, 10)
                        await data.update_coins_if_levels_off(self, message, coins_on_xp)
                        return

                else:
                    await data.on_message_send(self, message)

            else:
                result = await data.find_record(message)

                if result is not None:
                    xp, lvl, xplock = await data.fetch_record(message)
                    
                    if datetime.utcnow() > datetime.fromisoformat(xplock):

                        xp_to_add = random.randint(10, 20)
                        new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)
                        coins_on_xp = random.randint(1, 10)

                        await data.update_record(self, message, xp_to_add, new_lvl, coins_on_xp)

                        if new_lvl > lvl:
                            levelmessages, levelmessagechannel = await data.level_up_check(message)
                            levelmessage = await data.fetch_levelmessage(message)

                            if levelmessages == "OFF":
                                return
                            
                            if levelmessages == "ON":
                                if levelmessagechannel == 0:
                                    await message.reply(f":partying_face: {message.author.mention} is now level **{new_lvl:,}**!", mention_author=False)
                                    await log.level_up(self, message, new_lvl)

                                else:
                                    messagechannel = self.client.get_channel(levelmessagechannel)
                                    await message.channel.send(f"{levelmessage}")
                                    await log.level_up(self, message, new_lvl)

                    else:
                        return

                else:
                    await data.on_message_send(self, message)

    @commands.command()
    async def rankold(self, context, target: Optional[Member]):
        await log.cog_command(self, context)
        target = target or context.author

        if target is not None:
            result = await data.rank_command_target(target)

        if target is None:
            result = await data.rank_command_context(context)

        if result is not None:
            async with context.typing():
                await asyncio.sleep(1)
                img = Image.open("./data/img/rank_cards/neon_simple.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("./data/fonts/Quotable.otf", 35)
                font1 = ImageFont.truetype("./data/fonts/Quotable.otf", 24)
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(target.avatar_url)) as response:
                        image = await response.read()
                icon = Image.open(BytesIO(image)).convert("RGBA")
                img.paste(icon.resize((156, 156)), (50, 60))
                draw.text((242, 100), f"{str(result[1])}", (140, 86, 214), font=font)
                draw.text((242, 180), f"{str(result[0])}", (140, 86, 214), font=font)
                draw.text((50,220), f"{target.name}", (140, 86, 214), font=font1)
                draw.text((50,240), f"#{target.discriminator}", (255, 255, 255), font=font1)
                img.save("./data/img/imgswap.png")
                ffile = discord.File("./data/img/imgswap.png")
                await context.reply(file=ffile, mention_author=False)

        else:
            await context.reply("You are not in the database :(\nDont worry though, you were just added! Try running the command again.", mention_author=False)
    
    @commands.command(aliases=["rt"])
    async def ranktest(self, context, target: Optional[Member]):
        await log.cog_command(self, context)
        target = target or context.author
        if target is not None:
            exp, level = await data.rank_command_target(target)
            ids = db.column(f"SELECT UserID FROM users WHERE GuildID = {target.guild.id} ORDER BY XP DESC")
            message_count = db.record(f"SELECT GlobalMessageCount FROM users WHERE UserID = {context.author.id} and GuildID = {context.guild.id}")[0]

        if exp or level is not None:
            async with context.typing():
                await asyncio.sleep(1)

                rank = f"{ids.index(target.id)+1}"
                final_xp = 100
                xp = exp
                user_name = str(target.name)
                discriminator = f"#{target.discriminator}"

                new_lvl = int(((xp) // 42) ** 0.55)
                print(new_lvl)

                background = Image.new("RGB", (1000, 240))
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(target.avatar_url)) as response:
                        image = await response.read()
                        icon = Image.open(BytesIO(image)).convert("RGBA").resize((200, 200))
                        bigsize = (icon.size[0] * 3, icon.size[1] * 3)
                        mask = Image.new("L", bigsize, 0)
                        draw = ImageDraw.Draw(mask)
                        draw.ellipse((0, 0) + bigsize, 255)
                        mask = mask.resize(icon.size, Image.ANTIALIAS)
                        icon.putalpha(mask)
                        background.paste(icon, (20, 20), mask=icon)
                        draw = ImageDraw.Draw(background, "RGB")
                        big_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 60, encoding="utf-8")
                        medium_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 40, encoding="utf-8")
                        small_font = ImageFont.FreeTypeFont("./data/fonts/ABeeZee-Regular.otf", 30, encoding="utf-8")

                        text_size = draw.textsize(str(level), font=big_font)
                        offset_x = 1000 - 15 - text_size[0]
                        offset_y = 10
                        draw.text((offset_x, offset_y), str(level), font=big_font, fill="#11ebf2")
                        text_size = draw.textsize("LEVEL", font=small_font)
                        offset_x -= text_size[0] + 5
                        draw.text((offset_x, offset_y + 27), "LEVEL", font=small_font, fill="#11ebf2")

                        text_size = draw.textsize(f"#{rank}", font=big_font)
                        offset_x -= text_size[0] + 15
                        draw.text((offset_x, offset_y), f"#{rank}", font=big_font, fill="#fff")
                        text_size = draw.textsize("RANK", font=small_font)
                        offset_x -= text_size[0] + 5
                        draw.text((offset_x, offset_y + 27), "RANK", font=small_font, fill="#fff")
                        
                        # draw.text((offset_x, offset_y), f"#{message_count}", font=big_font, fill="#fff")
                        # text_size = draw.textsize("KARMA", font=small_font)
                        # offset_x -= text_size[0] + 15
                        # draw.text((offset_x, offset_y + 27), "KARMA", font=small_font, fill="#fff")

                        bar_offset_x = 320
                        bar_offset_y = 160
                        bar_offset_x_1 = 950
                        bar_offset_y_1 = 200
                        circle_size = bar_offset_y_1 - bar_offset_y
                        draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")
                        draw.ellipse(
                            (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#727175"
                        )
                        draw.ellipse(
                            (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#727175"
                        )
                        bar_length = bar_offset_x_1 - bar_offset_x
                        progress = (final_xp - xp) * 100 / final_xp
                        progress = 100 - progress
                        progress_bar_length = round(bar_length * progress / 100)
                        bar_offset_x_1 = bar_offset_x + progress_bar_length
                        draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#11ebf2")
                        draw.ellipse(
                            (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#11ebf2"
                        )
                        draw.ellipse(
                            (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#11ebf2"
                        )
                        text_size = draw.textsize(f"/ {final_xp} XP", font=small_font)
                        offset_x = 950 - text_size[0]
                        offset_y = bar_offset_y - text_size[1] - 10
                        draw.text((offset_x, offset_y), f"/ {final_xp:,} XP", font=small_font, fill="#727175")
                        text_size = draw.textsize(f"{xp:,}", font=small_font)
                        offset_x -= text_size[0] + 8
                        draw.text((offset_x, offset_y), f"{xp:,}", font=small_font, fill="#fff")
                        text_size = draw.textsize(user_name, font=medium_font)
                        offset_x = bar_offset_x
                        offset_y = bar_offset_y - text_size[1] - 5
                        draw.text((offset_x, offset_y), user_name, font=medium_font, fill="#fff")
                        offset_x += text_size[0] + 5
                        offset_y += 10
                        draw.text((offset_x, offset_y), discriminator, font=small_font, fill="#727175")
                        background.show()

                        background.save("./data/img/imgswap.png")
                        ffile = discord.File("./data/img/imgswap.png")
                        await context.reply(file=ffile, mention_author=False)

        else:
            await context.reply("You are not in the database :(\nDon't worry though, you were just added! Try running the command again.", mention_author=False)
    


def setup(client):
    client.add_cog(level(client))
