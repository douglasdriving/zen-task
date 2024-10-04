import tkinter as tk
from ..task_retriever import TaskRetriever
from ..task import Task


class ZenModePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Zen Mode").pack(padx=10, pady=10)
        self._add_return_button(controller)
        self.task_retriever = TaskRetriever()
        next_task: Task = self.task_retriever.get_next_task()

    def _add_return_button(self, controller):
        create_task_button = tk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame("MainMenu"),
        )
        create_task_button.pack(padx=10, pady=10)
