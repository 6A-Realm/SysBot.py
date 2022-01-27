import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

class ERRORS(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Error Handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            pass
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You are missing required arguments.")
        if isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send("You were unclear with your arguments.")
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.send(f"You are on command cooldown. Try again in `{round(error.retry_after, 2)} seconds`.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You're missing the following permissions: \n**{', '.join(error.missing_permissions)}**")
        if isinstance(error, discord.ext.commands.errors.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
        if isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send("This member was not found.")
        if isinstance(error, discord.ext.commands.errors.GuildNotFound):
            await ctx.send("This guild was not found.")
        if isinstance(error, discord.ext.commands.errors.UserNotFound):
            await ctx.send("This user was not found.")
        if isinstance(error, discord.ext.commands.errors.ChannelNotFound):
            await ctx.send("This channel was not found.")
        if isinstance(error, discord.ext.commands.errors.RoleNotFound):
            await ctx.send("This role was not found.")
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"I'm missing the following permissions: \n**{', '.join(error.missing_permissions)}**")
        if isinstance(error, commands.NotOwner):
            await ctx.send("Only the owner of this bot can use that command.")


def setup(client):
        client.add_cog(ERRORS(client))