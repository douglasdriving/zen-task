import tkinter as tk


class DropdownEntry(tk.Frame):

    parent: tk.Frame

    def __init__(self, parent, options, on_entry_change: callable = None):
        tk.Frame.__init__(self, parent, takefocus=True)

        self.parent = parent

        self.options: list[str] = options
        self.entry_var = tk.StringVar()

        self.bind("<FocusIn>", self._highlight_field_and_show_list)
        self.bind("<FocusOut>", self._remove_highlight_and_hide_list)

        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.entry.pack()

        self.listbox = tk.Listbox(self, height=len(options))
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.listbox.pack_forget()

        for option in self.options:
            self.listbox.insert(tk.END, option)

        if on_entry_change:
            self.entry_var.trace_add(
                "write", lambda *args: on_entry_change(self.entry_var.get())
            )

        self._bind_keys()

    def _bind_keys(self):
        self.bind("<Down>", lambda e: self._move_highlight(1))
        self.bind("<Up>", lambda e: self._move_highlight(-1))
        self.bind("<Return>", self._select_highlighted_and_move_to_next_field)

    def _highlight_field_and_show_list(self, event):
        self.entry.config(bg="yellow")
        self.listbox.pack()
        self.listbox.selection_set(0)
        self.listbox.activate(0)

    def _remove_highlight_and_hide_list(self, event=None):
        self.after(100, self.listbox.pack_forget)
        self.entry.config(bg="white")
        self.listbox.select_clear(0, tk.END)

    def on_listbox_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.entry_var.set(self.listbox.get(selection[0]))
            self.listbox.pack_forget()

    def get_value(self):
        return self.entry_var.get()

    def reset(self):
        self.entry_var.set("")
        self.listbox.pack_forget()

    def _move_highlight(self, steps: int):
        selection = self.listbox.curselection()
        if selection:
            self.listbox.selection_clear(selection[0])
            new_index = (selection[0] + steps) % len(self.options)
            self.listbox.selection_set(new_index)
            self.listbox.activate(new_index)

    def _select_highlighted_and_move_to_next_field(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.entry_var.set(self.listbox.get(selection[0]))
            self.listbox.select_clear(0, tk.END)
            self.listbox.pack_forget()
            self.focus_set()
        if self.parent.focus_next_field:
            self.parent.focus_next_field()
