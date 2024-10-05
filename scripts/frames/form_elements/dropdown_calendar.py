import tkinter as tk
import tkcalendar as tkc
import datetime


class DropDownCalendar(tk.Frame):

    parent: object
    controller: object
    is_open: tk.BooleanVar
    checkbox: tk.Checkbutton
    calendar: tkc.Calendar

    def __init__(self, parent, controller, checkbox_label: str):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.checkbox_label = checkbox_label
        self.is_open = tk.BooleanVar(value=False)
        self._add_checkbox(checkbox_label)
        self._add_calendar()

    def reset(self):
        self.is_open.set(False)
        self._remove_calendar()

    def get_date(self):
        has_date = self.is_open.get() and self.calendar.get_date()
        if has_date:
            deadline = self.calendar.get_date()
            deadline_datetime = datetime.datetime.strptime(deadline, "%m/%d/%y")
            return deadline_datetime
        else:
            return None

    def _add_checkbox(self, label: str):
        self.checkbox = tk.Checkbutton(
            self,
            text=label,
            variable=self.is_open,
            command=self._toggle_calendar,
        )
        self.checkbox.pack()

    def _toggle_calendar(self):
        if self.is_open.get():
            self._add_calendar()
        else:
            self._remove_calendar()

    def _add_calendar(self):
        self.calendar = tkc.Calendar(self)
        self.calendar.pack()

    def _remove_calendar(self):
        self.calendar.pack_forget()
        self.calendar.destroy()
