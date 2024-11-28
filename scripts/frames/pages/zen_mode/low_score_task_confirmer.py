import tkinter as tk
from ....task.task import Task


class LowScoreTaskConfirmer(tk.Frame):

    controller: object
    task: Task
    parent: tk.Frame

    def __init__(
        self,
        parent: tk.Frame,
        controller: object,
        task: Task,
        on_yes: callable,
        on_no: callable,
    ):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.task = task
        self._setup_frame(on_yes, on_no)

    def _setup_frame(self, on_yes: callable, on_no: callable):
        tk.Label(self, text="The following task has a low score:").pack(
            padx=10, pady=10
        )
        tk.Label(self, text=self.task.description).pack(padx=10, pady=10)
        tk.Label(self, text="Is is still in lign with your priorities?").pack(
            padx=10, pady=10
        )
        tk.Button(
            self,
            text="Yes, I still want to work on this",
            command=on_yes,
        ).pack(padx=10, pady=10)
        tk.Button(
            self,
            text="No, I want to skip this task",
            command=on_no,
        ).pack(padx=10, pady=10)
