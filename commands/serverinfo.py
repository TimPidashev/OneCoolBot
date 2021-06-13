import discord
from discord.ext import commands
from utils import log

class serverinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["srvrinf", "si"])
    async def serverinfo(self, context):
        await log.cog_command(self, context)

        embed = discord.Embed(
        title="Server Info",
        colour=0x9b59b6
        )
        embed.set_thumbnail(
            url=context.guild.icon_url
        )

        fields = [("Owner", context.guild.owner, False),
                  ("Created At", context.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Region", context.guild.region, False),
                  ("Members", len(context.guild.members), False)]

        for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(
            text=f"ID: {context.guild.id}"
        )

        await context.reply(embed=embed, mention_author=False)

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