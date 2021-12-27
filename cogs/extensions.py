import discord.ext.commands as commands

class extensions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        cog = extension.lower()
        try:
            ctx.client.load_extension(f'cogs.{cog}')
        except commands.ExtensionAlreadyLoaded:
            await ctx.reply(f'Extension {cog} already loaded.')
        except commands.ExtensionNotFound:
            await ctx.reply(f'Extension {cog} not found.')
        else:
            await ctx.reply(f"Error reloading {cog}.")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        cog = extension.lower()
        try:
            ctx.client.unload_extension(f'cogs.{cog}')
        except commands.ExtensionNotLoaded:
            await ctx.reply(f'Extension {cog} not loaded.')
        else:
            await ctx.reply(f"Error reloading {cog}.")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        cog = extension.lower()
        try:
            ctx.client.unload_extension(f'cogs.{cog}')
            ctx.client.load_extension(f'cogs.{cog}')
            await ctx.reply(f"{cog} reloaded.")
        except commands.ExtensionError as e:
            await ctx.reply(f"Error reloading {cog}.")


def setup(client):
    client.add_cog(extensions(client))