import pokemon.connection.wireless as sysbot
from pokemon.utils.values import sw, sh, bd, sp, b1s1
from yaml import load
import aiofiles
import discord
from discord.ext import commands
import asyncio
import typing
import binascii

# Loads switch ip and port from config file
with open("config.yaml") as file:
    data = load(file)
    switchip = data["ip"]
    switchport = data["port"]
    dir = data["directory"]
    screenshot = data["system-screenshot"]

with open("advanced/sudo.yaml") as file:
    data = load(file)
    sudo = data["sudo"]

# Screen shot protocol
async def protocol(self, ctx):
    if screenshot != True:
        return
    await asyncio.sleep(0.5)
    connection = sysbot.connection(self.client)
    await connection.connect()
    await connection.switch("pixelPeek")       
    await asyncio.sleep(1)
    screen = binascii.unhexlify((await connection._r.readline())[:-1])
    async with aiofiles.open("res/screen.jpg", "wb") as f:
        await f.write(screen)
    embed = discord.Embed(color=0xFFD700)
    image = discord.File("res/screen.jpg", filename="screen.jpg")
    embed.set_image(url="attachment://screen.jpg")
    await ctx.send(file=image, embed=embed)

# Cog 
class remote(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Owner/Sudo Lock ctx.bot is your commands.Bot instance
    def lock():
        async def check(ctx):
            information = await ctx.bot.application_info()
            return ctx.message.author == information.owner or ctx.message.author.id in sudo
        return commands.check(check)

# {-- Select, Directional, and Menu Buttons --}
    @commands.command()
    @lock()
    async def press(self, ctx, value=None, amount: typing.Optional[int] = 1):
        embed=discord.Embed(title="Nintendo Switch Manual Control", description="Bot owners and sudo members can remote control their connected Nintendo Switch on {switchip}:{switchport} using the following commands.", color=0x17c70a)
        embed.add_field(name="Select Buttons:", value="`x, a, b, y`", inline=False)
        embed.add_field(name="Directional Buttons:", value="`up, right, down, left`", inline=False)
        embed.add_field(name="Other Commands:", value="`inject, dump, home, plus min`", inline=False)
        embed.set_footer(text="Minus does not work for LGPE.")
        if value is None: 
            await ctx.send(embed=embed)

        singles = ["X", "A", "B", "Y", "PLUS", "MINUS", "HOME", "CAPTURE"]
        connection = sysbot.connection(self.client)
        await connection.connect()
        check = value.upper()
        if (check in singles):
                for x in range(amount):
                    await connection.switch(f"click {check}")
                    await asyncio.sleep(0.5)
                await protocol(self, ctx)

        elif check == "UP":
            for up in range(amount):
                await connection.switch("setStick RIGHT yVal 0x7FFF")
                await connection.switch("setStick RIGHT yVal 0x0000")
                await asyncio.sleep(0.5)
            await protocol(self, ctx)
        elif check == "RIGHT":
            for right in range(amount):
                await connection.switch("setStick RIGHT 0x7FFF 0x0")
                await connection.switch("setStick RIGHT 0x0 0x0")
                await asyncio.sleep(0.5)
            await protocol(self, ctx)
        elif check == "DOWN":
            for down in range(amount):
                await connection.switch("setStick RIGHT yVal -0x8000")
                await connection.switch("setStick RIGHT yVal 0x0000")
                await asyncio.sleep(0.5)
            await protocol(self, ctx)
        elif check == "LEFT":
            for left in range(amount):
                await connection.switch("setStick RIGHT -0x8000 0x0")
                await connection.switch("setStick RIGHT 0x0 0x0")
            await protocol(self, ctx)
            
        else:
            await ctx.send(embed=embed)

    @commands.command()
    @lock()
    async def spamb(self, ctx):
        for b in range(15):
            connection = sysbot.connection(self.client)
            await connection.connect()
            await connection.switch("click B")
            await asyncio.sleep(0.5)
        await protocol(self, ctx)

# { -- Pokemon commands --}
    @commands.command()
    @lock()
    async def switch(self, ctx, function=None):
        embed=discord.Embed(title="Pokemon Remote Control", description="Bot owners and sudo members can remote control their connected Nintendo Switch on {switchip}:{switchport} using the following commands.", color=0x17c70a)
        embed.add_field(name="Inject Pokemon:", value="`inject to Files/sysbot/inject.eb8`", inline=False)
        embed.add_field(name="Dump Pokemon:", value="`dump to Files/sysbot/dump.eb8`", inline=False)
        embed.set_footer(text="As of now, these commands only work for BDSP.")
        if function is None:
            await ctx.send(embed=embed)
        check = function.lower()
        connection = sysbot.connection(self.client)
        await connection.connect()
        await connection.switch("getTitleID")
        title = ((await connection._r.read(689))[:-1]).decode("utf-8")
        if check == "inject":
            if title == bd or sp:
                input = open("Files/sysbot/inject.eb8", "rb")
                inject = str(binascii.hexlify(input.read(344)).decode("utf-8"))
                await connection.switch(f"pointerPoke 0x{inject} {b1s1}")
                await ctx.send("Pokemon injected.")
            elif title == sw or sh:
                input = open("Files/sysbot/inject.ek8", "rb")
                inject = str(binascii.hexlify(input.read(344)).decode("utf-8"))
                await connection.switch(f"pointerPoke 0x4293D8B0")
                await ctx.send("Pokemon injected.")
            else:
                ctx.send("Injection not set up for this game yet.")
        elif check == "dump":
            if title == bd or sp:
                await connection.switch(f"pointerPeek 344 {b1s1}")
                pokemon = (await connection._r.read(689))[:-1]
                with open("Files/sysbot/dump.eb8", "wb") as f:
                    f.write(binascii.unhexlify(pokemon))
                await ctx.send("Pokemon dumped.")
            elif title == sw or sh:
                await connection.switch(f"pointerPeek 344 0x4293D8B0")
                pokemon = (await connection._r.read(689))[:-1]
                with open("Files/sysbot/dump.ek8", "wb") as f:
                    f.write(binascii.unhexlify(pokemon))
                await ctx.send("Pokemon dumped.")   
            else:
                ctx.send("Dumping not set up for this game yet.")
        else:
            await ctx.send(embed=embed)

# {-- Screen Settings --}
    @commands.command()
    @lock()
    async def screen(self, ctx, function=None, delay: typing.Optional[int] = 60):
        embed=discord.Embed(title="Nintendo Switch Manual Screen Control", description="Bot owners and sudo members can control their connected Nintendo Switch screen on {switchip}:{switchport} using the following commands.", color=0x17c70a)
        embed.add_field(name="Screen Commands:", value="`on, off, shot, capture, percent`", inline=False)
        embed.set_footer(text="Capture does not work for LGPE.")
        if function is None:
            await ctx.send(embed=embed)
        check = function.lower()
        connection = sysbot.connection(self.client)
        await connection.connect()
        if check == "off":
            await connection.switch("screenOff")
            await ctx.send("Your switch screen was turned `off`.")
        elif check == "on":
            await connection.switch("screenOn")
            await ctx.send("Your switch screen was turned `on`.")
        elif check == "delay":
            await connection.switch("screenOn")
            await ctx.send(f"Your switch screen was turned `on`. It will turn off in `{delay}` seconds.")
            await asyncio.sleep(delay)
            await connection.switch("screenOff")
            await ctx.send(f"Your switch screen was turned `off`.")
        elif check == "shot":
            await protocol(ctx)
        elif check == "capture":
            await connection.switch("click CAPTURE")
            embed=discord.Embed(description="Your switch screen was attempted to be captured.", color=0x17c70a)
            embed.set_footer(text="Note that this function does not work for LGPE.")
            await ctx.send(embed=embed)
        elif check in ["battery", "percent"]:
            await connection.switch("charge")
            charge = ((await connection._r.read(689))[:-1]).decode("utf-8")
            await ctx.send(f"{switchip}'s battery level is at {str(charge)}%.")

        else:
            await ctx.send(embed=embed)

# {-- Other --}
    @commands.command()
    @lock()
    async def newcontroller(self, ctx):
        connection = sysbot.connection(self.client)
        await connection.connect()
        await connection.switch("detachController")
        await asyncio.sleep(0.5)
        await connection.switch("controllerType 1")
        await ctx.send("Your controller was reset.")

    @commands.command()
    async def titleid(self, ctx): 
        connection = sysbot.connection(self.client)
        await connection.connect()
        await connection.switch("getTitleID")
        title = ((await connection._r.read(689))[:-1]).decode("utf-8")
        await ctx.send(title)

    @commands.command()
    async def peek(self, ctx):
        connection = sysbot.connection(self.client)
        await connection.connect()
        await connection.switch("pixelPeek")       
        await asyncio.sleep(1)
        screen = binascii.unhexlify((await connection._r.readline())[:-1])
        async with aiofiles.open("res/screen.jpg", "wb") as f:
            await f.write(screen)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file = image, embed = embed)


def setup(client):
    client.add_cog(remote(client))