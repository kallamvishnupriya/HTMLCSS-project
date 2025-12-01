import tkinter as tk
from tkinter import messagebox, ttk


# --------------------------------------------------------
# OOP BANK SYSTEM (same logic, GUI on top)
# --------------------------------------------------------

class Account:
    def __init__(self, account_number, owner_name, balance=0.0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            return False, "Deposit amount must be positive."
        self.balance += amount
        return True, f"Deposited {amount}. New balance: {self.balance}"

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Withdraw amount must be positive."
        if amount > self.balance:
            return False, "Insufficient balance."
        self.balance -= amount
        return True, f"Withdrew {amount}. New balance: {self.balance}"

    def view_balance(self):
        return f"Owner: {self.owner_name}\nBalance: {self.balance}"


class SavingsAccount(Account):
    def __init__(self, account_number, owner_name, balance=0.0, interest_rate=0.03):
        super().__init__(account_number, owner_name, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return f"Interest added: {interest}. New balance: {self.balance}"


class CurrentAccount(Account):
    def __init__(self, account_number, owner_name, balance=0.0, overdraft_limit=500.0):
        super().__init__(account_number, owner_name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Withdraw amount must be positive."

        if amount > self.balance + self.overdraft_limit:
            return False, "Overdraft limit exceeded."

        self.balance -= amount
        return True, f"Withdrew {amount}. New balance: {self.balance}"


# --------------------------------------------------------
# TKINTER GUI
# --------------------------------------------------------

accounts = {}


def create_account():
    acc_num = entry_acc.get()
    owner = entry_owner.get()
    bal = entry_balance.get()

    if not acc_num or not owner or not bal:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        bal = float(bal)
    except:
        messagebox.showerror("Error", "Balance must be a number.")
        return

    acc_type = combo_type.get()

    if acc_type == "Savings Account":
        acc = SavingsAccount(acc_num, owner, bal)
        accounts[acc_num] = acc
        messagebox.showinfo("Success", "Savings Account Created!")

    elif acc_type == "Current Account":
        try:
            overdraft = float(entry_overdraft.get())
        except:
            messagebox.showerror("Error", "Overdraft must be a number.")
            return
        acc = CurrentAccount(acc_num, owner, bal, overdraft)
        accounts[acc_num] = acc
        messagebox.showinfo("Success", "Current Account Created!")

    else:
        messagebox.showerror("Error", "Select account type.")


def find_account():
    acc_num = entry_action_acc.get()
    if acc_num in accounts:
        return accounts[acc_num]
    messagebox.showerror("Error", "Account not found.")
    return None


def deposit_money():
    acc = find_account()
    if not acc: return

    try:
        amount = float(entry_amount.get())
    except:
        messagebox.showerror("Error", "Enter valid amount.")
        return

    success, msg = acc.deposit(amount)
    messagebox.showinfo("Info", msg)


def withdraw_money():
    acc = find_account()
    if not acc: return

    try:
        amount = float(entry_amount.get())
    except:
        messagebox.showerror("Error", "Enter valid amount.")
        return

    success, msg = acc.withdraw(amount)
    messagebox.showinfo("Info", msg)


def view_balance():
    acc = find_account()
    if not acc: return
    messagebox.showinfo("Balance", acc.view_balance())


def add_interest():
    acc = find_account()
    if not acc: return

    if isinstance(acc, SavingsAccount):
        msg = acc.add_interest()
        messagebox.showinfo("Success", msg)
    else:
        messagebox.showerror("Error", "Only savings accounts can add interest")


# --------------------------------------------------------
# GUI Layout
# --------------------------------------------------------

root = tk.Tk()
root.title("Bank Account Simulator - Tkinter")
root.geometry("600x500")
root.resizable(False, False)


title = tk.Label(root, text="Bank Account Simulator", font=("Arial", 18, "bold"))
title.pack(pady=10)


# ---------------- CREATE ACCOUNT FRAME ----------------
frame_create = tk.LabelFrame(root, text="Create Account", font=("Arial", 12))
frame_create.pack(padx=10, pady=10, fill="x")

tk.Label(frame_create, text="Account Number:").grid(row=0, column=0, padx=5, pady=5)
entry_acc = tk.Entry(frame_create)
entry_acc.grid(row=0, column=1)

tk.Label(frame_create, text="Owner Name:").grid(row=1, column=0, padx=5, pady=5)
entry_owner = tk.Entry(frame_create)
entry_owner.grid(row=1, column=1)

tk.Label(frame_create, text="Initial Balance:").grid(row=2, column=0, padx=5, pady=5)
entry_balance = tk.Entry(frame_create)
entry_balance.grid(row=2, column=1)

tk.Label(frame_create, text="Account Type:").grid(row=3, column=0, padx=5, pady=5)
combo_type = ttk.Combobox(frame_create, values=["Savings Account", "Current Account"])
combo_type.grid(row=3, column=1)

tk.Label(frame_create, text="Overdraft Limit:").grid(row=4, column=0, padx=5, pady=5)
entry_overdraft = tk.Entry(frame_create)
entry_overdraft.grid(row=4, column=1)

btn_create = tk.Button(frame_create, text="Create Account", command=create_account)
btn_create.grid(row=5, column=0, columnspan=2, pady=10)


# ---------------- ACTION FRAME ----------------
frame_action = tk.LabelFrame(root, text="Account Actions", font=("Arial", 12))
frame_action.pack(padx=10, pady=10, fill="x")

tk.Label(frame_action, text="Account Number:").grid(row=0, column=0, padx=5, pady=5)
entry_action_acc = tk.Entry(frame_action)
entry_action_acc.grid(row=0, column=1)

tk.Label(frame_action, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
entry_amount = tk.Entry(frame_action)
entry_amount.grid(row=1, column=1)


btn_deposit = tk.Button(frame_action, text="Deposit", width=12, command=deposit_money)
btn_deposit.grid(row=2, column=0, pady=5)

btn_withdraw = tk.Button(frame_action, text="Withdraw", width=12, command=withdraw_money)
btn_withdraw.grid(row=2, column=1, pady=5)

btn_view = tk.Button(frame_action, text="View Balance", width=12, command=view_balance)
btn_view.grid(row=3, column=0, pady=5)

btn_interest = tk.Button(frame_action, text="Add Interest", width=12, command=add_interest)
btn_interest.grid(row=3, column=1, pady=5)


root.mainloop()
