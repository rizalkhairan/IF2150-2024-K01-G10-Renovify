import tkinter as tk
import src.database.database as db

class Task:
    def __init__(self, taskId, projectId, name, status, start_date, completion_date, description, budget):
        self.__taskId = taskId
        self.__projectId = projectId
        self.name = name
        self.status = status
        self.start_date = start_date
        self.completion_date = completion_date
        self.description = description
        self.budget = budget

    def getTaskId(self):
        return self.__taskId
    
    def getProjectId(self):
        return self.__projectId

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getStatus(self):
        return self.status

    def getStartDate(self):
        return self.start_date

    def getCompletionDate(self):
        return self.completion_date

    def getBudget(self):
        return self.budget

    def setId(self, newId):
        self.__taskId = newId

    def setName(self, newName):
        self.name = newName

    def setDescription(self, newDesc):
        self.description = newDesc

    def toggleStatus(self):
        self.status = not self.status

    def setStartDate(self, start):
        self.start_date = start

    def setDeadline(self, complete):
        self.completion_date = complete

    def setBudget(self, newBudget):
        self.budget = newBudget

class TaskController:
    def __init__(self):
        self.db = db.DBConnection()

    def saveTask(self, task_list: list[Task], task: Task):
        name = task.getName()
        description = task.getDescription()
        status = task.getStatus()
        start_date = task.getStartDate()
        completion_date = task.getCompletionDate()
        budget = task.getBudget()

        if(task not in task_list):
            if (len(task_list) == 0):
                task.__taskId = 1
            else:
                task.__taskId = max(task_list, key=lambda task: task.__taskId).__taskId, + 1
            index = len(task_list)
            task_list.append(task)

            # def createTask(self, name, description, status, start_date, completion_date, budget):
            self.db.createTask(name, description, status, start_date, completion_date, budget)

        else:
            index = task_list.index(task)
            task_list[index] = task
            self.db.editTask(task.getTaskId(), name, description, status, start_date, completion_date, budget)

    def deleteTask(self, task_list: list[Task], task: Task):
        index = task_list.index(task)
        del task_list[index]
        self.db.deleteTask(task.getTaskId())

