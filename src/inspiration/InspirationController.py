from src.database.database import DBConnection
from src.inspiration.Inspiration import Inspiration
from src.inspiration.InspirationList import InspirationList
from src.inspiration.InspirationForm import InspirationForm

class InspirationController:
    def __init__(self):
        self.InspirationList = InspirationList()
        self.db = DBConnection()
        self.getAllProjects()

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

    def createInspiration(self):
        inspiration_form = InspirationForm()
        inspiration_id, name, cached_image_path, link, date_updated, tags = inspiration_form.inputInspiration()
        self.db.createInspiration(inspiration_id, name, cached_image_path, link, date_updated, tags)
    
    def editInspiration(self):
        inspiration_form = InspirationForm()
        inspiration_id, name, cached_image_path, link, date_updated, tags = inspiration_form.inputInspiration()
        self.db.editInspiration(inspiration_id, name, cached_image_path, link, date_updated, tags)

    def deleteInspiration(self, inspiration_id: int):
        self.db.deleteInspiration(inspiration_id)


if __name__=='__main__':
    import customtkinter as ctk
    root = ctk.CTk()
    inspiration = InspirationList(root)
    inspiration.showInspiration()
    root.mainloop()