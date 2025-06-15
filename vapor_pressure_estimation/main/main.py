import os
abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
os.chdir(dirname) # now no matter where the script is open, the directory is set to here and here only
# https://stackoverflow.com/questions/1432924/python-change-the-scripts-working-directory-to-the-scripts-own-directory

import pandas as pd
from periodic_table import request_df # local import
df = request_df()
yaws = pd.read_csv("yaws_csv.csv").drop(columns=["No."]) # no need for inplace

import re
import numpy as np
from math import pi

import tkinter as tk
from tkinter import ttk
from AutoSuggestCombobox import AutoSuggestCombobox # local import

from IPython.display import display # for debugging purposes

####################
# Global Variables #
####################
mass_lib = dict(zip(df.Symbol, df.AtomicMass))

####################


root = tk.Tk()
root.geometry("1280x720") # https://en.wikipedia.org/wiki/16:9_aspect_ratio
root.iconbitmap("ZL icon.ico")
root.title("Composition Calculator")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1) # almost all frames need to also expand by writing these two lines of code
# https://stackoverflow.com/questions/63973865/tkinter-treeview-resizing-the-treeview-to-fit-screen

ttk.Label(root, text="ZL_calculator_v11").grid(row=1, sticky="e") # tells what version is this calculator on the bottom right corner

main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nesw")
main_frame.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)

notebook = ttk.Notebook(main_frame)
notebook.grid(sticky="nesw", padx=5, pady=5)
notebook.enable_traversal()

#################
# Style Configs #
#################
style = ttk.Style()
style.configure("calculator.TLabel", font="TKDefaultFont 12")
style.configure("calculator.TButton", font="TKDefaultFont 8", width=1, height=1)
style.configure("calculator.Treeview", font="TKDefaultFont 12") # https://www.plus2net.com/python/tkinter-treeview-style.php
# style.configure("calculator.Treeview.Heading", font="TKDefaultFont 12") #https://stackoverflow.com/questions/46932332/tkinter-treeview-change-column-font-size

# style.configure("Input.TSpinbox", font="TKDefaultFont 12") # for some reason this doesn't work???
# style.configure("TEntry", font="TKDefaultFont 12") # same thing here???
# style.theme_use("clam") # I rather not...; only "clam" supports color changes...
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-style-layer.html

#################



##########################
# Composition Calculator #
##########################

calculator_frame = ttk.Frame(notebook)
notebook.add(calculator_frame, text="Composition Calculator")
calculator_frame.configure(padding=5) # this acts as an overall border around all widgets
calculator_frame.rowconfigure(0, weight=2) # for the main inputs
calculator_frame.rowconfigure(1, weight=1) # for the element & index entries
calculator_frame.rowconfigure(2, weight=2) # for the treeview widget
calculator_frame.columnconfigure(0, weight=1) # allows every subframes to expand the column space

console_frame = ttk.Frame(calculator_frame) # intended to be a 2x2 grid space
console_frame.grid(row=0, sticky="nesw")
console_frame.rowconfigure(0, weight=1)
console_frame.rowconfigure(1, weight=1)
console_frame.rowconfigure(2, weight=1)
# console_frame.columnconfigure(0, weight=1)

def only_floats(input_text):
    if input_text == ".": # only known bug: if more than 1 decimal point is accidently written, then can't ctrl+A delete everything
        return True
    try:
        float(input_text)
        return True
    except ValueError:
        return False
validation = root.register(only_floats)
# https://python-forum.io/thread-30593.html
# https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter
# https://tkdocs.com/tutorial/widgets.html#entry
# https://stackoverflow.com/questions/22410327/entry-tkinter-is-not-allowing-to-erase-data-if-selected-all-and-pressed-delete-o
# https://pythonassets.com/posts/textbox-entry-validation-in-tk-tkinter/
# https://www.pythontutorial.net/tkinter/tkinter-validation/

