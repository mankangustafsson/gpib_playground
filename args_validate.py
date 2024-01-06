import argparse
from quantiphy import Quantity


def valid_frequency(f):
    try:
        frequency = Quantity(f, 'Hz')
        return frequency
    except ValueError:
        raise argparse.ArgumentTypeError(f'{f} is not a valid frequency')


def add_frequency(parser, flag='-f', default=None, help_prefix=''):
    parser.add_argument(flag, type=valid_frequency, metavar='frequency',
                        default=default, help='desired frequency. '
                        f'{help_prefix} Decimal values with suffixes '
                        'k, M and G is also allowed')
