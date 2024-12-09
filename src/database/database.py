import os
import sqlite3

class DBConnection:
    def __init__(self, db_name='user_data.db'):
        self.db_path = os.path.join('data', 'user', db_name)

        if os.path.exists(self.db_path):
            self.con = sqlite3.connect(self.db_path)
        else:
            print("Database not found, creating new database...")
            self.con = sqlite3.connect(self.db_path)

            # Inisialisasi tabel database
            projects_table = """
            CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR[100],
                description VARCHAR[1000],
                status VARCHAR[20],
                start_date TEXT,
                completion_date TEXT,
                budget REAL
            );
            """
            tasks_table = """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                name VARCHAR[100],
                description VARCHAR[1000],
                status VARCHAR[20],
                start_date TEXT,
                completion_date TEXT,
                budget REAL,
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            );
            """
            inspirations_table = """
            CREATE TABLE IF NOT EXISTS inspirations (
                inspiration_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                name VARCHAR[100],
                cached_image_path TEXT,
                link TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            );
            """
            budget_table = """
            CREATE TABLE IF NOT EXISTS budget (
                budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                description VARCHAR[1000],
                amount REAL,
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            );
            """
            cur = self.con.cursor()
            cur.execute(projects_table)
            cur.execute(tasks_table)
            cur.execute(inspirations_table)
            cur.execute(budget_table)
            self.con.commit()
            cur.close()
        
        pass
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.con.close()
    

    def getAllProjects(self):
        cur = self.con.execute("SELECT * FROM projects")
        result = cur.fetchall()
        cur.close()
        return result

    def getProjects(self, project_id):
        cur = self.con.execute("SELECT * FROM projects WHERE project_id=?", (project_id,))
        result = cur.fetchall()
        cur.close()
        return result

    def createProject(self, name, description, status, start_date, completion_date, budget):
        cur = self.con.execute("INSERT INTO projects (name, description, status, start_date, completion_date, budget) VALUES (?, ?, ?, ?, ?, ?)",
                                (name, description, status, start_date, completion_date, budget))
        self.con.commit()
        cur.close()
        return
    
    def editProject(self, project_id, name, description, status, start_date, completion_date, budget):
        cur = self.con.execute("UPDATE projects SET name=?, description=?, status=?, start_date=?, completion_date=?, budget=? WHERE project_id=?",
                                (name, description, status, start_date, completion_date, budget, project_id))
        self.con.commit()
        cur.close()
        return
    
    def deleteProject(self, project_id):
        cur = self.con.execute("DELETE FROM projects WHERE project_id=?", (project_id,))
        self.con.commit()
        cur.close()
        return
    

if __name__=='__main__':
    with DBConnection('tests.db') as db:
        db.createProject('Project 1', 'Description 1', 'Ongoing', '2021-01-01', '2021-12-31', 1000000)
        db.createProject('Project 3', 'Description 2', 'Ongoing', '2021-01-01', '2021-12-31', 2000000)
        c = db.con.cursor()
        for row in c.execute("SELECT * FROM projects"):
            print(row)
        db.con.commit()
        c.close()
