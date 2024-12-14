from customtkinter import *
from src.project.project_form import ProjectForm
from src.project.utility import Utility
from src.project.project import Project
from PIL import Image


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
                                       command=lambda p=project: self.showProjectDetails(p),
                                       fg_color=self.frame.cget("fg_color"))
            button_details.grid(row=idx, column=0)
            button_edit = CTkButton(self.frame, text="", image=pencil, width=5, command=lambda p=project: self.edit(self.proj_list, p))  # noqa
            button_edit.grid(row=idx, column=1)
            delete_button = CTkButton(self.frame, text="", image=trash, width=5, command=lambda p=project: self.delete(self.proj_list, p))  # noqa
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
        budget = CTkLabel(details_frame, text=f"Budget: {Utility.format_currency_int(project.budget)}")

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
