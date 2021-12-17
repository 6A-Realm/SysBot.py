# Easiest way for me to do this in one sitting was to make it one long file

# Packages, yay
import discord
from discord.ext import commands, tasks
from discord.utils import get
from rich import style
from yaml import load, dump
from rich.console import Console
import socket
import random
import os
import datetime
import binascii
import asyncio
import pyautogui
import typing
import io
import base64
import aiohttp
import numpy as np

console = Console()
queue = []

# Loads switch ip and port from config file
with open("config.yaml") as file:
    data = load(file)
    switchip = data["ip"]
    switchport = data["port"]
    dir = data["directory"]

# Simple file reader to load advanced settings
with open("advanced/blacklist.yaml", encoding='utf-8') as file:
    data = load(file)
    userblacklist = data["userblacklist"]

with open("advanced/logs.yaml", encoding='utf-8') as file:
    data = load(file)
    log = data["log"]

with open("advanced/priority.yaml", encoding='utf-8') as file:
    data = load(file)
    priority = data["priority"]

with open("advanced/sudo.yaml", encoding='utf-8') as file:
    data = load(file)
    sudo = data["sudo"]

# sys-botbase to send commands
def switch(serv, content):
    content += '\r\n'
    serv.sendall(content.encode())

# IP/Port connection to switch (same thing you would put in sysbot)
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.settimeout(15)
try:
    serv.connect((switchip, switchport))
    console.print(f"Successfully connected to {switchip}:{switchport}.", style="green")
    switch(serv, "screenOff")
    console.print("Switch screen was turned off.", style="green")
except socket.error:
    console.print(f"Unable to connect to {switchip}:{switchport}.", style="red")
    console.print(f"\nClick here to follow the connection troubleshooting guide by the official sysbot team.\nhttps://github.com/kwsch/SysBot.NET/wiki/Troubleshooting-Connection-Errors)\nAlternatively, you can use this bot without a switch by deleting the cogs/bdsp.py file.")

# Title IDs
p = "010003F003A34000"
e = "0100187003A36000"
sw = "0100ABF008968000"
sh = "01008DB008C2C000"
bd = "0100000011D90000"
sp = "010018E011D92000"

