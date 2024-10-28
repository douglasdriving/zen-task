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

        self.bind("<FocusIn>", lambda e: self._on_focus())
        self.bind("<FocusOut>", lambda e: self._on_focus_lost())

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

        def _set_open():
            self.dropdown_button.config(text="Close Dropdown")
            self.dropdown_open = True

        def _create_window():
            self.dropdown_window = tk.Frame(self, bg="lightgray", padx=10, pady=10)
            self.dropdown_window.pack(fill="both", expand=True)

        def _add_content():

            def _add_message(message: str):
                tk.Label(self.dropdown_window, text=message).pack(anchor="w")

            def _populate(tasks_from_db):

                checkbuttons: list[tk.Checkbutton] = []
                highlight_index = 0

                def _populate_with_listed_tasks():
                    for task in self.tasks_listed:
                        checkbutton = tk.Checkbutton(
                            self.dropdown_window,
                            text=task.description,
                            variable=self.tasks_listed[task],
                        )
                        checkbutton.pack(anchor="w")
                        checkbuttons.append(checkbutton)

                def _populate_with_new_tasks(tasks: list[Task]):
                    for task in tasks:
                        if any(
                            t.description == task.description for t in self.tasks_listed
                        ):
                            continue
                        else:
                            var = tk.BooleanVar()
                            self.tasks_listed[task] = var
                            checkbox = tk.Checkbutton(
                                self.dropdown_window,
                                text=task.description,
                                variable=var,
                            )
                            checkbox.pack(anchor="w")

                def _change_highlight_index(change: int = 1):
                    nonlocal highlight_index
                    checkbuttons[highlight_index].config(bg="white")
                    highlight_index += change
                    if highlight_index >= len(checkbuttons):
                        highlight_index = 0
                    elif highlight_index < 0:
                        highlight_index = len(checkbuttons) - 1
                    checkbuttons[highlight_index].config(bg="lightblue")

                _populate_with_listed_tasks()
                _populate_with_new_tasks(tasks_from_db)
                if checkbuttons and len(checkbuttons) > 0:
                    checkbuttons[0].config(bg="lightblue")
                    # allow you to navigate with the arrow keys (should be able to not choose anything)
                    self.bind("<Down>", lambda e: _change_highlight_index(1))
                    self.bind("<Up>", lambda e: _change_highlight_index(-1))
                    # allow you to select with the enter key (which checks the box of the currently highlighted task)
                    self.bind(
                        "<Return>", lambda e: checkbuttons[highlight_index].invoke()
                    )

            no_project_selected = len(self.projects) == 0
            if no_project_selected:
                _add_message("no projects selected")
            else:
                tasks_from_db: list[Task] = self.task_retriever.get_available_tasks(
                    self.projects
                )
                no_tasks = not tasks_from_db or len(tasks_from_db) == 0
                if no_tasks:
                    _add_message("no tasks in selected projects")
                else:
                    _populate(tasks_from_db)

        if not self.dropdown_open:
            _set_open()
            _create_window()
            _add_content()

    def close_dropdown(self):
        if self.dropdown_open:
            self.dropdown_button.config(text="Select Dependencies")
            self.dropdown_open = False
            self.dropdown_window.destroy()

    def get_selected_tasks(self) -> list[Task]:
        return [task for task, var in self.tasks_listed.items() if var.get()]

    def _on_focus(self):
        self.dropdown_button.config(bg="yellow")
        self.bind("<Return>", lambda e: self._toggle_dropdown())

    def _on_focus_lost(self):
        self.dropdown_button.config(bg="white")
        self.unbind("<Return>")
