# I used Google Gemini to make this quick for me

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

class AutoResizingEntry(ttk.Entry):
    """
    A ttk.Entry widget that automatically resizes its width
    to fit the content typed into it.
    """
    def __init__(self, master=None, **kwargs):
        """
        Initialize the AutoResizingEntry widget.

        Args:
            master: The parent widget.
            **kwargs: Additional keyword arguments for the ttk.Entry widget.
        """
        # A minimum width can be specified in the kwargs
        self.min_width = kwargs.pop('min_width', 1)

        super().__init__(master, **kwargs)

        # Get the font object for the widget
        self.font = tkfont.Font(font=self['font'])

        # Create a variable to hold the entry's text
        self.var = tk.StringVar()
        self.config(textvariable=self.var)

        # Add a trace to the variable to call the resize method on write
        self.var.trace_add('write', self._resize)

        # Call resize initially to set the starting width
        self._resize()

    def _resize(self, *args):
        """
        Private method to handle the resizing of the entry widget.
        This is called whenever the content of the entry's variable changes.
        """
        # Measure the width of the current text in pixels
        text_width_pixels = self.font.measure(self.var.get())

        # Measure the width of a single '0' character to approximate
        # the width of one character unit for the entry widget.
        # This is a common way to translate pixel width to character width.
        zero_width_pixels = self.font.measure('0')

        if zero_width_pixels > 0:
            # Calculate the required width in character units
            # Add a small buffer (e.g., 1 character) for cursor visibility
            new_width = (text_width_pixels // zero_width_pixels) + 1
        else:
            # Fallback based on text length if '0' has no width
            new_width = len(self.var.get()) + 1


        # Ensure the width is not less than the specified minimum width
        final_width = max(self.min_width, new_width)

        # Update the widget's width configuration
        self.config(width=final_width)


if __name__ == '__main__':
    # --- Demo Application ---
    root = tk.Tk()
    root.title("Auto-Resizing Entry Demo")
    root.geometry("500x300")

    # Apply a theme
    style = ttk.Style(root)
    style.theme_use('clam')

    # Main frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # --- Auto-Resizing Entry ---
    ttk.Label(main_frame, text="Auto-Resizing Entry:").pack(pady=(0, 5), anchor='w')
    auto_entry = AutoResizingEntry(main_frame, min_width=20, font=('Helvetica', 12))
    auto_entry.pack(fill=tk.X, expand=True, pady=(0, 20))
    auto_entry.insert(0, "Type here and watch it grow...")


    # --- Standard Entry for Comparison ---
    ttk.Label(main_frame, text="Standard ttk.Entry:").pack(pady=(0, 5), anchor='w')
    standard_entry = ttk.Entry(main_frame, font=('Helvetica', 12))
    standard_entry.pack(fill=tk.X, expand=True, pady=(0, 20))
    standard_entry.insert(0, "This one has a fixed width.")
    
    # --- Another Label to show layout ---
    ttk.Label(main_frame, text="Another widget below.").pack(pady=(10, 0), anchor='w')


    # Start the main loop
    root.mainloop()
