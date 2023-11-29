from args_validate import add_frequency
from Lab import Lab
from PowerMeter import PowerMeter

import argparse
import sys


def valid_commands(cmd):
    if cmd.lower() not in ['preset', 'init', 'zero', 'read',
                           'oc1', 'oc0', 'probes']:
        msg = '%s is not a valid command' % cmd
        raise argparse.ArgumentTypeError(msg)
    return cmd.lower()


def valid_operation(op):
    if op.upper() not in ['A-B', 'B-A', 'A/B', 'B/A']:
        msg = '%s is not a valid operation' % op
        raise argparse.ArgumentTypeError(msg)
    return op.upper()


def valid_offset(o):
    try:
        offset = float(o)
        if offset < -99.99 or offset > 99.99:
            msg = '%f as offset is too small or too large' % offset
            raise argparse.ArgumentTypeError(msg)
        return offset
    except ValueError:
        msg = '%s is not a valid offset' % o
        raise argparse.ArgumentTypeError(msg)


def valid_unit(u):
    if u.lower() in ['w', 'watt']:
        return 'W'
    elif u.lower() in ['d', 'db', 'dbm']:
        return 'dBm'
    else:
        msg = '%s is not a valid unit' % u
        raise argparse.ArgumentTypeError(msg)


parser = argparse.ArgumentParser()
parser.add_argument('commands', type=valid_commands, nargs='*',
                    help='valid commands are: preset, init, zero, read and'
                    ' probes. probes prints probe info')
parser.add_argument('-a', type=int, choices=[1, 2, 3, 4], metavar='probe_id',
                    help='associates probe_id with sensor A')
parser.add_argument('-b', type=int, choices=[1, 2, 3, 4], metavar='probe_id',
                    help='associates probe_id with sensor B')
add_frequency(parser,
              help_prefix='Frequency to calculate calibration factor for.')
add_frequency(parser, flag='-f1',
              help_prefix='Frequency to use for probe 1, overrides -f.')
add_frequency(parser, flag='-f2',
              help_prefix='Frequency to use for probe 2, overrides -f.')
parser.add_argument('-o', type=valid_offset, metavar='offset',
                    help='offset to add to read values')
parser.add_argument('-oa', type=valid_offset, metavar='offset',
                    help='offset to add to read values read from sensor A, '
                    'overrides -o')
parser.add_argument('-ob', type=valid_offset, metavar='offset',
                    help='offset to add to read values read from sensor B, '
                    'overrides -o')
parser.add_argument('-op', type=valid_operation, metavar='operation',
                    help='two sensor read, valid operations are A-B, B-A,'
                    ' A/B and B/A')
parser.add_argument('-u', type=valid_unit, default='dBm', metavar='unit',
                    help='display values in unit. Valid units are dBm and '
                    'Watt')

args = parser.parse_args()
# print(args)

pm = PowerMeter()
if not args.commands:
    parser.print_help()

for cmd in args.commands:
    if cmd == 'init' or cmd == 'preset':
        pm.preset()
    elif cmd == 'zero':
        if args.a is None and args.b is None:
            print('zero command requires sensor A or B argument with a valid '
                  'probe')
            sys.exit(-1)
        if args.a is not None and args.b is not None:
            print('zero command can only be performed with one sensor at the '
                  'time')
            sys.exit(-1)
        sensor = 'A' if args.a is not None else 'B'
        probe = args.a if args.a is not None else args.b
        pm.zero(sensor, probe - 1)
    elif cmd == 'read':
        sensors = []
        probeList = []
        frequencies = []
        offsets = []
        if args.a is not None:
            sensors.append('A')
            probeList.append(args.a - 1)
        if args.b is not None:
            sensors.append('B')
            probeList.append(args.b - 1)
        if args.f1 is not None:
            frequencies.append(args.f1)
        if args.f2 is not None:
            frequencies.append(args.f2)
        if len(frequencies) == 0 and args.f is not None:
            frequencies.append(args.f)
        offsets.append(args.oa if args.oa is not None else 0 if args.o is None else args.o)
        offsets.append(args.ob if args.ob is not None else 0 if args.o is None else args.o)
        pm.read(sensors, probeList, frequencies, offsets, args.op, args.u)
    elif cmd == 'probes':
        Lab.printProbes()
    else:
        pm.test_port(cmd == 'oc1')
