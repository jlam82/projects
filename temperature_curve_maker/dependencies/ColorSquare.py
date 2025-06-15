# Refactored by Google Gemini

import tkinter as tk
from tkinter import ttk
import random

class ColorSquare:
    """
    Helper class for Step.py

    Create an instance of a colored square with a white border.
    This version simulates RGBA transparency against a known white background.
    Call .canvas.<geometry_manager>() to pack the widget onto the parent frame.
    """
    def __init__(self, parent, hexcode, alpha=1.0, canvas_size=15, border_size=3):
        """
        Initializes the ColorSquare widget.

        Args:
            parent: The parent tkinter widget.
            hexcode (str): The hexadecimal color code for the square.
            alpha (float): The opacity level, from 0.0 (transparent) to 1.0 (opaque).
            canvas_size (int): The total width and height of the canvas widget.
            border_size (int): The size of the border within the canvas.
        """
        # The background color is constant white
        self.bg_color_rgb = (255, 255, 255)
        self.canvas = tk.Canvas(
            parent, width=canvas_size, height=canvas_size, bg='#FFFFFF', highlightthickness=0
        )
        self.border_size = border_size
        self.canvas_size = canvas_size

        # Store original color and alpha for later changes
        self.original_hexcode = hexcode
        self.alpha = alpha

        # Calculate the initial blended color
        blended_hex = self._get_blended_color(hexcode, alpha)

        # Create the inner rectangle that represents the color
        self.color_sq = self.canvas.create_rectangle(
            border_size, border_size,
            canvas_size - border_size, canvas_size - border_size,
            fill=blended_hex, outline="black"
        )

    def _get_blended_color(self, hexcode, alpha):
        """
        Calculates the blended color against a white background.

        Args:
            hexcode (str): The foreground color.
            alpha (float): The opacity level.

        Returns:
            str: The resulting solid hex color string.
        """
        # 1. Convert foreground hex to RGB
        hexcode = hexcode.lstrip('#')
        fg_r, fg_g, fg_b = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))

        # 2. Get background RGB
        bg_r, bg_g, bg_b = self.bg_color_rgb

        # 3. Apply the alpha blending formula for each channel
        #    Result = (Foreground * Alpha) + (Background * (1 - Alpha))
        final_r = int((fg_r * alpha) + (bg_r * (1 - alpha)))
        final_g = int((fg_g * alpha) + (bg_g * (1 - alpha)))
        final_b = int((fg_b * alpha) + (bg_b * (1 - alpha)))

        # 4. Convert the final RGB back to a hex string for Tkinter
        return f'#{final_r:02x}{final_g:02x}{final_b:02x}'

    def change_color(self, new_hexcode=None, new_alpha=None):
        """
        Changes the fill color and/or alpha of the square.

        Args:
            new_hexcode (str, optional): The new hexadecimal color code. Defaults to None.
            new_alpha (float, optional): The new alpha value. Defaults to None.
        """
        # Update the stored color/alpha if new values are provided
        if new_hexcode is not None:
            self.original_hexcode = new_hexcode
        if new_alpha is not None:
            self.alpha = new_alpha

        # Recalculate the blended color with the current properties
        blended_hex = self._get_blended_color(self.original_hexcode, self.alpha)
        self.canvas.itemconfig(self.color_sq, fill=blended_hex)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Alpha Blender")
    root.geometry("300x150")

    # --- WIDGET SETUP ---
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill="both", expand=True)

    # Frame to hold the color square and label
    display_frame = ttk.Frame(main_frame)
    display_frame.pack(pady=5)

    # The color we will be manipulating
    base_color = "#0000FF" # Blue

    # Create the initial color square
    color_square = ColorSquare(display_frame, base_color, alpha=1.0, canvas_size=40, border_size=5)
    color_square.canvas.pack(side=tk.LEFT, padx=(0, 10))

    # Add a label next to it
    ttk.Label(display_frame, text="PID 1").pack(side=tk.LEFT)

    # --- CONTROLS for DEMONSTRATION ---
    controls_frame = ttk.Frame(main_frame)
    controls_frame.pack(pady=10)

    # Alpha Slider
    alpha_label = ttk.Label(controls_frame, text="Alpha:")
    alpha_label.pack(side=tk.LEFT)

    alpha_var = tk.DoubleVar(value=1.0)
    alpha_slider = ttk.Scale(
        controls_frame,
        from_=0.0,
        to=1.0,
        orient="horizontal",
        variable=alpha_var,
        command=lambda new_val: color_square.change_color(new_alpha=float(new_val))
    )
    alpha_slider.pack(side=tk.LEFT, padx=5)

    # Random Color Button
    def update_the_color():
        """Generates a random hex color and calls the change_color method."""
        random_color = f'#{random.randint(0, 0xFFFFFF):06x}'
        color_square.change_color(new_hexcode=random_color)
        print(f"Changing base color to: {random_color}")

    change_button = ttk.Button(
        controls_frame,
        text="Random Color",
        command=update_the_color
    )
    change_button.pack(side=tk.LEFT, padx=5)

    root.mainloop()
