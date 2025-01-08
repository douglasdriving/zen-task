import tkinter as tk
import winsound
import random


class PausePage(tk.Frame):

    parent: tk.Frame
    controller: object
    instructions: tk.Label
    time_label: tk.Label
    next_task_button: tk.Button
    return_button: tk.Button
    break_prompts = [
        "close your eyes and take 3 deep breaths",
        "focus far into the distance for 20 seconds",
        "stretch your arms and shoulders",
        "relax all muscles in your body",
        "stretch your neck",
        "drink some water",
        "arch and round your back (cat-cow stretch) 3 times while seated",
        "roll your wrists and ankles",
        "shake your hands and legs",
        "imagine a peaceful place, be there for a moment",
        "close your eyes and massage your temples",
        "write down a positive thing about your day",
        "do a 1 minute mindfullness meditation",
        "stand up and walk around a few steps",
        "doodle something on a piece of paper",
        "write down 1 thing that you are feeling right now",
    ]

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

    def begin_pause(self, time_in_seconds: float):
        if time_in_seconds < 10:
            time_in_seconds = 10
        self._show_random_break_prompt()
        self._start_timer(time_in_seconds)
        self._set_buttons_shown(False)

    def _show_random_break_prompt(self):
        prompt = random.choice(self.break_prompts)
        self.instructions.config(text=prompt)

    def _start_timer(self, time_in_seconds: float):
        time_in_seconds = int(time_in_seconds)
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
                self._on_pause_complete()

        update_timer()

    def _on_pause_complete(self):
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
            command=lambda: self.controller.show_frame("TaskPreparationPage"),
        )

    def _create_return_button(self):
        self.return_button = tk.Button(
            self,
            text="<- Main Menu",
            command=lambda: self.controller.show_frame("MainMenu"),
        )
