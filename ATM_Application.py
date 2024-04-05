class Admin:
    def __init__(self):
        self.bank_details = {}  
        self.customer_details = {} 

    def manage_bank_details(self, bank_name, amount):
        self.bank_details[bank_name] = amount

    def manage_customer_details(self, name, account_number, pin, balance=0):
        self.customer_details[account_number] = {
            "name": name,
            "pin": pin,
            "balance": balance,
            "mini_statement": [],
        }

    def manage_amount(self, bank_name, amount):
        if bank_name in self.bank_details:
            self.bank_details[bank_name] += amount
        else:
            print("Bank not found.")

    def get_customer_balance(self, account_number):
        if account_number in self.customer_details:
            return self.customer_details[account_number]["balance"]
        else:
            return None


class Customer:
    def __init__(self, account_number, pin):
        self.account_number = account_number
        self.pin = pin

    def withdraw(self, amount, admin):
        if self.account_number in admin.customer_details:
            if admin.customer_details[self.account_number]["balance"] >= amount:
                admin.customer_details[self.account_number]["balance"] -= amount
                admin.customer_details[self.account_number]["mini_statement"].append(
                    f"Withdrawn {amount}"
                )
                return f"Withdrawn {amount}. New balance: {admin.customer_details[self.account_number]['balance']}"
            else:
                return "Insufficient funds"
        else:
            return "Account not found"

    def deposit(self, amount, admin):
        if self.account_number in admin.customer_details:
            admin.customer_details[self.account_number]["balance"] += amount
            admin.customer_details[self.account_number]["mini_statement"].append(
                f"Deposited ${amount}"
            )
            return f"Deposited {amount}. New balance: {admin.customer_details[self.account_number]['balance']}"
        else:
            return "Account not found"

    def check_balance(self, admin):
        if self.account_number in admin.customer_details:
            return f"Your balance: {admin.customer_details[self.account_number]['balance']}"
        else:
            return "Account not found"

    def change_pin(self, new_pin, admin):
        if self.account_number in admin.customer_details:
            admin.customer_details[self.account_number]["pin"] = new_pin
            return "PIN changed successfully"
        else:
            return "Account not found"

    def transfer(self, recipient_account_number, amount, admin):
        if (
            self.account_number in admin.customer_details
            and recipient_account_number in admin.customer_details
        ):
            if (
                admin.customer_details[self.account_number]["balance"] >= amount
                and self.account_number != recipient_account_number
            ):
                admin.customer_details[self.account_number]["balance"] -= amount
                admin.customer_details[recipient_account_number]["balance"] += amount
                admin.customer_details[self.account_number]["mini_statement"].append(
                    f"Transferred {amount} to {recipient_account_number}"
                )
                admin.customer_details[recipient_account_number]["mini_statement"].append(
                    f"Received {amount} from {self.account_number}"
                )
                return f"Transferred {amount} to {recipient_account_number}. New balance: {admin.customer_details[self.account_number]['balance']}"
            else:
                return "Transfer failed"
        else:
            return "Account(s) not found"

    def generate_mini_statement(self, admin):
        if self.account_number in admin.customer_details:
            return admin.customer_details[self.account_number]["mini_statement"]
        else:
            return "Account not found"


def main():
    admin = Admin()

    while True:
        print("1. Admin\n2. User")
        choice = int(input("Enter Your Choice: "))

        if choice == 1:
            while True:
                print("\n1. Create Bank\n2. Create User")
                choice = int(input("Enter Your Choice: "))

                if choice == 1:
                    bank_name = input("Enter Bank Name: ")
                    amount = int(input("Enter Amount: "))
                    admin.manage_bank_details(bank_name, amount)
                elif choice == 2:
                    name = input("Enter Name: ")
                    acc_no = int(input("Enter Account Number: "))
                    bal = int(input("Enter Balance: "))
                    pin = input("Enter PIN: ")
                    admin.manage_customer_details(name, acc_no, pin, bal)

                con = input("Do you want to continue (Y/N)? ").lower()

                if con == 'n':
                    break

        elif choice == 2:
            acc_no = int(input("Enter Account Number: "))
            pin = input("Enter PIN: ")

            if acc_no in admin.customer_details and admin.customer_details[acc_no]["pin"] == pin:
                customer = Customer(acc_no, pin)

                while True:
                    print("\n1. Withdraw\n2. Deposit\n3. Change PIN\n4. Check Balance\n5. Amount Transfer\n6. Mini Statement")
                    choice = int(input("Enter Your Choice: "))

                    if choice == 1:
                        amount = int(input("Enter Amount to Withdraw: "))
                        print(customer.withdraw(amount, admin))
                    elif choice == 2:
                        amount = int(input("Enter Amount to Deposit: "))
                        print(customer.deposit(amount, admin))
                    elif choice == 3:
                        new_pin = input("Enter New PIN: ")
                        print(customer.change_pin(new_pin, admin))
                    elif choice == 4:
                        print(customer.check_balance(admin))
                    elif choice == 5:
                        recipient_acc = int(input("Enter Recipient's Account Number: "))
                        amount = int(input("Enter Amount to Transfer: "))
                        print(customer.transfer(recipient_acc, amount, admin))
                    elif choice == 6:
                        print(customer.generate_mini_statement(admin))

                    con = input("Do you want to continue (Y/N)? ").lower()

                    if con == 'n':
                        break
            else:
                print("Invalid Account Number or PIN")
                continue

        con_main = input("Do you want to continue as Admin/User (Y/N)? ").lower()

        if con_main == 'n':
            break

if __name__ == "__main__":
    main()