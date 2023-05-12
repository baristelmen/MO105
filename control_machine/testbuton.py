import tkinter as tk
import time
from threading import Timer


class KeyTracker:
    def __init__(self, key, on_key_press, on_key_release):
        self.key = key
        self.last_press_time = 0
        self.last_release_time = 0
        self.on_key_press = on_key_press
        self.on_key_release = on_key_release

    def is_pressed(self):
        return time.time() - self.last_press_time < 0.1

    def report_key_press(self, event):
        if event.keysym == self.key:
            if not self.is_pressed():
                self.on_key_press(event)
            self.last_press_time = time.time()

    def report_key_release(self, event):
        if event.keysym == self.key:
            timer = Timer(0.1, self.report_key_release_callback, args=[event])
            timer.start()

    def report_key_release_callback(self, event):
        if not self.is_pressed():
            self.on_key_release(event)
        self.last_release_time = time.time()


class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.parent = master
        self.pack()
        self.up_button = self.__button_set(
            self.up, self.stop, "\u1431", "Up", "normal"
        )
        self.down_button = self.__button_set(
            self.down, self.stop, "\u142f", "Down", "normal"
        )
        self.up_button.pack()
        self.down_button.pack()
        self.upstatut, self.downstatut = False, False

    def up(self, event):
        if not self.upstatut:
            self.upstatut = True
            print("up")

    def down(self, event):
        if not self.downstatut:
            self.downstatut = True
            print("down")

    def stop(self, event):
        if self.upstatut or self.downstatut:
            self.upstatut = False
            self.downstatut = False
            print("Stop")

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
            # self.parent.bind(f"<KeyPress-{keyb}>", commandpress)
            button.bind("<ButtonPress>", commandpress)
        else:
            commandpress = lambda *args: None
        if action_release is not None:
            commandrelease = lambda event, widget=button, comand=action_release: self.__is_disabled(
                event, widget, comand
            )
            # self.parent.bind(f"<KeyRelease-{keyb}>", commandrelease)
            button.bind("<ButtonRelease>", commandrelease)
        else:
            commandrelease = lambda *args: None
        key_tracker = KeyTracker(keyb, commandpress, commandrelease)
        self.parent.bind(f"<KeyPress-{keyb}>", key_tracker.report_key_press)
        self.parent.bind(f"<KeyRelease-{keyb}>", key_tracker.report_key_release)
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


root = tk.Tk()
root.title("Viewer")
root.geometry("100x60")
app = MainWindow(root)
root.mainloop()
