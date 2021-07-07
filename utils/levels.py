import discord
from discord.ext import commands
from db import db
from . import log
import asyncio
import json

with open("config.json") as file:
    config = json.load(file)
    devthings = config["devthings"]

async def level_up_process(self, message, new_lvl):
    role, coins = db.record(f"SELECT LevelRoleID, LevelCoins FROM guildsettings WHERE GuildID = ? AND RoleLevel = ?",
        message.guild.id,
        new_lvl
    )
    role_id = message.guild.get_role(role)
    await message.author.add_roles(role_id)
    await log.add_role(self, message, role_id)

    db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
        coins,
        message.author.id
    )
    db.commit()
    await log.coin_add(self, message, coins)

async def level_up(self, message, new_lvl):
    await message.reply(f":partying_face: {message.author.mention} is now level **{new_lvl:,}**!", mention_author=False)
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

        db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
            coins_to_add,
            message.author.id
        )
        db.commit()