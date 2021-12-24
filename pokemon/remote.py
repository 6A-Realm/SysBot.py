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

with open("advanced/sudo.yaml") as file:
    data = load(file)
    sudo = data["sudo"]

# Cog 
class remote(commands.Cog):
    def __init__(self, client):
        self.client = client


# {-- Remote Control --}
# {-- Select/Menu Buttons --}
    @commands.group(invoke_without_command=True)
    async def click(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            embed=discord.Embed(title="Nintendo Switch Manual Control", description="Bot owners and sudo members can remote control their connected Nintendo Switch on {switchip}:{switchport} using the following commands.", color=0x17c70a)
            embed.add_field(name="Select Buttons:", value="`x, a, b, y`", inline=False)
            embed.add_field(name="Directional Buttons:", value="`up, right, down, left`", inline=False)
            embed.add_field(name="Other Commands:", value="`inject, dump, home, plus min`", inline=False)
            embed.set_footer(text="Minus does not work for LGPE.")
            await ctx.send(embed=embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

    @click.group()
    async def x(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "click X")
            await asyncio.sleep(1)
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file=image, embed=embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

    @click.group()
    async def a(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "click A")
            await asyncio.sleep(1)
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file=image, embed=embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

    @click.group()
    async def b(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "click B")
            await asyncio.sleep(1)
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file=image, embed=embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

    @click.group()
    async def y(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "click Y")
            await asyncio.sleep(1)
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file=image, embed=embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

# {-- Direction Buttons --}
    @click.group()
    async def up(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "setStick RIGHT yVal 0x7FFF")
            switch(serv, "setStick RIGHT yVal 0x0000")
            await asyncio.sleep(1)
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file=image, embed=embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

    @click.group()
    async def right(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "setStick RIGHT 0x7FFF 0x0")
            switch(serv, "setStick RIGHT 0x0 0x0")
            await asyncio.sleep(1)
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file=image, embed=embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

    @click.group()
    async def down(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "setStick RIGHT yVal -0x8000")
            switch(serv, "setStick RIGHT yVal 0x0000")
            await asyncio.sleep(1)
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file=image, embed=embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

    @click.group()
    async def left(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "setStick RIGHT -0x8000 0x0")
            switch(serv, "setStick RIGHT 0x0 0x0")
            await asyncio.sleep(1)
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file=image, embed=embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

# {-- Other Buttons --}
    @click.group()
    async def plus(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "click PLUS")
            await asyncio.sleep(1)
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file=image, embed=embed)    
        else: 
            await ctx.send("You do not have permission to use this command.")

    @click.group()
    async def minus(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "click MINUS")
            await asyncio.sleep(1)
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file=image, embed=embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

    @click.group()
    async def home(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "click HOME")
            await asyncio.sleep(1)
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file = image, embed = embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

# { -- Sysbot commands --}
    @click.group()
    async def inject(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
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
        else: 
            await ctx.send("You do not have permission to use this command.")

    @click.group()
    async def dump(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
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
            await ctx.send("You do not have permission to use this command.")

# {-- Screen Settings --}
    @commands.group(invoke_without_command=True)
    async def screen(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            embed=discord.Embed(title="Nintendo Switch Manual Screen Control", description="Bot owners and sudo members can control their connected Nintendo Switch screen on {switchip}:{switchport} using the following commands.", color=0x17c70a)
            embed.add_field(name="Screen Commands:", value="`on, off, shot, capture, percent`", inline=False)
            embed.set_footer(text="Capture does not work for LGPE.")
            await ctx.send(embed=embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

    @screen.group()
    async def off(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "screenOff")
            await ctx.send("Your switch screen was turned off.")
        else: 
            await ctx.send("You do not have permission to use this command.")

    @screen.group()
    async def on(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "screenOn")
            await ctx.send("Your switch screen was turned on.")
        else: 
            await ctx.send("You do not have permission to use this command.")

    @screen.group()
    async def shot(self, ctx):  
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:          
            screen = pyautogui.screenshot()
            screen.save(dir)
            embed = discord.Embed(color=0xFFD700)
            image = discord.File("res/screen.jpg", filename="screen.jpg")
            embed.set_image(url="attachment://screen.jpg")
            await ctx.send(file = image, embed = embed)
        else: 
            await ctx.send("You do not have permission to use this command.")

    @screen.group() ##Doesnt work for LGPE
    async def capture(self, ctx): 
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "click CAPTURE")
        else: 
            await ctx.send("You do not have permission to use this command.")

    @screen.group()
    async def percent(self, ctx): 
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "charge")
            await asyncio.sleep(1)
            charge = serv.recv(689)
            charge = charge[0:-1]
            charge = str(charge,'utf-8')
            await ctx.send(f"{switchip}'s battery level is at {charge}%.")
        else: 
            await ctx.send("You do not have permission to use this command.")

# {-- Extra --}
    @commands.command()
    async def detach(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "detachController")
            await ctx.send("Your controller was detached.")
        else: 
            await ctx.send("You do not have permission to use this command.")

## IMaker
    @commands.command()
    async def pixelPeek(self, ctx):
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
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
        else: 
            await ctx.send("You do not have permission to use this command.")

    @commands.command()
    async def titleid(self, ctx): 
        information = await self.client.application_info()
        if ctx.message.author == information.owner or ctx.message.author.id in sudo:
            switch(serv, "getTitleID")
            title = serv.recv(689)
            title = title[0:-1]
            title = str(title,'utf-8')
            await ctx.send(title)
        else: 
            await ctx.send("You do not have permission to use this command.")


def setup(client):
    client.add_cog(remote(client))