from .task import Task


class TaskRater:

    task: Task

    def __init__(self, task: Task):
        self.task = task

    def ask_user_for_ratings(self):
        print("--------------------")
        print("Please rate the following task: ")
        print("--------------------")
        self.task.print_details()
        self._ask_user_for_value()
        self._ask_user_for_excitement()
        self._ask_user_for_estimated_time_in_minutes()
        self._ask_user_for_cognitive_load()
        print("--------------------")
        print("Task rated:")
        self.task.print_details_and_ratings()
        return self.task

    def _ask_user_for_value(self):
        self.task.value = self._get_validated_input(
            "Please rate the value you would get from completing this task from 1-5.",
            "Value: ",
        )

    def _ask_user_for_excitement(self):
        self.task.excitement = self._get_validated_input(
            "Please rate the excitement you would get from completing this task from 1-5.",
            "Excitement: ",
        )

    def _ask_user_for_estimated_time_in_minutes(self):
        self.task.estimated_time_in_minutes = self._get_validated_input(
            "Please rate the estimated time you would need to complete this task from 1-5.",
            "Estimated time in minutes: ",
            1,
            500000000,
        )

    def _ask_user_for_cognitive_load(self):
        self.task.cognitive_load = self._get_validated_input(
            "Please rate the cognitive load you would experience from completing this task from 1-5.",
            "Cognitive load: ",
        )

    def _get_validated_input(
        self, prompt_message, input_message, min_value=1, max_value=5
    ):
        print("--------------------")
        print(prompt_message)
        while True:
            try:
                value = int(input(input_message))
                if min_value <= value <= max_value:
                    return value
                else:
                    print("Value must be betwee", min_value, "and", max_value)
            except ValueError:
                print("Value must be an integer")
