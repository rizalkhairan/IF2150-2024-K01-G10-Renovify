import tkinter as tk
from tkinter import ttk, messagebox
from project import *

# atribut : 
# expenseId : integer
# projectId :  integer
# description :  String
# amount : float
class Expense:
    def __init__(self) -> None:
        self.expenseid: int = None #expense ID
        self.projectid: int = None #project ID from project brader
        self.description: str = ""
        self.amount: int = 0

    def getExpenseId(self):
        return self.expenseid
    def getDescription(self):
        return self.description
    def getAmount(self):
        return self.amount

    def setExpenseId(self, newExpenseId):
        self.expenseid = newExpenseId
    def setDescription(self, newDesc):
        self.description = newDesc
    def setAmount(self, newAmount):
        self.amount = newAmount


class ShowBudget: #BOUNDARY
    def __init__(self, con):
        self.con = con

    def displayAllProjectsBudget(self):
        cur = self.con.execute("""
            SELECT 
                project_id, 
                name AS project_name, 
                budget 
            FROM projects
        """)
        result = cur.fetchall()
        cur.close()

        # Format dan kembalikan hasil
        all_projects_budget = []
        for row in result:
            all_projects_budget.append({
                "project_id": row[0],
                "project_name": row[1],
                "budget": row[2]
            })
        return all_projects_budget

    def displayProjectBudget(self, project_id):
        cur = self.con.execute("""
            SELECT 
                project_id, 
                name AS project_name, 
                budget 
            FROM projects
            WHERE project_id = ?
        """, (project_id,))
        result = cur.fetchone()
        cur.close()

        # Jika proyek tidak ditemukan
        if not result:
            return {"error": "Project not found"}

        # Format dan kembalikan hasil
        project_budget = {
            "project_id": result[0],
            "project_name": result[1],
            "budget": result[2]
        }
        return project_budget
        
    def displayAllProjectsWithTasksBudget(self):
        root = tk.Tk()
        root.title("All Projects and Tasks Budget")

        tk.Label(root, text="Project Budgets", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(root, columns=("Task", "Budget"), show="headings")
        tree.heading("Task", text="Task")
        tree.heading("Budget", text="Budget")
        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        data = self.controller.getAllProjectsWithTasksBudget()
        for project, tasks in data.items():
            tree.insert("", "end", values=(f"{project} (Project)", "---"))
            for task, budget in tasks.items():
                tree.insert("", "end", values=(f"  {task}", budget))

        root.mainloop()

    def getProjectTasksBudget(self, project_id):
            query = """
                SELECT SUM(budget) as total_task_budget
                FROM tasks
                WHERE project_id = ?;
            """
            cur = self.con.execute(query, (project_id,))
            result = cur.fetchone()
            cur.close()

            return result['total_task_budget'] if result['total_task_budget'] else 0

class ExpenseForm: #BOUNDARY
    def __init__(self, db_connection):
        self.con = db_connection  # Connection to the database

    def createExpenseForm(self):
        self.root = tk.Tk()
        self.root.title("Create Expense")

        tk.Label(self.root, text="Create Expense", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Project Name:").pack(anchor="w", padx=10)
        self.project_entry = tk.Entry(self.root)
        self.project_entry.pack(padx=10, pady=5)

        tk.Label(self.root, text="Expense Description:").pack(anchor="w", padx=10)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.pack(padx=10, pady=5)

        tk.Label(self.root, text="Expense Amount:").pack(anchor="w", padx=10)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(padx=10, pady=5)

        tk.Button(self.root, text="Submit", command=self.submit_expense).pack(pady=10)

        self.root.mainloop()
    def inputExpenseForm(self):
        project_name = input("Enter project name: ")
        description = input("Enter expense description: ")
        try:
            amount = float(input("Enter expense amount: "))
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            return

        if self.__validateInput(project_name, description, amount):
            # Save expense to the database
            self.__saveExpense(project_name, description, amount)
        else:
            print("Failed to validate input. Please try again.")

    def __showExpenseForm(self):
        print("Please fill in the details below:")

    def __validateInput(self, project_name, description, amount):
        if not project_name or not description or amount <= 0:
            print("Validation Error: All fields are required and amount must be positive.")
            return False

        # Check if project exists in the database
        cur = self.con.execute("SELECT * FROM projects WHERE name=?", (project_name,))
        project = cur.fetchone()
        if not project:
            print(f"Validation Error: Project '{project_name}' does not exist.")
            return False

        return True
    
    def __saveExpense(self, project_name, description, amount):
        # Get project_id based on project_name
        cur = self.con.execute("SELECT project_id FROM projects WHERE name=?", (project_name,))
        project_id = cur.fetchone()[0]

        # Insert expense into the database
        self.con.execute(
            "INSERT INTO expenses (project_id, description, amount) VALUES (?, ?, ?)",
            (project_id, description, amount)
        )
        self.con.commit()
        print("Expense has been successfully added.")

class ExpenseList: #BOUNDARY
    def __init__(self, db_connection):
        self.con = db_connection  # Connection to the database

    def showExpenses(self):
        root = tk.Tk()
        root.title("Expenses")

        tk.Label(root, text="Project Expenses", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(root, columns=("Description", "Amount"), show="headings")
        tree.heading("Description", text="Description")
        tree.heading("Amount", text="Amount")
        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        expenses = self.controller.getAllExpenses()
        for expense in expenses:
            tree.insert("", "end", values=(expense["description"], expense["amount"]))

        root.mainloop()

    def create(self, project_name, description, amount):
        # Use ExpenseForm for input and validation
        form = ExpenseForm(self.con)
        form.__saveExpense(project_name, description, amount)

    def edit(self, expense_id, new_description, new_amount):
        cur = self.con.execute("UPDATE expenses SET description=?, amount=? WHERE expense_id=?", 
                                (new_description, new_amount, expense_id))
        self.con.commit()
        print(f"Expense ID {expense_id} has been updated.")

    def delete(self, expense_id):
        cur = self.con.execute("DELETE FROM expenses WHERE expense_id=?", (expense_id,))
        self.con.commit()
        print(f"Expense ID {expense_id} has been deleted.")


class DisplayCompareExpense: #BOUNDARY
    def __init__(self, controller):
        self.controller = controller

    def displayExpenseComparison(self):
        root = tk.Tk()
        root.title("Expense Comparison")

        tk.Label(root, text="Expense vs Budget Comparison", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(root, columns=("Project", "Budget", "Expenses", "Difference"), show="headings")
        tree.heading("Project", text="Project")
        tree.heading("Budget", text="Budget")
        tree.heading("Expenses", text="Expenses")
        tree.heading("Difference", text="Difference")
        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        comparison_data = self.controller.calculateComparison()
        for project_data in comparison_data:
            tree.insert(
                "", "end",
                values=(
                    project_data["project"],
                    project_data["budget"],
                    project_data["expenses"],
                    project_data["difference"],
                ),
            )

        root.mainloop()

class CompareExpenseController:
# Q-20-1
# SELECT Expense FROM Project WHERE id = <id>
# Mengambil Expense dari proyek
# Q-20-2
# SELECT Budget FROM Project WHERE id = <id>
# Mengambil Budget dari proyek
# Q-20-3
# SELECT (Budget - Expense) AS Difference FROM Project WHERE id = <specific_project_id>;
# Menghitung perbedaan Expense dan Budget
    def __init__(self, db_connection):
        self.con = db_connection

    def calculateComparison(self):
        # Ambil semua proyek dari database
        cur = self.con.execute("SELECT project_id, name, budget FROM projects")
        projects = cur.fetchall()
        cur.close()

        comparison_data = []

        for project in projects:
            project_id = project[0]
            project_name = project[1]
            budget = project[2]

            # Hitung total pengeluaran untuk proyek ini
            cur = self.con.execute("SELECT SUM(amount) FROM expenses WHERE project_id = ?", (project_id,))
            expense = cur.fetchone()[0]
            cur.close()

            expense = expense if expense else 0  # Jika tidak ada pengeluaran, setel ke 0
            difference = budget - expense

            # Tambahkan hasil ke data perbandingan
            comparison_data.append({
                "project_name": project_name,
                "budget": budget,
                "expense": expense,
                "difference": difference
            })

        return comparison_data


