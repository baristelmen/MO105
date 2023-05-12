import tkinter as tk

## classes derived from tkinter classes


class dFrame(tk.Frame):
    def enable(self, state="normal"):
        def cstate(widget):
            # Is this widget a container?
            if widget.winfo_children:
                # It's a container, so iterate through its children
                for w in widget.winfo_children():
                    # change its state
                    try:
                        w.configure(state=state)
                    except tk.TclError:
                        pass
                    # and then recurse to process ITS children
                    cstate(w)

        cstate(self)

    def disable(self):
        self.enable("disabled")


class CustomOptionMenu(tk.OptionMenu):
    """
    OptionMenu with label, anda method to reset the choices
    search_option = true add an entry used to search a value in choices
    """

    def __init__(
        self, master, variable, *values, label="", search_option=False, **kwargs
    ):
        self.callback = kwargs.get("command")
        self.master = master
        self.variable = variable
        self.values = list(values)
        current_column, current_row = self.master.grid_size()
        if "row" in kwargs:
            row = kwargs.get("row")
            del kwargs["row"]
        else:
            row = current_row
        if "column" in kwargs:
            column = kwargs.get("column")
            del kwargs["column"]
        else:
            column = current_column
        super().__init__(master, variable, *values, **kwargs)
        if label:
            self.label = tk.Label(self.master, text=label)

        if search_option:
            self.entry = CustomEntry(self.master, None, None)
            self.entry.bind("<KeyRelease>", self._check_input)
            try:
                self.label.grid(
                    column=column, row=row, rowspan=2, padx=(10, 0), sticky="w"
                )
            except AttributeError:
                column = column - 1
            self.entry.grid(column=column + 1, row=row, sticky="nw")
            self.grid(column=column + 1, row=row + 1, sticky="sw")

        else:
            try:
                self.label.grid(column=column, row=row, padx=(10, 0), sticky="w")
            except AttributeError:
                column = column - 1
            self.grid(column=column + 1, row=row, sticky="w")

    def reset_menu(self, choices=None):
        if choices is None:
            choices = self.values
        variable_value = self.variable.get()
        if variable_value and variable_value not in choices:
            self.variable.set("")
        menu = self["menu"]
        menu.delete(0, "end")
        for choice in choices:
            menu.add_command(
                label=choice,
                command=tk._setit(self.variable, choice, callback=self.callback),
            )

    def _check_input(self, event):
        value = self.entry.get()
        if value:
            data = []
            for item in self.values:
                if value.lower() in item.lower():
                    data.append(item)
            self.reset_menu(data)
        else:
            self.reset_menu(self.values)

    def get(self):
        return self.variable.get()


