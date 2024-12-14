import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import customtkinter as ctk
from src.database.database import DBConnection
from src.inspiration.Inspiration import Inspiration
from src.inspiration.InspirationList import InspirationList
from src.inspiration.InspirationForm import InspirationForm

class InspirationController:
    def __init__(self, master: ctk.CTk):
        self.db = DBConnection()
        self.inspirations = [Inspiration() for _ in range(8)]   # Dummy inspirations
        self.master = master

    def showAllInspirations(self):
        self.inspiration_list = InspirationList(master=self.master, controller=self)
        self.inspiration_list.showInspirations(self.inspirations)   # self.inspirations ganti dengan self.getAllInspirations()


    def getAllInspirations(self):
        inspirations = []
        result = self.db.getAllProjects()
        for row in result:
            inspiration = Inspiration()
            inspiration.setInspirationId(row[0])
            inspiration.setName(row[1])
            inspiration.setCachedImagePath(row[2])
            inspiration.setExternalLink(row[3])
            inspiration.setDateUpdated(row[4])
            tags = self.db.getTagsById(inspiration.getInspirationId())
            inspiration.setTags(tags)
            inspirations.append(inspiration)
        
        self.inspirations = inspirations
        return inspirations

    def getInspiration(self, inspiration_id: int):
        inspiration = Inspiration()
        result = self.db.getProject(inspiration_id)
        for row in result:
            inspiration.setInspirationId(row[0])
            inspiration.setName(row[1])
            inspiration.setCachedImagePath(row[2])
            inspiration.setExternalLink(row[3])
            inspiration.setDateUpdated(row[4])
            tags = self.db.getTagsById(inspiration.getInspirationId())
            inspiration.setTags(tags)
        
        return inspiration
    
    def createInspiration(self, name: str, cached_image_path: str, link: str, date_updated: str, tags: list[str]):
        self.db.createInspiration(name, cached_image_path, link, date_updated, tags)

    def editInspiration(self, inspiration_id: int, name: str, cached_image_path: str, link: str, date_updated: str, tags: list[str]):
        self.db.editInspiration(inspiration_id, name, cached_image_path, link, date_updated, tags)

    def deleteInspiration(self, inspiration_id: int):
        self.db.deleteInspiration(inspiration_id)

    def createInspirationForm(self):
        inspiration_form = InspirationForm(master=self.master, controller=self)
        inspiration_form.showInspirationForm(-1)
    
    def editInspirationForm(self, inspiration_id: int):
        inspiration_form = InspirationForm(master=self.master, controller=self)
        inspiration_form.showInspirationForm(inspiration_id)


if __name__=='__main__':
    main_frame = ctk.CTk()
    main_frame.geometry("800x600")
    controller = InspirationController(main_frame)
    controller.showAllInspirations()
    main_frame.mainloop()