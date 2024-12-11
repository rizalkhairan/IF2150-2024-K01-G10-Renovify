from customtkinter import *  # noqa: F403
from PIL import Image
import src.database.database as db
# from tkcalendar import Calendar


class Project:
    def __init__(self) -> None:
        self.id: int = None
        self.name: str = ""
        self.description: str = ""
        self.status: bool = False       # done atau belum (true done false blum)
        self.start_date: str = ""
        self.deadline: str = ""
        self.budget: int = 0

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getStatus(self):
        return self.status

    def getStartDate(self):
        return self.start_date

    def getDeadline(self):
        return self.deadline

    def getBudget(self):
        return self.budget

    def setId(self, newId):
        self.id = newId

    def setName(self, newName):
        self.name = newName

    def setDescription(self, newDesc):
        self.description = newDesc

    def toggleStatus(self):
        self.status = not self.status

    def setStartDate(self, start):
        self.start_date = start

    def setDeadline(self, complete):
        self.deadline = complete

    def setBudget(self, newBudget):
        self.budget = newBudget


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PROJECT CONTROLLER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class ProjectController:
    def __init__(self):
        self.db = db.DBConnection()

    def saveProject(self, project_list: list[Project], project: Project):
        name = project.getName()
        description = project.getDescription()
        status = project.getStatus()
        start_date = project.getStartDate()
        completion_date = project.getDeadline()
        budget = project.getBudget()

        if (project not in project_list):  # Create new

            # Cari id tertinggi dan tambah 1
            if (len(project_list) == 0):
                project.id = 1
            else:
                project.id = max(project_list, key=lambda
                                 project: project.id).id, + 1
            index = len(project_list)
            project_list.append(project)

            # def createProject(self, name, description, status, start_date, completion_date, budget):
            self.db.createProject(name, description, status, start_date, completion_date, budget)

        else:
            index = project_list.index(project)
            project_list[index] = project
            self.db.editProject(project.getId(), name, description, status, start_date, completion_date, budget)

    def getAllProjects(self):
        result = self.db.getAllProjects()
        project_list = []
        for row in result:
            project = Project()
            project.id = row[0]
            project.name = row[1]
            project.description = row[2]
            project.status = row[3]
            project.start_date = row[4]
            project.deadline = row[5]
            project.budget = row[6]
            project_list.append(project)

        return project_list

    # def getProject(self, project: Project, filter):
    #     self.db.getProjects(project.getId())

    def deleteProject(self, project_list: list[Project], project: Project):
        index = project_list.index(project)
        del project_list[index]

        self.db.deleteProject(project.getId())


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  PROJECT FORM <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class ProjectForm():
    def __init__(self, master: CTk, controller: ProjectController):
        self.master = master
        self.controller = controller
        self.entries = {}

    def createProjectForm(self, project_list: list[Project], project: Project):
        fields = ["Name", "Description", "Start Date", "End Date", "Budget"]
        if (not project.id):  # Jika proyek belum ada
            header = "Create new Project"
        else:
            header = "Edit Project"

        self.modal_window = CTkToplevel(self.master)
        self.modal_window.grab_set()
        self.modal_window.minsize(400, 450)
        form_frame = CTkFrame(self.modal_window)
        form_frame.place(relx=0.5, rely=0.1, anchor=N)
        form_label = CTkLabel(form_frame, text=header, anchor=N, font=("Arial", 20))
        form_label.grid(row=1, columnspan=2, pady=10)

        for i, field in enumerate(fields):
            label = CTkLabel(form_frame, text=field)
            label.grid(row=i + 2, column=0, padx=10, pady=5, sticky="w")

            if (field == "Description"):
                insert = 1.0
                entry = CTkTextbox(form_frame, width=200, height=100)
                entry.grid(row=i + 2, column=1, padx=10, pady=5)
            else:
                insert = 0
                entry = CTkEntry(form_frame, width=200, border_width=0)
                entry.grid(row=i + 2, column=1, padx=10, pady=5)

            key = field.lower().replace(" ", "_")
            self.entries[key] = entry
            entry.insert(insert, getattr(project, key, ""))

            if (key == "budget"):
                if (getattr(project, key, "") == 0):
                    entry.delete(0, END)
                entry.bind("<KeyRelease>", lambda event: Utility.format_currency(entry))

        button_submit = CTkButton(form_frame, text="Submit",
                                  command=lambda: self.inputProjectForm(project_list, project))
        button_submit.grid(row=i + 3, pady=10, columnspan=2)

    def inputProjectForm(self, project_list: list[Project], project: Project):
        error = self.validateInput()
        if error:
            error_window = CTkToplevel(self.master)
            error_window.grab_set()
            label = CTkLabel(error_window, text=error)
            label.grid(padx=10, pady=5, sticky="w")
            button_submit = CTkButton(error_window, text="OK", command=error_window.destroy)
            button_submit.grid(pady=10)
            return
        project.setName(self.entries["name"].get())
        project.setDescription(self.entries["description"].get("1.0", END).strip())
        project.setStartDate(self.entries["start_date"].get())
        project.setDeadline(self.entries["end_date"].get())
        project.setBudget(int(self.entries["budget"].get().replace('.', '')))

        self.controller.saveProject(project_list, project)
        self.closeProjectForm()

    def deleteProjectForm(self, project_list: list[Project], project: Project):
        self.modal_window = CTkToplevel(self.master)
        self.modal_window.grab_set()
        form_label = CTkLabel(self.modal_window, text="Are you sure you want to delete this project?", anchor=N)
        form_label.grid(row=0, pady=10, padx=10)
        p_title = CTkLabel(self.modal_window, text=project.name, anchor=N, font=("Arial", 15))
        p_title.grid(row=1)

        button_frame = CTkFrame(self.modal_window, fg_color=self.modal_window.cget("fg_color"))
        button_frame.grid()
        button_yes = CTkButton(button_frame, text="Delete", width=40,
                               command=lambda: (self.controller.deleteProject(project_list, project),
                                                self.closeProjectForm()))
        button_yes.grid(row=2, column=1, padx=10)
        button_no = CTkButton(button_frame, text="Cancel", width=40, command=self.closeProjectForm)
        button_no.grid(row=2, column=0, padx=10)

    def validateInput(self):
        if not self.entries["name"].get().strip():
            return "Project name is required."
        if not self.entries["budget"].get().replace('.', '').isdigit():
            return "Budget must be a number."
        return None  # No errors

    def closeProjectForm(self):
        self.modal_window.destroy()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PROJECT LIST <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class ProjectList:
    def __init__(self, master: CTk, form: ProjectForm):
        self.master = master
        self.form = form

    def showProjects(self, p_list: list[Project]):
        # To watch for changes
        self.proj_list = p_list
        self.prev_list = p_list.copy()
        self.frame = CTkFrame(self.master)
        self.frame.place(relx=0.5, rely=0.1, anchor=N)
        self.updateUI()
        self.watchProjectList()

    def watchProjectList(self):
        if self.proj_list != self.prev_list:
            self.prev_list = self.proj_list.copy()
            self.updateUI()
        self.master.after(500, self.watchProjectList)

    def updateUI(self) -> None:
        for widget in self.frame.winfo_children():
            widget.destroy()

        if (len(self.proj_list) == 0):
            no_project_label = CTkLabel(self.frame, text="No Projects to show")
            no_project_label.grid(row=0, column=0, padx=10)
            idx = 0

        pencil = CTkImage(light_image=Image.open("img/penico.png"), size=(16, 16))
        trash = CTkImage(light_image=Image.open("img/trashico.png"), size=(16, 16))
        plus = CTkImage(light_image=Image.open("img/plusico.png"), size=(16, 16))

        for idx, project in enumerate(self.proj_list):
            button_details = CTkButton(self.frame, text=f"{project.name}", anchor=W,
                                       command=lambda: self.showProjectDetails(project),
                                       fg_color=self.frame.cget("fg_color"))
            button_details.grid(row=idx, column=0)
            button_edit = CTkButton(self.frame, text="", image=pencil, width=5, command=lambda: self.edit(self.proj_list, project))  # noqa
            button_edit.grid(row=idx, column=1)
            delete_button = CTkButton(self.frame, text="", image=trash, width=5, command=lambda: self.delete(self.proj_list, project))  # noqa
            delete_button.grid(row=idx, column=2)

        button_add = CTkButton(self.frame, text="", image=plus, width=68, command=lambda: self.create(self.proj_list))
        button_add.grid(row=idx + 1, column=1, columnspan=2)

    def showProjectDetails(self, project: Project):
        self.frame.destroy()
        self.frame = CTkFrame(self.master)
        self.frame.place(relx=0.5, rely=0.1, anchor=N)

        button_back = CTkButton(self.frame, text="<", width=50, command=lambda: (self.frame.destroy(),self.showProjects(self.proj_list)), font=("", 20))  # noqa
        button_back.place(relx=0.1, rely=0.1)

        details_frame = CTkFrame(self.frame)
        details_frame.place(relx=0.5, rely=0.1)

        title = CTkLabel(details_frame, text=project.name)
        desc = CTkLabel(details_frame, text=project.description)
        start = CTkLabel(details_frame, text=f"Start: {project.start_date}")
        end = CTkLabel(details_frame, text=f"End: {project.deadline}")
        budget = CTkLabel(details_frame, text=f"Budget: {project.budget}")

        title.grid(row=0, column=0, columnspan=2)
        desc.grid(row=1, column=0, columnspan=2)
        start.grid(row=2, column=0, columnspan=1)
        end.grid(row=2, column=1, columnspan=1)
        budget.grid(row=3, column=0, columnspan=2)

    def create(self, project_list: list[Project]):
        project = Project()
        self.form.createProjectForm(project_list, project)

    def edit(self, project_list: list[Project], project: Project):
        self.form.createProjectForm(project_list, project)
        self.waitForModalToClose()

    def delete(self, project_list: list[Project], project: Project):
        self.form.deleteProjectForm(project_list, project)

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
                # Format as currency
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
