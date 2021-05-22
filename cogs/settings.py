import discord
import asyncio
import os
from db import db
from discord.ext import commands
from utils import data, embed, log

class settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await log.online(self)

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["st", "s"])
    async def settings(self, context):
        await log.cog_command(self, context)
        await context.reply("Settings are currently under construction. 𝓣𝓲𝓶𝓶𝔂 thanks you for being patient.", mention_author=False)
        # message = context.message  
        # prefix = await data.get_prefix(context)

        # if message.content == f"{prefix}settings" or f"{prefix}st" or f"{prefix}s":
        #     await context.reply(embed=await embed.settings(context, prefix), mention_author=False)

        # else:
        #     await context.reply("**Error :(**\nThis is not a valid command. Use this handy command `{prefix}settings help` to help you out.", mention_author=False)

    # @settings.command(aliases=["hlp", "h"])
    # async def help(self, context):
    #     await log.cog_command(self, context)
    #     message = await context.reply(embed=await embed.settings_help_page_1(context), mention_author=False)

    #     await message.add_reaction("◀️")
    #     await message.add_reaction("▶️")
    #     await message.add_reaction("❌")
    #     pages = 2
    #     current_page = 1

    #     def check(reaction, user):
    #         return user == context.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]

    #     while True:
    #         try:
    #             reaction, user = await context.bot.wait_for("reaction_add", timeout=60, check=check)

    #             if str(reaction.emoji) == "▶️" and current_page != pages:
    #                 current_page += 1

    #                 if current_page == 2:
    #                     await message.edit(embed=await embed.settings_help_page_2(context))
    #                     await message.remove_reaction(reaction, user)
                
    #             if str(reaction.emoji) == "◀️" and current_page > 1:
    #                 current_page -= 1
                    
    #                 if current_page == 1:
    #                     await message.edit(embed=await embed.settings_help_page_1(context))
    #                     await message.remove_reaction(reaction, user)

    #             if str(reaction.emoji) == "❌":
    #                 await message.delete()
    #                 await context.message.delete()
    #                 break

    #             else:
    #                 await message.remove_reaction(reaction, user)
                    
    #         except asyncio.TimeoutError:
    #             await message.delete()
    #             await context.message.delete()
    #             break

    # @settings.command(aliases=["prfx", "p"])
    # async def prefix(self, context, arg=None):
    #     await log.cog_command(self, context)
    #     await context.reply("Settings are currently under construction. 𝓣𝓲𝓶𝓶𝔂 thanks you for being patient.")
        
        # if arg is not None and context.author == context.guild.owner or context.bot.is_owner:
        #     prefix = await data.update_prefix(context, arg)
        #     await context.reply(f"The prefix was changed to `{prefix}`", mention_author=False)
        
        # if arg == "None":
        #     prefix = await data.get_prefix(context)

        #     if context.author == context.guild.owner:
        #         await context.reply(f"The current prefix is `{prefix}`\nTo change the prefix, use this handy command: `{prefix}bot prefix <prefix>`", mention_author=False)

        #     else:
        #         await context.reply(f"The current prefix is `{prefix}`", mention_author=False)

    # @settings.command(aliases = ["lvls", "ls"])
    # async def levels(self, context, arg=None):
    #     await log.cog_command(self, context)
    #     levels = await data.fetch_level_settings(context)

    #     if arg == "on" and context.author == context.guild.owner:
    #         levels = "ON"
    #         db.execute(f"UPDATE guildconfig SET Levels = ? WHERE GuildID = {context.guild.id}",
    #             levels
    #         )
    #         db.commit()

    #         await context.reply("Levels were turned `on`", mention_author=False)

    #     if arg == "off" and context.author == context.guild.owner:
    #         levels = "OFF"
    #         db.execute(f"UPDATE guildconfig SET Levels = ? WHERE GuildID = {context.guild.id}",
    #             levels
    #         )
    #         db.commit()
        
    #         await context.reply("Levels were turned `off`", mention_author=False)

    #     if arg is None:
    #         levels = db.record(f"SELECT Levels from guildconfig WHERE GuildID = {context.guild.id}")[0]

    #         if levels == "OFF":
    #             await context.reply("Levels are currently `off`", mention_author=False)
                
    #         if levels == "ON":
    #             await context.reply("Levels are currently `on`", mention_author=False)

    # @settings.command(aliases=["lvlms", "lm"])
    # async def levelmessages(self, context, arg=None):
    #     await log.cog_command(self, context)
    #     levelmessage = db.record(f"SELECT LevelMessages FROM guildconfig WHERE GuildID = {context.guild.id}")[0]

    #     if arg == "on" and context.author == context.guild.owner:
    #         levelmessage = "ON"
    #         db.execute(f"UPDATE guildconfig SET LevelMessages = ? WHERE GuildID = {context.guild.id}",
    #             levelmessage
    #         )
    #         db.commit()

    #         message = db.record(f"SELECT LevelMessage FROM guildconfig WHERE GuildID = {context.guild.id}")[0]
    #         messagechannel = db.record(f"SELECT LevelMessageChannel FROM guildconfig WHERE GuildID = {context.guild.id}")[0]
    #         embed = discord.Embed(
    #             colour=0x9b59b6
    #        )
    #         embed.add_field(
    #             name="Current Settings",
    #             value="Level message turned on!",
    #             inline=False
    #         )
    #         embed.add_field(
    #             name="Current Level Message",
    #             value=f"{message}",
    #             inline=False
    #         )
    #         if messagechannel == 0:
    #             embed.add_field(
    #                 name="Current Level Message Channel",
    #                 value="None, level messages will be sent to the member in chat.",
    #                 inline=False
    #             )

    #         if messagechannel != 0:
            
    #             embed.add_field(
    #                 name="Current Level Message Channel",
    #                 value=f"{messagechannel}",
    #                 inline=False
    #             )

    #         await context.reply(embed=embed, mention_author=False)

    #     if arg == "off" and context.author == context.guild.owner:
    #         levelmessage = "OFF"
    #         db.execute(f"UPDATE guildconfig SET LevelMessages = ? WHERE GuildID = {context.guild.id}",
    #             levelmessage
    #         )
    #         db.commit()

    #         await context.reply("Level messages were turned `off`", mention_author=False)

    #     if arg is None:
    #         levelmessages = db.record(f"SELECT LevelMessages FROM guildconfig WHERE GuildID = {context.guild.id}")[0]

    #         if levelmessages == "OFF":
    #             await context.reply("Level messages are currently `off`", mention_author=False)

    #         if levelmessages == "ON":
    #             await context.reply("Level messages are currently `on`", mention_author=False)

    #         if levelmessages == "NONE":
    #             db.execute("INSERT INTO guildconfig (GuildID) VALUES (?)", context.guild.id)
    #             db.commit()

    #     if arg == "help":
    #         await context.reply("**Under Construction.**\nThe idea is that every command has its own small `help` description that will be supplied if the context is either not correct or close(determined by deep learning :eyes:) or the help command is specified.", mention_author=False)

def setup(client):
    client.add_cog(settings(client))