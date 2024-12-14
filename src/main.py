import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from customtkinter import *  # noqa: F403
from PIL import Image
import customtkinter as ctk
import src.database.database as db
import src.task.task as task
from tkcalendar import DateEntry
from tkinter import ttk
from datetime import datetime
from src.inspiration.InspirationController import InspirationController
from src.timeline.timeline import DisplayTimeline, TimelineController
from src.budget.budget import ShowBudget, BudgetController, ExpenseController, ExpenseForm, ExpenseList

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Custom Navbar")
        self.geometry("800x600")

        # Tentukan path ke database
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Lokasi main.py
        db_path = os.path.join(base_dir, "../database/your_database_file.db")  # Sesuaikan nama file

        # Inisialisasi TimelineController dengan path database
        self.timeline_controller = TimelineController(db_path)
        self.timeline_view = DisplayTimeline(self, self.timeline_controller)
        self.inspiration_controller = InspirationController(master=self)
        self.expense_controller = ExpenseController(master=self)
        self.expense_form = ExpenseForm(self, self.expense_controller)
        self.expense_list = ExpenseList(self, self.expense_controller)
        self.budget_controller = BudgetController(db_path)
        self.budget_view = ShowBudget(self, self.budget_controller)


        # Navbar container (frame)
        self.navbar_frame = CTkFrame(self, fg_color="#192841", height=80)
        self.navbar_frame.grid(row=0, column=0, sticky="ew")

        # Navbar buttons
        self.create_nav_button("Project", self.open_project, 0)
        self.create_nav_button("Inspiration", self.open_inspiration, 1)
        self.create_nav_button("Budget", self.open_budget, 2)
        self.create_nav_button("Timeline", self.open_timeline, 3)

    # ... rest of the methods remain unchanged ...

    def create_nav_button(self, text, command, position):
        button = CTkButton(
            self.navbar_frame,
            text=text,
            command=command,
            fg_color="#192841",  # Same as navbar background to blend
            hover_color="#404040",  # Highlight on hover
            text_color="white",
            corner_radius=0,  # Make the button edges square to match the navbar
            width=200
        )
        button.grid(row=0, column=position, sticky="ew")

    # Example functions for button actions
    def open_project(self):
        print("Opening Project section...")

    def open_inspiration(self):
        self.inspiration_controller.showAllInspirations()

    def open_budget(self):
        # self.inspiration_controller.showAllInspirations()
        self.budget_view.displayAllProjectsBudget()
        self.expense_list.showExpenses()
        self.expense_form.createExpenseForm()
        # print("Opening Budget section...")

    def open_timeline(self):
        # Membuka tampilan timeline
        self.timeline_view.displayMarkedCalendar()

if __name__ == "__main__":
    app = App()
    app.mainloop()
