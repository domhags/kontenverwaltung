import tkinter as tk
from tkinter import messagebox, ttk
from accountmanager import AccountManager
import csv


class AccountApp:
    def __init__(self, main_window):
        self.root = main_window
        self.root.title("Kontenverwaltung")
        self.root.geometry("400x400")

        self.account_manager = AccountManager()  # Initialisierung des Account Managers

        # Hauptframe der Applikation
        self.main_frame = tk.Frame(main_window)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Grid-Konfiguration für responsive Layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Erstellen der initialen Widgets beim Start
        self.show_main_menu()  # Anzeigen des Hauptmenüs beim Start

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.grid_forget()  # Entfernen aller Widgets im Hauptframe

    def show_main_menu(self):
        self.clear_frame()
        # Erstellen der Hauptmenü-Buttons
        tk.Button(self.main_frame, text="Konto erstellen",
                  command=self.create_account).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(self.main_frame, text="Konto löschen",
                  command=self.delete_account).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.main_frame, text="Alle Konten anzeigen",
                  command=self.display_all_accounts).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(self.main_frame, text="Kontostand anzeigen",
                  command=self.display_account_details).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.main_frame, text="Einzahlung",
                  command=self.deposit_to_account).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(self.main_frame, text="Abhebung",
                  command=self.withdraw_from_account).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.main_frame, text="Daten speichern",
                  command=self.save_accounts_to_csv).grid(row=3, column=0, padx=10, pady=5)
        tk.Button(self.main_frame, text="Beenden",
                  command=self.root.quit).grid(row=3, column=1, padx=10, pady=5)

    def create_account(self):
        self.clear_frame()
        # Erstellen eines neuen Kontos
        tk.Label(self.main_frame, text="Konto erstellen").grid(row=0, columnspan=2, pady=10)

        tk.Label(self.main_frame, text="Kontoinhaber").grid(row=1, column=0, padx=10, pady=5)
        holder_entry = tk.Entry(self.main_frame)
        holder_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.main_frame, text="Anfangssaldo (€)").grid(row=2, column=0, padx=10, pady=5)
        balance_entry = tk.Entry(self.main_frame)
        balance_entry.grid(row=2, column=1, padx=10, pady=5)

        def save_account():
            # Speichern des neuen Kontos
            holder = holder_entry.get().strip()
            balance = balance_entry.get().strip()
            if not holder:
                messagebox.showerror("Fehler", "Der Kontoinhaber muss angegeben werden.")
                return
            try:
                balance = float(balance) if balance else 0.0
                if balance < 0:
                    raise ValueError("Der Anfangssaldo darf nicht negativ sein.")
            except ValueError:
                messagebox.showerror("Fehler", "Ungültiger Anfangssaldo.")
                return
            account_number = self.account_manager.create_account(holder, balance)
            messagebox.showinfo("Erfolg", f"Konto erstellt. Kontonummer: {account_number}")
            self.show_main_menu()

        tk.Button(self.main_frame, text="Speichern",
                  command=save_account).grid(row=3, columnspan=2, padx=10, pady=5)
        tk.Button(self.main_frame, text="Zurück",
                  command=self.show_main_menu).grid(row=4, columnspan=2, padx=10, pady=5)

    def delete_account(self):
        self.clear_frame()
        # Löschen eines Kontos
        tk.Label(self.main_frame, text="Konto löschen").grid(row=0, columnspan=2, pady=10)

        tk.Label(self.main_frame, text="Kontonummer").grid(row=1, column=0, padx=10, pady=5)
        account_number_combobox = ttk.Combobox(self.main_frame)
        account_number_combobox.grid(row=1, column=1, padx=10, pady=5)

        account_data = [f"{account.account_number} - {account.account_holder}" for account in
                        self.account_manager.accounts]
        account_number_combobox['values'] = account_data

        def remove_account():
            # Löschvorgang eines Kontos
            selected_account = account_number_combobox.get().strip()
            if not selected_account:
                messagebox.showerror("Fehler", "Bitte wählen Sie ein Konto aus.")
                return
            account_number = int(selected_account.split(" - ")[0])
            if self.account_manager.delete_account(account_number):
                messagebox.showinfo("Erfolg", "Konto gelöscht.")
            else:
                messagebox.showerror("Fehler", "Konto nicht gefunden.")
            self.show_main_menu()

        tk.Button(self.main_frame, text="Löschen",
                  command=remove_account).grid(row=2, columnspan=2, padx=10, pady=5)
        tk.Button(self.main_frame, text="Zurück",
                  command=self.show_main_menu).grid(row=3, columnspan=2, padx=10, pady=5)

    def display_all_accounts(self):
        # Anzeige aller Konten
        self.clear_frame()
        tk.Label(self.main_frame, text="Alle Konten").grid(row=0, columnspan=2, pady=10)

        listbox = tk.Listbox(self.main_frame, width=100, height=20)
        listbox.grid(row=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=listbox.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        listbox.config(yscrollcommand=scrollbar.set)

        tk.Button(self.main_frame, text="Zurück",
                  command=self.show_main_menu).grid(row=2, columnspan=2, padx=10, pady=5)

        if not self.account_manager.accounts:
            messagebox.showinfo("Information", "Es sind keine Konten vorhanden.")
            return

        for account in self.account_manager.accounts:
            listbox.insert(tk.END, f"{account.account_number} | {account.account_holder} | {account.balance} €")

    def display_account_details(self):
        self.clear_frame()
        # Anzeige von Kontodetails eines bestimmten Kontos
        tk.Label(self.main_frame, text="Kontostand anzeigen").grid(row=0, columnspan=2, pady=10)

        tk.Label(self.main_frame, text="Kontonummer").grid(row=1, column=0, padx=10, pady=5)
        account_number_combobox = ttk.Combobox(self.main_frame)
        account_number_combobox.grid(row=1, column=1, padx=10, pady=5)

        account_data = [f"{account.account_number} - {account.account_holder}" for account in
                        self.account_manager.accounts]
        account_number_combobox['values'] = account_data

        def show_details():
            # Zeigt die Kontodetails an
            selected_account = account_number_combobox.get().strip()
            if not selected_account:
                messagebox.showerror("Fehler", "Bitte wählen Sie ein Konto aus.")
                return
            account_number = int(selected_account.split(" - ")[0])
            account = self.account_manager.find_account(account_number)
            if account:
                messagebox.showinfo("Kontodetails", f"Kontonummer: {account.account_number}\n"
                                                    f"Inhaber: {account.account_holder}\n"
                                                    f"Kontostand: {account.get_balance()} €")
            else:
                messagebox.showerror("Fehler", "Konto nicht gefunden.")
            self.show_main_menu()

        tk.Button(self.main_frame, text="Anzeigen",
                  command=show_details).grid(row=2, columnspan=2, padx=10, pady=5)
        tk.Button(self.main_frame, text="Zurück",
                  command=self.show_main_menu).grid(row=3, columnspan=2, padx=10, pady=5)

    def deposit_to_account(self):
        self.clear_frame()
        # Einzahlen auf ein Konto
        tk.Label(self.main_frame, text="Einzahlung").grid(row=0, columnspan=2, pady=10)

        tk.Label(self.main_frame, text="Kontonummer").grid(row=1, column=0, padx=10, pady=5)
        account_number_combobox = ttk.Combobox(self.main_frame)
        account_number_combobox.grid(row=1, column=1, padx=10, pady=5)

        account_data = [f"{account.account_number} - {account.account_holder}" for account in
                        self.account_manager.accounts]
        account_number_combobox['values'] = account_data

        tk.Label(self.main_frame, text="Betrag").grid(row=2, column=0, padx=10, pady=5)
        amount_entry = tk.Entry(self.main_frame)
        amount_entry.grid(row=2, column=1, padx=10, pady=5)

        def deposit():
            # Funktion zum Durchführen einer Einzahlung
            selected_account = account_number_combobox.get().strip()
            amount = amount_entry.get().strip()
            if not selected_account or not self.is_float(amount):
                messagebox.showerror("Fehler", "Ungültige Kontonummer oder Betrag.")
                return
            account_number = int(selected_account.split(" - ")[0])
            self.account_manager.deposit_to_account(account_number, float(amount))
            messagebox.showinfo("Erfolg", "Einzahlung erfolgreich.")
            self.show_main_menu()

        tk.Button(self.main_frame, text="Einzahlen",
                  command=deposit).grid(row=3, columnspan=2, padx=10, pady=5)
        tk.Button(self.main_frame, text="Zurück",
                  command=self.show_main_menu).grid(row=4, columnspan=2, padx=10, pady=5)

    def withdraw_from_account(self):
        self.clear_frame()
        # Abheben von einem Konto
        tk.Label(self.main_frame, text="Abhebung").grid(row=0, columnspan=2, pady=10)

        tk.Label(self.main_frame, text="Kontonummer").grid(row=1, column=0, padx=10, pady=5)
        account_number_combobox = ttk.Combobox(self.main_frame)
        account_number_combobox.grid(row=1, column=1, padx=10, pady=5)

        account_data = [f"{account.account_number} - {account.account_holder}" for account in
                        self.account_manager.accounts]
        account_number_combobox['values'] = account_data

        tk.Label(self.main_frame, text="Betrag").grid(row=2, column=0, padx=10, pady=5)
        amount_entry = tk.Entry(self.main_frame)
        amount_entry.grid(row=2, column=1, padx=10, pady=5)

        def withdraw():
            # Funktion zum Durchführen einer Abhebung
            selected_account = account_number_combobox.get().strip()
            amount = amount_entry.get().strip()

            if not selected_account or not self.is_float(amount):
                messagebox.showerror("Fehler", "Ungültige Kontonummer oder Betrag.")
                return

            account_number = int(selected_account.split(" - ")[0])
            success = self.account_manager.withdraw_from_account(account_number, float(amount))

            if success:
                messagebox.showinfo("Erfolg", "Abhebung erfolgreich.")
            else:
                account = self.account_manager.find_account(account_number)

                if not account:
                    messagebox.showerror("Fehler", "Konto nicht gefunden.")
                else:
                    messagebox.showerror("Fehler", "Unzureichender Kontostand.")

            self.show_main_menu()

        tk.Button(self.main_frame, text="Abheben",
                  command=withdraw).grid(row=3, columnspan=2, padx=10, pady=5)
        tk.Button(self.main_frame, text="Zurück",
                  command=self.show_main_menu).grid(row=4, columnspan=2, padx=10, pady=5)

    def save_accounts_to_csv(self):
        # Speichern der Kontodaten in eine CSV-Datei mit dem namen "accounts.csv"
        with open("accounts.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Kontonummer", "Kontoinhaber", "Kontostand"])
            for account in self.account_manager.accounts:
                writer.writerow([account.account_number, account.account_holder, account.balance])
        messagebox.showinfo("Erfolg", "Kontodaten wurden in accounts.csv gespeichert.")

    @staticmethod
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = AccountApp(root)
    root.mainloop()