# Cog 
class bdsp(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.trader.start()

# Sysbot.py
    @tasks.loop()
    async def trader(self):
        await self.client.wait_until_ready()
        if len(queue) > 0:
            user = queue[0]
            queued = get(self.client.get_all_members(), id=user)
            if queued == None:
                while (True):
                    switch(serv, "click B")
                    await asyncio.sleep(60)
            if queued != None:
                switch(serv, "getTitleID")
                title = serv.recv(689)
                title = title[0:-1]
                title = str(title,'utf-8')
                if title == "0100000011D90000" or "010018E011D92000":
                    await queued.send("Hello! Please prepare yourself, your trade is about to begin.")
                    # Injection
                    filepath1 = f'Files/sysbot/requested-{user}.eb8'
                    injector = open(filepath1, "rb")
                    injection = injector.read(344)
                    injection = str(binascii.hexlify(injection), "utf-8")

                    # This is the part I need that way I can read the file and inject it into box 1 slot 1
                    switch(serv, f"pointerPoke 0x{injection} 0x4E34DD0 0xB8 0x10 0xA0 0x20 0x20 0x20")

                    # Opening trade menu to internet
                    console.log(f"Opening the trade menu. Queuing: {user}.", style="green")
                    switch(serv, "click Y")
                    await asyncio.sleep(1)
                    switch(serv, "setStick RIGHT 0x7FFF 0x0")
                    switch(serv, "setStick RIGHT 0x0 0x0")
                    await asyncio.sleep(1)
                    for x in range(3):
                        switch(serv, "click A")
                        await asyncio.sleep(1)
                    switch(serv, "setStick RIGHT yVal -0x8000")
                    switch(serv, "setStick RIGHT yVal 0x0000")
                    await asyncio.sleep(1)
                    switch(serv, "setStick RIGHT yVal -0x8000")
                    switch(serv, "setStick RIGHT yVal 0x0000")
                    await asyncio.sleep(1)
                    for x in range(5):
                        switch(serv, "click A")
                        await asyncio.sleep(1)

                    # Trade code generator || There is probably a more efficent way
                    console.print("Generating 8 digit code.", style="red")
                    tradecode = []
                    for i in range(8): 
                        code = random.randint(0,8) 
                        tradecode.append(str(code))
                        if code == 1:
                            switch(serv, "click A")
                            await asyncio.sleep(3)
                        if code == 2:
                            switch(serv, "setStick RIGHT 0x7FFF 0x0")
                            switch(serv, "setStick RIGHT 0x0 0x0")
                            await asyncio.sleep(3)
                            switch(serv, "click A")
                            await asyncio.sleep(3)
                            switch(serv, "setStick RIGHT -0x8000 0x0")
                            switch(serv, "setStick RIGHT 0x0 0x0")
                            await asyncio.sleep(3)
                        if code == 3:
                            for x in range(2):
                                switch(serv, "setStick RIGHT 0x7FFF 0x0")
                                switch(serv, "setStick RIGHT 0x0 0x0")
                                await asyncio.sleep(3)
                            switch(serv, "click A")
                            await asyncio.sleep(3)
                            for x in range(2):
                                switch(serv, "setStick RIGHT -0x8000 0x0")
                                switch(serv, "setStick RIGHT 0x0 0x0")
                                await asyncio.sleep(3)
                        if code == 4:
                            switch(serv, "setStick RIGHT yVal -0x8000")
                            switch(serv, "setStick RIGHT yVal 0x0000")
                            await asyncio.sleep(3)                           
                            switch(serv, "click A")
                            await asyncio.sleep(3)     
                            switch(serv, "setStick RIGHT yVal 0x7FFF")
                            switch(serv, "setStick RIGHT yVal 0x0000")
                            await asyncio.sleep(3)
                        if code == 5:
                            switch(serv, "setStick RIGHT yVal -0x8000")
                            switch(serv, "setStick RIGHT yVal 0x0000")
                            await asyncio.sleep(3)  
                            switch(serv, "setStick RIGHT 0x7FFF 0x0")
                            switch(serv, "setStick RIGHT 0x0 0x0")
                            await asyncio.sleep(3)
                            switch(serv, "click A")
                            await asyncio.sleep(3)
                            switch(serv, "setStick RIGHT -0x8000 0x0")
                            switch(serv, "setStick RIGHT 0x0 0x0")
                            await asyncio.sleep(3)
                            switch(serv, "setStick RIGHT yVal 0x7FFF")
                            switch(serv, "setStick RIGHT yVal 0x0000")
                            await asyncio.sleep(3)
                        if code == 6:
                            switch(serv, "setStick RIGHT yVal -0x8000")
                            switch(serv, "setStick RIGHT yVal 0x0000")
                            await asyncio.sleep(3)  
                            for x in range(2):
                                switch(serv, "setStick RIGHT 0x7FFF 0x0")
                                switch(serv, "setStick RIGHT 0x0 0x0")
                                await asyncio.sleep(3)
                            switch(serv, "click A")
                            await asyncio.sleep(3)
                            for x in range(2):
                                switch(serv, "setStick RIGHT -0x8000 0x0")
                                switch(serv, "setStick RIGHT 0x0 0x0")
                                await asyncio.sleep(3) 
                            switch(serv, "setStick RIGHT yVal 0x7FFF")
                            switch(serv, "setStick RIGHT yVal 0x0000")
                            await asyncio.sleep(3)  
                        if code == 7:
                            for x in range(2):
                                switch(serv, "setStick RIGHT yVal -0x8000")
                                switch(serv, "setStick RIGHT yVal 0x0000")
                                await asyncio.sleep(3)                           
                            switch(serv, "click A")
                            await asyncio.sleep(3)   
                            for x in range(2):
                                switch(serv, "setStick RIGHT yVal 0x7FFF")
                                switch(serv, "setStick RIGHT yVal 0x0000")
                                await asyncio.sleep(3)
                        if code == 8:
                            for x in range(2):
                                switch(serv, "setStick RIGHT yVal -0x8000")
                                switch(serv, "setStick RIGHT yVal 0x0000")
                                await asyncio.sleep(3)  
                            switch(serv, "setStick RIGHT 0x7FFF 0x0")
                            switch(serv, "setStick RIGHT 0x0 0x0")
                            await asyncio.sleep(3)
                            switch(serv, "click A")
                            await asyncio.sleep(3)
                            switch(serv, "setStick RIGHT -0x8000 0x0")
                            switch(serv, "setStick RIGHT 0x0 0x0")
                            await asyncio.sleep(3)
                            for x in range(2):
                                switch(serv, "setStick RIGHT yVal 0x7FFF")
                                switch(serv, "setStick RIGHT yVal 0x0000")
                                await asyncio.sleep(3)
                        if code == 9:
                            for x in range(2):
                                switch(serv, "setStick RIGHT yVal -0x8000")
                                switch(serv, "setStick RIGHT yVal 0x0000")
                                await asyncio.sleep(3)  
                            for x in range(2):
                                switch(serv, "setStick RIGHT 0x7FFF 0x0")
                                switch(serv, "setStick RIGHT 0x0 0x0")
                                await asyncio.sleep(3)
                            switch(serv, "click A")
                            await asyncio.sleep(3)
                            for x in range(2):
                                switch(serv, "setStick RIGHT -0x8000 0x0")
                                switch(serv, "setStick RIGHT 0x0 0x0")
                                await asyncio.sleep(3) 
                            for x in range(2):
                                switch(serv, "setStick RIGHT yVal 0x7FFF")
                                switch(serv, "setStick RIGHT yVal 0x0000")
                                await asyncio.sleep(3)  
                        if code == 0:
                            switch(serv, "setStick RIGHT 0x7FFF 0x0")
                            switch(serv, "setStick RIGHT 0x0 0x0")
                            await asyncio.sleep(1)
                            for x in range(3):
                                switch(serv, "setStick RIGHT yVal -0x8000")
                                switch(serv, "setStick RIGHT yVal 0x0000")
                                await asyncio.sleep(3) 
                            switch(serv, "click A") 
                            for x in range(3):
                                switch(serv, "setStick RIGHT yVal 0x7FFF")
                                switch(serv, "setStick RIGHT yVal 0x0000")
                                await asyncio.sleep(3)  
                            switch(serv, "setStick RIGHT -0x8000 0x0")
                            switch(serv, "setStick RIGHT 0x0 0x0")
                            await asyncio.sleep(3) 

                    tradecode.insert(4, '-')
                    await queued.send(f'Your trade code is: `{"".join(ch for ch in tradecode)}`.')
                    console.print(f'Searching on code: {"".join(ch for ch in tradecode)}.', style="bold underline purple")
                    await asyncio.sleep(0.2)
                    await queued.send("I am searching...")
                    await asyncio.sleep(0.5)

                    # Searching
                    switch(serv, "click PLUS")
                    await asyncio.sleep(1)
                    switch(serv, "click A")
                    await asyncio.sleep(30)
                    switch(serv, "click Y")
                    await asyncio.sleep(1)
                    switch(serv, "click A")
                    await asyncio.sleep(1)
                    switch(serv, "setStick RIGHT yVal -0x8000")
                    switch(serv, "setStick RIGHT yVal 0x0000")
                    await asyncio.sleep(1)
                    switch(serv, "click A")
                    await asyncio.sleep(30)

                    # Assuming dude actually connects to the bot > initialize trade
                    console.print("Trade initalizing assuming connection was made.", style="yellow")
                    for x in range(6):
                        switch(serv, "click A")
                        await asyncio.sleep(3)
                    switch(serv, "click A")

                    # Increased for trade scene
                    # Make sure you have your pokedex completed.
                    await asyncio.sleep(60)

                    # Add "Here is what you traded me:" here
                    del queue[0]
                    console.print(f'Trade completed with {queued}.', style="green")

                    ## https://github.com/architdate/PKHeX-Plugins/blob/dff2ba71603c6e19d75a12dab94f50f5b2ef8402/PKHeX.Core.Injection/LiveHeXOffsets/RamOffsets.cs#L155
                    ## LiveHeXVersion.BD_v111 => ("[[[[main+4C1DCF8]+B8]+10]+A0]+20", 40),
                    ## Conversion "pointerPeek 0x4C1DCF8 0xB8 0x10 0xA0 0x20" 
                    # Thank you Manu for teaching me
                    switch(serv, "pointerPeek 344 0x4E34DD0 0xB8 0x10 0xA0 0x20 0x20 0x20")
                    await asyncio.sleep(1)
                    read = serv.recv(689)
                    read = read[0:-1]
                    filepath2 = f'Files/sysbot/traded-{queued}.eb8'
                    fileOut = open(filepath2, "wb")
                    fileOut.write(binascii.unhexlify(read))
                    fileOut.close()
                    await asyncio.sleep(0.5)
                    with open(filepath1, 'rb') as f, open(filepath2, 'rb') as f2:
                        if f == f2:
                            await queued.send("Failed to connect and trade with user.")
                        else:
                            file = discord.File(filepath2)
                            await queued.send(file=file, content="Here is what you traded to me:")

                    # Backing out to over world
                    console.print("Existing back to the overworld.", style="red")
                    switch(serv, "click B")
                    await asyncio.sleep(1)
                    switch(serv, "setStick RIGHT yVal 0x7FFF")
                    switch(serv, "setStick RIGHT yVal 0x0000")
                    await asyncio.sleep(1)
                    for x in range(2):
                        switch(serv, "click A")
                        await asyncio.sleep(2)
                    switch(serv, "click Y")
                    await asyncio.sleep(2)
                    switch(serv, "setStick RIGHT yVal -0x8000")
                    switch(serv, "setStick RIGHT yVal 0x0000")
                    await asyncio.sleep(2)
                    switch(serv, "click A")
                    console.print("Awaiting new users...", style="bold underline white")
                    logger = open("logs.txt", "a")
                    logtime = datetime.datetime.now()
                    logger.write(logtime + " || " + {queued} + " has traded with the bot" + "\n")
                    logger.close()

                if title == "010003F003A34000" or "0100187003A36000":
                    await queued.send("SysBot.py is not made for LGPE yet.")
                    del queue[0]

                if title == "0100ABF008968000" or "01008DB008C2C000":
                    await queued.send("SysBot.py is not made for SWSH yet.")
                    del queue[0]


# {-- Queue Module --}
    @commands.command()
    @commands.guild_only()
    async def testtradetest(self, ctx):
        if ctx.message.author.id in userblacklist:
            await ctx.send("User is blacklisted from using the bot.")
            if ctx.message.author.id in queue:
                await ctx.send("You are already in queue.")
            
            else:
                switch(serv, "getTitleID")
                title = serv.recv(689)
                title = title[0:-1]
                title = str(title,'utf-8')
                if title == "0100000011D90000" or "010018E011D92000":
                    for attachment in ctx.message.attachments:

                        if attachment.filename.endswith((".eb8")):

                            # Legality check by GriffinG1: https://github.com/GriffinG1/FlagBot/blob/22da7ae04e5f5383eb23b7aa75cc9fab7d90b355/addons/pkhex.py#L221
                            #r = await self.process_file(ctx, ctx.message.attachments, "api/bot/check")
                            #if r == 400:
                            #    return
                            #rj = r[1]
                            #reasons = rj["IllegalReasons"].split("\n")
                            #if reasons[0] == "Legal!":

                                # Logs in console
                                os.system('cls||clear')
                                await attachment.save(f"Files/sysbot/requested-{ctx.message.author.id}.eb8")
                                prioritycheck = discord.utils.find(lambda r: r.id == priority, ctx.message.guild.roles)
                                if prioritycheck in ctx.message.author.roles:
                                    queue.insert(0, ctx.message.author.id)
                                else:
                                    queue.append(ctx.message.author.id)
                                console.log(f'{ctx.message.author.name} has been added to the queue', style="blue")
                                await ctx.message.delete()
                                await ctx.send(f'{ctx.message.author.name} has been added to the queue. Current queue length: {len(queue)}.')
                                logger = open("logs.txt", "a")
                                logtime = datetime.datetime.now()
                                logger.write(logtime + " || " + {ctx.message.author.name} + " has requested to trade with the bot" + "\n")
                                logger.close()

                            #else:
                                #embed = discord.Embed(title="Your pokemon was illegal", description="", colour=discord.Colour.red())
                                #embed = self.list_to_embed(embed, reasons)
                                #await ctx.send(embed=embed)

                        else:
                            await ctx.channel.send("Unable to trade. Ensure your file ends in `.eb8` and is legal.")
                if title == "010003F003A34000" or "0100187003A36000":
                    await ctx.send("SysBot.py is not made for LGPE yet.")
                    del queue[0]

                if title == "0100ABF008968000" or "01008DB008C2C000":
                    await ctx.send("SysBot.py is not made for SWSH yet.")
                    del queue[0]
                else:
                    pass

    @commands.group(invoke_without_command=True)
    async def queue(self, ctx):
        if ctx.message.author.id in queue:
            person = ctx.message.author.id
            position = queue.index(person) + 1
            await ctx.send(f"Your current position is {position}")
        else:
            await ctx.send("You are not in queue.")

    @queue.group()
    async def list(self, ctx):
        list = []
        enter = '\n'
        counter = 0
        for x in queue:
            user = self.client.get_user(x.id)
            counter += 1
            list.append(f"{counter}) {user.name}")
        embed = discord.Embed(title="Queue List", description=f"{enter.join(y for y in list)}", colour=discord.Colour.blurple())
        await ctx.send(embed = embed)

    @queue.group()
    async def leave(self, ctx):
        if ctx.message.author.id in queue:
            person = ctx.message.author.id
            position = queue.index(person)
            if position > 0:
                ctx.send("Cannot remove you from the queue, currently being processed.")            
            else:
                person = ctx.message.author.id
                queue.remove(person)
                await ctx.send("Removed from queue.")
        else:
            ctx.send("You are not in queue.")

        embed = discord.Embed(title="Queue List", description=f"", colour=discord.Colour.blurple())
        await ctx.send(embed = embed)

    @queue.group()
    @commands.is_owner()
    async def remove(self, ctx, user: discord.User):
        person = user.id
        name = user.name
        if person in queue:
            queue.remove(person)
            await ctx.send(f"{name} was removed from the queue.")
        else:
            await ctx.send(f"{name} is not in queue.")

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

    @commands.command()
    @commands.is_owner()
    async def pixelPeek(self, ctx):
        switch(serv, "pixelPeek")
        await asyncio.sleep(1)
        peek = serv.recv(1024)
        peek = peek[0:-1]
        peek = str(peek,'utf-8')       
        image = open("res/screen.jpg", "wb")
        image.write(base64.b64decode(peek))
        image.close()
        embed = discord.Embed(color=0xFFD700)
        image = discord.File("res/screen.jpg", filename="screen.jpg")
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
    client.add_cog(bdsp(client))