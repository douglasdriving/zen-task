import tkinter as tk


class SelectionRow(tk.Frame):
    def __init__(self, parent, controller, values: list):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self._add_radio_buttons(values)

    def _add_radio_buttons(self, values: list):
        radio_frame = tk.Frame(self)
        radio_frame.pack(padx=10)

        # Initialize the StringVar with an empty string to ensure no selection
        self.value_var = tk.StringVar(value=-1)

        for value in values:
            tk.Radiobutton(
                radio_frame, text=value, variable=self.value_var, value=value
            ).pack(side=tk.LEFT, padx=10)

    def get_selected_value(self):
        return self.value_var.get()
