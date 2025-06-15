# REFERENCES:
# https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python

import tkinter as tk
from tkinter import ttk

class Tooltip(object):
    def __init__(self, widget):
        style = ttk.Style()
        style.configure(
            "Tooltip.TLabel",
            relief="solid",
            borderwidth=1,
            font=("TKDefaultFont", 10)
        )

        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if bool(self.tipwindow) or not bool(self.text):
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() # edited
        y = y + cy + self.widget.winfo_rooty() # edited
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x,y))
        # label = ttk.Label(tw, text=self.text, justify=tk.LEFT, relief=tk.SOLID, borderwidth=1, font=("Helvetica", 8))
        label = ttk.Label(tw, text=self.text, style="Tooltip.TLabel")
        label.pack(padx=1)
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if bool(tw):
            tw.destroy()
            
def CreateTooltip(widget, text):
    toolTip = Tooltip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

if __name__ == "__main__":
    root = tk.Tk()

    btn = ttk.Button(root, text="click me")
    btn.pack()
    CreateTooltip(btn, text=r"""Hello World
This is how tip looks like.
Best part is, it's not a menu.
Purely tipbox.""")

    root.mainloop()