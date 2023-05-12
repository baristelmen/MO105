import tkinter as tk
import tkinter.font

from arduino_interface import Arduino_interface
from manage_data import Manage_data
from print_textbox import Print_textbox


def get_screen__and_font_size():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    font = tk.font.Font().measure("0")
    root.destroy()
    return width, height, font


class Interface(tk.Tk):
    def __init__(self, frames_dict, windows_width, windows_height, title):
        super().__init__()
        self.frames_dict = frames_dict
        self.frames = {}
        for frame, param in self.frames_dict.items():
            args_place = {d: param.pop(d) for d in ["x", "y"]}
            container = frame(
                self,
                bd=10,
                highlightbackground="black",
                highlightthickness=1,
                **param,
            )
            container.place(**args_place)
            container.grid_propagate(0)
            self.frames[frame.__name__] = container
        self.geometry(f"{windows_width}x{windows_height}")
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        for key in self.frames_dict.keys():
            try:
                self.frames[key.__name__].on_closing()
            except AttributeError:
                pass
        self.destroy()


#%%
if __name__ == "__main__":
    character_number_rightframe = 60
    screenwidth, screenheight, font = get_screen__and_font_size()
    min_size_leftframe = 32 * font + 50
    min_size_rightframe = 60 * font
    frameratio = 0.62
    textminsize = max(
        min_size_leftframe * frameratio / (1 - frameratio), min_size_rightframe
    )
    windows_width = min(int(textminsize / frameratio), screenwidth - 20)
    windows_height = min(int(windows_width * frameratio), screenheight - 70)
    title = "Traction command and data read"
    frames_dict = {
        Arduino_interface: {
            "width": (1 - frameratio) * windows_width,
            "height": 2 * windows_height / 3,
            "x": 0,
            "y": 0,
        },
        Manage_data: {
            "width": (1 - frameratio) * windows_width,
            "height": windows_height / 3,
            "x": 0,
            "y": 2 * windows_height / 3,
            "display": True,
            "data_format": "%.3f",
            "delimiter": "\t",
        },
        Print_textbox: {
            "width": frameratio * windows_width,
            "height": windows_height,
            "line_character": character_number_rightframe,
            "x": (1 - frameratio) * windows_width,
            "y": 0,
        },
    }
    app = Interface(frames_dict, windows_width, windows_height, title)
    app.mainloop()
    if hasattr(app.frames["Manage_data"], "ploting"):
        datas = app.frames["Manage_data"].ploting.data_dicts
        figures = app.frames["Manage_data"].ploting.figures
    if hasattr(app, "data"):
        data = app.data
