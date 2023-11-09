from RfGen import RfGen

import argparse
from quantiphy import Quantity


def valid_frequency(f):
    try:
        frequency = Quantity(f, 'Hz')
        return frequency
    except:
        msg = '%s is not a valid frequency' % f
        raise argparse.ArgumentTypeError(msg)


def valid_power(p):
    try:
        pf = float(p)
        power = Quantity(pf, 'dBm')
        if power < -135.0 or power > 20.0:
            msg = '%s is outside valid range' % power
            raise argparse.ArgumentTypeError(msg)
        return power
    except argparse.ArgumentTypeError:
        raise
    except:
        msg = '%s is not a power' % p
        raise argparse.ArgumentTypeError(msg)


def valid_commands(cmd):
    if cmd.lower() not in ['on', 'off']:
        msg = '%s is not a valid command' % cmd
        raise argparse.ArgumentTypeError(msg)
    return cmd.lower()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=valid_commands, nargs='?',
                        default='on',
                        help='valid commands are: on, off. Controls RF output')
    parser.add_argument('-f', type=valid_frequency, metavar='frequency',
                        help='desired frequency.'
                        ' Decimal values with suffixes k, M and G is'
                        ' also allowed')
    parser.add_argument('-p', type=valid_power, metavar='power',
                        help='desired output power in dBm')
    args = parser.parse_args()

    RfGen().setCW(args.command == 'on', args.f, args.p, True)
