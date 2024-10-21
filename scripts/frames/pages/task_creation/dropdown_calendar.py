import tkinter as tk
import tkcalendar as tkc
import datetime


class DropDownCalendar(tk.Frame):

    parent: tk.Frame
    checkbox_label: str
    is_open: tk.BooleanVar
    calendar: tkc.Calendar
    checkbox: tk.Checkbutton

    def __init__(self, parent, controller, checkbox_label: str):
        tk.Frame.__init__(self, parent, takefocus=True)
        self.parent = parent
        self.controller = controller
        self.checkbox_label = checkbox_label
        self.is_open = tk.BooleanVar(value=False)
        self._add_checkbox(checkbox_label)
        self._add_calendar()
        self.bind("<FocusIn>", self._on_focus)
        self.bind("<FocusOut>", self._on_focus_out)

    def _on_focus(self, event):
        print("CALENDAR IS FOCUSed")
        self.checkbox.config(bg="yellow")
        self.bind("<Return>", lambda e: self._toggle_checkbox_and_calendar())
        self.bind("<Left>", lambda e: self._shift_day(-1))
        self.bind("<Right>", lambda e: self._shift_day(1))
        self.bind("<Up>", lambda e: self._shift_day(-7))
        self.bind("<Down>", lambda e: self._shift_day(7))

    def _on_focus_out(self, event):
        print("CALENDAR IS NOT FOCUSed")
        self.checkbox.config(bg="white")

    def _shift_day(self, days_to_shift: int):
        selected_date = self.calendar.selection_get()
        if selected_date:
            new_date = selected_date + datetime.timedelta(days=days_to_shift)
            self.calendar.selection_set(new_date)

    def _toggle_checkbox_and_calendar(self):
        self.is_open.set(not self.is_open.get())
        self._toggle_calendar()

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
