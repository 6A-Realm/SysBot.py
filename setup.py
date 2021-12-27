# SysBot.py setup tool

import asyncio
import os

# Install requirements.txt
print("Installing required modules.")
try:
    os.system('python -m pip -r requirements.txt')
except Exception as e:
    print(f"Unable to install requirements: {e}")

import discord
from discord.ext import commands
from yaml import load
import socket

# Load information from config.yaml
with open("config.yaml") as file:
    data = load(file)
    token = data["token"]
    switchip = data["ip"]
    switchport = data["port"]

client = commands.Bot(description="SysBot.py Setup", intents=discord.Intents.all())

# Log into discord and connect to switch tests
@client.event
async def on_ready():
    print(f"Successfully connected to: {client.user.tag}")
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serv.connect((switchip, switchport))
        print(f"Successfully connected to {switchip}:{switchport}.")
    except socket.error:
        print(f"Unable to connect to {switchip}:{switchport}.\nClick here to follow the connection troubleshooting guide by the official sysbot team.\nhttps://github.com/kwsch/SysBot.NET/wiki/Troubleshooting-Connection-Errors\nEnsure you have sys-botbase installed on your switch.")
    await asyncio.sleep(5)
    print("Setup successful. Now closing setup.py...")
    await asyncio.sleep(5)
    client.logout()

try:
    client.run('{}'.format(token))
except Exception as e:
    print(f"Error when logging in: {e}\n\n\nMake sure you have PRESENCE INTENT and SERVER MEMBERS INTENT turned on in the bot's settings page on the developer portal.")