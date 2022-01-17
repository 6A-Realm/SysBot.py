from twitchio.ext import commands
import yaml
from yaml import load
yaml.warnings({'YAMLLoadWarning': False})

##Loads information from config file
with open("config.yaml") as file:
    data = load(file)
    tmitoken = data["tmitoken"]
    clientid = data["clientid"]
    botnickname = data["botnickname"]
    botprefix = data["botprefix"]
    channel = data["channel"]
    support2 = data["support-server-invite"]

# Defining client
client = commands.Bot(irc_token=tmitoken, client_id=clientid, nick=botnickname, prefix=botprefix, initial_channels=[channel])

# Echo notification on start up
@client.event
async def event_ready():
    print(f"{botnickname} is connected to twitch.")
    ws = client._ws
    await ws.send_privmsg(channel, f"/me echo notification.")

@client.command()
async def discord(ctx):
    if ctx.author.name.lower() == botnickname.lower():
        return
    await ctx.send(support2)


if __name__ == "__main__":
    client.run()