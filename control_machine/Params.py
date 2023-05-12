READ_NOLOAD_VOLT = 0
READ_DELAY = 1
READ_VOLT2LOAD = 2
STOP = 3
UP_t = 4
DOWN_t = 5
UP_d = 6
DOWN_d = 7
ZERO = 8
READ_RADIUS = 9
PRINT_VOLT = 10
TAGS = [
    READ_NOLOAD_VOLT,
    READ_DELAY,
    READ_VOLT2LOAD,
    STOP,
    UP_t,
    DOWN_t,
    UP_d,
    DOWN_d,
    ZERO,
    READ_RADIUS,
    PRINT_VOLT,
]

# Values read from arduino at connection
arduino_move_limits = {
    "Maximum_move_duration": {
        "use": True,
        "unit": "ms",
        "vtype": int,
        "default_value": None,
        "help_text": "Maximum axe movement duration",
        "code_UP": UP_t,
        "code_DOWN": DOWN_t,
    },
    "Maximum_move_distance": {
        "use": False,
        "unit": "cm",
        "vtype": float,
        "default_value": None,
        "help_text": "Maximum axe movement distance\n(Depend on Radius)",
        "code_UP": UP_d,
        "code_DOWN": DOWN_d,
    },
}

default_move_limits = "Maximum_move_duration"
delay_key = "Sampling_delay"

arduino_custom_params = {
    delay_key: {
        "use": True,
        "vtype": int,
        "unit": "ms",
        "default_value": None,
        "code": READ_DELAY,
        "help_text": "Delay between registered datapoints",
    },
    "Volt_to_load": {
        "use": True,
        "vtype": float,
        "unit": "Kg/V",
        "default_value": None,
        "code": READ_VOLT2LOAD,
        "help_text": "Conversion factor from Voltage to load",
    },
    "Radius": {
        "use": False,
        "vtype": float,
        "unit": "cm",
        "default_value": None,
        "code": READ_RADIUS,
        "help_text": "Equivalent radius beetwen\nthe axe and the encoder",
    },
    "No_load_Voltage": {
        "use": True,
        "vtype": float,
        "unit": "Volt",
        "default_value": None,
        "code": READ_NOLOAD_VOLT,
        "help_text": "Value of Offset Output voltage of the amplifier"
        "(Read when arduino is connected)",
    },
}
tabulationsize = 4
