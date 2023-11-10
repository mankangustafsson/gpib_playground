from Devices import Device
from Lab import Lab

import argparse
import array
import sys
import time

def valid_commands(cmd):
    if cmd.lower() not in ['load', 'save', 'default']:
        msg = '%s is not a valid command' % cmd
        raise argparse.ArgumentTypeError(msg)
    return cmd.lower()

def valid_genders(genders):
    if genders.upper() not in ['MM', 'FF', 'M0', 'F0']:
        msg = '%s is not a valid gender combo' % genders
        raise argparse.ArgumentTypeError(msg)
    return genders.upper()

def load_kit(inputFile):
      print('Loading cal kit from file to VNA...', end = '', flush = True)
      data = array.array('b')
      while True:
            try: data.fromfile(inputFile, 1024)
            except EOFError: break
      inputFile.close()
      dev.write_binary_values('INPUCALK', data, is_big_endian=True,
                              header_fmt='hp', datatype='b')
      dev.write('OPC?; SAVEUSEK')
      print('..done.')

def save_kit(outputFile, beep = False):
      print('Saving cal kit from VNA to file...', end = '', flush = True)
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

def set_default_kit(genders):
    print('Loading default %s cal kit to VNA...' % genders, flush = True)
    dev.write('CALKN50') # To get the class definitations like we want
    dev.write('MODI1')
    
    print('Short male...', end ='', flush = True)
    dev.write('DEFS 1')
    dev.write('STDTSHOR')
    dev.write('OFSZ 50')
    dev.write('OFSD 26.296763E-12')
    dev.write('OFSL 0.0E+9')
    dev.write('C0 1.972678')
    dev.write('C1 6613.309399')
    dev.write('C2 -1625.587777')
    dev.write('C3 94.519818')
    dev.write('MINF 0')
    dev.write('MAXF 6E+9')
    dev.write('STDD')
    print('done')
      
    print('Open male...', end ='', flush = True)
    dev.write('DEFS 2')
    dev.write('STDTOPEN')
    dev.write('OFSZ 50')
    dev.write('OFSD 43.059930E-12')
    dev.write('OFSL 1.818363E+9')
    dev.write('C0 -14.992043')
    dev.write('C1 -1009.382660')
    dev.write('C2 1377.725656')
    dev.write('C3 -138.223997')
    dev.write('MINF 0')
    dev.write('MAXF 6E+9')
    dev.write('STDD')
    print('done')
      
    if genders in ['MM', 'M0']:
        print('Load male...', end ='', flush = True)
        dev.write('DEFS 3')
        dev.write('LABS "LOAD"')
        dev.write('STDTLOAD')
        dev.write('OFSZ 52.383099')
        dev.write('OFSD 17.961624E-12')
    else: # 'FF' & 'F0'
        print('Load female...', end ='', flush = True)
        dev.write('DEFS 3')
        dev.write('LABS "LOAD"')
        dev.write('STDTLOAD')
        dev.write('OFSZ 50.589652')
        dev.write('OFSD 29.614480E-12')
    dev.write('OFSL 0.0E+9')
    dev.write('C0 0.0')
    dev.write('C1 0.0')
    dev.write('C2 0.0')
    dev.write('C3 0.0')
    dev.write('MINF 0')
    dev.write('MAXF 6E+9')
    dev.write('STDD')
    print('done')
    if genders == 'MM':
        print('Thru male...', end ='', flush = True)
        dev.write('DEFS 4')
        dev.write('STDTDELA')
        dev.write('OFSZ 50.747533')
        dev.write('OFSD 42.264620E-12')
    elif genders == 'FF':
        print('Thru female...', end ='', flush = True)
        dev.write('DEFS 4')
        dev.write('STDTDELA')
        dev.write('OFSZ 50')
        dev.write('OFSD 76.991933E-12')
    else: 
        print('No delay thru ...', end ='', flush = True)
        dev.write('DEFS 4')
        dev.write('STDTDELA')
        dev.write('OFSZ 50')
        dev.write('OFSD 0.0E-12')
    dev.write('OFSL 0.0E+9')
    dev.write('MINF 0')
    dev.write('MAXF 6E+9')
    dev.write('STDD')
    print('done')

    print('Short female...', end ='', flush = True)
    dev.write('DEFS 7')
    dev.write('STDTSHOR')
    dev.write('OFSZ 50')
    dev.write('OFSD 0.0E-12')
    dev.write('OFSL 962.266512E+9')
    dev.write('C0 28.454226')
    dev.write('C1 2380.746494')
    dev.write('C2 -3135.518359')
    dev.write('C3 358.471292')
    dev.write('MINF 0')
    dev.write('MAXF 6E+9')
    dev.write('STDD')
    print('done')
    
    print('Open female...', end ='', flush = True)
    dev.write('DEFS 8')
    dev.write('STDTOPEN')
    dev.write('OFSZ 50')
    dev.write('OFSD 0.0E-12')
    dev.write('OFSL 0.0E+9')
    dev.write('C0 0')
    dev.write('C1 0')
    dev.write('C2 0')
    dev.write('C3 0')
    dev.write('MINF 0')
    dev.write('MAXF 6E+9')
    dev.write('STDD')
    print('done')
    kitname = 'SMA (' + genders +')'
    dev.write('LABK "%s"' %kitname)
    dev.write('KITD')
    dev.write('OPC?; SAVEUSEK; SOFR')
    print('Default cal kit loaded.')
      
parser = argparse.ArgumentParser()
parser.add_argument('command', type = valid_commands, nargs='?',
                    default = 'save',
                    help = 'valid commands are: load, save and default. '
                    'save is the default')
parser.add_argument('genders', type = valid_genders, nargs='?',
                    default = 'MM',
                    help = 'valid genders: MM, FF, F0 & M0. '
                    'MM is the default. First letter is gender of load. '
                    'Second letter is gender of thru port. '
                    '0 means no thru, i.e. mixed connector.')
parser.add_argument('-i', type = argparse.FileType('rb'),
                    metavar = 'input_file', nargs = '?',
                    help = 'file to use for load command')
parser.add_argument('-o', type = argparse.FileType('wb'),
                    metavar = 'output_file', nargs = '?',
                    help = 'file to use for save and default command')
args = parser.parse_args()

dev = Lab.connectByType(Device.Type.VNA, hint='8753')

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
      set_default_kit(args.genders)
      if args.o is not None:
            save_kit(args.o)

dev.close()
