from pokemon.connection import switch, serv
from pokemon.values import bd, sp
from discord.ext import commands
from yaml import load
from rich.console import Console
console = Console()

# Simple file reader to load advanced settings
with open("advanced/blacklist.yaml", encoding='utf-8') as file:
    data = load(file)
    userblacklist = data["userblacklist"]

with open("advanced/priority.yaml", encoding='utf-8') as file:
    data = load(file)
    priority = data["priority"]

# Queue List by Discord ID
queuelist = []

# Cog 
class request(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Request Module --}
    @commands.command()
    @commands.guild_only()
    async def ttrade(self, ctx):
        user = ctx.message.author.id
        if user in userblacklist:
            return await ctx.send("User is blacklisted from using the bot.")
        if ctx.message.author.id in queuelist:
            return await ctx.send("You are already in queue.")
        switch(serv, "getTitleID")
        title = serv.recv(689)
        title = title[:-1]
        title = str(title,'utf-8')
        if title in [bd, sp]:
            for attachment in ctx.message.attachments:
                if attachment.filename.endswith((".eb8")):
                    await attachment.save(f"Files/sysbot/requested-{user}.eb8")

                    if user in priority:
                        queuelist.insert(0, user)
                    else:
                        queuelist.append(user)
                        console.log(f'{ctx.message.author.name} has been added to the queue', style="blue")
                        await ctx.message.delete()
                        await ctx.send(f'{ctx.message.author.name} has been added to the queue. Current queue length: {len(queuelist)}.')
                else:
                    await ctx.channel.send("Unable to trade. Ensure your file ends in `.eb8` and is legal.")


def setup(client):
    client.add_cog(request(client))