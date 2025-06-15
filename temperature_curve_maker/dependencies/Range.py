import tkinter as tk
from tkinter import ttk

try: # relative import
    from SpinboxClear import SpinboxClear
except ImportError: # for * import
    from .SpinboxClear import SpinboxClear
    
class Range:
    """
    Helper class for Step.py

    Create a framed collection of one label widget and multiple SpinboxClear classes.
    
    After taking in a parent frame and label text as mandatory parameters,
    optional parameters may additionally be passed as variable-tk.StringVar()
    key-value pairs.
    
    Intended to be used to display and function as a range setup.
    """
    def __init__(self, parent, label=None, range=None, root=None, **kwargs):
        self.frame = ttk.Frame(parent)

        self.label = ttk.Label(self.frame, text=label)
        self.label.grid(row=0, column=0, columnspan=len(kwargs))

        for n, (key, value) in enumerate(kwargs.items()):
            setattr(self, key, SpinboxClear(self.frame, value, range=range, row=1, column=n))

if __name__ == "__main__":
    root = tk.Tk()

    temp = Range(root, "Temperature (\u00B0C)", range=(0, 1700, 1), T0=tk.StringVar(), T=tk.StringVar())
    temp.frame.pack()

    root.mainloop()

    print(temp.T0.var.get(), temp.T.var.get()) # an example on how to retrieve the string values