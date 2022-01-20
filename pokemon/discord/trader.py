from pokemon.discord.pokeinput import queuelist
from pokemon.connection.wireless import switch, serv
from pokemon.utils.values import getready, failed, success, errormessage, b1s1, p, e, sw, sh, bd, sp
from pokemon.utils.tradecode import numpadcode
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
            queued = get(self.client.get_all_members(), id = user)

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

                        # Opening trade menu to internet
                        console.log(f"Opening the trade menu. Queuing: {queued.name}.", style="green")
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
                        await numpadcode(queued)
                        
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
                        await asyncio.sleep(50)

                        # Backing out to over world
                        console.print(f'Backing out to overworld.', style="magenta")
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

                        # "Here is what you traded me:"
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
                        file = discord.File(filepath2)
                        await queued.send(file = file, content = success)
                        console.print(f'Trade completed with {queued}.', style="green")
                        os.remove(filepath1)

                        # End
                        queuelist.remove(user)
                        console.print("Ready for next trade.", style="bold underline white")
                    else:
                        queuelist.remove(user)
                        await queued.send(errormessage)


def setup(client):
    client.add_cog(trader(client))