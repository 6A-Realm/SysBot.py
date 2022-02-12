from pokemon.discord.pokeinput import queuelist
import pokemon.connection.wireless as sysbot
from pokemon.utils.values import getready, failed, success, errormessage, b1s1, p, e, sw, sh, bd, sp
from pokemon.utils.tradecode import numpadcode
import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import aiofiles
import random
import string
import binascii
from rich.console import Console
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

        # Trade handler
        if len(queuelist) > 0:

            user = list(queuelist.keys())[0]
            queued = get(self.client.get_all_members(), id = user)
            injection = list(queuelist.values())[0]

            if queued != None:

                connection = sysbot.connection(self.client)
                await connection.connect()
                await connection.switch("getTitleID")
                title = ((await connection._r.read(689))[:-1]).decode("utf-8")
                if title in [bd, sp]:
                    msg = await queued.send(getready)

                    # Inject into box 1 slot 1
                    connection = sysbot.connection(self.client)
                    await connection.connect()
                    inject = injection.hex()
                    await connection.switch(f"pointerPoke 0x{inject} {b1s1}")

                    # Opening trade menu to internet
                    console.log(f"Opening the trade menu. Queuing: {queued.name}.", style = "green")
                    await connection.switch("click Y")
                    await asyncio.sleep(1)
                    await connection.switch("setStick RIGHT 0x7FFF 0x0")
                    await connection.switch("setStick RIGHT 0x0 0x0")
                    await asyncio.sleep(1.5)
                    for x in range(3):
                        await connection.switch("click A")
                        await asyncio.sleep(1)
                    await connection.switch("setStick RIGHT yVal -0x8000")
                    await connection.switch("setStick RIGHT yVal 0x0000")
                    await asyncio.sleep(0.5)
                    await connection.switch("setStick RIGHT yVal -0x8000")
                    await connection.switch("setStick RIGHT yVal 0x0000")
                    await asyncio.sleep(0.5)
                    for x in range(10):
                        await connection.switch("click A")
                        await asyncio.sleep(1)
                    await asyncio.sleep(6)

                    # Trade code generator
                    await numpadcode(self, queued)
                    
                    # Searching
                    await connection.switch("click PLUS")
                    await asyncio.sleep(1)
                    for x in range(3):
                        await connection.switch("click A")
                        await asyncio.sleep(1)
                    await asyncio.sleep(10)
                    await connection.switch("click Y")
                    await asyncio.sleep(1)
                    await connection.switch("click A")
                    await asyncio.sleep(1)
                    await connection.switch("setStick RIGHT yVal -0x8000")
                    await connection.switch("setStick RIGHT yVal 0x0000")
                    await asyncio.sleep(0.5)
                    await connection.switch("click A")
                    await asyncio.sleep(50)

                    # Assuming dude actually connects to the bot > initialize trade
                    console.print("Trade initalizing assuming connection was made.", style = "yellow")
                    for x in range(6):
                        await connection.switch("click A")
                        await asyncio.sleep(3)
                    await connection.switch("click A")
                    await asyncio.sleep(50)

                    # Backing out to over world
                    console.print(f'Backing out to overworld.', style = "magenta")
                    await connection.switch("click B")
                    await asyncio.sleep(1)
                    await connection.switch("setStick RIGHT yVal 0x7FFF")
                    await connection.switch("setStick RIGHT yVal 0x0000")
                    await asyncio.sleep(1)
                    for x in range(2):
                        await connection.switch("click A")
                        await asyncio.sleep(2)
                    await connection.switch("click Y")
                    await asyncio.sleep(1)
                    await connection.switch("setStick RIGHT yVal -0x8000")
                    await connection.switch("setStick RIGHT yVal 0x0000")
                    await asyncio.sleep(0.5)
                    await connection.switch("click A")

                    # "Here is what you traded me:"
                    await connection.switch(f"pointerPeek 344 {b1s1}")
                    filepath2 = f"Files/dump/{msg.id}.eb8"
                    pokemon = (await connection._r.read(689))[:-1]
                    async with aiofiles.open(filepath2, 'wb+') as f:
                        await f.write(binascii.unhexlify(pokemon))
                    console.print(f'Dumped {filepath2}', style = "red")
                    await queued.send(file = discord.File(filepath2), content = success) 
                    console.print(f'Trade completed with {queued}.', style = "green")

                    # End
                    del queuelist[user]
                    console.print("Ready for next trade.", style = "bold underline white")
                    await asyncio.sleep(5)


def setup(client):
    client.add_cog(trader(client))