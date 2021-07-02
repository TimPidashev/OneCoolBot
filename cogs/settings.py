import discord
from discord.ext import commands
from db import db 
from utils import checks, colours, log
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option, create_choice

guild_ids = [791160100567384094, 788629323044093973]

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass
    
    @cog_ext.cog_slash(
        name="settings", 
        description="configure me to your liking", 
        guild_ids=guild_ids,
        options=[
            create_option(
                name="colortheme",
                description="Change my color theme!",
                required=False,
                option_type=3,
                choices=[
                    create_choice(
                        name="black",
                        value="black,0"
                    ),
                    create_choice(
                        name="teal",
                        value="teal,0x1abc9c"
                    ),
                    create_choice(
                        name="dark teal",
                        value="dark teal,0x11806a"
                    ),
                    create_choice(
                        name="green",
                        value="green,0x2ecc71"
                    ),
                    create_choice(
                        name="dark green",
                        value="dark green,0x1f8b4c"
                    ),
                    create_choice(
                        name="blue",
                        value="blue,0x3498db"
                    ),
                    create_choice(
                        name="dark blue",
                        value="dark blue,0x206694"
                    ),
                    create_choice(
                        name="purple",
                        value="purple,0x9b59b6"
                    ),
                    create_choice(
                        name="dark purple",
                        value="dark purple,0x71368a"
                    ),
                    create_choice(
                        name="magenta",
                        value="magenta,0xe91e63"
                    ),
                    create_choice(
                        name="dark magenta",
                        value="dark magenta,0xad1457"
                    ),
                    create_choice(
                        name="gold",
                        value="gold,0xf1c40f"
                    ),
                    create_choice(
                        name="dark gold",
                        value="dark gold,0xc27c0e"
                    ),
                    create_choice(
                        name="orange",
                        value="orange,0xe67e22"
                    ),
                    create_choice(
                        name="dark orange",
                        value="dark orange,0xa84300"
                    ),
                    create_choice(
                        name="red",
                        value="red,0xe74c3c"
                    ),
                    create_choice(
                        name="dark red",
                        value="dark red,0x992d22"
                    ),
                    create_choice(
                        name="lighter grey",
                        value="lighter grey,0x95a5a6s"
                    ),
                    create_choice(
                        name="light grey",
                        value="light grey,0x979c9f"
                    ),
                    create_choice(
                        name="dark grey",
                        value="dark grey,0x607d8b"
                    ),
                    create_choice(
                        name="darker grey",
                        value="darker grey,0x546e7a"
                    ),
                    create_choice(
                        name="greyple",
                        value="greyple,0x99aab5"
                    ),
                    create_choice(
                        name="blurple",
                        value="blurple,0x7289da"
                    )

                ]
    
            )
        ],
        connector={
            "colortheme": "colortheme",
        }
    )

    async def settings(self, context: SlashContext, colortheme: str):
        await log.slash_command(self, context)
        if colortheme:
            #add rainbow and custom colorthemes as purchases in economy later!
            color, value = colortheme.split(",")
            await colours.change_colour(context, value)
            embed = discord.Embed(colour=await colours.colour(context))
            embed.add_field(
                name="Color Theme",
                value=f"Color theme changed to `{color}`",
                inline=True
            )
            await context.send(embed=embed)
        
        else:
            return

def setup(client):
    client.add_cog(Settings(client))