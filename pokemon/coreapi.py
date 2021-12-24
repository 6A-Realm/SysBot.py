### All made by GriffinG1 ###

import discord
from discord.ext import commands
import asyncio
import aiohttp
from datetime import datetime
from pokemon.exceptions import PKHeXMissingArgs

### All made by GriffinG1 ###
api_url = " https://flagbrew.org/"

class coreapi(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='legality', aliases=['illegal'])
    async def check_legality(self, ctx, *, data=""):
        """Checks the legality of either a provided URL or attached pkx file. URL *must* be a direct download link"""
        if not data and not ctx.message.attachments:
            raise PKHeXMissingArgs()
        r = await self.process_file(ctx, data, ctx.message.attachments, "api/v2/pksm/legality")
        if r == 400:
            return
        rj = r[1]
        reasons = rj["IllegalReasons"].split("\n")
        if reasons[0] == "Legal!":
            return await ctx.send("That Pokemon is legal!")
        embed = discord.Embed(title="Legality Issues", description="", colour=discord.Colour.red())
        embed = self.list_to_embed(embed, reasons)
        await ctx.send(embed=embed)

### All made by GriffinG1 ###

def setup(client):
    client.add_cog(coreapi(client))

### All made by GriffinG1 ###