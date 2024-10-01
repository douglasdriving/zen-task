from .task_creator import TaskCreator


class App:
    def __init__(self):
        pass

    def run(self):
        task_creator = TaskCreator()
        task = task_creator.create_task()
        print(task.__dict__)
