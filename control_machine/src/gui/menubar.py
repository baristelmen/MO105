import tkinter as tk
from tkinter import messagebox
import serial.tools.list_ports
import logging
import time

class MenuBar(tk.Menu):
    def __init__(self, root, on_port_selected=None):
        super().__init__(root)
        self.root = root

        self.on_port_selected = on_port_selected
        self.selected_port = None

        # File menu
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        self.add_cascade(label="File", menu=file_menu)

        # Connect menu
        self.connect_menu = tk.Menu(self, tearoff=0)
        self.connect_menu.add_command(label="Refresh", command=self.refresh_ports)

        # Ports submenu (initial state)
        self.ports_menu = tk.Menu(self.connect_menu, tearoff=0)
        self.ports_menu.add_command(label="None", state="disabled")
        self.connect_menu.add_cascade(label="Ports", menu=self.ports_menu)

        self.add_cascade(label="Connect", menu=self.connect_menu)

        # Help menu
        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.add_cascade(label="Help", menu=help_menu)

        self.arduino = None

        ## Check if the ports are alrady available
        self.refresh_ports()

        self.logger = logging.getLogger("AppLogger")

    # Placeholder methods
    def new_file(self):
        print("New file")

    def open_file(self):
        print("Open file")

    def show_about(self):
        messagebox.showinfo("About", "Your Application v1.0")

    def refresh_ports(self):
        # Clear current ports menu
        self.ports_menu.delete(0, tk.END)

        # Get available serial ports
        ports = list(serial.tools.list_ports.comports())
        if ports:
            for port in ports:
                self.ports_menu.add_command(
                    label=port.device,
                    command=lambda p=port.device: self.select_port(p)
                )
        else:
            self.ports_menu.add_command(label="None", state="disabled")

    def select_port(self, port_name):
        self.selected_port = port_name
        print(f"Selected port: {port_name}")
        if self.on_port_selected:
            self.on_port_selected(port_name)

    def get_selected_port(self):
        return self.selected_port
