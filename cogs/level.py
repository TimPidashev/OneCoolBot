import discord
from discord.ext import commands
import aiosqlite
import asyncio

START_BAL = 100
db = aiosqlite.connect("main.sqlite")

class level(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        await db
        cursor = await db.cursor()
        await cursor.exexute("""CREATE TABLE IF NOT EXISTS main(
        num INTEGER NOT NULL PRIMARY KEY

        user_name TEXT
        balance INTEGER
        user_id INTEGER NOT NULL
        )""")
        await db.commit()
        print("DB ready!")

    @commands.command()
    async def balance(self, context):
        cursor = await db.commit()
        USER_ID = context.message.author.id
        USER_NAME = str(context.message.author)

        await cursor.execute(f"SELECT user_id FROM main WHERE user_id={USER_ID}")
        result_userID = await cursor.fetchone()

        if result_userID == None:
            await cursor.execute("INSERT INTO main(user_name, balance, user_id)values(?,?,?)",(USER_NAME,START_BAL,USER_ID))
            await db.commit()

            await context.send("**New DB User!**\nPlease execute the command again!")

        else:
            await cursor.execute(f"SELECT balance FROM main WHERE user_id={USER_ID}")
            result_userBal = await cursor.fetchone()
            await context.send(f"{USER_NAME}'s Balance!\n\nMoney:\n${result_userBal[0]}")

    @commands.command()
    async def beg(self, context):
        ID = context.message.author.id
        USER_NAME = str(context.message.author)

        await cursor.execute(f"SELECT user_id FROM main WHERE user_id={USER_ID}")
        result_userID = await cursor.fetchone()

        if result_userID == None:
            await cursor.execute("INSERT INTO main(user_name, balance, user_id)values(?,?,?)",(USER_NAME,START_BAL,USER_ID))
            await db.commit()

            await context.send("**New DB User!**\nPlease execute the command again!")

        else:
            addup = random.randint(100,500)
            await cursor.execute("UPDATE main SET balance = balance + ? WHERE user_id=?"(addup,USER_ID))
            await db.commit()

            await context.send(f"**BEG**\n\nYou have gotten `${addup}` from begging!")
def setup(client):
    client.add_cog(level(client))
