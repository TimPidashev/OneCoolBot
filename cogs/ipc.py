from discord.ext import commands, ipc
from termcolor import colored

class IpcRoutes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(colored("[ipc]: online...", "white"))

    @ipc.server.route()
    async def get_member_count(self, data):
        guild = self.client.get_guild(
            data.guild_id
        )  # get the guild object using parsed guild_id

        return guild.member_count  # return the member count to the client
    
def setup(client):
    client.add_cog(IpcRoutes(client))