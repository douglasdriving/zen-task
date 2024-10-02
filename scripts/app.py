from .task_creator import TaskCreator
from .task_rater import TaskRater
from .task import Task
from datetime import datetime


class App:

    def __init__(self):
        pass

    def run(self):

        # task_creator = TaskCreator()
        # task = task_creator.create_task()

        task = Task(
            "example task",
            "all the example criteria fulfilled",
            "1. example step 2. example step 3. example step",
            "example project",
            datetime(2024, 10, 6),
        )

        task_rater = TaskRater(task)
        rated_task = task_rater.ask_user_for_ratings()
