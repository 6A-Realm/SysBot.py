import discord
from pokemon.connection.wireless import switch, serv
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
bdspshowdown = "https://7d256e9c7525.up.railway.app/pokemon/BDSP/showdown"

# Convert 

# Check legality
async def check(ctx, pkx, attachment, response, user):
    # Send to coreapi instance 
    if response["is_legal"] is True:
        if pkx is True:
            await attachment.save(f"Files/sysbot/requested-{user}.eb8")

        # Add to queue
        queuelist.append(user)
        console.log(f'{ctx.message.author.name} has been added to the queue', style="blue")
        await ctx.message.delete()
        await ctx.send(f'{ctx.message.author.name} has been added to the queue. Current queue length: {len(queuelist)}.')
        queuelength.clear()
        queuelength.append(f"{len(queuelist)}")

    else: 
        reasonslist = []
        counter = 0
        enter = "\n"
        reasons = response["illegal_reasons"].split("\n")
        for r in reasons: 
            counter += 1
            reasonslist.append(f"{counter}. {r}")
        embed = discord.Embed(title="Your Pokémon is illegal:", description=f"{enter.join(re for re in reasonslist)}", color = discord.Colour.red())
        await ctx.reply(embed = embed)

# Cog 
class request(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Test}
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(hello)

# {-- Request Module --}
    @commands.command()
    @commands.guild_only()
    async def ttrade(self, ctx, set: str = None):
        user = ctx.message.author.id
        if user in userblacklist:
            return await ctx.send("User is blacklisted from using the bot.")
        if ctx.message.author.id in queuelist:
            return await ctx.send("You are already in queue.")
        switch(serv, "getTitleID")
        title = serv.recv(689)
        title = title[:-1]
        title = str(title,'utf-8')
        if title in [bd, sp]:
            pkx = False
            if not set and len(ctx.message.attachments) != 0:
                attachment = ctx.message.attachments[0]
                if str(attachment).split(".")[-1].lower() == "eb8":
                    pkx = True

                    # Convert to bytes and save
                    buffer = io.BytesIO()
                    await attachment.save(buffer)
                    data = buffer.getvalue()
                    response = loads((await (await requests.post(coreapi, data={"pokemon": data})).content.read()).decode("utf-8"))

                    await check(ctx, pkx, attachment, response, user)

                elif str(attachment).split(".")[-1].lower() == "pb8":

                    # Convert to bytes and save
                    buffer = io.BytesIO()
                    await attachment.save(buffer)
                    data = bytearray(buffer.getvalue())
                    pc = Pokecypto(data = data)
                    encrypt = pc.encrypt()
                    attachment = io.BytesIO(encrypt).read()
                    async with aiofiles.open(f"Files/sysbot/requested-{user}.eb8", 'wb+') as f:
                        await f.write(attachment)
                        
                    response = loads((await (await requests.post(coreapi, data={"pokemon": data})).content.read()).decode("utf-8"))

                    await check(ctx, pkx, attachment, response, user)

                else:
                    await ctx.send("Incorrect file type. Please provide a `.pb8` or `.eb8`.")

            elif (not ctx.message.attachments) and (set is not None): 

                # Convert showdown to file
                showdown = await requests.post(bdspshowdown, json={"showdownSet": set})
                bytes = io.BytesIO()
                bytes.write(await showdown.content.read())
                data = bytearray(bytes.getvalue())

                # Convert to bytes and save
                pc = Pokecypto(data = data)
                encrypt = pc.encrypt()
                attachment = io.BytesIO(encrypt).read()

                async with aiofiles.open(f"Files/sysbot/requested-{user}.eb8", 'wb+') as f:
                    await f.write(attachment)

                response = loads((await (await requests.post(coreapi, data={"pokemon": data})).content.read()).decode("utf-8"))
                
                await check(ctx, pkx, attachment, response, user)


            else:
                await ctx.send("Incorrect command usage. Either provide a valid file or showdown set.")


def setup(client):
    client.add_cog(request(client))