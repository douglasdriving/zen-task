from datetime import datetime


class Task:

    id: int

    description: str
    definition_of_done: str
    detailed_steps: str
    deadline: datetime
    project: str

    value: int
    excitement: int
    estimated_time_in_minutes: int
    cognitive_load: int

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

    def rate(
        self,
        value: int,
        excitement: int,
        estimated_time_in_minutes: int,
        cognitive_load: int,
    ):
        self.value = value
        self.excitement = excitement
        self.estimated_time_in_minutes = estimated_time_in_minutes
        self.cognitive_load = cognitive_load

    def print_details_and_ratings(self):
        print("--------------------")
        self.print_details()
        self.print_ratings()
        print("--------------------")

    def print_details(self):
        print("Description: ", self.description)
        print("Definition of done: ", self.definition_of_done)
        print("Detailed steps: ", self.detailed_steps)
        print("Deadline: ", self.deadline)
        print("Project: ", self.project)

    def print_ratings(self):
        print("Value: ", self.value)
        print("Excitement: ", self.excitement)
        print("Estimated time in minutes: ", self.estimated_time_in_minutes)
        print("Cognitive load: ", self.cognitive_load)

    def calculate_score(self):
        time_score = self._calculate_time_score()
        score = self.value + self.excitement - time_score - self.cognitive_load
        return score

    def _calculate_time_score(self):
        time_score = 1
        if self.estimated_time_in_minutes > 5:
            time_score = 2
        if self.estimated_time_in_minutes > 15:
            time_score = 3
        if self.estimated_time_in_minutes > 45:
            time_score = 4
        if self.estimated_time_in_minutes > 120:
            time_score = 5
        return time_score
