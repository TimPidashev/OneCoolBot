"""
MIT License

Copyright (c) 2021 Timothy Pidashev
"""


import discord
import asyncio
import json
from discord.ext import commands
from db import db

#loading bot config
with open("config.json") as file:
    config = json.load(file)

#checks if invoked command is run by owner
async def is_owner(context):
    return context.message.author.id in config["owner_ids"]