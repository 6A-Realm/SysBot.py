from pokemon.connection import switch, serv
from pokemon.titles import bd, sp
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
# {-- Select/Menu Buttons --}
    @commands.group(invoke_without_command=True)
    @lock()
    async def click(self, ctx):
        embed=discord.Embed(title="Nintendo Switch Manual Control", description="Bot owners and sudo members can remote control their connected Nintendo Switch on {switchip}:{switchport} using the following commands.", color=0x17c70a)
        embed.add_field(name="Select Buttons:", value="`x, a, b, y`", inline=False)
        embed.add_field(name="Directional Buttons:", value="`up, right, down, left`", inline=False)
        embed.add_field(name="Other Commands:", value="`inject, dump, home, plus min`", inline=False)
        embed.set_footer(text="Minus does not work for LGPE.")
        await ctx.send(embed=embed)

    @click.group()
    @lock()
    async def x(self, ctx):
        switch(serv, "click X")
        await protocol(ctx)

    @click.group()
    @lock()
    async def a(self, ctx):
        switch(serv, "click A")
        await protocol(ctx)

    @click.group()
    @lock()
    async def b(self, ctx):
        switch(serv, "click B")
        await protocol(ctx)

    @click.group()
    @lock()
    async def spamb(self, ctx):
        for x in range(15):
            switch(serv, "click B")
            await asyncio.sleep(0.5)
        await protocol(ctx)

    @click.group()
    @lock()
    async def y(self, ctx):
        switch(serv, "click Y")
        await protocol(ctx)

# {-- Direction Buttons --}
    @click.group()
    @lock()
    async def up(self, ctx):
        switch(serv, "setStick RIGHT yVal 0x7FFF")
        switch(serv, "setStick RIGHT yVal 0x0000")
        await protocol(ctx)

    @click.group()
    @lock()
    async def right(self, ctx):
        switch(serv, "setStick RIGHT 0x7FFF 0x0")
        switch(serv, "setStick RIGHT 0x0 0x0")
        await protocol(ctx)

    @click.group()
    @lock()
    async def down(self, ctx):
        switch(serv, "setStick RIGHT yVal -0x8000")
        switch(serv, "setStick RIGHT yVal 0x0000")
        await protocol(ctx)

    @click.group()
    @lock()
    async def left(self, ctx):
        switch(serv, "setStick RIGHT -0x8000 0x0")
        switch(serv, "setStick RIGHT 0x0 0x0")
        await protocol(ctx)

# {-- Other Buttons --}
    @click.group()
    @lock()
    async def plus(self, ctx):
        switch(serv, "click PLUS")
        await protocol(ctx)

    @click.group()
    @lock()
    async def minus(self, ctx):
        switch(serv, "click MINUS")
        await protocol(ctx)

    @click.group()
    @lock()
    async def home(self, ctx):
        switch(serv, "click HOME")
        await protocol(ctx)


# { -- Sysbot commands --}
    @commands.group(invoke_without_command=True)
    @lock()
    async def pokemon(self, ctx):
        await ctx.reply("Inject or dump pokemon into your game.")

    @pokemon.group()
    @lock()
    async def inject(self, ctx):
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

    @pokemon.group()
    @lock()
    async def dump(self, ctx):
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

# {-- Screen Settings --}
    @commands.group(invoke_without_command=True)
    @lock()
    async def screen(self, ctx):
        embed=discord.Embed(title="Nintendo Switch Manual Screen Control", description="Bot owners and sudo members can control their connected Nintendo Switch screen on {switchip}:{switchport} using the following commands.", color=0x17c70a)
        embed.add_field(name="Screen Commands:", value="`on, off, shot, capture, percent`", inline=False)
        embed.set_footer(text="Capture does not work for LGPE.")
        await ctx.send(embed=embed)

    @screen.group()
    @lock()
    async def off(self, ctx):
        switch(serv, "screenOff")
        await ctx.send("Your switch screen was turned off.")

    @screen.group()
    @lock()
    async def on(self, ctx):
        switch(serv, "screenOn")
        await ctx.send("Your switch screen was turned on.")

    @screen.group()
    @lock()
    async def shot(self, ctx):  
        await protocol(ctx)

    @screen.group() ##Doesnt work for LGPE
    @lock()
    async def capture(self, ctx): 
        switch(serv, "click CAPTURE")

    @screen.group()
    @lock()
    async def percent(self, ctx): 
        switch(serv, "charge")
        await asyncio.sleep(1)
        charge = serv.recv(689)
        charge = charge[0:-1]
        charge = str(charge,'utf-8')
        await ctx.send(f"{switchip}'s battery level is at {charge}%.")

# {-- Extra --}
    @commands.command()
    @lock()
    async def detach(self, ctx):
        switch(serv, "detachController")
        await ctx.send("Your controller was detached.")

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