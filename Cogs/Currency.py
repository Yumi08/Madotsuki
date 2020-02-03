import discord
from discord.ext import commands

from Bot import data

class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setnum(self, ctx, num : int):
        original_num = data.num
        data.num = num
        await ctx.send(f"Setting num from {original_num} to {data.num}")

def setup(client):
    print("Loading Currency cog.")
    client.add_cog(Currency(client))