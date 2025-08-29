from datetime import datetime

class InvestmentPlatform:
    """Represents a single investment platform with its balance and history."""
    def __init__(self, name, balance=0.0, interest_rate=0.0):
        self.name = name
        self.balance = balance
        self.interest_rate = interest_rate
        self.history = []

    def deposit(self, amount):
        """Adds a specified amount to the balance and logs the transaction."""
        if amount > 0:
            self.balance += amount
            self._log_transaction("Deposit", amount)
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        """Subtracts a specified amount from the balance and logs the transaction."""
        if 0 < amount <= self.balance:
            self.balance -= amount
            self._log_transaction("Withdrawal", -amount)
        else:
            print("Withdrawal amount is invalid or exceeds balance.")

    def apply_interest(self):
        """Calculates and adds interest to the balance."""
        interest = self.balance * (self.interest_rate / 100)
        if interest > 0:
            self.balance += interest
            self._log_transaction("Interest", interest)
        return interest

    def _log_transaction(self, tx_type, amount):
        """Private method to log a transaction with a timestamp."""
        self.history.append({
            "type": tx_type,
            "amount": amount,
            "balance": self.balance,
            "timestamp": datetime.now().isoformat()
        })

    def to_dict(self):
        """Converts the platform object to a dictionary for JSON serialization."""
        return {
            "name": self.name,
            "balance": self.balance,
            "interest_rate": self.interest_rate,
            "history": self.history
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a platform object from a dictionary."""
        platform = cls(data['name'], data['balance'], data['interest_rate'])
        platform.history = data.get('history', [])
        return platform