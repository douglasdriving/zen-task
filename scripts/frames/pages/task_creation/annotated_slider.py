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
