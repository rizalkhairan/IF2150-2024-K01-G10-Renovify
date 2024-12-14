from customtkinter import *
from src.project.project_form import ProjectForm
from src.project.utility import Utility
from src.project.project import Project
from src.project.project_filter import ProjectFilterUI
from PIL import Image

IMG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'img'))

class ProjectList:
    def __init__(self, master: CTk):
        self.master = master
        self.form = ProjectForm(self.master)
        self.filter = ProjectFilterUI(self.master, self)
        self.controller_project_list = self.form.controller.project_list

    def showProjects(self):
        # To watch for changes
        if hasattr(self, 'frame') and self.frame is not None:
            self.frame.destroy()

        self.current_page = 0
        self.projects_per_page = 15
        self.max_pages = (len(self.controller_project_list) - 1) // self.projects_per_page + 1

        self.proj_list = self.controller_project_list
        self.prev_list = self.controller_project_list.copy()
        self.frame = CTkFrame(self.master, width=700, height=500)
        self.frame.place(x=50, y=50)
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

        start_idx = self.current_page * self.projects_per_page
        end_idx = start_idx + self.projects_per_page
        current_projects = self.proj_list[start_idx:end_idx]


        if (len(self.proj_list) == 0):
            no_project_label = CTkLabel(self.frame, text="No projects to show", anchor=W,
                                        fg_color=self.frame.cget("fg_color"), font=("", 20), width=550)
            no_project_label.grid(row=0, column=0, padx=10)
            idx = 0
            
        pencil_path = os.path.join(IMG_PATH, "penico.png")
        trash_path = os.path.join(IMG_PATH, "trashico.png")
        plus_path = os.path.join(IMG_PATH, "plusico.png")

        pencil = CTkImage(light_image=Image.open(pencil_path), size=(16, 16))
        trash = CTkImage(light_image=Image.open(trash_path), size=(16, 16))
        plus = CTkImage(light_image=Image.open(plus_path), size=(16, 16))

        for idx, project in enumerate(current_projects):

            button_details = CTkButton(self.frame, text=f"{project.name}", anchor=W,
                                       command=lambda p=project: self.showProjectDetails(p),
                                       fg_color=self.frame.cget("fg_color"), font=("", 20), width=550)
            button_details.grid(row=idx, column=0, sticky="w", padx=(5, 0))
            button_edit = CTkButton(self.frame, text="", image=pencil, width=30, command=lambda p=project: self.edit(self.proj_list, p))
            button_edit.grid(row=idx, column=1)
            delete_button = CTkButton(self.frame, text="", image=trash, width=30, command=lambda p=project: self.delete(self.proj_list, p))
            delete_button.grid(row=idx, column=2)

        button_add = CTkButton(self.frame, text="", image=plus, width=68, command=lambda: self.create(self.proj_list))
        button_add.grid(row=idx + 1, column=1, columnspan=2)
        self.button_filter = CTkButton(self.master, text="Filter", width=75, command=self.filter.open_filter_window) # noqa
        self.button_filter.place(x=700, y=50)
        self.button_reset_filter = CTkButton(self.master, text="Reset Filter", width=68, command=self.resetFilter) # noqa
        self.button_reset_filter.place(x=700, y=80)

        self.prev_button = CTkButton(self.master, text="Previous", command=self.previousPage, width=80)
        self.prev_button.place(x=50, y=530)

        self.next_button = CTkButton(self.master, text="Next", command=self.nextPage, width=80)
        self.next_button.place(x=595, y=550)

    def nextPage(self):
        if self.current_page < self.max_pages - 1:
            self.current_page += 1
            self.updateUI()

    def previousPage(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.updateUI()

    def applyFiltered(self):
        query, params = self.filter.project_filter.build_filter_query(self.filter.filter_values)
        self.form.controller.applyFilterController(query, params)
        self.controller_project_list = self.form.controller.project_list
        self.showProjects()

    def resetFilter(self):
        self.form.controller.resetFilter()
        self.controller_project_list = self.form.controller.project_list
        self.frame.destroy()
        self.showProjects()

    def showTaskList(self, project_id):
        from src.task.task import TaskForm  # Pastikan path impor sesuai
        from src.task.task import TaskController
        from src.task.task import Task

        # Hapus tampilan proyek
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.button_filter.destroy()
        self.button_reset_filter.destroy()
        self.prev_button.destroy()
        self.next_button.destroy()

        # Membuat objek task baru
        task = Task()  # Pastikan Task adalah kelas yang valid dan sesuai
        task.setProjectId(project_id)  # Menambahkan projectId pada task baru
        task_controller = TaskController()

        # Panggil createTaskForm dengan project_id dan task
        task_form = TaskForm(master=self.master, controller=task_controller)
        task_form.createTaskForm(project_id, task)
        task_form.modal_window.grab_set()  # Menampilkan modal

    def showProjectDetails(self, project: Project):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.button_filter.destroy()
        self.button_reset_filter.destroy()
        self.prev_button.destroy()
        self.next_button.destroy()

        self.frame.destroy()
        self.frame = CTkFrame(self.master, width=600, height=500, fg_color=self.master.cget("fg_color"))
        self.frame.place(relx=0.5, rely=0.1, anchor=N)

        button_back = CTkButton(self.master, text="<", width=50, command=lambda: (self.frame.destroy(),button_back.destroy(),self.showProjects()), font=("", 20))
        button_back.place(relx=0.1, rely=0.1)

        title = CTkLabel(self.frame, text=project.name, justify="center", anchor="center", font=("", 25))
        desc = CTkLabel(self.frame, text=project.description, wraplength=300, justify="center", anchor="center", font=("", 15))
        start = CTkLabel(self.frame, text=f"Start: {project.start_date}", justify="center", anchor="center", font=("", 15))
        end = CTkLabel(self.frame, text=f"End: {project.deadline}", justify="center", font=("", 15))
        budget = CTkLabel(self.frame, text=f"Budget: {Utility.format_currency_int(project.budget)}",
                        justify="center", anchor="center", font=("", 15))

        title.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        desc.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        start.grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        end.grid(row=2, column=1, columnspan=1, padx=5, pady=5)
        budget.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        if (not project.status or project.status == '0'):
            done_text = "Mark as done"
            color = "#1F6AA5"
        elif (project.status):
            done_text = "Mark as not done"
            color = "green"
        mark_done = CTkButton(self.frame, text=done_text, width=20, fg_color=color,
                            command=lambda: (project.toggleStatus(), self.form.controller.saveProject(self.controller_project_list, project),
                                            self.showProjects(), button_back.destroy(), print(project.status)), font=("", 15))
        mark_done.grid(row=5, column=0, columnspan=2, pady=10)

        # Tombol View Tasks
        view_tasks = CTkButton(self.frame, text="View Tasks", width=20, fg_color="#1F6AA5",
                            command=lambda: self.showTaskList(project.id), font=("", 15))
        view_tasks.grid(row=6, column=0, columnspan=2, pady=10)

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