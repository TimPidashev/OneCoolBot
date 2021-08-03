"""
MIT License

Copyright (c) 2021 Timothy Pidashev
"""


import discord
import asyncio
import random
from discord import Member, Embed
from discord.ext.commands import Cog
from typing import Optional
from datetime import datetime, timedelta
from discord.ext import commands
from utils import levels, log
import ez_db as db

db = db.AsyncDB(db_path="./data/database/database.db", build_path="./data/database/build.sql")

class Level(commands.Cog):
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

            result = (await db.record("SELECT GuildID, UserID FROM users WHERE (GuildID, UserId) = (?, ?)",
                message.guild.id,
                message.author.id
            ))
            if result is not None:
                xp, lvl, xplock = (await db.record("SELECT XP, Level, XPLock FROM users WHERE (GuildID, UserID) = (?, ?)", 
                    message.guild.id, 
                    message.author.id
                ))
                
                if datetime.utcnow() > datetime.fromisoformat(xplock):
                    xp_to_add = random.randint(10, 20)
                    new_lvl, xp_needed = await levels.next_level_details(lvl)
                    current_level = await levels.find_level(xp + xp_to_add)
                    coins_on_xp = random.randint(1, 10)
                    
                    await db.execute(f"UPDATE users SET XP = XP + ?, Level = ?, Coins = Coins + ?, XPLock = ? WHERE GuildID = {message.guild.id} AND UserID = {message.author.id}",
                        xp_to_add,
                        current_level,
                        coins_on_xp,
                        (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
                    )

                    await db.commit()
                    await log.exp_add(self, message, xp_to_add)
                    await log.coin_add(self, message, coins_on_xp)

                    if current_level > lvl:
                        await levels.level_up(self, message, current_level)
    
                else:
                    pass

            else:
                try:
                
                    await db.execute("INSERT OR IGNORE INTO users (GuildID, UserID) VALUES (?, ?)",
                        message.guild.id,
                        message.author.id
                    )
                    await db.commit()
                    await log.member_redundant_add_db(self, message)

                except:
                    pass #so dms are not flagged as errors
                
def setup(client):
    client.add_cog(Level(client))