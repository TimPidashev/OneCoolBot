import discord
import asyncio
from discord.ext import commands
from utils import checks, colours, log
from db import db

#lazy functions instead of class functions for cleaner code 
async def fetch_prefix(self, context, arg):
    prefix = db.record(f"SELECT Prefix FROM guilds WHERE GuildID = {context.guild.id}")[0]
    return prefix

async def update_prefix(self, context, arg):
     db.execute(f"UPDATE guilds SET Prefix = ? WHERE GuildID = {context.guild.id}", arg)
     db.commit()

async def update_prefix_embed(self, context, arg):
    embed = discord.Embed(colour=await colours.colour(context))
    embed.add_field(
        name="**:) success**",
        value=f"Prefix was changed to `{arg}`",
        inline=True
    )
    await context.reply(embed=embed, mention_author=False)

async def not_server_owner(self, context):
    embed = discord.Embed(colour=await colours.colour(context))
    embed.add_field(
        name="**:| oops**",
        value=f"This command is only available to `server owners`, sorry!",
        inline=True
    )
    await context.reply(embed=embed, mention_author=False)  

async def command_error(self, context, error):
    embed = discord.Embed(colour=await colours.colour(context))
    embed.add_field(
        name="**:( error**",
        value=f"An internal error occured, how about giving that command another go?",
        inline=True
    )
    await context.reply(embed=embed, mention_author=False)  

async def help(self, context):
    embed = discord.Embed(colour=await colours.colour(context))

    fields=[("***Command***", "`prefix`", True),
            ("***Options***", "`change` `help`", True),
            ("***Aliases***", "`prfx` `prf` `pr` `p`", True),
            ("`change`", "To change prefix, just type a new prefix after `prefix`", False)]

    embed.set_footer(text="Use this command to change my prefix!")

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)    

    await context.reply(embed=embed, mention_author=False)

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["prfx", "prf", "pr", "p"])
    @commands.is_owner()
    async def prefix(self, context, arg=None):
        await log.cog_command(self, context)
        if arg is not None and context.author == context.guild.owner:
            try:
                await update_prefix(self, context, arg)
                await update_prefix_embed(self, context, arg)

            except Exception as error:
                await command_error(self, context, error)

        elif arg is not None and context.author != context.guild.owner:
            await not_server_owner(self, context)

        elif arg is None:        
            await log.cog_command(self, context)
            prefix = await fetch_prefix(self, context, arg)
            await context.reply(f"The current prefix is `{prefix}`", mention_author=False)

    @prefix.command(aliases=["hlp", "h"])
    async def help(self, context):
        await log.cog_command(self, context)
        await help(self, context)

def setup(client):
    client.add_cog(Prefix(client))