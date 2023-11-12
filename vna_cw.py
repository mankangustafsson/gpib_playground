from Devices import Device
from Lab import Lab
from quantiphy import Quantity

import argparse


def valid_frequency(f):
    try:
        frequency = Quantity(f, 'Hz')
        return frequency
    except ValueError:
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
        power = Quantity(pf, 'dB')
        if power < -75.0 or power > -5.0:
            raise argparse.ArgumentTypeError(f'{power} is outside valid range')
        return power
    except argparse.ArgumentTypeError:
        raise
    except ValueError:
        raise argparse.ArgumentTypeError(f'{p}%s is not a power')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=valid_frequency, metavar='frequency',
                        help='desired frequency.'
                        ' Decimal values with suffixes k, M and G is'
                        ' also allowed')
    parser.add_argument('-p', type=valid_port, metavar='port',
                        default='1', help='desired output port')
    parser.add_argument('-d', type=valid_power, metavar='power',
                        default='-10.0', help='desired output power in dBm')
    parser.add_argument('-u', metavar='unit',
                        default='8722', help='unit to connect to')
    args = parser.parse_args()
    # print(args)

    dev = Lab.connectByType(Device.Type.VNA, hint=args.u, verbose=False)
    if dev is None:
        exit(1)

    q = f'{args.p}; POWE {args.d}; CWFREQ {args.f}'
    #print(q)
    dev.write(q)
    dev.close()
