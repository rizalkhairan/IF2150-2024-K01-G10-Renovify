import os
import sqlite3

class DBConnection:
    """
        Layer koneksi database SQLite3. Handle koneksi database dan inisialisasi database.

        Validasi input dan pemrosesan data minimal. 
    """

    def __init__(self, db_name='user_data.db'):
        os.makedirs(os.path.join('data', 'user'), exist_ok=True)
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
                name VARCHAR[100],
                cached_image_path TEXT,
                link TEXT,
                date_updated VARCHAR[20]
            );
            """
            tags_table = """
            CREATE TABLE IF NOT EXISTS tags (
                tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                inspiration_id INTEGER,
                tag VARCHAR[20],
                FOREIGN KEY (inspiration_id) REFERENCES inspirations(inspiration_id)
            );
            """
            expenses_table = """
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            cur.execute(tags_table)
            cur.execute(expenses_table)
            self.con.commit()
            cur.close()
        
        pass
    
    # Context Manager. Menutup koneksi database ketika keluar dari with statement
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.con.close()
    

    """ Operasi CRUD Projects """
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

    """ Operasi CRUD Tasks """
    def getAllTasksOfProject(self, project_id):
        cur = self.con.execute("SELECT * FROM tasks WHERE project_id=?", (project_id,))
        result = cur.fetchall()
        cur.close()
        return result
    
    def getTask(self, task_id):
        cur = self.con.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,))
        result = cur.fetchall()
        cur.close()
        return result

    def createTask(self, project_id, name, description, status, start_date, completion_date, budget):
        cur = self.con.execute("INSERT INTO tasks (project_id, name, description, status, start_date, completion_date, budget) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (project_id, name, description, status, start_date, completion_date, budget))
        self.con.commit()
        cur.close()
        return

    def editTask(self, task_id, project_id, name, description, status, start_date, completion_date, budget):
        cur = self.con.execute("UPDATE tasks SET project_id=?, name=?, description=?, status=?, start_date=?, completion_date=?, budget=? WHERE task_id=?",
                                (project_id, name, description, status, start_date, completion_date, budget, task_id))
        self.con.commit()
        cur.close()
        return
    
    def deleteTask(self, task_id):
        cur = self.con.execute("DELETE FROM tasks WHERE task_id=?", (task_id,))
        self.con.commit()
        cur.close()
        return
    
    """ Operasi CRUD Inspirations """
    def getAllInspirations(self):
        cur = self.con.execute("SELECT * FROM inspirations")
        result = cur.fetchall()
        cur.close()
        return result
    
    def getInspirations(self, inspiration_id):
        cur = self.con.execute("SELECT * FROM inspirations WHERE inspiration_id=?", (inspiration_id,))
        result = cur.fetchall()
        cur.close()
        return result
    
    def createInspiration(self, name, cached_image_path, link, date_updated):
        cur = self.con.execute("INSERT INTO inspirations (name, cached_image_path, link, date_updated) VALUES (?, ?, ?, ?)",
                                (name, cached_image_path, link, date_updated))
        self.con.commit()
        cur.close()
        return
    
    def editInspiration(self, inspiration_id, name, cached_image_path, link, date_updated):
        cur = self.con.execute("UPDATE inspirations SET name=?, cached_image_path=?, link=?, date_updated=? WHERE inspiration_id=?",
                                (name, cached_image_path, link, date_updated, inspiration_id))
        self.con.commit()
        cur.close()
        return
    
    def deleteInspiration(self, inspiration_id):
        cur = self.con.execute("DELETE FROM inspirations WHERE inspiration_id=?", (inspiration_id,))
        self.con.commit()
        cur.close()
    
    """ Operasi CRUD Tags """
    def getAllTags(self, inspiration_id):
        cur = self.con.execute("SELECT tag FROM tags WHERE inspiration_id=?", (inspiration_id,))
        result = cur.fetchall()
        cur.close()
        tags = []
        for row in result:
            tags.append(row[0])
        return tags
    
    def createTag(self, inspiration_id, tag):
        cur = self.con.execute("INSERT INTO tags (inspiration_id, tag) VALUES (?, ?)", (inspiration_id, tag))
        self.con.commit()
        cur.close()
        return
    
    def deleteTag(self, inspiration_id, tag):
        cur = self.con.execute("DELETE FROM tags WHERE inspiration_id=? AND tag=?", (inspiration_id, tag))
        self.con.commit()
        cur.close()
        return

    """ Operasi CRUD Expenses """
    def getAllExpensesOfProject(self, project_id):
        cur = self.con.execute("SELECT * FROM expenses WHERE project_id=?", (project_id,))
        result = cur.fetchall()
        cur.close()
        return result
    
    def createExpense(self, project_id, description, amount):
        cur = self.con.execute("INSERT INTO expenses (project_id, description, amount) VALUES (?, ?, ?)",
                                (project_id, description, amount))
        self.con.commit()
        cur.close()
        return
    
    def editExpense(self, expense_id, project_id, description, amount):
        cur = self.con.execute("UPDATE expenses SET project_id=?, description=?, amount=? WHERE expense_id=?",
                                (project_id, description, amount, expense_id))
        self.con.commit()
        cur.close()
        return
    
    def deleteExpense(self, expense_id):
        cur = self.con.execute("DELETE FROM expenses WHERE expense_id=?", (expense_id,))
        self.con.commit()
        cur.close()
        return
    

if __name__=='__main__':
    with DBConnection('test.db') as db:
        db.createProject('Project 1', 'Description 1', 'Ongoing', '2021-01-01', '2021-12-31', 1000000)
        db.createProject('Project 3', 'Description 2', 'Ongoing', '2021-01-01', '2021-12-31', 2000000)
        c = db.con.cursor()
        for row in c.execute("SELECT * FROM projects"):
            print(row)
        db.con.commit()
        c.close()