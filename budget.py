# budget.py
# A budget tracker to manage income, expenses and savings

import tkinter as tk
from tkinter import messagebox

# ══════════════════════════════════════════
# DATA — stored in lists
# ══════════════════════════════════════════

transactions = []    # list of dictionaries — each one is a transaction
# example: {"description": "Salary", "amount": 45000, "type": "income"}

# ══════════════════════════════════════════
# LOGIC
# ══════════════════════════════════════════

def get_totals():
    """Calculate total income, expenses and savings"""
    total_income   = 0
    total_expenses = 0

    for t in transactions:
        if t["type"] == "income":
            total_income += t["amount"]
        else:
            total_expenses += t["amount"]

    savings = total_income - total_expenses
    return total_income, total_expenses, savings

def add_transaction(transaction_type):
    """Called when + Income or - Expense button is clicked"""
    description = entry_desc.get().strip()    # get text from description box
    amount_text  = entry_amount.get().strip() # get text from amount box

    # validation — make sure fields are not empty
    if not description:
        messagebox.showwarning("Missing!", "Please enter a description.")
        return

    # validation — make sure amount is a valid number
    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Invalid!", "Please enter a valid amount.")
        return

    # save the transaction
    transactions.append({
        "description": description,
        "amount": amount,
        "type": transaction_type    # "income" or "expense"
    })

    # clear the input fields
    entry_desc.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

    # refresh everything on screen
    update_display()

def delete_last():
    """Remove the most recent transaction"""
    if transactions:
        transactions.pop()    # .pop() removes the last item from a list
        update_display()
    else:
        messagebox.showinfo("Empty!", "No transactions to delete.")

def clear_all():
    """Wipe all transactions after confirmation"""
    if messagebox.askyesno("Clear all?", "Are you sure you want to clear everything?"):
        transactions.clear()
        update_display()

def update_display():
    """Refresh the summary cards and transaction list"""
    income, expenses, savings = get_totals()

    # update the 3 summary cards
    label_income.config(text=f"₹{income:,.0f}")
    label_expenses.config(text=f"₹{expenses:,.0f}")
    label_savings.config(
        text=f"₹{savings:,.0f}",
        fg="#30d158" if savings >= 0 else "#ff453a"   # green if positive, red if negative
    )

    # update savings status message
    if savings > 0:
        status = f"You are saving ₹{savings:,.0f}. Great job!"
        status_label.config(text=status, fg="#30d158")
    elif savings == 0:
        status_label.config(text="Breaking even — try to save more!", fg="#ff9f0a")
    else:
        status_label.config(text=f"Overspending by ₹{abs(savings):,.0f}! Cut expenses.", fg="#ff453a")

    # clear the transaction listbox and reload
    listbox.delete(0, tk.END)

    # show newest transactions first using reversed()
    for t in reversed(transactions):
        if t["type"] == "income":
            listbox.insert(tk.END, f"  + ₹{t['amount']:,.0f}   {t['description']}")
            listbox.itemconfig(tk.END, fg="#30d158")   # green for income
        else:
            listbox.insert(tk.END, f"  - ₹{t['amount']:,.0f}   {t['description']}")
            listbox.itemconfig(tk.END, fg="#ff453a")   # red for expense

# ══════════════════════════════════════════
# THE UI
# ══════════════════════════════════════════

window = tk.Tk()
window.title("Budget Tracker")
window.resizable(False, False)
window.configure(bg="#1c1c1e")

# ── Title ─────────────────────────────────
tk.Label(
    window, text="Budget Tracker",
    font=("Arial", 20, "bold"),
    bg="#1c1c1e", fg="white"
).pack(pady=(20, 10))

# ── Summary cards (Income / Expenses / Savings) ───
cards_frame = tk.Frame(window, bg="#1c1c1e")
cards_frame.pack(padx=20, pady=(0, 15))

