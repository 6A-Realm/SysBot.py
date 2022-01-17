from discord.ext import commands
from yaml import load
import socket
from rich.console import Console
from pokemon.utils.values import p, e, sw, sh, bd, sp
from cogs.presence import game
console = Console()


# Loads switch ip and port from config file
with open("config.yaml") as file:
    data = load(file)
    switchip = data["ip"]
    switchport = data["port"]
    autoscreen = data["autoscreen"]

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
    
    switch(serv, "detachController")
    switch(serv, "controllerType 1")

    switch(serv, "getTitleID")
    title = serv.recv(689)
    title = title[:-1]
    title = str(title,'utf-8')
    game.clear()
    if title in [bd, sp]:
        game.append("BDSP")
    elif title in [sw, sh]:
        game.append("SWSH")
    elif title in [p, e]:
        game.append("LGPE")
    else:
        game.append("Not playing a Pokémon game")

    if autoscreen == 2: 
        switch(serv, "screenOff")
        console.print("Switch screen was turned off.", style="green")

except socket.error:
    console.print(f"Unable to connect to {switchip}:{switchport}.", style="red")
    console.print("Click here to follow the connection troubleshooting guide: https://github.com/6A-Realm/SysBot.py/wiki/Connection-Issues", style="yellow")

class connection(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def socket(self, ctx):
        await ctx.send(f"Connected to {switchip}:{switchport}.")
    
    @socket.group()
    @commands.is_owner()
    async def close(self, ctx):
        serv.shutdown(socket.SHUT_RDWR)
        serv.close()
        await ctx.send("Socket closed.")

    @socket.group()
    @commands.is_owner()
    async def restart(self, ctx):
        serv.shutdown(socket.SHUT_RDWR)
        serv.close()
        try:
            serv.connect((switchip, switchport))
            console.print(f"Successfully connected to {switchip}:{switchport}.", style="green")
            await ctx.send("Socket restarted.")
            if autoscreen == 2: 
                switch(serv, "screenOff")
                console.print("Switch screen was turned off.", style="green")
                await ctx.send("Switch screen was turned off.")
        except socket.error:
            console.print(f"Unable to connect to {switchip}:{switchport}.", style="red")
            await ctx.send(f"Unable to connect to {switchip}:{switchport}.")


def setup(client):
    client.add_cog(connection(client))