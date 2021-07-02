from termcolor import colored
from pyfiglet import Figlet
from datetime import datetime, timedelta
import asyncio
import os
import sys

#logger
def logger(message):
    with open("./data/logs/client.log", "a+") as log:
        log.write(f"{message}\n")
        log.close()

def querylogger(message):
    with open("./data/logs/database.log", "a+") as log:
        log.write(f"{message}\n")
        log.close()

#logo
def logo():
    logo = Figlet(font="graffiti")
    print(colored(logo.renderText("OneCoolBot"), "magenta"))
    message = logo.renderText("OneCoolBot")
    logger(message)

#on_ready
async def online(self):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("cog:", "green"), colored(f"{self.qualified_name}", "magenta"), colored("loaded...", "green"))
    message = f"[{current_time}] cog: {self.qualified_name} loaded..."
    logger(message)

async def on_command_ready(self):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("command:", "green"), colored(f"{self.qualified_name}", "magenta"), colored("loaded...", "green"))
    message = f"[{current_time}] command: {self.qualified_name} loaded..."
    logger(message)

#music_node_connection
async def music_node_connect(self, node):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("client connected to node:", "green"), colored(f"{node.identifier}", "magenta"))
    message = f"[{current_time}] client connected to node: {node.identifier}"
    logger(message)

async def music_node_disconnect(self, node):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("connection lost to node:", "green"), colored(f"{node.identifier}", "magenta"))
    message = f"[{current_time}] connection lost to node: {node.identifier}"
    logger(message)

#command loggers
async def client_command(context):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("command:", "green"), colored(f"{context.command}", "magenta"), colored("used by", "green"), colored(f"{context.author.name}#{context.author.discriminator}", "magenta"), colored("in guild:", "green"), colored(f"{context.guild.name}", "magenta"))
    message = f"[{current_time}] command: {context.command} used by: {context.author.name}#{context.author.discriminator} in guild: {context.guild.name}#{context.guild.id}"
    logger(message)

async def cog_command(self, context):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored(f"{context.command}", "magenta"), colored("used by:", "green"), colored(f"{context.author.name}#{context.author.discriminator}", "magenta"), colored("in guild:", "green"), colored(f"{context.guild.name}", "magenta"))
    message = f"[{current_time}] {context.command} used by: {context.author.name}#{context.author.discriminator} in guild: {context.guild.name}#{context.guild.id}"
    logger(message)

async def slash_command(self, context):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored(f"slash command: {context.command}", "magenta"), colored("used by:", "green"), colored(f"{context.author.name}#{context.author.discriminator}", "magenta"), colored("in guild:", "green"), colored(f"{context.guild.name}", "magenta"))
    message = f"[{current_time}] slash command: {context.command} used by: {context.author.name}#{context.author.discriminator} in guild: {context.guild.name}#{context.guild.id}"
    logger(message)

#errors
async def help_error(self, context):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # print(colored(f"[{current_time}]", "magenta"), colored(f"{context.author.name}#{context.discriminator} command used in guild {context.guild.name}"))

#events
async def on_member_join(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "green"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("joined guild:", "green"), colored(f"{member.guild}", "magenta"))
    message = f"[{current_time}] member: {member.name}#{member.discriminator} joined guild: {member.guild}#{member.guild.id}"
    logger(message)

async def member_add_db(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "green"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("was added to users table in guild:", "green"), colored(f"{member.guild.name}", "magenta"))
    message = f"[{current_time}] member: {member.name}#{member.discriminator} was added to users table in guild: {member.guild.name}#{member.guild.id}"
    logger(message)

