from account import Account


class AccountManager:
    def __init__(self):
        self.accounts = []

    def create_account(self, new_holder, inital_balance=0.0):
        account_number = len(self.accounts) + 1
        account = Account(account_number, new_holder, inital_balance)
        self.accounts.append(account)
        print(f"Neues Konto angelegt: {account}")
        return account_number

    def delete_account(self, account_number):
        account = self.find_account(account_number)
        if account:
            self.accounts.remove(account)
            print(f"Konto {account_number} gelöscht.")
            return True
        print(f"Konto {account_number} nicht gefunden.")
        return False

    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

    def display_account(self):
        if not self.accounts:
            print("Keine Konten vorhanden.")
            return False
        for account in self.accounts:
            print(f"Konto {account.account_number} | Inhaber: {account.account_holder}")
        return True

    def display_all_accounts(self):
        if not self.accounts:
            print("Keine Konten vorhanden.")
            return False
        else:
            print("Alle Konten:")
            for account in self.accounts:
                print(account)
            return True

    def display_account_details(self):
        if not self.accounts:
            print("Keine Konten vorhanden.")
            return
        self.display_account()

        account_number = int(input("Kontonummer: ").strip())

        account = self.find_account(account_number)

        if account:
            print(f"ID: {account.account_number} | Inhaber: {account.account_holder} | "
                  f"Kontostand: {account.get_balance()}")
        else:
            print(f"Konto {account_number} nicht gefunden.")

    def deposit_to_account(self, account_number, amount):
        account = self.find_account(account_number)
        if account:
            account.deposit(amount)
            print(f"{amount} € auf Konto {account_number} eingezahlt.")
        else:
            print(f"Konto {account_number} nicht gefunden.")

    def withdraw_from_account(self, account_number, amount):
        account = self.find_account(account_number)
        if account:
            if account.withdraw(amount):
                print(f"{amount} € von Konto {account_number} abgehoben.")
            else:
                print(f"Nicht genug Guthaben auf Konto {account_number}.")
        else:
            print(f"Konto {account_number} nicht gefunden.")
