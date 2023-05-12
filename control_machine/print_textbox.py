import tkinter as tk
import sys


class StdoutRedirector:
    """
    Class that redefine stdout to diplay print in widget
    """

    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert("end", string)
        self.text_space.see("end")
        self.text_space.update()

    def flush(self):
        pass


class Print_textbox(tk.Frame):
    def __init__(self, parent, line_character, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.text_box = tk.Text(self, width=line_character, wrap=tk.WORD)
        self.text_box.grid(column=0, row=0)
        self.orig_stdout = sys.stdout  # Save stdout to reconfigure it on closing
        sys.stdout = StdoutRedirector(
            self.text_box
        )  # All print output send in text_box

    def on_closing(self):
        sys.stdout = self.orig_stdout
