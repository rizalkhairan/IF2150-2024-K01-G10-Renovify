import customtkinter as ctk
from PIL import Image
from Inspiration import Inspiration
from functools import partial

class InspirationList:
    def __init__(self, master: ctk.CTk, controller):
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.widgets = []

        self.pagination = 3

        self.controller = controller

    def destroyWidgets(self):
        for widget in self.widgets:
            widget.destroy()

    def showInspirations(self, inspirations: list[Inspiration]):
        self.inspirations = inspirations

        self.inspiration_frame = ctk.CTkFrame(self.master, width=800, height=500)
        self.inspiration_frame.grid(row=1, column=0)
        self.widgets.append(self.inspiration_frame)
        
        self.title = ctk.CTkLabel(self.inspiration_frame, text="Inspirations", width=800, height=50)    
        self.title.grid(row=0, column=0, pady=5)
        self.widgets.append(self.title)
        
        self.add_button = ctk.CTkButton(self.inspiration_frame, text="Create", width=50, height=30, command=self.create)
        self.add_button.grid(row=1, column=0, padx=5)
        self.widgets.append(self.add_button)

        self.inspiration_page = ctk.CTkFrame(self.inspiration_frame, width=800, height=500)
        self.inspiration_page.grid(row=2, column=0, pady=10)
        self.inspiration_page.grid_columnconfigure(0, weight=1)
        self.widgets.append(self.inspiration_page)
        self.page = InspirationPage(self.inspiration_page, self)
        self.page_count = 1+((len(inspirations)-1)//self.pagination)
        self.current_page = 0
        self.page.showPage(inspirations, self.current_page)

        self.button_frame = ctk.CTkFrame(self.inspiration_frame, width=800, height=50, fg_color='transparent')
        self.button_frame.grid(row=3, column=0)
        self.left_button = ctk.CTkButton(self.button_frame, text="<", width=30, height=1, command=self.prevPage)
        self.left_button.grid(row=0, column=0, padx=20)
        self.page_label = ctk.CTkLabel(self.button_frame, text=f"{self.current_page+1}/{self.page_count}", width=30, height=1)
        self.page_label.grid(row=0, column=1)
        self.right_button = ctk.CTkButton(self.button_frame, text=">", width=30, height=1, command=self.nextPage)
        self.right_button.grid(row=0, column=2, padx=20)
        
        self.widgets.append(self.button_frame)
        self.widgets.append(self.left_button)
        self.widgets.append(self.page_label)
        self.widgets.append(self.right_button)

    def prevPage(self):
        self.current_page = max(0, self.current_page-1)
        self.page.showPage(self.inspirations, self.current_page)
        self.page_label.destroy()
        self.page_label = ctk.CTkLabel(self.button_frame, text=f"{self.current_page+1}/{self.page_count}", width=30, height=1)
        self.page_label.grid(row=0, column=1)

    def nextPage(self):
        self.current_page = min(self.page_count-1, self.current_page+1)
        self.page.showPage(self.inspirations, self.current_page)
        self.page_label.destroy()
        self.page_label = ctk.CTkLabel(self.button_frame, text=f"{self.current_page+1}/{self.page_count}", width=30, height=1)
        self.page_label.grid(row=0, column=1)


    def create(self):
        self.controller.createInspirationForm()

    def edit(self, inspiration_id: int):
        self.controller.editInspirationForm(inspiration_id)

    def delete(self, inspiration_id: int):
        self.confirmation_window = ctk.CTkToplevel(width=200, height=100)
        self.confirmation_window.attributes("-topmost", True)
        self.confirmation_window.title("Are you sure?")
        self.confirmation_window.grid_columnconfigure(0, weight=1)
        
        self.confirm_button = ctk.CTkButton(self.confirmation_window, text="Yes", width=50, height=30, command=lambda: self.confirm_delete(inspiration_id))
        self.confirm_button.grid(row=0, column=0, padx=5)
        self.cancel_button = ctk.CTkButton(self.confirmation_window, text="No", width=50, height=30, command=self.cancel_delete)
        self.cancel_button.grid(row=0, column=1, padx=5)

    def confirm_delete(self, inspiration_id: int):
        self.controller.deleteInspiration(inspiration_id)
        self.confirmation_window.destroy()
    def cancel_delete(self):
        self.confirmation_window.destroy()

class InspirationPage():
    def __init__(self, master: ctk.CTkFrame, inspiration_list: InspirationList):
        self.master = master
        self.widgets = []
        self.inspiration_list = inspiration_list
        self.pagination = self.inspiration_list.pagination
    
    def destroyWidgets(self):
        for widget in self.widgets:
            widget.destroy()

    def showPage(self, inspirations: list[Inspiration], page: int):
        self.destroyWidgets()

        first_index = page*self.pagination
        last_index = min(len(inspirations), page*self.pagination+self.pagination)
        inspirations = inspirations[first_index:last_index]
        for i, inspiration in enumerate(inspirations):
            title = ctk.CTkLabel(self.master, text=f"{inspiration.getName()}", width=200, height=50)
            title.grid(row=0, column=i, padx=5)
            self.widgets.append(title)


            image = ctk.CTkImage(light_image=Image.open('img/logo.jpg'), size=(250, 250))
            image = ctk.CTkLabel(self.master, image=image, text='')
            image.grid(row=1, column=i, padx=5)
            self.widgets.append(image)

            date_label = ctk.CTkLabel(self.master, text=f"{inspiration.getDateUpdated()}", width=20, height=5, font=('Arial', 10))
            date_label.grid(row=2, column=i, padx=5, sticky='w')
            self.widgets.append(date_label)

            link_label = ctk.CTkLabel(self.master, text=f"{inspiration.getExternalLink()}", width=20, height=5, font=('Arial', 10))
            link_label.grid(row=2, column=i, padx=5, sticky='e')
            self.widgets.append(link_label)
            
            tags = ctk.CTkTextbox(self.master, width=200, height=50, fg_color='transparent', wrap='word')
            tags.insert("0.0", f"Tags: {', '.join(inspiration.getTags())}")
            # tags._textbox.tag_configure("text", justify='center')
            tags.configure(state='disabled')
            tags.grid(row=3, column=i, padx=5)
            self.widgets.append(tags)    

            edit_delete_frame = ctk.CTkFrame(self.master, width=250, height=50, fg_color="transparent")
            edit_delete_frame.grid(row=4, column=i, padx=5)
            self.widgets.append(edit_delete_frame)
            edit_action = partial(self.inspiration_list.edit, inspiration.getInspirationId())
            edit_icon = Image.open('img/penico.png')
            edit_icon = ctk.CTkImage(light_image=edit_icon, size=(20, 20))
            edit_button = ctk.CTkButton(edit_delete_frame, text="Edit", image=edit_icon, width=50, height=30, command=edit_action)
            edit_button.grid(row=0, column=0, padx=5)
            self.widgets.append(edit_button)
            delete_action = partial(self.inspiration_list.delete, inspiration.getInspirationId())
            delete_icon = Image.open('img/trashico.png')
            delete_icon = ctk.CTkImage(light_image=delete_icon, size=(20, 20))
            delete_button = ctk.CTkButton(edit_delete_frame, text="Delete", image=delete_icon,width=50, height=30, command=delete_action)
            delete_button.grid(row=0, column=1, padx=5)
            self.widgets.append(delete_button)