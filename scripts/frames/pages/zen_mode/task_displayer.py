import tkinter as tk
from ....task.task import Task
from ....db.task_checker import TaskChecker


class TaskDisplayer(tk.Frame):

    task_description: tk.Label
    project: tk.Label
    definition_of_done: tk.Label
    steps: tk.Label
    end_task: tk.Button
    task: Task
    task_checker = TaskChecker()
    on_task_end: callable

    def __init__(self, parent: tk.Frame, task: Task, on_task_end: callable):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.task = task
        self.on_task_end = on_task_end
        self._setup_frame()

    def _setup_frame(self):
        self._setup_project_label()
        self._setup_task_description()
        self._setup_definition_of_done()
        self._setup_steps_label()
        self._setup_steps_textbox()
        self._setup_end_task_button()

    def _setup_project_label(self):
        self.project = tk.Label(self, text=self.task.project, bg="pink", padx=5, pady=5)
        self.project.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def _setup_task_description(self):
        task_text = self.task.description
        self.task_description = tk.Label(
            self, text=task_text, font=("Helvetica", 10, "bold")
        )
        self.task_description.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    def _setup_definition_of_done(self):
        definition_of_done = tk.Label(
            self, text=("D.O.D: " + self.task.definition_of_done)
        )
        definition_of_done.grid(
            row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w"
        )

    def _setup_steps_label(self):
        steps_label = tk.Label(self, text="Break down:", anchor="w")
        steps_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    def _setup_steps_textbox(self):
        self.steps_textbox = tk.Text(self, height=10, width=50, padx=5, pady=5)
        self.steps_textbox.grid(row=4, column=0, columnspan=2, padx=10, sticky="w")

    def _setup_end_task_button(self):
        end_task = tk.Button(
            self,
            text="End Task",
            command=self._end_task,
            bg="green",
            fg="white",
            font=("Helvetica", 12, "bold"),
        )
        end_task.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky="e")

    def _end_task(self):
        self.task_checker.set_task_as_done(self.task.id)
        self.on_task_end()
