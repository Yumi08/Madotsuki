import discord
from discord.ext import commands

from Bot import data
from Structures.Data import UserAccount, BankAccount

class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(brief="Show your account statement.")
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

    @commands.command(brief="Show someone else's account statement.")
    async def statement_t(self, ctx, user : discord.User):
        try:
            data.user_accounts[user.id]
        except:
            data.user_accounts[user.id] = UserAccount()
        
        accts = data.user_accounts[user.id].accounts
        o = ""

        if data.user_accounts[user.id].accounts_public == False:
            await ctx.send(f"{user.name}\'s accounts are private!")
            return
        
        for i in range(len(accts)):
            o += f"{i}. - {accts[i].name} - {accts[i].balance}\n"

        await ctx.send(o)
        


    @commands.command(brief="Open an account.")
    async def open(self, ctx, name):
        try:
            data.user_accounts[ctx.author.id]
        except:
            data.user_accounts[ctx.author.id] = UserAccount()
        
        accts = data.user_accounts[ctx.author.id].accounts
        accts.append(BankAccount(name, 0))

        await ctx.send(f"Created account: {name}.")

    @commands.command(brief="Close an account")
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

    @commands.command(brief="Transfer between two of your own accounts.")
    async def transfer(self, ctx, num1 : int, num2 : int, amt : int):
        try:
            data.user_accounts[ctx.author.id]
        except:
            data.user_accounts[ctx.author.id] = UserAccount()
        
        accts = data.user_accounts[ctx.author.id].accounts
        o = ""
        acc1_orig = accts[num1].balance
        acc2_orig = accts[num2].balance

        if num2 == 0:
            await ctx.send("Cannot transfer into Inbound account.")
            return

        if accts[num1].balance < amt:
            await ctx.send(f"Insufficient balance in {accts[num1].name}!")
            return
        
        accts[num1].balance -= amt
        accts[num2].balance += amt

        o += f"{accts[num1].name} : {acc1_orig} -> {accts[num1].balance}\n"
        o += f"{accts[num2].name} : {acc2_orig} -> {accts[num2].balance}\n"
        o += "Transfer successful!"

        await ctx.send(o)

    @commands.command(brief="Send money to another person")
    async def send(self, ctx, acct_num : int, receiver : discord.User, amt : int):
        try:
            data.user_accounts[ctx.author.id]
        except:
            data.user_accounts[ctx.author.id] = UserAccount()

        try:
            data.user_accounts[receiver.id]
        except:
            data.user_accounts[receiver.id] = UserAccount()
        
        accts = data.user_accounts[ctx.author.id].accounts
        recv_accts = data.user_accounts[receiver.id].accounts
        o = ""
        acct_orig = accts[acct_num].balance
        recv_acct_orig = recv_accts[0].balance

        if accts[acct_num].balance < amt:
            await ctx.send(f"Insufficient balance in {accts[acct_num].name}!")
            return
        
        accts[acct_num].balance -= amt
        recv_accts[0].balance += amt

        o += f"Your {accts[acct_num].name} : {acct_orig} -> {accts[acct_num].balance}\n"
        if data.user_accounts[receiver.id].accounts_public == True:
            o += f"Their {recv_accts[0].name} : {recv_acct_orig} -> {recv_accts[0].balance}\n"
        o += f"Successfully sent {amt} to {receiver.name}!"

        await ctx.send(o)
    
    @commands.command(brief="Set your banking info to be public.")
    async def public_bank(self, ctx):
        try:
            data.user_accounts[ctx.author.id]
        except:
            data.user_accounts[ctx.author.id] = UserAccount()
        
        acct = data.user_accounts[ctx.author.id]

        acct.accounts_public = True

        await ctx.send("Set your bank to be public!")

    @commands.command(brief="Set your banking info to be private.")
    async def private_bank(self, ctx):
        try:
            data.user_accounts[ctx.author.id]
        except:
            data.user_accounts[ctx.author.id] = UserAccount()
        
        acct = data.user_accounts[ctx.author.id]

        acct.accounts_public = False

        await ctx.send("Set your bank to be private!")

def setup(client):
    print("Loading Currency cog.")
    client.add_cog(Currency(client))