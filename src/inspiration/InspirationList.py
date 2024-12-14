import customtkinter as ctk

class InspirationList:
    def __init__(self, master: ctk.CTk):
        self.master = master

    def showInspiration(self):
        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(fill='both', expand=True)

        create_new = ctk.CtkButton(self.main_frame, text='+', command=self.create())

        if (self.controller.number_of_inspirations==0):
            ctk.CTkLabel(self.main_frame, text='No inspirations found').pack()
        else:
            for i in range(self.controller.number_of_inspirations):
                ctk.CTkLabel(self.main_frame, text=self.controller.inspirations[i].title).pack()

    def create():
        pass

    def edit():
        pass

    def delete():
        pass