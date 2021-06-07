import discord
from discord.ext import commands
from utils import data, embed, log

class serverinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["srvrinf", "si"])
    async def serverinfo(self, context):
        await log.cog_command(self, context)
        await context.reply(embed=await embed.serverinfo(context), mention_author=False)

    @serverinfo.command(aliases=["alias", "als", "a"])
    async def aliases(self, context):
        await log.cog_command(self, context)
        await context.reply("**serverinfo** aliases: `srvrinf` `si`", mention_author=False)

    @serverinfo.command(aliases=["hlp", "h"])
    async def help(self, context):
        await log.cog_command(self, context)
        await context.reply("Shows server info.")

def setup(client):
    client.add_cog(serverinfo(client))