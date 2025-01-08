import tkinter as tk
import time
from ....db.task_retriever import TaskRetriever
from ....task.task import Task
from .task_displayer import TaskDisplayer
from .pause_page import PausePage
from .low_score_task_confirmer import LowScoreTaskConfirmer
from ....db.task_deleter import TaskDeleter


class ZenModePage(tk.Frame):

    parent: tk.Frame
    controller: object
    is_timer_running: bool
    time_task_started: float
    task_retriever = TaskRetriever()
    task_displayer: TaskDisplayer = None
    next_task: Task = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self._add_back_button(controller)

    def _add_back_button(self, controller):
        back_button = tk.Button(
            self,
            text="← Back",
            command=lambda: controller.show_frame("MainMenu"),
            bg="light yellow",
        )
        back_button.pack(anchor="nw", padx=10, pady=10)

    def load_next_task(self, projects: list[str]):
        self._clear_task()
        self.next_task: Task = self.task_retriever.get_next_task(projects)
        if self.next_task is None:
            tk.Label(self, text="No tasks left!").pack(padx=10, pady=10)
        elif self.next_task.has_low_score():
            self._ask_about_low_score_task()
        else:
            self._start_task()

    def _ask_about_low_score_task(self):

        low_score_task_confirmer: LowScoreTaskConfirmer

        def on_confirm():
            self._start_task()
            low_score_task_confirmer.destroy()

        def on_delete():
            low_score_task_confirmer.destroy()
            task_deleter = TaskDeleter(self.next_task.id)
            task_deleter.delete_task()
            self.controller.show_frame("TaskPreparationPage")

        low_score_task_confirmer = LowScoreTaskConfirmer(
            self,
            self.controller,
            self.next_task,
            on_confirm,
            on_delete,
        )
        low_score_task_confirmer.pack(padx=10, pady=10)

    def _clear_task(self):
        if hasattr(self, "task_displayer") and self.task_displayer:
            self.task_displayer.destroy()

    def _start_task(self):
        self.task_displayer = TaskDisplayer(self, self.next_task, self._on_task_end)
        self.task_displayer.pack()
        self.time_task_started = time.time()
        self.is_timer_running = True

    def _on_task_end(self):
        self._clear_task()
        self.is_timer_running = False
        meditation_page: PausePage = self.controller.show_frame("PausePage")
        time_spent_on_task = time.time() - self.time_task_started
        time_to_mediate = float(time_spent_on_task) / 10
        meditation_page.begin_pause(time_to_mediate)
        self.time_task_started = None
