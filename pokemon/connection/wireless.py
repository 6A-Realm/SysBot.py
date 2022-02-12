from discord.ext import commands
from yaml import load
import asyncio
from rich.console import Console
from pokemon.utils.values import p, e, sw, sh, bd, sp
console = Console()

# Loads switch ip and port from config file
with open("config.yaml") as file:
    data = load(file)
    switchip = data["ip"]
    switchport = data["port"]
    autoscreen = data["autoscreen"]
        
# SysBot extensions list
pdiscord = ["advanced", "pokeinput", "queue", "remote", "trader"]

# Game Title
setgame = ["Pokémon"]

class connection(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._r = None
        self._w = None

    # sys-botbase to send commands
    async def switch(self, content):
        try:
            content += '\r\n'
            self._w.write(content.encode())
            await self._w.drain()
        except Exception as e: 
            console.print(f"Unable to send commands to switch. {e}", style="red")

    # Ping switch, fetch title ID, check if auto screen off
    async def initiate(self):
        try:
            self._r, self._w = await asyncio.open_connection(switchip, switchport, limit = 524288)
            console.print(f"Successfully connected to {switchip}:{switchport}.", style="green")

            # Check title ID
            await self.switch("getTitleID")
            title = ((await self._r.read(689))[:-1]).decode("utf-8")
            setgame.clear()
            if title in [bd, sp]:
                setgame.append("BDSP")
            elif title in [sw, sh]:
                setgame.append("SWSH")
            elif title in [p, e]:
                setgame.append("LGPE")
            else:
                setgame.append("not a Pokémon game")

            # Check if auto screen off is toggled
            if autoscreen == 2: 
                await self.switch("screenOff")
                console.print("Switch screen was turned off.", style="green")

            # Set controller
            await self.switch("detachController")
            await self.switch("controllerType 1")

            # Close socket
            self._w.close()
            await self._w.wait_closed()

            for extension in pdiscord:
                try:
                    self.client.load_extension("pokemon.discord." + extension)
                except Exception as err:
                    console.print(f"Unable to load {extension} {err}.", style="red")
        except:
            console.print(f"Unable to connect to {switchip}:{switchport}.", style="red")
            console.print("Click here to follow the connection troubleshooting guide: https://github.com/6A-Realm/SysBot.py/wiki/Connection-Issues", style="yellow")

    # IP/Port connection to switch (same thing you would put in sysbot)
    async def connect(self):
        try:
            self._r, self._w = await asyncio.open_connection(switchip, switchport, limit = 1048576)
        except OSError: 
            console.print(f"Unable to connect to {switchip}:{switchport}.", style="red")

    @commands.command(invoke_without_command=True)
    @commands.is_owner()
    async def ip(self, ctx):
        await ctx.send(f"Connected to {switchip}:{switchport}.")

def setup(client):
    client.add_cog(connection(client))

def teardown(client):
    print("SysBot.py no longer connected to Switch.")