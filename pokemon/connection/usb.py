from discord.ext import commands
from yaml import load
import usb.core
import usb.util
import struct
from pokemon.utils.values import p, e, sw, sh, bd, sp
from rich.console import Console
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
        self.dev = None

    async def switch(self, content):
        try:
            self._w.write(struct.pack("<I", (len(content)+2)))
            self._w.write(content)
        except Exception as e: 
            console.print(f"Unable to send commands to switch. {e}", style="red")

    # Ping switch, fetch title ID, check if auto screen off
    async def initiate(self):
        self.dev = usb.core.find(idVendor=0x057E, idProduct=0x3000)
        if self.dev is not None:
            try:
                self.dev.set_configuration()
                intf = self.dev.get_active_configuration()[(0,0)]
                self._w = usb.util.find_descriptor(intf,custom_match=lambda e:usb.util.endpoint_direction(e.bEndpointAddress)==usb.util.ENDPOINT_OUT)
                self._r = usb.util.find_descriptor(intf,custom_match=lambda e:usb.util.endpoint_direction(e.bEndpointAddress)==usb.util.ENDPOINT_IN)

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

                await connection.switch("detachController")
                await connection.switch("controllerType 1")
                
                for extension in pdiscord:
                    try:
                        self.client.load_extension("pokemon.discord." + extension)
                    except Exception as err:
                        console.print(f"Unable to load {extension} {err}.", style="red")
            except:
                console.print(f"Unable to connect to Switch.", style="red")
                console.print("Click here to follow the connection troubleshooting guide: https://github.com/6A-Realm/SysBot.py/wiki/Connection-Issues", style="yellow")
        else:
            console.print(f"Connect your Switch via USB.", style="red")

    async def connect(self):
        self.dev = usb.core.find(idVendor=0x057E, idProduct=0x3000)
        if self.dev is not None:
            try:
                self.dev.set_configuration()
                intf = self.dev.get_active_configuration()[(0,0)]
                self._w = usb.util.find_descriptor(intf,custom_match=lambda e:usb.util.endpoint_direction(e.bEndpointAddress)==usb.util.ENDPOINT_OUT)
                self._r = usb.util.find_descriptor(intf,custom_match=lambda e:usb.util.endpoint_direction(e.bEndpointAddress)==usb.util.ENDPOINT_IN)
            except:
                console.print(f"Unable to connect to Switch.", style="red")
        else:
            console.print(f"Connect your Switch via USB.", style="red")


def setup(client):
    client.add_cog(connection(client))