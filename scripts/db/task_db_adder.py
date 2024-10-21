import sqlite3
from ..task.task import Task


class TaskDbAdder:
    """Add tasks to the database"""

    db = None
    cursor = None

    def __init__(self):
        self._initialize_db()
        pass

    def _initialize_db(self):
        self.db = sqlite3.connect("tasks.db")
        self.cursor = self.db.cursor()
        self._create_tasks_table_if_not_exists()
        self.db.commit()

    def _create_tasks_table_if_not_exists(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                description TEXT NOT NULL,
                detailed_steps TEXT NOT NULL,
                definition_of_done TEXT NOT NULL,
                deadline INTEGER,
                waiting_for_date INTEGER,
                project TEXT NOT NULL,
                value INTEGER NOT NULL,
                excitement INTEGER NOT NULL,
                estimated_time_in_minutes INTEGER NOT NULL,
                cognitive_load INTEGER NOT NULL
            )
            """
        )
        self.db.commit()

    def add_task(self, task: Task):
        task_id = self._add_task(task)
        task.id = task_id
        self.add_task_dependencies(task)

    def _add_task(self, task):
        self.cursor.execute(
            """
            INSERT INTO tasks (
                description,
                definition_of_done,
                detailed_steps,
                deadline,
                waiting_for_date,
                project,
                value,
                excitement,
                estimated_time_in_minutes,
                cognitive_load
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task.description,
                task.definition_of_done,
                task.detailed_steps,
                task.get_deadline_as_int_or_none(),
                task.get_waiting_for_date_as_int_or_none(),
                task.project,
                task.value,
                task.excitement,
                task.estimated_time_in_minutes,
                task.cognitive_load,
            ),
        )
        self.db.commit()
        task_id = self.cursor.lastrowid
        return task_id

    def add_task_dependencies(self, task: Task):
        for dependency in task.dependencies:
            self.cursor.execute(
                """
                INSERT INTO task_dependencies (task_id, dependency_task_id)
                VALUES (?, ?)
                """,
                (task.id, dependency.id),
            )
        self.db.commit()
