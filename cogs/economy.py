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

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)


    @cog_ext.cog_slash(
        name="market",
        description="A global market and trading system, complete with its own currency!",
        guild_ids=guild_ids
    )
    async def market(self, context):
        await log.cog_command(self, context)
        records = (await db.records("SELECT ItemName, Category, DateReleased, QuantityAvailable, QuantityLimit, Price, Popularity, WhoBoughtLast FROM globalmarket ORDER BY Popularity DESC"))
        records = [record for record in records]
        records.insert(0, ("Item", "Category", "Date Released", "Quantity Available", "Quantity Limit", "Price", "Popularity", "Who Bought Last"))

        menu = MenuPages(
            source=Market(context, records),
            clear_reactions_after=True, 
            timeout=100
        )

        await menu.start(context)
        return

    @cog_ext.cog_slash(
        name="wallet",
        description="Manage your funds, i guess",
        guild_ids=guild_ids
    )
    async def wallet(self, context: SlashContext, user: discord.Member=None):
        await log.slash_command(self, context)

        user = user or context.author
        balance = (await db.record("SELECT Coins FROM users WHERE UserID = ?", user.id))[0]
        embed = discord.Embed(colour=await colours.colour(context))
        embed.set_author(name=f"{user.name}", icon_url=user.avatar_url)
        embed.add_field(
            name="Balance:",
            value=f":coin: {balance}",
            inline=True
        )

        await context.send(embed=embed)

    @cog_ext.cog_slash(
        name="market-cap",
        description="See how many :coin: are widespread globally!",
        guild_ids=guild_ids
    )
    async def market_cap(self, context: SlashContext):
        cap = (await db.record("SELECT sum(Coins) FROM users"))[0]
        embed = discord.Embed(colour=await colours.colour(context))
        embed.add_field(name=f"**Current Market Cap:**", value=f"There are currently :coin: **{cap}** coins widespread globally")
        await context.send(embed=embed)

def setup(client):
    client.add_cog(Economy(client))