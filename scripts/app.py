from .task_creator import TaskCreator
from .task_rater import TaskRater
from .task import Task
from .task_db_adder import TaskDbAdder
from datetime import datetime


class App:

    def __init__(self):
        pass

    def run(self):

        print("App starting.")

        # task_creator = TaskCreator()
        # task = task_creator.create_task()

        exampleTask = Task(
            "example task",
            "all the example criteria fulfilled",
            "1. example step 2. example step 3. example step",
            "example project",
            datetime(2024, 10, 6),
        )

        # task_rater = TaskRater(task)
        # rated_task = task_rater.ask_user_for_ratings()

        exampleTask.value = 2
        exampleTask.excitement = 3
        exampleTask.estimated_time_in_minutes = 25
        exampleTask.cognitive_load = 2

        task_db_adder = TaskDbAdder()
        task_db_adder.add_task(exampleTask)

        print("App closed.")
