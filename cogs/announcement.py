import discord
from discord.ext import commands
import yaml
from yaml import load

# Simple file reader to load channels
with open("advanced/channels.yaml", encoding='utf-8') as file:
    data = load(file)
    channels = data["channels"]

# Loads token and prefix from config file
with open("config.yaml") as file:
    data = load(file)
    embedcolor = data["color"]
    support = data["support-server-name"]
    support2 = data["support-server-invite"]
    dmchannel = data["dmchannel"]
    botonname = data["botonname"]
    botdownname = data["botdownname"]

class Announcement(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Owner Only Commands --}
    @commands.command(help="Sends an update to all channels in channels.yaml", brief='boton <message>')
    @commands.is_owner()
    async def boton(self, ctx, *, message = None):
        try:
            for chan in channels:
                channel = self.client.get_channel(chan)
                if message is None:
                    info = discord.Embed(title='{0.user.name}'.format(self.client) + ' Is Online!', color=embedcolor)
                else:
                    info = discord.Embed(title='{0.user.name}'.format(self.client) + ' Is Online!', description=(message), color=embedcolor)
                await channel.send(embed=info)
                try:
                    await channel.edit(name=botonname)
                    overwrite = channel.overwrites_for(ctx.guild.default_role)
                    overwrite.send_messages = True
                    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                except Exception as e:
                    await ctx.send(e)
        except Exception as e:
            await ctx.send(e)

    @commands.command(help="Sends an announcement to all channels in channels.yaml", brief='announcement <message>')
    @commands.is_owner()
    async def announcement(self, ctx, *, message = None):
        try:
            for chan in channels:
                channel = self.client.get_channel(chan)
                if message is None:
                    info = discord.Embed(title='{0.user.name}'.format(self.client) + ' Update!', description=(message), color=embedcolor)
                else:
                    info = discord.Embed(title='{0.user.name}'.format(self.client) + ' Update!', description=(message), color=embedcolor)
                await channel.send(embed=info)
            await ctx.send("Announcement message has been sent.")
        except Exception as e:
            await ctx.send(e)

    @commands.command(help="Sends a bot has crashed message to all channels in channels.yaml", brief='botdown')
    @commands.is_owner()
    async def botdown(self, ctx):
        try:
            for chan in channels:
                channel = self.client.get_channel(chan)
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = False
                info = discord.Embed(title='{0.user.name}'.format(self.client) + ' Has Crashed!', description='The bot is experiencing some difficulty. An announcement will be set out when it is fixed.\nJoin the [Support Server](https://discord.gg/BcDexg4jDu) for more info and updates.', color=0xD60FBB)
                await channel.send(embed=info)
                try: 
                    await channel.edit(name=botdownname)
                    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                except Exception as e:
                    await ctx.send(e)
            await ctx.send("Bot down message has been sent.")
        except Exception as e:
            await ctx.send(e)

    @commands.command(name="redact", help="Removes the given number of messages in all of this bot's linked channels. Limited to purging 99 messages at a time.")
    @commands.is_owner()
    async def redact(self, ctx, amount: int = 1):
        for chan in channels:
            try:
                counter = 0
                channel = self.client.get_channel(chan)
                async for message in channel.history(limit = 10):
                        if message.author.id == self.client.user.id and counter < amount:
                            await message.delete()
                            counter += 1
                await ctx.send(f'{amount} message(s) redacted.')
            except Exception as e:
                await ctx.send(e)

# {-- Public Moderator Locked Commands --}
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def add(self, ctx):
        channel = ctx.message.channel.id
        with open("advanced/channels.yaml", encoding='utf-8') as file:
            data = load(file)
        if channel in data["channels"]:
            await ctx.send('This channel is already listed in the update list.')
        else:
            data["channels"].append(channel)
            channels.append(channel)
            with open('advanced/channels.yaml', 'w') as writer:
                yaml.dump(data, writer)
            await ctx.send('This channel has been added. You will now get announcements in this channel.')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def remove(self, ctx):
            channel = ctx.message.channel.id
            with open("advanced/channels.yaml", encoding='utf-8') as file:
                data = load(file)
            data["channels"].remove(channel)
            channels.remove(channel)
            with open('advanced/channels.yaml', 'w') as writer:
                yaml.dump(data, writer)
            await ctx.send('This channel has been removed. You will no longer get announcements in this channel.')


def setup(client):
    client.add_cog(Announcement(client))