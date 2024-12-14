import src.database.database as db
from src.project.project import Project


class ProjectController:
    def __init__(self):
        self.db = db.DBConnection()
        self.project_list = self.getAllProjects()

    def saveProject(self, project_list: list[Project], project: Project):
        name = project.getName()
        description = project.getDescription()
        status = project.getStatus()
        start_date = project.getStartDate()
        completion_date = project.getDeadline()
        budget = project.getBudget()

        if (project not in project_list):  # Create new
            # Cari id tertinggi dan tambah 1
            if (len(project_list) == 0):
                project.id = 1
            else:
                project.id = max(project_list, key=lambda
                                 project: project.id).id + 1
            index = len(project_list)
            project_list.append(project)

            # def createProject(self, name, description, status, start_date, completion_date, budget):
            self.db.createProject(name, description, status, start_date, completion_date, budget)

        else:
            index = project_list.index(project)
            project_list[index] = project
            self.db.editProject(project.getId(), name, description, status, start_date, completion_date, budget)

    def getAllProjects(self):
        result = self.db.getAllProjects()
        project_list = []
        for row in result:
            project = Project()
            project.id = row[0]
            project.name = row[1]
            project.description = row[2]
            project.status = int(row[3])
            project.start_date = row[4]
            project.deadline = row[5]
            project.budget = row[6]
            project_list.append(project)

        return project_list

    def getFilteredProjects(self, query, params):
        result = self.db.getFilteredProjects(query, params)
        project_list = []
        for row in result:
            project = Project()
            project.id = row[0]
            project.name = row[1]
            project.description = row[2]
            project.status = row[3]
            project.start_date = row[4]
            project.deadline = row[5]
            project.budget = row[6]
            project_list.append(project)

        return project_list

    def applyFilterController(self, query, params):
        self.project_list = self.getFilteredProjects(query, params)

    def resetFilter(self):
        self.project_list = self.getAllProjects()

    # def getProject(self, project: Project, filter):
    #     self.db.getProjects(project.getId())

    def deleteProject(self, project_list: list[Project], project: Project):
        index = project_list.index(project)
        del project_list[index]

        self.db.deleteProject(project.getId())
