from pokemon.connection import switch, serv
import discord
from discord.ext import commands
from yaml import load
from rich.console import Console
import os
import datetime

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

console = Console()

# Queue List by Discord ID
queuelist = []

# Cog 
class request(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Request Module --}
    @commands.command()
    @commands.guild_only()
    async def testtradetest(self, ctx):
        if ctx.message.author.id in userblacklist:
            await ctx.send("User is blacklisted from using the bot.")
            if ctx.message.author.id in queuelist:
                await ctx.send("You are already in queue.")
            
            else:
                switch(serv, "getTitleID")
                title = serv.recv(689)
                title = title[0:-1]
                title = str(title,'utf-8')
                if title == "0100000011D90000" or "010018E011D92000":
                    for attachment in ctx.message.attachments:

                        if attachment.filename.endswith((".eb8")):

                            # Legality check by GriffinG1: https://github.com/GriffinG1/FlagBot/blob/22da7ae04e5f5383eb23b7aa75cc9fab7d90b355/addons/pkhex.py#L221
                            #r = await self.process_file(ctx, ctx.message.attachments, "api/bot/check")
                            #if r == 400:
                            #    return
                            #rj = r[1]
                            #reasons = rj["IllegalReasons"].split("\n")
                            #if reasons[0] == "Legal!":

                                # Logs in console
                                os.system('cls||clear')
                                await attachment.save(f"Files/sysbot/requested-{ctx.message.author.id}.eb8")
                                prioritycheck = discord.utils.find(lambda r: r.id == priority, ctx.message.guild.roles)
                                if prioritycheck in ctx.message.author.roles:
                                    queuelist.insert(0, ctx.message.author.id)
                                else:
                                    queuelist.append(ctx.message.author.id)
                                console.log(f'{ctx.message.author.name} has been added to the queue', style="blue")
                                await ctx.message.delete()
                                await ctx.send(f'{ctx.message.author.name} has been added to the queue. Current queue length: {len(queuelist)}.')
                                logger = open("logs.txt", "a")
                                logtime = datetime.datetime.now()
                                logger.write(logtime + " || " + {ctx.message.author.name} + " has requested to trade with the bot" + "\n")
                                logger.close()

                            #else:
                                #embed = discord.Embed(title="Your pokemon was illegal", description="", colour=discord.Colour.red())
                                #embed = self.list_to_embed(embed, reasons)
                                #await ctx.send(embed=embed)

                        else:
                            await ctx.channel.send("Unable to trade. Ensure your file ends in `.eb8` and is legal.")
                if title == "010003F003A34000" or "0100187003A36000":
                    await ctx.send("SysBot.py is not made for LGPE yet.")
                    del queuelist[0]

                if title == "0100ABF008968000" or "01008DB008C2C000":
                    await ctx.send("SysBot.py is not made for SWSH yet.")
                    del queuelist[0]
                else:
                    pass


def setup(client):
    client.add_cog(request(client))