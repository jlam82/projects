import tkinter as tk
from tkinter import ttk # like messagebox and etc., must import seperately
from tkinter import messagebox 
from tkinter import simpledialog 
from tkinter import filedialog 
from pathlib import Path

root = tk.Tk()
font_size = tk.IntVar(value=12) 
root.title("My Diary")
root.geometry("800x600+300+300")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
# root.configure(background="#888") # supposedly added so the form_frame can be seen

"""sub-frame for form""" # he added this off camera
form_frame = ttk.Frame(root) # can replace almost all original tk. widgets with ttk.
form_frame.grid(sticky=tk.N+tk.E+tk.W+tk.S, padx=5, pady=5)
form_frame.columnconfigure(0, weight=1)
form_frame.rowconfigure(5, weight=1)

subj_frame = ttk.Frame(form_frame)
subj_frame.columnconfigure(1, weight=1)
subject_var = tk.StringVar()
ttk.Label(subj_frame, text="Subject: ").grid(sticky="we", padx=5, pady=5)
ttk.Entry(subj_frame, textvariable=subject_var).grid(row=0, column=1, sticky=tk.E + tk.W)
subj_frame.grid(sticky="ew")

cat_frame = ttk.Frame(form_frame)
cat_frame.columnconfigure(1, weight=1)
cat_var = tk.StringVar()
categories = ["Work", "Hobbies", "Health", "Bills"]
ttk.Label(cat_frame, text="Category: ").grid(row=1, column=0, sticky=tk.E + tk.W, padx=5, pady=5)

ttk.OptionMenu(
    cat_frame, 
    cat_var,
    categories[0], # ttk.OptionMenu slightly different from tk.'s; have to specify a default
    *categories
).grid(row=1, column=1, sticky=tk.E + tk.W, padx=5, pady=5)
cat_frame.grid(sticky="ew")

private_var = tk.BooleanVar(value=False)
private_inp = ttk.Checkbutton(form_frame, variable=private_var, text="Private?")
private_inp.grid(ipadx=5, ipady=5, sticky="w") # HE ADDED THIS BACK

"""datestamp""" # he added this off-camera too
datestamp_var = tk.StringVar(value="none")
datestamp_frame = ttk.Frame(form_frame)
for i in ("None", "Date", "Date+Time"):
    ttk.Radiobutton(
        datestamp_frame,
        text=i,
        value=i,
        variable=datestamp_var
    ).pack(side=tk.LEFT) # like checkoff buttons, but meant to be used in a group and only 1 can be on
datestamp_frame.grid(row=2, sticky="e")

message_frame = ttk.LabelFrame(form_frame, text="Message")
message_frame.columnconfigure(0, weight=1)
message_inp = tk.Text(message_frame) # there is no ttk. text widget
message_inp.grid(sticky="nesw")
scrollbar = ttk.Scrollbar(message_frame)
scrollbar.grid(row=0, column=1, sticky="nse")
message_frame.grid(sticky="nesw")
scrollbar.configure(command=message_inp.yview)
message_inp.configure(yscrollcommand=scrollbar.set)

save_btn = ttk.Button(root, text="Save") # HE BROUGHT THIS BACK TOO
save_btn.grid(sticky=tk.E, ipadx=5, ipady=5)

status_var = tk.StringVar()
status_bar = ttk.Label(root, textvariable=status_var)
status_bar.grid(row=100, ipadx=5, ipady=5, padx=5, pady=5, sticky="we")

"""changes from tk. widgets to ttk. widgets ends here, with out status_bar being the last"""

def weaksauce_encrypt(text, password):
    offset = sum([ord(i) for i in password])
    encoded = "".join(
        chr(min(ord(i) + offset, 2**20)) for i in text
    )
    return encoded

def weaksauce_decrypt(text, password): 
    offset = sum([ord(i) for i in password]) 
    decoded = "".join(
        chr(max(ord(i) - offset, 0)) for i in text
    )
    return decoded 

def open_file():
    file_path = filedialog.askopenfilename(
        title="Select a file to open",
        filetypes=[("Secret", "*.secret"), ("Text", "*.txt")]
    )
    if not file_path:
        return
    fp = Path(file_path) # path object
    filename = fp.stem
    category, subject = filename.split(" - ")
    message = fp.read_text()
    if fp.suffix == ".secret":
        password = simpledialog.askstring(
            "Enter Password",
            "Enter the password  used to encrypt the file."
        )
        message = weaksauce_decrypt(message, password)

    cat_var.set(category)
    subject_var.set(subject)
    message_inp.delete("1.0", tk.END)
    message_inp.insert("1.0", message)
    
def save():
    subject = subject_var.get()
    category = cat_var.get()
    private = private_var.get()
    message = message_inp.get("1.0", tk.END)
    extension = "txt" if not private else "secret"
    filename = f"{category} - {subject}.{extension}"
    if private:
        password = simpledialog.askstring(
            "Enter password",
            "Enter a password to encrypt a message."
        )
        message = weaksauce_encrypt(message, password)  
    with open(filename, "w") as fh:
        fh.write(message)
    status_var.set(f"Message was saved as {filename}")
    messagebox.showinfo("Saved", f"Message was saved to {filename}")

def private_warn(*arg):
    private = private_var.get()
    if private:
        response = messagebox.askokcancel(
            "Are you sure?",
            "Do you really want to encrypt this message?"
        )
        if not response:
            private_var.set(False)

private_var.trace_add("write", private_warn)

def check_filename(*args):
    subject = subject_var.get()
    category = cat_var.get()
    filename = f"{category} - {subject}.txt"
    if Path(filename).exists():
        status_var.set(f"WARNING: {filename} already exists!")
    else:
        status_var.set("")

subject_var.trace_add("write", check_filename)
cat_var.trace_add("write", check_filename)
private_var.trace_add("write", check_filename)

def set_font_size(*args):
    size = font_size.get()
    message_inp.configure(font=f"TKDefault {size}")

set_font_size()
font_size.trace_add("write", set_font_size)

menu = tk.Menu(root)
root.configure(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=root.destroy)

options_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Options", menu=options_menu)
options_menu.add_checkbutton(label="Private", variable=private_var)

help_menu = tk.Menu(menu, tearoff=0)
help_menu.add_command(
    label="About",
    command=lambda: messagebox.showinfo("About", "My Tkinter Diary")
)
menu.add_cascade(label="Help", menu=help_menu)

size_menu = tk.Menu(options_menu, tearoff=0)
for i in range(6, 33, 2):
    size_menu.add_radiobutton(label=i, value=i, variable=font_size)

options_menu.add_cascade(menu=size_menu, label="Font Size")

root.mainloop()