class Input: # has built-in validation and styling
    def __init__(self, parent, next_widget=True):
        self.Frame = ttk.Frame(parent)
        self.var = tk.StringVar()
        self.Label = ttk.Label(self.Frame, style="calculator.TLabel")
        self.Label.pack(side=tk.LEFT)
        self.Entry = ttk.Entry(
            self.Frame,
            textvariable=self.var,
            validate="key",
            validatecommand=(validation, "%S"),
            font="TKDefaultFont 12"
        )
        self.Entry.pack(side=tk.LEFT)
        if not next_widget:
            self.Entry.bind("<Tab>", self.focus_next_widget)

mass = Input(console_frame)
mass.Label.configure(text="Total Mass (g) : ")
mass.Frame.grid(row=0, column=0, sticky="w")

temperature = Input(console_frame)
temperature.Label.configure(text="Temperature (\u00B0C) : ")
temperature.Frame.grid(row=1, column=0, sticky="w")

pressure_var = tk.StringVar()
pressure_var.set("Total Calculated Vapor Pressure: ")
pressure_label = ttk.Label(console_frame, textvariable=pressure_var, style="calculator.TLabel")
pressure_label.grid(row=2, column=0, sticky="w")

pressure_warning = ttk.Label(console_frame, text="WARNING: Calculated vapor pressure over 2 atm!", style="calculator.TLabel", foreground="red")

# """CHANGED THIS OUT FOR APPLICATION MENUS (but may potentially bring it back)"""
# class Terminal: 
#     def __init__(self, parent):
#         self.Frame = ttk.Frame(parent)
#         self.screen = tk.Text(
#             self.Frame,
#             font="TKDefaultFont 12",
#             width=32, # so these parameter's are based on CHARACTER units, not normal
#             height=9 # changing height will also push down the display table; arbitrary number set here
#         )
#         self.screen.pack(fill=tk.BOTH)
#         self.screen.config(state="disabled") # https://www.geeksforgeeks.org/how-to-disable-an-entry-widget-in-tkinter/

#         self.cmd = ttk.Entry(self.Frame)
#         self.cmd.pack(fill=tk.X)

# terminal = Terminal(console_frame)
# terminal.Frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

# """Scrapped Code"""
# input_frame = ttk.Frame(console_frame) # this is brought back thanks to the terminal widget
# input_frame.pack(side=tk.LEFT, fill=tk.Y) # have to use pack method here!
# input_frame.rowconfigure(1, weight=1)
# input_frame.columnconfigure(0, weight=1)

element_index_frame = ttk.Frame(calculator_frame)
element_index_frame.grid(row=1, column=0, sticky="w")
ttk.Label(element_index_frame, text="Elements & Indices: ", style="calculator.TLabel").grid(row=0, sticky="w", pady=5) # Element & Indices label
class ElementIndex: # making a class here was SO MUCH BETTER; old code had a shit ton of exec() (see jupyter_notebook.ipynb in folder before)
    def __init__(self, parent): # originally had "elements" and "abbrev" as arg. but refactored it out
        self.Frame = ttk.Frame(parent)
        # self.elements = df.Name.to_list() # assigning attributes here is unnecessary
        # self.symbols = df.Symbol.to_list() # abbrev
        self.element_var = tk.StringVar()
        self.index_var = tk.StringVar() # tk.IntVar() will set default value to 0
        self.Combobox = AutoSuggestCombobox(self.Frame, textvariable=self.element_var, font="TKDefaultFont 12", width=15)
        self.Combobox.set_completion_list(df.Name.to_list(), df.Symbol.to_list())
        self.Combobox.pack(side=tk.LEFT)
        self.spinbox = ttk.Spinbox( # don't need tkinter variable to get values for spinbox
            self.Frame, 
            values=("", 2, 3, 4, 5, 6, 7, 8, 9, 10), 
            textvariable=self.index_var,
            validate="key", 
            validatecommand=(validation, "%S"),
            font="TKDefaultFont 13", # 12 weirdly did not had the right size as the element entry...
            width=2
        )
        self.spinbox.pack(side=tk.LEFT, padx=5) # https://www.geeksforgeeks.org/python-tkinter-spinbox/
        self.Button = ttk.Button(
            self.Frame, 
            text="\u00D7", # https://tex.stackexchange.com/questions/484229/package-inputenc-error-unicode-character-%C3%97-u00d7
            style="calculator.TButton",
            command=self.clear_entries
        )
        self.Button.pack(side=tk.LEFT)
        self.Button.bind("<FocusIn>", self.focus_next_widget)

    def clear_entries(self):
        self.Combobox.delete("0", tk.END)
        self.spinbox.delete("0", tk.END)

    def focus_next_widget(self, event): # we want if the user is tabbing to NOT focus on the clearing button widget; also work for the Terminal class!
        event.widget.tk_focusNext().focus()
        return "break"
    # https://stackoverflow.com/questions/52061933/getting-tab-key-to-go-to-next-field-with-tkinter-text-instead-of-indent 

