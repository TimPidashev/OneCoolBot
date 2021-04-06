import discord
import psutil
import os
import time
import asyncio
import logging
import sqlite3
from glob import glob
from pyfiglet import Figlet
from db import db
from discord.utils import get
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from termcolor import colored, cprint
from dotenv import load_dotenv
from discord.ext import commands, tasks, ipc

load_dotenv()
Token = os.getenv("BOT_TOKEN")

class OneCoolBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key="my_secret_key")
    
    async def on_ready(self):
        print("Bot is ready.")

    async def on_ipc_ready(self):
        print("Ipc is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

client = OneCoolBot(command_prefix=".", intents=discord.Intents.all())

@client.ipc.route()
async def get_member_count(data):
    guild = my_bot.get_guild(
        data.guild_id
    )

    return guild.member_count


if __name__ == "__main__":
    client.ipc.start()

client.run(Token, reconnect=True)