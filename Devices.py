from enum import Enum, auto
import pyvisa
import time


class Device:
    class Type(Enum):
        COUNTER = (auto(),)
        POWER_METER = (auto(),)
        OSCILLOSCOPE = (auto(),)
        RF_GEN = (auto(),)
        VNA = (auto(),)
        SPECTRUM_ANALYZER = (auto(),)
        ATTENUATOR_DRIVER = (auto(),)
        PSU = auto()

    def __init__(self, address, name, deviceType, idQuery="*IDN?", term=None):
        self.address = address
        self.name = name
        self.deviceType = deviceType
        self.idQuery = idQuery
        self.term = term
        self.dev = None

    def __del__(self):
        if self.dev:
            self.dev.close()

    def connect(self, verbose=True):
        rm = pyvisa.ResourceManager()
        try:
            if self.address.startswith("ASRL"):
                self.dev = rm.open_resource(self.address, baud_rate=115200)
            else:
                self.dev = rm.open_resource(self.address)

            self.dev.timeout = 5000
            if self.term is not None:
                self.dev.read_termination = self.term
                self.dev.write_termination = self.term
            if verbose:
                print("Connecting to " + self.address + "...", end="", flush=True)
            name = self.dev.query(self.idQuery)
            while not self.name in name:
                time.sleep(0.1)
                name = self.dev.query(self.idQuery)
            if verbose:
                print("connected to " + name)
            return self.dev
        except:
            print(f"Failed to connect to {self.address}")
            return self.dev
