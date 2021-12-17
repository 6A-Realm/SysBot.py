import discord
import discord.ext.commands as commands
import json
import time

def setup(bot):
    bot.add_cog(extensions(bot))


def duration_to_str(duration):
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    duration = []
    if days > 0: duration.append(f'{days} days')
    if hours > 0: duration.append(f'{hours} hours')
    if minutes > 0: duration.append(f'{minutes} minutes')
    if seconds > 0 or len(duration) == 0: duration.append(f'{seconds} seconds')

    return ', '.join(duration)


class extensions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.start_time = time.time()

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, name):
        cog = name.lower()
        try:
            ctx.bot.load_extension(f'cogs.{cog}')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'Extension {name} already loaded.')
        except commands.ExtensionNotFound:
            await ctx.send(f'Extension {name} not found.')
        else:
            self.bot.conf['extensions'].append(cog)
            with open(self.bot.conf_file, 'w') as fp:
                json.dump(self.bot.conf, fp)
            await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, name):
        cog = name.lower()
        try:
            ctx.bot.unload_extension(f'cogs.{cog}')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'Extension {name} not loaded.')
        else:
            self.bot.conf['extensions'].remove(cog)
            with open(self.bot.conf_file, 'w') as fp:
                json.dump(self.bot.conf, fp)
            await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *extensions):
        if extensions is None:
            extensions = self.bot.conf['extensions']

        for name in extensions:
            cog = name.lower()
            try:
                ctx.bot.unload_extension(f'cogs.{cog}')
                ctx.bot.load_extension(f'cogs.{cog}')
            except commands.ExtensionError as e:
                await ctx.send(f'Error reloading extension {name} : {e}')

        await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')