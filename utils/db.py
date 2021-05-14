from db import db
import asyncio
import sqlite3
from utils import embed
from db import db

async def prefix(context):
    prefix = db.record(f"SELECT Prefix FROM guilds WHERE GuildID = {context.guild.id}")
    return prefix