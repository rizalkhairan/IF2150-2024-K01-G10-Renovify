import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from customtkinter import *
from tkinter import messagebox, ttk
import src.database.database as db
from PIL import Image

# atribut : 
# expenseId : integer
# projectId :  integer
# description :  String
# amount : float
class ShowBudget: #BOUNDARY
    def __init__(self, controller):
        self.controller = controller

    def displayAllProjectsBudget(self):
        # Root Window Setup
        root = CTk()
        root.title("All Projects Budget")
        root.geometry("800x500")

        # Title Label
        CTkLabel(root, text="All Projects Budget", font=("Arial", 24, "bold")).pack(pady=15)

        # Scrollable Table Frame
        table_frame = CTkScrollableFrame(root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header Row
        header_frame = CTkFrame(table_frame)
        header_frame.pack(fill="x", pady=5)
        headers = ["Project Name", "Budget"]
        for i, header in enumerate(headers):
            CTkLabel(header_frame, text=header, font=("Arial", 16, "bold"), width=20, anchor="center").grid(row=0, column=i, padx=5, pady=5)

        # Data Rows
        projects_budget = self.controller.getAllProjectsBudget()
        for row_index, project_data in enumerate(projects_budget, start=1):
            CTkLabel(table_frame, text=project_data['project'], font=("Arial", 14), anchor="w").grid(row=row_index, column=0, padx=5, pady=5, sticky="w")
            CTkLabel(table_frame, text=f"{project_data['budget']}", font=("Arial", 14), anchor="center").grid(row=row_index, column=1, padx=5, pady=5, sticky="w")

        # Run Main Loop
        root.mainloop()


    def displayProjectBudget(self, project_name):
        # Root Window Setup
        root = CTk()
        root.title(f"Budget for {project_name}")
        root.geometry("600x400")

        # Title Label
        CTkLabel(root, text=f"Budget for Project: {project_name}", font=("Arial", 24, "bold")).pack(pady=15)

        # Data
        project_budget = self.controller.getProjectBudget(project_name)

        # Display Project Budget
        CTkLabel(root, text=f"Project Name: {project_budget['project']}", font=("Arial", 16)).pack(pady=10, anchor="w")
        CTkLabel(root, text=f"Total Budget: {project_budget['budget']}", font=("Arial", 16)).pack(pady=10, anchor="w")

        # Run Main Loop
        root.mainloop()


    def displayAllProjectsWithTasksBudget(self):
        # Root Window Setup
        root = CTk()
        root.title("All Projects with Task Budgets")
        root.geometry("1000x600")

        # Title Label
        CTkLabel(root, text="Projects with Task Budgets", font=("Arial", 24, "bold")).pack(pady=15)

        # Scrollable Table Frame
        table_frame = CTkScrollableFrame(root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header Row
        header_frame = CTkFrame(table_frame)
        header_frame.pack(fill="x", pady=5)
        headers = ["Project Name", "Task Name", "Task Budget"]
        for i, header in enumerate(headers):
            CTkLabel(header_frame, text=header, font=("Arial", 16, "bold"), width=30, anchor="center").grid(row=0, column=i, padx=5, pady=5)

        # Data Rows
        projects_with_tasks_budget = self.controller.getProjectsTasksBudget()
        for row_index, project_data in enumerate(projects_with_tasks_budget, start=1):
            CTkLabel(table_frame, text=project_data['project'], font=("Arial", 14), anchor="w").grid(row=row_index, column=0, padx=5, pady=5, sticky="w")
            CTkLabel(table_frame, text=project_data['task'], font=("Arial", 14), anchor="center").grid(row=row_index, column=1, padx=5, pady=5, sticky="w")
            CTkLabel(table_frame, text=f"{project_data['task_budget']}", font=("Arial", 14), anchor="center").grid(row=row_index, column=2, padx=5, pady=5, sticky="w")

        # Run Main Loop
        root.mainloop()

    def getProjectTasksBudget(self):
        result = []
        
        # Iterasi setiap proyek
        for project in self.projects:
            project_name = project["project"]
            tasks = project["tasks"]

            # Iterasi setiap task dalam proyek
            for task in tasks:
                result.append({
                    "project": project_name,
                    "task": task["task"],
                    "task_budget": task["budget"]
                })

        return result
    
class Expense:
    def __init__(self, expenseId=None, projectId=None, description='', amount=0):
        self.expenseId = expenseId #expense ID
        self.projectId = projectId
        self.description = description
        self.amount = amount

    def getProjectId(self):
        return self.projectId        
    def getExpenseId(self):
        return self.expenseId
    def getDescription(self):
        return self.description
    def getAmount(self):
        return self.amount

    def setExpenseId(self, newExpenseId):
        self.expenseId = newExpenseId
    def setDescription(self, newDesc):
        self.description = newDesc
    def setAmount(self, newAmount):
        self.amount = newAmount
 
class ExpenseController:
    def __init__(self):
        self.db = db.DBConnection()

    def saveExpense(self, Expense_list: list[Expense], Expense: Expense):
        expense_id = Expense.getExpenseId()
        description = Expense.getDescription()
        amount = Expense.getAmount()

        if Expense not in Expense_list:
            if len(Expense_list) == 0:
                Expense.ExpenseId = 1 
            else:
                Expense.ExpenseId = max(Expense_list, key=lambda Expense: Expense.ExpenseId).ExpenseId + 1
            Expense_list.append(Expense)
            self.db.createExpense(expense_id, description, amount)
        else:
            index = Expense_list.index(Expense)
            Expense_list[index] = Expense
            self.db.editExpense(expense_id, description, amount, Expense.ExpenseId)

    def deleteExpense(self, Expense_list: list[Expense], Expense: Expense):
        index = Expense_list.index(Expense)
        del Expense_list[index]
        self.db.deleteExpense(Expense.getExpenseId())

class ExpenseForm: #BOUNDARY
    def __init__(self, master: CTk, controller: ExpenseController):
        self.master = master
        self.controller = controller
        self.entries = {}

    def validateInput(self):
        # Check if project exists in the database
        # cur = self.controller.execute("SELECT * FROM projects WHERE name=?", (project_name,))
        # project = cur.fetchone()
        # if not project:
        #     return (f"Validation Error: Project '{project_name}' does not exist.")
        if not self.entries["description"].get().strip():
            return "Description name is required."
        if not self.entries["amount"].get().replace('.', '').isdigit():
            return "Amount must be a valid number."

        return None


    def createExpenseForm(self, expense_list: list[Expense], expense: Expense):
        fields = ["Description", "Amount"]
        header = "Create New Expense" if expense.get("expenseId") is None else "Edit Expense"

        self.modal_window = CTkToplevel(self.master)
        self.modal_window.grab_set()
        self.modal_window.minsize(400, 450)
        form_frame = CTkFrame(self.modal_window)
        form_frame.place(relx=0.5, rely=0.1, anchor=N)
        form_label = CTkLabel(form_frame, text=header, anchor=N, font=("Segoe UI", 16))
        form_label.grid(row=1, columnspan=2, pady=10)

        for i, field in enumerate(fields):
            label = CTkLabel(form_frame, text=field)
            label.grid(row=i + 2, column=0, padx=10, pady=5, sticky="w")

            key = field.lower().replace(" ", "_")

            if field == "Description":
                entry = CTkTextbox(form_frame, width=200, height=100)
                entry.grid(row=i + 2, column=1, padx=10, pady=5)
                entry.insert("1.0", getattr(expense, key, ""))
            else:
                entry = CTkEntry(form_frame, width=200, border_width=0)
                entry.grid(row=i + 2, column=1, padx=10, pady=5)
                entry.insert(0, getattr(expense, key, ""))

            self.entries[key] = entry

        button_submit = CTkButton(form_frame, text="Submit", command=lambda: self.inputExpenseForm(expense_list, expense))
        button_submit.grid(row=i + 3, pady=10, columnspan=2)

    def inputExpenseForm(self, expense_list: list[Expense], expense: Expense):
        error = self.validateInput()
        if error:
            error_window = CTkToplevel(self.master)
            error_window.grab_set()
            label = CTkLabel(error_window, text=error)
            label.grid(padx=10, pady=5, sticky="w")
            button_submit = CTkButton(error_window, text="OK", command=error_window.destroy)
            button_submit.grid(pady=10)
            return
        
        # expense.setExpenseId(self.entries["expense_id"].get())
        expense.setDescription(self.entries["description"].get("1.0", END).strip())
        amount_str = self.entries["amount"].get().replace('.', '').strip()
        expense.setAmount(int(amount_str))

        self.controller.saveExpense(expense_list, expense)
        self.closeExpenseForm()

    def deleteExpenseForm(self, expense_list: list[Expense], expense: Expense):
        self.modal_window = CTkToplevel(self.master)
        self.modal_window.grab_set()
        form_label = CTkLabel(self.modal_window, text="Are you sure you want to delete this project?", anchor=N)
        form_label.grid(row=0, pady=10, padx=10)
        p_title = CTkLabel(self.modal_window, text="Expense", anchor=N, font=("Arial", 15))
        p_title.grid(row=1)

        button_frame = CTkFrame(self.modal_window, fg_color=self.modal_window.cget("fg_color"))
        button_frame.grid()
        button_yes = CTkButton(button_frame, text="Delete", width=40,
                               command=lambda: (self.controller.deleteExpense(expense_list, expense),
                                                self.closeExpenseForm()))
        button_yes.grid(row=2, column=1, padx=10)
        button_no = CTkButton(button_frame, text="Cancel", width=40, command=self.closeExpenseForm)
        button_no.grid(row=2, column=0, padx=10)

    # def validateInput(self):
    #     if not self.entries["name"].get().strip():
    #         return "Expense name is required."
    #     if not self.entries["budget"].get().replace('.', '').isdigit():
    #         return "Budget must be a number."
    #     return None  # No errors

    def closeExpenseForm(self):
        self.modal_window.destroy()

class ExpenseList: #BOUNDARY
    def __init__(self, master: CTk, form: ExpenseForm):
        self.master = master
        self.form = form

    def showExpenses(self, p_list: list[Expense]):
        self.expense_list = p_list
        self.prev_list = p_list.copy()
        self.frame = CTkFrame(self.master)
        self.frame.place(relx=0.5, rely=0.1, anchor=N)
        self.updateUI()
        self.watchExpenseList()

    def watchExpenseList(self):
        if self.expense_list != self.prev_list:
            self.prev_list = self.expense_list.copy()
            self.updateUI()
        self.master.after(500, self.watchExpenseList)

    def updateUI(self):
        # Clear existing widgets
        for widget in self.frame.winfo_children():
            widget.destroy()

        if len(self.expense_list) == 0:
            no_expense_label = CTkLabel(self.frame, text="No Expense to show")
            no_expense_label.grid(row=0, column=0, padx=10, pady=10)
            idx = 0

        try:
            pencil = CTkImage(light_image=Image.open("../../img/penico.png"), size=(16, 16))
            trash = CTkImage(light_image=Image.open("../../img/trashico.png"), size=(16, 16))
            plus = CTkImage(light_image=Image.open("../../img/plusico.png"), size=(16, 16))
        except Exception as e:
            print(f"Error loading images: {e}")
            pencil, trash, plus = None, None, None

        # Menampilkan daftar expense dengan dropdown status
        for idx, expense in enumerate(self.expense_list):
            expense_frame = CTkFrame(self.frame)
            expense_frame.grid(row=idx, column=0, padx=10, pady=10, sticky="w")

            button_details = CTkButton(
                expense_frame,
                text=f"{expense.name}",
                anchor=W,
                command=lambda e=expense: self.showExpenseDetails(e),
                fg_color=self.frame.cget("fg_color")
            )
            button_details.grid(row=0, column=0, sticky="w", padx=10, pady=5)

            button_edit = CTkButton(
                expense_frame,
                text="",
                image=pencil,
                width=5,
                command=lambda t=expense: self.edit(self.expense_list, t)
            )
            button_edit.grid(row=0, column=2, padx=5, pady=5)

            delete_button = CTkButton(
                expense_frame,
                text="",
                image=trash,
                width=5,
                command=lambda t=expense: self.delete(self.expense_list, t)
            )
            delete_button.grid(row=0, column=3, padx=5, pady=5)

        button_add = CTkButton(
            self.frame,
            text="Add Expense",
            image=plus,
            width=100,
            command=lambda: self.create(self.expense_list)
        )
        button_add.grid(row=idx + 1, column=0, columnspan=4, pady=10, padx=10)

    def showExpenseDetails(self, expense: Expense):
        self.frame.destroy()
        self.frame = CTkFrame(self.master)
        self.frame.place(relx=0.5, rely=0.1, anchor=N)

        button_back = CTkButton(self.frame, text="<", width=50, command=lambda: (self.frame.destroy(),self.showExpenses(self.expense_list)), font=("", 20))  # noqa
        button_back.place(relx=0.1, rely=0.1)

        details_frame = CTkFrame(self.frame)
        details_frame.place(relx=0.5, rely=0.1)

        # title_text = expense.getProjectId
        title = CTkLabel(details_frame, text="expense.name")
        desc = CTkLabel(details_frame, text=expense.description)
        amount = CTkLabel(details_frame, text=f"Amount: {expense.amount}")

        title.grid(row=0, column=0, columnspan=2)
        desc.grid(row=1, column=0, columnspan=2)
        amount.grid(row=3, column=0, columnspan=2)

    def create(self, expense_list: list[Expense]):
        expense = expense()  
        self.form.createExpenseForm(expense_list, expense)

    def edit(self, expense_list: list[Expense], expense: Expense):
        self.form.createExpenseForm(expense_list, expense)
        self.waitForModalToClose()

    def delete(self, expense_list: list[Expense], expense: Expense):
        self.form.deleteExpenseForm(expense_list, expense)

    def waitForModalToClose(self):
        if self.form.modal_window is None or not self.form.modal_window.winfo_exists():
            self.updateUI()
        else:
            self.master.after(100, self.waitForModalToClose)

    # def showExpenses(self):
    #     root = CTk()
    #     root.title("Expenses")
    #     root.geometry("500x400")

    #     CTkLabel(root, text="Project Expenses", font=("Arial", 20)).pack(pady=10)

    #     frame = CTkScrollableFrame(root)
    #     frame.pack(fill="both", expand=True, padx=10, pady=10)

    #     expenses = self.controller.getAllExpenses()
    #     for expense in expenses:
    #         CTkLabel(frame, text=f"{expense['description']} - {expense['amount']}").pack(anchor="w", pady=2)

    #     root.mainloop()

    # def create(self, project_name, description, amount):
    #     # Use ExpenseForm for input and validation
    #     form = ExpenseForm(self.controller)
    #     form.saveExpense(self, project_name, description, amount)

    # def edit(self, expense_id, new_description, new_amount):
    #     cur = self.controller.execute("UPDATE expenses SET description=?, amount=? WHERE expense_id=?", 
    #                             (new_description, new_amount, expense_id))
    #     self.controller.commit()
    #     print(f"Expense ID {expense_id} has been updated.")

    # def delete(self, expense_id):
    #     cur = self.controller.execute("DELETE FROM expenses WHERE expense_id=?", (expense_id,))
    #     self.con.commit()
    #     print(f"Expense ID {expense_id} has been deleted.")


class DisplayCompareExpense:
    def __init__(self, controller):
        self.controller = controller

    def displayExpenseComparison(self):
        # Root Window Setup
        root = CTk()
        root.title("Expense Comparison")
        root.geometry("800x500")

        # Title Label
        CTkLabel(root, text="Expense vs Budget Comparison", font=("Arial", 24, "bold")).pack(pady=15)

        # Scrollable Table Frame
        table_frame = CTkScrollableFrame(root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header Row
        header_frame = CTkFrame(table_frame)
        header_frame.pack(fill="x", pady=5)
        headers = ["Project", "Budget", "Expense", "Difference"]
        for i, header in enumerate(headers):
            CTkLabel(header_frame, text=header, font=("Arial", 16, "bold"), width=20, anchor="center").grid(row=0, column=i, padx=5, pady=5)

        # Data Rows
        comparison_data = self.controller.calculateComparison()
        for row_index, project_data in enumerate(comparison_data, start=1):
            project = project_data['project']
            budget = project_data['budget']
            expenses = project_data['expenses']
            difference = project_data['difference']

            # Determine Difference Display and Color
            if difference >= 0:
                diff_text = f"+{difference}"  # Add positive sign
                diff_color = "green"
            else:
                diff_text = f"{difference}"  # Negative values already have "-"
                diff_color = "red"

            # Display data in columns
            CTkLabel(table_frame, text=project, font=("Arial", 14), anchor="w").grid(row=row_index, column=0, padx=5, pady=5, sticky="w")
            CTkLabel(table_frame, text=f"{budget}", font=("Arial", 14), anchor="center").grid(row=row_index, column=1, padx=5, pady=5, sticky="w")
            CTkLabel(table_frame, text=f"{expenses}", font=("Arial", 14), anchor="center").grid(row=row_index, column=2, padx=5, pady=5, sticky="w")
            CTkLabel(table_frame, text=diff_text, font=("Arial", 14), fg_color=None, text_color=diff_color, anchor="center").grid(row=row_index, column=3, padx=5, pady=5, sticky="w")

        # Run Main Loop
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
    def __init__(self):
        self.db = db.DBConnection()

    def calculateComparison(self):
        # Ambil semua proyek dari database
        cur = self.db.execute("SELECT project_id, name, budget FROM projects")
        projects = cur.fetchall()
        cur.close()

        comparison_data = []

        for project in projects:
            project_id = project[0]
            project_name = project[1]
            budget = project[2]

            # Hitung total pengeluaran untuk proyek ini
            cur = self.db.execute("SELECT SUM(amount) FROM expenses WHERE project_id = ?", (project_id,))
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

# class ExampleController:
#     def getAllProjectsWithTasksBudget(self):
#         return {
#             "Project A": {"Task 1": 500, "Task 2": 300},
#             "Project B": {"Task 3": 700, "Task 4": 200},
#         }

#     def validateInput(self, project_name, description, amount):
#         return bool(project_name and description and amount.isdigit())

#     def createExpense(self, project_name, description, amount):
#         print(f"Expense created for {project_name}: {description} - {amount}")

#     def getAllExpenses(self):
#         return [
#             {"description": "Purchase Materials", "amount": 100},
#             {"description": "Worker Payment", "amount": 200},
#         ]

#     def calculateComparison(self):
#         return [
#             {"project": "Project A", "budget": 1000, "expenses": 700, "difference": 300},
#             {"project": "Project B", "budget": 500, "expenses": 600, "difference": -100},
#         ]


if __name__ == "__main__":
    set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

    # Uncomment to test each boundary class
    # ShowBudget(controller).displayAllProjectsWithTasksBudget()
    # ExpenseForm(master, controller).createExpenseForm()
    # ExpenseList(controller).showExpenses()
    # DisplayCompareExpense(controller).displayExpenseComparison()

    root = CTk()
    controller = ExpenseController()

    expense1 = {"projectId": 1, "expenseId": 1, "description": "aa", "amount": 200}
    expense2 = {"projectId": 2, "expenseId": 2, "description": "bb", "amount": 300}
    expense3 = {"projectId": 3, "expenseId": 3, "description": "cc", "amount": 400}
    expense_list = [expense1, expense2, expense3]

    form = ExpenseForm(root, controller)  
    form.createExpenseForm(expense_list, expense1)

    root.mainloop()