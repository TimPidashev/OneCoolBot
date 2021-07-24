"""
MIT License

Copyright (c) 2021 Timothy Pidashev

Exempt lines 183-203(taken from the DiscordLevellingSystem to reduce dependencies)
"""


import discord
from discord.ext import commands
from collections import namedtuple
from db import db
from . import log
import asyncio
import json
import random

with open("config.json") as file:
    config = json.load(file)
    devthings = config["devthings"]

LEVELS_AND_XP = {
    "0": 0,
    "1": 100,
    "2": 255,
    "3": 475,
    "4": 770,
    "5": 1150,
    "6": 1625,
    "7": 2205,
    "8": 2900,
    "9": 3720,
    "10": 4675,
    "11": 5775,
    "12": 7030,
    "13": 8450,
    "14": 10045,
    "15": 11825,
    "16": 13800,
    "17": 15980,
    "18": 18375,
    "19": 20995,
    "20": 23850,
    "21": 26950,
    "22": 30305,
    "23": 33925,
    "24": 37820,
    "25": 42000,
    "26": 46475,
    "27": 51255,
    "28": 56350,
    "29": 61770,
    "30": 67525,
    "31": 73625,
    "32": 80080,
    "33": 86900,
    "34": 94095,
    "35": 101675,
    "36": 109650,
    "37": 118030,
    "38": 126825,
    "39": 136045,
    "40": 145700,
    "41": 155800,
    "42": 166355,
    "43": 177375,
    "44": 188870,
    "45": 200850,
    "46": 213325,
    "47": 226305,
    "48": 239800,
    "49": 253820,
    "50": 268375,
    "51": 283475,
    "52": 299130,
    "53": 315350,
    "54": 332145,
    "55": 349525,
    "56": 367500,
    "57": 386080,
    "58": 405275,
    "59": 425095,
    "60": 445550,
    "61": 466650,
    "62": 488405,
    "63": 510825,
    "64": 533920,
    "65": 557700,
    "66": 582175,
    "67": 607355,
    "68": 633250,
    "69": 659870,
    "70": 687225,
    "71": 715325,
    "72": 744180,
    "73": 773800,
    "74": 804195,
    "75": 835375,
    "76": 867350,
    "77": 900130,
    "78": 933725,
    "79": 968145,
    "80": 1003400,
    "81": 1039500,
    "82": 1076455,
    "83": 1114275,
    "84": 1152970,
    "85": 1192550,
    "86": 1233025,
    "87": 1274405,
    "88": 1316700,
    "89": 1359920,
    "90": 1404075,
    "91": 1449175,
    "92": 1495230,
    "93": 1542250,
    "94": 1590245, 
    "95": 1639225,
    "96": 1689200,
    "97": 1740180,
    "98": 1792175,
    "99": 1845195,
    "100": 1899250
}

MAX_XP = LEVELS_AND_XP["100"]
MAX_LEVEL = 100

async def level_up_process(self, message, new_lvl):
    role, coins = (await db.record(f"SELECT LevelRoleID, LevelCoins FROM guildsettings WHERE GuildID = ? AND RoleLevel = ?",
        message.guild.id,
        new_lvl
    ))
    role_id = message.guild.get_role(role)
    await message.author.add_roles(role_id)
    await log.add_role(self, message, role_id)

    await db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
        coins,
        message.author.id
    )
    await db.commit()
    await log.coin_add(self, message, coins)

async def level_up(self, message, new_lvl):
    async with message.channel.typing():
        await log.level_up(self, message, new_lvl)

        if message.guild.id in config["devthings"]:
            if new_lvl == 5:
                await level_up_process(self, message, new_lvl)

            if new_lvl == 10:
                await level_up_process(self, message, new_lvl)

            if new_lvl == 20:
                await level_up_process(self, message, new_lvl)

            if new_lvl == 30:
                await level_up_process(self, message, new_lvl)

            if new_lvl == 40:
                await level_up_process(self, message, new_lvl)

            if new_lvl == 50:
                await level_up_process(self, message, new_lvl)

            if new_lvl == 75:
                await level_up_process(self, message, new_lvl)
                #make sure this is one user with most exp!

        else:
            coins = random.randint(10, 1000)

            await db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                coins,
                message.author.id
            )
            await db.commit()

async def next_level_details(current_level: int) -> tuple:
    temp = current_level + 1
    if temp > 100:
        temp = 100
    key = str(temp)
    value = LEVELS_AND_XP[key]
    Details = namedtuple("Details", ["level", "xp_needed"])
    return Details(level=int(key), xp_needed=value)

async def find_level(current_total_xp: int) -> int:
    if current_total_xp in LEVELS_AND_XP.values():
        for level, xp_needed in LEVELS_AND_XP.items():
            if current_total_xp == xp_needed:
                return int(level)
    else:
        for level, xp_needed in LEVELS_AND_XP.items():
            if 0 <= current_total_xp <= xp_needed:
                level = int(level)
                level -= 1
                if level < 0: level = 0
                return level