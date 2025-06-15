import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFilter
import sympy as sp

from pathway import pathway
from img_to_roi import clear_old_rois, get_rois
from img_border import clear_old_borders, border_rois
from interpreter import interpret, translate, display

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
os.chdir(dirname) # now the working directory is set to the file path

roi_folder = pathway(dirname, "rois")
roi_border = pathway(os.getcwd(), "rois_bordered")

root = tk.Tk()
root.geometry("1280x576") # not 16:9 (an extension of 1024x576)

style = ttk.Style()
style.configure("TButton", font="TKDefault 12")
style.configure("TLabel", font="TKDefault 24") # sure why not

left_frame = ttk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

right_frame = ttk.Frame(root)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH)

ocr_var = tk.StringVar()
def set_ocr_var(*args):
    global ocr_var
    ocr_var.set(interpret(roi_border))
    root.event_generate("<<ForTranslation>>")
    root.event_generate("<<ForDisplay>>")

class DrawingCanvas:
    def __init__(self, parent_frame):
        # tkinter canvas widget & PIL Image
        self.canvas = tk.Canvas( # 16:9 aspect ratio; https://en.wikipedia.org/wiki/16:9_aspect_ratio
            parent_frame, 
            width=1024,
            height=576,
            bg="#525657"
        )
        self.image = Image.new(
            "RGB", 
            (self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()), # inherits the dim. of the canvas widget set earlier
            "#525657"
        )

        # various other parameters
        self.last_x, self.last_y = None, None  # initialize last position
        self.draw_image = ImageDraw.Draw(self.image)
        self.save_id = None

        # bind mouse events for drawing on the canvas
        self.canvas.bind("<B1-Motion>", self.draw) # set to left-click motion; calls on its own method
        self.canvas.bind("<ButtonRelease-1>", self.handle_ButtonRelease_1) # set to left-click; same here
        self.canvas.bind("<ButtonRelease-3>", self.handle_ButtonRelease_3) # ButtonRelease-2 is middle click
    
    """The widget's main feature: drawing"""
    def draw(self, event): # draws a line on the canvas following the mouse movement
        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill="white", width=5)
            self.draw_image.line([self.last_x, self.last_y, x, y], fill="white", width=5)
            # self.image = self.image.filter(ImageFilter.SMOOTH_MORE) # this somehow breaks the program?
        self.last_x, self.last_y = x, y

    def reset_position(self, event): # resets the last position when the mouse is released
        self.last_x, self.last_y = None, None

    def clear_drawings(self, *args): # apparently event was needed here; or *args????
        self.canvas.delete(tk.ALL)
        # self.draw_image = ImageDraw.Draw(self.image) # reassign a few new image draw; this does not work
        self.image = Image.new("RGB", (self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()), "#525657")
        self.draw_image = ImageDraw.Draw(self.image)

    """The widget's save functionality"""
    def ocr_sequence(self, event):
        self.image.save("img.png") # units in ms; will save to the current directory
        clear_old_rois(roi_folder) # first clear any old ocr's
        get_rois( # then get the rois
            pathway(dirname, "img.png"),
            roi_folder
        )

        clear_old_borders(roi_border) # same thing here
        border_rois(roi_folder, roi_border) # then finally border them
        root.event_generate("<<ForInterpretation>>")

    def handle_ButtonRelease_1(self, event):
        self.reset_position(event)
        self.ocr_sequence(event)
        
    def handle_ButtonRelease_3(self, event):
        self.clear_drawings(event)

        global ocr_var
        ocr_var.set("") # this should not work, but it does (because ocr_var is defined afterwards)

root.bind("<<ForInterpretation>>", set_ocr_var)

drawing_canvas = DrawingCanvas(left_frame)
drawing_canvas.canvas.pack()

##################
# Interpretation #
##################
interpretation_var = tk.StringVar()
def set_interpretation_var(*args):
    global interpretation_var
    interpretation_var.set(
        display(translate(ocr_var.get()))
    )

interpretation_frame = ttk.Frame(right_frame)
interpretation_frame.pack(side=tk.TOP)

interpretation_label = ttk.Label(interpretation_frame, text="Interpretation:")
interpretation_label.grid(row=0, column=0, sticky=tk.E)

interpretation_result = ttk.Label(interpretation_frame, textvariable=ocr_var) # temporarily setting this to ocr_var
interpretation_result.grid(row=1, column=0, sticky=tk.N)

# root.bind("<<ForDisplay>>", set_interpretation_var) # disabling this as well

###############
# Calculation #
###############
def calculate(expr):
    if not any(["x" in expr, "y" in expr, "z" in expr]):
        try:
            symbolic_expr = sp.sympify(expr)
            calculations = symbolic_expr.evalf()
        except ValueError:
            calculations = "?"
    else:
        calculations = "?"

    return calculations

calculation_frame = ttk.Frame(right_frame)
calculation_frame.pack(side=tk.TOP)

calculation_label = ttk.Label(calculation_frame, text="Calculations:")
calculation_label.grid(row=0, column=0, sticky=tk.E)

calculation_result = tk.Text(calculation_frame, font="TKDefaultFont 12", width=1, height=9) # so width actually doesn't matter if use sticky all side, but it needs to at least be set
calculation_result.grid(row=1, column=0, sticky="nesw")

def insert_calculations(*args):
    calculations = calculate(ocr_var.get())
    calculation_result.delete("1.0", tk.END)
    calculation_result.insert("1.0", calculations)
    # print(calculations)

root.bind("<<ForTranslation>>", insert_calculations)

if __name__ == "__main__":
    root.mainloop()

"""
Scrapped Code:
if self.save_id:
        self.canvas.after_cancel(self.save_id)
    self.save_id = self.canvas.after(2000, self.save) # units in ms; need to figure out how to have this interuppted if click again

def handle_event_in_timeframe(self, event):
# This event is triggered if something happens before the 2000ms
    if self.save_id:
        self.canvas.after_cancel(self.save_id)  # Cancel the previously scheduled save
        print("Event occurred before timeout, save cancelled!")

    # You can now trigger the new action after the event happens
    self.save_id = self.canvas.after(2000, self.image.save("img.png"))  # Start the timer again after 2000ms
    print("Timer reset to trigger a new save.")

def handle_b1_motion(self, event):
    self.draw(event)
    self.handle_event_in_timeframe(event)

def handle_button_release_1(self, event):
    self.reset_position(event)
    self.ocr_sequence(event)

x, y, z = sp.symbols("x, y, z")
def calculate(ocr_var):
    try:
        expr = translate(ocr_var)
        symbolic_expr = sp.sympify(expr)
        if any(["x" in expr, "y" in expr, "z" in expr]):
            if "x" in expr: # I only really care for the case the expression is of one (mathematical) variable type
                calculations = sp.solve(symbolic_expr, x)
            elif "y" in expr:
                calculations = sp.sympify(symbolic_expr, y)
            elif "z" in expr:
                calculations = sp.sympify(symbolic_expr, z)
        else: # then this assumes to be an arithmetic expression
            calculations = symbolic_expr.evalf()
    except ValueError:
        calculations = None
            
    return calculations
"""