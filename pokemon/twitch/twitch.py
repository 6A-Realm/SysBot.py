from twitchio.ext import commands
import yaml
from yaml import load
yaml.warnings({'YAMLLoadWarning': False})
from pokemon.connection.wireless import switch, serv
import io
from aiohttp_requests import requests
from pokemon.utils.pokecrypto import *
from pokemon.utils.uqueue import queuelist
from pokemon.utils.values import bd, sp
import random
import string
import aiofiles
from json import loads
from rich.console import Console

console = Console()

# Simple file reader to load advanced settings
with open("advanced/blacklist.yaml", encoding = 'utf-8') as file:
    data = load(file)
    userblacklist = data["userblacklist"]

##Loads information from config file
with open("config.yaml") as file:
    data = load(file)
    tmitoken = data["tmitoken"]
    clientid = data["clientid"]
    botnickname = data["botnickname"]
    botprefix = data["botprefix"]
    channel = data["channel"]
    support2 = data["support-server-invite"]

# Defining client
client = commands.Bot(irc_token = tmitoken, client_id = clientid, nick = botnickname, prefix = botprefix, initial_channels = [channel])

# On ready
@client.event
async def event_ready():
    print("SysBot-Twitch.py has been turned on.")

    # Echo notification on start up
    ws = client._ws
    await ws.send_privmsg(channel, f"SysBot-Twitch.py echo notification.")

# Discord command
@client.command()
async def discord(ctx):
    if ctx.author.name.lower() == botnickname.lower():
        return
    await ctx.send(support2)

# Trade command
@client.command()
async def trade(ctx, set: str = None):

    # Check if blacklisted
    user = ctx.message.author.id
    if user in userblacklist:
        return await ctx.send("User is blacklisted from using the bot.")
    
    #check if in queue
    if ctx.message.author.id in queuelist:
        return await ctx.send("You are already in queue.")
    switch(serv, "getTitleID")
    title = serv.recv(689)
    title = title[:-1]
    title = str(title,'utf-8')
    if title in [bd, sp]:
        if set is not None:
            # Convert showdown to file
            showdown = await requests.post("https://7d256e9c7525.up.railway.app/pokemon/BDSP/showdown", json={"showdownSet": set})
            bytes = io.BytesIO()
            bytes.write(await showdown.content.read())
            data = bytearray(bytes.getvalue())

            # Convert to bytes and save
            pc = Pokecypto(data = data)
            encrypt = pc.encrypt()
            attachment = io.BytesIO(encrypt).read()

            randomizer = "" + ('').join(random.choices(string.ascii_letters + string.digits, k=20))

            async with aiofiles.open(f"Files/sysbot/requested-{randomizer}.eb8", 'wb+') as f:
                await f.write(attachment)

            response = loads((await (await requests.post("https://coreapi-production.up.railway.app/api/PokemonInfo", data = {"pokemon": data})).content.read()).decode("utf-8"))
            
            # Send to coreapi instance 
            if response["is_legal"] is True:

                # Add to queue
                console.log(f'User has been added to the queue', style="blue")
                await ctx.send(f'You have been added to the queue. Current queue length: {len(queuelist)}.')
            else: 
                reasonslist = []
                counter = 0
                enter = "\n"
                reasons = response["illegal_reasons"].split("\n")
                for r in reasons: 
                    counter += 1
                    reasonslist.append(f"{counter}. {r}")

                await ctx.send(f"Your Pokémon is illegal:\n{enter.join(re for re in reasonslist)}")

# Queue commands
@client.command()
async def queue(ctx):
    if ctx.message.author.id in queuelist:
        person = ctx.message.author.id
        position = queuelist.index(person) + 1
        await ctx.send(f"Your current position is {position}")
    else:
        await ctx.send("You are not in queue.")

@client.command()
async def list(ctx):
    length = {len(queuelist)}
    if length == 0:
        return await ctx.send("Queue is empty. Awaiting trades.")
    counter = 0
    for x in queuelist:
        counter += 1
    await ctx.send(f"There are {counter} users in queue")

@client.command()
async def leave(ctx):
    if ctx.message.author.id in queuelist:
        person = ctx.message.author.id
        position = queuelist.index(person)
        if position < 2:
            ctx.send("Cannot remove you from the queue, currently being processed.")            
        else:
            person = ctx.message.author.id
            queuelist.remove(person)
            await ctx.send("Removed from queue.")
    else:
        ctx.send("You are not in queue.")


if __name__ == "__main__":
    client.run()