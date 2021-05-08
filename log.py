from termcolor import colored
from pyfiglet import Figlet
from datetime import datetime
import asyncio

#logo
def logo():
    logo = Figlet(font="graffiti")
    print(colored(logo.renderText("OneCoolBot"), "magenta"))

#on_ready
async def online(self):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("cog", "green"), colored(f"{self.qualified_name}", "magenta"), colored("online...", "green"))

#music_node_connection
async def music_node_connect(self, node):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("connected to node:", "green"), colored(f"{node.identifier}", "magenta"))

async def music_node_disconnect(self, node):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("connection lost to node:", "green"), colored(f"{node.identifier}", "magenta"))

#command loggers
async def client_command(context):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("command:", "green"), colored(f"{context.command}", "magenta"), colored("used by", "green"), colored(f"{context.author.name}#{context.author.discriminator}", "magenta"), colored("in guild", "green"), colored(f"{context.guild.name}", "magenta"), colored("at", "green"), colored(f"{current_time}", "magenta"))

async def cog_command(self, context):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[cogs.{self.qualified_name}]:", "magenta"), colored(f"{context.command}", "magenta"), colored("used by", "green"), colored(f"{context.author.name}#{context.author.discriminator}", "magenta"), colored("in guild", "green"), colored(f"{context.guild.name}", "magenta"), colored("at", "green"), colored(f"{current_time}", "magenta"))
    
#errors
async def help_error(self, context):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # print(colored(f"[{current_time}]", "magenta"), colored(f"{context.author.name}#{context.discriminator} command used in guild {context.guild.name}"))

#events
async def on_member_join(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "green"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("joined", "green"), colored(f"{member.guild}#{member.guild.id}", "magenta"))

async def member_add_db(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "green"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("was added to users table", "green"))

async def member_add_db_error(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occured when adding member:", "red"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("from users table", "red"))

async def on_guild_join(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("joined guild:", "green"), colored(f"{guild.name}#{guild.id}", "magenta"))

async def guild_add_db(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("guild:", "green"), colored(f"{guild.name}#{guild.id}", "magenta"), colored("was added to the guilds table", "green"))

async def guild_add_db_error(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occured when adding guild:", "red"), colored(f"{guild.name}#{guild.id}", "magenta"), colored("from guilds table", "red"))

async def on_member_remove(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "green"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("left", "green"), colored(f"{member.guild}#{member.guild.id}", "magenta"))

async def member_remove_db(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored(f"member:", "green"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("was removed from users table", "green"))

async def member_remove_db_error(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occured when removing member:", "red"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("from users table", "red"))

async def on_guild_remove(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("left guild:", "green"), colored(f"{guild.name}#{guild.id}", "magenta"))

async def on_guild_remove_db(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("guild:", "green"), colored(f"{guild.name}#{guild.id}", "magenta"), colored("was removed from the guilds table", "green"))

async def on_guild_remove_db_error(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occured when removing guild:", "red"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("from guilds table", "red"))

async def exp_add(self, message, xp_to_add):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("added", "cyan"), colored(f"{xp_to_add}", "magenta"), colored("xp to", "cyan"), colored(f"{message.author}", "magenta"), colored("in guild:", "cyan"), colored(f"{message.guild.name}", "magenta"))

async def coin_add(self, message, coins_on_xp):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("added", "blue"), colored(f"{coins_on_xp}", "magenta"), colored("coins to", "blue"), colored(f"{message.author}", "magenta"), colored("in guild:", "blue"), colored(f"{message.guild.name}", "magenta"))

async def level_up(self, message, new_lvl):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "cyan"), colored(f"{message.author}", "magenta"), colored("has leveled up to level:", "cyan"), colored(f"{new_lvl:,}", "magenta"), colored("in guild:", "cyan"), colored(f"{message.guild.name}", "magenta"))

async def member_redundant_add_db(self, message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "green"), colored(f"{message.author}#{message.author.discriminator}", "magenta"), colored("was added to users table", "green"))