elem_ind_widgets = [] # now this allows me to create as ElementIndex widgets as needed
for i in range(0, 5):
    exec_str1 = f"""
elem_ind{i+1} = ElementIndex(element_index_frame)
elem_ind{i+1}.Frame.grid(row=1, column={i}, padx=10) # must specify row otherwise it gets posted diagonally
elem_ind_widgets.append(elem_ind{i+1})
    """ # ok, so this works, but the indent fix is horrendous (still keeping it though)
    exec(exec_str1)

def get_molecular_form(*args): # *args to eat up arguments; may change this??
    symbols_re = {} # a dictionary ensures unique keys
    for i in args: 
        regex_find = re.findall("\(([^\(\)]+)\)", i.element_var.get()) # https://stackoverflow.com/questions/6208367/regex-to-match-stuff-between-parentheses
        if regex_find:
            symbols_re.update(
                {regex_find[0]: i.index_var.get()}
            )
        del regex_find
    
    return symbols_re

    
def calculate_composition(**kwargs): # this function expects the symbols_re dictionary to be inputted
    """Get mass"""
    m = float(mass.var.get())

    """Split symbols_re dict. keys and values"""
    molar_masses = []
    indices = []
    for i, j in kwargs.items():
        molar_masses.append(mass_lib[i])
        if j == "":
            indices.append(1)
        else:
            indices.append(int(j))
    molar_masses = np.array(molar_masses)
    indices = np.array(indices)
    print(molar_masses)
    
    """Calculate the total molecular weight"""
    mol_wts = molar_masses@indices # will help convert to g/mol.

    """Construct composition dataframe for return"""
    comp = pd.DataFrame( # decided with a df because of np compatibility
        zip(kwargs.keys(), indices, (m/mol_wts)*indices*molar_masses),  # (m/mol_wts)*indices
        columns=("Formula", "Indices", "Compositions") # tuple here because why not; "Elements" is called "Formula" instead for calculate_vapor_pressure()
    ) 
    # n_tot = comp["Mole fraction"].sum()
    # comp["Mole fraction"] = comp["Mole fraction"]/n_tot
    # print(comp, n_tot)
    return m, comp

    """Scrapped Code"""
    # molar_masses = np.array([mass_lib[i] for i in args[0].keys()])
    # indices = np.array([1 if i == "" else int(i) for i in args[0].values()])


def calculate_chamber_volume(l=120, r=15): # Default dimension: 15mm x 12cm; chamber shape: test tube
    hemi = (2/3)*pi*r**3 # the bottom of a test tube "looks" like a hemisphere
    cylinder = pi*r**2*(l-r) # the main body of a test tube is a cylinder

    return hemi + cylinder # and the sum of the two is the total volume; *units are in cubic mm!


