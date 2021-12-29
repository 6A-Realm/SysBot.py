import discord
from discord.ext import commands
import json
    
class friend(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Public Commands --}
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def addcode(self, ctx): 
        await ctx.send("Use the command addcode <version> <fcode> to enter your friend code. Versions are switch, ds, and home.")

    @addcode.group()
    @commands.guild_only()
    async def switch(self, ctx, *, fc): 
        with open('res/friendcodes-switch.json', 'r') as f: 
            codes = json.load(f) 
        if str(ctx.message.author.id) in codes:
            await ctx.send("Use the `change switch` command to edit your friend-code.")
        else:
            codes[str(ctx.message.author.id)] = fc
            with open('res/friendcodes-switch.json', 'w') as f: 
                json.dump(codes, f, indent=4) 
            await ctx.send(f"`{fc}` added.")

    @addcode.group()
    @commands.guild_only()
    async def ds(self, ctx, *, fc): 
        with open('res/friendcodes-ds.json', 'r') as f: 
            codes = json.load(f) 
        if str(ctx.message.author.id) in codes:
            await ctx.send("Use the `change ds` command to edit your friend-code.")
        else:
            codes[str(ctx.message.author.id)] = fc
            with open('res/friendcodes-ds.json', 'w') as f: 
                json.dump(codes, f, indent=4) 
            await ctx.send(f"`{fc}` added.")

    @addcode.group()
    @commands.guild_only()
    async def home(self, ctx, *, fc): 
        with open('res/friendcodes-home.json', 'r') as f: 
            codes = json.load(f) 
        if str(ctx.message.author.id) in codes:
            await ctx.send("Use the `change home` command to edit your friend-code.")
        else:
            codes[str(ctx.message.author.id)] = fc
            with open('res/friendcodes-home.json', 'w') as f: 
                json.dump(codes, f, indent=4) 
            await ctx.send(f"`{fc}` added.")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def change(self, ctx): 
        await ctx.send("Use the command change <version> <fcode> to enter your friend code. Versions are switch, ds, and home.")

    @change.group()
    @commands.guild_only()
    async def switch(self, ctx, *, fc): 
        with open('res/friendcodes-switch.json', 'r') as f:
            codes = json.load(f)
        codes[str(ctx.message.author.id)] = fc
        with open('res/friendcodes-switch.json', 'w') as f: 
            json.dump(codes, f, indent=4)
        await ctx.send(f'Your friend-code has been changed to: `{fc}`') 

    @change.group()
    @commands.guild_only()
    async def ds(self, ctx, *, fc): 
        with open('res/friendcodes-ds.json', 'r') as f:
            codes = json.load(f)
        codes[str(ctx.message.author.id)] = fc
        with open('res/friendcodes-ds.json', 'w') as f: 
            json.dump(codes, f, indent=4)
        await ctx.send(f'Your friend-code has been changed to: `{fc}`') 

    @change.group()
    @commands.guild_only()
    async def home(self, ctx, *, fc): 
        with open('res/friendcodes-home.json', 'r') as f:
            codes = json.load(f)
        codes[str(ctx.message.author.id)] = fc
        with open('res/friendcodes-home.json', 'w') as f: 
            json.dump(codes, f, indent=4)
        await ctx.send(f'Your friend-code has been changed to: `{fc}`') 

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def removecode(self, ctx): 
        await ctx.send("Use the command removecode <version> delete your friend code. Versions are switch, ds, and home.")

    @removecode.group()
    @commands.guild_only()
    async def switch(self, ctx): 
        try:
            with open('res/friendcodes-switch.json', 'r') as f:
                codes = json.load(f)
            codes.pop(str(ctx.message.author.id))
            with open('res/friendcodes-switch.json', 'w') as f:
                json.dump(codes, f, indent=4)
            await ctx.send("Your friend-code has been removed.")
        except:
            await ctx.send("You do not have a friend-code for this game version.")

    @removecode.group()
    @commands.guild_only()
    async def ds(self, ctx): 
        try:
            with open('res/friendcodes-ds.json', 'r') as f:
                codes = json.load(f)
            codes.pop(str(ctx.message.author.id))
            with open('res/friendcodes-ds.json', 'w') as f:
                json.dump(codes, f, indent=4)
            await ctx.send("Your friend-code has been removed.")
        except:
            await ctx.send("You do not have a friend-code for this game version.")

    @removecode.group()
    @commands.guild_only()
    async def home(self, ctx): 
        try:
            with open('res/friendcodes-home.json', 'r') as f:
                codes = json.load(f)
            codes.pop(str(ctx.message.author.id))
            with open('res/friendcodes-home.json', 'w') as f:
                json.dump(codes, f, indent=4)
            await ctx.send("Your friend-code has been removed.")
        except:
            await ctx.send("You do not have a friend-code for this game version.")

    @commands.command()
    async def fcode(self, ctx):
        embed=discord.Embed(title=f'Your friend codes', description="Your saved friend codes are listed below.", color=ctx.author.color)
        with open('res/friendcodes-switch.json', 'r') as f:
            codes = json.load(f)
        if str(ctx.message.author.id) in codes:
            embed.add_field(name="Switch:", value={codes[str(ctx.message.author.id)]}, inline=False)
        else: 
            pass
        with open('res/friendcodes-ds.json', 'r') as f:
            codes = json.load(f)
        if str(ctx.message.author.id) in codes:
            embed.add_field(name="DS::", value={codes[str(ctx.message.author.id)]}, inline=False)
        else: 
            pass        
        with open('res/friendcodes-home.json', 'r') as f:
            codes = json.load(f)
        if str(ctx.message.author.id) in codes:
            embed.add_field(name="Home:", value={codes[str(ctx.message.author.id)]}, inline=False)
        else: 
            pass


def setup(client):
    client.add_cog(friend(client))
