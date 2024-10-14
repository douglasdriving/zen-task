import tkinter as tk
from .page import Page


class StartupPage(Page):

    instruction: tk.Label
    button: tk.Button

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

    def _setup_page(self):
        self.instruction = tk.Label(self)
        self.button = tk.Button(self)
        self.instruction.pack()
        self.button.pack()
        self._show_cleaning_prompt()

    def _show_cleaning_prompt(self):
        self._change_instrution(
            "Make sure your workspace is clean and organized.",
            "My workspace is clean",
            self._show_positioning_prompt,
        )

    def _show_positioning_prompt(self):
        self._change_instrution(
            "Sit in a comfortable position with your back straight.",
            "I'm sitting in a good position",
            self._show_breathing_prompt,
        )

    def _show_breathing_prompt(self):
        self._change_instrution(
            "Take 3 deep breaths and relax.",
            "I'm relaxed and ready",
            self._move_to_main_menu,
        )

    def _move_to_main_menu(self):
        self.controller.show_frame("MainMenu")

    def _change_instrution(self, instruction: str, button_text: str, command: callable):
        self.instruction.config(text=instruction)
        self.button.config(text=button_text, command=command)
