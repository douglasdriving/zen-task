import tkinter as tk
from tkinter import ttk
from .frames.main_menu import MainMenu
from .frames.task_creation_page import TaskCreationPage
from .frames.zen_mode_page import ZenModePage
from .frames.meditation_page import MeditationPage
from .frames.startup_page import StartupPage


class App:

    window: tk.Tk
    canvas: tk.Canvas
    scrollbar: ttk.Scrollbar
    scrollable_frame: ttk.Frame
    frames: dict[str, tk.Frame]

    def __init__(self):
        self._create_window()
        self._create_scrollable_canvas()
        self._add_frames()
        self.show_frame("StartupPage")

    def _add_frames(self):
        self.frames = {}
        for F in (MainMenu, TaskCreationPage, ZenModePage, MeditationPage, StartupPage):
            page_name = F.__name__
            frame = F(parent=self.scrollable_frame, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def _create_window(self):
        self.window = tk.Tk()
        self.window.title("ZenTask")

    def _create_scrollable_canvas(self):
        # Create a canvas and a vertical scrollbar
        self.canvas = tk.Canvas(self.window)
        self.scrollbar = ttk.Scrollbar(
            self.window, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def show_frame(self, page_name):
        if page_name not in self.frames:
            raise ValueError(f"Invalid page name: {page_name}")
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()
        return frame

    def run(self):
        self.window.mainloop()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
