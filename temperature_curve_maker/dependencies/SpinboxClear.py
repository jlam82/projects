import tkinter as tk
from tkinter import ttk

try: # relative import
    from functions import only_floats
except ImportError: # for * import
    from .functions import only_floats

class SpinboxClear:
    """
    Helper class for Range.py.
    
    Contains a spinbox and clear button.
    """
    root = None  # class-level variable to store the Tk instance

    def __init__(self, parent, tkvar, range: tuple=None, **kwargs):
        if not SpinboxClear.root:
            try: # try to find a root from an existing widget (this fails silently if none exists)
                SpinboxClear.root = tk._default_root or tk.Tk() # this line is magic?
            except Exception as e:
                raise RuntimeError("Could not initialize or find a Tk root window.") from e
        
        validation = SpinboxClear.root.register(only_floats)  # register validation on the root instance

        style = ttk.Style()
        style.configure("TButton", font="TKDefaultFont 8", width=1, height=1)

        self.Frame = ttk.Frame(parent)
        self.var = tkvar

        self.Spinbox = ttk.Spinbox(
            self.Frame, textvariable=tkvar, 
            validate="key", validatecommand=(validation, "%S"),
            font="TKDefaultFont 13"
        )

        width = 3
        if range: # will try to auto-set widths for each of the entries
            if all(isinstance(i, int) for i in range):
                width = len(str(range[1])) + 1
                self.Spinbox.configure(width=width, from_=range[0], to=range[1], increment=range[2])
        else:
            self.Spinbox.configure(width=width)

        self.Spinbox.set("")  # Start every entry blank
        self.Spinbox.pack(side=tk.LEFT)

        self.Button = ttk.Button(
            self.Frame, text="\u00D7", command=lambda: self.Spinbox.delete("0", tk.END)
        )
        self.Button.pack(side=tk.LEFT)
        self.Button.bind("<FocusIn>", self.focus_next_widget)

        self.Frame.grid(**kwargs)
    
    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

if __name__ == "__main__":
    root = tk.Tk()
    spinbox_clear = SpinboxClear(root, tk.StringVar(), range=(0, 1700, 1))
    
    root.mainloop()