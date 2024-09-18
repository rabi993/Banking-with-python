import random

class Account:
    def __init__(self, name, email, password, address, account_type, bank):
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.account_type = account_type
        self.account_number = self.generate_account_number()
        self.balance = 0
        self.loan_count = 0
        self.loan_amount = 0
        self.transaction_history = []
        self.transactions_enabled = True  
        self.loan_enabled = True  
        self.bank = bank 

    def generate_account_number(self):
        return random.randint(10000000, 99999999)
    
    def deposit(self, amount):
        if not self.transactions_enabled:
            return "Transactions are disabled for this account"
        self.balance += amount
        self.bank.increase_total_balance(amount)  
        self.transaction_history.append(f"Deposited {amount}")
        return f"Deposit successful. New balance: {self.balance}"
    
    def withdraw(self, amount):
        if not self.transactions_enabled:
            return "Transactions are disabled for this account"
        if amount > self.balance:
            if self.balance == 0:
                return "Sorry!! The bank will be bankrupt."
            return "Withdrawal amount exceeded"
        else:
            self.balance -= amount
            self.bank.decrease_total_balance(amount)  
            self.transaction_history.append(f"Withdrew {amount}")
            return f"Withdrawal successful. New balance: {self.balance}"
    def transfer(self, amount, target_account):
        if not self.transactions_enabled:
            return "Transactions are disabled for this account"
        if amount > self.balance:
            return "Insufficient balance"
        else:
            self.balance -= amount
            target_account.balance += amount
            self.transaction_history.append(f"Transferred {amount} to account {target_account.account_number}")
            target_account.transaction_history.append(f"Received {amount} from account {self.account_number}")
            return "Transfer successful"
    
    def take_loan(self, loan_amount, bank):
        if not self.loan_enabled:
            return "Loan feature is disabled for this account"
        if self.loan_count >= 2 or not bank.loan_feature:
            return "Loan request denied"
        self.balance += loan_amount
        self.loan_count += 1
        self.loan_amount += loan_amount
        bank.total_loan_amount += loan_amount
        self.transaction_history.append(f"Loan of {loan_amount} taken")
        return "Loan granted"

    def repay_loan(self, amount, bank):
        if amount > self.balance:
            return "Insufficient balance"
        elif amount > self.loan_amount:
            return "Repayment amount exceeds the loan amount"
        else:
            self.balance -= amount
            self.loan_amount -= amount
            bank.total_loan_amount -= amount
            self.transaction_history.append(f"Repaid loan of {amount}")
            return f"Loan repayment successful. Remaining loan amount: {self.loan_amount}"
    
    def get_transaction_history(self):
        return self.transaction_history
    
    def enable_transactions(self):
        self.transactions_enabled = True
        return "Transactions enabled"
    
    def disable_transactions(self):
        self.transactions_enabled = False
        return "Transactions disabled"
    
    def enable_loan(self):
        self.loan_enabled = True
        return "Loan feature enabled"
    
    def disable_loan(self):
        self.loan_enabled = False
        return "Loan feature disabled"

