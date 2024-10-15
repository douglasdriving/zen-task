import tkinter as tk
from ..form_elements.annotated_slider import AnnotatedSlider
from ...task import Task
from ...task_db_adder import TaskDbAdder
from ..form_elements.dropdown_calendar import DropDownCalendar
from ...project_db_retriever import ProjectDbRetriever
from ..form_elements.entry_with_dropdown import DropdownEntry


class TaskCreationPage(tk.Frame):

    parent: object
    controller: object
    text_fields: dict[str, tk.Text]
    sliders: dict[str, AnnotatedSlider]
    calendars: dict[str, DropDownCalendar]
    project_entry: DropdownEntry
    bottom_message: tk.Label
    time_estimate_field: tk.Entry
    task_db_adder: TaskDbAdder

    def __init__(self, parent, controller):
        self.task_db_adder = TaskDbAdder()
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.text_fields = {}
        self.sliders = {}
        self.calendars = {}
        self._add_page_content()

    def _add_page_content(self):
        self._add_return_button()
        tk.Label(self, text="Task Creation").pack(padx=10, pady=10)
        self._add_input_fields()
        tk.Button(self, text="Add", command=self._add_task).pack(padx=10, pady=10)
        self._add_bottom_message_label()
        self._clean_values()

    def _add_bottom_message_label(self):
        self.bottom_message = tk.Label(self, text="")
        self.bottom_message.pack(padx=10, pady=10)

    def _add_input_fields(self):
        self._add_labeled_text_field("description", "Description", 2)
        self._add_labeled_text_field("dod", "Definition of done", 2)
        self._add_labeled_text_field("steps", "Detailed steps", 5)
        self._add_calendar_field("deadline")
        self._add_calendar_field("waiting for date")
        self._add_project_field()
        self._add_value_slider()
        self._add_excitement_slider()
        self._add_time_estimate_field()
        self._add_effort_slider()

    def _add_project_field(self):
        tk.Label(self, text="Project").pack()
        project_retriever = ProjectDbRetriever()
        projects = project_retriever.get_all_projects()
        self.project_entry = dropdown_entry = DropdownEntry(self, projects)
        dropdown_entry.pack()

    def _add_effort_slider(self):
        self._add_labeled_slider(
            "effort",
            "How much effort do you think this task will require?",
            [1, 2, 3, 4, 5],
            [
                "trivial, i know exactly what to do",
                "easy, i know what to do",
                "medium, it will require a bit of thinking",
                "hard, i will need to focus",
                "very hard, i will need a lot of mental energy",
            ],
        )

    def _add_excitement_slider(self):
        self._add_labeled_slider(
            "excitement",
            "How excited are you about working on this?",
            [1, 2, 3, 4, 5],
            [
                "i really dont want to work on this",
                "not very excited",
                "this is ok",
                "this is exciting",
                "i cant wait to work on this",
            ],
        )

    def _add_value_slider(self):
        self._add_labeled_slider(
            "value",
            "How much better would your life be if you completed this task?",
            [1, 2, 3, 4, 5],
            [
                "it would not change",
                "it would be a little bit better",
                "it would improve",
                "it would improve a lot",
                "it would be a game changer",
            ],
        )

    def _add_calendar_field(self, label: str):
        calendar = DropDownCalendar(self, self.controller, label)
        calendar.pack()
        self.calendars[label] = calendar

    def _add_labeled_slider(
        self, label: str, message: str, values: list, annotations: list
    ):
        if len(values) != len(annotations):
            Exception("Values and annotations must have the same length")
        tk.Label(self, text=message).pack(padx=10)
        slider = AnnotatedSlider(self, self.controller, values, annotations)
        self.sliders[label] = slider
        slider.pack(padx=10)

    def _add_labeled_text_field(self, label: str, message: str, height=3):
        tk.Label(self, text=message).pack(padx=10)
        entryField = tk.Text(self, width=50, height=height)
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
        task = self._create_task_from_user_input()
        self.task_db_adder.add_task(task)
        self.bottom_message.config(text="Added task: " + task.description)
        self._clean_values()
        self.text_fields["description"].focus_set()

    def _create_task_from_user_input(self):
        task = Task(
            description=self.text_fields["description"].get("1.0", tk.END).strip(),
            definition_of_done=self.text_fields["dod"].get("1.0", tk.END).strip(),
            detailed_steps=self.text_fields["steps"].get("1.0", tk.END).strip(),
            deadline=self.calendars["deadline"].get_date(),
            project=self.project_entry.get_value().strip(),
            waiting_until=self.calendars["waiting for date"].get_date(),
        )
        task.rate(
            value=self.sliders["value"].get_selected_value(),
            excitement=self.sliders["excitement"].get_selected_value(),
            estimated_time_in_minutes=self.time_estimate_field.get(),
            cognitive_load=self.sliders["effort"].get_selected_value(),
        )
        return task

    def _clean_values(self):
        for entry in self.text_fields.values():
            entry.delete("1.0", tk.END)
        for calendar in self.calendars.values():
            calendar.reset()
        self.time_estimate_field.delete(0, tk.END)
        for selection in self.sliders.values():
            selection.value_var.set(-1)
