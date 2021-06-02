import discord
from discord.ext import commands
from discord.utils import get
from utils import data, log
import os
import time
import io
import matplotlib
import matplotlib.pyplot as plt 
import numpy as np 
import asyncio
from db import db

async def get_date():
        timestamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d'))
        return timestamp
        
async def get_dateList(startDate):
    i = 6
    dateList = []
    while i >= 0:
        loopDate = startDate - timedelta(days=i)
        loopDate = str(loopDate.strftime('%Y-%m-%d'))
        dateList.append(loopDate)
        i = i-1
    return dateList

class stats(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)
        db.connect("./data/database.db")

    @commands.Cog.listener()
    async def on_message(self, message):
        message_count = 1
        db.execute(f"UPDATE users SET GlobalMessageCount = GlobalMessageCount + ? WHERE GuildID = {message.guild.id} and UserID = {message.author.id}", message_count)
        db.commit()
        

    @commands.command(aliases=["msgcnt", "msgct"])
    async def messagecount(self, context):
        message_count = db.record(f"SELECT GlobalMessageCount FROM users WHERE UserID = {context.author.id} and GuildID = {context.guild.id}")[0]
        # x_array=[0, 1, 2, 3, 4, 5, 6]
        # message_count=[25, 48, 67, 98, 43, 150, 98]
        # plt.figure(figsize=(7,1))
        # plt.plot(x_array, message_count)
        # plt.ylabel("Activity")
        # plt.xlabel("Date")
        # plt.title(f"{context.author.name}'s activity for the past 7 days")
        # filename =  "./data/img/graph.png"
        # plt.savefig(filename)
        # graph = discord.File(filename)
        # await context.reply(file=graph, mention_author=False)
        await context.reply(f"You have sent **{message_count}** messages globally.", mention_author=False)
    

    
        

def setup(client):
    client.add_cog(stats(client))