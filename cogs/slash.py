import discord
from discord.ext import commands
from yaml import load
from discord_slash import cog_ext, SlashContext
from discord_components import DiscordComponents, SelectOption, Select, Button, ButtonStyle
import asyncio
import os


##Loads token and prefix from config file
with open("config.yaml") as file:
        data = load(file)
        botprefix = data["botprefix"]
        support2 = data["support-server-invite"]

class slash(commands.Cog):
    def __init__(self, client):
        self.client = client
        DiscordComponents(self.client)

# {-- Public Slash Commands --}
    @cog_ext.cog_slash(name="help", description="Help dropdown menu")
    async def _guide(self, ctx: SlashContext):

        # Public Embeds
        embed=discord.Embed(title=f'{self.client.user.name} Commands', description=f"Utilize the dropdown menu to select help pages.\nThing to remember: Prefix = `{botprefix}`, Required Parameter = `<>`, Optional Parameter = `[]`\n[Support Server]({support2})", color=0x17c70a)
        embed.add_field(name="**Help Modules:**", value="**Page 1** | SysBot Commands\n**Page 2** | Pokemon Files Commands\n**Page 3** | Miscellaneous Commands\n**Page 4** | Channel Management Commands\n**Page 5** | Moderation Commands\n**Page 6** | Switch Commands\n**Page 7** | Owner Commands\n**Page 8** | Bot Management Commands", inline=True)
        embed.add_field(name="📢 Bot Commits", value="⋅ Help command.", inline=True)
        
        sysbot=discord.Embed(title=f'SysBot Module', description=f"Thing to remember: Prefix = `{botprefix}`, Required Parameter = `<>`, Optional Parameter = `[]`", color=0x17c70a)
        sysbot.add_field(name="testtradetest <eb8>", value="Request a pokemon from the bot.", inline=True)
        sysbot.add_field(name="guide", value="Shows a video on how to use SysBot.", inline=True)
        sysbot.add_field(name="languide", value="Shows instructions on how to download LAN play.", inline=True)
        sysbot.add_field(name="lgpeg", value="Shows a video on how to use the LGPE SysBot.", inline=True)
        sysbot.add_field(name="queue", value="Sends you current queue position.", inline=True)
        sysbot.add_field(name="queue list", value="Displays the total queue list.", inline=True)
        sysbot.add_field(name="queue leave", value="Requests to leave the queue.", inline=True)

        files=discord.Embed(title=f'Files Module', description=f"Thing to remember: Prefix = `{botprefix}`, Required Parameter = `<>`, Optional Parameter = `[]`", color=0x17c70a) 
        files.add_field(name="pk8", value="Sends a `pk8` file.", inline=True)
        files.add_field(name="ek8", value="Sends a `ek8` file.", inline=True)
        files.add_field(name="pk7", value="Sends a `pk7` file.", inline=True)
        files.add_field(name="pk6", value="Sends a `pk6` file.", inline=True)
        files.add_field(name="pb8", value="Sends a `pb8` file.", inline=True)
        files.add_field(name="eb8", value="Sends a `eb8` file.", inline=True)
        files.add_field(name="pb7", value="Sends a `pb7` file.", inline=True)

        general=discord.Embed(title=f'Miscellaneous Module', description=f"Thing to remember: Prefix = `{botprefix}`, Required Parameter = `<>`, Optional Parameter = `[]`", color=0x17c70a) 
        general.add_field(name="prefix", value="Fetchs the bot's prefix.", inline=True)
        general.add_field(name="latency", value="Reports latency.", inline=True)
        general.add_field(name="invite", value="Sends invite link to bot's home server.", inline=True)
        general.add_field(name="support", value="Sends bot's donation link.", inline=True)
        general.add_field(name="vote", value="Vote for a SysBot mode.", inline=True)
        general.add_field(name="votelock", value="3 votes will lock the channel the command is used in.", inline=True)
        general.add_field(name="addcode", value="Saves your friend code.", inline=True)
        general.add_field(name="fcode", value="Shows saved your friend codes.", inline=True)
        general.add_field(name="changecode", value="Changes your friend code.", inline=True)
        general.add_field(name="removecode", value="Deletes your friend code.", inline=True)


        # Admin Embeds
        amanagement=discord.Embed(title=f'Channel Management Module', description=f"Thing to remember: Prefix = `{botprefix}`, Required Parameter = `<>`, Optional Parameter = `[]`", color=0x17c70a) 
        amanagement.add_field(name="lock", value="Prevents members from type in used channel.", inline=True)
        amanagement.add_field(name="unlock", value="Allows members from type in used channel.", inline=True)
        amanagement.add_field(name="say <message>", value="Bot repeats message.", inline=True)
        amanagement.add_field(name="purge <amount>", value="Deletes requested amount of messages in used channel.", inline=True)
        amanagement.add_field(name="slowmode <amount>", value="Changes the slowmode of used channel.", inline=True)
        amanagement.add_field(name="add", value="Adds channel to bot's announcement notification list.", inline=True)
        amanagement.add_field(name="remove", value="Removes channel from bot's announcement notification list..", inline=True)

        moderation=discord.Embed(title=f'Moderation Module', description=f"Thing to remember: Prefix = `{botprefix}`, Required Parameter = `<>`, Optional Parameter = `[]`", color=0x17c70a) 
        moderation.add_field(name="kick <member> [reason]", value="Kicks mentioned member.", inline=True)
        moderation.add_field(name="ban <member> [reason]", value="Bans mentioned member.", inline=True)
        moderation.add_field(name="shareban <member> [reason]", value="Bans mentioned member and announces in all linked channels.", inline=True)
        moderation.add_field(name="unban <member>", value="Unbans mentioned member.", inline=True)
        moderation.add_field(name="userinfo <member>", value="Displays mentioned member's info.", inline=True)
        moderation.add_field(name="warn <reason>", value="Warns mentioned member.", inline=True)
        moderation.add_field(name="addrole <member> <role>", value="Gives mentioned member a role.", inline=True)
        moderation.add_field(name="removerole <member> <role>", value="Removes mentioned member a role.", inline=True)
        moderation.add_field(name="mute <member <duration> [reason]", value="Mutes mentioned member for said duration.", inline=True)
        moderation.add_field(name="unmute <member>", value="Unmutes member.", inline=True)
        moderation.add_field(name="category <channel> <category>", value="Moves the channels category location.", inline=True)
        moderation.add_field(name="addban", value="Adds channel to bot's shareban notification list.", inline=True)
        moderation.add_field(name="removeban", value="Removes channel from bot's shareban notification list.", inline=True)

        # Sudo Embeds
        sremote=discord.Embed(title=f'Switch Module', description=f"Thing to remember: Prefix = `{botprefix}`, Required Parameter = `<>`, Optional Parameter = `[]`", color=0x17c70a)
        sremote.add_field(name="click [x, a, b, or y]", value="Tells switch to click selected button.", inline=True)
        sremote.add_field(name="spamb", value="Tells switch to spam press the b button.", inline=True)
        sremote.add_field(name="click [up, right, down, left]", value="Tells switch which direction to move.", inline=True)
        sremote.add_field(name="click [plus. minus, home]", value="Clicks selected hotkey on switch.", inline=True)
        sremote.add_field(name="pokemon [inject, dump]", value="Dumps or injects pokemon into box 1 slot 1.", inline=True)
        sremote.add_field(name="screen [on, off, shot, capture, percent, pixelPeek]", value="Controls the switch screen.", inline=True)
        sremote.add_field(name="reconnect", value="Attempts to reconnect to your switch.", inline=True)

        # Owner Embeds
        owner=discord.Embed(title=f'Owner Module', description=f"Thing to remember: Prefix = `{botprefix}`, Required Parameter = `<>`, Optional Parameter = `[]`", color=0x17c70a)
        owner.add_field(name="boton <message>", value="Sends a bot online message.", inline=True)
        owner.add_field(name="announcment <message>", value="Sends an announcement message.", inline=True)
        owner.add_field(name="botdown <message>", value="Sends a bot offline message.", inline=True)
        owner.add_field(name="redact <amount>", value="Redacts desired amount of announcement messages.", inline=True)
        owner.add_field(name="addsudo <member>", value="Adds member to sudo list.", inline=True)
        owner.add_field(name="removesudo <member>", value="Removes member from sudo list.", inline=True)
        owner.add_field(name="blacklist <member>", value="Adds member to blacklist.", inline=True)
        owner.add_field(name="unblacklist <member>", value="Removes member from blacklist.", inline=True)
        owner.add_field(name="loghere", value="Adds channel to logging output.", inline=True)
        owner.add_field(name="dontlog", value="Removes channel from logging output.", inline=True)

        omanagement=discord.Embed(title=f'Bot Management Module', description=f"Thing to remember: Prefix = `{botprefix}`, Required Parameter = `<>`, Optional Parameter = `[]`", color=0x17c70a)
        omanagement.add_field(name="directmessage <userid> <content>", value="Sends message to directed user.", inline=True)
        omanagement.add_field(name="send <channelid> <content>", value="Sends message to directed channel.", inline=True)
        omanagement.add_field(name="list", value="List all servers the bot is in, including name, guild ID, owner, and invite.", inline=True)
        omanagement.add_field(name="leave <guildid>", value="Leaves server from directed guild.", inline=True)
        omanagement.add_field(name="createguild <name>", value="Creates a guild.", inline=True)
        omanagement.add_field(name="deleteguild <guildid>", value="Deletes an owned guild.", inline=True)
        omanagement.add_field(name="rename <name>", value="Renames the bot's name.", inline=True)
        omanagement.add_field(name="repfp <image>", value="Change the bot's pfp.", inline=True)
        omanagement.add_field(name="botinvite", value="Generates a bot invite.", inline=True)
        omanagement.add_field(name="load <cog>", value="Loads a cog.", inline=True)
        omanagement.add_field(name="reload <cogs>", value="Reloads a cog.", inline=True)
        omanagement.add_field(name="unload <cog>", value="Unloads a cog.", inline=True)
        omanagement.add_field(name="restart", value="Restarts the bot.", inline=True)
        omanagement.add_field(name="shutdown", value="Turns off the bot.", inline=True)

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

    @cog_ext.cog_slash(name="guide", description="How to use Sysbot guide")
    async def _guide(self, ctx: SlashContext):
            embed=discord.Embed(title="How To Use Sysbot", url="https://youtu.be/1WbOHrQfMlc", description="This is a [guide](https://youtu.be/1WbOHrQfMlc) on how to use sysbot.\nPlease watch the complete video on how to use the bots.\nAll bots are in this bots official server.", color=ctx.author.color)
            embed.set_thumbnail(url="https://i.ytimg.com/vi/1WbOHrQfMlc/mqdefault.jpg")
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="invite", description="Want an invite?")
    async def _invite(self, ctx):
        await ctx.send(support2)

    @cog_ext.cog_slash(name="languide", description="How to connect to LAN guide")
    async def _languide(self, ctx: SlashContext):
            embed=discord.Embed(title="How To Use LAN Sysbot", url="https://docs.google.com/document/d/e/2PACX-1vR9tpYmZ3qCbqOeZb1XwnNESAauTf9rVJVzJ1G22TkmGsVZf8LVJs-o-rNshKsYZuyZBdrdRDzTtsqH/pub", description=f"""
            This is a [lan guide](https://docs.google.com/document/d/e/2PACX-1vR9tpYmZ3qCbqOeZb1XwnNESAauTf9rVJVzJ1G22TkmGsVZf8LVJs-o-rNshKsYZuyZBdrdRDzTtsqH/pub) on how to connect to LAN. 
            Here are some helpful videos to get you started:
            [LAN Installation on WINDOWS](https://www.youtube.com/watch?v=qQSQH6F6ogk) || By Optimisim247.
            [LAN Installation on MAC](https://www.youtube.com/watch?v=nhC8qgjauL0&t=369s)
            All bots are in the bots official [Pokemon LAN server](https://discord.gg/pkmn).""", color= ctx.author.color)
            embed.set_thumbnail(url="https://i.ytimg.com/vi/1WbOHrQfMlc/mqdefault.jpg")  
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="lgpe", description="How to use the LGPE Sysbot guide")
    async def _lgpe(self, ctx: SlashContext):
            embed=discord.Embed(title="How To Use The LGPE Sysbot", url="https://www.youtube.com/watch?v=0dS2QTxqFnI", description="This is a [guide](https://www.youtube.com/watch?v=0dS2QTxqFnI) on how to use the LGPE sysbot.\nPlease watch the complete video on how to use the bots.\nAll bots are in this bots official server.", color=ctx.author.color)
            embed.set_thumbnail(url="https://i.ytimg.com/vi/1WbOHrQfMlc/mqdefault.jpg")
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="missingno", description="Provides a safe missingno file.")
    async def _missingno(self, ctx):
            filepath = f"res/missingno.pk8"
            if os.path.exists(filepath):
                    await ctx.send(file=discord.File(filepath))

    @cog_ext.cog_slash(name="prefix", description="Gives you the bot's prefix")
    async def _prefix(self, ctx):
        await ctx.send(f'My prefix is `{botprefix}`.')

def setup(client):
    client.add_cog(slash(client))