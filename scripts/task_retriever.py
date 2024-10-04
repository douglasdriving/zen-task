import sqlite3
from .task import Task
from datetime import datetime


class TaskRetriever:
    def __init__(self):
        pass

    def get_next_task(self):
        tasks = self._get_all_tasks()
        next_task = self._pick_best_task(tasks)
        return next_task

    def _get_all_tasks(self):
        tasks_data = self._get_all_task_data_from_db()
        tasks = self._make_tasks_from_data(tasks_data)
        return tasks

    def _make_tasks_from_data(self, tasks_data):
        tasks: list[Task] = []
        for task_data in tasks_data:
            task = Task(
                description=task_data[1],
                detailed_steps=task_data[2],
                definition_of_done=task_data[3],
                deadline=datetime.fromtimestamp(task_data[4]),
                project=task_data[5],
            )
            task.rate(
                value=task_data[6],
                excitement=task_data[7],
                estimated_time_in_minutes=task_data[8],
                cognitive_load=task_data[9],
            )
            tasks.append(task)
        return tasks

    def _get_all_task_data_from_db(self):
        db = sqlite3.connect("tasks.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks_data = cursor.fetchall()
        db.close()
        return tasks_data

    def _pick_best_task(self, tasks: list[Task]):
        next_task: Task = tasks[0]
        best_score = next_task.calculate_score()
        for task in tasks:
            if task.calculate_score() > best_score:
                next_task = task
                best_score = task.calculate_score()
        return next_task