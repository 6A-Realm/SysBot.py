import discord
from discord import shard
from discord.ext import commands
import os
import yaml
from yaml import load
yaml.warnings({'YAMLLoadWarning': False})
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from colorama import Fore
import ctypes
from rich.console import Console
from asyncio.tasks import create_task
from asyncio.runners import run
import json

# Loads token and autolauncher from config file
with open("config.yaml") as file:
    data = load(file)
    token = data["token"]
    autolauncher = data["autolauncher"]

# Fetch prefix 
def get_prefix(client, message):        
    with open("res/prefix.json", "r") as f:
        prefixes = json.load(f)
    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(*prefix)(client, message)

##Simple bot settings like mentioning as a prefix, settings all intents to true, deleting built in discord.py help command
client = commands.AutoShardedBot(description="SysBot 1.1.4", command_prefix=get_prefix, intents=discord.Intents.all(), help_command = None, pm_help = False)
slash = SlashCommand(client, sync_commands=True)
pokemon = ["connection", "pokeinput", "queue", "remote", "trader", "advanced"]       
console = Console()

#Bot Start Up
@client.event
async def on_ready():
    ctypes.windll.kernel32.SetConsoleTitleW('{0.user}'.format(client) + ' ALPHA')
    print(f'''{Fore.LIGHTBLUE_EX}
   _____           ____        _                 
  / ____|         |  _ \      | |                
 | (___  _   _ ___| |_) | ___ | |_   _ __  _   _ 
  \___ \| | | / __|  _ < / _ \| __| | '_ \| | | |
  ____) | |_| \__ \ |_) | (_) | |_ _| |_) | |_| |
 |_____/ \__, |___/____/ \___/ \__(_)  __/ \__, |
          __/ |                     | |     __/ |
         |___/                      |_|    |___/ 
                                            \x1b[0m{Fore.MAGENTA}By 6A\x1b[0m
    ''')
    if autolauncher == 0:
        console.print("Would you like to connect a Nintendo Switch to your bot?\nType Y to load the sysbot module, type N to continue without the sysbot.", style="yellow")
        yes = {'yes', 'y'}
        choice = input().lower()
        if choice in yes:
            for extension in pokemon:
                try:
                    client.load_extension("pokemon." + extension) 
                except Exception as e:
                    console.print(f"Unable to load {extension}.", style="red")
        
        else:
            print('The bot will launch without sysbot commands.')
    if autolauncher == 1:
        console.print("Autolauncher set to true.", style="green")
        for extension in pokemon:
            try:
                client.load_extension("pokemon." + extension)
            except Exception as e:
                console.print(f"Unable to load {extension}.", style="red")
    if autolauncher ==2:
        console.print('The bot will launch without sysbot commands.', style="blue")

# Build Plugins List
plugins = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        plugins.append("cogs." + filename[:-3])

for filename in os.listdir('./helper'):
    if filename.endswith('.py'):
        if not filename.startswith('names') and not filename.startswith('solver'):
            plugins.append("helper." + filename[:-3])
            
# Load plugins
if __name__ == '__main__':
    for x in plugins:
        try:
            client.load_extension(x)
        except Exception as e:
            console.print(f"Unable to load {x}.", style="red")

try:
    client.run('{}'.format(token))
except Exception as e:
    print(f"Error when logging in: {e}")