class Linked_option_menus(CustomOptionMenu):
    """
    OptionMenu updated when a tk variable is changed according to linkinfo = (tk.variable,Optionchoices)
    or linkinfo = [(tk.variableA,OptionchoicesA),(tk.variableB,OptionchoicesB),...]
    Optionchoices are dictionarry {tkvariable value:list of choice}
    """

    def __init__(
        self, master, variable, label, linkinfo, reciprocal=False, **kwargs
    ):
        self.master = master
        self.label = label
        if reciprocal:
            self.command = self.set_variable
        else:
            self.command = None

        if isinstance(linkinfo, tuple):
            linkinfo = [linkinfo]
        self.traced_variables, self.dicts_choices = map(list, zip(*linkinfo))
        assert len(self.traced_variables) == len(
            self.dicts_choices
        ), "Error in linkinfo argument, should be in form (tk.variable,Optionchoices)"
        " or [(tk.variableA,OptionchoicesA),(tk.variableB,OptionchoicesB),...]"
        for dict_choices in self.dicts_choices:
            dict_choices = add_allvalue_item_to_dict(dict_choices)
        values = self.dicts_choices[0][""]
        super().__init__(
            self.master,
            variable,
            *values,
            label=label,
            command=self.command,
            **kwargs,
        )
        for i, traced in enumerate(self.traced_variables):
            if traced is not None:
                traced.trace_add(
                    "write",
                    self.update_menu_choice,
                )

    def set_variable(self, value):
        if value:
            for dico, targetvar in zip(self.dicts_choices, self.traced_variables):
                if targetvar is not None:
                    key = set(get_all_key(value, dico)) - {""}
                    if len(key) == 1:
                        key = [e for e in key][0]
                        if targetvar.get() != key:
                            targetvar.set(key)
                    else:
                        targetvar.set("")

    def update_menu_choice(self, *args):
        choices = list(
            set.intersection(
                *[
                    set(x)
                    for x in [
                        dico[traced_var.get()]
                        for dico, traced_var in zip(
                            self.dicts_choices, self.traced_variables
                        )
                    ]
                ]
            )
        )
        if choices != self.values:
            self.reset_menu(choices)
            self.values = choices

    def reset(self, linkinfo):
        if isinstance(linkinfo, tuple):
            linkinfo = [linkinfo]
        traced_variables, dicts_choices = map(list, zip(*linkinfo))
        for dict_choices in dicts_choices:
            dict_choices = add_allvalue_item_to_dict(dict_choices)
        for traced_variable, dict_choices in zip(traced_variables, dicts_choices):
            self.dicts_choices[
                self.traced_variables.index(traced_variable)
            ] = dict_choices
        self.reload_menu()

    def reload_menu(self):
        choices = []
        for i, dict_choices in enumerate(self.dicts_choices):
            choices.append(self.dicts_choices[i][""])
        choices = set(sum(choices, []))
        self.variable.set("")
        self.reset_menu(choices)
        self.values = list(choices)


class CustomEntry(tk.Entry):
    """
    Tk entry with validation method for Type (None,float or int) a callback when focus out
    and methods to set value (even if disabled) and get value using Type
    """

    def __init__(self, root, Type=None, command=None, *args, **kwargs):
        # if Type not in [None, float, int, str]:
        #     print(
        #         f"Warning : validation may not work properly for {Type.__name__}"
        #     )
        self.Type = Type
        self.command = command
        if "validatecommand" in kwargs:
            validatecommand = kwargs.get("validatecommand")
        elif Type not in (None, str) or self.command is not None:
            validatecommand = (
                root.register(
                    lambda inp, event_type: self._Validation(
                        inp,
                        event_type,
                    )
                ),
                "%P",
                "%V",
            )
            if "validate" not in kwargs:
                kwargs["validate"] = "all"
        else:
            validatecommand = None
        super().__init__(root, validatecommand=validatecommand, *args, **kwargs)

    def setValue(self, value, command=True):
        if "disabled" in self.config("state"):
            self.configure(state="normal")
            disabled = True
        else:
            disabled = False
        self.clear()
        if value is not None:
            val = str(value)
            if self._validentry(val):
                self.insert(0, val)
                if command and self.command is not None:
                    self.command(value)
            else:
                print(f"Invalid entry in setValue = {value}")
        if disabled:
            self.configure(state="disabled")

    def clear(self):
        self.delete(0, tk.END)

    def get(self):
        try:
            return self.Type(super().get())
        except (TypeError, ValueError):
            return super().get()

    def _validentry(self, inp):
        if self.Type is None:
            return True
        if istype(inp, self.Type) or inp == "":
            return True
        else:
            self.bell()
            return False

    def _Validation(self, inp, event_type):
        """

        Parameters
        ----------
        inp : Value
            Value in Entry %P in validatecommand
        event_type : str
            Reason for the call :%V in validatecommand.

        Returns
        -------
        TYPE Bool
            Bool needed for validation

        """
        if event_type == "focusout":
            if inp == "":
                self.bell()
                return True
            else:
                if self.command is not None:
                    try:
                        self.command(self.Type(inp))
                    except TypeError:
                        self.command(inp)
                return True
        else:
            return self._validentry(inp)


class ToolTip(object):
    """
    Add toolTip help message on a widget.
    """

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.showtip)
        self.widget.bind("<Leave>", self.hidetip)

    def showtip(self, event):
        "Display text in tooltip window"
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(1)
        self.tipwindow.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tipwindow,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
        )
        label.pack(ipadx=1)

    def hidetip(self, event):
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None


