from Devices import Device
from Lab import Lab

from quantiphy import Quantity
import sys
import time

if __name__ == "__main__":
    try:
        center = Quantity(sys.argv[1], "Hz")
        span = Quantity(sys.argv[2], "Hz")

        dev = Lab.connectByType(
            Device.Type.SPECTRUM_ANALYZER, hint="E4407", verbose=True
        )
        if dev is None:
            exit(1)

        print(
            "Setting span {} - {}".format(
                Quantity(center - span / 2, "Hz"), Quantity(center + span / 2, "Hz")
            )
        )
        dev.write(":SENS:FREQ:CENTER {:12.0f}Hz".format(center))
        dev.write(":SENS:FREQ:SPAN {:12.0f}Hz".format(span))
        dev.query("*OPC?")
        dev.write(":CALC:MARKER1:MAX")
        dev.write(":CALC:MARKER1:CPEAK:STATE ON")
        dev.write(":CALC:MARKER1:FCOUNT:STATE ON")
        dev.query("*OPC?")
        time.sleep(0.1)
        pf = Quantity(dev.query(":CALC:MARKER1:FCOUNT:X?"), "Hz")
        pp = Quantity(float(dev.query(":CALC:MARKER1:Y?")), "dBm")
        print("Peak {:3.2q} at {}".format(pp, pf))
    except IndexError:
        raise SystemExit("Usage: {} center span".format(sys.argv[0]))
