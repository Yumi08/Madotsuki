import discord
from discord.ext import commands

from Bot import data

class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def statement(self, ctx):
        await ctx.send(data.user_accounts[str(ctx.author.id)])

    @commands.command()
    async def setnum(self, ctx, num : int):
        data.user_accounts[str(ctx.author.id)] = num
        await ctx.send("Done!")

def setup(client):
    print("Loading Currency cog.")
    client.add_cog(Currency(client))