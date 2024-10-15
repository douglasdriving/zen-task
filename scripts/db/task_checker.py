import sqlite3


class TaskChecker:
    """sets a task as done in db"""

    def __init__(self):
        self.db = sqlite3.connect("tasks.db")
        self.cursor = self.db.cursor()

    def set_task_as_done(self, task_id: int):
        self.cursor.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        self.db.commit()
