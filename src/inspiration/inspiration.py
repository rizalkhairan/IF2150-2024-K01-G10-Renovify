import customtkinter as ctk
from src.database.database import DBConnection()

class InspirationList:
    def __init__(self, master: ctk.CTk, controller: InspirationController):
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

class InspirationForm:
    def __init__(self):
        pass

class InspirationController:
    def __init__(self):
        self.InspirationList = InspirationList()
        self.db = DBConnection()
        self.getAllProjects()

    def getAllProjects(self):
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
            inspirations.append(inspiration)

class Inspiration:
    def __init__(self):
        pass  

    def setInspirationId(self, inspiration_id):
        self.inspiration_id = inspiration_id

    def setName(self, name):
        self.name = name

    def setCachedImagePath(self, cached_image_path):
        self.cached_image_path = cached_image_path

    def setExternalLink(self, external_link):
        self.external_link = external_link
    
    def setTags(self, tags):
        self.tags = tags
    
    def setDateUpdated(self, date_updated):
        self.date_updated = date_updated
    
    def getInspirationId(self):
        return self.inspiration_id

    def getName(self):
        return self.name
    
    def getCachedImagePath(self):
        return self.cached_image_path
    
    def getExternalLink(self):
        return self.external_link
    
    def getTags(self):
        return self.tags
    
    def getDateUpdated(self):
        return self.date_updated


if __name__=='__main__':
    root = ctk.CTk()
    inspiration = InspirationList(root)
    inspiration.showInspiration()
    root.mainloop()