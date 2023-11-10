from Devices import Device
from Lab import Lab

from quantiphy import Quantity
import sys

if __name__ == "__main__":
    try:
        freq = Quantity(sys.argv[1], 'Hz')
        power = Quantity(sys.argv[2], 'dBm')
        state = sys.argv[3].upper()

        dev = Lab.connectByType(Device.Type.RF_GEN, hint='SMP02', verbose=True)
        if dev is None:
            exit(1)

        if state == 'OFF':
            dev.write('*RST;*CLS')
        print('Setting {} {} {}'.format(freq, power, state.lower()))
        dev.write('SOURCE:FREQUENCY:CW {}'.format(freq))
        dev.write('POW {:3.1f}'.format(power))
        dev.write('OUTP:STAT {}'.format(state))
    except IndexError:
        raise SystemExit(f'Usage: {sys.argv[0]} frequency dBm on/off')
