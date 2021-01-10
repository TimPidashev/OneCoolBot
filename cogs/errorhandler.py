import discord
import traceback
import sys
from discord.ext import commands

class errorhandler(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        if hassattr(context.command, "on_error"):
            return

        cog = context.cog
        if cog:
            if cog.get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound)

        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await context.send(f"{context.command} has been disabled :(")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await context.author.send(f"{context.command} can not be used in private messages.")
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if context.command.qualified_name == "tag list":
                await context.send("I could not find that membe. Please try again.")

        else:
            return

def setup(client):
    client.add_cog(errorhandler(client))
