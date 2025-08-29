from config import CURRENCY_SYMBOL

def display_summary(platforms):
    """Displays a summary of all investment platforms."""
    if not platforms:
        print("\nNo platforms to display. Please add a platform first.")
        return

    print("\n--- Platform Summary ---")
    total_balance = 0
    for name, platform in platforms.items():
        print(f"Platform: {name}")
        print(f"  - Balance: {CURRENCY_SYMBOL}{platform.balance:,.2f}")
        print(f"  - Interest Rate: {platform.interest_rate}%")
        total_balance += platform.balance

    print("-------------------------")
    print(f"Total Balance Across All Platforms: {CURRENCY_SYMBOL}{total_balance:,.2f}")
    print("-------------------------")

def display_platform_history(platform):
    """Displays the transaction history for a single platform."""
    print(f"\n--- Transaction History for {platform.name} ---")
    if not platform.history:
        print("No transactions recorded yet.")
        return

    for record in platform.history:
        print(f"  - Type: {record['type']}, Amount: {CURRENCY_SYMBOL}{record['amount']:,.2f}, "
              f"New Balance: {CURRENCY_SYMBOL}{record['balance']:,.2f}, Date: {record['timestamp']}")