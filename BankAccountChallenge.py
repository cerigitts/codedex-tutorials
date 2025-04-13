# Bank Account Challenge

class BankAccount:
    def __init__(self, first_name, last_name, account_id, account_type, pin, balance):
        self.first_name = first_name
        self.last_name = last_name
        self.account_id = account_id
        self.account_type = account_type
        self.pin = pin
        self.balance = balance
        
    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        self.balance = self.balance - amount
        return self.balance

    def display_balance(self):
        print(f"${self.balance}")

bank_account = BankAccount("Ceri", "Gittins", 123456, "Savings", 1234, 5000.00)

bank_account.deposit(98)
bank_account.display_balance()
bank_account.withdraw(50)
bank_account.display_balance()

