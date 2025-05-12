import tkinter as tk
from tkinter import ttk
import logging

class DataTable(tk.Frame):
    def __init__(self, parent, width: int, height: int):
        super().__init__(parent, width=width, height=height, bg="red")

        self.grid_propagate(False)

        # Highlight border to visualize frame bounds
        self.config(highlightbackground="blue", highlightthickness=2)
        
        # Place the frame on the parent
        self.grid(row=0, column=0, sticky="ew", padx=0, pady=(5, 5))

        # Add the Treeview table

        columns_def = ("id", "Time", "Load (kg)", "Force (N)")

        self.table = ttk.Treeview(self, columns=columns_def, show="headings", height=10)
        for col in columns_def:
            self.table.heading(col, text=col)
            self.table.column(col, width=90, anchor='center')
        self.table.grid(row=0, column=0, sticky="nsew")

        # Add the vertical scrollbar
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")  # 'ns' means up and down

        # Configure the Treeview to use the scrollbar
        self.table.config(yscrollcommand=self.scrollbar.set)

        self.grid_rowconfigure(0, weight=1)

        self.logger = logging.getLogger("AppLogger")
        self.logger.info("Data frame is initialized")

    def add_row(self, data):
        """Add a row to the table with sample data"""
        # You can add custom logic here to generate new values dynamically
        item_id  = self.table.insert('', 'end', values=data)

        ## Automatically scroll to the last row
        self.table.see(item_id)

    def update_row(self, index, new_values):
        """Update an existing row at the given index"""
        items = self.table.get_children()  # Get all item IDs
        if index < len(items):
            item_id = items[index]  # Get the item ID at the specified index
            self.table.item(item_id, values=new_values)
        else:
            print("Index out of range")

    def clear_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

    def has_data(self):
        """Check if the table has any rows"""
        return bool(self.table.get_children())