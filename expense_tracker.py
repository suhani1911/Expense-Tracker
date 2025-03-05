import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("800x500+20+20")
        self.expenses = []  
        self.loadExpenses()

        # Heading
        heading = tk.Label(root, text="Personal Expense Tracker", font=("Arial", 24, "bold"), fg="#333")
        heading.pack(pady=10)

        # buttons
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack( fill=tk.Y, padx=20, pady=10)
        btn_add_expense = tk.Button(button_frame, text="Add Expense", font=("Arial", 14), command=self.openAddExpenseWindow)
        btn_add_expense.pack(pady=10)

        btn_view_expenses = tk.Button(button_frame, text="View Expenses", font=("Arial", 14), command=self.openViewExpensesWindow)
        btn_view_expenses.pack(pady=10)

        btn_track_budget = tk.Button(button_frame, text="Track Budget", font=("Arial", 14), command=self.openBudgetTrackingWindow)
        btn_track_budget.pack(pady=10)

        btn_save_expenses = tk.Button(button_frame, text="Save Expenses", font=("Arial", 14), command=self.saveExpenses)
        btn_save_expenses.pack(pady=10)

        btn_exit = tk.Button(button_frame, text="Exit", font=("Arial", 14), command=self.root.quit)
        btn_exit.pack(pady=10)

    def openAddExpenseWindow(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Expense")
        add_window.geometry("800x500+20+20")

        tk.Label(add_window, text="Add Expense", font=("Arial", 18, "bold"), fg="#333").pack(pady=10)

        tk.Label(add_window, text="Date (YYYY-MM-DD):", font=("Arial", 12)).pack(pady=5)#date input
        date_entry = tk.Entry(add_window, font=("Arial", 12))
        date_entry.pack(pady=5)

        tk.Label(add_window, text="Category (e.g., Food, Travel):", font=("Arial", 12)).pack(pady=5)#category input
        category_entry = tk.Entry(add_window, font=("Arial", 12))
        category_entry.pack(pady=5)

        tk.Label(add_window, text="Amount Spent:", font=("Arial", 12)).pack(pady=5)#amount input
        amount_entry = tk.Entry(add_window, font=("Arial", 12))
        amount_entry.pack(pady=5)

        tk.Label(add_window, text="Description:", font=("Arial", 12)).pack(pady=5)#description input
        description_entry = tk.Entry(add_window, font=("Arial", 12))
        description_entry.pack(pady=5)

        def submit_expense():
            try:
                date = date_entry.get().strip()
                category = category_entry.get().strip()
                amount = float(amount_entry.get().strip())
                description = description_entry.get().strip()

                if not date or not category or not description:
                    raise ValueError("Fields cannot be empty.")
                datetime.strptime(date, "%Y-%m-%d")

                expense = {
                    'date': date,
                    'category': category,
                    'amount': amount,
                    'description': description
                }
                self.expenses.append(expense)
                messagebox.showinfo("Success", "Expense added successfully!")
                add_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        submit_btn = tk.Button(add_window, text="Add Expense", font=("Arial", 14), bg="#5cb85c", fg="white", command=submit_expense)
        submit_btn.pack(pady=20)

    def openViewExpensesWindow(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Expenses")
        view_window.geometry("800x500+20+20")

        get_date = tk.StringVar()
        get_category = tk.StringVar()

        tk.Label(view_window, text="View Expenses", font=("Arial", 18, "bold"), fg="#333").pack(pady=10)

        btn_all = tk.Button(view_window, text="All Expenses", font=("Arial", 12), command=lambda: self.viewExpensesAll(view_window))
        btn_all.pack(pady=5)

        btn_date = tk.Button(view_window, text="Expenses by Date", font=("Arial", 12), command=lambda: self.viewExpensesDate(view_window, get_date.get()))
        btn_date.pack(pady=5)

        get_date_entry = tk.Entry(view_window, textvariable=get_date, font=("goudy old style", 15), bg="lightyellow")
        get_date_entry.pack(pady=5)

        btn_category = tk.Button(view_window, text="Expenses by Category", font=("Arial", 12), command=lambda: self.viewExpensesCategory(view_window, get_category.get()))
        btn_category.pack(pady=5)

        get_category_entry = tk.Entry(view_window, textvariable=get_category, font=("goudy old style", 15), bg="lightyellow")
        get_category_entry.pack(pady=5)

        self.expense_output = tk.Text(view_window, height=250, width=80)
        self.expense_output.place(x=0, y=300, height=250, width=800)

    def viewExpensesAll(self, view_window):
        if not self.expenses:
            messagebox.showinfo("No Data", "No expenses recorded yet.")
            return
        all_expenses = "\n".join([f"Date: {e['date']}, Category: {e['category']}, Amount: {e['amount']}, Description: {e['description']}" for e in self.expenses])
        self.displayExpenses(view_window, all_expenses)

    def viewExpensesDate(self, view_window, date):
        if not date:
            messagebox.showinfo("Invalid Input", "Please enter a date.")
            return
        date_expenses = [e for e in self.expenses if e['date'] == date]
        if not date_expenses:
            messagebox.showinfo("No Data", f"No expenses found for {date}.")
            return
        all_expenses = "\n".join([f"Date: {e['date']}, Category: {e['category']}, Amount: {e['amount']}, Description: {e['description']}" for e in self.expenses])
        self.displayExpenses(view_window, all_expenses)

    def viewExpensesCategory(self, view_window, category):
        if not category:
            messagebox.showinfo("Invalid Input", "Please enter a category.")
            return
        category_expenses = [e for e in self.expenses if e['category'] == category]
        if not category_expenses:
            messagebox.showinfo("No Data", f"No expenses found for category {category}.")
            return
        all_expenses = "\n".join([f"Date: {e['date']}, Category: {e['category']}, Amount: {e['amount']}, Description: {e['description']}" for e in self.expenses])
        self.displayExpenses(view_window, all_expenses)

    def displayExpenses(self, view_window, expenses_str):
        self.expense_output.delete(1.0, tk.END)  
        self.expense_output.insert(tk.END, expenses_str)
        

    def openBudgetTrackingWindow(self):
        budget_window = tk.Toplevel(self.root)
        budget_window.title("Budget Tracking")
        budget_window.geometry("800x500+20+20")
        get_budget=tk.DoubleVar()

        tk.Label(budget_window, text="Enter Your Monthly Budget", font=("Arial", 14)).pack(pady=20)

        budget_entry = tk.Entry(budget_window,textvariable=get_budget, font=("goudy old style", 15), bg="lightyellow")
        budget_entry.pack(pady=10)

        check_budget_button = tk.Button(budget_window, text="Check Budget", font=("Arial", 12), command=lambda: self.trackBudget(budget_window,get_budget.get()))
        check_budget_button.pack(pady=10)

    def trackBudget(self,budget_window,budget):
        try:
            monthly_budget = budget
            if monthly_budget <= 0:
                messagebox.showerror("Error", "Please enter a valid positive budget.")
                return

            total = sum(expense['amount'] for expense in self.expenses)
            if total > monthly_budget:
                messagebox.showwarning("Budget Exceeded", "You have exceeded your budget!")
                budget_window.destroy()
            else:
                remaining = monthly_budget - total
                messagebox.showinfo("Budget Status", f"You have {remaining} left for the month.")
                budget_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Invalid budget input. Please enter a valid number.")

    def saveExpenses(self):
        filename = "expenses.csv"
        try:
            df = pd.DataFrame(self.expenses)
            df.to_csv(filename, index=False)
            messagebox.showinfo("Success", f"Expenses saved to {filename} successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def loadExpenses(self):
        filename = "expenses.csv"
        try:
            df = pd.read_csv(filename)
            for _, row in df.iterrows():
                expense = {
                    'date': row['date'],
                    'category': row['category'],
                    'amount': float(row['amount']),
                    'description': row['description']
                }
                self.expenses.append(expense)
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading expenses: {e}")

    

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()





# -------------cmd working-----------------
# import pandas as pd
# from datetime import datetime

# #Add expense to expense tracker
# def addExpense(expenses):
#     while True:
#         try:
#             date = input("Enter the date (YYYY-MM-DD): ").strip()
#             if not date:
#                 print("Date cannot be empty. Please try again.")
#                 continue
#             datetime.strptime(date, "%Y-%m-%d")  
            
#             category = input("Enter the category (e.g., Food, Travel): ").strip()
#             if not category:
#                 print("Category cannot be empty. Please try again.")
#                 continue

#             amount_input = input("Enter the amount spent: ").strip()
#             if not amount_input:
#                 print("Amount cannot be empty. Please try again.")
#                 continue
#             amount = float(amount_input)
#             if amount <= 0:
#                 print("Amount must be greater than 0. Please try again.")
#                 continue
#             description = input("Enter a brief description: ").strip()
#             if not description:
#                 print("Description cannot be empty. Please try again.")
#                 continue

#             expense = {
#                 'date': date,
#                 'category': category,
#                 'amount': amount,
#                 'description': description
#             }
#             expenses.append(expense)
#             print("Expense added successfully!\n")
#             break  # Exit the loop once a valid expense is added
#         except ValueError:
#             print("Invalid input. Please enter the correct values.\n")

# #View  expense from expense tracker
# def viewExpenses(expenses):
#     if not expenses:
#         print("No expenses recorded yet.\n")
#         return
#     else:
#         print("----------View Menu----------")
#         print("1.All Expenses")
#         print("2.Expenses made on specific date")
#         print("3.Expenses made for specific category")
#         num=int(input("Enter your choice:"))
#         if num==1:
#             viewExpensesAll(expenses)
#         elif num==2:
#             viewExpensesDate(expenses)
#         elif num==3:
#             viewExpensesCategory(expenses)
#         else:
#             print("Invalid choice,try again.")

# def viewExpensesAll(expenses):
#     print("\nYour Expenses:")
#     print(f"{'Date':<15}{'Category':<15}{'Amount':<10}{'Description':<30}")
#     print("-" * 70)
#     for expense in expenses:
#         # No need to check for missing keys because addExpense ensures completeness
#         print(f"{expense['date']:<15}{expense['category']:<15}{expense['amount']:<10}{expense['description']:<30}")
#     print("-" * 70)

# def viewExpensesDate(expenses):
#     date= input("Enter the date (YYYY-MM-DD): ").strip()
#     date_expenses = [ex for ex in expenses if ex['date'] ==date]

#     if not date_expenses:
#         print(f"No expenses found for the date {date}.\n")
#         return

#     print(f"\nExpenses for {date}:")
#     print(f"{'Category':<15}{'Amount':<10}{'Description':<30}")
#     print("-" * 70)
#     for expense in date_expenses:
#         print(f"{expense['category']:<15}{expense['amount']:<10}{expense['description']:<30}")
#     print("-" * 70)

# def viewExpensesCategory(expenses):
#     category=input("Enter the category(Food,Travel): ").strip()
#     category_expenses = [ex for ex in expenses if ex['category'] ==category]

#     if not category_expenses:
#         print(f"No expenses found for category {category}.\n")
#         return

#     print(f"\nExpenses for {category}:")
#     print(f"{'Category':<15}{'Amount':<10}{'Description':<30}")
#     print("-" * 70)
#     for expense in category_expenses:
#         print(f"{expense['category']:<15}{expense['amount']:<10}{expense['description']:<30}")
#     print("-" * 70)



# # Function to set and track the budget
# def trackBudget(expenses):
#     try:
#         monthly_budget = float(input("Enter your monthly budget: "))
#         total_expenses = sum(expense['amount'] for expense in expenses)

#         print(f"Total Expenses: {total_expenses}")
#         if total_expenses > monthly_budget:
#             print("You have exceeded your budget!\n")
#         else:
#             remaining = monthly_budget - total_expenses
#             print(f"You have {remaining} left for the month.\n")
#     except ValueError:
#         print("Invalid input. Please try again.\n")

# # Function to save expenses to a CSV file
# def saveExpenses(expenses):
#     filename = "expenses.csv"
#     try:
#         df = pd.DataFrame(expenses)
#         df.to_csv(filename, index=False)
#         print(f"Expenses saved to {filename} successfully!\n")
#     except Exception as e:
#         print(f"An error occurred while saving expenses: {e}\n")

# # Function to load expenses from a CSV file using pandas
# def loadExpenses(expenses):
#     filename = "expenses.csv"
#     try:
#         df = pd.read_csv(filename)
#         for _, row in df.iterrows():
#             expense = {
#                 'date': row['date'],
#                 'category': row['category'],
#                 'amount': float(row['amount']),  # Ensure amount is converted to float
#                 'description': row['description']
#             }
#             expenses.append(expense)
#         print(f"Expenses loaded from {filename} successfully!\n")
#     except FileNotFoundError:
#         print(f"No previous data found in {filename}. Starting fresh.\n")
#     except Exception as e:
#         print(f"An error occurred while loading expenses: {e}\n")

# # Function to display the interactive menu
# def display_menu():
#     expenses=[]#store the expenses
#     loadExpenses(expenses)
#     while True:
#         print("\n----------Expense Tracker----------")
#         print("1. Add Expense")
#         print("2. View Expenses")
#         print("3. Track budget")
#         print("4. Save Expenses")
#         print("5. Exit")

#         choice = input("Enter your choice: ")

#         if choice == '1':
#             addExpense(expenses)
#         elif choice == '2':
#             viewExpenses(expenses)
#         elif choice == '3':
#             trackBudget(expenses)
#         elif choice == '4':
#             saveExpenses(expenses)
#         elif choice == '5':
#             saveExpenses(expenses)
#             print("Exiting the program.")
#             break
#         else:
#             print("Invalid choice. Please select a valid option.\n")

# display_menu()


