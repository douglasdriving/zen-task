import tkinter as tk
from ....db.task_retriever import TaskRetriever
from ....task.task import Task


class DependenciesInputField(tk.Frame):

    parent: tk.Frame
    tasks_listed: dict[Task, tk.BooleanVar]
    dropdown_button: tk.Button
    dropdown_open: bool = False
    dropdown_window: tk.Frame
    projects: list[str]
    task_retriever: TaskRetriever

    def __init__(self, parent):
        # Add some margin above the initialization
        margin = tk.Frame(parent, height=10)
        margin.pack()

        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.dropdown_open = False
        self.task_retriever = TaskRetriever()
        self.projects = []
        self.tasks_listed = {}
        self._setup_field()

    def _setup_field(self):
        self.dropdown_button = tk.Button(
            self, text="Select Dependencies", command=self._toggle_dropdown
        )
        self.dropdown_button.pack()

    def update_projects(self, projects: list[str]):
        self.projects = projects
        if self.dropdown_open:
            self._reload_dropdown()

    def _reload_dropdown(self):
        self.tasks_listed = {}
        self.close_dropdown()
        self._open_dropdown()

    def _toggle_dropdown(self):
        if self.dropdown_open:
            self.close_dropdown()
        else:
            self._open_dropdown()

    def _open_dropdown(self):

        if self.dropdown_open:
            return

        self.dropdown_button.config(text="Close Dropdown")
        self.dropdown_open = True

        # Create a new window (simulates the dropdown)
        self.dropdown_window = tk.Frame(self, bg="lightgray", padx=10, pady=10)
        self.dropdown_window.pack(fill="both", expand=True)

        # fill dropdown with available tasks
        if len(self.projects) == 0:
            tk.Label(self.dropdown_window, text="no projects selected").pack(anchor="w")
        else:
            tasks_from_db: list[Task] = self.task_retriever.get_available_tasks(
                self.projects
            )
            if not tasks_from_db or len(tasks_from_db) == 0:
                tk.Label(
                    self.dropdown_window, text="no tasks in selected projects"
                ).pack(anchor="w")
            else:
                for task in self.tasks_listed:
                    checkbox = tk.Checkbutton(
                        self.dropdown_window,
                        text=task.description,
                        variable=self.tasks_listed[task],
                    )
                    checkbox.pack(anchor="w")
                for task in tasks_from_db:
                    if any(
                        t.description == task.description for t in self.tasks_listed
                    ):
                        continue
                    else:
                        var = tk.BooleanVar()
                        self.tasks_listed[task] = var
                        checkbox = tk.Checkbutton(
                            self.dropdown_window, text=task.description, variable=var
                        )
                        checkbox.pack(anchor="w")

    def close_dropdown(self):
        if self.dropdown_open:
            self.dropdown_button.config(text="Select Dependencies")
            self.dropdown_open = False
            self.dropdown_window.destroy()

    def get_selected_tasks(self) -> list[Task]:
        return [task for task, var in self.tasks_listed.items() if var.get()]
