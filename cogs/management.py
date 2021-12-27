import discord
from discord.ext import commands
import json
import asyncio

class admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def changeprefix(self, ctx, new):
        try:
            with open("res/prefix.json", "r") as f:
                prefixes = json.load(f)
            prefixes[str(ctx.guild.id)] = new
            with open("res/prefix.json", "w") as f:
                json.dump(prefixes, f, indent=4)
            await ctx.send(f"Prefix set to `{new}`.")
        except:
            await ctx.send("Unable to change the prefix at this time.")

    @commands.command(help="Prevents members from type in used channel.", brief='lock')
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel : discord.TextChannel=None):
            channel = channel or ctx.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await ctx.message.delete()
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send(':red_circle: **Channel locked.** This bot is offline, please use one of the other bots.')
            if ctx.channel.id == 860765383908655144:
                down = discord.Embed(title="LGPE Bot Is Down!", description=f"Many users have been experiencing bot disconnection, meaning that they cannot complete their trades. This means the bot has crashed; therefore, this channel has been locked.\n\n\n**Do not DM anyone about the bot. Do not ask when the bot will be up.**\n\n\nRemember, this is a free service that nobody else offers. This is also something that the other sysbot creators said would be impossible to make.\n\n\nThank you for waiting patiently.", colour=discord.Colour.orange())
                down.set_footer(text="Failure to follow bolded line will result in a ban.")  
                await ctx.send(embed = down)

    @commands.command(help="Allows members to type in used channel.", brief='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : discord.TextChannel=None):
            channel = channel or ctx.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = True
            await ctx.message.delete()
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send(':green_circle: **Channel unlocked.** This bot is now online and ready to use.')

    @commands.command(aliases=['repeat'])
    @commands.has_permissions(manage_channels=True)
    async def say(self, ctx,*,message):
        await ctx.send(f"{message}")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def purge(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit+1)
        response = await ctx.send(f'{limit} messages cleared by {ctx.author}')
        await asyncio.sleep(2)
        await response.delete()


    @commands.command(help="Sets a slowmode in used channel.", brief='slowmode <amount>')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def downmessage(self, ctx):
        down = discord.Embed(title="LGPE Bot Is Down!", description=f"Many users have been experiencing bot disconnection, meaning that they cannot complete their trades. This means the bot has crashed; therefore, this channel has been locked.\n\n\n**Do not DM anyone about the bot. Do not ask when the bot will be up.**\n\n\nRemember, this is a free service that nobody else offers. This is also something that the other sysbot creators said would be impossible to make.\n\n\nThank you for waiting patiently.", colour=discord.Colour.orange())
        down.set_footer(text="Failure to follow bolded line will result in a ban.")  
        await ctx.send(embed = down)


def setup(client):
    client.add_cog(admin(client))