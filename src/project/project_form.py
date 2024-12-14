from customtkinter import *
from src.project.project_controller import ProjectController
from src.project.utility import Utility
from src.project.project import Project


class ProjectForm():
    def __init__(self, master: CTk):
        self.master = master
        self.controller = ProjectController()
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
                entry = CTkTextbox(form_frame, width=200, height=100, fg_color="#343638")
                entry.grid(row=i + 2, column=1, padx=10, pady=5)
            else:
                insert = 0
                entry = CTkEntry(form_frame, width=200, border_width=0)
                entry.grid(row=i + 2, column=1, padx=10, pady=5)

            key = field.lower().replace(" ", "_")
            self.entries[key] = entry
            entry.insert(insert, getattr(project, key, ""))

            self.configureEntry(entry, key)

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
        start_date = self.entries["start_date"].get().strip()
        if start_date and not Utility.is_valid_date(start_date):
            return "Start date must be in DD-MM-YYYY format."
        end_date = self.entries["end_date"].get().strip()
        if end_date and not Utility.is_valid_date(end_date):
            return "End date must be in DD-MM-YYYY format."
        return None  # No errors

    def closeProjectForm(self):
        self.modal_window.destroy()

    def configureEntry(self, entry: CTkEntry, key: str):
        if (key == "budget"):
            if entry.get() == '0':
                entry.delete(0, END)
            entry.bind("<KeyRelease>", lambda event: Utility.format_currency(entry))
            entry.configure(placeholder_text="Rp.100.000.000")

        if (key == "start_date" or key == "end_date"):
            entry.configure(placeholder_text="DD-MM-YYYY")

        if (key == "name"):
            entry.configure(placeholder_text="Home Project")
