import discord
from discord.ext import commands
from yaml import load
import io
from aiohttp_requests import requests
from json import loads
import json
from discord_components import Button, ButtonStyle

# API link
pinfo = "https://coreapi-production.up.railway.app/api/PokemonInfo"

# Loads values from config.yaml
with open("config.yaml") as file:
    data = load(file)
    botprefix = data["defaultprefix"]
    embedcolor = data["color"]
    support = data["support-server-name"]
    support2 = data["support-server-invite"]
    dmchannel = data["dmchannel"]

class EVENTS(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Forwards dms to specified channel dmchannel in config.yaml
    @commands.Cog.listener()
    async def on_message(self, message):

        #Ignore all bots
        if message.author.bot:
            return
            
        if isinstance(message.channel, discord.DMChannel):

            # Ignore arg
            if message.content.startswith('+'):
                return
            if message.attachments:                
                return message.channel.send("Please do not send files via dms.")

            channel = self.client.get_channel(dmchannel)
            embed=discord.Embed(title = f"**{message.author}** sent:", description = message.content, color = discord.Colour.random())
            embed.set_footer(text = f"Reply using {botprefix}directmessage {message.author.id}")
            await channel.send(embed=embed)    
            await self.client.process_commands(message)
            
        else:
            for attachment in message.attachments:                
                if attachment.filename.endswith((".eb8", ".pb8", ".pk6", ".pk7", ".ek8", ".pk8")) and message.content == "":

                    # Convert to bytes and save
                    buffer = io.BytesIO()
                    await attachment.save(buffer)
                    data = buffer.getvalue()

                    # Send to coreapi instance 
                    response = loads((await (await requests.post(pinfo, data={"pokemon": data})).content.read()).decode("utf-8"))
                    species = response["species"]
                    gender = response["gender"]
                    item = response["held_item"]
                    ability = response["ability"]
                    level = response["level"]
                    shiny = response["is_shiny"]

                    nature = response["nature"]

                    m1 = response["move1"]
                    m2 = response["move2"]
                    m3 = response["move3"]
                    m4 = response["move4"]

                    information = f"```{species} ({gender}) @ {item}\nAbility: {ability}\nLevel: {level}\nShiny: {shiny}\n{nature} Nature\n-{m1}\n-{m2}\n-{m3}\n-{m4}```"
                    await message.channel.send(information)
                    await self.client.process_commands(message)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
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
    async def on_guild_remove(self, guild):
        with open("res/prefix.json", "r") as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open("res/prefix.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        print(f"Client left {guild.name}")

def setup(client):
        client.add_cog(EVENTS(client))