async def member_add_db_error(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occured when adding member:", "red"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("to  users table in guild:", "red"), colored(f"{member.guild.name}", "magenta"))
    message = f"[{current_time}] an error occured when adding member: {member.name}#{member.discriminator} to users table in guild: {member.guild.name}#{member.guild.id}"
    logger(message)

async def on_guild_join(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("client joined guild:", "green"), colored(f"{guild.name}#{guild.id}", "magenta"))
    message = f"[{current_time}] client joined guild: {guild.name}#{guild.id}"
    logger(message)

async def guild_add_db(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("guild:", "green"), colored(f"{guild.name}#{guild.id}", "magenta"), colored("was added to the guilds table", "green"))
    message = f"[{current_time}] guild: {guild.name}#{guild.id} was added to guilds table"
    logger(message)

async def guild_add_db_error(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occured when adding guild:", "red"), colored(f"{guild.name}#{guild.id}", "magenta"), colored("to guilds table", "red"))
    message = f"[{current_time}] an error occurred when adding guild: {guild.name}#{guild.id} to guilds table"
    logger(message)

async def on_member_remove(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "green"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("left guild:", "green"), colored(f"{member.guild}#{member.guild.id}", "magenta"))
    message = f"[{current_time}] member: {member.name}#{member.discriminator} left guild: {member.guild.name}#{member.guild.id}"
    logger(message)

async def member_remove_db(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored(f"member:", "green"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("was removed from users table in guild:", "green"), colored(f"{member.guild.name}", "magenta"))
    message = f"[{current_time}] member: {member.name}#{member.discriminator} was removed from guilds table in guild: {member.guild.name}#{member.guild.id}"
    logger(message)
    
async def member_remove_db_error(self, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occured when removing member:", "red"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("from users table in guild:", "red"), colored(f"{member.guild.name}", "magenta"))
    message = f"[{current_time}] an error occured when trying to remove member: {member.name}#{member.discriminator} from users table in guild: {member.guild.name}#{member.guild.id}"
    logger(message)

async def on_guild_remove(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("client left guild:", "green"), colored(f"{guild.name}#{guild.id}", "magenta"))
    message = f"[{current_time}] client left guild: {guild.name}#{guild.id}"
    logger(message)

async def on_guild_remove_db(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("guild:", "green"), colored(f"{guild.name}#{guild.id}", "magenta"), colored("was removed from the guilds table", "green"))
    message = f"[{current_time}] guild: {guild.name}#{guild.id} was removed from guilds table"
    logger(message)

async def on_guild_remove_db_error(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occured when removing guild:", "red"), colored(f"{guild.name}", "magenta"), colored("from guilds table", "red"))
    message = f"[{current_time}] an error occured when removing guild: {guild.name}#{guild.id} from guilds table"
    logger(message)

async def exp_add(self, message, xp_to_add):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("added", "cyan"), colored(f"{xp_to_add}", "magenta"), colored("xp to member", "cyan"), colored(f"{message.author}", "magenta"), colored("in guild:", "cyan"), colored(f"{message.guild.name}", "magenta"))
    message = f"[{current_time}] added {xp_to_add} xp to member: {message.author} in guild: {message.guild.name}#{message.guild.id}"
    logger(message)

async def coin_add(self, message, coins_on_xp):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("added", "blue"), colored(f"{coins_on_xp}", "magenta"), colored("coins to member:", "blue"), colored(f"{message.author}", "magenta"), colored("in guild:", "blue"), colored(f"{message.guild.name}", "magenta"))
    message = f"[{current_time}] added {coins_on_xp} coins to member: {message.author} in guild: {message.guild.name}#{message.guild.id}"
    logger(message)

async def level_up(self, message, new_lvl):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "cyan"), colored(f"{message.author}", "magenta"), colored("has leveled up to level:", "cyan"), colored(f"{new_lvl:,}", "magenta"), colored("in guild:", "cyan"), colored(f"{message.guild.name}", "magenta"))
    message = f"[{current_time}] member: {message.author} has leveled up to level: {new_lvl:,} in guild: {message.guild.name}#{message.guild.id}"
    logger(message)

async def member_redundant_add_db(self, message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "green"), colored(f"{message.author}", "magenta"), colored("was added to users table in guild:", "green"), colored(f"{message.guild.name}", "magenta"))
    message = f"[{current_time}] member: {message.author} was added to users table in guild: {message.guild.name}#{message.guild.id}"
    logger(message)

async def clear_messages(self, context, amount):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "yellow"), colored(f"{context.author.name}#{context.author.discriminator}", "magenta"), colored("removed", "yellow"), colored(f"{amount}", "magenta"), colored("messages in guild:", "yellow"), colored(f"{context.guild.name}", "magenta"))
    message = f"[{current_time}] member: {context.author.name}#{context.author.discriminator} removed {amount} messages in guild: {context.guild.name}#{context.guild.id}"
    logger(message)

async def kick_member(self, context, member, reason):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "yellow"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("was kicked from guild:", "yellow"), colored(f"{context.guild.name}", "magenta"), colored("by member:", "yellow"), colored(f"{context.author.name}.", "magenta"), colored(f"Reason: {reason}", "yellow"))
    message = f"[{current_time}] member: {member.name}#{member.discriminator} was kicked from guild: {context.guild.name}#{context.guild.id} by member: {context.author.name}#{context.author.id}. Reason: {reason}"
    logger(message)

async def kick_member_error(self, context, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occured while trying to kick member:", "red"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("from guild:", "red"), colored(f"{context.guild.name}", "magenta"))
    message = f"[{current_time}] an error occured while trying to kick member: {member.name}#{member.discriminator} from guild: {context.guild.name}#{context.guild.id}"
    logger(message)

async def ban_member(self, context, member, reason):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "yellow"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("was banned from guild:", "yellow"), colored(f"{context.guild.name}", "magenta"), colored("by member:", "yellow"), colored(f"{context.author}.", "magenta"), colored(f"Reason: {reason}", "yellow"))
    message = f"[{current_time}] member: {member.name}#{member.discriminator} was banned from guild: {context.guild.name}#{context.guild.id} by member: {context.author}. Reason: {reason}"
    logger(message)

