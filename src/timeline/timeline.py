import customtkinter as ctk
from tkcalendar import Calendar
from datetime import datetime


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
                            date_pattern='yyyy-mm-dd', font=("Arial", 11))
        calendar.grid(row=1, column=0, padx=20, pady=10)

        # Menambahkan detail timeline proyek di bawah kalender
        self.project_info_text = ctk.CTkTextbox(self.modal_window,
                                                width=400, height=200)
        self.project_info_text.grid(row=2, column=0, padx=20, pady=10)
        self.updateProjectInfo()

        for project in projects_dates:
            name, start_date, end_date = project
            # Tandai tanggal mulai proyek pada kalender
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            calendar.calevent_create(start_date_obj, name, 'project')
            # Tandai tanggal selesai proyek pada kalender
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            calendar.calevent_create(end_date_obj, name, 'project')

        # Menambahkan tombol untuk menutup window
        button_close = ctk.CTkButton(self.modal_window, text="Close",
                                     command=self.modal_window.destroy)
        button_close.grid(row=3, column=0, pady=10)

        # Menampilkan keterangan jadwal proyek pada tanggal yang diklik
        calendar.bind("<<CalendarSelected>>",
                      lambda event: self.showProjectDetails(calendar))

    # Menampilkan detail timeline proyek di bawah kalender
    def updateProjectInfo(self):
        projects_dates = self.timeline_controller.getAllProjectDates()
        project_details = ""

        for project in projects_dates:
            name, start_date, end_date = project
            project_details += f"Project {name}\n"
            project_details += f"Starting date: {start_date}\n"
            project_details += f"Completion date: {end_date}\n\n"

        self.project_info_text.delete(1.0, "end")
        self.project_info_text.insert("insert", project_details)

    # Menampilkan detail jadwal proyek pada tanggal yang diklik di kalender
    def showProjectDetails(self, calendar):
        selected_date = calendar.get_date()
        selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

        projects_on_selected_date = [
            project for project in
            self.timeline_controller.getAllProjectDates()
            if selected_date_obj >= datetime.strptime(project[1],
                                                      "%Y-%m-%d").date()
            and selected_date_obj <= datetime.strptime(project[2],
                                                       "%Y-%m-%d").date()
        ]

        if projects_on_selected_date:
            project_details = "\n".join(
                [f"Project '{
                        project[0]
                        }'is scheduled from {project[1]} to {project[2]}"
                    for project in projects_on_selected_date]
            )
            self.showNotification(f"Projects on {selected_date}",
                                  project_details)
        else:
            self.showNotification("No Project",
                                  "No project scheduled on this date.")

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


class TimelineController:
    def __init__(self, db_path):
        self.db_path = db_path

    def getAllProjectDates(self):
        with DBConnection(self.db_path) as db:
            projects = db.getAllProjects()
            project_dates = []
            for project in projects:
                name = project[1]
                start_date = project[4]
                end_date = project[5]
                project_dates.append((name, start_date, end_date))
            return project_dates
