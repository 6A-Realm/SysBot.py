import discord
from discord.ext import commands
import json
    
class Friend(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Public Commands --}
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def addcode(self, ctx, version = None, fc = None):
        if version is None and fc is None: 
            await ctx.send("Use the command addcode <version> <fcode> to enter your friend code. Versions are switch, 3ds, and home.")
        
        if version is not None and fc is None:
            await ctx.send("Incorrect usage. No friend code defined.")
        
        if version == "switch" and fc is not None:
            with open('res/friendcodes-switch.json', 'r') as f: 
                codes = json.load(f) 
            if str(ctx.message.author.id) in codes:
                codes.pop(str(ctx.message.author.id))
                with open('res/friendcodes-switch.json', 'w') as f:
                    json.dump(codes, f, indent=4)
            codes[str(ctx.message.author.id)] = fc
            with open('res/friendcodes-switch.json', 'w') as f: 
                json.dump(codes, f, indent=4) 
            await ctx.send(f"`{fc}` added.")
        
        if version == "3ds" and fc is not None:
            with open('res/friendcodes-ds.json', 'r') as f: 
                codes = json.load(f) 
            if str(ctx.message.author.id) in codes:
                codes.pop(str(ctx.message.author.id))
                with open('res/friendcodes-switch.json', 'w') as f:
                    json.dump(codes, f, indent=4)
            codes[str(ctx.message.author.id)] = fc
            with open('res/friendcodes-ds.json', 'w') as f: 
                json.dump(codes, f, indent=4) 
            await ctx.send(f"`{fc}` added.")

        if version == "home" and fc is not None:
            with open('res/friendcodes-home.json', 'r') as f: 
                codes = json.load(f) 
            if str(ctx.message.author.id) in codes:
                codes.pop(str(ctx.message.author.id))
                with open('res/friendcodes-switch.json', 'w') as f:
                    json.dump(codes, f, indent=4)
            codes[str(ctx.message.author.id)] = fc
            with open('res/friendcodes-home.json', 'w') as f: 
                json.dump(codes, f, indent=4) 
            await ctx.send(f"`{fc}` added.")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def removecode(self, ctx, version = None): 
        if version is None:
            await ctx.send("Use the command removecode <version> delete your friend code. Versions are switch, 3ds, and home.")
        
        if version == "switch":
            try:
                with open('res/friendcodes-switch.json', 'r') as f:
                    codes = json.load(f)
                codes.pop(str(ctx.message.author.id))
                with open('res/friendcodes-switch.json', 'w') as f:
                    json.dump(codes, f, indent=4)
                await ctx.send("Your friend-code has been removed.")
            except:
                await ctx.send("You do not have a friend-code for this game version.")

        if version == "3ds":
            try:
                with open('res/friendcodes-ds.json', 'r') as f:
                    codes = json.load(f)
                codes.pop(str(ctx.message.author.id))
                with open('res/friendcodes-ds.json', 'w') as f:
                    json.dump(codes, f, indent=4)
                await ctx.send("Your friend-code has been removed.")
            except:
                await ctx.send("You do not have a friend-code for this game version.")

        if version == "home":
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
        embed = discord.Embed(title = f'Your friend codes', description = "Your saved friend codes are listed below.", color = ctx.author.color)
        with open('res/friendcodes-switch.json', 'r') as f:
            codes = json.load(f)
        if str(ctx.message.author.id) in codes:
            embed.add_field(name = "__Switch:__", value = str(codes[str(ctx.message.author.id)]), inline=False)
        with open('res/friendcodes-ds.json', 'r') as f:
            codes = json.load(f)
        if str(ctx.message.author.id) in codes:
            embed.add_field(name = "__3DS:__", value = str(codes[str(ctx.message.author.id)]), inline=False)
        with open('res/friendcodes-home.json', 'r') as f:
            codes = json.load(f)
        if str(ctx.message.author.id) in codes:
            embed.add_field(name = "__Home:__", value= str(codes[str(ctx.message.author.id)]), inline=False)
        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Friend(client))