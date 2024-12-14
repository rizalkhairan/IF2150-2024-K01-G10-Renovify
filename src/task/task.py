import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from customtkinter import *  # noqa: F403
from PIL import Image
import src.database.database as db
from tkcalendar import DateEntry
from tkinter import ttk
from datetime import datetime

IMG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'img'))

# def get_combobox_style(task):
#     if task.status == 0:  # "Not Started"
#         return 'white'
#     elif task.status == 1:  # "In Progress"
#         return 'yellow'
#     elif task.status == 2:  # "Completed"
#         return 'green'
#     return 'white'

class Task:
    def __init__(self, taskId=None, projectId=None, name='', status=False, start_date=None, completion_date=None, description='', budget=0):
        self.taskId = taskId
        self.projectId = projectId
        self.name = name
        self.status = status
        self.start_date = start_date
        self.completion_date = completion_date
        self.description = description
        self.budget = budget

    def getTaskId(self):
        return self.taskId
    
    def getProjectId(self):
        return self.projectId

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getStatus(self):
        return self.status

    def getStartDate(self):
        return self.start_date

    def getCompletionDate(self):
        return self.completion_date

    def getBudget(self):
        return self.budget

    def setId(self, newId):
        self.taskId = newId
    
    def setProjectId(self, newId):
        self.projectId = newId

    def setName(self, newName):
        self.name = newName

    def setDescription(self, newDesc):
        self.description = newDesc

    def setStatus(self, new_status):
        self.status = new_status

    def toggleStatus(self, new_status=None):
        if new_status is not None:
            self.status = new_status
        else:
            self.status = (self.status + 1) % 3 

    def setStartDate(self, start):
        self.start_date = start

    def setDeadline(self, complete):
        self.completion_date = complete

    def setBudget(self, newBudget):
        self.budget = newBudget

class TaskController:
    def __init__(self):
        self.db = db.DBConnection()

    def getAllTasks(self):
        task_list = []
        result = self.db.getAllTasksOfProject() 
        for row in result:
            task = Task()  
            task.setTaskId(row[0]) 
            task.setName(row[1]) 
            task.setDescription(row[2]) 
            task.setStartDate(row[3])  
            task.setDeadline(row[4]) 
            task.setCompletionDate(row[5])  
            task.setStatus(row[6])  
            task.setBudget(row[7])  # 
            
            
            tags = self.db.getAllTagsForTask(task.getTaskId())  
            task.setTags(tags)
            
            task_list.append(task)
        
        return task_list

    def saveTask(self, task_list: list[Task], task: Task):
        project_id = task.getProjectId()
        name = task.getName()
        description = task.getDescription()
        status = task.getStatus()
        start_date = task.getStartDate()
        completion_date = task.getCompletionDate()
        budget = task.getBudget()

        if task not in task_list:
            if len(task_list) == 0:
                task.taskId = 1 
            else:
                task.taskId = max(task_list, key=lambda task: task.taskId).taskId + 1
            task_list.append(task)
            self.db.createTask(project_id, name, description, status, start_date, completion_date, budget)
        else:
            index = task_list.index(task)
            task_list[index] = task
            self.db.editTask(project_id, name, description, status, start_date, completion_date, budget, task.taskId)

    def deleteTask(self, task_list: list[Task], task: Task):
        index = task_list.index(task)
        del task_list[index]
        self.db.deleteTask(task.getTaskId())

