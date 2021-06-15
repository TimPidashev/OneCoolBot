import discord
from discord.ext import commands
from utils import log
from db import db
import asyncio
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

EXCLUDED_COMMANDS = ['help']
# db.connect("./data/database.db")
guild_ids = [791160100567384094]

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def on_ready(self):
        pass
        
    @commands.command(aliases=["hlp", "h"])
    async def help(self, context, arg=None):
        await log.cog_command(self, context)
        if arg is None:
            async with context.typing():
                await asyncio.sleep(1)

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
                
                message = await context.reply(embed=page_1, mention_author=False)
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
                            await context.message.delete()
                            break

                        else:
                            await message.remove_reaction(reaction, user)
                            
                    except asyncio.TimeoutError:
                        await message.delete()
                        await context.message.delete()
                        break
            
        elif arg is not None:
            if arg == "aliases" or arg == "alias" or arg == "als" or arg == "a":
                await log.cog_command(self, context)
                await context.reply("**help** aliases: `hlp` `h`", mention_author=False)

            else:
                return

        else:
            return

    @cog_ext.cog_slash(name="help", description="A descriptive help command.", guild_ids=guild_ids)
    async def help(self, context: SlashContext):
        await log.slash_command(self, context)
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

    @cog_ext.cog_slash(name="help-aliases", description="Shows command aliases.", guild_ids=guild_ids)
    async def help_aliases(self, context: SlashContext):
        await log.slash_command(self, context)
        await context.send("**help** aliases: `hlp` `h`")

def setup(client):
    client.add_cog(help(client))