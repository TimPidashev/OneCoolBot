import sqlite3 
import asyncio
from db import db
from utils import log
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

user_add_count = 0
guild_add_count = 0
guildconfig_add_count = 0

#establish_database_connection
def connect():
    db.connect("./data/database.db")

#get_prefix
async def get_prefix(context):
    prefix = db.record(f"SELECT Prefix FROM guilds WHERE GuildID = {context.guild.id}")[0]
    return prefix

async def update_prefix(context, arg):
    db.execute(f"UPDATE guilds SET Prefix = ? WHERE GuildID = {context.guild.id}", arg)
    db.commit()

    prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?", context.guild.id)[0]
    return prefix

#LEVEL STUFF BELOW
async def level_check(message):
    level_check = db.record(f"SELECT Levels FROM guildconfig WHERE GuildID = {message.guild.id}")[0]
    return level_check

async def find_record(message):
    result = db.record("SELECT GuildID, UserID FROM users WHERE (GuildID, UserId) = (?, ?)",
        message.guild.id,
        message.author.id
    )   
    return result

async def fetch_record(message):
    xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM users WHERE (GuildID, UserID) = (?, ?)", 
        message.guild.id, 
        message.author.id
    )
    return xp, lvl, xplock

async def update_record(self, message, xp_to_add, new_lvl, coins_on_xp):
    db.execute(f"UPDATE users SET XP = XP + ?, Level = ?, Coins = Coins + ?, XPLock = ? WHERE GuildID = {message.guild.id} AND UserID = {message.author.id}",
        xp_to_add,
        new_lvl,
        coins_on_xp,
        (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
    )
    db.commit()
    await log.exp_add(self, message, xp_to_add)
    await log.coin_add(self, message, coins_on_xp)

async def level_up_check(message):
    levelmessages, levelmessagechannel = db.record(f"SELECT LevelMessages, LevelMessageChannel FROM guildconfig WHERE GuildID = {message.guild.id}")
    return levelmessages, levelmessagechannel

async def on_message_send(self, message):
    db.execute("INSERT OR IGNORE INTO users (GuildID, UserID) VALUES (?, ?)",
        message.guild.id,
        message.author.id
    )
    db.commit()
    await log.member_redundant_add_db(self, message)

async def update_coins_if_levels_off(self, message, coins_on_xp):
    
    db.execute(f"UPDATE users SET Coins = Coins + ?, XPLock = ? WHERE GuildID = {message.guild.id} AND UserID = {message.author.id}",
        coins_on_xp,
        (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
    )
    db.commit()
    await log.coin_add(self, message, coins_on_xp)

async def fetch_levelmessage(message):
    levelmessage = db.record(f"SELECT LevelMessage FROM guildconfig WHERE GuildID = {message.guild.id}")[0]
    return levelmessage

async def update_users_table(self):
    db.multiexec(
        "INSERT OR IGNORE INTO users (GuildID, UserID) VALUES (?, ?)",
        (
            (member.guild.id, member.id,)
            for guild in self.guilds
            for member in guild.members
            if not member.bot
        ),
    )
    await log.update_users_table()

async def update_guilds_table(self):
    db.multiexec(
        "INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
        ((guild.id,) for guild in self.guilds),
    )
    db.commit()
    await log.update_guilds_table()

async def update_guildconfig_table(self):
    db.multiexec(
        "INSERT OR IGNORE INTO guildconfig (GuildID) VALUES (?)",
        ((guild.id,) for guild in self.guilds),
    )
    db.commit()
    await log.update_guildconfig_table()

#SETTINGS BELOW
async def fetch_level_settings(context):
    levels = db.record(f"SELECT Levels FROM guildconfig WHERE GuildID = {context.guild.id}")[0]
    return levels

#AI STUFF HERE
async def fetch_ailock(message):
    ailock = db.record("SELECT AILock FROM users WHERE UserID = (?)", message.author.id)[0]
    return ailock

async def update_ailock(message):
    db.execute(f"UPDATE users SET AILock = ? WHERE UserID = {message.author.id}", (datetime.utcnow() + timedelta(seconds=8)).isoformat())
    db.commit()


