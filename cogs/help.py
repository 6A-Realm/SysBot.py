import discord
from discord.ext import commands
from yaml import load
from discord_components import DiscordComponents, SelectOption, Select, Button, ButtonStyle
import asyncio

with open("config.yaml") as file:
    data = load(file)
    botprefix = data["botprefix"]
    support2 = data["support-server-invite"]

ttr = str(f"""
```yaml
Prefix: {botprefix} - Required Parameter: <> - Optional Parameter: ()
```
""")

sysbotval = str(f"""
 ⋅ testtradetest `<eb8>`: Request a pokemon from the bot.
 ⋅ guide: Shows a video on how to use SysBot.
 ⋅ languide: Shows instructions on how to download LAN play.
 ⋅ lgpe: Shows a video on how to use the LGPE SysBot.
 ⋅ queue: Sends you current queue position.
 ⋅ queue list: Displays the total queue list.
 ⋅ queue leave: Requests to leave the queue.
""")

filesval = str(f"""
 ⋅ pk8 `<pokemon>`: Sends a `pk8` file.
 ⋅ ek8 `<pokemon>`: Sends a `ek8` file.
 ⋅ pk7 `<pokemon>`: Sends a `pk7` file.
 ⋅ pk6 `<pokemon>`: Sends a `pk6` file.
 ⋅ pb8 `<pokemon>`: Sends a `eb8` file.
 ⋅ eb8 `<pokemon>`: Sends a `eb8` file.
 ⋅ pb7 `<pokemon>`: Sends a `pb7` file.
""")

miscellaneousval = str(f"""
 ⋅ prefix: Fetchs the bot's prefix.
 ⋅ latency: Reports latency.
 ⋅ invite: Sends invite link to bot's home server.
 ⋅ support: Sends bot's donation link.
 ⋅ vote: Vote for a SysBot mode.
 ⋅ votelock: 3 votes will lock the channel the command is used in.
 ⋅ addcode: Saves your friend code.
 ⋅ fcode: Shows saved your friend code.
 ⋅ changecode: Changes your friend code.
 ⋅ removecode: Deletes your friend code.
""")

chanval = str(f"""
 ⋅ lock: Prevents members from type in used channel.
 ⋅ unlock: Allows members from type in used channel.
 ⋅ say <message>: Sends invite link to bot's home server.
 ⋅ purge <amount>: Bot repeats message.
 ⋅ slowmode <amount>: Changes the slowmode of used channel.
 ⋅ add: Adds channel to bot's announcement notification list.
 ⋅ remove: Removes channel from bot's announcement notification list.
""")

modval = str(f"""
 ⋅ kick  <member> (reason): Kicks mentioned member.
 ⋅ ban  <member> (reason): Bans mentioned member.
 ⋅ shareban <member> (reason): Bans mentioned member and announces in all linked channels.
 ⋅ unban <member>: Unbans mentioned member.
 ⋅ userinfo <member>: Displays mentioned member's info.
 ⋅ warn <member> <reason>: Warns mentioned member.
 ⋅ addrole <member> <role>: Gives mentioned member a role.
 ⋅ removerole <member> <role>: Removes mentioned member a role.
 ⋅ mute <member> <duration> (reason): Mutes mentioned member for said duration.
 ⋅ unmute <member>: Unmutes member.
 ⋅ category <channel> <category>: Moves the channels category location.
 ⋅ addban: Adds channel to bot's shareban notification list.
 ⋅ removeban: Removes channel from bot's shareban notification list.
""")

remoteval = str(f"""
 ⋅ click (x, a, b, or y): Tells switch to click selected button.
 ⋅ spamb: Tells switch to spam press the b button.
 ⋅ click (up, right, down, left): Tells switch which direction to move.
 ⋅ click (plus. minus, home): Clicks selected hotkey on switch.
 ⋅ pokemon (inject, dump): Dumps or injects pokemon into box 1 slot 1.
 ⋅ screen (on, off, shot, capture, percent): Controls the switch screen.
 ⋅ reconnect: Attempts to reconnect to your switch.
""")

ownerval = str(f"""
 ⋅ boton <message>: Sends a bot online message.
 ⋅ announcment <message>: Sends an announcement message.
 ⋅ botdown <message>: Sends a bot offline message.
 ⋅ redact <amount>: Redacts desired amount of announcement messages.
 ⋅ addsudo <member>: Adds member to sudo list.
 ⋅ removesudo <member>: Removes member from sudo list.
 ⋅ blacklist <member>: Saves your friend code.
 ⋅ unblacklist <member>: Shows saved your friend code.
 ⋅ loghere: Adds channel to logging output.
 ⋅ dontlog: Removes channel from logging output.
""")

