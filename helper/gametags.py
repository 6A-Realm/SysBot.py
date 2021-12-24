from discord.ext import commands
import json
    
class tag(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Public Commands --}
    @commands.command()
    @commands.guild_only()
    async def addtag(self, ctx, *, t): 
        with open('res/tags.json', 'r') as f: 
            codes = json.load(f) 
        if str(ctx.message.author.id) in codes:
            await ctx.send("Use the `change` command to edit your tag.")
        else:
            codes[str(ctx.message.author.id)] = t
            with open('res/tags.json', 'w') as f: 
                json.dump(codes, f, indent=4) 
            await ctx.send(f"`{t}` added.")

    @commands.command()
    async def mytag(self, ctx): 
        with open('res/tags.json', 'r') as f:
            codes = json.load(f)
        if str(ctx.message.author.id) in codes:
            await ctx.send(f"Your tag is `{codes[str(ctx.message.author.id)]}`.")
        else: 
            await ctx.send("Create your own tag using `addtag`.")

    @commands.command()
    @commands.guild_only()
    async def changetag(self, ctx, *, t): 
        with open('res/tags.json', 'r') as f:
            codes = json.load(f)
        codes[str(ctx.message.author.id)] = t
        with open('res/tags.json', 'w') as f: 
            json.dump(codes, f, indent=4)
        await ctx.send(f'Your tag has been changed to: `{t}`') 

    @commands.command()
    @commands.guild_only()
    async def removetag(self, ctx): 
        with open('res/tags.json', 'r') as f:
            codes = json.load(f)
        codes.pop(str(ctx.message.author.id))
        with open('res/tags.json', 'w') as f:
            json.dump(codes, f, indent=4)
        await ctx.send("Your tag has been removed.")

    @commands.command()
    async def tag(self, ctx, * tag): 
        with open('res/tags.json', 'r') as f:
            codes = json.load(f)
        if str(tag) in codes:
            await ctx.send(f"<@{codes[str(tag)]}>")
        else: 
            return

def setup(client):
    client.add_cog(tag(client))
