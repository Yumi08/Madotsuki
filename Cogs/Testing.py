import discord
from discord.ext import commands

class Testing(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

def setup(client):
    print("Loading Testing cog.")
    client.add_cog(Testing(client))