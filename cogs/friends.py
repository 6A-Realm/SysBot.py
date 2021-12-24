from discord.ext import commands
import json
    
class friend(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Public Commands --}
    @commands.command()
    @commands.guild_only()
    async def addcode(self, ctx, *, fc): 
        with open('res/friendcodes.json', 'r') as f: 
            codes = json.load(f) 
        if str(ctx.message.author.id) in codes:
            await ctx.send("Use the `changecode` command to edit your friend-code.")
        else:
            codes[str(ctx.message.author.id)] = fc
            with open('res/friendcodes.json', 'w') as f: 
                json.dump(codes, f, indent=4) 
            await ctx.send(f"`{fc}` added.")

    @commands.command()
    async def fcode(self, ctx): 
        with open('res/friendcodes.json', 'r') as f:
            codes = json.load(f)
        if str(ctx.message.author.id) in codes:
            await ctx.send(f"Your friend code is `{codes[str(ctx.message.author.id)]}`.")
        else: 
            await ctx.send("Add your friend-code using `addcode`.")

    @commands.command()
    @commands.guild_only()
    async def changecode(self, ctx, *, fc): 
        with open('res/friendcodes.json', 'r') as f:
            codes = json.load(f)
        codes[str(ctx.message.author.id)] = fc
        with open('res/friendcodes.json', 'w') as f: 
            json.dump(codes, f, indent=4)
        await ctx.send(f'Your friend-code has been changed to: `{fc}`') 

    @commands.command()
    @commands.guild_only()
    async def removecode(self, ctx): 
        with open('res/friendcodes.json', 'r') as f:
            codes = json.load(f)
        codes.pop(str(ctx.message.author.id))
        with open('res/friendcodes.json', 'w') as f:
            json.dump(codes, f, indent=4)
        await ctx.send("Your friend-code has been removed.")


def setup(client):
    client.add_cog(friend(client))
