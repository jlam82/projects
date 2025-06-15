import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.colors as mcolors

try: # for relative import 
    from Step import Step # subclass for Curve
    from Surveilled import Surveilled # parent class for inheritance
    from ColorSquare import ColorSquare
except ImportError: # for * import
    from .Step import Step
    from .Surveilled import Surveilled
    from .ColorSquare import ColorSquare

class Curve(Surveilled):
    """
    Class module containing respective step classes, add button, etc.
    """
    pid_state = False
    __instances = []
    mcolor = tuple(mcolors.TABLEAU_COLORS.values()) # it's off by one "s" yes

    """Complementary functions for the toggle_pid() class method."""
    """Known bug: raise an error upon closing the window (this seems benign)"""
    def enable_pids(step):
        step.destroyButton.grid_forget()

        step.pid_frame.grid(row=0, column=3)
        step.destroyButton.grid(row=0, column=4)
    
    def disable_pids(step):
        step.pid_frame.grid_forget()
        step.destroyButton.grid_forget()

        step.destroyButton.grid(row=0, column=3)

    @classmethod
    def toggle_pids(cls):
        for curve in cls.__instances:
            steps = curve[0] # first thing in the tuple is the steps
            if Curve.pid_state: # be careful with the logic here
                steps[0].pid_frame.grid(row=0, column=3) # separated because its destroyButton is missing
                # Curve.venable_pids(steps[1:])
                for step in steps[1:]:
                    Curve.enable_pids(step)
            else:
                steps[0].pid_frame.grid_forget()
                for step in steps[1:]:
                    Curve.disable_pids(step)
                # Curve.vdisable_pids(steps[1:])

    def _get_curve_data(steps):
        """
        Helper method to get all data within a Curve instance.
        """
        return np.array([(step.time.t.var.get(), step.temp.T.var.get()) for step in steps], dtype=object)
    
    @classmethod
    def get_all_data(cls):
        """
        Get all step information for each curve
        """
        return [Curve._get_curve_data(curve[0]) for curve in Curve.__instances]
    
    @classmethod
    def remove_data(cls, index):
        """
        Class method to help remove an instance's steps.

        Needed for CurveNotebook.
        """
        del Curve.__instances[index]

    @classmethod
    def reassign_colors(cls):
        """
        Reassign curve colors when tab numbers are updated.
        """
        for n, curve in enumerate(Curve.__instances):
            curve[1].change_color(Curve.mcolor[n])

    def decrease(step):
        """Complementary function for the Step class"""
        """Reduces the step_var attribute value as well as the grid row by 1."""
        n = step.step_var.get()
        
        step.step_var.set(n-1)

        step.frame.grid_forget()
        step.frame.grid(row=(n-1), column=0, sticky="nsw")

    def __init__(self, parent, mcolor="#000000"):
        super().__init__()

        style = ttk.Style()
        style.configure("add.TButton", font="TKDefaultFont 24", width=2, height=3)
        self.i = tk.PhotoImage(width=1, height=1)
        self.frame = ttk.Frame(parent) # the main frame

        # add portion
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X)
        
        add_btn = ttk.Button(
            header_frame, text="+", image=self.i, compound="c", style="add.TButton"
        )
        add_btn.pack(side=tk.LEFT)

        add_lbl = ttk.Label(header_frame, text="Add step")
        add_lbl.pack(side=tk.LEFT, padx=10)

        # curve colors
        color_frame = ttk.Frame(header_frame)
        color_frame.pack(side=tk.RIGHT, padx=5)

        self.color_square = ColorSquare(color_frame, mcolor)
        self.color_square.canvas.pack(side=tk.LEFT)

        ttk.Label(color_frame, text="Curve").pack(side=tk.LEFT)

        # step portion
        self.step_frame = ttk.LabelFrame(self.frame, text="Step")
        self.step_frame.pack(fill=tk.BOTH, padx=5)

        self.steps = []
        self.steps.append(Step(self.step_frame)) # base case
        self.steps[0].step_var.set(1)
        self.steps[0].temp.T.var.set(20)
        self.steps[0].destroyButton.destroy() # remove Step 1's destroy button from view
        if not Curve.pid_state: # check if pids are disabled from the start
            self.steps[0].pid_frame.grid_forget()
        self.steps[0].frame.grid(row=0, column=0, sticky="nsw")
        
        add_btn.configure(command=self.create_step)
        Curve.destroyer.trace_add("write", self.destroy)

        # track the instance
        Curve.__instances.append([self.steps, self.color_square]) # store the steps and color

    def create_step(self):
        n = len(self.steps) + 1 # convention set with +1

        self.steps.append(Step(self.step_frame))
        self.steps[-1].step_var.set(n)
        self.steps[-1].temp.T.var.set(self.steps[-2].temp.T.var.get())
        self.steps[-1].frame.grid(row=n, column=0, sticky="nsw")
    
    def destroy(self, *args): # eat up any given arguments
        to_destroy = Curve.destroyer.get()
        to_destroy -= 1 # change convention

        for step in self.steps[to_destroy:]:
            Curve.decrease(step)

        self.steps[to_destroy].frame.destroy() # destroy the Step class; this raises an exception when deleting the last number (vectorizing used to fix this)
        del self.steps[to_destroy] # remove from memory

if __name__ == "__main__":
    root = tk.Tk()

    destroyer, observer = tk.IntVar(), tk.BooleanVar()
    Surveilled.set_destroyer(destroyer); Surveilled.set_observer(observer)

    curve1 = Curve(root, Curve.mcolor[0])
    curve1.frame.pack()

    Curve.pid_state = True
    # Curve.pid_state = False
    def observe(*args): # example observer
        Curve.toggle_pids()
        print(Curve.get_all_data())
    observer.trace_add("write", observe)

    root.mainloop()