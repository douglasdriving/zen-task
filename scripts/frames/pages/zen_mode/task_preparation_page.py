import tkinter as tk
from ..page import Page
from .project_select_button_row import ProjectSelectButtonRow
from .zen_mode_page import ZenModePage


class TaskPreparationPage(Page):

    project_select_button_row: ProjectSelectButtonRow

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

    def _setup_page(self):
        self._add_return_button()
        tk.Label(self, text="What projects do you want to work on?").pack()
        self.project_select_button_row = ProjectSelectButtonRow(
            self, self.controller, None
        )
        self.project_select_button_row.pack()
        tk.Button(
            self,
            text="Start next task",
            command=lambda: self._go_to_zen_mode_page(),
        ).pack()

    def on_show(self):
        self.project_select_button_row.update_project_list()

    def _go_to_zen_mode_page(self):
        zen_mode_page: ZenModePage = self.controller.show_frame(ZenModePage.__name__)
        projects = self.project_select_button_row.get_selected_projects()
        zen_mode_page.load_next_task(projects)

    def _add_return_button(self):
        tk.Button(
            self,
            text="<- Back",
            command=lambda: self.controller.show_frame("MainMenu"),
        ).pack(padx=10, pady=10)
