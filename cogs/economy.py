import discord
from discord.ext import commands
from db import db
from utils import checks, colours, log
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, create_choice
from discord.ext.menus import MenuPages, ListPageSource
from discord import Member, Embed

guild_ids = [791160100567384094]

# class Market(ListPageSource):
#     def __init__(self, context, data):
#         self.context = context

#         super().__init__(data, per_page=10)

#     async def write_page(self, menu, offset, fields=[]):
#         offset = (menu.current_page * self.per_page) + 1
#         len_data = len(self.entries)

#         embed = Embed(
#             title="Market",
#             colour=await colours.colour(self.context),
#         )

#         # embed.set_thumbnail(url=self.context.guild.icon_url)
#         embed.set_footer(
#             text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} items"
#         )

#         for name, value in fields:
#             embed.add_field(name=name, value=value, inline=False)

#         return embed

#     async def format_page(self, menu, entries):
#         offset = (menu.current_page * self.per_page) + 1
#         fields = []
#         table = "\n".join(
#             f"{idx+offset}. **Item:** ~ `{entry[1]}`"
#             for idx, entry in enumerate(entries)
#         )

#         fields.append(("Items for sale:", table))

#         return await self.write_page(menu, offset, fields)

class Market(ListPageSource):
    def __init__(self, context, data):
        self.context = context

        super().__init__(data, per_page=10)

    async def write_page(self, menu, offset, fields=[]):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)
        embed = Embed(
            title="Market",
            colour=await colours.colour(self.context),
        )
        # embed.set_thumbnail(url=self.context.guild.icon_url)
        embed.set_footer(
            text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} items"
        )
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        return embed

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        fields = []
        table = "\n".join(
            f"{idx+offset}. **Item:** ~ `{entries[0]}`"
            for idx, entry in enumerate(entries)
        )
        fields.append(("Items for sale:", table))
        return await self.write_page(menu, offset, fields)



class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)


    @commands.command(aliases=["mrk", "m"])
    async def market(self, context):
        await log.cog_command(self, context)
        records = db.records("SELECT ItemName, Category, DateReleased, QuantityAvailable, QuantityLimit, Price, Popularity, WhoBoughtLast FROM globalmarket ORDER BY Popularity DESC")
        records = [record for record in records]
        records.insert(0, ("Item", "Category", "Date Released", "Quantity Available", "Quantity Limit", "Price", "Popularity", "Who Bought Last"))

        menu = MenuPages(
            source=Market(context, records),
            clear_reactions_after=True, 
            timeout=100
        )

        await menu.start(context)



def setup(client):
    client.add_cog(economy(client))