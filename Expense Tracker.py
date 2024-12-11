import tkinter as tk
from tkinter import messagebox, ttk
import csv

# Function to add expense
def add_expense():
    date = entry_date.get()
    category = entry_category.get()
    amount = entry_amount.get()
    description = entry_description.get()

    if date and category and amount and description:
        with open('expenses.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount, description])
        entry_date.delete(0, tk.END)
        entry_category.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_description.delete(0, tk.END)
        messagebox.showinfo('Success', 'Expense added!')
        view_expenses()
    else:
        messagebox.showwarning('Input Error', 'All fields are required.')

# Function to view expenses
def view_expenses():
    try:
        with open('expenses.csv', 'r') as file:
            reader = csv.reader(file)
            expenses_list.delete(*expenses_list.get_children())
            for row in reader:
                expenses_list.insert('', tk.END, values=row)
    except FileNotFoundError:
        open('expenses.csv', 'w').close()

# Function to delete a selected expense permanently
def delete_expense():
    selected_item = expenses_list.selection()
    if not selected_item:
        messagebox.showwarning("Delete Error", "No expense selected.")
        return

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected expense permanently?")
    if not confirm:
        return

    for item in selected_item:
        selected_values = expenses_list.item(item, 'values')
        expenses_list.delete(item)

        # Remove the selected item from the CSV file
        all_expenses = []
        with open('expenses.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if list(selected_values) != row:
                    all_expenses.append(row)

        with open('expenses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(all_expenses)

    messagebox.showinfo('Success', 'Expense deleted permanently!')
    view_expenses()

# Creating the main window
root = tk.Tk()
root.title('Expense Tracker')
root.configure(bg='#333333')  # Dark background color

# Setting up the theme with Yellow, White, and Pink accents
style = ttk.Style()
style.theme_use('clam')
style.configure('Treeview.Heading', background='#ffcc00', foreground='black', font=('Arial', 14, 'bold'))
style.configure('Treeview', background='#333333', foreground='white', rowheight=25, fieldbackground='#333333', font=('Arial', 12))

# Define RGB Colors
label_bg = '#333333'  # Dark background for labels
label_fg = '#ffcc00'  # Yellow color for labels
button_bg = '#ff66b2'  # Pink background for buttons
button_fg = 'white'  # White text for buttons
entry_bg = '#e0e0e0'  # Light gray background for entries
entry_fg = '#333333'  # Dark text for entries
success_button_bg = '#4caf50'  # Green color for success button (Add Expense)
success_button_fg = 'white'  # White text for the success button

# Creating and placing widgets
tk.Label(root, text='Date', bg=label_bg, fg=label_fg, font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)
entry_date = tk.Entry(root, font=('Arial', 14), bg=entry_bg, fg=entry_fg)
entry_date.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text='Category', bg=label_bg, fg=label_fg, font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10)
entry_category = tk.Entry(root, font=('Arial', 14), bg=entry_bg, fg=entry_fg)
entry_category.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text='Amount (INR)', bg=label_bg, fg=label_fg, font=('Arial', 14)).grid(row=2, column=0, padx=10, pady=10)
entry_amount = tk.Entry(root, font=('Arial', 14), bg=entry_bg, fg=entry_fg)
entry_amount.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text='Description', bg=label_bg, fg=label_fg, font=('Arial', 14)).grid(row=3, column=0, padx=10, pady=10)
entry_description = tk.Entry(root, font=('Arial', 14), bg=entry_bg, fg=entry_fg)
entry_description.grid(row=3, column=1, padx=10, pady=10)

tk.Button(root, text='Add Expense', command=add_expense, bg=success_button_bg, fg=success_button_fg, font=('Arial', 14)).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text='View Expenses', command=view_expenses, bg='#ffcc00', fg='black', font=('Arial', 14)).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text='Delete Selected Expense', command=delete_expense, bg=button_bg, fg=button_fg, font=('Arial', 14)).grid(row=6, column=0, columnspan=2, pady=10)

# Treeview to display expenses
columns = ('date', 'category', 'amount', 'description')
expenses_list = ttk.Treeview(root, columns=columns, show='headings', height=8)
for col in columns:
    expenses_list.heading(col, text=col.capitalize(), anchor=tk.W)
expenses_list.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

view_expenses()  # Initial load of expenses
root.mainloop()
