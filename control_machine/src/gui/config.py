import tkinter as tk
import logging

class ExperimentalConfig(tk.Frame):
    def __init__(self, parent, width: int, height: int):
        super().__init__(parent, width=width, height=height, bg="red")

        # Prevent frame from resizing to fit child widgets
        self.grid_propagate(False)

        # Highlight border to visualize frame bounds
        self.config(highlightbackground="blue", highlightthickness=2)

        # Create widgets
        self.create_widgets()

        # Place the frame on the parent
        self.grid(row=0, column=0, padx=5, pady=5)

        # Allow columns to expand
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(99, weight=1)  # Spacer row at bottom

        self.logger = logging.getLogger("AppLogger")
        self.logger.info("Experimental config frame is initialized")

    def create_widgets(self):
        """Creates the widgets for the experimental configuration frame"""
        row_num = 0

        # Config title row
        row_frame = tk.Frame(self, bg="black")
        row_frame.grid(row=row_num, column=0, columnspan=3, sticky="ew", padx=0, pady=(5, 5))

        exp_label = tk.Label(row_frame, text="Config", bg="black", fg="white", font=("Helvetica", 12))
        exp_label.pack(anchor="center")

        row_num += 1

        ## Move duration label
        md_label = tk.Label(self, text="Move duration:", bg="red", fg="white", font=("Helvetica", 12))
        md_label.grid(row=row_num, column=0, padx=10, pady=(5,5), sticky="nw")

        ## Move duration entry
        self.md_entry = tk.Entry(self, font=("Helvetica", 12))
        self.md_entry.grid(row=row_num, column=1, padx=10, pady=(5,5), sticky="ew")
        self.md_entry.insert(0, "5")

        ## Unit label
        mdu_label = tk.Label(self, text="s", bg="red", fg="white", font=("Helvetica", 12))
        mdu_label.grid(row=row_num, column=2, padx=10, pady=(5,5), sticky="ew")

        row_num += 1
        # Frequency label
        f_label = tk.Label(self, text="Frequency:", bg="red", fg="white", font=("Helvetica", 12))
        f_label.grid(row=row_num, column=0, padx=10, pady=(5,5), sticky="nw")

        # Frequency entry
        self.f_entry = tk.Entry(self, font=("Helvetica", 12), width=10)
        self.f_entry.grid(row=row_num, column=1, padx=10, pady=(5,5), sticky="ew")
        self.f_entry.insert(0, "5")

        # Frequency unit label
        fu_label = tk.Label(self, text="Hz", bg="red", fg="white", font=("Helvetica", 12))
        fu_label.grid(row=row_num, column=2, padx=10, pady=(5,5), sticky="ew")