async def ban_member_error(self, context, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occured while trying to ban member:", "red"), colored(f"{member.name}", "magenta"), colored("from guild:", "red"), colored(f"{context.guild.name}", "magenta"))
    message = f"[{current_time}] an error occured while trying to ban member: {member.name}#{member.discriminator} from guild: {context.guild.name}#{context.guild.id}"
    logger(name)

async def unban_member(self, context, member, reason):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "yellow"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("was unbanned from guild:", "yellow"), colored(f"{context.guild.name}", "magenta"), colored("by member:", "yellow"), colored(f"{context.author}.", "magenta"), colored(f"Reason: {reason}", "yellow"))
    message = f"[{current_time}] member: {member.name}#{member.discriminator} was unbanned from guild: {context.guild.name}#{context.guild.id} by member: {context.author}. Reason: {reason}"
    logger(message)

async def unban_member_error(self, context, member):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occured while trying to unban member:", "red"), colored(f"{member.name}#{member.discriminator}", "magenta"), colored("from guild:", "red"), colored(f"{context.guild.name}", "magenta"))
    message = f"[{current_time}] an error occured while trying to unban member: {member.name}#{member.discriminator} from guild: {context.guild.name}#{context.guild.id}"
    logger(message)

async def advertise(self, message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "yellow"), colored(f"{message.author.name}#{member.author.discriminator}", "magenta"), colored("tried to advertise:", "yellow"), colored(f"{message.content}", "magenta"), colored("in guild:", "yellow"), colored(f"{message.guild.name}", "magenta"))
    message = f"[{current_time}] member: {message.author.name}#{message.author.discriminator} tried to advertise: {message.content} in guild: {message.guild.name}#{message.guild.id}"
    logger(message)

async def report(self, message_count):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("Activity Report:", "green"), colored(f"{message_count}", "magenta"), colored("messages were sent in the last minute.", "green"))
    message = f"[{current_time}] Activity Report: {message_count} messages were sent in the last minute."
    logger(message)

async def guildconfig_add_db(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("added guild:", "green"), colored(f"{guild.name}", "magenta"), colored("to guildconfig table", "green"))
    message = f"[{current_time}] added guild: {guild.name}#{guild.id} to guildconfig table"
    logger(message)

async def guild_config_add_db_error(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occurred while trying to add guild:", "red"), colored(f"{guild.name}", "magenta"), colored("to guildconfig table", "red"))
    message = f"[{current_time}] an error occured while trying to add guild: {guild.name}#{guild.id} to guildconfig table"
    logger(message)

async def on_guild_remove_guildconfig(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("removed guild:", "green"), colored(f"{guild.name}", "magenta"), colored("from guildconfig table", "green"))
    message = f"[{current_time}] removed guild: {guild.name}#{guild.id} from guildconfig table"
    logger(message)

async def on_guild_remove_guildcofig_error(self, guild):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("an error occurred while trying to remove guild:", "red"), colored(f"{guild.name}", "magenta"), colored("from guildconfig table", "red"))
    message = f"[{current_time}] an error occured while trying to remove guild: {guild.name}#{guild.id} from guildconfig table"
    logger(message)
    
async def client_connect(self):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("client connected to gateway", "green"))
    message = f"[{current_time}] client connected to gateway"
    logger(message)

async def on_shard_ready(self, shard_id):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("client connected to shard:", "green"), colored(f"{shard_id}", "magenta"))
    message = f"[{current_time}] client connected to shard: {shard_id}"
    logger(message)

async def client_disconnect(self):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("client disconnected from gateway, attempting to reconnect...", "red"))
    message = f"[{current_time}] client disconnected from gateway, attempting to reconnect..."
    logger(message)

async def client_close():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("client process closed by owner", "green"))
    message = f"[{current_time}] client process closed by owner"
    logger(message)

async def client_reconnect(self):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("client reconnected to gateway", "green"))
    message = f"[{current_time}] client reconnected to gateway"
    logger(message)

async def update_users_table():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("updated users table", "green"))
    message = f"[{current_time}] updated users table"
    logger(message)

async def update_guilds_table():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("updated guilds table", "green"))
    message = f"[{current_time}] updated guilds table"
    logger(message)

async def update_guildconfig_table():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("updated guildconfig table", "green"))
    message = f"[{current_time}] updated guildconfig table"
    logger(message)

async def is_owner_false(self, context, error):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[{current_time}]", "magenta"), colored("member:", "yellow"), colored(f"{context.author.name}#{context.author.discriminator}", "magenta"), colored("attempted to use sudo command:", "yellow"), colored(f"{context.command}", "magenta"), colored("in guild:", "yellow"), colored(f"{context.guild.name}#{context.guild.id}", "magenta"))
    message = f"[{current_time}] member: {context.author.name}#{context.author.discriminator} attempted to use sudo command: {context.command} in guild: {context.guild.name}#{context.guild.id}"
    logger(message)

