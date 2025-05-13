import tkinter as tk
import os
from tkinter import filedialog
import logging

class OutputConfig(tk.Frame):
    def __init__(self, parent, width: int, height: int):
        super().__init__(parent, width=width, height=height, bg="white")

        # Prevent frame from resizing to fit child widgets
        self.grid_propagate(False)

        # Highlight border to visualize frame bounds
        self.config(highlightbackground="blue", highlightthickness=2)

        # Place the frame on the parent
        self.grid(row=0, column=0, padx=5, pady=5)

        # Allow columns to expand
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(99, weight=1)  # Spacer row at bottom

        row_num = 0

        # Config title row
        row_frame = tk.Frame(self, bg="black")
        row_frame.grid(row = row_num, column=0, columnspan=3, sticky="ew", padx=0, pady=(5, 5))

        op_label = tk.Label(row_frame, text="Output parameters", bg="black", fg="white", font=("Helvetica", 12))
        op_label.pack(anchor="center")

        row_num += 1

        self.file_path = tk.StringVar()
        self.file_path.set(os.path.join(os.getcwd(), "output.txt"))  # default file

        # Folder label
        fl_label = tk.Label(self, text="Current folder:", bg="white", fg="black", font=("Helvetica", 12))
        fl_label.grid(row=row_num, column=0, padx=10, pady=(5,5), sticky="nw")

        # Folder entry
        self.file_path = tk.StringVar(value="")  # Start empty
        self.fe_entry = tk.Entry(self, textvariable=self.file_path, width=10, state='readonly')
        self.fe_entry.grid(row=row_num, column=1, padx=10, pady=(5,5), sticky="ew")

        # Button
        button = tk.Button(self, text="Browse", command=self.select_output_file)
        button.grid(row = row_num, column=2, padx=5, pady=5, sticky="ew")

        self.logger = logging.getLogger("AppLogger")
        self.logger.info("Output frame is initialized")

    def select_output_file(self):
        selected_file = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            initialfile="",  # <- Keeps filename box empty
            title="Select output file",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if selected_file:
            if not selected_file.lower().endswith(".txt"):
                selected_file += ".txt"
            self.file_path.set(selected_file)
            self.logger.info(f"Output file selected: {selected_file}")