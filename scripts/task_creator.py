from .task import Task
from datetime import datetime


class TaskCreator:
    def __init__(self):
        pass

    def create_task(self):
        print("creating new task")
        description = self._ask_for_description()
        definition_of_done = self._ask_for_definition_of_done()
        detailed_steps = self._ask_for_detailed_steps()
        deadline = self._ask_for_deadline()
        project = self._ask_for_project()
        task = Task(description, definition_of_done, detailed_steps, project, deadline)
        return task

    def _ask_for_project(self):
        while True:
            print("write project name (at least 3 characters):")
            detailed_steps = input("")
            if len(detailed_steps) >= 5:
                return detailed_steps
            print("project name is too short. Please enter at least 3 characters.")

    def _ask_for_detailed_steps(self):
        while True:
            print("write detailed steps (at least 5 characters):")
            detailed_steps = input("")
            if len(detailed_steps) >= 5:
                return detailed_steps
            print("Detailed steps are too short. Please enter at least 5 characters.")

    def _ask_for_definition_of_done(self):
        while True:
            print("write the definition of done (at least 5 characters):")
            definition_of_done = input("")
            if len(definition_of_done) >= 5:
                return definition_of_done
            print(
                "Definition of done is too short. Please enter at least 5 characters."
            )

    def _ask_for_description(self):
        while True:
            print("describe the task briefly (at least 5 characters):")
            description = input("")
            if len(description) >= 5:
                return description
            print("Description is too short. Please enter at least 5 characters.")

    def _ask_for_deadline(self):
        while True:
            print(
                "write the deadline in the format YYYY-MM-DD. leave empty if no deadline"
            )
            deadline = input("")
            if deadline == "":
                return None
            try:
                deadline = datetime.strptime(deadline, "%Y-%m-%d")
                if deadline.date() < datetime.today().date():
                    print("The deadline must be today or a future date.")
                    continue
                return deadline
            except ValueError:
                print(
                    "Invalid date format. Please enter the date in the format YYYY-MM-DD."
                )
