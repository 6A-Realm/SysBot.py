import asyncio
import discord
from discord.ext import commands
import os
import glob
import random

class PKHeX(commands.Cog):
    def __init__(self, client):
        self.client = client

# Settings for pk8 bot. Do not change or no files will be found
    def namek8(self, filepath):
        with open(filepath, "rb") as f:
            data = f.read()[88:112]
            name = data.decode("utf-16", "ignore").replace("\0", "")
        return name

    @commands.command()
    @commands.guild_only()
    async def pk8(self, ctx, *, query):
        check = False
        for filepath in glob.glob(f"Files/pk8/*.pk8"):
            if (self.namek8(filepath).lower() == query.lower()):
                await ctx.send(file=discord.File(filepath))
                check = True
        await asyncio.sleep(10)
        if check == False:
            await ctx.send("The `pk8` for this pokemon does not exist yet.")
            return
        else:
            return

    @commands.command()
    @commands.guild_only()
    async def ek8(self, ctx, pokemon_name):
        filepath = f"Files/ek8/{pokemon_name}.ek8"
        if os.path.exists(filepath):
            await ctx.send(file=discord.File(filepath))
        else:
            await ctx.send("The `ek8` for this pokemon does not exist yet.")

    @commands.command()
    @commands.guild_only()
    async def pk7(self, ctx, pokemon_name):
        filepath = f"Files/pk7/{pokemon_name}.pk7"
        if os.path.exists(filepath):
            await ctx.send(file=discord.File(filepath))
        else:
            await ctx.send("The `pk7` for this pokemon does not exist yet.")

    @commands.command()
    @commands.guild_only()
    async def pk6(self, ctx, pokemon_name):
        filepath = f"Files/pk6/{pokemon_name}.pk6"
        if os.path.exists(filepath):
            await ctx.send(file=discord.File(filepath))
        else:
            await ctx.send("The `pk6` for this pokemon does not exist yet.")

    @commands.command()
    @commands.guild_only()
    async def pb7(self, ctx, pokemon_name):
        filepath = f"Files/pb7/{pokemon_name}.pb7"
        if os.path.exists(filepath):
            await ctx.send(file=discord.File(filepath))
        else:
            await ctx.send("The `pb7` for this pokemon does not exist yet.")

    @commands.command()
    @commands.guild_only()
    async def pb8(self, ctx, pokemon_name):
        filepath = f"Files/pb8/{pokemon_name}.pb8"
        if os.path.exists(filepath):
            await ctx.send(file=discord.File(filepath))
        else:
            await ctx.send("The `pb8` for this pokemon does not exist yet.")

    @commands.command()
    @commands.guild_only()
    async def eb8(self, ctx, pokemon_name):
        filepath = f"Files/eb8/{pokemon_name}.eb8"
        if os.path.exists(filepath):
            await ctx.send(file=discord.File(filepath))
        else:
            await ctx.send("The `eb8` for this pokemon does not exist yet.")

    @commands.command()
    @commands.guild_only()
    async def dump(self, ctx, amount: int = 1):
        if amount > 5:
            await ctx.send("You are not able to request more than 5 files at a time.")
        else:
            list = []
            detected = False
            for a in range(amount):
                filepath = f"Files/dump/"
                file = random.choice(os.listdir(filepath))
                if file not in list:
                    list.append(file)
                    await ctx.send(file=discord.File(filepath + file))
                else:
                    detected = True
            if detected is True:
                await ctx.send(f"Duplicate removed resulting in less than {amount} files.")
            else:
                await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.guild_only()
    async def submit(self, ctx):
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith((".pk6", ".pk7", ".pk8", ".pb7", ".pb8", ".eb8")):
                await attachment.save("Files/submitted/"+attachment.filename)
                await ctx.channel.send("File has been submitted for review. Thank you for your contribution.")
            else:
                await ctx.channel.send("An error occurred with this file. Please submit only .pk6, .pk7, and .pk8 files.")


def setup(client):
    client.add_cog(PKHeX(client))