import discord
from discord.ext import commands, tasks
import random
import asyncio
from pokemon.connection import game

# Cog 
class presence(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.presence.start()

# Presence Loop
    @tasks.loop()
    async def presence(self):
        await self.client.wait_until_ready()

        # Presence  
        eb8s = random.randint(5,45) 
        await self.client.change_presence(activity=discord.Activity(type = discord.ActivityType.watching, name = ".eb8s only."))
        await asyncio.sleep(eb8s)

        help = random.randint(5,45) 
        await self.client.change_presence(activity = discord.Game(name = f'@{self.client.user.name} help'))
        await asyncio.sleep(help)

        pokemon = random.randint(5,45) 
        await self.client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "you get your pokemon"))
        await asyncio.sleep(pokemon)

        playing = random.randint(5,45) 
        await self.client.change_presence(activity = discord.Game(name = game))
        await asyncio.sleep(playing)

        invite = random.randint(5,45) 
        await self.client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = ".gg/pkmn"))
        await asyncio.sleep(invite)

        py = random.randint(5,45) 
        await self.client.change_presence(activity = discord.Game(name = 'SysBot.py'))
        await asyncio.sleep(py)


def setup(client):
    client.add_cog(presence(client))