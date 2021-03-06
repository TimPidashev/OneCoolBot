"""
MIT License

Copyright (c) 2021 Timothy Pidashev
"""


import discord
import asyncio
from discord.ext import commands
from . import db

#owner_ids
owner_id_str = db.record("SELECT OwnerIDS FROM botconfig")[0]
owner_ids = map(int, owner_id_str.split(","))

#checks if invoked command is run by owner
async def is_owner(context):
    return context.message.author.id in map(int, owner_id_str.split(","))

#add initial support for command-toggles
async def is_on(context):
    pass
