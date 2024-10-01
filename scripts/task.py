from datetime import datetime


class Task:

    def __init__(
        self,
        description: str,
        definition_of_done: str,
        detailed_steps: str,
        project: str,
        deadline: datetime = None,
    ):
        self.description = description
        self.definition_of_done = definition_of_done
        self.detailed_steps = detailed_steps
        self.deadline = deadline
        self.project = project
