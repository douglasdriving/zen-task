import tkinter as tk
from ....db.project_db_retriever import ProjectDbRetriever


class ProjectSelectButtonRow(tk.Frame):

    def __init__(self, parent, controller, project_select_command):
        tk.Frame.__init__(self, parent)
        retriever = ProjectDbRetriever()
        projects = retriever.get_all_projects()
        self.selected_projects = {}

        def update_selected_projects():
            selected = [
                project for project, var in self.selected_projects.items() if var.get()
            ]
            project_select_command(selected)

        for project in projects:
            var = tk.BooleanVar()
            self.selected_projects[project] = var
            tk.Checkbutton(
                self,
                text=project,
                variable=var,
                command=update_selected_projects,
            ).pack()
