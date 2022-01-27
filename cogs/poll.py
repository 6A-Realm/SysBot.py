import discord
from discord import client
from discord.ext import commands
from yaml import load, dump

#Loads color
with open("config.yaml") as file:
    data = load(file)
    embedcolor = data["color"]
    
class Polling(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Public Commands --}
    @commands.command(no_pm=True)
    @commands.guild_only()
    async def poll(self, ctx, *, question: str):
            embed = discord.Embed(title="Quick Poll", description=f'{question}', color=0xFFD700)
            poll = await ctx.send(embed = embed)
            await poll.add_reaction("👍")
            await poll.add_reaction("👎")

    @commands.command()
    @commands.is_owner()
    async def poll(ctx,*,message):
        embed = discord.Embed(title="Bot Mode Poll", description=f"Which mode should I switch to next?\n{message}", color=embedcolor)
        embed.add_field(name="Y-Comm =", value="🎮", inline=False)
        embed.add_field(name="LAN =", value="💻", inline=False)
        embed.add_field(name="LGPE =", value="🐀", inline=False)
        embed.add_field(name="ACNH =", value="🍂", inline=False)
        embed.set_footer(text="Poll will end in 1 hour.")
        poll = await ctx.send(embed=embed)
        await poll.add_reaction('🎮')
        await poll.add_reaction('💻')
        await poll.add_reaction('🐀')    
        await poll.add_reaction('🍂')

    client.ycomm1 = 0
    client.lan1 = 0
    client.lgpe1 = 0
    client.acnh1 = 0

    @commands.group(invoke_without_command=True)
    async def vote(ctx):
        await ctx.message.delete()
        await ctx.send('Choices are: ycomm, lan, lgpe, and acnh.')

    @vote.group()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def ycomm(ctx):
        await ctx.message.delete()
        client.ycomm += 1
        await ctx.author.send('You voted for y-comm mode.')

    @vote.group()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def lan(ctx):
        await ctx.message.delete()
        client.lan += 1
        await ctx.author.send('You voted for LAN mode.')

    @vote.group()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def lgpe(ctx):
        await ctx.message.delete()
        client.lgpe += 1
        await ctx.author.send('You voted for LGPE mode.')

    @vote.group()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def acnh(ctx):
        await ctx.message.delete()
        client.acnh += 1
        await ctx.author.send('You voted for acnh.')

    @vote.group()
    @commands.is_owner()
    async def results(ctx):
        await ctx.send(f'**__Current Votes:__**\nY-Comm: {client.ycomm}\nLAN: {client.lan}\nLGPE:{client.lgpe}\nACNH:{client.acnh}')

    @vote.group()
    @commands.is_owner()
    async def clear(ctx):
        client.ycomm = 0
        client.lan = 0 
        client.lgpe = 0
        client.acnh = 0
        await ctx.send('Tallys were reset.')


def setup(client):
    client.add_cog(Polling(client))
