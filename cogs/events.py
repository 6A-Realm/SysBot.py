import discord
from discord.ext import commands
from yaml import load
import json
from discord_components import Button, ButtonStyle

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

    # Forwards dms to specified channel dmchannel in config.yaml
    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):

            # Ignore arg
            if message.author.bot:
                return
            if message.content.startswith('+'):
                return
            if message.attachments:                
                return message.channel.send("Please do not send files via dms.")

            channel = self.client.get_channel(dmchannel)
            embed=discord.Embed(title = f"**{message.author}** sent:", description = message.content, color = discord.Colour.random())
            embed.set_footer(text = f"Reply using {botprefix}directmessage {message.author.id}")
            await channel.send(embed=embed)    
            await self.client.process_commands(message)

    @commands.Cog.listener()
    async def on_guild_join(guild):
        # Add prefix
        with open("res/prefix.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = botprefix
        with open("res/prefix.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        # Welcome message in first channel that a message can be sent in
        welcomer = discord.Embed(title = 'Thanks for adding me!', description = f"Thank you for adding me to {guild.name}!\nYou can use the `{botprefix}help` command to get started!\nDon't forget to join our official server [{support}]({support2})", color=embedcolor)
        components = [
            [
                Button(label = 'Support Server', style = ButtonStyle.URL, url = support2)
            ]
        ]
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed = welcomer, components = components)
            break
        try:
            # Try to dm server owner
            await guild.owner.send(embed = welcomer)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(guild):
        with open("res/prefix.json", "r") as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open("res/prefix.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        print(f"Client left {guild.name}")

def setup(client):
        client.add_cog(Events(client))