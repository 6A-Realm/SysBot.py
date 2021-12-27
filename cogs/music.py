import discord
from discord.ext import commands
import DiscordUtils

music = DiscordUtils.Music()

async def check(ctx):
    if ctx.member.voice is None:
        embed = discord.Embed(description="You are required to be in a voice channel to use this command.", color = discord.Colour.red)
        return await ctx.send(embed = embed)

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def play(self, ctx, *, url):
        check(ctx)
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        if voice == None:
            await ctx.author.voice.channel.connect() 
        else:
            pass
        msg = await ctx.send(f"Searching for {url}...")
        player = music.get_player(guild_id = ctx.guild.id)
        if not player:
            player = music.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_client.is_playing():
            await player.queue(url, search=True)
            song = await player.play()
            await msg.edit(f"Now Playing: **{song.name}**.")
        else:
            song = await player.queue(url, search=True)
            await msg.edit(f"Added **{song.name}** to music queue.")

    @commands.command()
    async def pause(self, ctx):
        await check(ctx)
        player = music.get_player(guild_id = ctx.guild.id)
        song = await player.pause()
        await ctx.reply(f"**{song.name}** has been paused.")

    @commands.command()
    async def resume(self, ctx):
        player = music.get_player(guild_id = ctx.guild.id)
        song = await player.resume()
        await ctx.send(f"**{song.name}** has been resumed.")

    @commands.command()
    async def volume(self, ctx, vol):
        player = music.get_player(guild_id=ctx.guild.id)
        song, volume = await player.change_volume(float(vol) / 100)
        await ctx.send(f"Volume changed to {volume*100}%")

    @commands.command()
    async def loop(self, ctx):
        player = music.get_player(guild_id = ctx.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.message.add_reaction("✓")
        else:
            await ctx.send(f"No longer looping **{song.name}**")

    @commands.command()
    async def musicqueue(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        queue = []
        enter = '\n'
        counter = 0
        for song in player.current_queue():
            counter +=1
            queue.append(f"{counter}) [{song.name}]({song.url})")
        embed = discord.Embed(title="Music Queue", description=f"{enter.join(ch for ch in queue)}", color = ctx.author.color)
        await ctx.send(embed = embed)

    @commands.command()
    async def skip(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        data = await player.skip(force=True)
        await ctx.send(f"Skipped **{data[0].name}**.")

    @commands.command()
    @commands.has_permissions(move_members=True)
    async def resetqueue(self, ctx, index):
        player = music.get_player(guild_id = ctx.guild.id)
        for song in player.current_queue():
            await player.remove_from_queue(int(index))
        await ctx.send(f"Queue cleared.")


def setup(client):
    client.add_cog(music(client))