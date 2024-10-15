import tkinter as tk
from ....project_db_retriever import ProjectDbRetriever


class ProjectSelectButtonRow(tk.Frame):

    def __init__(self, parent, controller, project_select_command):
        tk.Frame.__init__(self, parent)
        retriever = ProjectDbRetriever()
        projects = retriever.get_all_projects()
        self.selected_project = tk.StringVar(
            value=""
        )  # Initialize with an empty string
        for project in projects:
            tk.Radiobutton(
                self,
                text=project,
                value=project,
                variable=self.selected_project,
                command=lambda p=project: project_select_command(p),
            ).pack()
