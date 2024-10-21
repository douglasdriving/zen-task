import tkinter as tk
from ....db.project_db_retriever import ProjectDbRetriever


class ProjectSelectButtonRow(tk.Frame):

    selected_projects: dict[str, tk.BooleanVar]
    project_select_command: callable
    project_retriever: ProjectDbRetriever

    def __init__(self, parent, controller, project_select_command):
        tk.Frame.__init__(self, parent)
        self.project_select_command = project_select_command
        self.project_retriever = ProjectDbRetriever()
        self.update_project_list()

    def update_project_list(self):
        projects = self.project_retriever.get_all_projects()

        if not hasattr(self, "selected_projects"):
            self.selected_projects = {}

        existing_projects = set(self.selected_projects.keys())

        for project in projects:
            if project not in existing_projects:
                var = tk.BooleanVar()
                self.selected_projects[project] = var
                tk.Checkbutton(
                    self,
                    text=project,
                    variable=var,
                    command=self.project_select_command,
                ).pack()

    def get_selected_projects(self):
        selected_projects = [
            project for project, var in self.selected_projects.items() if var.get()
        ]
        return selected_projects if selected_projects else []
