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

    def close(self):
        if self.dev is not None:
            try:
                self.dev.close()
            except Exception:
                pass
            finally:
                self.dev = None

    def __del__(self):
        self.close()

    def connect(self, verbose=True):
        self.close()
        rm = pyvisa.ResourceManager()
        dev = None
        try:
            if self.address.startswith("ASRL"):
                dev = rm.open_resource(self.address, baud_rate=115200)
            else:
                dev = rm.open_resource(self.address)

            dev.timeout = 5000
            if self.term is not None:
                dev.read_termination = self.term
                dev.write_termination = self.term
            if verbose:
                print("Connecting to " + self.address + "...", end="", flush=True)

            name = None
            for _ in range(10):
                name = dev.query(self.idQuery)
                if self.name in name:
                    self.dev = dev
                    if verbose:
                        print("connected to " + name)
                    return self.dev
                time.sleep(0.1)

            raise ConnectionError(
                f"Unexpected identity response {name!r} from {self.address}"
            )
        except Exception as exc:
            if dev is not None:
                try:
                    dev.close()
                except Exception:
                    pass
            self.dev = None
            print(f"Failed to connect to {self.address}: {exc}")
            return None