class TaskForm():
    def __init__(self, master: CTk, controller: TaskController):
        self.master = master
        self.controller = controller
        self.entries = {}

    def validateInput(self):
        start_date_str = self.entries["start_date"].get().strip()
        end_date_str = self.entries["end_date"].get().strip()

        # print(f"Start Date: {start_date_str}")
        # print(f"End Date: {end_date_str}")

        if not start_date_str:
            return "Start date is required."
        if not end_date_str:
            return "End date is required."

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            if end_date < start_date:
                return "End date cannot be earlier than start date."
            
            # print(f"Start Date (datetime): {start_date}")
            # print(f"End Date (datetime): {end_date}")

        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

        if not self.entries["name"].get().strip():
            return "Task name is required."
        if not self.entries["budget"].get().replace('.', '').isdigit():
            return "Budget must be a valid number."

        return None

    def createTaskForm(self, task_list: list[Task], task: Task):
        fields = ["Name", "Description", "Start Date", "End Date", "Budget"]
        header = "Create New Task" if not task.taskId else "Edit Task"

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

            if field in ["Start Date", "End Date"]:
                entry = DateEntry(form_frame,
                                  date_pattern="yyyy-mm-dd",
                                  background="white",
                                  disabledbackground="grey",
                                  bordercolor="grey",
                                  headersbackground="lightblue",
                                  headersforeground="black",
                                  weekendbackground="lightgray",
                                  weekendforeground="red",
                                  font=("Arial", 12))
                entry.grid(row=i + 2, column=1, padx=10, pady=5)
            else:
                if field == "Description":
                    entry = CTkTextbox(form_frame, width=200, height=100)
                    entry.grid(row=i + 2, column=1, padx=10, pady=5)
                    entry.insert("1.0", getattr(task, key, ""))
                else:
                    entry = CTkEntry(form_frame, width=200, border_width=0)
                    entry.grid(row=i + 2, column=1, padx=10, pady=5)
                    entry.insert(0, getattr(task, key, ""))

            self.entries[key] = entry

        button_submit = CTkButton(form_frame, text="Submit", command=lambda: self.inputTaskForm(task_list, task))
        button_submit.grid(row=i + 3, pady=10, columnspan=2)


    def inputTaskForm(self, task_list: list[Task], task: Task):
        error = self.validateInput()
        if error:
            error_window = CTkToplevel(self.master)
            error_window.grab_set()
            label = CTkLabel(error_window, text=error)
            label.grid(padx=10, pady=5, sticky="w")
            button_submit = CTkButton(error_window, text="OK", command=error_window.destroy)
            button_submit.grid(pady=10)
            return
        
        task.setName(self.entries["name"].get())
        task.setDescription(self.entries["description"].get("1.0", END).strip())
        task.setStartDate(self.entries["start_date"].get())
        task.setDeadline(self.entries["end_date"].get())

        budget_str = self.entries["budget"].get().replace('.', '').strip()
        task.setBudget(int(budget_str))

        self.controller.saveTask(task_list, task)
        self.closeTaskForm()


    def deleteTaskForm(self, task_list: list[Task], task: Task):
        self.modal_window = CTkToplevel(self.master)
        self.modal_window.grab_set()
        form_label = CTkLabel(self.modal_window, text="Are you sure you want to delete this project?", anchor=N)
        form_label.grid(row=0, pady=10, padx=10)
        p_title = CTkLabel(self.modal_window, text=task.name, anchor=N, font=("Arial", 15))
        p_title.grid(row=1)

        button_frame = CTkFrame(self.modal_window, fg_color=self.modal_window.cget("fg_color"))
        button_frame.grid()
        button_yes = CTkButton(button_frame, text="Delete", width=40,
                               command=lambda: (self.controller.deleteTask(task_list, task),
                                                self.closeTaskForm()))
        button_yes.grid(row=2, column=1, padx=10)
        button_no = CTkButton(button_frame, text="Cancel", width=40, command=self.closeTaskForm)
        button_no.grid(row=2, column=0, padx=10)

    # def validateInput(self):
    #     if not self.entries["name"].get().strip():
    #         return "Task name is required."
    #     if not self.entries["budget"].get().replace('.', '').isdigit():
    #         return "Budget must be a number."
    #     return None  # No errors

    def closeTaskForm(self):
        self.modal_window.destroy()

