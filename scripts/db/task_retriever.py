import sqlite3
from ..task.task import Task
from datetime import datetime


class TaskRetriever:
    def __init__(self):
        pass

    def get_next_task(self, projects: list[str] = []):
        tasks = self.get_available_tasks(projects)
        if len(tasks) == 0:
            return None
        else:
            next_task = self._pick_best_task(tasks)
            return next_task

    def get_available_tasks(self, projects: list[str] = []):
        tasks_data = self._get_available_tasks_from_db(projects)
        tasks = self._make_tasks_from_data(tasks_data)
        return tasks

    def _get_available_tasks_from_db(self, projects: list[str] = []):
        placeholders = ", ".join(["?" for _ in projects])
        query = """
            SELECT t.*
            FROM tasks t
            LEFT JOIN task_dependencies td ON t.id = td.task_id
            LEFT JOIN tasks dep ON td.dependency_task_id = dep.id
            WHERE t.done = 0
            AND (t.waiting_for_date IS NULL OR t.waiting_for_date <= ?)
            AND t.project IN ({})
            GROUP BY t.id
            HAVING COUNT(CASE WHEN dep.done = 0 THEN 1 END) = 0
            """.format(
            placeholders
        )
        params = [datetime.now().timestamp()] + projects
        results = self._execute_query("tasks.db", query, params)
        return results

    def _execute_query(self, db_name: str, query: str, params: list):
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        db.close()
        return results

    def _make_tasks_from_data(self, tasks_data):
        tasks: list[Task] = []
        for task_data in tasks_data:
            task: Task = self._make_task_from_data(task_data)
            tasks.append(task)
        return tasks

    def _make_task_from_data(self, task_data):
        deadline = None
        if task_data[4] != None:
            deadline = datetime.fromtimestamp(task_data[4])
        waiting_until = None
        if task_data[11] != None:
            waiting_until = datetime.fromtimestamp(task_data[11])
        task = Task(
            description=task_data[1],
            detailed_steps=task_data[2],
            definition_of_done=task_data[3],
            deadline=deadline,
            waiting_until=waiting_until,
            project=task_data[5],
        )
        task.rate(
            value=task_data[6],
            excitement=task_data[7],
            estimated_time_in_minutes=task_data[8],
            cognitive_load=task_data[9],
        )
        task.id = task_data[0]
        return task

    def _pick_best_task(self, tasks: list[Task]):
        next_task: Task = tasks[0]
        for task in tasks:
            next_task = self._pick_best_of_two_tasks(task, next_task)
        return next_task

    def _pick_best_of_two_tasks(self, task_1: Task, task_2: Task):
        deadline_status_is_same = (
            task_1.is_deadline_today_or_earlier()
            == task_2.is_deadline_today_or_earlier()
        )
        if deadline_status_is_same:
            if task_1.calculate_score() > task_2.calculate_score():
                return task_1
            else:
                return task_2
        else:
            if task_1.is_deadline_today_or_earlier():
                return task_1
            else:
                return task_2