botmanval = str(f"""
 ⋅ directmessage <userid> <content>: Sends message to directed user.
 ⋅ send <channelid> <content>: Sends message to directed channel.
 ⋅ list: List all servers the bot is in, including name, guild ID, owner, and invite.
 ⋅ leave <guildid>: Leaves server from directed guild.
 ⋅ createguild <name>: Creates a guild.
 ⋅ deleteguild <guildid>: Deletes an owned guild.
 ⋅ rename <name>: Renames the bot's name.
 ⋅ repfp <image>: Change the bot's pfp.
 ⋅ botinvite: Generates a bot invite.
 ⋅ load <cog>: Loads a cog.
 ⋅ reload <cog>: Reloads a cog.
 ⋅ unload <cog>: Unloads a cog.
 ⋅ restart: Restarts the bot.
 ⋅ shutdown: Turns off the bot.
""")

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
        DiscordComponents(self.client)

    @commands.command()
    async def help(self, ctx):

        # Embeds
        embed=discord.Embed(title=f'{self.client.user.name} Commands', description=f"Utilize the dropdown menu to select help pages.{ttr}", color= ctx.author.color)
        embed.add_field(name="**Help Modules:**", value="**Page 1** | SysBot Commands\n**Page 2** | Pokemon Files Commands\n**Page 3** | Miscellaneous Commands\n**Page 4** | Channel Management Commands\n**Page 5** | Moderation Commands\n**Page 6** | Switch Commands\n**Page 7** | Owner Commands\n**Page 8** | Bot Management Commands", inline=True)
        embed.add_field(name="📢 Bot News", value="⋅ Help command has been added.", inline=True)
        sysbot=discord.Embed(title=f'SysBot Module', description=ttr, color=ctx.author.color)
        sysbot.add_field(name="SysBot Commands", value=sysbotval, inline=True)
        files=discord.Embed(title=f'Files Module', description=ttr, color=ctx.author.color)
        files.add_field(name="Pkx and Ekx Search Commands", value=filesval, inline=True)
        general=discord.Embed(title=f'Miscellaneous Module', description=ttr, color=ctx.author.color)
        general.add_field(name="General Commands", value=miscellaneousval, inline=True)
        amanagement=discord.Embed(title=f'Channel Management Module', description=ttr, color=ctx.author.color)
        amanagement.add_field(name="Channel Commands", value=chanval, inline=True)
        moderation=discord.Embed(title=f'Moderation Module', description=ttr, color=ctx.author.color)
        moderation.add_field(name="Server Moderation Commands", value=modval, inline=True)
        sremote=discord.Embed(title=f'Switch Module', description=ttr, color=ctx.author.color)
        sremote.add_field(name="Switch Remote Control Commands", value=remoteval, inline=True)
        owner=discord.Embed(title=f'Owner Module', description=ttr, color=ctx.author.color)
        owner.add_field(name="Owner Only Commands", value=ownerval, inline=True)
        omanagement=discord.Embed(title=f'Bot Management Module', description=ttr, color=ctx.author.color)
        omanagement.add_field(name="Bot Management Commands", value=botmanval, inline=True)

        components=[
            [
                Select(
                    placeholder="Select a help menu",
                    options=[
                        SelectOption(label="Page 1 | SysBot Module", value="sysbot"),
                        SelectOption(label="Page 2 | Files Module", value="files"),
                        SelectOption(label="Page 3 | Miscellaneous Module", value="general"),
                        SelectOption(label="Page 4 | Channel Management Module", value="amanagement"),
                        SelectOption(label="Page 5 | Moderation Module", value="moderation"),
                        SelectOption(label="Page 6 | Switch Remote Module", value="sremote"),
                        SelectOption(label="Page 7 | Owner Module", value="owner"),
                        SelectOption(label="Page 8 | Bot Management Module", value="omanagement")
                        ],
                    )
            ],
            [
                Button(label='Support Server', style=ButtonStyle.URL, url=support2)
            ]
        ]

        message = await ctx.reply(embed=embed, components=components)

        while(True):
            try:
                interaction = await self.client.wait_for("select_option", check=None, timeout=10.0)
                if interaction.values[0] == "sysbot":
                    await interaction.respond(type=7, ephemeral=False, embed=sysbot)
                if interaction.values[0] == "files":
                    await interaction.respond(type=7, ephemeral=False, embed=files)
                if interaction.values[0] == "general":
                    await interaction.respond(type=7, ephemeral=False, embed=general)
                if interaction.values[0] == "amanagement":
                    await interaction.respond(type=7, ephemeral=False, embed=amanagement)
                if interaction.values[0] == "moderation":
                    await interaction.respond(type=7, ephemeral=False, embed=moderation)
                if interaction.values[0] == "sremote":
                    await interaction.respond(type=7, ephemeral=False, embed=sremote)
                if interaction.values[0] == "owner":
                    await interaction.respond(type=7, ephemeral=False, embed=owner)
                if interaction.values[0] == "omanagement":
                    await interaction.respond(type=7, ephemeral=False, embed=omanagement)
            except asyncio.TimeoutError:
                await message.disable_components()
                return


def setup(client):
    client.add_cog(help(client))
