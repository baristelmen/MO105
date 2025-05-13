import tkinter as tk
from tkinter import ttk
from src.gui.config import ExperimentalConfig
from src.gui.machine import MachineConfig
from src.gui.output import OutputConfig
from src.gui.log import LogFrame
from src.gui.control import ButtonPanel
from src.gui.data import DataTable
from src.gui.copyright import CopyrightConfig
from src.gui.menubar import MenuBar
import logging
import serial

# Utility function
def disable_frame(frame: tk.Frame):
    for child in frame.winfo_children():
        try:
            child.configure(state="disabled")
        except tk.TclError:
            pass  # Not all widgets support the 'state' option

class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = 0

        start_width = 820
        start_height = 600

        self.geometry(f"{start_width}x{start_height}")
        self.title("Traction command and data read")
        self.resizable(False, False)
        self.config(bg="grey")

        self.columnconfigure(0, weight=0)  # Fixed width
        self.columnconfigure(1, weight=1)  # Only used by log_app to stretch

        # Only initialize the menu bar at first
        self.menubar = MenuBar(self, on_port_selected=self.check_port)
        self.config(menu=self.menubar)

        self.log_app = LogFrame(self, 400, 60)
        self.log_app.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.copyright_app = CopyrightConfig(self, 400, 30)
        self.copyright_app.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.logger = logging.getLogger("AppLogger")
        self.logger.info("Welcome to the Traction command and data read application")
        self.logger.info("Initializing the main window")
        self.logger.info("Please select a COM port from the menu")

    ## It is to check if the correct port is selected
    ## and to initialize the main UI
    def check_port(self, selected_port):
        try:
            connection = serial.Serial(port =selected_port, baudrate=9600, timeout=1)
        except serial.SerialException as e:
            self.logger.error(f"Error connecting to port {selected_port}: {e}")
            self.logger.error("Please select a different COM port from the menu or refresh the list")
            return
        
        connection.close()
        self.init_main_ui(selected_port)

    def init_main_ui(self, selected_port):
        
        # Here you can store the port if needed
        self.selected_port = selected_port

        self.log_app = LogFrame(self, 400, 60)
        self.log_app.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.logger.info("-" * 50)

        self.copyright_app = CopyrightConfig(self, 400, 30)
        self.copyright_app.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.exp_app = ExperimentalConfig(self, 400, 120)
        self.exp_app.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.machine_app = MachineConfig(self, 400, 120)
        self.machine_app.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.output_app = OutputConfig(self, 400, 80)
        self.output_app.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        self.data_app = DataTable(self, 400, 200)
        self.data_app.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=5, pady=5)

        self.control_app = ButtonPanel(self, 400, 50, self.data_app, self.exp_app, self.machine_app, self.output_app, self.selected_port)
        self.control_app.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        self.logger.info("Everything is initialized. Ready to go!")
        self.logger.info("-" * 50)