def calculate_vapor_pressure(m, comp): # dependent on calculate_composition()
    T = float(temperature.var.get()) # has conditional under populate_calculator_tree()
    i_sum = comp.Indices.sum()
    yaws_merged =  yaws.merge(comp, how="inner", on="Formula") # used to do this with .query() and .isin(), was so much more work...; has conditional under populate_calculator_tree(); https://pandas.pydata.org/docs/reference/api/pandas.merge.html
    yaws_merged["Name"] = yaws_merged.apply(lambda x: f"{x.Name} ({x.Formula})", axis=1) # to help populate the treeview widget later; axis parameter here was important

    antoine = yaws_merged.query(f"{T} > Tmin & {T} < Tmax") # this will further filter the dataframe for elements with appropriate temp. range
    display(antoine, i_sum)
    ideal = pd.concat([yaws_merged, antoine]).drop_duplicates(keep=False) # set minus; there's an error in ref: https://stackoverflow.com/questions/18180763/set-difference-for-pandas

    if not antoine.empty:
        """Getting the Antoine Coefficients"""
        As = antoine.pop("A").to_numpy() # using .pop() here can make it easier to organize the final df, possibly saving memory?
        Bs = antoine.pop("B").to_numpy()
        Cs = antoine.pop("C").to_numpy()

        """Calculating the partial vapor pressures via Raoult's Law"""
        pure_pressures = 10**(As - Bs/(Cs + T)) # will give back pressure as mmHG
        pure_pressures /= 760 # formula: 760mmHg = 1 atm
        mole_frac = antoine.Indices.to_numpy()/i_sum # this is literally index/sum of index
        # print(mole_frac)
        antoine["Pressures"] = mole_frac*pure_pressures # Raoult's Law here; appending more onto the df
        
        """Appending and dropping information onto the split dataframe"""
        antoine.drop(columns=["Tmin", "Tmax"], inplace=True)
        antoine["Method"] = "Antoine Equation" # https://stackoverflow.com/questions/24039023/add-column-with-constant-value-to-pandas-dataframe

    if not ideal.empty:
        """Bring back the molar masses via mass_lib global variable"""
        molar_masses = np.array([mass_lib[i] for i in ideal.Formula])

        """Dropping information onto the split dataframe"""
        ideal = ideal[["Formula", "Name", "Indices", "Compositions"]] # keeping the formula column will help populate the treeview widget as IID's

        """Calculate individual pressures via Ideal Gas Law"""
        K = T + 273.17 # converting celsius to Kelvins
        V = calculate_chamber_volume()*1e-6 # 1 cubic m = 1000 L
        R = 0.082057 # using the atm unit specific gas constant! https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Physical_Properties_of_Matter/States_of_Matter/Properties_of_Gases/Gas_Laws/The_Ideal_Gas_Law
        ns = ideal.Compositions/molar_masses # should match in dimensions
        ideal["Pressures"] = (ns*R*K)/V # same as for the Antoine calculations

        """Appending information onto the split dataframe"""
        ideal["Method"] = "Ideal Gas law"

    if not (antoine.empty or ideal.empty): # De Morgan's Law here
        return pd.concat([antoine, ideal], axis=0) # most likely scenario
    elif antoine.empty:
        return ideal # for the case all of the element falls outside of the temperature range
    elif ideal.empty:
        return antoine # for the case none of the element falls outside of the temperature range

    """Scrapped code"""
    # names_formulas = pd.concat([antoine.pop(i) for i in ["Name", "Formula"]], axis=1) # https://stackoverflow.com/questions/49329569/how-do-you-pop-multiple-columns-off-a-pandas-dataframe-into-a-new-dataframe
    # antoine["Symbol"] = names_formulas.apply(lambda x: f"{x.Name} ({x.Formula})", axis=1) # https://stackoverflow.com/questions/58602169/why-doesnt-f-string-formatting-work-for-pandas; https://stackoverflow.com/questions/13331698/how-to-apply-a-function-to-two-columns-of-pandas-dataframe

