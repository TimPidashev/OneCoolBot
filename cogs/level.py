import discord
import time
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
from discord.ext import commands
from utils import levels, log
from db import db
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)

    #LEVELLING SYSTEM
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            context = await self.client.get_context(message)
            
            if context.command:
                return

            result = db.record("SELECT GuildID, UserID FROM users WHERE (GuildID, UserId) = (?, ?)",
                message.guild.id,
                message.author.id
            )
            if result is not None:
                xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM users WHERE (GuildID, UserID) = (?, ?)", 
                    message.guild.id, 
                    message.author.id
                )
                
                if datetime.utcnow() > datetime.fromisoformat(xplock):

                    xp_to_add = random.randint(10, 20)
                    new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)
                    coins_on_xp = random.randint(1, 10)

                    db.execute(f"UPDATE users SET XP = XP + ?, Level = ?, Coins = Coins + ?, XPLock = ? WHERE GuildID = {message.guild.id} AND UserID = {message.author.id}",
                        xp_to_add,
                        new_lvl,
                        coins_on_xp,
                        (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
                    )

                    db.commit()
                    await log.exp_add(self, message, xp_to_add)
                    await log.coin_add(self, message, coins_on_xp)

                    if new_lvl > lvl:
                        await levels.level_up(self, message, new_lvl)
    
                else:
                    pass

            else:
                try:
                
                    db.execute("INSERT OR IGNORE INTO users (GuildID, UserID) VALUES (?, ?)",
                        message.guild.id,
                        message.author.id
                    )
                    db.commit()
                    await log.member_redundant_add_db(self, message)

                except:
                    pass #so dms are not flagged as errors
                
def setup(client):
    client.add_cog(level(client))