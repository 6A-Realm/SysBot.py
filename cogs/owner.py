import discord
from discord.ext import commands

class owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, help="Sends message to directed user.", brief="directmessage <userid> <message>")
    @commands.is_owner()
    async def directmessage(self, ctx, user: discord.User, *, content):
        direct = await user.create_dm()
        await ctx.message.delete()
        await direct.send(content)
        
    @commands.command(help="Sends message to directed channel.", brief="send <channelid> <message>")
    @commands.is_owner()
    async def send(self, ctx, channel: int, *,message):
        channel = self.client.get_channel(channel)
        if channel:
            await channel.send(f"{message}")

    @commands.command(help="List all servers the bot is in, including name, guild ID, owner, and invite.", brief="list")
    @commands.is_owner()
    async def list(self, ctx):
            servernames = []
            enter = '\n'
            counter = 0
            for guild in self.client.guilds:
                counter += 1
                guild = self.client.get_guild(guild.id)
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
                servernames.append(f"{counter}) [{guild.name}]({invitelink}) ⋅ {guild.id} ⋅ {guild.owner}")
            embed = discord.Embed(title=f"{self.client.user.name}'s Servers", description=f"{enter.join(ch for ch in servernames)}", colour=discord.Colour.dark_blue())
            await ctx.send(embed = embed)

    @commands.command(help="Leaves server from directed guild.", brief="leave <serverid>")
    @commands.is_owner()
    async def leave(self, ctx, guild_id):
        await self.client.get_guild(int(guild_id)).leave()
        await ctx.send(f"I left {guild_id}.")

    @commands.command(help="Create a guild.", brief="createguild <prefered name>")
    @commands.is_owner()
    async def createguild(self, ctx, *, name):
        await self.client.create_guild(name)
        await ctx.send(f"I created {name}.")

    @commands.command(help="deletes server from directed guild.", brief="delete <serverid>")
    @commands.is_owner()
    async def deleteguild(self, ctx, guild_id):
        try:
            await self.client.get_guild(int(guild_id)).delete()
            await ctx.send(f"I deleted {guild_id}.")
        except: 
            await ctx.send(f"I am not the owner of {guild_id}.")
                     
    @commands.command(help="Renames the bot's name.", brief='rename <desiredname>')
    @commands.is_owner()
    async def rename(self, ctx, *, message):
        try: 
            await self.client.user.edit(username=message)
            await ctx.send(f"Name changed to {message}")
        except Exception as e:
            await ctx.send(e)

    @commands.command(help="Change the bot's pfp.", brief='repfp <attached image>')
    @commands.is_owner()
    async def repfp(self, ctx):
        try: 
            for attachment in ctx.message.attachments:
                await attachment.save(f"res/newpfp.jpg")
            with open("res/newpfp.jpg", "rb") as image:
                f = image.read()
                b = bytearray(f) 
                await self.client.user.edit(avatar=b)
                await ctx.send('Avatar is changed.')
        except:
            ctx.send("An error has occured while changing pfps.")

    @commands.command()
    @commands.is_owner()
    async def botinvite(self, ctx):
        await ctx.send(f'https://discord.com/oauth2/authorize?client_id={self.client.user.id}&permissions=67496977&scope=bot%20applications.commands')

    @commands.command(aliases=['kill'])
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down helper.py... bye bye")
        await self.client.logout()

def setup(client):
    client.add_cog(owner(client))