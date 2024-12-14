import customtkinter as ctk
from src.inspiration.Inspiration import Inspiration

class InspirationList:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.pagination = 5

    def showInspiration(self, inspirations: list[Inspiration]):
        self.inspiration_frame = ctk.CTkFrame(self.master)
        self.inspiration_frame.pack(fill='both', expand=True)


        index_first = 0
        index_last = min(self.pagination, len(inspirations))
        InspirationPage(self.inspiration_frame).showPage(inspirations[index_first:index_last])

    def create():
        pass

    def edit():
        pass

    def delete():
        pass

class InspirationPage():
    def __init__(self, master: ctk.CTkFrame):
        self.master = master
        self.page_frame = ctk.CTkFrame(self.master)

    
    def showPage(self, inspirations):
        for inspiration in inspirations:
            InspirationFrame(self.page_frame).showInspiration(inspiration)

class InspirationFrame():
    def __init__(self, master: ctk.CTkFrame):
        self.master = master

    def showInspiration(self, inspiration: Inspiration):
        pass