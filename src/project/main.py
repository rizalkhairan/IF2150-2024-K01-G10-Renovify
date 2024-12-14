import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from customtkinter import *
# from tkcalendar import Calendar
from src.project.project import Project
from src.project.project_controller import ProjectController
from src.project.project_form import ProjectForm
from src.project.project_list import ProjectList


set_default_color_theme("blue")

# for i in range(1, 6):
#     project = pr.Project()
#     project.id = i
#     project.name = f"Project {i}"
#     project.description = f"Description of Project {i}"
#     project.status = i % 2 == 0  # Alternate between done (True) and not done (False)
#     project.start_date = f"2024-12-{i:02d}"
#     project.completion_date = f"2024-12-{i+10:02d}"
#     project.budget = i * 1000
#     project_list.append(project)


def move_focus(event):
    event.widget.tk_focusNext().focus_set()


root = CTk()
root.geometry("800x600")
default_font = CTkFont(family="Helvetica", size=50)

# def main():

project = Project()
project_display = ProjectList(root)
project_display.showProjects()


# cal = Calendar(root, selectmode="day", year=2024, month=12, day=4)
# cal.pack(pady=20)

root.mainloop()
