import asyncio
import asyncpg

#define database creds
credentials = {"user": "timmy", "password": "changethispassword", "database": "onecoolbot", "host": "127.0.0.1"}

async def run():
    connection = await asyncpg.connect(**credentials)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

