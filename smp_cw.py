import pyvisa
from quantiphy import Quantity
import sys
import time

address = 'GPIB0::28::INSTR'
rm = pyvisa.ResourceManager()
dev = rm.open_resource(address)
dev.timeout = 5000
print('Connecting to ' + address + '...',
                  end ='', flush = True)
name = dev.query('*IDN?')
while not 'SMP02' in name:
    time.sleep(0.1)
    name = dev.query('*IDN?')
print('connected to ' + name)
try:    
    freq = Quantity(sys.argv[1], 'Hz')
    power = Quantity(sys.argv[2], 'dBm')
    state = sys.argv[3].upper()
    if state == 'OFF':
        dev.write('*RST;*CLS')
    print('Setting {} {} {}'.format(freq, power, state.lower()))
    dev.write('SOURCE:FREQUENCY:CW {}'.format(freq))
    dev.write('POW {:3.1f}'.format(power))
    dev.write('OUTP:STAT {}'.format(state))
except IndexError:
    raise SystemExit('Usage: {} frequency dBm on/off'.format(sys.argv[0]))
