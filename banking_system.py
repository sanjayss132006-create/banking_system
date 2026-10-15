from abc import ABC, abstractmethod
from datetime import datetime


class Account(ABC):
    def __init__(self, name, account_no, balance=0):
        self.name = name
        self.account_no = account_no
        self.__balance = balance
        self.transactions = []
        self.record("Account created")

    def record(self, message):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append(f"{time} - {message}")

    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            print("Enter a valid amount.")
            return
        self.__balance += amount
        self.record(f"Deposited Rs.{amount:.2f}")
        print("Deposit successful!")

    def withdraw(self, amount):
        if amount <= 0:
            print("Enter a valid amount.")
        elif amount > self.__balance:
            print("Insufficient balance.")
        else:
            self.__balance -= amount
            self.record(f"Withdrawn Rs.{amount:.2f}")
            print("Withdrawal successful!")

    @abstractmethod
    def account_type(self):
        pass

    def show_details(self):
        print("\nAccount Holder:", self.name)
        print("Account Number:", self.account_no)
        print("Account Type:", self.account_type())
        print("Balance: Rs.", self.get_balance())


class SavingsAccount(Account):
    def account_type(self):
        return "Savings Account"


class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        name = input("Enter account holder name: ")
        number = input("Enter account number: ")

        if not name.strip() or not number.strip():
            print("Name and account number are required.")
            return

        if number in self.accounts:
            print("Account number already exists.")
            return

        try:
            balance = float(input("Enter opening balance: "))
            if balance < 0:
                print("Balance cannot be negative.")
                return
        except ValueError:
            print("Enter a valid amount.")
            return

        self.accounts[number] = SavingsAccount(
            name, number, balance
        )
        print("Account created successfully!")

    def find_account(self):
        number = input("Enter account number: ")
        account = self.accounts.get(number)

        if account is None:
            print("Account not found.")
        return account

    def run(self):
        while True:
            print("\n--- PYTHON BANKING SYSTEM ---")
            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Check Balance")
            print("5. Transaction History")
            print("6. Account Details")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.create_account()

            elif choice in ("2", "3", "4", "5", "6"):
                account = self.find_account()

                if account is None:
                    continue

                if choice in ("2", "3"):
                    try:
                        amount = float(input("Enter amount: "))
                        if choice == "2":
                            account.deposit(amount)
                        else:
                            account.withdraw(amount)
                    except ValueError:
                        print("Enter a valid amount.")

                elif choice == "4":
                    print("Balance: Rs.", account.get_balance())

                elif choice == "5":
                    print("\n--- Transaction History ---")
                    for transaction in account.transactions:
                        print(transaction)

                elif choice == "6":
                    account.show_details()

            elif choice == "7":
                print("Thank you for using our bank!")
                break

            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    bank = Bank()
    bank.run()