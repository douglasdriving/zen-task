import tkinter as tk
import winsound


class MeditationPage(tk.Frame):

    parent: tk.Frame
    controller: object
    instructions: tk.Label
    time_label: tk.Label

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self._setup_page()

    def _setup_page(self):
        self.instructions = tk.Label(self, text="...")
        self.time_label = tk.Label(self, text="00:00")
        self.instructions.pack()
        self.time_label.pack()

    def start_meditation(self, time_in_seconds: int):
        self.instructions.config(
            text=f"close your eyes and breath. you are here and now"
        )
        self._start_timer(time_in_seconds)

    def _start_timer(self, time_in_seconds: int):
        def update_timer():
            nonlocal time_in_seconds
            minutes, seconds = divmod(time_in_seconds, 60)
            self.time_label.config(text=f"{minutes:02}:{seconds:02}")
            if time_in_seconds > 0:
                time_in_seconds -= 1
                self.after(1000, update_timer)
            else:
                self._on_meditation_complete()

        update_timer()

    def _on_meditation_complete(self):
        self._play_sound()
        self.instructions.config(text="thank you for slowing down")
        self.time_label.pack_forget()
        self._add_next_task_button()
        self._add_return_button()

    def _play_sound(self):
        frequency = 300
        duration = 700
        winsound.Beep(frequency, duration)

    def _add_next_task_button(self):
        tk.Button(
            self,
            text="Next Task ->",
            command=lambda: self.controller.show_frame("ZenModePage"),
        ).pack(padx=10, pady=10)

    def _add_return_button(self):
        tk.Button(
            self,
            text="<- Main Menu",
            command=lambda: self.controller.show_frame("MainMenu"),
        ).pack(padx=10, pady=10)
