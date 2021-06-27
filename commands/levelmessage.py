import discord
from discord.ext import commands
import asyncio
from db import db
from utils import checks, log

class levelmessages(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass


    @commands.group(pass_context=True, invoke_without_command=True, aliases=["lvlmsgs", "lvlms", "lmsg", "lm"])
    async def levelmessage(self, context, arg=None):
        await log.cog_command(self, context)
        level_message_check = db.record(
            f"SELECT LevelMessageCheck FROM guildconfig WHERE GuildID = {context.guild.id}"
        )[0]
        
        level_message = db.record(
            f"SELECT LevelMessage FROM guildconfig WHERE GuildID = {context.guild.id}"
        )[0]

        level_message_channel = db.record(
            f"SELECT LevelMessageChannel FROM guildconfig WHERE GuildID = {context.guild.id}"
        )[0]

        embed = discord.Embed(colour=0x9b59b6)

        if level_message_check == "off":
            embed.add_field(
                name="Level Messages",
                value=f"Currently `{level_message_check}`",
                inline=True
            )
            embed.set_footer(
                text=f"Confused? Add `help` after command."
            )
            
        if level_message_check == "on":
            embed.add_field(
                name="Level Messages",
                value=f"Currently `{level_message_check}`",
                inline=True
            )
            embed.add_field(
                name="Level Message",
                value=f"`{level_message}`",
                inline=False
            )
            
            if level_message_channel == 0:
                embed.add_field(
                    name="Level Message Channel",
                    value="`None`",
                    inline=False
                )   

            if level_message_channel != 0:
                embed.add_field(
                    name="Level Message Channel",
                    value=f"#{level_message_channel}",
                    inline=False
                )   

        await context.reply(embed=embed, mention_author=False)

    @levelmessage.command(aliases=["hlp", "h"])
    async def help(self, context):
        embed = discord.Embed(colour=0x9b59b6)

        fields=[("***Command:***", "`levelmessage`", True),
                ("***Options:***", "`set` `help` `aliases`", True),
                ("`set`: ***Usage:*** see `lm set help`", "Set the levelmessage, turn levelmessages *on* or *off*, and *change* level message channel.", False),
                ("`aliases`:", "Shows command aliases.", False),
                ("`help`:", "Shows this message.", False)]

        embed.set_footer(text="Use this command to configure levelmessages")

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)    

        await context.reply(embed=embed, mention_author=False)

    @levelmessage.command(aliases=["als", "a"])
    async def aliases(self, context):
        await log.cog_command(self, context)
        embed = discord.Embed(colour=0x9b59b6)
        embed.add_field(
            name="***Command:*** `levelmessage`",
            value="***Aliases:*** `lvlmsg`, `lvlm`, `lmsg`, `lm`",
            inline=False
        )
        await context.reply(embed=embed, mention_author=False)

    @levelmessage.command(aliases=["st", "s"])
    async def set(self, context, arg1=None, arg2=None, arg3=None):
        await log.cog_command(self, context)

        if context.author != context.guild.owner:
            await context.reply(":| oops\nThis command is limited to server owners only.", mention_author=False)
            return

        if arg1 == "help" or arg1 == "hlp" or arg1 == "h":
            embed = discord.Embed(colour=0x9b59b6)
            
            fields = [("***Command:***", "`levelmessage set`", True),
                      ("***Options:***", "`levelmessage` `levelmessagechannel` `help`", True),
                      ("`levelmessage:` ***Options:***", "`on/off:` turn levelmessages on/off.\n`your level message:` type a new level message after command to change your servers level message.", False),
                      ("`levelmessagechannel:` ***Options:***", "`direct` *on/off*: send levelmessages in the same channel as the user.\n`#channel_name:` sets specified channel as the levelmessagechannel.", False),
                      ("`levelmessagecard:` ***Options:***", "`Coming soon!`\nLevel message cards are a unique way of rewarding a member for their chat activity!", False),
                      ("`help`:", "Shows this message.", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)  

            embed.set_footer(text="Input a prefix after command to change server prefix.")

            await context.reply(embed=embed, mention_author=False)
        
        if arg1 is None:
            await context.reply("**:| oops**\nMake sure to input your intended command options. See `lm set help`", mention_author=False)

        if arg1 is not None and arg1 != "help" or arg1 != "hlp" or arg1 != "h":
            if arg1 == "levelmessage" or arg1 == "lvlmsg" or arg1 == "lmsg" or arg1 == "lm":
                if arg2 is None:
                    await context.reply("**:| oops**\nMake sure to input your intended command options.", mention_author=False)

                elif arg2 == "on":
                    try:
                        db.execute(f"UPDATE guildconfig SET LevelMessageCheck = ? WHERE GuildID = {context.guild.id}", arg2)
                        db.commit()
                        await context.reply(f"**:) success**\nLevel Messages were turned `{arg2}`", mention_author=False)

                    except:
                        await context.reply("**:( error**\nAn internal error occured. How about giving that command another go?", mention_author=False)

                elif arg2 == "off":
                    try:
                        db.execute(f"UPDATE guildconfig SET LevelMessageCheck = ? WHERE GuildID = {context.guild.id}", arg2)
                        db.commit()
                        await context.reply(f"**:) success**\nLevel Messages were turned `{arg2}`", mention_author=False)

                    except:
                        await context.reply("**:( error**\nAn internal error occured. How about giving that command another go?", mention_author=False)

                else:
                    await context.reply("**:| oops**\nThis option does not exist, see `lm set help`", mention_author=False)







        

def setup(client):
    client.add_cog(levelmessages(client))