def make_card(parent, title, color):
    """Helper to create one summary card"""
    frame = tk.Frame(parent, bg=color, padx=20, pady=12)
    frame.pack(side="left", padx=6)
    tk.Label(frame, text=title, font=("Arial", 11), bg=color, fg="white").pack()
    value_label = tk.Label(frame, text="₹0", font=("Arial", 18, "bold"), bg=color, fg="white")
    value_label.pack()
    return value_label

label_income   = make_card(cards_frame, "Income",   "#1a3a2a")
label_expenses = make_card(cards_frame, "Expenses", "#3a1a1a")
label_savings  = make_card(cards_frame, "Savings",  "#1a2a3a")

# ── Status message ────────────────────────
status_label = tk.Label(
    window, text="Add your first transaction below!",
    font=("Arial", 12), bg="#1c1c1e", fg="#888888"
)
status_label.pack(pady=(0, 15))

# ── Input area ────────────────────────────
input_frame = tk.Frame(window, bg="#2c2c2e", padx=20, pady=15)
input_frame.pack(padx=20, pady=(0, 10), fill="x")

tk.Label(input_frame, text="Description", font=("Arial", 12),
         bg="#2c2c2e", fg="#888888").pack(anchor="w")
entry_desc = tk.Entry(input_frame, font=("Arial", 13), bg="#3a3a3c",
                      fg="white", insertbackground="white",
                      relief="flat", bd=5)
entry_desc.pack(fill="x", pady=(2, 10))

tk.Label(input_frame, text="Amount (₹)", font=("Arial", 12),
         bg="#2c2c2e", fg="#888888").pack(anchor="w")
entry_amount = tk.Entry(input_frame, font=("Arial", 13), bg="#3a3a3c",
                        fg="white", insertbackground="white",
                        relief="flat", bd=5)
entry_amount.pack(fill="x", pady=(2, 12))

# Income and Expense buttons side by side
btn_row = tk.Frame(input_frame, bg="#2c2c2e")
btn_row.pack(fill="x")

tk.Button(
    btn_row, text="+ Add Income",
    font=("Arial", 13, "bold"),
    bg="#1a3a2a", fg="#30d158",
    activebackground="#30d158", activeforeground="#1a3a2a",
    relief="flat", bd=0, cursor="hand2", height=2,
    command=lambda: add_transaction("income")
).pack(side="left", expand=True, fill="x", padx=(0, 5))

tk.Button(
    btn_row, text="- Add Expense",
    font=("Arial", 13, "bold"),
    bg="#3a1a1a", fg="#ff453a",
    activebackground="#ff453a", activeforeground="#3a1a1a",
    relief="flat", bd=0, cursor="hand2", height=2,
    command=lambda: add_transaction("expense")
).pack(side="left", expand=True, fill="x")

# ── Transaction list ──────────────────────
tk.Label(
    window, text="Transactions",
    font=("Arial", 13, "bold"),
    bg="#1c1c1e", fg="#888888"
).pack(anchor="w", padx=20, pady=(10, 4))

listbox = tk.Listbox(
    window,
    font=("Arial", 13),
    bg="#2c2c2e", fg="white",
    selectbackground="#3a3a3c",
    relief="flat", bd=0,
    height=8
)
listbox.pack(padx=20, fill="x")

# ── Bottom action buttons ─────────────────
bottom_frame = tk.Frame(window, bg="#1c1c1e")
bottom_frame.pack(padx=20, pady=15, fill="x")

tk.Button(
    bottom_frame, text="Undo last",
    font=("Arial", 12),
    bg="#2c2c2e", fg="#ff9f0a",
    relief="flat", bd=0, cursor="hand2",
    command=delete_last
).pack(side="left", padx=(0, 8))

tk.Button(
    bottom_frame, text="Clear all",
    font=("Arial", 12),
    bg="#2c2c2e", fg="#ff453a",
    relief="flat", bd=0, cursor="hand2",
    command=clear_all
).pack(side="left")

# ── Start ─────────────────────────────────
update_display()
window.mainloop()