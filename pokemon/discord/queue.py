from pokemon.pokeinput import queuelist
import discord
from discord.ext import commands, tasks

# Cog 
class queued(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Queue Module --}   
    @commands.group(invoke_without_command=True)
    async def queue(self, ctx):
        if ctx.message.author.id in queuelist:
            person = ctx.message.author.id
            position = queuelist.index(person) + 1
            await ctx.send(f"Your current position is {position}")
        else:
            await ctx.send("You are not in queue.")

    @queue.group()
    async def list(self, ctx):
        list = []
        enter = '\n'
        counter = 0
        for x in queuelist:
            user = self.client.get_user(x.id)
            counter += 1
            list.append(f"{counter}) {user.name}")
        embed = discord.Embed(title="Queue List", description=f"{enter.join(y for y in list)}", colour=discord.Colour.blurple())
        await ctx.send(embed = embed)

    @queue.group()
    async def leave(self, ctx):
        if ctx.message.author.id in queuelist:
            person = ctx.message.author.id
            position = queuelist.index(person)
            if position < 2:
                ctx.send("Cannot remove you from the queue, currently being processed.")            
            else:
                person = ctx.message.author.id
                queuelist.remove(person)
                await ctx.send("Removed from queue.")
        else:
            ctx.send("You are not in queue.")

        embed = discord.Embed(title="Queue List", description=f"", colour=discord.Colour.blurple())
        await ctx.send(embed = embed)

    @queue.group()
    @commands.is_owner()
    async def remove(self, ctx, user: discord.User):
        person = user.id
        name = user.name
        if person in queuelist:
            queuelist.remove(person)
            await ctx.send(f"{name} was removed from the queue.")
        else:
            await ctx.send(f"{name} is not in queue.")


def setup(client):
    client.add_cog(queued(client))
