from pokemon.discord.pokeinput import queuelist
from pokemon.connection.wireless import switch, serv
from pokemon.utils.values import getready, failed, success, errormessage, b1s1, p, e, sw, sh, bd, sp
import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import os
import binascii
from rich.console import Console
import random
import string

console = Console()

# Trade loop cog 
class trader(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.trader.start()

# Trade Loop
    @tasks.loop()
    async def trader(self):
        await self.client.wait_until_ready()
        if len(queuelist) > 0:
            user = queuelist[0]
            queued = get(self.client.get_all_members(), id=user)

            # Stay awake protocol
            if queued is None:
                while (True):
                    switch(serv, "click B")
                    await asyncio.sleep(15)

            if queued != None:
                switch(serv, "getTitleID")
                title = serv.recv(689)
                title = title[0:-1]
                title = str(title,'utf-8')
                if title in [bd, sp]:
                    await queued.send(getready)

                    # Injection
                    filepath1 = f'Files/sysbot/requested-{user}.eb8'
                    if os.path.exists(filepath1):
                        injector = open(filepath1, "rb")
                        injection = injector.read(344)
                        injection = str(binascii.hexlify(injection), "utf-8")

                        # Inject into box 1 slot 1
                        for i in range(2):
                            switch(serv, f"pointerPoke 0x{injection} {b1s1}")
                        await asyncio.sleep(0.5)
                        
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
                        await asyncio.sleep(0.5)
                        switch(serv, "setStick RIGHT yVal -0x8000")
                        switch(serv, "setStick RIGHT yVal 0x0000")
                        await asyncio.sleep(0.5)
                        for x in range(10):
                            switch(serv, "click A")
                            await asyncio.sleep(1)
                        await asyncio.sleep(5)

                        # Trade code generator
                        console.print("Generating 8 digit code.", style="red")

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
                            switch(serv, f"touch {X} {Y}")
                            await asyncio.sleep(0.5)

                        tradecode.insert(4, '-')
                        await queued.send(f'Your trade code is: `{"".join(tradecode)}`.')
                        console.print(f'Searching on code: {"".join(tradecode)}.', style="bold underline purple")
                        await asyncio.sleep(0.2)
                        await queued.send("I am searching...")
                        await asyncio.sleep(0.5)

                        # Searching
                        switch(serv, "click PLUS")
                        await asyncio.sleep(1)
                        for x in range(3):
                            switch(serv, "click A")
                            await asyncio.sleep(1)
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
                        await asyncio.sleep(60)

                        # Add "Here is what you traded me:" here
                        del queuelist[0]
                        console.print(f'Backing out to overworld.', style="magenta")
                        ## https://github.com/architdate/PKHeX-Plugins/blob/dff2ba71603c6e19d75a12dab94f50f5b2ef8402/PKHeX.Core.Injection/LiveHeXOffsets/RamOffsets.cs#L155
                        ## LiveHeXVersion.BD_v111 => ("[[[[main+4C1DCF8]+B8]+10]+A0]+20", 40),
                        ## Conversion "pointerPeek 0x4C1DCF8 0xB8 0x10 0xA0 0x20" 
                        switch(serv, f"pointerPeek 344 {b1s1}")
                        await asyncio.sleep(1)
                        read = serv.recv(689)
                        read = read[0:-1]
                        char = "" + ('').join(random.choices(string.ascii_letters + string.digits, k=10))
                        filepath2 = f'Files/dump/{char}.eb8'
                        fileOut = open(filepath2, "wb")
                        fileOut.write(binascii.unhexlify(read))
                        fileOut.close()
                        await asyncio.sleep(0.5)
                        with open(filepath1, 'rb') as f, open(filepath2, 'rb') as f2:
                            if f == f2:
                                console.print(f'Failed to connect to {queued}.')
                                await queued.send(failed)
                            else:
                                file = discord.File(filepath2)
                                await queued.send(file = file, content = success)
                                console.print(f'Trade completed with {queued}.', style="green")
                        os.remove(filepath1)

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
                    else:
                        del queuelist[0]
                        await queued.send(errormessage)


def setup(client):
    client.add_cog(trader(client))