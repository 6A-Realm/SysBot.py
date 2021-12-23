from discord.ext import commands
from yaml import load, dump
import socket
from rich.console import Console
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
    if autoscreen == 2: 
        switch(serv, "screenOff")
        console.print("Switch screen was turned off.", style="green")
except socket.error:
    console.print(f"Unable to connect to {switchip}:{switchport}.", style="red")
    console.print(f"\nClick here to follow the connection troubleshooting guide by the official sysbot team.\nhttps://github.com/kwsch/SysBot.NET/wiki/Troubleshooting-Connection-Errors")

class connection(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(connection(client))