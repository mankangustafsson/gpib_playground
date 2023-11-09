import pyvisa

from quantiphy import Quantity
import sys
import time
import argparse

def valid_frequency(f):
    try:
        frequency = Quantity(f, 'Hz');
        return frequency
    except:
        raise argparse.ArgumentTypeError(f'{f} is not a valid frequency')

def valid_port(p):
    if p == '1':
        return 'S11'
    elif p == '2':
        return 'S22'
    raise argparse.ArgumentTypeError(f'{p} is not a valid port')

def valid_power(p):
    try:
        pf = float(p)
        power = Quantity(p, 'dB');
        if power < -75.0 or power > -5.0:
            raise argparse.ArgumentTypeError(f'{power} is outside valid range')
        return power
    except argparse.ArgumentTypeError:
        raise
    except:
        raise argparse.ArgumentTypeError(f'{p}%s is not a power')


parser = argparse.ArgumentParser()
parser.add_argument('-f', type = valid_frequency, metavar = 'frequency',
                    help = 'desired frequency.'
                    ' Decimal values with suffixes k, M and G is also allowed')
parser.add_argument('-p', type = valid_port, metavar = 'port', default = '1',
                    help = 'desired output port')
parser.add_argument('-d', type = valid_power, metavar = 'power',
                    default = '-10.0', help = 'desired output power in dBm')
args = parser.parse_args()
print(args)

rm = pyvisa.ResourceManager()
dev = rm.open_resource('GPIB1::16::INSTR')
dev.timeout = 1000
q = f'{args.p}; POWE {args.d}; CWFREQ {args.f}'
print(q)
dev.write(q)
dev.close()

