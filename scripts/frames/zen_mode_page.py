import tkinter as tk
from ..task_retriever import TaskRetriever
from ..task import Task


class ZenModePage(tk.Frame):

    task_description: tk.Label
    project_name: tk.Label
    task_definition_of_done: tk.Label
    task_detailed_steps: tk.Label
    next_task: Task

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.task_retriever = TaskRetriever()
        self._setup_page(controller)

    def on_show(self):
        self.load_next_task()

    def _setup_page(self, controller):
        self._add_return_button(controller)
        tk.Label(self, text="Zen Mode").pack(padx=10, pady=10)
        self._add_task_info_fields()
        tk.Button(self, text="End Task", command=self._end_task).pack(padx=10, pady=10)

    def _add_return_button(self, controller):
        button = tk.Button(
            self,
            text="<- Back",
            command=lambda: controller.show_frame("MainMenu"),
        )
        button.pack(padx=10, pady=10)

    def _add_task_info_fields(self):
        self.project_name = tk.Label(self, text="Project: ...")
        self.project_name.pack(padx=10, pady=10)
        self.task_description = tk.Label(self, text="Task: ...")
        self.task_description.pack(padx=10, pady=10)
        self.task_definition_of_done = tk.Label(self, text="Definition of done: ...")
        self.task_definition_of_done.pack(padx=10, pady=10)
        self.task_detailed_steps = tk.Label(self, text="Steps: ...")
        self.task_detailed_steps.pack(padx=10, pady=10)

    def load_next_task(self):
        self.next_task: Task = self.task_retriever.get_next_task()
        self.task_description.config(text="Task: " + self.next_task.description)
        self.project_name.config(text="Project: " + self.next_task.project)
        self.task_definition_of_done.config(
            text="Definition of done: " + self.next_task.definition_of_done
        )
        self.task_detailed_steps.config(text="Steps: " + self.next_task.detailed_steps)

    def _end_task(self):
        print("Task ended. NOT IMPLEMENTED YET")
