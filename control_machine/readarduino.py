import serial
import time

# import builtins
import numpy as np

import serial.tools.list_ports

from copy import deepcopy
from Params import *


def copy_param(dict_param):
    ret = deepcopy(dict_param)
    for param, value in dict_param.items():
        if not value["use"]:
            del ret[param]
    return ret


arduino_move_limits = copy_param(arduino_move_limits)
arduino_custom_params = copy_param(arduino_custom_params)


def timeout_corection(timeout, delay):
    if delay / 1000.0 >= timeout:
        print(
            f"timeout = {timeout} s too small for delay = {delay} {arduino_custom_params[delay_key]['unit']}"
        )
        timeout = np.ceil(2 * delay * 1.1 / 1000) / 2
    return timeout


def find_arduino():
    """
    Find serial port with "arduino" anywhere in PortInfo.
    If no port found, display list of available port then ask to choose one of them.
    If nothing is written in input wait 10s for a new port to be connected and return it.
    Returns
    -------
    str or None
        serial port : "device"

    """
    # serial_port = [p.device for p in serial.tools.list_ports.grep("arduino")]
    ports = get_ports()
    serial_port = [p.device for p in ports if hasattr(p, "Font")]
    if len(serial_port) == 1:
        serial_port = serial_port[0]
        print(f"Arduino find in port {serial_port}")
        return serial_port
    elif len(serial_port) > 1:
        print(f"Arduino find in ports {serial_port}")
        return serial_port
    else:
        print("Arduino port not found, available serial device are:")
        for p in ports:
            print(p.__dict__)
            print("\n")
        time.sleep(0.5)
        serial_port = input(
            "Enter device and validate, or validate and plug in arduino: "
        )
        if serial_port:
            return serial_port
        else:
            print("Waiting for arduino connection...")
            return find_new_port()


def get_ports():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if (
            "arduino".casefold()
            in " ".join([str(value) for value in p.__dict__.values()]).casefold()
        ):
            p.Font = "bold"
    return ports


def find_new_port(maxtime=10):
    """
    Parameters
    ----------
    maxtime : number, optional
        Time to wait for port connexion in seconds. The default is 10.

    Returns
    -------
    serial_port : str or None
        New port connected or nothing.

    """
    initial_ports = list(serial.tools.list_ports.comports())
    number_of_available_port = len(initial_ports)
    ports = list(serial.tools.list_ports.comports())
    prev_time = time.time()
    while len(ports) == number_of_available_port:
        ports = list(serial.tools.list_ports.comports())
        dt = time.time() - prev_time
        if dt > maxtime:
            print("No new connection")
            return None
    if len(ports) < number_of_available_port:
        disconected_ports = list(set(initial_ports) - set(ports))
        print(
            f"The device at port {disconected_ports[0].device} has been disconnected"
        )
        return None
    else:
        newports = list(set(ports) - set(initial_ports))
        serial_port = newports[0].device
        print(f"New device connected on port {serial_port}")
        return serial_port


