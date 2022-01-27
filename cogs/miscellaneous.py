import discord
from discord.ext import commands
from yaml import load
import json
import asyncio

# Loads token and prefix from config file
with open("config.yaml") as file:
    data = load(file)
    support = data["support-server-name"]
    support2 = data["support-server-invite"]
    donation = data["donation"]

class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def prefix(self, ctx):
        with open("res/prefix.json", "r") as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.message.guild.id)]
        await ctx.send(f'My prefix in this server is: `{prefix}`')

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
        if donation != "None":
            await ctx.send(donation)
        else: 
            await ctx.send("There is no donation link for this bot.")

    @commands.command()
    async def source(self, ctx):
        embed = discord.Embed(title="SysBot.py Source Code", url="https://github.com/6A-Realm/SysBot.py", description="Here is the source code for this bot.\nhttps://github.com/6A-Realm/SysBot.py", color=ctx.author.color)       
        await ctx.send(embed = embed)

    @commands.command()
    async def channelid(self, ctx):
        await ctx.send(ctx.message.channel.id) 

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

    @commands.command()
    @commands.guild_only()
    async def servericon(self, ctx):
        icon = ctx.guild.icon_url
        try:
            await ctx.send(icon)    
        except Exception as e:
            await ctx.send("Server has no icon.")

    @commands.command()
    async def serverinfo(self, ctx, server: discord.Guild = None):
        if server is None:
            server = ctx.guild
        embed = discord.Embed(title = server.name, color = 0x00CC99)
        embed.add_field(name = "Owner:", value = f"{server.owner}")
        embed.add_field(name = "Members:", value = f"{server.member_count}")
        embed.add_field(name = "Channels:", value = len([x for x in server.channels if type(x) == discord.channel.TextChannel]))
        embed.add_field(name = "Roles:", value = len(server.roles))
        embed.add_field(name = "Region:", value = str(server.region).title())
        embed.add_field(name = "Created:", value = server.created_at.__format__("%A, %B %d, %Y at %H:%M:%S"))
        embed.set_thumbnail(url = server.icon_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(title = "Member Info", color = user.color)
        embed.add_field(name = "Name", value = user.display_name)
        embed.add_field(name = "ID:", value = user.id)
        embed.add_field(name = "Created:", value = user.created_at.__format__("%A, %B %d, %Y at %H:%M:%S"))
        embed.add_field(name = "Joined:", value = user.joined_at.__format__("%A, %B %d, %Y at %H:%M:%S"))
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.channel.send(embed = embed)

    @commands.command()
    async def remind(self, ctx, duration, *, reminder):
        unit = duration[-1]
        if unit == 's':
            time = int(duration[:-1])
            longunit = 'seconds'
        elif unit == 'm':
            time = int(duration[:-1]) * 60
            longunit = 'minutes'
        elif unit == 'h':
            time = int(duration[:-1]) * 60 * 60
            longunit = 'hours'
        else:
            await ctx.send('Invalid Unit! Use `s`, `m`, or `h`.')
            return
        await ctx.send(f"You will be reminded to **{reminder}** in **{time} {longunit}**.")

        await asyncio.sleep(time)
        await ctx.send(f"⏰ You are being reminded to **{reminder}**")

    @commands.command()
    async def sysbotbase(self, ctx):
        await ctx.reply("https://github.com/olliz0r/sys-botbase/releases/latest")


def setup(client):
    client.add_cog(Miscellaneous(client))