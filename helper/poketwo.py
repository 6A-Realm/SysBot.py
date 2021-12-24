from helper.names import pokemon
from helper.solver import solver
from discord.ext import commands

poketwo = 716390085896962058
pokemonbot = 669228505128501258



class poketwo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        #The pokémon is G____dor.
        if (message.content.startswith('The pokémon is ') and message.author.id == poketwo):
            print(message.content)
            split = message.content.split(" ", 4)[3:-1]
            print(split)
            split = split.replace("\\" , "")
            final = solver(split,pokemon)
            if (len(final) == 0):
                await message.channel.send("Pokémon could not be solved.")
            for i in range(len(final)):
                await message.channel.send("The pokemon is " + final[i])
        
        if (message.content.startswith('The wild pokémon is ') and message.author.id == pokemonbot):
            split = message.content.split(" ", 5)[4:0]
            message.channel.send(split)
            split = split.replace("\\" , "")
            final = solver(split,pokemon)
            if (len(final) == 0):
                await message.channel.send("Pokémon could not be solved.")
            for i in range(len(final)):
                await message.channel.send("The pokemon is " + final[i])





def setup(client):
    client.add_cog(poketwo(client))