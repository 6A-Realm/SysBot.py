import discord
from discord.ext import commands
import io
from aiohttp_requests import requests
from pokemon.utils.pokecrypto import *
from json import loads
import base64
import aiofiles

# API links
pinfo = "https://coreapi-production.up.railway.app/api/PokemonInfo"
bdspshowdown = "https://pokegenpkhex-production.up.railway.app/pokemon/BDSP/showdown"

# Legality check 
async def check(ctx, response):
    # Send to coreapi instance 
    if response["is_legal"] is True:
        await ctx.send("The pokémon provided is legal and can be traded.")

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
class API(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Public Commands --}
    @commands.command()
    @commands.guild_only()
    async def legal(self, ctx, *, set: str = None):

        if not set and len(ctx.message.attachments) != 0:
            for attachment in ctx.message.attachments:                
                if attachment.filename.endswith((".eb8", ".pb8", ".pk6", ".pk7", ".ek8", ".pk8")):

                        # Convert to bytes and save
                        buffer = io.BytesIO()
                        await attachment.save(buffer)
                        data = buffer.getvalue()

                        # Send to coreapi instance 
                        response = loads((await (await requests.post(pinfo, data={"pokemon": data})).content.read()).decode("utf-8"))
                        await check(ctx, response)
        
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

                    response = loads((await (await requests.post(pinfo, data={"pokemon": data})).content.read()).decode("utf-8"))
                    await check(ctx, response)

                else:
                    return await ctx.channel.send("Ensure your file is valid, created from PKHeX.")

    @commands.command()
    @commands.guild_only()
    async def info(self, ctx):
        for attachment in ctx.message.attachments:                
            if attachment.filename.endswith((".eb8", ".pb8", ".pk6", ".pk7", ".ek8", ".pk8")):

                    # Convert to bytes and save
                    buffer = io.BytesIO()
                    await attachment.save(buffer)
                    data = buffer.getvalue()

                    # Send to coreapi instance 
                    response = loads((await (await requests.post(pinfo, data={"pokemon": data})).content.read()).decode("utf-8"))
                    species = response["species"]
                    gender = response["gender"]
                    item = response["held_item"]

                    ability = response["ability"]
                    level = response["level"]
                    shiny = response["is_shiny"]

                    nature = response["nature"]

                    m1 = response["move1"]
                    m2 = response["move2"]
                    m3 = response["move3"]
                    m4 = response["move4"]

                    information = f"{species} ({gender}) @ {item}\nAbility: {ability}\nLevel: {level}\nShiny: {shiny}\n{nature} Nature\n-{m1}\n-{m2}\n-{m3}\n-{m4}"
                    await ctx.send(information)

            else:
                return await ctx.channel.send("Ensure your file is valid, created from PKHeX.")
                
    @commands.command()
    @commands.guild_only()
    async def trainerinfo(self, ctx):
        for attachment in ctx.message.attachments:                
            if attachment.filename.endswith((".eb8", ".pb8", ".pk6", ".pk7", ".ek8", ".pk8")):

                    # Convert to bytes and save
                    buffer = io.BytesIO()
                    await attachment.save(buffer)
                    data = buffer.getvalue()

                    # Send to coreapi instance 
                    response = loads((await (await requests.post(pinfo, data={"pokemon": data})).content.read()).decode("utf-8"))
                    ot = response["ot"]
                    tid = response["tid"]
                    sid = response["sid"]

                    information = f"**OT:** {ot} **TID:** {tid} **SID:** {sid}"

                    await ctx.send(information)

            else:
                return await ctx.channel.send("Ensure your file is valid, created from PKHeX.")

    @commands.command()
    @commands.guild_only()
    async def qr(self, ctx):
        for attachment in ctx.message.attachments:                
            if attachment.filename.endswith((".eb8", ".pb8", ".pk6", ".pk7", ".ek8", ".pk8")):

                    # Convert to bytes and save
                    buffer = io.BytesIO()
                    await attachment.save(buffer)
                    data = buffer.getvalue()

                    # Send to coreapi instance 
                    response = loads((await (await requests.post(pinfo, data={"pokemon": data})).content.read()).decode("utf-8"))
                    qr = discord.File(io.BytesIO(base64.decodebytes(response['qr'].encode("ascii"))), 'qr.png')
                    await ctx.send(file = qr)

            else:
                return await ctx.channel.send("Ensure your file is valid, created from PKHeX.")

    @commands.command()
    @commands.guild_only()
    async def convert(self, ctx, *, set: str = None):

        if set is not None:

                # Convert showdown to file
                showdown = await requests.post(bdspshowdown, json={"showdownSet": set})
                bytes = io.BytesIO()
                bytes.write(await showdown.content.read())
                data = bytearray(bytes.getvalue())

                # Convert to bytes and save
                pc = Pokecypto(data = data)
                encrypt = pc.encrypt()
                attachment = io.BytesIO(encrypt).read()

                response = loads((await (await requests.post(pinfo, data={"pokemon": data})).content.read()).decode("utf-8"))
                
                if response["is_legal"] is True:
                    species = response["species"]
                    async with aiofiles.open(f"Files/sysbot/{species}.eb8", 'wb+') as f:
                        await f.write(attachment)
                    await ctx.send(file=discord.File(f"Files/sysbot/{species}.eb8"))
                
                else:
                    await ctx.send("Unable to generate a legal file from the provided showdown set.")
        
        else:
            await ctx.send("Provide a showdown set to convert.")


def setup(client):
    client.add_cog(API(client))