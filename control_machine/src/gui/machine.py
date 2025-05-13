import tkinter as tk
import logging

class MachineConfig(tk.Frame):
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
        row_frame.grid(row=row_num, column=0, columnspan=3, sticky="ew", padx=0, pady=(5, 5))

        mp_label = tk.Label(row_frame, text="Machine parameters", bg="black", fg="white", font=("Helvetica", 12))
        mp_label.pack(anchor="center")

        row_num += 1
        # Load to Voltage label
        lv_label = tk.Label(self, text="Load to Voltage:", bg="white", fg="black", font=("Helvetica", 12))
        lv_label.grid(row=row_num, column=0, padx=10, pady=(5,5), sticky="nw")

        ## Read only entry with a default value
        self.lv_var = tk.StringVar()
        self.lv_entry = tk.Entry(self, font=("Helvetica", 12), width=10, textvariable=self.lv_var, state='readonly')
        self.lv_entry.grid(row=row_num, column=1, padx=10, pady=(5,5), sticky="ew")
        self.lv_var.set("0")

        # Load to Voltage unit label
        lvu_label = tk.Label(self, text="kg/V", bg="white", fg="black", font=("Helvetica", 12))
        lvu_label.grid(row = row_num, column=2, padx=10, pady=(5,5), sticky="ew")

        row_num += 1
        # Normal Voltage label
        nv_label = tk.Label(self, text="Normal voltage:", bg="white", fg="black", font=("Helvetica", 12))
        nv_label.grid(row=row_num, column=0, padx=10, pady=(5,5), sticky="nw")

        # Normal Voltage entry
        self.nv_var = tk.StringVar()
        self.nv_entry = tk.Entry(self, font=("Helvetica", 12), width=10, textvariable=self.nv_var, state='readonly')
        self.nv_entry.grid(row=row_num, column=1, padx=10, pady=(5,5), sticky="ew")
        self.nv_var.set("0")

        # Normal Voltage unit label
        nvu_label = tk.Label(self, text="V", bg="white", fg="black", font=("Helvetica", 12))
        nvu_label.grid(row = row_num, column=2, padx=10, pady=(5,5), sticky="ew")

        self.logger = logging.getLogger("AppLogger")
        self.logger.info("Machine frame is initialized")