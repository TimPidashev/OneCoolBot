from . import db
import asyncio

async def build():
    await db.build()

asyncio.run(build())