class _reloadable_menu(tk.Menu):
    def __init__(
        self, parent, labelsgetter, callback, tearoff=0, *args, **kwargs
    ):
        super().__init__(parent, tearoff=tearoff, *args, **kwargs)
        # self.open = False
        self.callback = callback
        self.labelsgetter = labelsgetter
        self.parent = parent
        self.repopulate()

    def repopulate(self):

        # Clear all current population
        self.delete(0, "end")
        values = self.labelsgetter()
        if values is not None:
            # Add the new menu items
            for value in values:
                if callable(self.callback):
                    try:
                        Font = value.Font
                        self.add_command(
                            label=str(value),
                            command=lambda val=value: self.callback(val),
                            font=Font,
                        )
                    except AttributeError:
                        self.add_command(
                            label=str(value),
                            command=lambda val=value: self.callback(val),
                        )
                elif isinstance(self.callback, list):
                    menu_p = tk.Menu(self.parent, tearoff=0)
                    for (lab, call) in self.callback:
                        menu_p.add_command(
                            label=lab,
                            command=lambda val=value, callback=call: callback(
                                val
                            ),
                        )
                    try:
                        Font = value.Font
                        self.add_cascade(
                            label=str(value), underline=0, menu=menu_p, font=Font
                        )
                    except AttributeError:
                        self.add_cascade(
                            label=str(value), underline=0, menu=menu_p
                        )


class reloadable_menu(object):
    """
    A Menu with labels updated at opening, params is a dictionary{label:param} ,
    where param is the parameters as dictionary : 'labelsgetter' is a method to get labels of the menu
    and 'callback', callback(label) is called on selection
    """

    def __init__(self, parent, params, tearoff=0, *args, **kwargs):
        self.parent = parent
        self.menu = []
        for label, param in params.items():
            menu = _reloadable_menu(
                self.parent, tearoff=tearoff, *args, **{**param, **kwargs}
            )
            self.parent.add_cascade(label=label, menu=menu)
            self.menu.append(menu)
        self.parent.bind("<<MenuSelect>>", self.updateMainMenuOptions)
        self.activeMenu = None

    def updateMainMenuOptions(self, event):
        try:
            activeMenuIndex = self.parent.nametowidget(".").call(
                event.widget, "index", "active"
            )
            newMenu = self.parent.winfo_children()[activeMenuIndex]
            if newMenu != self.activeMenu:
                if isinstance(newMenu, _reloadable_menu):
                    newMenu.repopulate()
                    self.activeMenu = newMenu
        except TypeError:  # The active menu index is 'none'; all menus are closed
            self.activeMenu = None
        #         activeMenu.open = True
        # except TypeError:  # The active menu index is 'none'; all menus are closed
        #     for menuWidget in self.parent.winfo_children():
        #         menuWidget.open = False

    def block_reloading(self):
        self.parent.unbind("<<MenuSelect>>")

    def allow_reloading(self):
        self.parent.bind("<<MenuSelect>>", self.updateMainMenuOptions)
        for m in self.menu:
            m.repopulate()


## dictionary manipulation
def get_key(val, dico):
    for key, value in dico.items():
        try:
            if val in value.keys():
                return key
        except AttributeError:
            try:
                if val in value:
                    return key
            except TypeError:
                if val == value:
                    return key


def get_all_key(val, dico):
    for key, value in dico.items():
        try:
            if val in value.keys():
                yield key
        except AttributeError:
            try:
                if val in value:
                    yield key
            except TypeError:
                if val == value:
                    yield key


def add_allvalue_item_to_dict(dico, key=""):
    allvalues = set([item for sublist in dico.values() for item in sublist])
    try:
        if set(dico[key]) != allvalues:
            raise ValueError(
                f"key '{key}' already used and not contain all values"
            )
    except KeyError:
        dico.update({key: list(allvalues)})
    return dico


def list_to_dico(choices):
    return dict(
        {"": list(choices)},
        **{c: [i for i in choices if i != c] for c in choices},
    )


