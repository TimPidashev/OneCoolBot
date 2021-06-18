from . import db
import asyncio

async def run():
    await db.build()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
