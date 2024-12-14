import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from customtkinter import *  # noqa: F403
from PIL import Image, ImageTk
import customtkinter as ctk
import src.database.database as db
import src.task.task as task
from tkcalendar import DateEntry
from tkinter import ttk
from datetime import datetime
from src.inspiration.InspirationController import InspirationController
from src.timeline.timeline import DisplayTimeline, TimelineController
from src.project.project_list import ProjectList
# from src.budget.budget import ShowBudget, ExpenseController, ExpenseForm, ExpenseList

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Custom Navbar")
        self.geometry("800x600")

        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        
        self.project_view = ProjectList(master=self)
        self.timeline_controller = TimelineController()
        self.timeline_view = DisplayTimeline(self, self.timeline_controller)
        self.inspiration_controller = InspirationController(master=self)
        # self.expense_controller = ExpenseController()
        # self.expense_form = ExpenseForm(self, self.expense_controller)
        # self.expense_list = ExpenseList(self, self.expense_controller)
        # self.budget_controller = BudgetController()
        # self.budget_view = ShowBudget(self, self.budget_controller)

        img_path = os.path.join(base_dir, "../img/renovify.png") 
        self.image = Image.open(img_path) 
        self.photo = ImageTk.PhotoImage(self.image)  

        self.img_label = CTkLabel(self, image=self.photo, text="") 
        self.img_label.grid(row=1, column=0, padx=20, pady=20)

        self.navbar_frame = CTkFrame(self, fg_color="#192841", height=80)
        self.navbar_frame.grid(row=0, column=0, sticky="ew")

        self.create_nav_button("Project", self.open_project, 0)
        self.create_nav_button("Inspiration", self.open_inspiration, 1)
        self.create_nav_button("Budget", self.open_budget, 2)
        self.create_nav_button("Timeline", self.open_timeline, 3)

    def create_nav_button(self, text, command, position):
        button = CTkButton(
            self.navbar_frame,
            text=text,
            command=command,
            fg_color="#192841",  
            hover_color="#404040",  
            text_color="white",
            corner_radius=0, 
            width=200,
            font=("Segoe UI", 16)  
        )
        button.grid(row=0, column=position, sticky="ew")

    def open_project(self):
        self.inspiration_controller.inspiration_list.destroyWidgets()
        self.project_view.showProjects()

    def open_inspiration(self):
        self.inspiration_controller.showAllInspirations()

    def open_budget(self):
        # self.inspiration_controller.showAllInspirations()
        # self.budget_view.displayAllProjectsBudget()
        # self.expense_list.showExpenses()
        # self.expense_form.createExpenseForm()
        # print("Opening Budget section...")
        pass

    def open_timeline(self):
        self.timeline_view.displayMarkedCalendar()

if __name__ == "__main__":
    app = App()
    app.mainloop()