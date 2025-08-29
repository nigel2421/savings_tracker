import models
import storage
import ui
import reports
from config import CURRENCY_SYMBOL

def main():
    """Main function to run the application."""
    platforms = storage.load_platforms()

    while True:
        choice = ui.display_menu()

        if choice == '1': # Add New Platform
            name, balance, interest_rate = ui.get_platform_details()
            if name not in platforms:
                platforms[name] = models.InvestmentPlatform(name, balance, interest_rate)
                print(f"Platform '{name}' added.")
            else:
                print(f"Platform '{name}' already exists.")

        elif choice == '2': # Update Existing Platform
            if not platforms:
                print("No platforms to update.")
                continue
            
            platform_name = input("Enter the name of the platform to update: ")
            if platform_name in platforms:
                platform = platforms[platform_name]
                while True:
                    update_choice = ui.update_platform_menu(platform_name)
                    if update_choice == '1': # Deposit
                        amount = ui.get_transaction_amount("deposit")
                        platform.deposit(amount)
                    elif update_choice == '2': # Withdraw
                        amount = ui.get_transaction_amount("withdrawal")
                        platform.withdraw(amount)
                    elif update_choice == '3': # Apply Interest
                        interest_earned = platform.apply_interest()
                        print(f"Interest of {CURRENCY_SYMBOL}{interest_earned:,.2f} applied.")
                    elif update_choice == '4':
                        break
                    else:
                        print("Invalid option.")
                    storage.save_platforms(platforms) # Save after each update
            else:
                print("Platform not found.")

        elif choice == '3': # View Summary
            reports.display_summary(platforms)
            if platforms:
                show_history = input("Show transaction history for a platform? (y/n): ")
                if show_history.lower() == 'y':
                    platform_name = input("Enter platform name: ")
                    if platform_name in platforms:
                        reports.display_platform_history(platforms[platform_name])
                    else:
                        print("Platform not found.")

        elif choice == '4': # Exit
            storage.save_platforms(platforms)
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()