def get_state(comp):
    T = float(temperature.var.get())
    T += 273.15 # converting from celsius to kelvins
    states = pd.concat( # will add a new column full of NaN (which is fine)
        [comp.merge( # merging this with comp
            df[["Symbol", "MeltingPoint", "BoilingPoint"]].rename(columns={"Symbol": "Formula"}), # isolating columns that matters only
            how="inner", 
            on="Formula"
        ), pd.DataFrame(columns=["State"])],
        axis=1
    )

    solids = states.query(f"{T} < MeltingPoint")
    if not solids.empty: # boolean array error: https://stackoverflow.com/questions/18548370/pandas-can-only-compare-identically-labeled-dataframe-objects-error
        states.loc[states.Formula.isin(solids.Formula), "State"] = "Solid" # https://stackoverflow.com/questions/38886080/why-use-loc-in-pandas

    liquids = states.query(f"{T} > MeltingPoint & {T} < BoilingPoint")
    if not liquids.empty:
        states.loc[states.Formula.isin(liquids.Formula), "State"] = "Liquid"

    gases = states.query(f"{T} > BoilingPoint")
    if not gases.empty:
        states.loc[states.Formula.isin(gases.Formula), "State"] = "Gas"

    return states[["Formula", "State"]]

display_table_frame = ttk.Frame(calculator_frame)
display_table_frame.grid(row=2, sticky="nesw")
display_table_frame.rowconfigure(1, weight=1) # this allows the display table to expand its row space
display_table_frame.columnconfigure(0, weight=1) # and this allows it to expand its column space

ttk.Label(display_table_frame, text="Display Table:", style="calculator.TLabel").grid(row=0, column=0, sticky="w", pady=5) # Display table label
ct_cols = (
    "Element", 
    "Index", 
    "Calculated mass (g)", 
    "State",
    "Partial Vapor Pressure (atm)", 
    "Method",
    "Toxicity",
    "Air Sensitivity"
) # "ct_cols" for "calculator_tree_columns"
calculator_tree = ttk.Treeview(
    display_table_frame, 
    style="calculator.Treeview",
    columns=ct_cols, # created columns, but haven't named them yet
    show="headings",
)
calculator_tree.grid(row=1, column=0, sticky="nesw")

for i in ct_cols:
    calculator_tree.column(i, width=tk.NO) # ChatGPT got me to this combination of parameters
    calculator_tree.heading(i, text=i) # now the columns are named

def populate_calculator_tree(*args):
    children = calculator_tree.get_children()
    if children:
        calculator_tree.delete(*children)

    symbols_re = get_molecular_form(*elem_ind_widgets) # polymorphism here
    if mass.var.get(): # .get() only works with tk.StringVar()?
        m, comp = calculate_composition(**symbols_re)
        # comp["Formula"] = comp.apply(lambda x: f"{df.loc[x.Formula].Name}") # come back later for renaming development
        for i in zip(comp.Formula, comp.Indices, comp.Compositions.round(3)): # there has to be a better way to iterate through rows
            calculator_tree.insert(
                "",
                tk.END,
                iid=i[0], # making the index ID element symbols
                values=i
            )

        from IPython.display import display

    if not comp.empty and temperature.var.get(): # the composition is required to do Raoult's Law
        vapor = calculate_vapor_pressure(m, comp)
        total_vapor_pressure = vapor.Pressures.sum() # better to sum before setting to scientific notation
        vapor.Pressures = vapor.apply(lambda x: "{:.3e}".format(x.Pressures), axis=1) # https://stackoverflow.com/questions/67638356/scientific-notation-for-a-list-of-integers-in-python
        
        states = get_state(comp)
        vapor_states = vapor.merge(states, how="inner", on="Formula") # must merge in order to properly assign states to elements
        for i in zip(vapor_states.Formula, vapor_states.State, vapor_states.Pressures, vapor_states.Method):
            for n, j in enumerate(["State", "Partial Vapor Pressure (atm)", "Method"]): # double iteration, not good
                calculator_tree.set( # https://stackoverflow.com/questions/68272925/tkinter-treeview-insert-value-at-the-last-row-of-a-specific-column
                    i[0], # iid
                    column=j,
                    value=i[n+1]
                )   

        if total_vapor_pressure >= 2:
            pressure_warning.tkraise()
            pressure_warning.grid(row=2, column=1, sticky="w", padx=5)
        elif total_vapor_pressure < 2:
            pressure_warning.grid_forget() # there's specific geometry manager forget methods???

        pressure_var.set("Total Calculated Vapor Pressure: " + str(total_vapor_pressure.round(3)) + " atm")
        get_state(comp)

    """Scrapped code"""
    # if comp: # only populate if there is a composition calculation to be made # removing safety for now

    # elems, inds = symbols_re.keys(), list(symbols_re.values()) # trying to not typecast as much as possible
    # while "" in inds:
    #     n = inds.index("")
    #     inds.remove("")
    #     inds.insert(n, "1")
    # try:
    #     del n
    # except UnboundLocalError:
    #     pass # try and except clause here rather than "del n" in while loop to prevent constant assignment of the variable


