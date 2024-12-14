import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import customtkinter as ctk
from tkcalendar import Calendar
import src.database.database as database
from datetime import datetime
from src.database.database import DBConnection


class DisplayTimeline:
    def __init__(self, master: ctk.CTk,
                 timeline_controller: 'TimelineController'):
        self.master = master
        self.timeline_controller = timeline_controller

    def displayMarkedCalendar(self):
        # Mengambil daftar tanggal mulai dan tanggal berakhir setiap proyek
        projects_dates = self.timeline_controller.getAllProjectDates()

        # Jika belum ada proyek
        if not projects_dates:
            self.showNotification(
                "No Projects",
                "There are no projects with start and end dates."
                )
            return

        # Membuat window untuk kalender
        self.master.withdraw()  # Menyembunyikan window master
        self.modal_window = ctk.CTkToplevel(self.master)
        self.modal_window.grab_set()
        self.modal_window.title("Project Timeline")

        # Menambahkan title window
        title_label = ctk.CTkLabel(
            self.modal_window,
            text="Project Timeline",
            font=("Arial", 20),
            text_color="#E2C4C4"
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Membuat kalender timeline
        calendar = Calendar(self.modal_window, selectmode='day',
                            date_pattern='dd-mm-yyyy', font=("Arial", 11))
        calendar.grid(row=1, column=0, padx=20, pady=10)

        # Menambahkan detail timeline proyek di bawah kalender
        self.project_info_text = ctk.CTkTextbox(self.modal_window,
                                                width=400, height=200)
        self.project_info_text.grid(row=2, column=0, padx=20, pady=10)
        self.updateProjectInfo()

        for project in projects_dates:
            name, start_date, end_date = project
            # Tandai tanggal mulai proyek pada kalender
            start_date_obj = datetime.strptime(start_date, '%d-%m-%Y').date()
            calendar.calevent_create(start_date_obj, name, 'project')
            # Tandai tanggal selesai proyek pada kalender
            end_date_obj = datetime.strptime(end_date, '%d-%m-%Y').date()
            calendar.calevent_create(end_date_obj, name, 'project')

        # Menambahkan tombol untuk menutup window
        button_close = ctk.CTkButton(self.modal_window, text="Close",
                                     command=self.closeModal)
        button_close.grid(row=3, column=0, pady=10)

        # Menampilkan keterangan jadwal proyek pada tanggal yang diklik
        calendar.bind("<<CalendarSelected>>",
                      lambda event: self.showProjectDetails(calendar))

        # Menangani event ketika modal window ditutup dengan tombol exit
        self.modal_window.protocol("WM_DELETE_WINDOW", self.closeModal)

    # Menampilkan detail timeline proyek di bawah kalender
    def updateProjectInfo(self):
        projects_dates = self.timeline_controller.getAllProjectDates()
        unique_projects = set()  # Menggunakan set untuk menghindari duplikasi
        project_details = ""

        for project in projects_dates:
            name, start_date, end_date = project
            project_key = (name, start_date, end_date)
            if project_key not in unique_projects:
                unique_projects.add(project_key)
                start_date_word = self.format_date_to_words(start_date)
                end_date_word = self.format_date_to_words(end_date)
                project_details += f"'{name}'\n"
                project_details += f"Starting date: {start_date_word}\n"
                project_details += f"Completion date: {end_date_word}\n\n"

        self.project_info_text.delete(1.0, "end")
        self.project_info_text.insert("insert", project_details)

    # Menampilkan detail jadwal proyek pada tanggal yang diklik di kalender
    def showProjectDetails(self, calendar):
        selected_date = calendar.get_date()
        selected_date_obj = datetime.strptime(selected_date, '%d-%m-%Y').date()

        projects_on_selected_date = [
            project for project in
            self.timeline_controller.getAllProjectDates()
            if selected_date_obj >= datetime.strptime(project[1],
                                                      "%d-%m-%Y").date()
            and selected_date_obj <= datetime.strptime(project[2],
                                                       "%d-%m-%Y").date()
        ]

        unique_projects = set()  # Menggunakan set untuk menghindari duplikasi
        filtered_projects = []

        for project in projects_on_selected_date:
            name, start_date, end_date = project
            project_key = (name, start_date, end_date)
            if project_key not in unique_projects:
                unique_projects.add(project_key)
                filtered_projects.append(project)

        if filtered_projects:
            project_details = "\n".join(
                [
                    f"'{project[0]}' is scheduled from "
                    f"{self.format_date_to_words(project[1])} to "
                    f"{self.format_date_to_words(project[2])}"
                    for project in filtered_projects
                ]
            )
            self.showNotification(f"Projects on {selected_date}",
                                  project_details)
        else:
            self.showNotification("No Project",
                                  "No project scheduled for this date.")

    # Menampilkan pop-up untuk jadwal proyek pada tanggal yang diklik
    def showNotification(self, title, message):
        popup = ctk.CTkToplevel(self.master)
        popup.grab_set()
        popup.title(title)
        popup.configure(bg="#2B2B2B")

        title_label = ctk.CTkLabel(
            popup,
            text=title,
            font=("Arial", 16),
            text_color="#E2C4C4"
        )
        title_label.pack(pady=(20, 10), padx=20)

        message_label = ctk.CTkLabel(
            popup,
            text=message,
            font=("Arial", 14),
            text_color="#FFFFFF",
            wraplength=300
        )
        message_label.pack(pady=(0, 20), padx=20)

        close_button = ctk.CTkButton(popup, text="Close",
                                     command=popup.destroy)
        close_button.pack(pady=10)

    # Mengubah format YYYY-MM-DD menjadi string tanggal
    def format_date_to_words(self, date_str):
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        day = date_obj.day
        month = date_obj.strftime('%B')
        year = date_obj.year
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        return f"{month} {day}{suffix} {year}"

    def closeModal(self):
        self.modal_window.destroy()  # Menutup window timeline
        self.master.deiconify()  # Menampilkan kembali window master


class TimelineController:
    def __init__(self):
        self.db = DBConnection()

    def getAllProjectDates(self):
        with database.DBConnection() as db:
            projects = db.getAllProjects()
            project_dates = []
            for project in projects:
                name = project[1]
                start_date = project[4]
                end_date = project[5]
                project_dates.append((name, start_date, end_date))
            return project_dates
