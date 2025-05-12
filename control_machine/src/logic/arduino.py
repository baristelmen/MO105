import serial
from src.logic.Params import *
import time
import pandas as pd


def format_str(labels, tabulation=tabulationsize):
    for label in labels:
        yield f"{{:<{len(label)+tabulation}}}"

class Arduino(serial.Serial):
    def __init__(self, port, baudrate = 9600, timeout = 1):
        super().__init__(port = port, baudrate = baudrate)

        self.timeout = timeout

        self.reset_input_buffer()
        self.reset_output_buffer()

        self.read_serial_data()
        self.read_default_parameters()

        self.serial_dataframe = None

    def read_serial_data(self, buffer = None):
        if buffer is None:
            buffer = []
            while len(buffer) < 2:
                line = self.readline().decode('utf-8').strip()
                if line:
                    buffer.append(line)
                else:
                    raise Exception("No data read from serial port. Check arduino code")
            self._arduino_buffer = buffer

    def read_default_parameters(self):
        ## First thing that arduino send is the maximum move duration
        ## We need to have an integer value
        self._Maximum_move_duration = int(self._arduino_buffer[0])

        ## Second thing that arduino send is the sampling delay, volt to load and no load voltage
        ## The order is important, it should be the same as in arduino code
        self._Sampling_delay = self._arduino_buffer[1].split()[0]
        self._Volt_to_load = self._arduino_buffer[1].split()[1]
        self._No_load_Voltage = self._arduino_buffer[1].split()[2]

    def read_data(self):
        if self.in_waiting > 0:
            data = self.readline().decode('utf-8').rstrip()
            return data
        return None

    def close(self):
        """Close port"""
        self.reset_input_buffer()
        self.reset_output_buffer()
        self.STOP()
        super().close()

    def STOP(self):
        self.write(bytes([STOP]))

    ## Duration is in ms
    ## Direction is either "up" or "down"
    ## If duration is None, it will use the maximum move duration
    def move_piston(self, direction, move_duration = None):
        if move_duration is None:
            move_duration = self._Maximum_move_duration

        print(self._Maximum_move_duration)
        # print(f"Moving {direction} for {move_duration} ms")

        if direction not in ["up", "down"]:
            raise Exception(
                f"Invalid direction: {direction} should be 'up' or 'down'"
            )
        
        if int(move_duration) <= 0:
            raise Exception(
                f"Invalid duration: {move_duration} should be positive and non-zero"
            )

        if direction == "up":
            self.send_data(UP_t, int(move_duration))
        if direction == "down":
            self.send_data(DOWN_t, int(move_duration))

    def send_data(self, tag, data):
        if tag in TAGS:
            self.write(bytes([tag]) + (str(round(data, 3)) + "x").encode())
        else:
            raise Exception(f"tag should be any of {TAGS}")

    def stop(self):
        if self.upstatut or self.downstatut:
            self.upstatut = False
            self.downstatut = False
            self.STOP()

    def _wait_and_read_data(self, maxwait=10):

        self.serial_dataframe = pd.DataFrame(columns=['Time', 'LoadVolt', 'Load', 'Force'])

        prev_time = time.time()
        T = 0
        while self.in_waiting <= 0:
            dt = time.time() - prev_time
            if dt > 1:
                print("waiting for data")
                prev_time = time.time()
                T += 1
            if T > maxwait:
                print("No data")
                return None
        ## read labels
        raw = self.read_until()
        labels = raw.decode("utf-8").strip().split("\t")
        formatstr = "".join(format_str(labels, tabulation=tabulationsize))
        print(formatstr.format(*labels).strip())

        ## TODO: Change the block below

        ## Read the first incoming data
        raw = self.read_until()
#        self.serial_data = pd.DataFrame(columns=['Time', 'LoadVolt', 'Load', 'Force'])

        ## Read the rest of the data
        ## There is no check if there is a data or not.
        ## It is assumed that the data is always there
        ## If not, it will be controlled above?
        ## TODO: Add a logic here
        while raw:    
            decoded = raw.decode("utf-8").strip()
            self.values = list(map(float, decoded.split()))
            self.values.append(self.values[2]*9.81)
            self.serial_dataframe.loc[len(self.serial_dataframe)] = self.values
            print(self.values)
            raw = self.read_until()

        return self.serial_dataframe
    
    def auto_move(self, move_duration, direction = "down"):
        self.reset_input_buffer()
        self.reset_output_buffer()
        self.move_piston(direction, move_duration)
        # return self._wait_and_read_data()