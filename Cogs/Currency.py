import discord
from discord.ext import commands

from Bot import data, bot_name
from Structures.Data import UserAccount, BankAccount, Commodities

import random

class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    def __try_user(self, userid):
        try:
            data.user_accounts[userid]
        except:
            data.user_accounts[userid] = UserAccount()
            if userid == self.client.user.id:
                data.user_accounts[self.client.user.id].accounts = [BankAccount("Reserve", 1000000)]

    @commands.command(brief="Show your account statement.")
    async def statement(self, ctx):
        self.__try_user(ctx.author.id)

        accts = data.user_accounts[ctx.author.id].accounts
        o = ""

        for i in range(len(accts)):
            o += f"{i}. - {accts[i].name} - {accts[i].balance:,} {accts[i].commodity}\n"

        await ctx.send(o)

    @commands.command(brief="Show someone else's account statement.")
    async def statement_t(self, ctx, user : discord.User):
        self.__try_user(user.id)

        accts = data.user_accounts[user.id].accounts
        o = ""

        if data.user_accounts[user.id].accounts_public == False:
            await ctx.send(f"{user.name}\'s accounts are private!")
            return

        for i in range(len(accts)):
            o += f"{i}. - {accts[i].name} - {accts[i].balance:,} {accts[i].commodity}\n"

        await ctx.send(o)

    @commands.command(brief="Open an account.")
    async def open(self, ctx, name, commodity : str):
        self.__try_user(ctx.author.id)

        accts = data.user_accounts[ctx.author.id].accounts
        accts.append(BankAccount(name, 0, Commodities[commodity]))

        await ctx.send(f"Created account: {name}.")

    @commands.command(brief="Close an account")
    async def close(self, ctx, num : int):
        self.__try_user(ctx.author.id)

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
        self.__try_user(ctx.author.id)

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
        if accts[num1].commodity != accts[num2].commodity:
            await ctx.send(f"Can't convert {accts[num1].commodity} to {accts[num2].commodity}!")
            return

        accts[num1].balance -= amt
        accts[num2].balance += amt

        o += f"{accts[num1].name} : {acc1_orig:,} {accts[num1].commodity} -> {accts[num1].balance:,} {accts[num1].commodity}\n"
        o += f"{accts[num2].name} : {acc2_orig:,} {accts[num2].commodity} -> {accts[num2].balance:,} {accts[num2].commodity}\n"
        o += "Transfer successful!"

        await ctx.send(o)

    @commands.command(brief="Send money to another person")
    async def send(self, ctx, acct_num : int, receiver : discord.User, amt : int):
        self.__try_user(ctx.author.id)
        self.__try_user(receiver.id)

        accts = data.user_accounts[ctx.author.id].accounts
        recv_accts = data.user_accounts[receiver.id].accounts
        o = ""
        acct_orig = accts[acct_num].balance
        recv_acct_orig = recv_accts[0].balance

        if accts[acct_num].balance < amt:
            await ctx.send(f"Insufficient balance in {accts[acct_num].name}!")
            return
        if accts[acct_num].commodity != recv_accts[0].commodity:
            await ctx.send(f"Can't convert {accts[acct_num].commodity} to {recv_accts[0].commodity}!")
            return

        accts[acct_num].balance -= amt
        recv_accts[0].balance += amt

        o += f"Your {accts[acct_num].name} : {acct_orig:,} {accts[acct_num].commodity} -> {accts[acct_num].balance:,} {accts[acct_num].commodity}\n"
        if data.user_accounts[receiver.id].accounts_public == True:
            o += f"Their {recv_accts[0].name} : {recv_acct_orig:,} {recv_accts[0].commodity}-> {recv_accts[0].balance:,} {recv_accts[0].commodity}\n"
        o += f"Successfully sent {amt:,} {recv_accts[0].commodity} to {receiver.name}!"

        await ctx.send(o)

    @commands.command(brief="Set your banking info to be public.")
    async def public_bank(self, ctx):
        self.__try_user(ctx.author.id)

        acct = data.user_accounts[ctx.author.id]

        acct.accounts_public = True

        await ctx.send("Set your bank to be public!")

    @commands.command(brief="Set your banking info to be private.")
    async def private_bank(self, ctx):
        self.__try_user(ctx.author.id)

        acct = data.user_accounts[ctx.author.id]

        acct.accounts_public = False

        await ctx.send("Set your bank to be private!")

    @commands.command(brief="Flip a coin to win big!")
    async def flip(self, ctx, acct_num : int, amt : int, side : str):
        self.__try_user(ctx.author.id)
        self.__try_user(self.client.user.id)

        user_accts = data.user_accounts[ctx.author.id].accounts
        bot_accts = data.user_accounts[self.client.user.id].accounts
        o = ""

        choice = False
        result = bool(random.getrandbits(1))

        if side.lower() == "heads" or side.lower() == "h":
            choice = True
        elif side.lower() == "tails" or side.lower() == "t":
            choice = False
        else:
            await ctx.send("Please say either \"Heads\" or \"Tails\"!")
            return

        if user_accts[acct_num].balance < amt:
            await ctx.send(f"Insufficient balance in {user_accts[acct_num].name}!")
            return
        if bot_accts[0].balance < amt:
            await ctx.send(f"Insufficient balance in {bot_name}\'s reserve!")
            return

        if choice == True:
            o += "Heads!\n"
        else:
            o += "Tails!\n"

        if choice == result:
            o += f"You won {amt:,} {user_accts[acct_num].commodity} into your {user_accts[acct_num].name} account!"
            user_accts[acct_num].balance += amt
            bot_accts[0].balance -= amt
        else:
            o += "Sorry, you lost."
            user_accts[acct_num].balance -= amt
            bot_accts[0].balance += amt

        await ctx.send(o)


def setup(client):
    print("Loading Currency cog.")
    client.add_cog(Currency(client))
