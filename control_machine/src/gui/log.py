import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import logging

# Utility function
def disable_frame(frame: tk.Frame):
    for child in frame.winfo_children():
        try:
            child.configure(state="disabled")
        except tk.TclError:
            pass  # Not all widgets support the 'state' option

class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.after(0, self.text_widget.insert, tk.END, msg + '\n')
        self.text_widget.after(0, self.text_widget.see, tk.END)


## Logs should be readoly. The user still can modify the text
## but it will not be saved
## TODO: readonly logs
class LogFrame(tk.Frame):
    def __init__(self, parent, width: int, height: int):
        super().__init__(parent, width=width, height=height, bg="white")
        self.log_widget = ScrolledText(self, height=10, state='normal')
        self.log_widget.pack(fill=tk.BOTH, expand=True)

        # Set up the logger to use this text area
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.DEBUG)

        handler = TextHandler(self.log_widget)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)