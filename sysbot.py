import discord
from discord import shard
from discord.ext import commands, ipc
import os
import yaml
from yaml import load
yaml.warnings({'YAMLLoadWarning': False})
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from colorama import Fore
import ctypes
from rich.console import Console
import asyncio
from asyncio.tasks import create_task
from asyncio.runners import run
from discord.ext.commands import CommandNotFound
import json

##Loads token and prefix from config file
with open("config.yaml") as file:
    data = load(file)
    token = data["token"]
    botprefix = data["botprefix"]
    embedcolor = data["color"]
    support = data["support-server-name"]
    support2 = data["support-server-invite"]
    dmchannel = data["dmchannel"]
    autolauncher = data["autolauncher"]

# Fetch prefix 
def get_prefix(client, message):
    with open("res/prefix.json", "r") as f:
        prefixes = json.load(f)
    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(*prefix)(client, message)

##Simple bot settings like mentioning as a prefix, settings all intents to true, deleting built in discord.py help command
client = commands.AutoShardedBot(shard_count=1, description="SysBot 1.1.0", command_prefix=get_prefix, intents=discord.Intents.all(), help_command = None, pm_help = False)
slash = SlashCommand(client, sync_commands=True)
pokemon = ["connection", "coreapi", "pokeinput", "queue", "remote", "trader", "advanced"]       
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

#Looped status sequence
    while True:
        await client.change_presence(activity=discord.Game(name=f'{str(botprefix)}help'))
        await asyncio.sleep(30)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you get your pokemon"))
        await asyncio.sleep(30)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".eb8s only."))
        await asyncio.sleep(30)
        await client.change_presence(activity=discord.Game(name=f'BDSP ooo'))
        await asyncio.sleep(30)

# Error Handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        pass
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("You are missing required arguments.")
    if isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("You were unclear with your arguments.")
    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await ctx.send(f"Looks like you have already casted a vote recently!")    
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You're missing the following permissions: \n**{', '.join(error.missing_permissions)}**")
    if isinstance(error, discord.ext.commands.errors.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
    if isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("This member was not found.") 
    if isinstance(error, discord.ext.commands.errors.GuildNotFound):
        await ctx.send("This guild was not found.")      
    if isinstance(error, discord.ext.commands.errors.UserNotFound):
        await ctx.send("This user was not found.")  
    if isinstance(error, discord.ext.commands.errors.ChannelNotFound):
        await ctx.send("This channel was not found.")  
    if isinstance(error, discord.ext.commands.errors.RoleNotFound):
        await ctx.send("This role was not found.")   
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f"I'm missing the following permissions: \n**{', '.join(error.missing_permissions)}**")
    if isinstance(error, commands.NotOwner):
        await ctx.send("Only the owner of this bot can use that command.")
        
##Events
@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        if message.author.bot:
            return
        channel = client.get_channel(dmchannel)
        embed=discord.Embed(title=f"**{message.author}** ({message.author.id}) sent:", description=f"```{message.content}```", color=0x0d1d96)
        embed.set_footer(text=f"Reply using the command .directmessage {message.author.id}")
        await channel.send(embed=embed)    
    await client.process_commands(message)

@client.event
async def on_guild_join(guild):
    welcomer = discord.Embed(title = 'Thanks for adding me!', description = f"""
        Thank you for adding me to {guild.name}!
        You can use the `{botprefix}help` command to get started!
        Dont forget to join our official server [{support}]({support2}) 
        """, color=embedcolor)
    welcomer.set_thumbnail(url="")
    welcomer.set_footer(text=support2)
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed = welcomer)
        break
    try:
        await guild.owner.send(embed = welcomer)
    except:
        pass
    with open("res/prefix.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = botprefix
    with open("res/prefix.json", "w") as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open("res/prefix.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open("res/prefix.json", "w") as f:
        json.dump(prefixes, f, indent=4)

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