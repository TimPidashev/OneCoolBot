"""
MIT License

Copyright (c) 2021 Timothy Pidashev
"""


import discord
import asyncio
from discord.ext import commands
import ez_db as db

db = db.DB(db_path="./data/database/database.db", build_path="./data/database/build.sql")

owner_id_str = db.record("SELECT OwnerIDS FROM botconfig")[0]

owner_ids = map(int, owner_id_str.split(","))

#checks if invoked command is run by owner
async def is_owner(context):
    return context.message.author.id in owner_ids