##Helpers functions


def istype(num, Type):
    # Type int or float
    try:
        _ = Type(num)
        return True
    except ValueError:
        return False


def disable(widgets):
    """
    Select widget type Entry, Button or Radiobutton and disable them.

    Parameters
    ----------
    widgets : list
        list of tk widgets

    Returns
    -------
    res : list
        list of widget disabled.

    """
    res = []
    for widget in widgets:
        if (
            widget.winfo_class() in ["Entry", "Button", "Radiobutton"]
            and widget.cget("state") == "normal"
        ):
            widget.configure(state="disabled")
            res.append(widget)
    return res


def enable(widgets):
    """
    Enable widgets

    Parameters
    ----------
    widgets : list
        list of tk widgets

    Returns
    -------
    None.

    """
    for widget in widgets:
        widget.configure(state="normal")


def create_selection(
    root,
    command,
    variable,
    name,
    unit,
    vtype,
    default_value,
    help_text,
    row,
    pady,
    **kwargs,
):
    """
    Create radiobutton linked with a command, an entry with validation method and a label (unit of entry)
    Parameters
    ----------
    root : widget
        Tk widget.
    command : Method
        Method to call when radiobuton is selected.
    variable : tk Stringvar
        Variable linked with radiobutton.
    name : str
        text and value of radiobutton.
    unit : str
        Unit of the entry (text after entry).
    vtype : method
        type of expected entry (float,int).
    default_value : number
        Default value for entry.
    help_text : str
        Help tooltip
    row : int
        row where widget are placed
    pady : tuple of int
        Empty vertical space between widgets
    **kwargs : various parameters
        Unused.

    Returns
    -------
    w_label : Radiobutton widget
        Radiobutton before entry.
    w_entry : Entry widget
        Entry.
    w_unit : widget
        Label afetr entry.

    """
    w_label = tk.Radiobutton(
        root,
        text=name.replace("_", " "),
        variable=variable,
        value=name,
        command=command,
    )
    if help_text:
        _ = ToolTip(w_label, help_text)
    w_entry = CustomEntry(
        root,
        Type=vtype,
        validate="all",
        command=lambda *args, **kwargs: None,
        width=10,
    )
    w_entry.setValue(default_value, False)
    w_unit = tk.Label(root, text=unit)
    place_entry(row, pady, w_label, w_entry, w_unit)
    return w_label, w_entry, w_unit


def create_entry(
    root,
    name,
    vtype,
    default_value,
    unit,
    command,
    row,
    pady,
    help_text=None,
    **kwargs,
):
    """
    Create an entry with label, unit and validation method
    Parameters
    ----------
    root : widget
        Tk widget.
    name : str
        Name of the entry (text before entry).
    vtype : method
        type of expected entry (float,int).
    default_value : number
        Entry value when created.
    unit : str
        Unit of the entry (text after entry).
    command : lambda function
        Command when entry is validated (focusout)
    help_text : str
        Text displayed when hovering over label
    row : int
        row where widget are placed
    pady : tuple of int
        Empty vertical space between widgets
    **kwargs : various parameters
        Unused.

    Returns
    -------
    w_label : widget
        Label before entry.
    w_entry : Entry widget
        Entry.
    w_unit : widget
        Label afetr entry.

    """
    w_label = tk.Label(root, text=name.replace("_", " "))
    if help_text:
        _ = ToolTip(w_label, help_text)
    w_entry = CustomEntry(
        root,
        Type=vtype,
        validate="all",
        command=command,
        width=10,
    )
    w_entry.setValue(default_value, False)
    w_unit = tk.Label(root, text=unit)
    place_entry(row, pady, w_label, w_entry, w_unit)
    return w_label, w_entry, w_unit


def place_entry(row, pady, w_label, w_entry, w_unit):
    w_label.grid(
        column=0, row=row, pady=pady, padx=(30, 0), sticky="w", columnspan=2
    )
    w_entry.grid(column=2, row=row, pady=pady)
    w_unit.grid(column=3, row=row, pady=pady)
