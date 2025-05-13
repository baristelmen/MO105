import tkinter as tk
from src.logic.arduino import Arduino as arduino
from src.gui.data import DataTable
from threading import Thread
import time
import pandas as pd
import logging
from tkinter import messagebox

class ButtonPanel(tk.Frame):
    def __init__(self, parent, width: int, height: int, shared_application, 
                 shared_config = None, 
                 machine_app = None, 
                 output_app = None,
                 port = None):
        super().__init__(parent, width=width, height=height, bg="white", takefocus=True)

        self.shared_application = shared_application  # Save reference to DataTable
        self.shared_config = shared_config
        self.machine_app = machine_app
        self.output_app = output_app

        self.ar = arduino(port = port, baudrate=9600, timeout=1)

        self.grid_propagate(False)

        # Highlight border to visualize frame bounds
        self.config(highlightbackground="blue", highlightthickness=2)
        
        # Place the frame on the parent
        self.grid(row=0, column=0, sticky="ew", padx=0, pady=(5, 5))

        large_font = ("Helvetica", 12, "bold")  # You can adjust the size

        # First child frame (Start, Stop)
        control_frame = tk.Frame(self,  bg="white")
        
        start_btn = tk.Button(control_frame, text="Start", font=large_font, width=5, command=self.start_auto_move)
        stop_btn = tk.Button(control_frame, text="Stop", font=large_font, width=5, command=self.stop_move)
        start_btn.pack(side="left", padx=5)
        stop_btn.pack(side="left", padx=5)

        control_frame.grid(row=0, column=0, sticky="nesw", padx=0, pady=(5, 5))
        control_frame.pack(side="left", padx=10, pady=5, fill="both", expand=True)

        # Second child frame (Up, Down)
        direction_frame = tk.Frame(self,  bg="white")

        ## Creating up button
        up_btn = tk.Button(direction_frame, text="Up", font=large_font, width=5)
        up_btn.pack(side="left", padx=5)

        # Bind press and release events
        ## lambda function is used to pass the event to the function
        ## and to avoid calling the function directly. It is necessary!
        up_btn.bind("<ButtonPress-1>", lambda event: self.move_piston_up())
        up_btn.bind("<ButtonRelease-1>", lambda event: self.stop_move())

        ## Creating down button
        down_btn = tk.Button(direction_frame, text="Down", font=large_font, width=5)
        down_btn.pack(side="left", padx=5)

        # Bind press and release events
        ## lambda function is used to pass the event to the function
        ## and to avoid calling the function directly. It is necessary!
        down_btn.bind("<ButtonPress-1>", lambda event: self.move_piston_down())
        down_btn.bind("<ButtonRelease-1>", lambda event: self.stop_move())

        ## Final placing of the frame
        direction_frame.grid(row=0, column=1, sticky="nesw", padx=0, pady=(5, 5))
        direction_frame.pack(side="right", padx=10, pady=5, fill="both", expand=True)
        ## Logging function to set up the logger
        self.logger = logging.getLogger("AppLogger")
        self.logger.info("Control frame is initialized")

        ## Initialize the variables
        self.moving = False
        self.upstatut, self.downstatut = False, False
        self.upstatus, self.downstatus = False, False

        self.set_load_to_voltage()
        self.set_normal_voltage()

        self.serial_dataframe = None
        self.experiment = False

    def check_output_file(self):
        if self.output_app.file_path.get() != "":
            self.logger.info(f"Output file is set to {self.output_app.file_path.get()}")
            return True
        else:
            self.logger.info("Output file is not set. Set it!")
            return False

    def set_load_to_voltage(self):
        if self.machine_app is not None:
            try:
                 self.machine_app.lv_var.set(self.ar._Volt_to_load)
            except Exception as e:
                self.logger.info(f"Error during setting load to voltage: {e}")
                
    def set_normal_voltage(self):
        if self.machine_app is not None:
            try:
                self.machine_app.nv_var.set(self.ar._No_load_Voltage)
            except Exception as e:
                self.logger.info(f"Error during setting normal voltage: {e}")


    def set_frequency(self):
        if self.shared_config is not None:
            
            frequency = (1 / int(self.shared_config.f_entry.get()))*1000
            print(f"Frequency is set to {frequency}")
            try:
                self.ar.send_data(1, int(frequency))
            except Exception as e:
                self.logger.info(f"Error during setting frequency: {e}")
        else:
            self.logger.info("Shared config is not set. Cannot set frequency")

    def move_piston_up(self):
        if not self.upstatus:
            self.upstatus = True
            self.moving = True
            self.ar.move_piston(direction = "up")
            self.logger.info("Piston is moving up: Maximum move duration is -> 10 seconds")
            self.shared_application.clear_table()
        else:
            self.logger.info("Piston is already moving. Please stop it before moving in the other direction")

    def move_piston_down(self):
        if not self.downstatus:
            self.downstatus = True
            self.moving = True
            self.ar.move_piston(direction = "down")
            self.logger.info("Piston is moving down: Maximum move duration is -> 10 seconds")
            self.shared_application.clear_table()
        else:
            self.logger.info("Piston is already moving. Please stop it before moving in the other direction")

    def start_auto_move(self):
        
        if self.check_output_file() == False:
            messagebox.showerror("Error", "Output file is not set. Set it!")
            return
        
        if not self.moving:
            self.moving = True
            self.experiment = True
            self.default_piston_move_duration = int(self.shared_config.md_entry.get())
            self.default_piston_move_duration = self.default_piston_move_duration*1000 ## in seconds
            self.set_frequency()
            ## Never use functions directly in the Thread
            ## it will be executed in the main thread so it will block the GUI
            ## use args to pass the arguments to the function
            self.thread = Thread(target=self.move_and_read, args=(self.default_piston_move_duration,), daemon=False)
            self.thread.start()
            print("Thread started")
        
        ## Sometimes the thread is not finished yet
        ## and the user is trying to start a new one
        ## It is not a problem but it is better to inform the user
        if self.thread.is_alive():
            self.logger.info("Auto move is in progress. Please stop it before starting a new one or wait for it to finish")
        else:
            self.logger.info("Auto move is finished. You can start a new one")
            self.upstatus, self.downstatus = False, False
            self.moving = False

    ## This function is abstracted from main arudino class
    ## to allow for easy testing and debugging
    def move_and_read(self, duration = 5000, direction = "down", maxwait=10):
        print("Starting move_and_read")
        try:
            self.ar.auto_move(move_duration = duration, direction=direction)
            self.logger.info(f"Piston is moving for {duration} ms in {direction} direction")
        except Exception as e:
            self.logger.info(f"Error during auto move: {e}")
            self.moving = False
            return

        id = 0

        self.serial_dataframe = pd.DataFrame(columns=['id', 'Time (s)', 'Load (kg)', 'Force (N)'])
        self.shared_application.clear_table()

        prev_time = time.time()
        T = 0
        while self.ar.in_waiting <= 0:
            dt = time.time() - prev_time
            if dt > 1:
                print("waiting for data")
                prev_time = time.time()
                T += 1
            if T > maxwait:
                print("No data")
                return None
        ## read labels
        raw = self.ar.read_until()
        labels = raw.decode("utf-8").strip().split("\t")
        print(labels)

        ## TODO: Change the block below
        ## Read the first incoming data
        raw = self.ar.read_until()

        while raw:    
            decoded = raw.decode("utf-8").strip()
            self.values = list(map(float, decoded.split()))

            self.values = [id, self.values[0], self.values[2], self.values[2]*9.81]
            id += 1
            self.serial_dataframe.loc[len(self.serial_dataframe)] = self.values
            
            print(self.values)
            self.shared_application.add_row(data = self.values)

            raw = self.ar.read_until()

        self.moving = False
        self.serial_dataframe["Adjusted force (N)"] = self.serial_dataframe["Force (N)"] - self.serial_dataframe["Force (N)"].iloc[0]
        self.serial_dataframe.to_csv(self.output_app.file_path.get(), index=False, sep = ";")
        self.output_app.file_path.set("")

    def stop_move(self):
        if self.moving:
            self.ar.STOP()
            self.logger.info("Piston is stopped. Ready for the next move")
            
            ## Here we need to put self.moving to False
            ## to allow for the next move to be started
            self.moving = False
            self.upstatus, self.downstatus = False, False
            self.experiment = False
        else:
            self.logger.info("Piston is already stopped. Ready for the next move")
            
            ## It is an assurance to reinitialize the moving variable
            ## in case the stop button is pressed twice
            self.moving = False
            self.upstatus, self.downstatus = False, False
            self.experiment = False

        if self.shared_application.has_data():
            self.logger.info("Data saved to a file")



        
