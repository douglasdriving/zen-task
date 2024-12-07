from .db_executer import DbExecuter


class TaskDeleter:

    db_executer = DbExecuter()

    def __init__(self, task_id: int):
        self.task_id = task_id

    def delete_task(self):
        query = "DELETE FROM tasks WHERE id = ?"
        params = [self.task_id]
        self.db_executer.execute_query(query, params)
        print(f"Task with id {self.task_id} deleted.")
