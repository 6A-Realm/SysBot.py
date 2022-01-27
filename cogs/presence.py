import discord
from discord.ext import commands, tasks
import random
import asyncio

# Queue Length
queuelength = []

# Game Title
game = ["Pokémon"]

# Cog 
class PRESENCE(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.presence.start()

# Presence Loop
    @tasks.loop()
    async def presence(self):
        await self.client.wait_until_ready()

        # Presence
        length = len(queuelength)
        queue = random.randint(5,45) 
        if length > 0:
            await self.client.change_presence(activity = discord.Game(name = f"Trading with {length} members"))
            await asyncio.sleep(queue)
        else:
            await self.client.change_presence(status = discord.Status.idle, activity = discord.Game(name=f"SysBot queue is empty"))
            await asyncio.sleep(queue)

        playing = random.randint(5,45) 
        await self.client.change_presence(activity = discord.Game(name = ''.join(game)))
        await asyncio.sleep(playing)

        help = random.randint(5,45) 
        await self.client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = f"@{self.client.user.name} help"))
        await asyncio.sleep(help)

        py = random.randint(5,45) 
        await self.client.change_presence(activity = discord.Game(name = "SysBot.py by 6A"))
        await asyncio.sleep(py)


def setup(client):
    client.add_cog(PRESENCE(client))