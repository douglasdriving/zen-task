import tkinter as tk
from .annotated_slider import AnnotatedSlider
from ....task.task import Task
from ....db.task_db_adder import TaskDbAdder
from .dropdown_calendar import DropDownCalendar
from ....db.project_db_retriever import ProjectDbRetriever
from ....db.task_retriever import TaskRetriever
from .entry_with_dropdown import DropdownEntry
from .dependencies_input_field import DependenciesInputField


class TaskCreationPage(tk.Frame):

    parent: object
    controller: object

    text_fields: dict[str, tk.Text]
    sliders: dict[str, AnnotatedSlider]
    calendars: dict[str, DropDownCalendar]
    project_entry: DropdownEntry
    bottom_message: tk.Label
    task_dependency_field: DependenciesInputField
    task_db_adder: TaskDbAdder
    add_task_button: tk.Button
    task_retriever = TaskRetriever()

    focus_fields: list[tk.Frame] = []
    currently_focused_field_id: int = 0

    def __init__(self, parent, controller):
        self.task_db_adder = TaskDbAdder()
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.text_fields = {}
        self.sliders = {}
        self.calendars = {}
        self.focus_fields = []
        self._setup_page()

    def _setup_page(self):
        self._add_return_button()
        tk.Label(self, text="Task Creation").pack(padx=10, pady=10)
        self._add_input_fields()
        self._add_add_button()
        self._add_bottom_message_label()
        self._clean_values()

    def _add_add_button(self):
        self.add_task_button = tk.Button(self, text="Add", command=self._add_task)
        self.add_task_button.pack(padx=10, pady=10)
        self._add_focus_field(self.add_task_button)
        self.add_task_button.bind("<Return>", lambda e: self._add_task())

    def focus_next_field(self):
        self.focus_fields[self.currently_focused_field_id].config(bg="white")
        self.currently_focused_field_id += 1
        if self.currently_focused_field_id >= len(self.focus_fields):
            self.currently_focused_field_id = 0
        target_field = self.focus_fields[self.currently_focused_field_id]
        target_field.focus_set()
        target_field.config(bg="yellow")

    def _focus_field(self, field_id: int):
        self.currently_focused_field_id = field_id
        self.focus_fields[field_id].focus_set()

    def _add_bottom_message_label(self):
        self.bottom_message = tk.Label(self, text="")
        self.bottom_message.pack(padx=10, pady=10)

    def _add_input_fields(self):
        description_field = self._add_labeled_text_field(
            "description", "Description", 2
        )
        description_field.focus_set()
        self.currently_focused_field_id = 0
        self._add_labeled_text_field("dod", "Definition of done", 2)
        self._add_labeled_text_field("steps", "Detailed steps", 5)
        self._add_calendar_field("deadline")
        self._add_calendar_field("waiting for date")
        self._add_project_field()
        self._add_dependencies_field()
        self._add_value_slider()
        self._add_excitement_slider()
        self._add_time_estimate_field()
        self._add_effort_slider()

    def _add_project_field(self):
        tk.Label(self, text="Project").pack()
        project_retriever = ProjectDbRetriever()
        projects = project_retriever.get_all_projects()
        self.project_entry = dropdown_entry = DropdownEntry(
            self, projects, self._on_project_change
        )
        dropdown_entry.pack()
        self._add_focus_field(dropdown_entry)

    def _on_project_change(self, project: str):
        self.task_dependency_field.update_projects([project])

    def _add_effort_slider(self):
        self._add_labeled_slider(
            "effort",
            "How much effort do you think this task will require?",
            [1, 2, 3, 4, 5],
            [
                "Trivial, i know exactly what to do",
                "Easy, i know what to do",
                "Medium, it will require a bit of thinking",
                "Quite hard, I will need to concentrate",
                "Hard, it requires full focus",
            ],
        )

    def _add_excitement_slider(self):
        self._add_labeled_slider(
            "excitement",
            "How much would you enjoy working on this?",
            [1, 2, 3, 4, 5],
            [
                "I wouldnt really enjoy it",
                "It would be ok",
                "I would might enjoy it a little bit",
                "I would probably enjoy it",
                "I would definitely enjoy it",
            ],
        )

    def _add_value_slider(self):
        example_tasks = []
        for i in range(1, 6):
            task = self.task_retriever.get_example_task_by_value(i)
            example_tasks.append(task.description)

        self._add_labeled_slider(
            "value",
            "How important is this in your life?",
            [1, 2, 3, 4, 5],
            [
                f"Not that important (example: {example_tasks[0]})",
                f"A little bit important (example: {example_tasks[1]})",
                f"Quite important (example: {example_tasks[2]})",
                f"Definitely important (example: {example_tasks[3]})",
                f"Very important (example: {example_tasks[4]})",
            ],
        )

    def _add_calendar_field(self, label: str):
        calendar = DropDownCalendar(self, self.controller, label)
        calendar.pack()
        self.calendars[label] = calendar
        self._add_focus_field(calendar)

    def _add_labeled_slider(
        self, label: str, message: str, values: list, annotations: list
    ):
        if len(values) != len(annotations):
            Exception("Values and annotations must have the same length")
        tk.Label(self, text=message).pack(padx=10)
        slider = AnnotatedSlider(self, self.controller, values, annotations)
        self.sliders[label] = slider
        slider.pack(padx=10)
        self._add_focus_field(slider)

    def _add_labeled_text_field(self, label: str, message: str, height=3):
        tk.Label(self, text=message).pack(padx=10)
        entryField = tk.Text(self, width=50, height=height)
        entryField.pack(padx=10)
        self.text_fields[label] = entryField
        focus_field_id = self._add_focus_field(entryField)
        entryField.bind("<FocusIn>", lambda e: self._focus_field(focus_field_id))
        return entryField

    def _add_focus_field(self, field: tk.Frame):
        self.focus_fields.append(field)
        focus_field_id = len(self.focus_fields) - 1
        field.bind("<Tab>", lambda e: self.focus_next_field() or "break")
        return focus_field_id

    def _add_return_button(self):
        tk.Button(
            self,
            text="<- Return",
            command=lambda: self.controller.show_frame("MainMenu"),
        ).pack(padx=10, pady=10)

    def _add_time_estimate_field(self):
        self._add_labeled_slider(
            "time",
            "How much time do you think this task will require?",
            [1, 2, 3, 4, 5],
            [
                "Less than 15 min",
                "15 - 30 min",
                "30 min - 1 hour",
                "1 - 2 hours",
                "More than 2 hours",
            ],
        )

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
            dependencies=self.task_dependency_field.get_selected_tasks(),
        )
        task.rate(
            value=self.sliders["value"].get_selected_value(),
            excitement=self.sliders["excitement"].get_selected_value(),
            time_complexity=self.sliders["time"].get_selected_value(),
            cognitive_load=self.sliders["effort"].get_selected_value(),
        )
        return task

    def _clean_values(self):
        for entry in self.text_fields.values():
            entry.delete("1.0", tk.END)
        for slider in self.sliders.values():
            slider.reset()
        for calendar in self.calendars.values():
            calendar.reset()
        self.project_entry.reset()
        self.task_dependency_field.close_dropdown()

    def _add_dependencies_field(self):
        self.task_dependency_field = DependenciesInputField(self)
        self.task_dependency_field.pack()
        self._add_focus_field(self.task_dependency_field)
