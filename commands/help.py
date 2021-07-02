import discord
from discord.ext import commands
from utils import log
from db import db
import asyncio
from dislash import *

guild_ids = [791160100567384094]

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def on_ready(self):
        pass
        
    @slash_commands.command(name="help", description="A descriptive help command.", guild_ids=guild_ids)
    async def help(self, context):
        #help
        prefix = db.record("SELECT Prefix FROM guilds WHERE GuildID = ?",
            context.guild.id,
        )[0]
        
        page_1 = discord.Embed(
            title="Index",
            description="The home page of the help command!", 
            colour=0x9b59b6
        )
        fields = [("`General`", "**The basic commands for day-to-day tasks.", False),
                ("`Economy`", "A global market and trading system, complete with its own currency!", False),
                ("`Games`", "Play with friends, compete with strangers, and make some extra coins while having fun!", False),
                ("`Music`", "Listen to low-latency music streams for studying and hanging with friends in voice-chat!", False),
                ("`Moderation`", "Make sure your server is always under control, with an advanced toolset for your moderators, and auto-moderation for the tech-savvy!", False),
                ("`Settings`", "Configure OneCoolBot with ease right in discord, with a dashboard coming later.", False)]

        page_1.set_footer(
            text="To scroll through pages, react to the arrows below."
        )

        for name, value, inline in fields:
            page_1.add_field(name=name, value=value, inline=inline)

        page_2 = discord.Embed(
            title="General", 
            description="The overview of the general commands.", 
            colour=0x9b59b6
        )
        fields = [("`help`", "Your looking at this command.\n**subcommands:** `aliases`", False),
                ("`info`", "Displays bot status, ping, and other miscellaneous content.\n**subcommands:** `aliases` `help`", False),
                ("`serverinfo`", "Displays server info, such as user count.\n**subcommands:** `aliases` `help`", False),
                ("`userinfo`", "Displays user info, discord stats, and the like.\n**subcommands:** `aliases` `help`", False)]

        page_2.set_footer(
            text=f"Handy tip! To see what a command can do, use the `help` subcommand."
        )

        for name, value, inline in fields:
            page_2.add_field(name=name, value=value, inline=inline)

        page_3 = discord.Embed(
            title="Economy", 
            description="A global market and trading system, complete with its own currency!", 
            colour=0x9b59b6
        )
        fields = [("Under Construction!", "Economy is currently being polished and completely refactored. Should be complete in a weeek or two.", False)]

        for name, value, inline in fields:
            page_3.add_field(name=name, value=value, inline=inline)

        page_4 = discord.Embed(
            title="Games", 
            description="Play with friends, compete with strangers, and make some extra coins all while having fun!", 
            colour=0x9b59b6
        )
        fields = [("Under Construction!", "Games are currently being polished and completely refactored. ETA not known yet, be patient!", False)]

        for name, value, inline in fields:
            page_4.add_field(name=name, value=value, inline=inline)

        page_5 = discord.Embed(
            title="Music",
            description="Listen to low-latency music streams for studying and hanging with friends in voice-chat!",
            colour=0x9b59b6
        )
        fields = [("Commands", "`connect` connect bot to voice chat\n`play` <search song to play>\n`pause` pause player\n`resume` resume player\n`skip` skip current song\n`stop`\n`volume` change volume\n`shuffle` shuffle queue\n`equalizer` change equalizer\n`queue` see songs queue\n`current` see currently played song\n`swap` swap song\n`music` see music status\n`spotify` see spotify rich presence", False)]
        
        for name, value, inline in fields:
            page_5.add_field(name=name, value=value, inline=inline)

        page_5.set_footer(
            text=f"Music is stable, but will be refactored to use new discord features and spotify integration, including playlists!"
        )

        page_6 = discord.Embed(
            title="Moderation", 
            description="Make sure your server is always under control, with an advanced toolset for your moderators, and auto-moderation for the tech-savvy!", 
            colour=0x9b59b6
        )
        fields = [(f"`{prefix}clear` <message_amount>", "Clear messages from a channel.", False),
                (f"`{prefix}kick` <@member> <reason>", "Kick mentioned member from server.", False),
                (f"`{prefix}ban` <@member> <reason>", "Ban mentioned member from server.", False),
                (f"`{prefix}unban` <@member> <reason>", "Unbans mentioned member from server.", False)]

        for name, value, inline in fields:
            page_6.add_field(name=name, value=value, inline=inline)

        page_6.set_footer(
            text="Is being refactored, as is most of the bot lol. Will be complete and shiny with ai moderation soon!"
        )
        
        message = await context.send(embed=page_1)
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("❌")
        pages = 6
        current_page = 1

        def check(reaction, user):
            return user == context.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]

        while True:
            try:
                reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" and current_page != pages:
                    current_page += 1

                    if current_page == 2:
                        await message.edit(embed=page_2)
                        await message.remove_reaction(reaction, user)
                    
                    elif current_page == 3:
                        await message.edit(embed=page_3)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 4:
                        await message.edit(embed=page_4)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 5:
                        await message.edit(embed=page_5)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 6:
                        await message.edit(embed=page_6)
                        await message.remove_reaction(reaction, user)
                
                if str(reaction.emoji) == "◀️" and current_page > 1:
                    current_page -= 1
                    
                    if current_page == 1:
                        await message.edit(embed=page_1)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 2:
                        await message.edit(embed=page_2)
                        await message.remove_reaction(reaction, user)
                    
                    elif current_page == 3:
                        await message.edit(embed=page_3)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 4:
                        await message.edit(embed=page_4)
                        await message.remove_reaction(reaction, user)

                    elif current_page == 5:
                        await message.edit(embed=page_5)
                        await message.remove_reaction(reaction, user)

                if str(reaction.emoji) == "❌":
                    await message.delete()
                    break

                else:
                    await message.remove_reaction(reaction, user)
                    
            except asyncio.TimeoutError:
                await message.delete()
                break

    @commands.command()
    async def test(self, context):
        message = await context.send(
            "This message has a select menu!",
            components=[
                SelectMenu(
                    custom_id="test",
                    placeholder="Choose up to 2 options",
                    max_values=2,
                    options=[
                        SelectOption("Option 1", "value 1"),
                        SelectOption("Option 2", "value 2"),
                        SelectOption("Option 3", "value 3")
                    ]
                )
            ]
        )
        # Wait for someone to click on it
        interaction = await message.wait_for_dropdown()
        # Send what you received
        labels = [option.label for option in interaction.select_menu.selected_options]
        await interaction.reply(f"Options: {', '.join(labels)}")

def setup(client):
    client.add_cog(help(client))