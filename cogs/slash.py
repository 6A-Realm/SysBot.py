import discord
from discord.ext import commands
from yaml import load
from discord_slash import cog_ext, SlashContext
import os
import json

##Loads token and prefix from config file
with open("config.yaml") as file:
        data = load(file)
        support2 = data["support-server-invite"]

class SLASH(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Public Slash Commands --}
    @cog_ext.cog_slash(name="guide", description="How to use Sysbot guide")
    async def _guide(self, ctx: SlashContext):
            embed=discord.Embed(title="How To Use Sysbot", url="https://youtu.be/1WbOHrQfMlc", description="This is a [guide](https://youtu.be/1WbOHrQfMlc) on how to use sysbot.\nPlease watch the complete video on how to use the bots.\nAll bots are in this bots official server.", color=ctx.author.color)
            embed.set_thumbnail(url="https://i.ytimg.com/vi/1WbOHrQfMlc/mqdefault.jpg")
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="invite", description="Want an invite?")
    async def _invite(self, ctx):
        await ctx.send(support2)

    @cog_ext.cog_slash(name="languide", description="How to connect to LAN guide")
    async def _languide(self, ctx: SlashContext):
            embed=discord.Embed(title="How To Use LAN Sysbot", url="https://docs.google.com/document/d/e/2PACX-1vR9tpYmZ3qCbqOeZb1XwnNESAauTf9rVJVzJ1G22TkmGsVZf8LVJs-o-rNshKsYZuyZBdrdRDzTtsqH/pub", description=f"""
            This is a [lan guide](https://docs.google.com/document/d/e/2PACX-1vR9tpYmZ3qCbqOeZb1XwnNESAauTf9rVJVzJ1G22TkmGsVZf8LVJs-o-rNshKsYZuyZBdrdRDzTtsqH/pub) on how to connect to LAN. 
            Here are some helpful videos to get you started:
            [LAN Installation on WINDOWS](https://www.youtube.com/watch?v=qQSQH6F6ogk) || By Optimisim247.
            [LAN Installation on MAC](https://www.youtube.com/watch?v=nhC8qgjauL0&t=369s)
            All bots are in the bots official [Pokemon LAN server](https://discord.gg/pkmn).""", color= ctx.author.color)
            embed.set_thumbnail(url="https://i.ytimg.com/vi/1WbOHrQfMlc/mqdefault.jpg")  
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="lgpe", description="How to use the LGPE Sysbot guide")
    async def _lgpe(self, ctx: SlashContext):
            embed=discord.Embed(title="How To Use The LGPE Sysbot", url="https://www.youtube.com/watch?v=0dS2QTxqFnI", description="This is a [guide](https://www.youtube.com/watch?v=0dS2QTxqFnI) on how to use the LGPE sysbot.\nPlease watch the complete video on how to use the bots.\nAll bots are in this bots official server.", color=ctx.author.color)
            embed.set_thumbnail(url="https://i.ytimg.com/vi/1WbOHrQfMlc/mqdefault.jpg")
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="missingno", description="Provides a safe missingno file.")
    async def _missingno(self, ctx):
            filepath = f"res/missingno.pk8"
            if os.path.exists(filepath):
                    await ctx.send(file=discord.File(filepath))

    @cog_ext.cog_slash(name="prefix", description="Gives you the bot's prefix")
    async def _prefix(self, ctx):
        with open("res/prefix.json", "r") as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        await ctx.send(f'My prefix in this server is: `{prefix}`')

def setup(client):
    client.add_cog(SLASH(client))