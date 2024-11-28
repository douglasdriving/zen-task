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
        task_description = tk.Label(self, text="Task: " + self.task.description)
        project = tk.Label(self, text="Project: " + self.task.project)
        definition_of_done = tk.Label(
            self, text="Definition of done: " + self.task.definition_of_done
        )
        steps = tk.Label(self, text="Steps: " + self.task.detailed_steps)
        end_task = tk.Button(self, text="End Task", command=self._end_task)
        task_description.pack(padx=10, pady=10)
        project.pack(padx=10, pady=10)
        definition_of_done.pack(padx=10, pady=10)
        steps.pack(padx=10, pady=10)
        end_task.pack(padx=10, pady=10)

    def _end_task(self):
        self.task_checker.set_task_as_done(self.task.id)
        self.on_task_end()
