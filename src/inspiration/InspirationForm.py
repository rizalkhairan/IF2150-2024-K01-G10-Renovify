import customtkinter as ctk
from datetime import datetime

class InspirationForm:
    def __init__(self, master: ctk.CTk, controller):
        self.master = ctk.CTkToplevel(width=400, height=500)
        self.master.attributes("-topmost", True)
        self.widgets = []

        self.controller = controller
    
    def destroyWidgets(self):
        for widget in self.widgets:
            widget.destroy()
    
    def showInspirationForm(self, inspiration_id):
        self.inspiration_id = inspiration_id    
        if inspiration_id==-1:
            title_text = "Create Inspiration"
        else:
            title_text = "Edit Inspiration"
        self.title = ctk.CTkLabel(self.master, text=title_text, width=400, height=50)
        self.title.grid(row=0, column=0, columnspan=2, pady=5)
        
        self.name_entry_label = ctk.CTkLabel(self.master, text="Name", width=20, height=30)
        self.name_entry_label.grid(row=1, column=0, pady=5)
        self.widgets.append(self.name_entry_label)
        self.name_entry = ctk.CTkEntry(self.master, width=250, height=30)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.widgets.append(self.name_entry)
        if (inspiration_id != -1):
            self.name_entry.insert(0, self.controller.getInspiration(inspiration_id).getName())

        self.link_entry_label = ctk.CTkLabel(self.master, text="Link", width=20, height=30)
        self.link_entry_label.grid(row=2, column=0, pady=5)
        self.widgets.append(self.link_entry_label)
        self.link_entry = ctk.CTkEntry(self.master, width=250, height=30)
        self.link_entry.grid(row=2, column=1, padx=5, pady=5)
        self.widgets.append(self.link_entry)
        if (inspiration_id != -1):
            self.link_entry.insert(0, self.controller.getInspiration(inspiration_id).getExternalLink())

        self.tags_label = ctk.CTkLabel(self.master, text="Tags\n(Separate by each line)", width=20, height=30)
        self.tags_label.grid(row=3, column=0, pady=5)
        self.widgets.append(self.tags_label)
        self.tags_textbox = ctk.CTkTextbox(self.master, width=250, height=50)
        self.tags_textbox.grid(row=3, column=1, padx=5, pady=5)
        self.widgets.append(self.tags_textbox)
        if (inspiration_id != -1):
            tags = self.controller.getInspiration(inspiration_id).getTags()
            tags_str = ""
            for tag in tags:
                tags_str += tag + "\n"
            self.tags_textbox.insert(0.0, tags_str)

        self.submit_button = ctk.CTkButton(self.master, text="Submit", width=50, height=30, command=self.inputInspiration)   
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=5)
    
    def inputInspiration(self):
        name = self.name_entry.get()
        cached_image_path = "img/logo.jpg"
        link = self.link_entry.get()
        date_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tags = self.tags_textbox.get("0.0", "end-1c").split("\n")
        if self.inspiration_id == -1:
            self.controller.createInspiration(name, cached_image_path, link, date_update, tags)
        else:
            self.controller.editInspiration(self.inspiration_id, name, cached_image_path, link, date_update, tags)
        self.destroyWidgets()
        self.controller.inspiration_list.showInspirations(self.controller.getAllInspirations())
        self.master.destroy()