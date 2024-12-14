from customtkinter import *
from src.project.project_form import ProjectForm
from src.project.utility import Utility
from src.project.project import Project
from src.project.project_filter import ProjectFilterUI
from PIL import Image


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
        self.proj_list = self.controller_project_list
        self.prev_list = self.controller_project_list.copy()
        self.frame = CTkFrame(self.master, width=700, height=500)
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
                                       command=lambda p=project: self.showProjectDetails(p),
                                       fg_color=self.frame.cget("fg_color"))
            button_details.grid(row=idx, column=0)
            button_edit = CTkButton(self.frame, text="", image=pencil, width=30, command=lambda p=project: self.edit(self.proj_list, p))  # noqa
            button_edit.grid(row=idx, column=1)
            delete_button = CTkButton(self.frame, text="", image=trash, width=30, command=lambda p=project: self.delete(self.proj_list, p))  # noqa
            delete_button.grid(row=idx, column=2)

        button_add = CTkButton(self.frame, text="", image=plus, width=68, command=lambda: self.create(self.proj_list))
        button_add.grid(row=idx + 1, column=1, columnspan=2)

        button_filter = CTkButton(self.master, text="Filter", width=75, command=self.filter.open_filter_window) # noqa
        button_filter.place(relx=0.1, rely=0.1, relheight=0.05, relwidth=0.12)
        button_reset_filter = CTkButton(self.master, text="Reset Filter", width=68, command=self.resetFilter) # noqa
        button_reset_filter.place(relx=0.1, rely=0.175, relheight=0.05, relwidth=0.12)

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

    def showProjectDetails(self, project: Project):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.frame = CTkFrame(self.master)
        self.frame.place(relx=0.5, rely=0.1, anchor=N)

        button_back = CTkButton(self.master, text="<", width=50, command=lambda: (self.frame.destroy(),button_back.destroy(),self.showProjects()), font=("", 20))  # noqa
        button_back.place(relx=0.1, rely=0.1)

        details_frame = CTkFrame(self.frame, fg_color=self.frame.cget("fg_color"))
        details_frame.place(relx=0, rely=0.1)

        title = CTkLabel(details_frame, text=project.name)
        desc = CTkLabel(details_frame, text=project.description)
        start = CTkLabel(details_frame, text=f"Start: {project.start_date}")
        end = CTkLabel(details_frame, text=f"End: {project.deadline}")
        budget = CTkLabel(details_frame, text=f"Budget: {Utility.format_currency_int(project.budget)}")

        title.grid(row=0, column=0, columnspan=2)
        desc.grid(row=1, column=0, columnspan=2)
        start.grid(row=2, column=0, columnspan=1)
        end.grid(row=2, column=1, columnspan=1)
        budget.grid(row=3, column=0, columnspan=2)

        if (project.status):
            done_text = "Mark as done"
            color = "#1F6AA5"
        else:
            done_text = "Mark as not done"
            color = "green"
        print(project.status)
        mark_done = CTkButton(details_frame, text=done_text, width=20, fg_color=color,
                              command=lambda: (project.toggleStatus(),self.form.controller.saveProject(self.controller_project_list,project),                   # noqa
                                               self.showProjects(), button_back.destroy(),print(project.status)), font=("", 20))  # noqa
        mark_done.grid(row=5, column=0, columnspan=2, pady=10)

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
