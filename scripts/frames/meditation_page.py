import tkinter as tk
import winsound


class MeditationPage(tk.Frame):

    parent: tk.Frame
    controller: object
    instructions: tk.Label
    time_label: tk.Label
    next_task_button: tk.Button
    return_button: tk.Button

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
        self._create_next_task_button()
        self._create_return_button()

    def start_meditation(self, time_in_seconds: int):
        self.instructions.config(
            text=f"close your eyes and breath. you are here and now"
        )
        self._start_timer(time_in_seconds)
        self._set_buttons_shown(False)

    def _start_timer(self, time_in_seconds: int):
        self.time_label.config(
            text=f"{time_in_seconds // 60:02}:{time_in_seconds % 60:02}"
        )

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
        self._set_buttons_shown(True)

    def _play_sound(self):
        frequency = 300
        duration = 700
        winsound.Beep(frequency, duration)

    def _set_buttons_shown(self, show: bool):
        if show:
            self.next_task_button.pack()
            self.return_button.pack()
        else:
            self.next_task_button.pack_forget()
            self.return_button.pack_forget()

    def _create_next_task_button(self):
        self.next_task_button = tk.Button(
            self,
            text="Next Task ->",
            command=lambda: self.controller.show_frame("ZenModePage"),
        )

    def _create_return_button(self):
        self.return_button = tk.Button(
            self,
            text="<- Main Menu",
            command=lambda: self.controller.show_frame("MainMenu"),
        )
