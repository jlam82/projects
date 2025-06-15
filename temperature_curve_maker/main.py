import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import accumulate

import os
abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
os.chdir(dirname) # now the path is set at this file no matter where it is opened

import ctypes # for 4k resolutions
ctypes.windll.shcore.SetProcessDpiAwareness(1)

from dependencies import *

root = tk.Tk()
root.title("Blue Box Furnace Code")
root.geometry("1600x900")

####################
# Global Variables #
####################
colors = tuple(mcolors.TABLEAU_COLORS.values())

########################
# Controller Variables #
########################
destroyer, observer = tk.IntVar(), tk.BooleanVar()
Surveilled.set_destroyer(destroyer); Surveilled.set_observer(observer)

#################
# Style Configs #
#################
style = ttk.Style()
style.configure("TLabel", font="TKDefaultFont 12")
style.configure("add.TButton", font="TKDefaultFont 24", width=2, height=3)
style.configure("title.TEntry", font="TKDefaultFont 12")

i = tk.PhotoImage(width=1, height=1)

#######
# GUI #
#######
toolbar_frame = ttk.Frame(root)
toolbar_frame.pack(fill=tk.X)

application_frame = ttk.Frame(root)
application_frame.rowconfigure(0, weight=1) # now the canvas expands vertically
application_frame.columnconfigure(1, weight=1) # allow the graph to expand horizontally

application_frame.pack(fill="both", expand=True)

# starting graph
graph_frame = ttk.Frame(application_frame)
graph_frame.grid(row=0, column=1, sticky="nesw")

fig, ax = plt.subplots()
ax.set_xlim(0, 5); ax.set_ylim(20, 25)
ax.set_xlabel("Time"); ax.set_ylabel("Temperature (\u00B0C)")
# ax.grid()

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)
canvas.draw()

# toolbar
toolbar = CustomToolbar(canvas, toolbar_frame)
toolbar.update() # initialize the toolbar
toolbar.pack(side=tk.TOP, fill=tk.X)
ttk.Separator(toolbar_frame, orient="horizontal").pack(side=tk.TOP, fill=tk.X) # seperation line

def toggle_pids(*args):
    if Curve.pid_state:
        Curve.pid_state = False
    else:
        Curve.pid_state = True

    Curve.toggle_pids()

pid_icon = ImageTk.PhotoImage(Image.open("images/mpl-data_images/subplots.png")) # stock matplotlib icon image
pid_btn = ToggleButton(toolbar, callback_func=toggle_pids, image=pid_icon, style="Toolbutton")
toolbar.add_custom_button(pid_btn, before=True, where=0) # before the "save" button
CreateTooltip(pid_btn, text="Toggle PID veiw")

pdf_icon = to_toolbar_icon(Image.open("images/pdf_icon_gray.png"))
pdf_btn = ttk.Button(toolbar, image=pdf_icon, style="Toolbutton")
toolbar.add_custom_button(pdf_btn, where=1)
CreateTooltip(pdf_btn, text="Export graph and steps to PDF")

debug_btn = ttk.Button(toolbar, width=2, style="Toolbutton")
toolbar.add_custom_button(debug_btn, where=2)
CreateTooltip(debug_btn, text="Update the graph (DEBUG)")

# interface_frame[add_frame, step_frame]
interface_frame = ttk.Frame(application_frame)
interface_frame.grid(row=0, column=0, sticky="nesw", padx=1)

# title frame
title_frame = ttk.Frame(interface_frame)
title_frame.pack(fill=tk.X, pady=5)

ttk.Label(title_frame, text="Graph title: ").pack(side=tk.LEFT)

title_var = tk.StringVar()
title_entry = ttk.Entry(title_frame, textvariable=title_var, style="title.TEntry")
title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True) # wow first time I had to call all of this

# sidebar
notebook = CurveNotebook(interface_frame)
notebook.pack(fill=tk.BOTH)
notebook.enable_traversal()

curve1 = Curve(root, colors[0])
notebook.add(curve1.frame, text="Curve 1", sticky="nesw")

notebook.create_add_btn()

######################
# Contoller Settings #
######################
def observe(*args):
    global fig, ax, canvas

    # pid state
    Curve.toggle_pids()
    Curve.reassign_colors()
    
    # the graph
    ax.clear()

    tab_labels = [notebook.tab(tab_id, option="text") for tab_id in notebook.tabs()][:-1] # the last one is just the "+" tab
    array_list = Curve.get_all_data()

    origin = np.array(["0", "20"], dtype=object)
    for array, label in zip(array_list, tab_labels):
        array = np.vstack((origin, array)) # first stack the origin on top
        float_array = np.where(array == "", np.nan, array).astype(float) # now this is the proper type cast
        pid_levels = get_pid_levels(float_array)

        xs = list(accumulate(float_array[:, 0])) # we want the accumulation of the time intervals
        ys = float_array[:, 1]

        ax.scatter(xs, ys, zorder=2)
        ax.vlines(xs, 20, ys, colors="k", linestyles="dashed")
        ax.plot(xs, ys, label=label)

    ax.set_xlabel("Time (hr)"); ax.set_ylabel("Temperature (\u00B0C)")
    ax.set_ylim(bottom=20) # https://stackoverflow.com/questions/11744990/how-to-set-auto-for-upper-limit-but-keep-a-fixed-lower-limit
    ax.set_title(title_var.get())
    ax.legend(loc="upper right")

    # pid
    if Curve.pid_state:
        selected_tab = notebook.index(notebook.select())
        pid_levels = get_pid_levels(array_list[selected_tab])

        x = np.linspace(min(xs), max(xs), 100)
        for level in pid_levels:
            ax.fill_between(x, 20, level*np.ones_like(x), color=colors[selected_tab], alpha=0.1)

    canvas.draw()

observer.trace_add("write", observe)
root.bind("<<NotebookTabCreated>>", observe) # event from CurveNotebook; this double outputs
root.bind("<<NotebookTabClosed>>", observe) # event from CustomNotebook
root.bind("<<NotebookTabRenamed>>", observe) # event from CustomNotebook
root.bind("<<NotebookTabChanged>>", observe) # this just exists???
title_var.trace_add("write", observe)
debug_btn.configure(command=observe)

if __name__ == "__main__":
    root.mainloop()