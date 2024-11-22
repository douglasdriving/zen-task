import tkinter as tk
from .annotated_slider import AnnotatedSlider


class TimeEstimateField(tk.Frame):

    controller: object

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def validate_positive_integer(value_if_allowed):
            if value_if_allowed.isdigit() and int(value_if_allowed) > 0:
                return True
            elif value_if_allowed == "":
                return True
            else:
                return False

        vcmd = (self.register(validate_positive_integer), "%P")
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)
        tk.Label(frame, text="Estimated time in minutes").pack(side=tk.LEFT, padx=10)
        entry = tk.Entry(frame, validate="key", validatecommand=vcmd)
        entry.pack(side=tk.LEFT, padx=10)
        self.time_estimate_field = entry
        self._add_focus_field(entry)
