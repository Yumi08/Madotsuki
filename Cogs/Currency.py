import discord
from discord.ext import commands

from Bot import data
from Structures.Data import UserAccount, BankAccount

class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def statement(self, ctx):
        try:
            data.user_accounts[ctx.author.id]
        except:
            data.user_accounts[ctx.author.id] = UserAccount()
        
        accts = data.user_accounts[ctx.author.id].accounts
        o = ""
        
        for i in range(len(accts)):
            o += f"{i}. - {accts[i].name} - {accts[i].balance}\n"

        await ctx.send(o)

    @commands.command()
    async def open(self, ctx, name):
        try:
            data.user_accounts[ctx.author.id]
        except:
            data.user_accounts[ctx.author.id] = UserAccount()
        
        accts = data.user_accounts[ctx.author.id].accounts
        accts.append(BankAccount(name, 0))

        await ctx.send(f"Created account: {name}.")

    @commands.command()
    async def close(self, ctx, num : int):
        try:
            data.user_accounts[ctx.author.id]
        except:
            data.user_accounts[ctx.author.id] = UserAccount()
        
        accts = data.user_accounts[ctx.author.id].accounts

        if num >= len(accts):
            await ctx.send("Out of range!")
        elif num == 0:
            await ctx.send("Cannot delete Inbound account.")
        elif accts[num].balance != 0:
            await ctx.send("Cannot delete account with more than 0 balance.")
        else:
            await ctx.send(f"Deleting {accts[num].name}...")
            del accts[num]

    @commands.command()
    async def transfer(self, ctx, num1 : int, num2 : int, amt : int):
        try:
            data.user_accounts[ctx.author.id]
        except:
            data.user_accounts[ctx.author.id] = UserAccount()
        
        accts = data.user_accounts[ctx.author.id].accounts
        o = ""
        acc1_orig = accts[num1].balance
        acc2_orig = accts[num2].balance

        if accts[num1].balance < amt:
            await ctx.send(f"Insufficient balance in {accts[num1].name}!")
            return
        
        accts[num1].balance -= amt
        accts[num2].balance += amt

        o += f"{accts[num1].name} : {acc1_orig} -> {accts[num1].balance}\n"
        o += f"{accts[num2].name} : {acc2_orig} -> {accts[num2].balance}\n"
        o += "Transfer successful!"

        await ctx.send(o)

def setup(client):
    print("Loading Currency cog.")
    client.add_cog(Currency(client))