class Bank:
    def __init__(self):
        self.accounts = {}
        self.total_balance = 0
        self.total_loan_amount = 0
        self.loan_feature = True
    
    def add_account(self, account):
        if account.account_number in self.accounts:
            return "Account already exists"
        self.accounts[account.account_number] = account
        return f"Account created successfully with account number {account.account_number}"
    
    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            return "Account deleted successfully"
        return "Account not found"

    def get_total_balance(self):
        return self.total_balance

    def increase_total_balance(self, amount):
        self.total_balance += amount

    def decrease_total_balance(self, amount):
        self.total_balance -= amount

    def get_total_loan_amount(self):
        return self.total_loan_amount
    
    def toggle_loan_feature(self, status):
        self.loan_feature = status
        return "Loan feature enabled" if status else "Loan feature disabled"
    
    def get_account(self, account_number):
        return self.accounts.get(account_number)
    
    def transfer_money(self, from_account, to_account, amount):
        return from_account.transfer(amount, to_account)
    
    def enable_account_transactions(self, account_number):
        account = self.get_account(account_number)
        if account:
            return account.enable_transactions()
        return "Account not found"
    
    def disable_account_transactions(self, account_number):
        account = self.get_account(account_number)
        if account:
            return account.disable_transactions()
        return "Account not found"
    
    def enable_account_loan(self, account_number):
        account = self.get_account(account_number)
        if account:
            return account.enable_loan()
        return "Account not found"
    
    def disable_account_loan(self, account_number):
        account = self.get_account(account_number)
        if account:
            return account.disable_loan()
        return "Account not found"
    
    def authenticate_user(self, name, password, account_number):
        account = self.get_account(account_number)
        if account and account.name == name and account.password == password:
            return account
        return None


class User:
    def __init__(self, bank):
        self.bank = bank

    def create_account(self, name, email, password, address, account_type):
        account = Account(name, email, password, address, account_type, self.bank)  
        result = self.bank.add_account(account)
        return f"Account created successfully! Your account number is {account.account_number}"
    
    def login(self, name, password, account_number):
        account = self.bank.authenticate_user(name, password, account_number)
        if account:
            return account
        return "Invalid login credentials"


class Admin:
    def __init__(self, bank):
        self.bank = bank
        self.name = "admin"
        self.password = "admin"
        self.email = "admin@gmail.com"
    
    def login(self, name, password):
        if self.name == name and self.password == password:
            return True
        return False
    
    def create_account(self, name, email, password, address, account_type):
        account = Account(name, email, password, address, account_type, self.bank) 
        return self.bank.add_account(account)
    
    def delete_account(self, account_number):
        return self.bank.delete_account(account_number)
    
    def get_all_accounts(self):
        return self.bank.accounts
    
    def check_total_balance(self):
        return self.bank.get_total_balance()
    
    def check_total_loan_amount(self):
        return self.bank.get_total_loan_amount()
    
    def toggle_loan_feature(self, status):
        return self.bank.toggle_loan_feature(status)
    
    def show_user_transaction_history(self, account_number):
        account = self.bank.accounts.get(account_number)
        if account:
            history = account.get_transaction_history()
            if history:
                return "\n".join(history)
            else:
                return "No transactions found for this user."
        else:
            return "Account not found."
    
    def enable_account_transactions(self, account_number):
        return self.bank.enable_account_transactions(account_number)
    
    def disable_account_transactions(self, account_number):
        return self.bank.disable_account_transactions(account_number)
    
    def enable_account_loan(self, account_number):
        return self.bank.enable_account_loan(account_number)
    
    def disable_account_loan(self, account_number):
        return self.bank.disable_account_loan(account_number)


def user_menu(user, account):
    while True:
        print("\nUser Menu:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transfer Money")
        print("5. Take Loan")
        print("6. Repay Loan")
        print("7. Check Transaction History")
        print("8. Exit")

        try:
            choice = input("Enter your choice: ")

            if choice == "1":
                amount = float(input("Enter amount to deposit: "))
                result = account.deposit(amount)
                print(result)

            elif choice == "2":
                amount = float(input("Enter amount to withdraw: "))
                result = account.withdraw(amount)
                print(result)

            elif choice == "3":
                print(f"Available balance: {account.balance}")

            elif choice == "4":
                target_account_number = int(input("Enter target account number: "))
                amount = float(input("Enter amount to transfer: "))
                target_account = user.bank.get_account(target_account_number)
                if target_account:
                    result = user.bank.transfer_money(account, target_account, amount)
                    print(result)
                else:
                    print("Account does not exist")

            elif choice == "5":
                loan_amount = float(input("Enter loan amount: "))
                result = account.take_loan(loan_amount, user.bank)
                print(result)

            elif choice == "6":
                print(f"Outstanding loan amount: {account.loan_amount}")
                amount = float(input("Enter amount to repay: "))
                result = account.repay_loan(amount, user.bank)
                print(result)

            elif choice == "7":
                history = account.get_transaction_history()
                if history:
                    print("\nTransaction History:")
                    for record in history:
                        print(record)
                else:
                    print("No transactions found")

            elif choice == "8":
                break

            else:
                print("Invalid choice, please try again.")
        
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")


