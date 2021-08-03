"""
MIT License

Copyright (c) 2021 Timothy Pidashev
"""


import discord
import asyncio
import ez_db as db

db = db.AsyncDB(db_path="./data/database/database.db", build_path="./data/database/build.sql")

async def colour(context):
    colour = (await db.record(f"SELECT ColorTheme FROM usersettings WHERE UserID = {context.author.id}"))[0]
    return int(colour, base=16)

async def colour_hex(context, target):
    colour = (await db.record(f"SELECT ColorTheme FROM usersettings WHERE UserID = {target.id}"))[0]
    hexthingy = "#"
    color = (colour)[2:]
    return hexthingy + color
    
async def change_colour(context, value):
    await db.execute(f"UPDATE usersettings SET ColorTheme = ? WHERE UserID = {context.author.id}",
        value
    )
    await db.commit()
