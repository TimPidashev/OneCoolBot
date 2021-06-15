import asyncpg
import asyncio
from . import db
import os

credentials = {"user": "timmy", "password": "changethispassword", "database": "onecoolbot", "host": "127.0.0.1"}

async def connect(**credentials):
	try:
		connection = await asyncpg.connect(**credentials)
	
	except:
		#create database if not exists
		system = await asyncpg.connect(database="template1", user="postgres")
		await system.execute(f"CREATE DATABASE {database} OWNER {user}")
		await system.close()
        #connect to newly created database
		connection = await asyncpg.connect(**credentials)

	return connection

async def build(sql_file):
    db = await asyncpg.connect(**credentials)
    with open(sql_file, "r") as sql:
        data = sql.read()
    await db.execute(data)
    await db.close()

asyncio.get_event_loop().run_until_complete(
	connect(**credentials)
)
asyncio.get_event_loop().run_until_complete(
	build(sql_file="./db/build.sql")
)
