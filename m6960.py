import argparse
from quantiphy import Quantity
from Probe import Probe
import pyvisa
import time

def valid_commands(cmd):
    if cmd.lower() not in ['preset', 'init', 'read', 'probe']:
        msg = '%s is not a valid command' % cmd
        raise argparse.ArgumentTypeError(msg)
    return cmd.lower()


def valid_frequency(f):
    try:
        frequency = Quantity(f, 'Hz')
        return frequency
    except ValueError:
        msg = '%s is not a valid frequency' % f
        raise argparse.ArgumentTypeError(msg)


parser = argparse.ArgumentParser()
parser.add_argument('commands', type=valid_commands, nargs='*',
                    help='valid commands are: preset, init, read and'
                    ' probe. probe prints probe info')
parser.add_argument('-f', type=valid_frequency, metavar='frequency',
                    help='frequency to calculate calibration factor for. '
                    'Decimal values with suffixes k, M and G is also allowed')

args = parser.parse_args()
# print(args)

probe = Probe('MI6914', 100.0, 0.0, dict([(0.01E+9, 96.4),
                                          (2.0E+9, 98.9),
                                          (6.0E+9, 97.4),
                                          (10.0E+9, 96.4),
                                          (12.0E+9, 95.7),
                                          (14.0E+9, 95.2),
                                          (16.0E+9, 94.9),
                                          (18.0E+9, 93.0),
                                          (20.0E+9, 93.9),
                                          (22.0E+9, 93.7),
                                          (24.0E+9, 92.0),
                                          (26.0E+9, 91.3),
                                          (28.0E+9, 92.6),
                                          (30.0E+9, 90.5),
                                          (32.0E+9, 89.0),
                                          (34.0E+9, 89.6),
                                          (36.0E+9, 89.1),
                                          (38.0E+9, 85.6),
                                          (40.0E+9, 88.0)]))

if not args.commands:
    parser.print_help()
    exit(0)

rm = pyvisa.ResourceManager()
# print(rm.list_resources())
pm = rm.open_resource('GPIB2::13::INSTR')
pm.timeout = 3000
pm.read_termination = '\r\n'
pm.write_termination = '\r\n'

for cmd in args.commands:
    if cmd == 'init' or cmd == 'preset':
#        pm.write('RE')
#        print('1')
#        time.sleep(1)
        pm.write('SQ0')
        print('2')
        time.sleep(1)
        pm.write('AV200E')
        print('3')
        time.sleep(1)
        pm.write('LF4.7E')
        print('4')
        time.sleep(1)
        print(pm.query('RS'))
    elif cmd == 'read':
        cal_factor = 100.0
        if args.f is None:
            print('No frequency specified, using calibration factor 100')

        cal_factor = probe.get_cf(args.f)
        pm.write(f'CF{cal_factor:2.2f}E')
        time.sleep(0.2)
        pm.write('AV5E')
        #pm.write('TR00')
        for n in range(3):
            time.sleep(10)
            power = pm.query('')
            if power[0] == 'V' and power[2] == 'D':
                dbm = float(power[3:])
                print(f'{args.f:10q};{dbm:.2f}; dBm')
                break

    elif cmd == 'probe':
        print(f'\nProbe {probe}')
        probe.print_cal_table()
pm.close()
