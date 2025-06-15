# REFERENCES:
# https://stackoverflow.com/questions/78792558/is-there-a-way-to-add-close-and-add-buttons-to-tabs-in-tkinter-ttk-notebook
# https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook/39459376#39459376
# https://www.youtube.com/watch?v=n5gItcGgIkk

import tkinter as tk
from tkinter import ttk

try: # for relative import
    from AutoResizingEntry import AutoResizingEntry
except ImportError:
    from .AutoResizingEntry import AutoResizingEntry

class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False
    
    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            CustomNotebook.__initialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        self.bind("<Double-1>", self.rename)

    def create_add_btn(self):
        f""" # f-string indicates new edits
        Original code:
        >>> self.add(tk.Frame(self), state='disabled') # '+' tab
        under the __init__() method

        The purpose of moving this is so the add button appears at the
        right-hand side of the transversal.

        The trade-off however is that the method must be manually
        called upon (which is fine...)
        """
        self.add(tk.Frame(self), state='disabled') # '+' tab

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""
        element = self.identify(event.x, event.y)
        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            if self.tab(index, 'state') == 'disabled':  # "+" tab is pressed
                self.add_new_tab(index)
                return "break"
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def add_new_tab(self, add_index):
        """Adds a new tab on button '+' pressed"""
        pass
        # Your code for the new tab there. Example:
        self.insert(add_index, tk.Label(text='Just a test tab'), text='NewTab')
        self.select(add_index)

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            '''),
            tk.PhotoImage("img_add", data='''
                iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAAXNSR0IArs4c6QAA
                AARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAB+SURBVChTY2ZA
                AyJSxtVcPFJq3748Pw8VAgMmKI0EGHkZGZi4oBw4wKIQOyBaISPITSDroHyG//8Z
                7IHkF0ZGxrNQIQZGxv/vmRj+M7xg/M/4FIZBioByH1HE/jO9hGhBAiJSJh2ikqa5
                UC4cUN8zGApBDmdgZPgM5UIBAwMAe9MjkX8aHzEAAAAASUVORK5CYII=''')  # "+" image
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"),
                            ("disabled", "img_add"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])
    
    def rename(self, event): # new code
        x, y = event.x, event.y
        element = self.identify(x, y)

        if element == "label": # usually tab, but that's actually only the "+" tab
            tab_index = self.index("@%d,%d" % (event.x, event.y)) # it's actually hard to get specific info from ttk.Notebook.tabs()...
            tab_label = self.tab(tab_index, "text")

            entry_edit = AutoResizingEntry(self)

            entry_edit.editing_column_index = tab_index # assign the entry widget the notebook tab index

            entry_edit.insert(0, tab_label) # insert back the text
            entry_edit.select_range(0, tk.END) # have the text selected

            entry_edit.focus()
            entry_edit.bind("<FocusOut>", self.on_focus_out)
            entry_edit.bind("<Return>", self.on_enter_pressed)

            entry_edit.place(x=x, y=y-entry_edit.winfo_reqheight()//2) # this value here ended up being 10 anyways... # https://stackoverflow.com/questions/3950687/how-to-find-out-the-current-widget-size-in-tkinter

    def on_enter_pressed(self, event, tab_index=None):
        new_label = event.widget.get()
        tab_index = event.widget.editing_column_index # get back the tab index

        self.tab(tab_index, text=new_label)
        self.event_generate("<<NotebookTabRenamed>>")

        event.widget.destroy()

    def on_focus_out(self, event):
        event.widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()

    notebook = CustomNotebook(width=200, height=200)
    notebook.pack(side="top", fill="both", expand=True)

    for color in ("red", "orange", "green", "blue", "violet"):
        frame = tk.Frame(notebook, background=color)
        notebook.add(frame, text=color)
    notebook.create_add_btn() # new method being employed

    root.mainloop()