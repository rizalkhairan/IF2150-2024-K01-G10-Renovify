import customtkinter as ctk

class InspirationForm:
    def __init__(self, master: ctk.CTk, controller):
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.widgets = []

        self.controller = controller
    
    def destroyWidgets(self):
        for widget in self.widgets:
            widget.destroy()
    
    def showInspirationForm(self, inspiration_id):        
        pass

    