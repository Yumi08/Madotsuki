from enum import Enum

class Commodities(Enum):
    Coins=0
    Points=1

    def __str__(self):
        return "%s" % self.name

class BankAccount:
    def __init__(self, name, balance, commodity = Commodities.Coins, erasable = True):
        self.name = name
        self.balance = balance
        self.commodity = commodity
        self.erasable = erasable

class UserAccount:
    def __init__(self):
        self.accounts = [BankAccount("Inbound", 0, erasable=False), BankAccount("Default", 1000)]
        self.accounts_public = True

class Data:
    def __init__(self):
        self.user_accounts = {}
