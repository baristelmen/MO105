import tkinter as tk
import tkinter.colorchooser
from matplotlib import pylab as plt
from matplotlib import lines, markers
from itertools import cycle
import utils

plt.ion()

lineschoices = {v.split("_")[-1]: k for k, v in lines.lineStyles.items()}
markerschoices = {v: k for k, v in markers.MarkerStyle.markers.items()}


def axe_manage(dic_figure, ylabel):
    if dic_figure["axe"].yaxis.get_label()._text == ylabel:
        return True
    try:
        if dic_figure["axe0"].yaxis.get_label()._text == ylabel:
            dic_figure["axe"], dic_figure["axe0"] = (
                dic_figure["axe0"],
                dic_figure["axe"],
            )
            return True
        else:
            return False
    except KeyError:
        dic_figure["axe0"] = dic_figure["axe"]
        dic_figure["axe"] = dic_figure["axe0"].twinx()
        return True


class Plot_Tool(tk.Toplevel):
    def __init__(self, master, data):
        super().__init__(master=master)
        prop_cycle = plt.rcParams["axes.prop_cycle"]
        self.colorcycle = cycle(prop_cycle.by_key()["color"])
        self.title("Plot data")

        # Data/figures stored
        self.data_dicts = {}
        self.figures = {}

        self.add_data(data)

        # option variables
        self.data_options = tk.StringVar(self)
        self.data_options.set(list(self.data_dicts.keys())[0])
        self.figure_option = tk.StringVar(self)
        self.figure_option.set("New figure")
        axislist = self.data_dicts["Data0"].dtype.names
        dict_choices = utils.list_to_dico(axislist)
        self.x_data_key = tk.StringVar(self, axislist[0])
        self.y_data_key = tk.StringVar(self, axislist[1])
        self.color = tk.StringVar(self)
        self.color.set(next(self.colorcycle))
        self.linestyle_option = tk.StringVar(self)
        self.linestyle_option.set("solid")
        self.marker_option = tk.StringVar(self)
        self.marker_option.set("nothing")

        self.previous_choices = data.dtype.names

        # Data choice
        current_data_label = tk.Label(self, text="Current data")
        self.current_data = utils.CustomOptionMenu(
            self, self.data_options, *self.data_dicts.keys()
        )
        # When option chosen : update axis choice if data available changed
        self.data_options.trace_add(
            "write", lambda traced_var, _, __,: self.reset_axis_choice(traced_var)
        )

        # axis choice
        self.Xaxis = utils.Linked_option_menus(
            self,
            self.x_data_key,
            "X axis",
            (self.y_data_key, dict_choices),
            row=1,
            column=1,
        )
        self.Yaxis = utils.Linked_option_menus(
            self,
            self.y_data_key,
            "Y axis",
            (self.x_data_key, dict_choices),
            row=2,
            column=1,
        )

        # Figure choice
        self.figure_menu = utils.CustomOptionMenu(
            self, self.figure_option, "New figure"
        )
        # When figure chosen, fix xaxis if figure not new figure
        self.figure_option.trace_add(
            "write",
            lambda traced_var, _, __: self.update_figure_options(traced_var),
        )

        self.color_button = tk.Button(
            self, text="Color", bg=self.color.get(), command=self.color_select
        )

        # When color chosen, change button color
        self.color.trace_add(
            "write",
            lambda traced_var, _, __: self.color_button.configure(
                bg=self.getvar(traced_var)
            ),
        )

        # Linestyle choice
        linestyle_label = tk.Label(self, text="Linestyle")
        self.linestyle_menu = tk.OptionMenu(
            self, self.linestyle_option, *lineschoices.keys()
        )

        # Marker choice
        markerstyle_label = tk.Label(self, text="Marker")
        self.markerstyle_menu = tk.OptionMenu(
            self, self.marker_option, *markerschoices.keys()
        )

        # Plot & show
        self.plotbutton = tk.Button(self, text="Plot", command=self.plot)
        self.plotbutton.configure(state="normal")
        self.x_data_key.trace_add(
            "write", lambda a, b, c: self.plot_button_enable()
        )
        self.y_data_key.trace_add(
            "write", lambda a, b, c: self.plot_button_enable()
        )
        self.showbutton = tk.Button(self, text="Show", command=self.show)

        # Place widgets
        current_data_label.grid(column=0, row=0, padx=(10, 0), sticky="w")
        self.current_data.grid(column=1, row=0, sticky="w")
        self.figure_menu.grid(column=0, row=3, padx=(10, 0), columnspan=2)
        self.color_button.grid(column=0, row=4, padx=(10, 0), columnspan=2)
        linestyle_label.grid(column=0, row=5, padx=(10, 0))
        self.linestyle_menu.grid(column=1, row=5, padx=(10, 0))
        markerstyle_label.grid(column=0, row=6, padx=(10, 0))
        self.markerstyle_menu.grid(column=1, row=6, padx=(10, 0))
        self.plotbutton.grid(column=2, row=3, padx=(10, 0), rowspan=2)
        self.showbutton.grid(column=2, row=5, padx=(10, 0), rowspan=2)

        self.geometry("400x300")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def reset_axis_choice(self, traced_var):
        selected = self.getvar(traced_var)
        choices = utils.list_to_dico(self.data_dicts[selected].dtype.names)
        if choices != self.previous_choices:
            self.Xaxis.reset((self.y_data_key, choices))
            self.Yaxis.reset((self.x_data_key, choices))
            self.previous_choices = choices
            if self.figure_option.get() != "New figure":
                self.figure_option.set("New figure")

    def plot_button_enable(self):
        if self.x_data_key.get() == "" or self.y_data_key.get() == "":
            self.plotbutton.configure(state="disabled")
        else:
            self.plotbutton.configure(state="normal")

    def update_figure_options(self, traced_var):
        if self.getvar(traced_var) == "New figure":
            self.Xaxis.configure(state="normal")
            choices = utils.list_to_dico(
                self.data_dicts[self.data_options.get()].dtype.names
            )
            self.Xaxis.reset((self.y_data_key, choices))
        else:
            currentxaxis = (
                self.figures[self.figure_option.get()]["axe"]
                .xaxis.get_label()
                ._text
            )
            self.x_data_key.set(currentxaxis)
            self.Xaxis.configure(state="disabled")

    def plot(self):
        if self.figure_option.get() == "New figure":
            figure_num = len(self.figures.keys())
            key = f"Figure{figure_num}"
            self.figures[key] = {}
            self.figures[key].update(zip(["figure", "axe"], plt.subplots()))
            self.figure_menu.reset_menu(
                ["New figure"] + list(self.figures.keys())
            )
        else:
            key = self.figure_option.get()
            if not axe_manage(self.figures[key], self.y_data_key.get()):
                print("There can't be more than two differents y axis on figure")
                return
        itemplotted = [self.x_data_key.get(), self.y_data_key.get()]
        curent_data = self.data_options.get()
        self.figures[key]["axe"].plot(
            *[self.data_dicts[curent_data][k] for k in itemplotted],
            linestyle=lineschoices[self.linestyle_option.get()],
            marker=markerschoices[self.marker_option.get()],
            color=self.color.get(),
            label=curent_data + " " + itemplotted[1].split()[0],
        )
        self.figures[key]["axe"].set_xlabel(itemplotted[0])
        self.figures[key]["axe"].set_ylabel(itemplotted[1])
        self.figures[key]["figure"].legend()
        self.figures[key]["figure"].canvas.draw()
        self.figures[key]["figure"].tight_layout()
        self.color.set(next(self.colorcycle))

    def color_select(self):
        _, color = tk.colorchooser.askcolor(title="Color Chooser")
        if color:
            self.color.set(color)

    def show(self):
        if self.figure_option.get() != "New figure":
            self.figures[self.figure_option.get()]["figure"].show()

    def add_data(self, data):
        assert self.winfo_exists()
        data_number = len(self.data_dicts)
        self.data_dicts[f"Data{data_number}"] = data
        try:
            self.current_data.reset_menu(self.data_dicts.keys())
        except AttributeError:
            pass

    def on_closing(self):
        plt.close("all")
        self.destroy()
