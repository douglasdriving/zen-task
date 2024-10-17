import tkinter as tk
import time
from ....db.task_retriever import TaskRetriever
from ....task.task import Task
from ....db.task_checker import TaskChecker
from ..meditation_page import MeditationPage
from .project_select_button_row import ProjectSelectButtonRow


class ZenModePage(tk.Frame):

    parent: tk.Frame
    controller: object
    task_description: tk.Label
    project_name: tk.Label
    task_definition_of_done: tk.Label
    task_detailed_steps: tk.Label
    next_task: Task
    task_checker: TaskChecker
    is_timer_running: bool
    time_task_started: float
    project_select_button_row: ProjectSelectButtonRow

    end_task_button: tk.Button

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.task_retriever = TaskRetriever()
        self.task_checker = TaskChecker()
        self._setup_page(controller)

    def on_show(self):
        self.project_select_button_row.update_project_list()
        self.load_next_task()

    def _setup_page(self, controller):
        self._add_return_button(controller)
        tk.Label(self, text="Zen Mode").pack(padx=10, pady=10)
        self.project_select_button_row = ProjectSelectButtonRow(
            self, controller, self.load_next_task
        )
        self.project_select_button_row.pack()
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
        projects = self.project_select_button_row.get_selected_projects()
        self.next_task: Task = self.task_retriever.get_next_task(projects)
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
        self.time_task_started = time.time()
        self.is_timer_running = True

    def _end_task(self):
        self.is_timer_running = False
        self.task_checker.set_task_as_done(self.next_task.id)
        meditation_page: MeditationPage = self.controller.show_frame("MeditationPage")
        time_spent_on_task = time.time() - self.time_task_started
        time_to_mediate = float(time_spent_on_task) / 10
        meditation_page.start_meditation(time_to_mediate)
        self.time_task_started = None
