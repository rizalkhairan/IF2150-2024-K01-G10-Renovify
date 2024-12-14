class Project:
    def __init__(self) -> None:
        self.id: int = None
        self.name: str = ""
        self.description: str = ""
        self.status: bool = 0       # done atau belum (true done false blum)
        self.start_date: str = ""
        self.deadline: str = ""
        self.budget: int = 0

    def __repr__(self):
        return f"Project ID: {self.id}\nName: {self.name}"

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getStatus(self):
        return self.status

    def getStartDate(self):
        return self.start_date

    def getDeadline(self):
        return self.deadline

    def getBudget(self):
        return self.budget

    def setId(self, newId):
        self.id = newId

    def setName(self, newName):
        self.name = newName

    def setDescription(self, newDesc):
        self.description = newDesc

    def toggleStatus(self):
        if (self.status == '0' or self.status == 0):
            self.status = 1
        elif (self.status == '1' or self.status == 1):
            self.status = 0

    def setStartDate(self, start):
        self.start_date = start

    def setDeadline(self, complete):
        self.deadline = complete

    def setBudget(self, newBudget):
        self.budget = newBudget
