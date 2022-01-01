import discord
from discord.ext import commands, tasks
from yaml import load
import asyncio

# Loads prefix from config file
with open("config.yaml") as file:
    data = load(file)
    botprefix = data["botprefix"]

# Cog 
class presence(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.presence.start()

# Presence Loop
    @tasks.loop()
    async def presence(self):
        await self.client.wait_until_ready()

        await self.client.change_presence(activity=discord.Game(name=f'{str(botprefix)}help'))
        await asyncio.sleep(30)
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you get your pokemon"))
        await asyncio.sleep(30)
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".eb8s only."))
        await asyncio.sleep(30)
        await self.client.change_presence(activity=discord.Game(name=f'BDSP ooo'))
        await asyncio.sleep(30)

def setup(client):
    client.add_cog(presence(client))