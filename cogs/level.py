import discord
from discord.ext import commands
import time
import random
import io
from datetime import datetime, timedelta
from db import db
from utils import log

class level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            context = await self.client.get_context(message)
            if context.command:
                return

            check_if_levelling_on = db.record(f"SELECT Levels FROM guildconfig WHERE GuildID = {message.guild.id}")[0]
        
            if check_if_levelling_on == "OFF":
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
                        coins_on_xp = random.randint(1, 10)
                        db.execute(f"UPDATE users SET Coins = Coins + ?, XPLock = ? WHERE GuildID = {message.guild.id} AND UserID = {message.author.id}",
                            coins_on_xp,
                            (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
                        )
                        db.commit()
                        await log.coin_add(self, message, coins_on_xp)
                        return

                else:
                    db.execute("INSERT OR IGNORE INTO users (GuildID, UserID) VALUES (?, ?)",
                        message.guild.id,
                        message.author.id
                    )
                    db.commit()
                    await log.member_redundant_add_db(self, message)

            else:
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

                        if new_lvl > lvl:
                            levelmessages, levelmessagechannel = db.record(f"SELECT LevelMessages, LevelMessageChannel FROM guildconfig WHERE GuildID = {message.guild.id}")
                            levelmessage = db.record(f"SELECT LevelMessage FROM guildconfig WHERE GuildID = {message.guild.id}")[0]

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
                    db.execute("INSERT OR IGNORE INTO users (GuildID, UserID) VALUES (?, ?)",
                        message.guild.id,
                        message.author.id
                    )
                    db.commit()
                    await log.member_redundant_add_db(self, message)



def setup(client):
    client.add_cog(level(client))
