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
#command loggers
async def client_command(context):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored("[client]:", "magenta"), colored(f"{context.command}", "magenta"), colored("used by", "green"), colored(f"{context.author.name}#{context.author.discriminator}", "magenta"), colored("in guild", "green"), colored(f"{context.guild.name}", "magenta"), colored("at", "green"), colored(f"{current_time}", "magenta"))

async def cog_command(self, context):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(colored(f"[cogs.{self.qualified_name}]:", "magenta"), colored(f"{context.command}", "magenta"), colored("used by", "green"), colored(f"{context.author.name}#{context.author.discriminator}", "magenta"), colored("in guild", "green"), colored(f"{context.guild.name}", "magenta"), colored("at", "green"), colored(f"{current_time}", "magenta"))
    
#error handler
# def error(self, context):