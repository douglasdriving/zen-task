from datetime import datetime


class Task:

    id: int

    description: str
    definition_of_done: str
    detailed_steps: str
    deadline: datetime
    waiting_for_date: datetime
    project: str
    dependencies: list["Task"]

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
        waiting_until: datetime = None,
        dependencies: list["Task"] = [],
    ):
        self.description = description
        self.definition_of_done = definition_of_done
        self.detailed_steps = detailed_steps
        self.deadline = deadline
        self.project = project
        self.waiting_for_date = waiting_until
        self.dependencies = dependencies

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
        print("Waiting until: ", self.waiting_for_date)
        print("Project: ", self.project)

    def print_ratings(self):
        print("Value: ", self.value)
        print("Excitement: ", self.excitement)
        print("Estimated time in minutes: ", self.estimated_time_in_minutes)
        print("Cognitive load: ", self.cognitive_load)

    def calculate_score(self):
        value_multiplier = self.value
        excitement_multiplier = self.excitement
        time_multiplier = 1 / self.estimated_time_in_minutes
        effort_multiplier = 1 / self.cognitive_load
        if datetime.now().hour > 13:  # in the afternoon, focus on lighter tasks
            effort_multiplier = 1 / self.cognitive_load
        score = (
            value_multiplier
            * excitement_multiplier
            * time_multiplier
            * effort_multiplier
        )
        return score

    def get_deadline_as_int_or_none(self):
        return self._get_date_as_int_or_none(self.deadline)

    def get_waiting_for_date_as_int_or_none(self):
        return self._get_date_as_int_or_none(self.waiting_for_date)

    def _get_date_as_int_or_none(self, datetime: datetime):
        timestamp: int = None
        if datetime:
            timestamp = int(datetime.timestamp())
        return timestamp

    def is_deadline_today_or_earlier(self):
        if not self.deadline:
            return False
        else:
            return self.deadline.date() <= datetime.now().date()
