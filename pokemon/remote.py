from pokemon.connection import switch, serv
from pokemon.values import bd, sp
from yaml import load
import discord
from discord.ext import commands
import asyncio
import pyautogui
import typing
import binascii
import PIL.Image as IMaker
import io
import base64

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
async def protocol(ctx):
    if screenshot == True:
        await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file=image, embed=embed)
    else:
        return

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

# {-- Remote Control --}
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
        check = value.upper()
        if (check in singles):
                for x in range(amount):
                    switch(serv, f"click {check}")
                    await asyncio.sleep(1)
                await protocol(ctx)

        elif check == "UP":
            for up in range(amount):
                switch(serv, "setStick RIGHT yVal 0x7FFF")
                switch(serv, "setStick RIGHT yVal 0x0000")
                await asyncio.sleep(1)
            await protocol(ctx)
        elif check == "RIGHT":
            for right in range(amount):
                switch(serv, "setStick RIGHT 0x7FFF 0x0")
                switch(serv, "setStick RIGHT 0x0 0x0")
                await asyncio.sleep(1)
            await protocol(ctx)
        elif check == "DOWN":
            for down in range(amount):
                switch(serv, "setStick RIGHT yVal -0x8000")
                switch(serv, "setStick RIGHT yVal 0x0000")
                await asyncio.sleep(1)
            await protocol(ctx)
        elif check == "LEFT":
            for left in range(amount):
                switch(serv, "setStick RIGHT -0x8000 0x0")
                switch(serv, "setStick RIGHT 0x0 0x0")
            await protocol(ctx)
            
        else:
            await ctx.send(embed=embed)

    @commands.command()
    @lock()
    async def spamb(self, ctx):
        for b in range(15):
            switch(serv, "click B")
            await asyncio.sleep(1)
        await protocol(ctx)

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
        if check == "inject":
            switch(serv, "getTitleID")
            title = serv.recv(689)
            title = title[0:-1]
            title = str(title,'utf-8')
            if title == bd or sp:
                fileIn = open("Files/sysbot/inject.eb8", "rb")
                pokemonToInject = fileIn.read(344)
                pokemonToInject = str(binascii.hexlify(pokemonToInject), "utf-8")
                switch(serv, f"pointerPoke 0x{pokemonToInject} 0x4E34DD0 0xB8 0x10 0xA0 0x20 0x20 0x20")
                await ctx.send("Pokemon injected.")
            else:
                ctx.send("Injection not set up for this game yet.")
        elif check == "dump":
            switch(serv, "getTitleID")
            title = serv.recv(689)
            title = title[0:-1]
            title = str(title,'utf-8')
            if title == bd or sp:
                switch(serv, "pointerPeek 344 0x4E34DD0 0xB8 0x10 0xA0 0x20 0x20 0x20")
                asyncio.sleep(0.5)
                pokemonBytes = serv.recv(689)
                pokemonBytes = pokemonBytes[0:-1]
                fileOut = open("Files/sysbot/dump.eb8", "wb")
                fileOut.write(binascii.unhexlify(pokemonBytes))
                fileOut.close()
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
        if check == "off":
            switch(serv, "screenOff")
            await ctx.send("Your switch screen was turned `off`.")
        elif check == "on":
            switch(serv, "screenOn")
            await ctx.send("Your switch screen was turned `on`.")
        elif check == "delay":
            switch(serv, "screenOn")
            await ctx.send(f"Your switch screen was turned `on`. It will turn off in `{delay}` seconds.")
            await asyncio.sleep(delay)
            switch(serv, "screenOff")
            await ctx.send(f"Your switch screen was turned `off`.")
        elif check == "shot":
            await protocol(ctx)
        elif check == "capture":
            switch(serv, "click CAPTURE")
            embed=discord.Embed(description="Your switch screen was attempted to be captured.", color=0x17c70a)
            embed.set_footer(text="Note that this function does not work for LGPE.")
            await ctx.send(embed=embed)
        elif check == "battery" or check == "percent":
            switch(serv, "charge")
            await asyncio.sleep(1)
            charge = serv.recv(689)
            charge = charge[0:-1]
            charge = str(charge,'utf-8')
            await ctx.send(f"{switchip}'s battery level is at {charge}%.")
        else:
            await ctx.send(embed=embed)

# {-- Controller Settings --}
    @commands.command()
    @lock()
    async def detach(self, ctx):
        switch(serv, "detachController")
        await ctx.send("Your controller was detached.")

    @commands.command()
    @lock()
    async def retach(self, ctx):
        switch(serv, "controllerType 1")        
        await ctx.send("Your controller was retached.")

    @commands.command()
    @lock()
    async def newattach(self, ctx):
        switch(serv, "detachController")
        await asyncio.sleep(0.5)
        switch(serv, "controllerType 1")        
        await ctx.send("Your controller was reset.")

# {-- Other --}
## IMaker
    @commands.command()
    @lock()
    async def pixelPeek(self, ctx):
        switch(serv, "pixelPeek")
        await asyncio.sleep(1)
        peek = serv.recv(1024)
        peek = peek[0:-1]
        print(peek)
        await ctx.send(peek)
        decode = base64.b64decode(peek)
        print(decode)
        image = IMaker.open(io.BytesIO(decode))
        print(image)
        image = image.save("res/screen.jpg")
        embed = discord.Embed(color=0xFFD700)
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file = image, embed = embed)

    @commands.command()
    @lock()
    async def titleid(self, ctx): 
        switch(serv, "getTitleID")
        title = serv.recv(689)
        title = title[0:-1]
        title = str(title,'utf-8')
        await ctx.send(title)

# {--- Reconnect to switch}
    @commands.command()
    @lock()
    async def reconnect(self, ctx):
        self.client.unload_extension("pokemon.connection")
        self.client.load_extension("pokemon.connection")
        await ctx.reply("Attempted to reconnect.")


def setup(client):
    client.add_cog(remote(client))