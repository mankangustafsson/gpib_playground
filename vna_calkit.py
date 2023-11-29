from Devices import Device
from Lab import Lab

import argparse
import array


def valid_commands(cmd):
    if cmd.lower() not in ['load', 'save', 'default', 'kits']:
        msg = '%s is not a valid command' % cmd
        raise argparse.ArgumentTypeError(msg)
    return cmd.lower()


def valid_genders(genders):
    if genders.upper() not in ['MM', 'FF', 'M0', 'F0']:
        msg = '%s is not a valid gender combo' % genders
        raise argparse.ArgumentTypeError(msg)
    return genders.upper()


def load_kit(inputFile):
    print('Loading cal kit from file to VNA...', end='', flush=True)
    data = array.array('b')
    while True:
        try:
            data.fromfile(inputFile, 1024)
        except EOFError:
            break
    inputFile.close()
    dev.write_binary_values('INPUCALK', data, is_big_endian=True,
                            header_fmt='hp', datatype='b')
    dev.write('OPC?; SAVEUSEK')
    print('..done.')


def save_kit(outputFile, beep=False):
    print('Saving cal kit from VNA to file...', end='', flush=True)
    data = dev.query_binary_values('OUTPCALK', is_big_endian=True,
                                   header_fmt='hp', datatype='c')
    binaryData = bytearray()
    for b in data:
        binaryData += b
    outputFile.write(binaryData)
    outputFile.close()
    if beep:
        dev.write('EMIB; SOFR')
    print('..done.')


def set_default_kit(kit, genders):
    for ck in Lab.calkits:
        if ck.short_name == kit:
            ck.load(dev, genders)
            return
    print(f'No kit named {kit} found!')


def print_kits():
    for ck in Lab.calkits:
        ck.print_kit()
        if not ck.verify():
            print('Calkit {ck} has duplicate standards')


parser = argparse.ArgumentParser()
parser.add_argument('command', type=valid_commands, nargs='?',
                    default='save',
                    help='valid commands are: load, save, default and kits. '
                    'save is the default')
parser.add_argument('genders', type=valid_genders, nargs='?',
                    default='MM',
                    help='valid genders: MM, FF, F0 & M0. '
                    'MM is the default. First letter is gender of load. '
                    'Second letter is gender of thru port. '
                    '0 means no thru, i.e. mixed connector.')
parser.add_argument('-i', type=argparse.FileType('rb'),
                    metavar='input_file', nargs='?',
                    help='file to use for load command')
parser.add_argument('-o', type=argparse.FileType('wb'),
                    metavar='output_file', nargs='?',
                    help='file to use for save and default command')
parser.add_argument('-u', metavar='unit',
                    default='8722', help='unit to connect to: 8753 or 8722')
parser.add_argument('-k', metavar='kit',
                    default='3.5mm', help='calkit to use as default: '
                    'SMA or 3.5mm')

args = parser.parse_args()

dev = Lab.connectByType(Device.Type.VNA, hint=args.u)

if args.command == 'save':
    if args.o is not None:
        save_kit(args.o, True)
    else:
        print('save command requires -o argument')
elif args.command == 'load':
    if args.i is not None:
        load_kit(args.i)
    else:
        print('load command requires -i argument')
elif args.command == 'default':
    set_default_kit(args.k, args.genders)
    if args.o is not None:
        save_kit(args.o)
elif args.command == 'kits':
    print_kits()
if dev is not None:
    dev.close()
