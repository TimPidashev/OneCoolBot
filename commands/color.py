import discord
from discord.ext import commands
from utils import checks, colours, log
from db import db
from dislash import *

guild_ids = [791160100567384094]

async def send_embed(colour, context, message, value):
    await colours.change_colour(colour, context, value)
    embed = discord.Embed(colour=await colours.colour(context))
    embed.add_field(
        name="Color Theme",
        value=f"Color theme changed to `{colour}`",
        inline=True
    )
    await message.delete()
    await context.reply(embed=embed)


class Color(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass

    @slash_commands.command(
        name="color", 
        description="Change my color theme!",
        guild_ids=guild_ids
    )
    async def color(self, context):
        message = await context.send(
            "Choose a color theme below!",
            components=[
                SelectMenu(
                    custom_id="Colors",
                    placeholder="Pick a color, any color!",
                    max_values=1,
                    options=[
                        #random values are because of placeholder errors, waiting on api updates
                        SelectOption("black", "A discord-themed shade of grey, yay!"),
                        SelectOption("teal", "put descr here when api updates"),
                        SelectOption("dark teal", " iu0o-8fas"),
                        SelectOption("green", "fdsadfa"),
                        SelectOption("dark green", "fasdlfy7usadoil"),
                        SelectOption("blue", "fsdalyfasiol"),
                        SelectOption("dark blue", "fsadklfyhsakjf"),
                        SelectOption("purple", "fsadkljfhas"),
                        SelectOption("dark purple", "sdfa98sad"),
                        SelectOption("magenta", "sadff4as67f"),
                        SelectOption("dark magenta", "asdff8s7ad"),
                        SelectOption("gold", "fasdo8ifi6sadf"), 
                        SelectOption("dark gold", "fasdoiuf6as"),
                        SelectOption("orange", "fasdoif67sa"),
                        SelectOption("dark orange", "fsdaiuof6tsa"),
                        SelectOption("red", "fsadoi7f6sa"),
                        SelectOption("dark red", "fsdaoif7uas"),
                        SelectOption("lighter grey", "fsad98f"),
                        SelectOption("dark grey", "sdfa98fs8"),
                        SelectOption("light grey", "asdffi67asd"),
                        SelectOption("darker grey", "dfuif6asdi"),
                        SelectOption("blurple", "jkhy2kj4"),
                        SelectOption("greyple", "put descrs here when api updates")
                    ]
                )
            ]
        )
        def check(inter):
            return inter.author == context.author and context.author == context.guild.owner

        inter = await message.wait_for_dropdown(check)
        labels = [option.label for option in inter.select_menu.selected_options]
        colour = f"{', '.join(labels)}"

        if colour == "black":
            value = "0"
            await send_embed(colour, context, message, value)

        elif colour == "teal":
            value = "0x1abc9c"
            await send_embed(colour, context, message, value)

        elif colour == "dark teal":
            value = "0x11806a"
            await send_embed(colour, context, message, value)

        elif colour == "green":
            value = "0x2ecc71"
            await send_embed(colour, context, message, value)

        elif colour == "dark green":
            value = "0x1f8b4c"
            await send_embed(colour, context, message, value)

        elif colour == "blue":
            value = "0x3498db"
            await send_embed(colour, context, message, value)

        elif colour == "dark blue":
            value = "0x206694"
            await send_embed(colour, context, message, value)

        elif colour == "purple":
            value = "0x9b59b6"
            await send_embed(colour, context, message, value)

        elif colour == "dark purple":
            value = "0x71368a"
            await send_embed(colour, context, message, value)
        
        elif colour == "magenta":
            value = "0xe91e63"
            await send_embed(colour, context, message, value)

        elif colour == "dark magenta":
            value = "0xad1457"
            await send_embed(colour, context, message, value)

        elif colour == "gold":
            value = "0xf1c40f"
            await send_embed(colour, context, message, value)

        elif colour == "dark gold":
            value = "0xc27c0e"
            await send_embed(colour, context, message, value)

        elif colour == "orange":
            value = "0xe67e22"
            await send_embed(colour, context, message, value)

        elif colour == "dark orange":
            value = "0xa84300"
            await send_embed(colour, context, message, value)

        elif colour == "red":
            value = "0xe74c3c"
            await send_embed(colour, context, message, value)

        elif colour == "dark red":
            value = "0x992d22"
            await send_embed(colour, context, message, value)

        elif colour == "lighter grey":
            value = "0x95a5a6"
            await send_embed(colour, context, message, value)

        elif colour == "dark grey":
            value = "0x607d8b"
            await send_embed(colour, context, message, value)

        elif colour == "light grey":
            value = "0x979c9f"
            await send_embed(colour, context, message, value)

        elif colour == "darker grey":
            value = "0x546e7a"
            await send_embed(colour, context, message, value)

        elif colour == "blurple":
            value = "0x7289da"
            await send_embed(colour, context, message, value)

        elif colour == "greyple":
            value = "0x99aab5"
            await send_embed(colour, context, message, value)

        else:
            return

def setup(client):
    client.add_cog(Color(client))