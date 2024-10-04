import tkinter as tk
from tkinter import messagebox  # Import messagebox
import tkcalendar as tkc
from .selection_row import SelectionRow
from ..task import Task
from datetime import datetime
from ..task_db_adder import TaskDbAdder


class TaskCreationPage(tk.Frame):

    def __init__(self, parent, controller):
        self.task_db_adder = TaskDbAdder()
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self._add_return_button()
        tk.Label(self, text="Task Creation").pack(padx=10, pady=10)

        self.text_fields: list[tk.Entry] = {}
        self.selection_fields: list[SelectionRow] = {}

        self._add_labeled_text_field("description", "Description")
        self._add_labeled_text_field("dod", "Definition of done")
        self._add_labeled_text_field("steps", "Detailed steps")
        self._add_deadline_field()
        self._add_labeled_text_field("project", "Project")
        self._add_labeled_selection_row(
            "value",
            "How valuable would it be to complete this task?",
            [1, 2, 3, 4, 5],
        )
        self._add_labeled_selection_row(
            "excitement",
            "How excited are you about working on this?",
            [1, 2, 3, 4, 5],
        )
        self._add_time_estimate_field()
        self._add_labeled_selection_row(
            "effort",
            "How much effort do you think this task will require?",
            [1, 2, 3, 4, 5],
        )
        tk.Button(self, text="Add", command=self._add_task).pack(padx=10, pady=10)

    def _add_deadline_field(self):
        tk.Label(self, text="Deadline").pack(padx=10)
        self.deadline_entry_field = tkc.Calendar(self)
        self.deadline_entry_field.pack(padx=10)

    def _add_labeled_selection_row(self, label: str, message: str, values: list):
        tk.Label(self, text=message).pack(padx=10)
        selectionRow = SelectionRow(
            self,
            self.controller,
            values,
        )
        self.selection_fields[label] = selectionRow
        selectionRow.pack(padx=10)

    def _add_labeled_text_field(self, label: str, message: str):
        tk.Label(self, text=message).pack(padx=10)
        entryField = tk.Entry(self)
        entryField.pack(padx=10)
        self.text_fields[label] = entryField

    def _add_return_button(self):
        tk.Button(
            self,
            text="<- Return",
            command=lambda: self.controller.show_frame("MainMenu"),
        ).pack(padx=10, pady=10)

    def _add_time_estimate_field(self):
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

    def _add_task(self):

        deadline = self.deadline_entry_field.get_date()
        deadline_datetime = datetime.strptime(deadline, "%m/%d/%y")

        task = Task(
            description=self.text_fields["description"].get(),
            definition_of_done=self.text_fields["dod"].get(),
            detailed_steps=self.text_fields["steps"].get(),
            project=self.text_fields["project"].get(),
            deadline=deadline_datetime,
        )

        task.rate(
            value=self.selection_fields["value"].get_selected_value(),
            excitement=self.selection_fields["excitement"].get_selected_value(),
            estimated_time_in_minutes=self.time_estimate_field.get(),
            cognitive_load=self.selection_fields["effort"].get_selected_value(),
        )

        self.task_db_adder.add_task(task)
        self._clean_values()

    def _clean_values(self):
        for entry in self.text_fields.values():
            entry.delete(0, tk.END)
        self.deadline_entry_field._remove_selection()
        self.time_estimate_field.delete(0, tk.END)
        for selection in self.selection_fields.values():
            selection.value_var.set(-1)
        messagebox.showinfo("Task added", "Task added successfully")
