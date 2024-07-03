from accountmanager import AccountManager


def main():
    manager = AccountManager()

    while True:
        print("\nKontoverwaltung\n"
              "1. Konto anlegen\n"
              "2. Konto löschen\n"
              "3. Geld einzahlen\n"
              "4. Geld abheben\n"
              "5. Konto anzeigen\n"
              "6. Alle Konten anzeigen\n"
              "7. Beenden\n")

        choice = input("Wählen Sie eine Option: ")

        if choice == "1":
            new_account_holder = input("Inhaber: ").strip()
            new_initial_balance = float(input("Anfangsstand: ").strip())
            manager.create_account(new_account_holder, new_initial_balance)

        elif choice == "2":
            if manager.display_all_accounts():
                try:
                    account_number = int(input("Kontonummer des zu löschenden Kontos: ").strip())
                    manager.delete_account(account_number)
                except ValueError:
                    print("Ungültige Eingabe. Bitte geben Sie eine gültige Kontonummer ein.")

        elif choice == "3":
            if manager.display_all_accounts():
                account_number = int(input("Kontonummer: ").strip())
                amount = float(input("Betrag: ").strip())
                manager.deposit_to_account(account_number, amount)

        elif choice == "4":
            manager.display_all_accounts()
            account_number = int(input("Kontonummer: ").strip())
            amount = float(input("Betrag: ").strip())
            manager.withdraw_from_account(account_number, amount)

        elif choice == "5":
            manager.display_account_details()

        elif choice == "6":
            manager.display_all_accounts()

        elif choice == "7":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")


if __name__ == "__main__":
    main()
