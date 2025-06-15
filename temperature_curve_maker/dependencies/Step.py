import tkinter as tk
from tkinter import ttk

try: # relative import (script development)
    from Surveilled import Surveilled
    from Range import Range
    from ColorSquare import ColorSquare
except ImportError: # for * import
    from .Surveilled import Surveilled
    from .Range import Range
    from .ColorSquare import ColorSquare

class Step(Surveilled):
    """
    Class module for retaining step information, including PID,
    set temperature, and time span.
    """
    def __init__(self, parent, hexcode="#000000", pid_no=None):
        super().__init__()

        style = ttk.Style()
        style.configure("destroy.TButton", font="TKDefaultFont 12", width=2, height=3)

        self.i = tk.PhotoImage(width=1, height=1) # had to put self here...

        self.frame = ttk.Frame(parent)
        self.subframe = ttk.Frame(self.frame) # *sigh*, making a subframe became necessary after all...
        self.subframe.pack(fill=tk.X)


        # step number
        self.step_var = tk.IntVar()
        self.step_label = ttk.Label(self.subframe, textvariable=self.step_var)
        self.step_label.grid(row=0, column=0, padx=10)
        

        # range settings
        """Slight bug: if the 2nd step gets deleted when there's only the 1st and 2nd step, it'll return the values of the 1st step and a duplicate."""
        """Reference: https://stackoverflow.com/questions/73501896/what-is-mode-argument-of-trace-add-method-in-tkinter"""
        self.time = Range(self.subframe, "Time Range (hr)", range=(1, 72, 1), t=tk.StringVar()) # originally was tk.DoubleVar() but I like to keep "" as a value
        self.time.t.var.trace_add("write", lambda *args: Step.observer.set(True)) # wow can't believe that works lmao
        self.time.t.var.trace_add("unset", lambda *args: Step.observer.set(True)) # for the case the step gets deleted
        self.time.frame.grid(row=0, column=1, padx=5)

        self.temp = Range(self.subframe, "Temperature (\u00B0C)", range=(1, 1700, 1), T=tk.StringVar())
        self.temp.T.var.trace_add("write", lambda *args: Step.observer.set(True))
        self.temp.T.var.trace_add("unset", lambda *args: Step.observer.set(True))
        self.temp.frame.grid(row=0, column=2)


        # color square & PID
        self.pid_frame = ttk.Frame(self.subframe) # separate frame for toggling
        self.pid_frame.grid(row=0, column=3)

        self.color_square = ColorSquare(self.pid_frame, hexcode)
        self.color_square.canvas.pack(side=tk.LEFT)

        self.pid_label = ttk.Label(self.pid_frame, text="PID")
        self.pid_label.pack(side=tk.LEFT) # no need to "save" this specific widget

        self.pid_no = ttk.Label(self.pid_frame, text=str(pid_no)) # polymorphism used here
        self.pid_no.pack(side=tk.LEFT)

        # destroy button
        self.destroyButton = ttk.Button( # by default no command is set; intended to be set then in main.py
            self.subframe, text="\u00D7", style="destroy.TButton",
            image=self.i, compound="c", 
            command=lambda: Step.destroyer.set(self.step_var.get())
        )
        self.destroyButton.grid(row=0, column=4)

        ttk.Separator(self.frame, orient="horizontal").pack(side=tk.BOTTOM, fill=tk.X, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    destroyer, observer = tk.IntVar(), tk.BooleanVar()
    Surveilled.set_destroyer(destroyer); Surveilled.set_observer(observer)

    def destroy(*args):
        to_destroy = destroyer.get()
        print(to_destroy)
    destroyer.trace_add("write", destroy)

    def observe(*args):
        observation = observer.get()
        print(observation)

        observer.set(False)
    observer.trace_add("write", observe)

    step = Step(root, hexcode="#ADD8E6", pid_no=1)
    step.frame.pack()

    root.mainloop()