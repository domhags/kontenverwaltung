from account import Account


class AccountManager:
    def __init__(self):
        # Initialisiert eine leere Liste für die Konten
        self.accounts = []

    def create_account(self, new_holder, inital_balance=0.0):
        # Erstellt ein neues Konto mit einem eindeutigen Kontonummernzähler und gibt die Kontonummer zurück
        account_number = len(self.accounts) + 1
        account = Account(account_number, new_holder, inital_balance)
        self.accounts.append(account)
        return account_number

    def delete_account(self, account_number):
        # Löscht ein Konto anhand der Kontonummer, falls es existiert
        account = self.find_account(account_number)
        if account:
            self.accounts.remove(account)
            return True
        return False

    def find_account(self, account_number):
        # Sucht nach einem Konto anhand der Kontonummer und gibt das Konto zurück, wenn es gefunden wird
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

    def display_all_accounts(self):
        # Gibt alle Konten zurück, falls vorhanden, ansonsten None
        return self.accounts if self.accounts else None

    def deposit_to_account(self, account_number, amount):
        # Führt eine Einzahlung auf das angegebene Konto aus, falls es existiert
        account = self.find_account(account_number)
        if account:
            account.deposit(amount)
            return True
        else:
            return False

    def withdraw_from_account(self, account_number, amount):
        # Führt eine Abhebung vom angegebenen Konto aus, falls es existiert und ausreichend Guthaben vorhanden ist
        account = self.find_account(account_number)
        if account:
            return account.withdraw(amount)
        return False
