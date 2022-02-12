import discord
import pokemon.connection.wireless as sysbot
from pokemon.utils.uqueue import queuelist
from pokemon.utils.values import hello, bd, sp
from pokemon.utils.pokecrypto import *
from cogs.presence import queuelength
from discord.ext import commands
from yaml import load
import io
from aiohttp_requests import requests
from json import loads
import aiofiles
from rich.console import Console
console = Console()


# Simple file reader to load advanced settings
with open("advanced/blacklist.yaml", encoding='utf-8') as file:
    data = load(file)
    userblacklist = data["userblacklist"]

# API links
coreapi = "https://coreapi-production.up.railway.app/api/PokemonInfo"
bdspshowdown = "https://pokegenpkhex-production-061e.up.railway.app/pokemon/BDSP/showdown"

async def addtoqueue(ctx, pokemon):
    queuelist[ctx.message.author.id] = pokemon
    console.log(f'{ctx.message.author.name} has been added to the queue', style="blue")
    await ctx.message.delete()
    await ctx.send(f'{ctx.message.author.name} has been added to the queue. Current queue length: {len(queuelist)}.')
    queuelength.clear()
    queuelength.append(f"{len(queuelist)}")

async def illegal(ctx, response):
    reasonslist = []
    counter = 0
    enter = "\n"
    reasons = response["illegal_reasons"].split("\n")
    for r in reasons: 
        counter += 1
        reasonslist.append(f"{counter}. {r}")
    embed = discord.Embed(title="Your Pokémon is illegal:", description=f"{enter.join(re for re in reasonslist)}", color = discord.Colour.red())
    await ctx.reply(embed = embed)

# Check legality
async def check(response, ctx, pokemon):
    # Send to coreapi instance 
    if response["is_legal"] is True:
        return await addtoqueue(ctx, pokemon)
    else: 
        return await illegal(ctx, response)

# Cog 
class request(commands.Cog):
    def __init__(self, client):
        self.client = client
        
# {-- Hello Module --}
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(hello)

# {-- Request Module --}
    @commands.command()
    @commands.guild_only()
    async def ttrade(self, ctx, *, set: str = None):

        # Checks if allowed to request
        if ctx.message.author.id in userblacklist:
            return await ctx.send("User is blacklisted from using the bot.")
        if ctx.message.author.id in queuelist:
            return await ctx.send("You are already in queue.")

        # Check title ID
        connection = sysbot.connection(self.client)
        await connection.connect()
        await connection.switch("getTitleID")
        title = ((await connection._r.read(689))[:-1]).decode("utf-8")

        if title in [bd, sp]:

            # Check if file
            if not set and len(ctx.message.attachments) != 0:
                attachment = ctx.message.attachments[0]
                if str(attachment).split(".")[-1].lower() == "eb8":

                    # Convert to bytes and save
                    buffer = io.BytesIO()
                    await attachment.save(buffer)
                    pokemon = buffer.getvalue()

                    # Check coreapi for legality
                    response = loads((await (await requests.post(coreapi, data={"pokemon": pokemon})).content.read()).decode("utf-8"))
                    await check(response, ctx, pokemon)

                elif str(attachment).split(".")[-1].lower() == "pb8":

                    buffer = io.BytesIO()
                    await attachment.save(buffer)
                    data = bytearray(buffer.getvalue())
                    pc = Pokecypto(data = data)
                    encrypt = pc.encrypt()
                    pokemon = io.BytesIO(encrypt).read()
                    response = loads((await (await requests.post(coreapi, data={"pokemon": data})).content.read()).decode("utf-8"))
                    await check(response, ctx, pokemon)

                else:
                    await ctx.send("Incorrect file type. Please provide a `.pb8` or `.eb8`.")

            # Check if showdown
            elif (not ctx.message.attachments) and (set is not None): 

                # Convert showdown to bytes
                showdown = await requests.post(bdspshowdown, json={"showdownSet": set}, headers = {"X-Pokemon-Encrypted": str(True).lower()})
                pokemon = (await showdown.content.read())
                if showdown.status < 300:
                    return await addtoqueue(ctx, pokemon)   
                else:
                    await ctx.send("Unable to generate a legal file from the provided showdown set.")

            else:
                await ctx.send("Incorrect command usage. Either provide a valid file or showdown set.")


def setup(client):
    client.add_cog(request(client))