for i in range(1, 6):
    exec_str2 = f"""
elem_ind{i}.element_var.trace_add('write', populate_calculator_tree)
elem_ind{i}.index_var.trace_add('write', populate_calculator_tree)
    """
    exec(exec_str2)
mass.var.trace_add("write", populate_calculator_tree) # for the case if mass is messed with mid-way
temperature.var.trace_add("write", populate_calculator_tree) # same with temperature

#####################
# Atomic Properties #
#####################

properties = df.drop(columns="CPKHexColor").fillna("") # the "CPKHexColor" column and its info are not relevant for this section; making NaN val. blank
# https://www.geeksforgeeks.org/replace-nan-values-with-zeros-in-pandas-dataframe/
cols = properties.columns.to_list()

properties_frame = ttk.Frame(notebook)
notebook.add(properties_frame, text="Atomic Properties")
properties_frame.columnconfigure(0, weight=1)
properties_frame.rowconfigure(0, weight=1)

properties_tree = ttk.Treeview(
    properties_frame,
    columns=cols, # created columns but haven't named them yet
    show="headings" # now treeview only shows headings
)
properties_tree.grid(row=0, column=0, sticky="nesw")

for i in cols:
    properties_tree.column(i, stretch=False, width=100)
    properties_tree.heading(i, text=i) # now the columns are named

for n in properties.index:
    properties_tree.insert(
        "",
        tk.END,
        iid=n,
        values=properties.iloc[n].to_list()
    )

properties_scrollbar_x = ttk.Scrollbar(properties_frame, orient=tk.HORIZONTAL)
properties_scrollbar_x.grid(row=1, column=0, sticky="ew")
properties_scrollbar_x.configure(command=properties_tree.xview)
properties_tree.configure(xscrollcommand=properties_scrollbar_x.set)

properties_scrollbar_y = ttk.Scrollbar(properties_frame, orient=tk.VERTICAL)
properties_scrollbar_y.grid(row=0, column=1, sticky="ns")
properties_scrollbar_y.configure(command=properties_tree.yview)
properties_tree.configure(yscrollcommand=properties_scrollbar_y.set)

def roll_wheel(event): # default scroll speed for the x-axis was really slow for some reason; this code fixed it
    direction = 0
    if event.num == 5 or event.delta == -120:
        direction = 20
    if event.num == 4 or event.delta == 120:
        direction = -20
    event.widget.xview_scroll(direction, tk.UNITS)
properties_tree.bind("<Shift-MouseWheel>", lambda event: roll_wheel(event))
# https://stackoverflow.com/questions/6863921/python-tkinter-canvas-xview-units

if __name__ == "__main__":
    # import ctypes
    # ctypes.windll.shcore.SetProcessDpiAwareness(1)

    root.mainloop()

    # root.withdraw()
    # root.destroy() # for cell magic
    # https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard

    # from IPython.display import display
    # display(
    #     yaws.query("Formula == 'Xe' or Formula == 'Ag'")[["A", "B", "C"]]
    # )

# https://www.tutorialspoint.com/how-to-disable-column-resizing-in-a-treeview-widget-in-tkinter
# https://wiki.tcl-lang.org/page/Drag+and+Drop+Notebook+Tabs
# https://github.com/TkinterEP/ttkwidgets/blob/master/ttkwidgets/table.py
# https://stackoverflow.com/questions/69219000/how-to-set-width-of-text-widget-in-tkinter-to-get-text-widget-equal-to-length-of