import tkinter as tk
from .task_creation_page import TaskCreationPage
from .zen_mode.zen_mode_page import ZenModePage


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self._add_create_task_button(controller)
        self._add_zen_mode_button(controller)

    def _add_create_task_button(self, controller):
        create_task_button = tk.Button(
            self,
            text="Create Task",
            command=lambda: controller.show_frame(TaskCreationPage.__name__),
        )
        create_task_button.pack(padx=10, pady=10)

    def _add_zen_mode_button(self, controller):
        enter_zen_mode_button = tk.Button(
            self,
            text="Enter Zen Mode",
            command=lambda: controller.show_frame(ZenModePage.__name__),
        )
        enter_zen_mode_button.pack(padx=10, pady=10)
