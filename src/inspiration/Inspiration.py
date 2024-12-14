class Inspiration:
    def __init__(self):
        pass  

    def setInspirationId(self, inspiration_id: int):
        self.inspiration_id = inspiration_id

    def setName(self, name:str):
        self.name = name

    def setCachedImagePath(self, cached_image_path: str):
        self.cached_image_path = cached_image_path

    def setExternalLink(self, external_link: str):
        self.external_link = external_link
    
    def setTags(self, tags: list[str]):
        self.tags = tags
    
    def setDateUpdated(self, date_updated: str):
        self.date_updated = date_updated
    
    def getInspirationId(self) -> int:
        return self.inspiration_id

    def getName(self) -> str:
        return self.name
    
    def getCachedImagePath(self) -> str:
        return self.cached_image_path
    
    def getExternalLink(self) -> str:
        return self.external_link
    
    def getTags(self) -> list[str]:
        return self.tags
    
    def getDateUpdated(self) -> str:
        return self.date_updated