from pathlib import Path
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import numpy as np

from readarduino import format_str
from analyze import Plot_Tool


class Manage_data(tk.Frame):
    def __init__(
        self,
        parent,
        display=True,
        data_format="%.3f",
        delimiter="\t",
        *args,
        **kwargs,
    ):
        super().__init__(parent, *args, **kwargs)
        # Utils variables
        self.delimiter = delimiter
        self.format = data_format
        self.path = Path.cwd()
        self.filename = None
        self.parent = parent
        self.display = display
        # Select txt file
        self.file_open_button = tk.Button(
            self, text="Select a File", command=self.select_file
        )

        # Show current path
        self.path_button = tk.Button(
            self, text="Show current path", command=self.show_path
        )

        # Save data in selected file
        self.save_button = tk.Button(
            self,
            text="savedata",
            state="disabled",
            command=self.save,
        )

        # Load and print data in selected file
        self.load_button = tk.Button(
            self,
            text="loaddata",
            state="disabled",
            command=self.load,
        )

        self.data_to_plot = tk.Button(
            self,
            text="Add data to plot tool",
            state="normal",
            command=self.send_data_to_plot_tool,
        )

        self.path_button.grid(
            column=0, row=0, columnspan=2, pady=10, padx=(30, 0)
        )
        self.file_open_button.grid(column=2, row=0, columnspan=2, pady=10)
        self.save_button.grid(column=0, row=1, pady=10, padx=(30, 0))
        self.load_button.grid(column=1, row=1, pady=10)
        self.data_to_plot.grid(column=2, row=1, pady=10)

    def select_file(self):
        filetypes = (("text files", "*.txt"),)
        self.filename = Path(
            tk.filedialog.asksaveasfilename(
                title="File selection",
                defaultextension=".txt",
                initialdir=self.path,
                filetypes=filetypes,
                confirmoverwrite=False,
            )
        )

        if self.filename.name:
            self.path = self.filename.parent.resolve()
            if self.filename.exists():
                self.load_button.configure(state="normal")
            else:
                self.save_button.configure(state="normal")
                self.load_button.configure(state="disabled")
            self.file_open_button.config(text=self.filename.name)
        else:
            self.file_open_button.config(text="Select a File")

    def show_path(self):
        tk.messagebox.showinfo("Current path", self.path.as_posix())

    def save(self):
        try:
            np.savetxt(
                self.filename,
                self.parent.data,
                self.format,
                delimiter=self.delimiter,
                header=self.delimiter.join(self.parent.data.dtype.names or ""),
            )
            print(f"Data saved in {self.filename.as_posix()}")
            self.file_open_button.config(text="Select a File")
            self.save_button.configure(state="disabled")
        except (ValueError, AttributeError):
            print("Nothing to save")

    def load(self):
        with open(self.filename, "r") as file:
            header = next(file)
        if header.startswith("#"):
            params = header[1:].strip().split(self.delimiter)
        else:
            print("No header, using generic names for data")
            params = [
                f"axe{i}"
                for i in range(len(header.strip().split(self.delimiter)))
            ]
        self.parent.data = np.loadtxt(
            self.filename,
            dtype={"names": params, "formats": ["f8"] * len(params)},
            delimiter=self.delimiter,
        )
        if self.display:
            try:
                self.parent.frames["Print_textbox"].text_box.delete("1.0", "end")
            except AttributeError:
                pass
            formatstr = "".join(format_str(params))
            print(formatstr.format(*params).strip())
            for d in self.parent.data:
                print(formatstr.format(*d))
        self.data_to_plot.configure(state="normal")

    def send_data_to_plot_tool(self):
        try:
            data = self.parent.data
        except AttributeError:
            print("No data available")
            pass
        if data.dtype.names is None:
            print("There is no name for data, using generic names")
            data = np.core.records.fromarrays(
                [*np.asarray(data)],
                names=[f"axe{i}" for i in range(len(data[0]))],
            )
        try:
            self.ploting.add_data(data)
        except (AttributeError, AssertionError):
            self.ploting = Plot_Tool(self, data)

    def on_closing(self):
        self.ploting.on_closing()
