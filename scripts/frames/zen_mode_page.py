import tkinter as tk
from ..task_retriever import TaskRetriever
from ..task import Task
from ..task_checker import TaskChecker
from .meditation_page import MeditationPage


class ZenModePage(tk.Frame):

    parent: tk.Frame
    controller: object
    task_description: tk.Label
    project_name: tk.Label
    task_definition_of_done: tk.Label
    task_detailed_steps: tk.Label
    next_task: Task
    task_checker: TaskChecker
    time_spent_on_current_task: int
    is_timer_running: bool

    end_task_button: tk.Button

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.task_retriever = TaskRetriever()
        self.task_checker = TaskChecker()
        self._setup_page(controller)

    def on_show(self):
        self.load_next_task()

    def _setup_page(self, controller):
        self._add_return_button(controller)
        tk.Label(self, text="Zen Mode").pack(padx=10, pady=10)
        self._add_task_info_fields()
        self.end_task_button = tk.Button(self, text="End Task", command=self._end_task)
        self.end_task_button.pack(padx=10, pady=10)

    def _add_return_button(self, controller):
        tk.Button(
            self,
            text="<- Back",
            command=lambda: controller.show_frame("MainMenu"),
        ).pack(padx=10, pady=10)

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
        self.next_task: Task = self.task_retriever.get_next_task()  # might return NONE
        if self.next_task is None:
            self.task_description.config(text="No tasks left")
            self.project_name.config(text="")
            self.task_definition_of_done.config(text="")
            self.task_detailed_steps.config(text="")
            self.end_task_button.config(state="disabled")
        else:
            self.task_description.config(text="Task: " + self.next_task.description)
            self.project_name.config(text="Project: " + self.next_task.project)
            self.task_definition_of_done.config(
                text="Definition of done: " + self.next_task.definition_of_done
            )
            self.task_detailed_steps.config(
                text="Steps: " + self.next_task.detailed_steps
            )
            self.end_task_button.config(state="normal")
            self._start_timer()

    def _start_timer(self):
        def update_timer():
            if self.is_timer_running:
                self.time_spent_on_current_task += 1
                self.after(1000, update_timer)

        self.is_timer_running = True
        self.time_spent_on_current_task = 0
        self.after(1000, update_timer)

    def _end_task(self):
        self.is_timer_running = False
        self.task_checker.set_task_as_done(self.next_task.id)
        meditation_page: MeditationPage = self.controller.show_frame("MeditationPage")
        meditation_page.start_meditation(float(self.time_spent_on_current_task) / 10)
