import discord
from discord.ext import commands
import yaml
from yaml import load

# Simple file reader to load channels
with open("advanced/ban.yaml", encoding='utf-8') as file:
    data = load(file)
    channels = data["ban"]
    
class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

# {-- Moderation Commands --}
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        if reason is None:
            reason = 'No reason given'
        author = ctx.message.author
        if member and author.top_role.position < member.top_role.position + 1:
            return await ctx.send("You cannot kick members that have a higher role than you.")
        if member.permissions_in(ctx.channel).kick_members:
            return await ctx.send("That user is a mod/admin.")
        else:
            try:
                guild = self.client.get_guild(ctx.guild.id)
                try:
                    invitelink = ""
                    i = 0
                    while invitelink == "":
                        channel = guild.text_channels[i]
                        link = await channel.create_invite(max_age=0,max_uses=0)
                        invitelink = str(link)
                        i += 1
                except: 
                    invitelink = "Unable to create an invite."
                await member.send(f"You have been kicked from **{guild}**.\nThe reason given was: `{reason}`.\nAdditional kicks will result in a ban.\n{invitelink}")
            except discord.Forbidden:
                pass
            await member.kick(reason=reason)
            await ctx.send(f"{member.name} has been kicked for `{reason}`.")
  
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason = None):
        if reason is None:
            reason = 'No reason given'
        author = ctx.message.author
        if member:
            if author.top_role.position < member.top_role.position + 1:
                return await ctx.send("You cannot ban members that have a higher role than you.")
        if member.permissions_in(ctx.channel).ban_members:
            return await ctx.send("That user is a mod/admin.")
        else:
            try:
                guild = self.client.get_guild(ctx.guild.id)
                await member.send(f"You have been banned from **{guild}**.\nThe reason given was: `{reason}`.")
            except discord.Forbidden:
                pass
            await member.ban(reason=reason)
            await ctx.send(f"{member.name} has been banned for `{reason}`.")
  
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def shareban(self, ctx, member: discord.Member, *, reason = None):
        if reason is None:
            reason = 'No reason given'
        author = ctx.message.author
        if member:
            if author.top_role.position < member.top_role.position + 1:
                return await ctx.send("You cannot ban members that have a higher role than you.")
        if member.permissions_in(ctx.channel).ban_members:
            return await ctx.send("That user is a mod/admin.")
        else:
            try:
                guild = self.client.get_guild(ctx.guild.id)
                await member.send(f"You have been banned from **{guild}**.\nThe reason given was: `{reason}`.")
            except discord.Forbidden:
                pass
            await member.ban(reason=reason)
            await ctx.send(f"{member.name} has been banned for `{reason}`.")
            for chan in channels:
                channel = self.client.get_channel(chan)
                guild = self.client.get_guild(self.client.guild.name)
                embed = discord.Embed(title=f'{member.name} Has Been Banned', description=f"Server: {guild}\nReason: {reason}\nBy: {author.name}", color=0xD60FBB)
                await channel.send(embed = embed)
                ask = await channel.send(f"React with a hammer if you would you like to ban {member.name} from your server?")
                reaction = await self.client.wait_for_reaction(['\N{hammer}'], ask)
                sharereason = "Shared Banned:" + reason
                await member.ban(reason=sharereason)
                await channel.send(f"You responded with {reaction.emoji} so {member.name} was banned from this guild.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        bans = list(map(lambda e: e[1].id, await ctx.guild.bans()))
        if id not in bans:
            return await ctx.send("This user is not banned.")
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f'{user.name} was unbanned')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        guild = self.client.get_guild(ctx.guild.id)
        embed = discord.Embed(description=f"You have been warned in {guild} for: {reason}", color=0xD60FBB)
        await member.send(embed = embed)
        await ctx.send(f"{member.name} was warned.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member, *, rolename: str):
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
        if not role:
            await self.client.create_role(server = ctx.message.server, name = role)
        await member.add_roles(role)
        await ctx.send(f'Added: `{role.name}`')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member, *, rolename: str):
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
        if not role:
            return await ctx.send('That role does not exist.')
        await member.remove_roles(role)
        await ctx.send(f'Removed: `{role.name}`')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member:discord.Member, duration, *, reason = None):
        if reason is None:
            reason = 'No reason given'
        unit = duration[-1]
        if unit == 's':
            time = int(duration[:-1])
            longunit = 'seconds'
        elif unit == 'm':
            time = int(duration[:-1]) * 60
            longunit = 'minutes'
        elif unit == 'h':
            time = int(duration[:-1]) * 60 * 60
            longunit = 'hours'
        else:
            await ctx.send('Invalid Unit! Use `s`, `m`, or `h`.')
            return
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
        for channel in ctx.guild.voice_channels:
            await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
        await ctx.send(f"{member} was muted for {time} {longunit}.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member, *, reason = None):
        if reason is None:
            reason = 'No reason given'
        for channel in ctx.message.guild.channels:
            await channel.set_permissions(member, overwrite=None, reason=reason)
            await ctx.send("Member unmuted")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def category(self, ctx, channel: int, category):
        channel = self.client.get_channel(channel)
        if channel:
            await channel.edit(category = category)
            await ctx.send(f"{channel.name} was moved to {category}.")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def addban(self, ctx):
        channel = ctx.message.channel.id
        with open("advanced/ban.yaml", encoding='utf-8') as file:
            data = load(file)
        if channel in data["ban"]:
            await ctx.send('This channel is already listed in the ban notifications list.')
        else:
            data["ban"].append(channel)
            channels.append(channel)
            with open('advanced/ban.yaml', 'w') as writer:
                yaml.dump(data, writer)
            await ctx.send('This channel has been added')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def removeban(self, ctx):
        channel = ctx.message.channel.id
        with open("advanced/ban.yaml", encoding='utf-8') as file:
            data = load(file)
        data["ban"].remove(channel)
        channels.remove(channel)
        with open('advanced/ban.yaml', 'w') as writer:
            yaml.dump(data, writer)
        await ctx.send('This channel has been removed.')


def setup(client):
    client.add_cog(Moderation(client))