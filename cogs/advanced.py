import discord
from discord import client
from discord.ext import commands
import yaml
from yaml import load, dump

# Simple file reader to load advanced settings
with open("advanced/blacklist.yaml", encoding='utf-8') as file:
    data = load(file)
    userblacklist = data["userblacklist"]

with open("advanced/logs.yaml", encoding='utf-8') as file:
    data = load(file)
    log = data["log"]

with open("advanced/priority.yaml", encoding='utf-8') as file:
    data = load(file)
    priority = data["priority"]

with open("advanced/sudo.yaml", encoding='utf-8') as file:
    data = load(file)
    sudo = data["sudo"]
    
class advanced(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Advanced Settings Commands --}
    @commands.command(pass_context=True)
    @commands.is_owner()
    async def addsuo(self, ctx, user: discord.User):
            person = user.id
            with open("advanced/sudo.yaml", encoding='utf-8') as file:
                data = load(file)
            if person in data["sudo"]:
                await ctx.send('This user already has sudo perms.')
            else:
                data["sudo"].append(person)
                sudo.append(person)
                with open('advanced/sudo.yaml', 'w') as writer:
                    yaml.dump(data, writer)

                await ctx.send('This user now has sudo permissons.')

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def removesudo(self, ctx, user: discord.User):
            person = user.id
            with open("advanced/sudo.yaml", encoding='utf-8') as file:
                datachan = load(file)
            datachan["sudo"].remove(person)
            sudo.remove(person)
            with open('advanced/sudo.yaml', 'w') as writer:
                yaml.dump(datachan, writer)
            await ctx.send('This user no longer has sudo permissons.')

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.User):
            person = user.id
            with open("advanced/blacklist.yaml", encoding='utf-8') as file:
                datachan = load(file)
            if person in datachan["userblacklist"]:
                await ctx.send('This user already blacklisted.')
            else:
                datachan["userblacklist"].append(person)
                userblacklist.append(person)
                with open('advanced/blacklist.yaml', 'w') as writer:
                    yaml.dump(datachan, writer)

                await ctx.send('This user now has blacklisted from using the bot.')

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.User):
            person = user.id
            with open("advanced/blacklist.yaml", encoding='utf-8') as file:
                datachan = load(file)
            datachan["userblacklist"].remove(person)
            userblacklist.remove(person)
            with open('advanced/blacklist.yaml', 'w') as writer:
                yaml.dump(datachan, writer)
            await ctx.send('This user no longer blacklisted.')

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def loghere(self, ctx):
            channel = ctx.message.channel.id

            with open("advanced/logs.yaml", encoding='utf-8') as file:
                data = load(file)
            if channel in data["log"]:
                await ctx.send('This channel is already listed in the update list.')
            else:
                data["log"].append(channel)
                log.append(channel)
                with open('advanced/logs.yaml', 'w') as writer:
                    yaml.dump(data, writer)

                await ctx.send('This channel has been added. You will now get announcements in this channel.')

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def dontlog(self, ctx):
            channel = ctx.message.channel.id
            with open("advanced/logs.yaml", encoding='utf-8') as file:
                data = load(file)
            try:
                data["log"].remove(channel)
                log.remove(channel)
                with open('advanced/logs.yaml', 'w') as writer:
                    yaml.dump(data, writer)
                await ctx.send('This channel has been removed. You will no longer get announcements in this channel.')
            except:
                await ctx.send('An error occured. Please try again later.')


def setup(client):
    client.add_cog(advanced(client))
