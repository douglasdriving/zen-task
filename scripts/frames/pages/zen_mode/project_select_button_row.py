import tkinter as tk
from ....db.project_db_retriever import ProjectDbRetriever


class ProjectSelectButtonRow(tk.Frame):

    def __init__(self, parent, controller, project_select_command):
        tk.Frame.__init__(self, parent)
        retriever = ProjectDbRetriever()
        projects = retriever.get_all_projects()
        self.selected_project = tk.StringVar(
            value=""
        )  # Initialize with an empty string

        # Add the "all" projects radio button
        tk.Radiobutton(
            self,
            text="All",
            value="all",
            variable=self.selected_project,
            command=lambda: project_select_command(None),
        ).pack()

        for project in projects:
            tk.Radiobutton(
                self,
                text=project,
                value=project,
                variable=self.selected_project,
                command=lambda p=project: project_select_command(p),
            ).pack()

        # Set the "all" projects button as the default selected button
        self.selected_project.set("all")
