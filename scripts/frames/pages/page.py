import tkinter as tk


class Page(tk.Frame):

    parent: tk.Frame
    controller: object

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self._setup_page()

    def _setup_page(self):
        print("Page setup not created for this page")
