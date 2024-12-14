from customtkinter import *


class ProjectFilter:
    def build_filter_query(self, filters: dict[str, any]) -> tuple[str, list[any]]:
        """
        Build the SQL query and parameters for filtering projects.

        :param filters: Dictionary of filters.
        :return: Tuple containing the query string and parameter list.
        """
        query = "SELECT * FROM projects WHERE 1=1"
        params = []

        # Add dynamic filters based on the table columns
        if 'status' in filters and filters['status'] is not None:
            query += " AND status = ?"
            params.append(filters['status'])

        if 'start_date_range' in filters and filters['start_date_range']:
            query += " AND start_date BETWEEN ? AND ?"
            params.extend(filters['start_date_range'])

        if 'completion_date_range' in filters and filters['completion_date_range']:
            query += " AND completion_date BETWEEN ? AND ?"
            params.extend(filters['completion_date_range'])

        if 'budget_range' in filters and filters['budget_range']:
            query += " AND budget BETWEEN ? AND ?"
            params.extend(filters['budget_range'])

        return query, params

    # def getFilteredProjects(self, query, params):


class ProjectFilterUI:
    def __init__(self, root, parent):
        self.root = root
        self.filter_values = {}
        self.project_filter = ProjectFilter()
        self.parent = parent

    def open_filter_window(self):
        filter_window = CTkToplevel(self.root)
        filter_window.title("Filter Projects")
        filter_window.geometry("400x500")

        # Status Filter (Dropdown)
        CTkLabel(filter_window, text="Status:").pack(pady=(10, 0))
        self.status_var = StringVar(value="All")
        self.status_menu = CTkOptionMenu(filter_window, variable=self.status_var, values=["All", "Done", "Not Done"])
        self.status_menu.pack(pady=5)

        # Start Date Range
        CTkLabel(filter_window, text="Start Date Range (YYYY-MM-DD):").pack(pady=(10, 0))
        self.start_date_entry1 = CTkEntry(filter_window, placeholder_text="Start Date")
        self.start_date_entry1.pack(pady=5)
        self.start_date_entry2 = CTkEntry(filter_window, placeholder_text="End Date")
        self.start_date_entry2.pack(pady=5)

        # Completion Date Range
        CTkLabel(filter_window, text="Completion Date Range (YYYY-MM-DD):").pack(pady=(10, 0))
        self.comp_date_entry1 = CTkEntry(filter_window, placeholder_text="Start Date")
        self.comp_date_entry1.pack(pady=5)
        self.comp_date_entry2 = CTkEntry(filter_window, placeholder_text="End Date")
        self.comp_date_entry2.pack(pady=5)

        # Budget Range
        CTkLabel(filter_window, text="Budget Range:").pack(pady=(10, 0))
        self.budget_entry1 = CTkEntry(filter_window, placeholder_text="Min Budget")
        self.budget_entry1.pack(pady=5)
        self.budget_entry2 = CTkEntry(filter_window, placeholder_text="Max Budget")
        self.budget_entry2.pack(pady=5)

        # Apply Filters Button
        apply_button = CTkButton(filter_window, text="Apply Filters", command=lambda: self.onSubmit(filter_window)) # noqa
        apply_button.pack(pady=20)

    def onSubmit(self, window):
        self.filter_values = {}
        status = self.status_var.get()
        if status == "Done":
            self.filter_values['status'] = True
        elif status == "Not Done":
            self.filter_values['status'] = False

        start_date1 = self.start_date_entry1.get().strip()
        start_date2 = self.start_date_entry2.get().strip()
        if start_date1 and start_date2:
            self.filter_values['start_date_range'] = (start_date1, start_date2)
        elif start_date1:
            self.filter_values['start_date_range'] = (start_date1, "9999-12-31")
        elif start_date2:
            self.filter_values['start_date_range'] = ("0000-01-01", start_date2)

        comp_date1 = self.comp_date_entry1.get().strip()
        comp_date2 = self.comp_date_entry2.get().strip()
        if comp_date1 and comp_date2:
            self.filter_values['completion_date_range'] = (comp_date1, comp_date2)
        elif comp_date1:
            self.filter_values['completion_date_range'] = (comp_date1, "9999-12-31")
        elif comp_date2:
            self.filter_values['completion_date_range'] = ("0000-01-01", comp_date2)

        budget1 = self.budget_entry1.get().strip()
        budget2 = self.budget_entry2.get().strip()
        if budget1 and budget2:
            self.filter_values['budget_range'] = (float(budget1), float(budget2))
        elif budget1:
            self.filter_values['budget_range'] = (float(budget1), float("inf"))
        elif budget2:
            self.filter_values['budget_range'] = (0, float(budget2))
        window.destroy()
        self.parent.applyFiltered()
