import sqlite3


class ProjectDbRetriever:

    db: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self):
        self.db = sqlite3.connect("tasks.db")
        self.cursor = self.db.cursor()

    def get_all_projects(self):
        self.cursor.execute("SELECT DISTINCT project FROM tasks WHERE done = 0")
        projects = self.cursor.fetchall()
        return [project[0] for project in projects]
