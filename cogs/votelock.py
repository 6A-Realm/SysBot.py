import discord
from discord import client
from discord.ext import commands
import asyncio


class votelock(commands.Cog):
    def __init__(self, client):
        self.client = client

    client.lan = 0

# {-- Public Commands --}
    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def votelock(self, ctx):
        client.lan += 1
        if client.lan == 1:
            await ctx.send(f'{ctx.message.author} has voted to lock this channel. 2 more votes are required.')
        if client.lan == 2: 
            await ctx.send(f'{ctx.message.author} has voted to lock this channel. 1 more vote is required.')
        if client.lan == 3: 
            await ctx.send(f'{ctx.message.author} has voted to lock this channel.')
            overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send(':red_circle: **Channel locked.** This bot is offline, please use one of the other bots.')
            if ctx.channel.id == 860765383908655144:
                down = discord.Embed(title="LGPE Bot Is Down!", description=f"Many users have been experiencing bot disconnection, meaning that they cannot complete their trades. This means the bot has crashed; therefore, this channel has been locked.\n\n\n**Do not DM anyone about the bot. Do not ask when the bot will be up.**\n\n\nRemember, this is a free service that nobody else offers. This is also something that the other sysbot creators said would be impossible to make.\n\n\nThank you for waiting patiently.", colour=discord.Colour.orange())
                down.set_footer(text="Failure to follow bolded line will result in a ban.")  
                await ctx.send(embed = down)
            client.lan = 0

# {-- Admin Commands --}
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def clearvotes(self, ctx):
        client.lan = 0
        await ctx.send('Votes have reset to 0.')


def setup(client):
    client.add_cog(votelock(client))
