"""
MIT License

Copyright (c) 2021 Timothy Pidashev
"""


import discord
import asyncio
from discord.ext import commands
import ez_db as db

db = db.DB(db_path="./data/database/database.db", build_path="./data/database/build.sql")

owner_ids = db.record("SELECT OwnerIDS FROM botconfig")[0]

#checks if invoked command is run by owner
async def is_owner(context):
    return context.message.author.id in list(owner_ids)
