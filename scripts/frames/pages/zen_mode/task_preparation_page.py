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
        self._add_label()
        self._add_project_select_button_row()
        self._add_start_task_button()

    def _add_label(self):
        tk.Label(self, text="What projects do you want to work on?").pack(
            anchor="w", padx=10
        )

    def _add_project_select_button_row(self):
        self.project_select_button_row = ProjectSelectButtonRow(
            self, self.controller, None
        )
        self.project_select_button_row.pack(anchor="w", padx=10)

    def _add_start_task_button(self):
        tk.Button(
            self,
            text="Next Task →",
            command=lambda: self._go_to_zen_mode_page(),
            bg="light green",
        ).pack(anchor="w", padx=10, pady=10)

    def on_show(self):
        self.project_select_button_row.update_project_list()

    def _go_to_zen_mode_page(self):
        zen_mode_page: ZenModePage = self.controller.show_frame(ZenModePage.__name__)
        projects = self.project_select_button_row.get_selected_projects()
        zen_mode_page.load_next_task(projects)

    def _add_return_button(self):
        return_button = tk.Button(
            self,
            text="← Back",
            command=lambda: self.controller.show_frame("MainMenu"),
            bg="light yellow",
        )
        return_button.pack(anchor="nw", padx=10, pady=10)
