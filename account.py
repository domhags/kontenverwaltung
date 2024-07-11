class Account:
    def __init__(self, account_number, account_holder, initial_balance=0.0):
        # Initialisiert ein Konto mit Kontonummer, Inhaber und Anfangssaldo von 0,0 €
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        # Führt eine Einzahlung auf das Konto aus, indem der Betrag zum aktuellen Saldo hinzugefügt wird
        self.balance += amount

    def withdraw(self, amount):
        # Führt eine Abhebung vom Konto aus, wenn ausreichend Guthaben vorhanden ist
        # Gibt True zurück, wenn die Abhebung erfolgreich war, ansonsten False
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        # Gibt den aktuellen Kontostand zurück
        return self.balance

    def __str__(self):
        # Gibt eine lesbare Zeichenfolge zurück, die das Konto repräsentiert
        return f"Konto {self.account_number} (Inhaber: {self.account_holder}, Kontostand: {self.balance} €)"
