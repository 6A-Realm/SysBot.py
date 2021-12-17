import discord
from discord.ext import commands
from yaml import load, dump

# Loads token and prefix from config file
with open("config.yaml") as file:
    data = load(file)
    botprefix = data["botprefix"]
    support = data["support-server-name"]
    support2 = data["support-server-invite"]
    donation = data["donation"]

class miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def prefix(self, ctx):
        await ctx.send(f'My prefix is: `{botprefix}`')

    @commands.command()
    @commands.guild_only()
    async def latency(self, ctx):
            await ctx.send(':ping_pong: Pong! ' + str(round(self.client.latency * 1000, 2)) + " ms")

    @commands.command()
    @commands.guild_only()
    async def invite(self, ctx):
        await ctx.send(support2)

    @commands.command()
    @commands.guild_only()
    async def support(self, ctx):
        await ctx.send(donation)

    @commands.command()
    @commands.guild_only()
    async def botstatus(self, ctx, user: discord.User):
        embed = discord.Embed(title=f"{user.name} is ", description= f'{user.name} is {user.activities[0].name}.', color=0xFFFFF6)
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    async def guide(self, ctx):
        embed=discord.Embed(title="How To Use Sysbot", url="https://youtu.be/1WbOHrQfMlc", description="This is a [guide](https://youtu.be/1WbOHrQfMlc) on how to use sysbot.\nPlease watch the complete video on how to use the bots.\nAll bots are in this bots official server.", color=ctx.author.color)
        embed.set_thumbnail(url="https://i.ytimg.com/vi/1WbOHrQfMlc/mqdefault.jpg")
        await ctx.send(embed=embed)

    @commands.command() 
    @commands.guild_only()
    async def languide(self, ctx):
        embed=discord.Embed(title="How To Use LAN Sysbot", url="https://docs.google.com/document/d/e/2PACX-1vR9tpYmZ3qCbqOeZb1XwnNESAauTf9rVJVzJ1G22TkmGsVZf8LVJs-o-rNshKsYZuyZBdrdRDzTtsqH/pub", description=f"""
        This is a [lan guide](https://docs.google.com/document/d/e/2PACX-1vR9tpYmZ3qCbqOeZb1XwnNESAauTf9rVJVzJ1G22TkmGsVZf8LVJs-o-rNshKsYZuyZBdrdRDzTtsqH/pub) on how to connect to LAN. 
        Here are some helpful videos to get you started:
        [LAN Installation on WINDOWS](https://www.youtube.com/watch?v=qQSQH6F6ogk) || By Optimisim247.
        [LAN Installation on MAC](https://www.youtube.com/watch?v=nhC8qgjauL0&t=369s)
        All bots are in the bots official [Pokemon LAN server](https://discord.gg/pkmn).""", color= ctx.author.color)
        embed.set_thumbnail(url="https://i.ytimg.com/vi/1WbOHrQfMlc/mqdefault.jpg")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def lgpe(self, ctx):
        embed=discord.Embed(title="How To Use The LGPE Sysbot", url="https://www.youtube.com/watch?v=0dS2QTxqFnI", description="This is a [guide](https://www.youtube.com/watch?v=0dS2QTxqFnI) on how to use the LGPE sysbot.\nPlease watch the complete video on how to use the bots.\nAll bots are in this bots official server.", color=ctx.author.color)
        embed.set_thumbnail(url="https://i.ytimg.com/vi/1WbOHrQfMlc/mqdefault.jpg")
        await ctx.send(embed=embed)
        
def setup(client):
    client.add_cog(miscellaneous(client))