class TaskList:
    def __init__(self, master: CTk, form: TaskForm, controller: TaskController):
        self.master = master
        self.form = form
        self.controller = controller

    def showTasks(self):
        # Mendapatkan semua task dari controller
        task_list = self.controller.getAllTasks()  # Memanggil fungsi getAllTasks() dari TaskController

        # Menyimpan daftar task di dalam instance
        self.task_list = task_list
        self.prev_list = task_list.copy()
        
        # Membuat UI dengan daftar task yang sudah didapatkan
        self.frame = CTkFrame(self.master)
        self.frame.place(relx=0.5, rely=0.1, anchor=N)
        self.updateUI()
        self.watchTaskList()

    def watchTaskList(self):
        if self.task_list != self.prev_list:
            self.prev_list = self.task_list.copy()
            self.updateUI()
        self.master.after(500, self.watchTaskList)

    def updateUI(self):
        # Clear existing widgets
        for widget in self.frame.winfo_children():
            widget.destroy()

        if len(self.task_list) == 0:
            no_task_label = CTkLabel(self.frame, text="No Task to show")
            no_task_label.grid(row=0, column=0, padx=10, pady=10)
            idx = 0

        try:
            pencil = CTkImage(light_image=Image.open("../../img/penico.png"), size=(16, 16))
            trash = CTkImage(light_image=Image.open("../../img/trashico.png"), size=(16, 16))
            plus = CTkImage(light_image=Image.open("../../img/plusico.png"), size=(16, 16))
        except Exception as e:
            print(f"Error loading images: {e}")
            pencil, trash, plus = None, None, None

        # Menampilkan daftar tugas dengan dropdown status
        for idx, task in enumerate(self.task_list):
            task_frame = CTkFrame(self.frame)
            task_frame.grid(row=idx, column=0, padx=10, pady=10, sticky="w")

            button_details = CTkButton(
                task_frame,
                text=f"{task.name}",
                anchor=W,
                command=lambda t=task: self.showTaskDetails(t),
                fg_color=self.frame.cget("fg_color")
            )
            button_details.grid(row=0, column=0, sticky="w", padx=10, pady=5)

            # Dropdown untuk memilih status tugas
            status_choices = ["Not Started", "In Progress", "Completed"]
            combobox = ttk.Combobox(task_frame, values=status_choices, state="readonly", width=15)
            combobox.set(status_choices[task.status])  # Menampilkan status awal berdasarkan nilai status task
            combobox.grid(row=0, column=1, padx=10, pady=5)

            # Update status saat memilih dropdown
            combobox.bind("<<ComboboxSelected>>", lambda event, t=task: self.updateTaskStatus(event, t))

            button_edit = CTkButton(
                task_frame,
                text="",
                image=pencil,
                width=5,
                command=lambda t=task: self.edit(self.task_list, t)
            )
            button_edit.grid(row=0, column=2, padx=5, pady=5)

            delete_button = CTkButton(
                task_frame,
                text="",
                image=trash,
                width=5,
                command=lambda t=task: self.delete(self.task_list, t)
            )
            delete_button.grid(row=0, column=3, padx=5, pady=5)

        button_add = CTkButton(
            self.frame,
            text="Add Task",
            image=plus,
            width=100,
            command=lambda: self.create(self.task_list)
        )
        button_add.grid(row=idx + 1, column=0, columnspan=4, pady=10, padx=10)

    def updateTaskStatus(self, event, task: Task):
        # Mendapatkan status yang dipilih dari dropdown
        status_str = event.widget.get()
        status_choices = ["Not Started", "In Progress", "Completed"]
        new_status = status_choices.index(status_str)  # Mendapatkan index untuk status

        # Update status task
        task.setStatus(new_status)
        self.updateUI()  # Menyegarkan tampilan setelah perubahan status

    def showTaskDetails(self, task: Task):
        self.frame.destroy()
        self.frame = CTkFrame(self.master)
        self.frame.place(relx=0.5, rely=0.1, anchor=N)

        button_back = CTkButton(self.frame, text="<", width=50, command=lambda: (self.frame.destroy(),self.showTasks(self.task_list)), font=("", 20))  # noqa
        button_back.place(relx=0.1, rely=0.1)

        details_frame = CTkFrame(self.frame)
        details_frame.place(relx=0.5, rely=0.1)

        title = CTkLabel(details_frame, text=task.name)
        desc = CTkLabel(details_frame, text=task.description)
        start = CTkLabel(details_frame, text=f"Start: {task.start_date}")
        end = CTkLabel(details_frame, text=f"End: {task.deadline}")
        budget = CTkLabel(details_frame, text=f"Budget: {task.budget}")

        title.grid(row=0, column=0, columnspan=2)
        desc.grid(row=1, column=0, columnspan=2)
        start.grid(row=2, column=0, columnspan=1)
        end.grid(row=2, column=1, columnspan=1)
        budget.grid(row=3, column=0, columnspan=2)

    def create(self, task_list: list[Task]):
        task = Task()  
        self.form.createTaskForm(task_list, task)

    def edit(self, task_list: list[Task], task: Task):
        self.form.createTaskForm(task_list, task)
        self.waitForModalToClose()

    def delete(self, task_list: list[Task], task: Task):
        self.form.deleteTaskForm(task_list, task)

    def waitForModalToClose(self):
        if self.form.modal_window is None or not self.form.modal_window.winfo_exists():
            self.updateUI()
        else:
            self.master.after(100, self.waitForModalToClose)

class Utility:
    @staticmethod
    def format_currency(entry: CTkEntry):
        value = entry.get()

        value = value.replace(".", "").strip()

        if value:
            try:
                cursor_position = entry.index(INSERT)
                formatted_value = f"{int(value):,}".replace(",", ".")
                num_commas_before_cursor = (cursor_position - 1) // 3
                num_commas_after_cursor = len(formatted_value
                                              [:cursor_position + num_commas_before_cursor]) - cursor_position
                entry.delete(0, END)
                entry.insert(0, formatted_value)
                entry.icursor(cursor_position + num_commas_after_cursor)
            except ValueError:
                pass

    def format_currency_int(budget: int) -> str:
        formatted = f"{budget:,}".replace(",", ".")
        return "Rp" + formatted

# if __name__ == "__main__":
#     root = CTk()
#     root.title("Task Manager")
#     root.geometry("800x600")  
#     style = ttk.Style(root)
#     style.configure("Custom.DateEntry",
#                     background="white",
#                     foreground="black",
#                     fieldbackground="lightblue",
#                     font=("Arial", 12),
#                     arrowcolor="blue")
    
#     controller = TaskController()
#     form = TaskForm(master=root, controller=controller)
#     task_list = TaskList(master=root, form=form)
#     tasks = []  
#     task_list.showTasks(tasks)
#     root.mainloop()