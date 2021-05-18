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
from utils import data

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
                return

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
                            levelmessages, levelmessage, levelmessagechannel = await data.level_up_check(message)
                            
                            if levelmessages == "OFF":
                                return
                            
                            if levelmessages == "ON":
                                if levelmessagechannel == "0":
                                    await message.reply(f"{levelmessage}", mention_author=False)
                                    await log.level_up(self, message, new_lvl)

                                else:
                                    messagechannel = self.client.get_channel(levelmessagechannel)
                                    await message.channel.send(f"{levelmessage}")

                    else:
                        return

                else:
                    await data.on_message_send(self, message)
                
def setup(client):
    client.add_cog(level(client))
