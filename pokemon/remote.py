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

# Cog 
class remote(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Remote Control --}
# {-- Select/Menu Buttons --}
    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def click(self, ctx):
        click = discord.Embed(title="Nintendo Switch Manual Control", description=f"Bot owners can control their connected Nintendo Switch on {switchip}:{switchport} using the following commands.", colour=discord.Colour.yellow())
        click.add_field(name = "`Select Buttons:`", value = "x, a, b, y")
        click.add_field(name = "`Directional Buttons:`", value = "up, right, down, left")
        click.add_field(name = "`Select Buttons:`", value = "x, a, b, y")
        click.add_field(name = "`Switch Commands:`", value = "inject, dump")
        click.add_field(name = "`Select Buttons:`", value = "x, a, b, y")
        click.add_field(name = "`Other Commands:`", value = "home, plus, minus")
        click.set_footer(text="Minus does not work for LGPE.")
        await ctx.send(embed = click)

    @click.group()
    @commands.is_owner()
    async def x(self, ctx):
        switch(serv, "click X")
        await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file=image, embed=embed)

    @click.group()
    @commands.is_owner()
    async def a(self, ctx):
        switch(serv, "click A")
        await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file=image, embed=embed)

    @click.group()
    @commands.is_owner()
    async def b(self, ctx, amount: typing.Optional[int] = 1):
        for x in range(0, amount):
            switch(serv, "click B")
            await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file=image, embed=embed)

    @click.group()
    @commands.is_owner()
    async def y(self, ctx):
        switch(serv, "click Y")
        await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file=image, embed=embed)

# {-- Direction Buttons --}
    @click.group()
    @commands.is_owner()
    async def up(self, ctx):
        switch(serv, "setStick RIGHT yVal 0x7FFF")
        switch(serv, "setStick RIGHT yVal 0x0000")
        await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file=image, embed=embed)

    @click.group()
    @commands.is_owner()
    async def right(self, ctx):
        switch(serv, "setStick RIGHT 0x7FFF 0x0")
        switch(serv, "setStick RIGHT 0x0 0x0")
        await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file=image, embed=embed)

    @click.group()
    @commands.is_owner()
    async def down(self, ctx):
        switch(serv, "setStick RIGHT yVal -0x8000")
        switch(serv, "setStick RIGHT yVal 0x0000")
        await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file=image, embed=embed)

    @click.group()
    @commands.is_owner()
    async def left(self, ctx):
        switch(serv, "setStick RIGHT -0x8000 0x0")
        switch(serv, "setStick RIGHT 0x0 0x0")
        await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file=image, embed=embed)

# {-- Other Buttons --}
    @click.group()
    @commands.is_owner()
    async def plus(self, ctx):
        switch(serv, "click PLUS")
        await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file=image, embed=embed)    
        
    @click.group()
    @commands.is_owner()
    async def minus(self, ctx):
        switch(serv, "click MINUS")
        await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file=image, embed=embed)

    @click.group()
    @commands.is_owner()
    async def home(self, ctx):
        switch(serv, "click HOME")
        await asyncio.sleep(1)
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file = image, embed = embed)

# { -- Sysbot commands --}
    @click.group()
    @commands.is_owner()
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

    @click.group()
    @commands.is_owner()
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
    @commands.is_owner()
    async def screen(self, ctx):
        screen = discord.Embed(title="Nintendo Switch Manual Screen Control", description=f"Bot owners can control their connected Nintendo Switch on {switchip}:{switchport} using the following commands.", colour=discord.Colour.yellow())
        screen.add_field(name = "`Screen Commands:`", value = "on, off, shot, capture, percent")
        screen.set_footer(text="Capture does not work for LGPE.")
        await ctx.send(embed = screen)

    @screen.group()
    @commands.is_owner()
    async def off(self, ctx):
        switch(serv, "screenOff")
        await ctx.send("Your switch screen was turned off.")

    @screen.group()
    @commands.is_owner()
    async def on(self, ctx):
        switch(serv, "screenOn")
        await ctx.send("Your switch screen was turned on.")

    @screen.group()
    async def shot(self, ctx):            
        screen = pyautogui.screenshot()
        screen.save(dir)
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file = image, embed = embed)

    @screen.group() ##Doesnt work for LGPE
    @commands.is_owner()
    async def capture(self, ctx): 
        switch(serv, "click CAPTURE")

    @screen.group()
    @commands.is_owner()
    async def percent(self, ctx): 
        switch(serv, "charge")
        await asyncio.sleep(1)
        charge = serv.recv(689)
        charge = charge[0:-1]
        charge = str(charge,'utf-8')
        await ctx.send(f"{switchip}'s battery level is at {charge}%.")

# {-- Extra --}
    @commands.command()
    @commands.is_owner()
    async def detach(self, ctx):
        switch(serv, "detachController")
        await ctx.send("Your controller was detached.")


## IMaker
    @commands.command()
    @commands.is_owner()
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
    @commands.is_owner()
    async def titleid(self, ctx): 
        switch(serv, "getTitleID")
        title = serv.recv(689)
        title = title[0:-1]
        title = str(title,'utf-8')
        await ctx.send(title)


def setup(client):
    client.add_cog(remote(client))