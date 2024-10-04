import tkinter as tk
from .frames.main_menu import MainMenu
from .frames.task_creation_page import TaskCreationPage
from .frames.zen_mode_page import ZenModePage

# from zen_mode_page import ZenModePage


class App:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Task App")
        self.container = tk.Frame(self.window)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (MainMenu, TaskCreationPage, ZenModePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        if page_name not in self.frames:
            raise ValueError(f"Invalid page name: {page_name}")
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    def run(self):
        self.window.mainloop()
