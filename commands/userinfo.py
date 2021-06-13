import discord
from discord.ext import commands
from utils import log

class userinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["usrinf", "ui"])
    async def userinfo(self, context, user: discord.Member = None):
        await log.cog_command(self, context)

        if isinstance(context.channel, discord.DMChannel):
            return

        if user is None:
            user = context.author 

        embed = discord.Embed(
            colour=0x9b59b6
        )
        embed.set_author(
            name=str(user), 
            icon_url=user.avatar_url
        )
        
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        members = sorted(context.guild.members, key=lambda m: m.joined_at)
        date_format = "%a, %d %b %Y at %I:%M %p"

        top_role = user.top_role
        
        fields = [("Joined this server at", user.joined_at.strftime(date_format), True),
                  ("Registered this account at", user.created_at.strftime(date_format), False),
                  ("Server join position", str(members.index(user)+1), True),
                  ("Roles [{}]".format(len(user.roles)-1), top_role.mention, True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(
            text="ID: " + str(user.id)
        )
        await context.reply(embed=embed, mention_author=False)

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