class Arduino(serial.Serial):
    def __init__(self, serial_port, baud_rate=9600, timeout=1):
        super().__init__(serial_port, baud_rate, timeout=timeout)
        time.sleep(5)  # wait for serial connexion to set up
        self.arduino_move_limits = self.read_arduino_prog_param(
            arduino_move_limits, False
        )
        self.arduino_custom_params = self.read_arduino_prog_param(
            arduino_custom_params, True
        )
        print(
            "".join(
                [
                    f"{key} = {getattr(self,'_'+key)} {self.arduino_custom_params[key]['unit']}\n"
                    for key in self.arduino_custom_params.keys()
                ]
            )
        )

    def read_arduino_prog_param(self, param_dico, is_attribute):
        dico = deepcopy(param_dico)
        params_default = self.read_until()
        if not params_default:
            raise Exception("No data read from serial port")
        results = params_default.decode("utf-8").strip().split()
        for key, result in zip(dico.keys(), results):
            if is_attribute:
                setattr(self, "_" + key, dico[key]["vtype"](result))
            dico[key]["default_value"] = dico[key]["vtype"](result)
        return dico

    def close(self):
        """Close port"""
        self.reset_input_buffer()
        self.reset_output_buffer()
        self.STOP()
        super().close()

    def __send_data(self, tag, data):
        if tag in TAGS:
            self.write(bytes([tag]) + (str(round(data, 3)) + "x").encode())
        else:
            raise Exception(f"tag should be any of {TAGS}")

    def correcttimeout(self):
        self.timeout = self.timeout

    def getter(self, key):
        return getattr(self, "_" + key)

    def setter(self, key, value):
        self.send_value(key, value)
        setattr(self, "_" + key, value)

    vars()[delay_key] = property(
        lambda self, k=delay_key: self.getter(k),
        lambda self, value, k=delay_key: self.setter(k, value)
        or self.correcttimeout(),
    )

    keylist = list(arduino_custom_params.keys())
    keylist.remove(delay_key)

    for key in keylist:
        vars()[key] = property(
            lambda self, k=key: self.getter(k),
            lambda self, value, k=key: self.setter(k, value),
        )

    @serial.Serial.timeout.setter
    def timeout(self, value):
        if self.timeout is not None:
            delay = getattr(self, delay_key)
            value = timeout_corection(value, delay)
            if value != self.timeout:
                print(f"Set timeout to {value} s")
        serial.Serial.timeout.fset(self, value)

    def send_value(self, key, value):
        vtype = self.arduino_custom_params[key]["vtype"]
        if vtype is int or vtype == "int":
            if not isinstance(value, int):
                value = round(value)
                print(f"{key} is not integer, using rounded {key} = {value}")
        if value != getattr(self, key):
            print(
                f"Set {key} to {value} {self.arduino_custom_params[key]['unit']}"
            )
            self.__send_data(self.arduino_custom_params[key]["code"], value)

    def STOP(self):
        self.write(bytes([STOP]))

    def SETZERO(self):
        self.write(bytes([ZERO]))

    def get_current_volt(self):
        self.write(bytes([PRINT_VOLT]))
        while self.in_waiting <= 0:
            pass
        raw = self.read_until()
        print(
            f"Current output voltage = {raw.decode('utf-8').strip()} V",
            flush=True,
        )

    def send_instruction(self, instruction, **limitation):
        if instruction not in ["up", "down"]:
            raise Exception(
                f"Invalid instruction: {instruction} should be 'up' or 'down'"
            )
        argname = [
            name for name in limitation.keys() & self.arduino_move_limits.keys()
        ]
        n = len(argname)
        if n == 0:
            argname = default_move_limits
            value = self.arduino_move_limits[argname]["default_value"]
        elif n > 1:
            raise Exception(
                f"Argument error {limitation} \n argument should be ONE of {self.arduino_move_limits.keys()}"
            )
        else:
            argname = argname[0]
            value = limitation[argname]
        Type = self.arduino_move_limits[argname]["vtype"]
        if not isinstance(value, Type):
            print(
                f"{argname.replace('_',' ')} = {value} is not {Type}, changing it to {Type(value)} "
            )
        if instruction == "up":
            self.__send_data(
                self.arduino_move_limits[argname]["code_UP"], Type(value)
            )
        if instruction == "down":
            self.__send_data(
                self.arduino_move_limits[argname]["code_DOWN"], Type(value)
            )

    def _wait_and_read_data(self, maxwait=10):
        prev_time = time.time()
        data = []
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
        ##read data
        raw = self.read_until()
        while raw:
            data.append(
                np.asarray([raw.decode("utf-8").strip().split()])
                .squeeze()
                .astype(float)
            )
            print(formatstr.format(*data[-1]), flush=True)
            raw = self.read_until()
        return np.core.records.fromarrays(
            [*np.asarray(data).transpose()], names=labels
        )

    def experiment(self, maxwait=10, **limitation):
        self.reset_input_buffer()
        self.reset_output_buffer()
        self.send_instruction("down", **limitation)
        return self._wait_and_read_data(maxwait=maxwait)


def format_str(labels, tabulation=tabulationsize):
    for label in labels:
        yield f"{{:<{len(label)+tabulation}}}"


def running_experiment(
    serial_port,
    baud_rate=9600,
    timeout=1,
    delay=None,
    volt2load=None,
    **limitation,
):
    """
    Parameters
    ----------
    serial_port : str
        Serial port of arduino.
    baud_rate : INT, optional
        Baud rate of serial communication in arduino programm. The default is 9600.
    timeout : float, optional
        Maximum delay in second to wait for data. The default is 1.
    delay : INT, optional
        Delay in ms between data arduino send. The default is None : value in arduino programm.
    volt2load : FLOAT, optional
        Conversion factor volt to load. The default is None : value in arduino programm.
    **limitation : argument in arduino_move_limits.keys() with value
        choosing witch limitation to apply to movement
    Returns
    -------
    Numpy array of data received.

    """
    # assert (duration is None) != (
    #     distance is None
    # ), "Have to specify either duration or distance"
    with Arduino(serial_port, baud_rate, timeout=timeout) as Ar:
        default_delay = Ar.arduino_custom_params[delay_key]["default_value"]
        if delay:
            setattr(Ar, delay_key, delay)
        else:
            assert (
                Ar.timeout > default_delay / 1000
            ), f"timeout = {Ar.timeout} s too small for default delay = {default_delay} {Ar.arduino_custom_params[delay_key]['unit']}"
        time.sleep(1)
        if volt2load is not None:
            Ar.send_volt2load(volt2load)
        return Ar.experiment(**limitation)


#%%

if __name__ == "__main__":
    duration = 5000
    delay = 300
    serial_port = find_arduino()
    if serial_port is not None:
        labels, data = running_experiment(
            serial_port, delay=delay, Maximum_move_duration=duration
        )
