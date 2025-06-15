# REFERENCES:
# https://stackoverflow.com/questions/68685881/how-to-add-an-edit-option-to-tkinter-matplotlib-navigation-toolbar
# https://www.youtube.com/watch?v=kQ_HizfSMH4

import tkinter as tk 
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas, parent):
        self.toolitems = ( # print "NavigationToolbar2Tk.toolitems" to see the default images
            ("Save", "Save current progress as a JSON", "filesave", "save_figure"), # this comma here is necessary?
        )
        super().__init__(canvas, parent)

    def add_custom_button(self, btn, before=False, where=0):
        if before: # not preferred but it works
            btn.pack(side=tk.LEFT, padx=2, pady=2, before=self.winfo_children()[where])
        else:
            btn.pack(side=tk.LEFT, padx=2, pady=2, after=self.winfo_children()[where])

    def override_default_tool_command(self, default_tool_command, new_command):
        """
        Overrides the callback function for a specific tool in the toolbar.
        Takes in the name of the tool as defined in the 'toolitems' tuple
        (e.g., 'Home', 'Back', 'Forward', etc.) and set a new command at its place.
        """
        for name, tooltip, image, method in self.toolitems:
            if method == default_tool_command: # I have no idea why this nesting is necessary
                if hasattr(self, '_buttons') and name in self._buttons:
                    self._buttons[name].config(command=new_command.__get__(self, self.__class__))

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    root = tk.Tk()
    fig, ax = plt.subplots()

    toolbar_frame = ttk.Frame(root)
    toolbar_frame.pack(fill=tk.X)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()

    toolbar = CustomToolbar(canvas, toolbar_frame)
    toolbar.update()
    toolbar.pack(side=tk.TOP, fill=tk.X)

    def new_command(*args): # callback function must eat up all arguments
        print("Hello World!")

    toolbar.override_default_tool_command("save_figure", new_command)

    root.mainloop()

# SCRAPPED CODE
# else:
#     raise NameError("Default matplotlib command not found.")

# def override_default_tool_button(self, default_name, custom_button_class):
#     original_btn = self._buttons[default_name]

#     original_pack_info = original_btn.pack_info()
#     original_tooltip, original_image = "", None
#     for name, tooltip, image, method in self.toolitems:
#         if name == default_name:
#             original_tooltip = tooltip
#             original_image = image
#             break
#     img = Image.open(f"../images/mpl-data_images/{original_image}.png")
#     mpl_img = ImageTk.PhotoImage(img)

#     original_btn.destroy()

#     new_btn = custom_button_class(self, image=mpl_img)
#     new_btn.pack(**original_pack_info)

#     self._buttons[default_name] = new_btn