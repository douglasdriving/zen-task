import tkinter as tk


class TaskCreationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Task Creation").pack(padx=10, pady=10)
        self._add_return_button(controller)

    def _add_return_button(self, controller):
        create_task_button = tk.Button(
            self,
            text="Return to Main Menu",
            command=lambda: controller.show_frame("MainMenu"),
        )
        create_task_button.pack(padx=10, pady=10)
