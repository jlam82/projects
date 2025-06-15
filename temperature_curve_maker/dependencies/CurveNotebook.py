import tkinter as tk
from tkinter import ttk
import matplotlib.colors as mcolors

try: # for relative import
    from CustomNotebook import CustomNotebook # parent class
    from Curve import Curve # subclass
except ImportError:
    from .CustomNotebook import CustomNotebook
    from .Curve import Curve

class CurveNotebook(CustomNotebook): # using inheritance to perform method override
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super().__init__(parent, *args, **kwargs)

        self.colors = tuple(mcolors.TABLEAU_COLORS.values())

    def add_new_tab(self, add_index):
        """
        Method override to customize adding a new tab.
        """
        tab_num = len(super().tabs())

        self.insert(
            add_index,
            Curve(self.parent, mcolor=self.colors[tab_num-1]).frame,
            text=f"Curve {tab_num}"
        )
        self.select(add_index)

        self.event_generate("<<NotebookTabCreated>>") # for the observer in main
    
    def on_close_release(self, event):
        """
        Method override for additional handling on closing a tab.

        Nearly copy-paste from CustomNotebook
        """
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))
        Curve.remove_data(index)

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

if __name__ == "__main__":
    from Surveilled import Surveilled

    root = tk.Tk()
    destroyer, observer = tk.IntVar(), tk.BooleanVar()
    Surveilled.set_destroyer(destroyer); Surveilled.set_observer(observer)

    def observe(*args): # example observer
        observation = observer.get()

        # Curve.pid_state = True
        Curve.pid_state = False
        Curve.toggle_pids()

        print(Curve.get_all_data())

        observer.set(False)
    observer.trace_add("write", observe)

    notebook = CurveNotebook(root)
    notebook.pack()
    notebook.enable_traversal()

    curve1 = Curve(root, tuple(mcolors.TABLEAU_COLORS.values())[0]) # spaghetti code sure but it works
    notebook.add(curve1.frame, text="Curve 1", sticky="nesw") # this way of initially starting some tab is fine 
    
    notebook.create_add_btn()

    root.mainloop()