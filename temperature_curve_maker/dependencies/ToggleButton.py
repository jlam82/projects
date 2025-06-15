# REFERENCES: https://stackoverflow.com/questions/23353746/how-to-make-button-in-python-tkinter-stay-pressed-until-another-one-is-pressed

import tkinter as tk
from tkinter import ttk

class ToggleButton(ttk.Button):
    def __init__(self, master, callback_func=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.callback_func = callback_func
        self.pressed = False
        self.configure(takefocus=False, command=self.toggle)
        
    def toggle(self):
        if self.pressed: # we want to then "unpress" the button
            self.state(["!pressed"])
            self.pressed = False
        else: # and vice versa
            self.state(["pressed"])
            self.pressed = True

        if self.callback_func:
            self.callback_func()

if __name__ == "__main__":
    root = tk.Tk()

    def callback_func():
        print("Hello World!")

    ToggleButton(root, callback_func=callback_func).pack()

    root.mainloop()