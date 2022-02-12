import pokemon.connection.wireless as sysbot
import random 
import asyncio
from rich.console import Console
console = Console()

# 8 digit code generator for num pad
async def numpadcode(self, queued):

    console.print("Generating 8 digit code.", style="red")

    # New connection 
    connection = sysbot.connection(self.client)
    await connection.connect()

    # Using touch to input 8 digit code more accurately
    tradecode = []
    for c in range(8): 
        code = random.randint(0,8)
        tradecode.append(str(code))
        if code in [1, 4, 7]:
            X = 500
        if code in [2, 5, 8, 0]:
            X = 700
        if code in [3, 6, 9]:
            X = 800
        if code in [1, 2, 3]:
            Y = 450
        if code in [4, 5, 6]:
            Y = 500
        if code in [7, 8, 9]:
            Y = 550
        if (code == 0):
            Y = 600
        await connection.switch(f"touch {X} {Y}")
        await asyncio.sleep(0.5)

    tradecode.insert(4, '-')
    await queued.send(f'Your trade code is: `{"".join(tradecode)}`.')
    console.print(f'Searching on code: {"".join(tradecode)}.', style="bold underline purple")
    await asyncio.sleep(0.2)
    await queued.send("I am searching...")
    await asyncio.sleep(0.5)

# Check code length
async def check(distributioncode):
    counter = 0
    for d in distributioncode:
        counter += 1
    if counter > 8:
        console.print("Code must be an 8 digit or less numerical code.", style="red")
        return

# Fixed code input
distributioncode = "000000"
async def fixedcode(self):

    if distributioncode.isdigit():

        await check(distributioncode)

        # New connection 
        connection = sysbot.connection(self.client)
        await connection.connect()

        console.print("Inputting code.", style="red")

        # Using touch to input 8 digit code more accurately
        for d in distributioncode: 
            if d in [1, 4, 7]:
                X = 500
            if d in [2, 5, 8, 0]:
                X = 700
            if d in [3, 6, 9]:
                X = 800
            if d in [1, 2, 3]:
                Y = 450
            if d in [4, 5, 6]:
                Y = 500
            if d in [7, 8, 9]:
                Y = 550
            if (d == 0):
                Y = 600
            await connection.switch(f"touch {X} {Y}")
            await asyncio.sleep(0.5)

        console.print(f'Searching on code: {distributioncode}.', style="bold underline purple")
        await asyncio.sleep(0.5)
    
    else:
        console.print("Code must be a numerical code.", style="red")
        return