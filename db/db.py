from os.path import isfile
import aiosqlite
from utils import log
import asyncio

DB_PATH = "./data/database.db"
BUILD_PATH = "./db/build.sql"

async def build():
    async with aiosqlite.connect(DB_PATH) as db:
        if isfile(BUILD_PATH):
            await scriptexec(BUILD_PATH)

async def commit():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.commit()

async def record(command, *values):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(command, tuple(values)) as cursor:
            return await cursor.fetchone()

async def field(command, *values):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(command, tuple(values)) as cursor:
            if (fetch := cursor.fetchone()) is not None:
                return fetch[0]

async def records(command, *values):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(command, tuple(values)) as cursor:
            return await cursor.fetchall()

async def column(command, *values):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(command, tuple(values)) as cursor:
            return [item[0] for item in await cursor.fetchall()]

async def execute(command, *values):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(command, tuple(values))

async def multiexec(command, valueset):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executemany(command, valueset)

async def scriptexec(path):
    async with aiosqlite.connect(DB_PATH) as db:
        with open(path, "r", encoding="utf-8") as script:
            await db.executescript(script.read())