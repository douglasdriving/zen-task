import tkinter as tk


class AnnotatedSlider(tk.Frame):

    controller: object
    values: list
    value_var: tk.IntVar
    annotations: list
    slider: tk.Scale
    annotation: tk.Label

    def __init__(self, parent, controller, values: list, annotations: list):
        if len(values) != len(annotations):
            Exception("Values and annotations must have the same length")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.values = values
        self.annotations = annotations
        self._add_slider_and_annotation()
        self.bind("<FocusIn>", lambda e: self._on_focus())
        self.bind("<FocusOut>", lambda e: self._on_focus_out())

    def _add_slider_and_annotation(self):
        slider_frame = tk.Frame(self)
        slider_frame.pack(padx=10)
        self.value_var = tk.IntVar(value=self.values[0])
        self.slider = tk.Scale(
            slider_frame,
            from_=self.values[0],
            to=self.values[-1],
            orient=tk.HORIZONTAL,
            variable=self.value_var,
            command=self._update_annotation_text,
        )
        self.slider.pack()
        self.annotation = tk.Label(slider_frame, text=self.annotations[0])
        self.annotation.pack()

    def _update_annotation_text(self, value):
        index = self.values.index(int(value))
        self.annotation.config(text=self.annotations[index])

    def get_selected_value(self):
        return self.value_var.get()

    def reset(self):
        self.slider.set(self.values[0])
        self._update_annotation_text(self.values[0])

    def _on_focus(self):
        self._set_background("yellow")
        self._add_arrow_controls()

    def _add_arrow_controls(self):
        self.bind("<Left>", self._move_left)
        self.bind("<Right>", self._move_right)

    def _set_background(self, color):
        self.annotation.config(bg=color)

    def _move_left(self, event):
        current_value = self.value_var.get()
        if current_value > self.values[0]:
            self.value_var.set(current_value - 1)

    def _move_right(self, event):
        current_value = self.value_var.get()
        if current_value < self.values[-1]:
            self.value_var.set(current_value + 1)

    def _on_focus_out(self):
        self._set_background("white")
        self._remove_arrow_controls()

    def _remove_arrow_controls(self):
        self.unbind("<Left>")
        self.unbind("<Right>")
