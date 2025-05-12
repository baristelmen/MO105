import tkinter as tk
from datetime import datetime
import logging

class CopyrightConfig(tk.Frame):
    def __init__(self, parent, width: int, height: int):
        super().__init__(parent, width=width, height=height, bg="red")

        # Prevent frame from resizing to fit child widgets
        self.grid_propagate(False)

        # Highlight border to visualize frame bounds
        self.config(highlightbackground="blue", highlightthickness=2)

        # Place the frame on the parent
        self.grid(row=0, column=0, padx=5, pady=5)

        # Grid setup for 3 equal sections
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left label
        self.status_label = tk.Label(self, text="Status: Connected | COM3", anchor="w", bg="lightgray")
        self.status_label.grid(row=0, column=0, sticky="w", padx=10)

        # Right label
        self.version_label = tk.Label(self, text="Version: v2.0.1", anchor="e", bg="lightgray")
        self.version_label.grid(row=0, column=2, sticky="e", padx=10)

        # Center label: truly centered using place()
        self.center_label = tk.Label(self, bg="lightgray")
        self.center_label.place(relx=0.5, rely=0.5, anchor="center")  # Absolute center of the frame
        self.update_clock()  # Start the update loop

        self.logger = logging.getLogger("AppLogger")
        self.logger.info("Experimental config frame is initialized")

    def update_clock(self):
        now = datetime.now().strftime("%A, %d %B %Y %H:%M:%S")  # With newline
        self.center_label.config(text=now)
        self.after(1000, self.update_clock)  # Call again after 1 second