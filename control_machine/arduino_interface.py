import tkinter as tk
import tkinter.messagebox
import utils
import traceback
from copy import deepcopy

from readarduino import (
    Arduino as Ar,
    arduino_custom_params,
    arduino_move_limits,
    delay_key,
    get_ports,
)

show_baud = False

row = 1

interface_arduino_move_limits = deepcopy(arduino_move_limits)
interface_arduino_custom_params = deepcopy(arduino_custom_params)

for name in interface_arduino_move_limits.keys():
    interface_arduino_move_limits[name]["row"] = row
    interface_arduino_move_limits[name]["pady"] = (0, 0)
    row = row + 1

default_baudrate = 9600
default_timeout = 1.0
baudrate_row = row
row = row + 2

for name in interface_arduino_custom_params.keys():
    interface_arduino_custom_params[name]["row"] = row
    interface_arduino_custom_params[name]["pady"] = (0, 10)
    row = row + 1

interface_arduino_custom_params["timeout"] = {
    "vtype": float,
    "unit": "s",
    "default_value": default_timeout,
    "help_text": "Waiting time when reading data",
    "row": baudrate_row + 1,
    "pady": (0, 10),
}


class Arduino_interface(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        # Utils variables
        self.timeout = default_timeout
        self.arduino = None
        self.upstatut, self.downstatut = False, False
        self.parent.data = None

        # Menu bar
        self.__create_menu_bar()
        self.searchcard = tk.Button(
            self, text="Allow reloading cards", command=self.allow_reload
        )
        # Selection (timing or distance)
        self.selection = interface_arduino_move_limits
        # Variables entries
        self.select_limit = tk.StringVar(self)
        self.select_limit.set(next(iter(self.selection.keys())))

        for name, features in self.selection.items():
            features.update(
                zip(
                    [l for l in ["w_label", "w_entry", "w_unit"]],
                    utils.create_selection(
                        self,
                        self.__select,
                        self.select_limit,
                        name,
                        **features,
                    ),
                )
            )
            self.selection[name]["w_entry"].configure(state="disabled")
            self.selection[name]["w_label"].configure(state="disabled")

        # parameters entries
        L_Baud, self.entry_baudrate, _ = utils.create_entry(
            self,
            "Baudrate",
            int,
            default_baudrate,
            "",
            lambda *args, **kwargs: None,
            baudrate_row,
            (10, 0),
            "Communication speed with arduino\nValue is set in arduino program",
        )

        self.entry_baudrate.configure(state="disabled")

        if not show_baud:
            L_Baud.grid_forget()
            self.entry_baudrate.grid_forget()

        self.entry_dico = interface_arduino_custom_params

        for name, features in self.entry_dico.items():
            features["command"] = lambda inp, key=name: self.__action(inp, key)
            self.entry_dico[name].update(
                zip(
                    [l for l in ["w_label", "w_entry", "w_unit"]],
                    utils.create_entry(self, name, **features),
                )
            )
            if name != "timeout":
                self.entry_dico[name]["w_entry"].configure(state="disabled")

        # Button show current voltage
        self.get_volt_button = tk.Button(
            self,
            text="Get current Voltage",
            command=self.get_volt,
        )

        # Buttons Up and Down
        self.up_button = self.__button_set(self.up, self.stop, "\u1431", "Up")

        self.down_button = self.__button_set(
            self.down, self.stop, "\u142f", "Down"
        )

        # Button set position to zero
        if "Radius" in self.entry_dico.keys():
            self.zero_button = tk.Button(
                self,
                text="Set position to zero",
                state="disabled",
                command=self.setzero,
            )

        # Button to start experiment
        self.start_experiment = self.__button_set(
            None, self.start, "START", "Return"
        )

        # Stop button
        self.stop_button = self.__button_set(None, self.stop, "STOP", "Escape")

        # Widget positionement
        self.searchcard.grid(row=0)
        self.get_volt_button.grid(row=row)
        self.up_button.grid(column=3, row=row + 1, pady=(10, 0))
        self.down_button.grid(column=3, row=row + 2, pady=(0, 10))

        try:
            self.zero_button.grid(column=0, row=row + 1, rowspan=2, padx=(30, 0))
        except AttributeError:
            pass

        self.start_experiment.grid(column=1, row=row + 1, rowspan=2, padx=10)

        self.stop_button.grid(column=2, row=row + 1, rowspan=2, padx=10)

    # Menu bar for port selection
    def __create_menu_bar(self):
        self.menu_bar = tk.Menu(self.parent, tearoff=0)
        self.menu_ports = utils.reloadable_menu(
            self.menu_bar,
            {
                "Available ports": {
                    "labelsgetter": get_ports,
                    "callback": [
                        ("Select", self.begin_com),
                        ("Show info", self.__showinfo),
                    ],
                }
            },
        )
        self.menu_ports.block_reloading()
        self.parent.config(menu=self.menu_bar)

    def block_reload(self):
        self.menu_ports.block_reloading()
        self.searchcard.configure(
            text="Allow reloading cards", command=self.allow_reload
        )

    def allow_reload(self):
        self.menu_ports.allow_reloading()
        self.searchcard.configure(
            text="Block reloading cards", command=self.block_reload
        )

    def __showinfo(self, port):
        tk.messagebox.showinfo(
            port.device,
            "\n".join(
                [":".join(map(str, item)) for item in port.__dict__.items()]
            ),
        )

    # Configure arduino com
    def begin_com(self, port):
        """
        Start communication with arduino
        """
        portname = port.device
        if self.arduino is not None:
            self.arduino.close()
        try:
            self.arduino = Ar(
                portname,
                self.entry_baudrate.get(),
                timeout=self.entry_dico["timeout"]["w_entry"].get(),
            )
            print("Conected to arduino")
        except Exception as e:
            print(f"Failed to open port {portname} because of {e}")
            traceback.print_exception(type(e), e, e.__traceback__)
            if self.arduino is not None:
                self.arduino_closed()
            return
        self.arduino_opened()

    def arduino_opened(self):
        listwid = self.winfo_children()
        utils.enable(listwid)
        self.entry_baudrate.setValue(self.arduino.baudrate)

        self.entry_baudrate.configure(state="disabled")
        # Update timeout (if not compatible with delay)
        self.arduino.timeout = self.entry_dico["timeout"]["w_entry"].get()
        # Update displayed timeout (if it has changed)
        self.__retrieve_value(None, "timeout")
        for name in self.entry_dico.keys():
            default = getattr(self.arduino, name)
            self.entry_dico[name]["w_entry"].setValue(default)
            self.entry_dico[name]["default_value"] = default
            self.entry_dico[name]["w_entry"].bind(
                "<FocusOut>",
                lambda event, k=name: self.__retrieve_value(event, k),
            )
        self.entry_dico[delay_key]["w_entry"].bind(
            "<FocusOut>",
            lambda event, k="timeout": self.__retrieve_value(event, k),
            add="+",
        )
        for name in self.selection.keys():
            default = self.arduino.arduino_move_limits[name]["default_value"]
            self.selection[name]["w_entry"].setValue(default)
            self.selection[name]["default_value"] = default
        self.__select()

    def arduino_closed(self):
        self.arduino = None
        for name in self.entry_dico.keys():
            if name != "timeout":
                self.entry_dico[name]["w_entry"].setValue(0)
        for feature in self.selection.values():
            feature["w_entry"].setValue(0)

        listwid = self.winfo_children()
        listwid = [
            l for l in listwid if l != self.entry_dico["timeout"]["w_entry"]
        ]
        _ = utils.disable(listwid)

        self.entry_baudrate.configure(state="normal")
        self.entry_baudrate.setValue(default_baudrate)
        _ = [
            features["w_entry"].unbind("<FocusOut>")
            for features in self.entry_dico.values()
        ]

    # Tkinter function (validation and widget feature)
    def __select(self):
        """
        Enable/disable entries depending on radiobutton selected
        """
        for name, features in self.selection.items():
            if self.select_limit.get() == name:
                features["w_entry"].configure(state="normal")
            else:
                features["w_entry"].setValue(features["default_value"])
                features["w_entry"].configure(state="disabled")

    def __retrieve_value(self, event, key):
        value = getattr(self.arduino, key)
        entry = self.entry_dico[key]["w_entry"]
        if entry.get() != value:
            entry.setValue(value)

    def __action(self, inp, key):
        if self.arduino is not None:
            setattr(self.arduino, key, inp)
        else:
            print(f"Setting {key} to {inp} {self.entry_dico[key]['unit']}")

    def __button_set(
        self,
        action_press,
        action_release,
        buttontext,
        keyb,
        default_state="disabled",
    ):
        """
        Setting button with different action on press and on release with shortcut on keyboard, that can be disabled

        Parameters
        ----------
        action_press : function
            Action when pressing button.
        action_release : function
            Action when release button.
        buttontext : str
            Text display on button.
        keyb : str
            Keyboard shortcut.

        Returns
        -------
        button : tk button
            Button object.

        """
        button = tk.Button(self, text=buttontext, state=default_state)
        if action_press is not None:
            commandpress = lambda event, widget=button, comand=action_press: self.__is_disabled(
                event, widget, comand
            )
            self.parent.bind(f"<KeyPress-{keyb}>", commandpress)
            button.bind("<ButtonPress>", commandpress)
        if action_release is not None:
            commandrelease = lambda event, widget=button, comand=action_release: self.__is_disabled(
                event, widget, comand
            )
            self.parent.bind(f"<KeyRelease-{keyb}>", commandrelease)
            button.bind("<ButtonRelease>", commandrelease)
        return button

    def __is_disabled(self, event, widget, command):
        """
        Do action only if button is not disabled

        Parameters
        ----------
        event : tk event
            Event defined in tk.bind.
        widget : tk widget
            Widget to check stae.
        command : function
            Action to do when event if widget not disabled.

        Returns
        -------
        None.

        """
        if "disabled" in widget.config("state"):
            return
        else:
            command(event)

    # Commands send to arduino
    def up(self, event):
        if not self.upstatut:
            self.upstatut = True
            self.arduino.send_instruction("up")

    def down(self, event):
        if not self.downstatut:
            self.downstatut = True
            self.arduino.send_instruction("down")

    def stop(self, event):
        if self.upstatut or self.downstatut:
            self.upstatut = False
            self.downstatut = False
            self.arduino.STOP()

    def setzero(self):
        self.arduino.SETZERO()

    def get_volt(self):
        self.arduino.get_current_volt()

    def start(self, event):
        # Disables entries and button except stop
        self.downstatut = True
        widgets = []
        for value in self.parent.frames.values():
            listwid = value.winfo_children()
            try:
                listwid.remove(self.stop_button)
            except:
                pass
            widgets = widgets + utils.disable(listwid)
        # Empty text and print arduino output datanames
        try:
            self.parent.frames["Print_textbox"].text_box.delete("1.0", "end")
        except KeyError:
            pass
        # Run arduino.experiment with current parameters
        argname = self.select_limit.get()
        value = self.selection[argname]["w_entry"].get()
        self.parent.data = self.arduino.experiment(**{argname: value})
        self.downstatut = False
        # Reenable widget disabled during experiment
        utils.enable(widgets)

    def on_closing(self):
        if self.arduino is not None:
            self.arduino.close()
