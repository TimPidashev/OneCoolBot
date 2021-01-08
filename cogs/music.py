import discord
import wavelink
import typing as t
from discord.ext import commands

class AlreadyConnectedToChannel(commands.CommandError):
    pass

class NoVoiceChannel(commands.CommandError):
    pass


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(**args, **kwargs)

    async def connect(self, context, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(context.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def disconnect(self):
        try:
            await self.destroy()
        except KeyError:
            pass

class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                pass #needs to disconnect the bot from the channel but functionality not yet implemented...

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink node '{node.identifier}' ready...")

    async def cog_check(self, context):
        if isinstance(context.channel, discord.DMChannel):
            await context.send("Music commands are not available in DMs.")
            return False

        return True

    async def start_nodes(self):

        nodes = {
            "MAIN": {
                "host": '127.0.0.1',
                "port": 2333,
                "rest_uri": 'http://127.0.0.1:2333',
                "password": 'youshallnotpass',
                "identifier": 'MAIN',
                "region": 'Vancouver',
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstnce(obj, discord.Guild):
            return self.wavelink.get_player(guild.id, cls=Player)

    @commands.command(name="connect")
    async def connect_command(self, context, *, channel: t.Optional[discord.VoiceChannel]):
        player = self.get_player(context)
        channel = await player.connection(context, channel)
        await context.send(f"Connected to {channel.name}...")

    @connect_command.error
    async def connect_command_error(self, context, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await context.send("Already connected to a voice channel.")
        elif isinstance(exc, NoVoiceChannel):
            await context.send("No suitable voice channel was provided.")

    @commands.command(name="disconnect")
    async def disconnect_command(self, context):
        await player.disconnect()
        await context.send("Disconnected")




def setup(client):
    client.add_cog(Music(client))
