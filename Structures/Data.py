class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

class UserAccount:
    def __init__(self):
        self.accounts = [BankAccount("Inbound", 0), BankAccount("Default", 1000)]
        self.accounts_public = True

class Data:
    def __init__(self):
        self.user_accounts = {}