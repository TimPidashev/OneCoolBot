import discord
from discord.ext import commands
from utils import data, embed, log

class userinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["usrinf", "ui"])
    async def userinfo(self, context, user: discord.Member = None):
        await log.cog_command(self, context)
        await context.reply(embed=await embed.userinfo(context, user), mention_author=False)

    @userinfo.command(aliases=["alias", "als", "a"])
    async def aliases(self, context):
        await log.cog_command(self, context)
        await context.reply("**userinfo** aliases: `usrinf` `ui`", mention_author=False)

    @userinfo.command(aliases=["hlp", "h"])
    async def help(self, context):
        await log.cog_command(self, context)
        await context.reply("Shows user info.", mention_author=False)
    
def setup(client):
    client.add_cog(userinfo(client))