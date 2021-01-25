import discord
import requests
import json
import asyncio
from discord.ext import commands

class crypto(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.guild_only()
    @commands.command()
    async def crypto(self, context):
        headers = {
            'X-CMC_PRO_API_KEY' : '8f8259ec-f70f-4fca-aff8-f6638d6aa614',
            'Accepts' : 'applications/json'
        }

        params = {
            'start' : '1',
            'limit' : '5',
            'convert' : 'USD'
        }

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        json = requests.get(url, params=params, headers=headers).json()

        coins = json['data']

        for x in coins:
            A = (x['symbol'], x['quote']['USD']['price'])
            B = (x['symbol'], x['quote']['USD']['price'])
            C = (x['symbol'], x['quote']['USD']['price'])
            D = (x['symbol'], x['quote']['USD']['price'])
            E = (x['symbol'], x['quote']['USD']['price'])
            await context.send(A)

def setup(client):
    client.add_cog(crypto(client))
