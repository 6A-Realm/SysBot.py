import discord
from discord.ext import commands
from yaml import load
import json

# Loads values from config.yaml
with open("config.yaml") as file:
    data = load(file)
    botprefix = data["botprefix"]
    embedcolor = data["color"]
    support = data["support-server-name"]
    support2 = data["support-server-invite"]
    dmchannel = data["dmchannel"]

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            if message.author.bot:
                return
            if message.content.startswith('+'):
                return
            channel = self.client.get_channel(dmchannel)
            embed=discord.Embed(title=f"**{message.author}** ({message.author.id}) sent:", description=f"```{message.content}```", color=0x0d1d96)
            embed.set_footer(text=f"Reply using the command .directmessage {message.author.id}")
            await channel.send(embed=embed)    
            await self.client.process_commands(message)

    @commands.Cog.listener()
    async def on_guild_join(guild):
        welcomer = discord.Embed(title = 'Thanks for adding me!', description = f"Thank you for adding me to {guild.name}!\nYou can use the `{botprefix}help` command to get started!\nDont forget to join our official server [{support}]({support2})", color=embedcolor)
        welcomer.set_footer(text=support2)
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed = welcomer)
            break
        try:
            await guild.owner.send(embed = welcomer)
        except:
            pass
        with open("res/prefix.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = botprefix
        with open("res/prefix.json", "w") as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(guild):
        with open("res/prefix.json", "r") as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open("res/prefix.json", "w") as f:
            json.dump(prefixes, f, indent=4)

def setup(client):
        client.add_cog(Events(client))