def admin_menu(admin):
    while True:
        print("\nAdmin Menu:")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. View All Accounts")
        print("4. Check Total Bank Balance")
        print("5. Check Total Loan Amount")
        print("6. Toggle Loan Feature")
        print("7. View User Transaction History")
        print("8. Enable/Disable Transactions for Account")
        print("9. Enable/Disable Loan for Account")
        print("10. Exit")

        try:
            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter account holder name: ")
                email = input("Enter account holder email: ")
                password = input("Enter account holder password: ")
                address = input("Enter account holder address: ")
                account_type = input("Enter account type (Savings/Current): ")
                result = admin.create_account(name, email, password, address, account_type)
                print(result)

            elif choice == "2":
                account_number = int(input("Enter account number to delete: "))
                result = admin.delete_account(account_number)
                print(result)

            elif choice == "3":
                accounts = admin.get_all_accounts()
                if accounts:
                    print("\nAll Accounts:")
                    for account in accounts.values():
                        print(f"Account Number: {account.account_number}, Name: {account.name}, Balance: {account.balance}")
                else:
                    print("No accounts found")

            elif choice == "4":
                print(f"Total bank balance: {admin.check_total_balance()}")

            elif choice == "5":
                print(f"Total loan amount: {admin.check_total_loan_amount()}")

            elif choice == "6":
                status = input("Enable or Disable loan feature (e/d): ").lower()
                if status == "e":
                    result = admin.toggle_loan_feature(True)
                elif status == "d":
                    result = admin.toggle_loan_feature(False)
                else:
                    result = "Invalid input"
                print(result)

            elif choice == "7":
                account_number = int(input("Enter account number to view transaction history: "))
                result = admin.show_user_transaction_history(account_number)
                print(result)

            elif choice == "8":
                account_number = int(input("Enter account number to modify transactions: "))
                status = input("Enable or Disable transactions (e/d): ").lower()
                if status == "e":
                    result = admin.enable_account_transactions(account_number)
                elif status == "d":
                    result = admin.disable_account_transactions(account_number)
                else:
                    result = "Invalid input"
                print(result)

            elif choice == "9":
                account_number = int(input("Enter account number to modify loan feature: "))
                status = input("Enable or Disable loan feature (e/d): ").lower()
                if status == "e":
                    result = admin.enable_account_loan(account_number)
                elif status == "d":
                    result = admin.disable_account_loan(account_number)
                else:
                    result = "Invalid input"
                print(result)

            elif choice == "10":
                break

            else:
                print("Invalid choice, please try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")


def main():
    bank = Bank()
    user = User(bank)
    admin = Admin(bank)

    while True:
        print("\nBanking System:")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Create User Account")
        print("4. Exit")

        try:
            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter admin name: ")
                password = input("Enter admin password: ")
                if admin.login(name, password):
                    admin_menu(admin)
                else:
                    print("Invalid admin credentials")

            elif choice == "2":
                name = input("Enter your name: ")
                password = input("Enter your password: ")
                account_number = int(input("Enter your account number: "))
                account = user.login(name, password, account_number)
                if account:
                    user_menu(user, account)
                else:
                    print("Invalid user credentials")

            elif choice == "3":
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                address = input("Enter your address: ")
                account_type = input("Enter account type (Savings/Current): ")
                result = user.create_account(name, email, password, address, account_type)
                print(result)

            elif choice == "4":
                break

            else:
                print("Invalid choice, please try again.")
        
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
