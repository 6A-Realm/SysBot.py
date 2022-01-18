import discord
from discord.ext import commands
from yaml import load
import json
import asyncio

# Loads token and prefix from config file
with open("config.yaml") as file:
    data = load(file)
    botprefix = data["defaultprefix"]
    support = data["support-server-name"]
    support2 = data["support-server-invite"]
    donation = data["donation"]

class miscellaneous(commands.Cog):
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
    async def channelid(self, ctx, *, name = None):
        channel = discord.utils.get(ctx.guild.channels, name = name)
        id = channel.id
        await ctx.send(id) 

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
        await ctx.send(icon)    

    @commands.command(name='sinfo', aliases=['server'])
    async def serverinfo(self, ctx, *, name:str = ""):
        """Get server info"""
        if name:
            server = None
            try:
                server = self.bot.get_guild(int(name))
                if not server:
                    return await ctx.send('Server not found :satellite_orbital:')
            except:
                for i in self.bot.guilds:
                    if i.name.lower() == name.lower():
                        server = i
                        break
                if not server:
                    return await ctx.send("Server not found :satellite_orbital: or maybe I'm not in it")
        else:
            server = ctx.guild

        # Count channels
        tchannel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])
        vchannel_count = len([x for x in server.channels if type(x) == discord.channel.VoiceChannel])
        # Count roles
        role_count = len(server.roles)
        # Count emojis
        emojis = len(server.emojis)
        # Count bots
        bot_count = len([x for x in server.members if x.bot])

        # Create embed
        em = discord.Embed(color=0x00CC99)
        em.set_author(name='Server Info:', icon_url=server.owner.avatar_url)
        em.add_field(name='Name', value=f'`{server.name}`')
        em.add_field(name='Owner', value=f'`{server.owner}`', inline=False)
        em.add_field(name='Members', value=f'`{server.member_count - bot_count}`')
        em.add_field(name='Bots', value=f'`{bot_count}`')
        em.add_field(name='Emojis', value=f'`{emojis}`')
        em.add_field(name='Text Channels', value=f'`{tchannel_count}`')
        em.add_field(name='Voice Channels', value=f'`{vchannel_count}`')
        em.add_field(name='Verification Level', value=f'`{str(server.verification_level).title()}`')
        em.add_field(name='Number of roles', value=f'`{role_count}`')
        em.add_field(name='Highest role', value=f'`{server.roles[-1]}`')
        em.add_field(name='Region', value=f'`{str(server.region).title()}`')
        em.add_field(name='Created At', value=f"`{server.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')}`", inline=False)
        em.set_thumbnail(url=server.icon_url)
        em.set_footer(text='Server ID: %s' % server.id)

        await ctx.send(embed=em)

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
    @commands.guild_only()
    async def botperms(self, ctx, *, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        member = ctx.guild.me
        await self.say_permissions(ctx, member, channel)

    @commands.command()
    async def sysbotbase(self, ctx):
        await ctx.reply("https://github.com/olliz0r/sys-botbase/releases/latest")

def setup(client):
    client.add_cog(miscellaneous(client))