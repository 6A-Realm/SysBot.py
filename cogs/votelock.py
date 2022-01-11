import discord
from discord.ext import commands

voted = []
votes = []

class votelock(commands.Cog):
    def __init__(self, client):
        self.client = client


# {-- Public Commands --}
    @commands.command()
    async def votelock(self, ctx):
        user = ctx.message.author.id
        channel = ctx.message.channel.id
        name = ctx.message.author.name
        counter = votes.count(channel)

        if ctx.message.author.id in voted:
            return await ctx.send(f"You've already voted to lock down a channel. {votes.count(channel)}/3 votes have been recorded.")

        voted.append(user)
        votes.append(channel)

        if counter <3:
            await ctx.message.delete()
            await ctx.send("{} voted to lock this channel. {}/3 votes have been recorded.".format(name, votes.count(channel)))
        if counter >=3:
            await ctx.message.delete()
            overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send(':red_circle: **Channel locked.** This bot is offline, please use one of the other bots.')
            down = discord.Embed(title="Bot Is Down!", description=f"Many users have been experiencing bot disconnection, meaning that they cannot complete their trades. This means the bot has crashed; therefore, this channel has been locked.\n\n\n**Do not DM anyone about the bot. Do not ask when the bot will be up.**\n\n\nRemember, this is a free service that nobody else offers. This is also something that the other sysbot creators said would be impossible to make.\n\n\nThank you for waiting patiently.", colour=discord.Colour.orange())
            down.set_footer(text="Failure to follow bolded line will result in a ban.")  
            await ctx.send(embed = down)
            while(True):
                if votes != 0 or voted != 0:
                    votes.clear()
                    voted.clear()
                else:
                    return

# {-- Admin Commands --}
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def clearvotes(self, ctx):
        voted.clear()
        votes.clear()
        await ctx.send('Votes have reset to 0.')


def setup(client):
    client.add_cog(votelock(client))