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



