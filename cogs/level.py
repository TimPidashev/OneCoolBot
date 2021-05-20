import discord
import time
import sqlite3
import asyncio
import random
import os
import aiohttp
import io
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
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
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
            level_check = await data.level_check(message)
            if context.command:
                return

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
    async def rank(self, context, target: Optional[Member]):
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

def setup(client):
    client.add_cog(level(client))
