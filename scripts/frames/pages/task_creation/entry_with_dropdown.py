import tkinter as tk


class DropdownEntry(tk.Frame):

    def __init__(self, parent, options, on_entry_change: callable = None):
        super().__init__(parent)
        self.options: list[str] = options
        self.entry_var = tk.StringVar()

        self.entry = tk.Entry(self, textvariable=self.entry_var)
        self.entry.pack()
        self.entry.bind("<FocusIn>", self.show_listbox)
        self.entry.bind("<FocusOut>", self.hide_listbox)

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

    def show_listbox(self, event=None):
        self.listbox.pack()

    def hide_listbox(self, event=None):
        self.after(100, self.listbox.pack_forget)

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
