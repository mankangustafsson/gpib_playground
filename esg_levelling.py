import argparse
import json
import pyvisa
import time

import Lab


def valid_range(start, stop):
    if start < 0 or stop < start or stop > 155:
        msg = '%d-%d is not a valid interval. 0-155 are the limits' % (start, stop)
        raise argparse.ArgumentTypeError(msg)
    return range(start, stop + 1)


def backup_entry(index, rf):
    freq = float(rf.query(f':SERV:PROD:CAL? 65,{index}'))
    offset = float(rf.query(f':SERV:PROD:CAL? 207,{index}'))
    return {"frequency": freq, "offset": offset}


def restore_entry(index, freq, offset, rf):
    rf.write(f':SERV:PROD:CAL 65,{index},{freq}')
    rf.write(f':SERV:PROD:CAL 207,{index},{offset}')
    print(f'Write freq/offset: {i:3}: {freq} {offset}')


def zero_entry(index, rf):
    rf.write(f':SERV:PROD:CAL 207,{index},0.0')
    print(f'Zero offset: {i:3}: 0.0')


parser = argparse.ArgumentParser()
parser.add_argument('command', choices=['backup', 'restore', 'verify', 'zero',
                                        'measure'])
parser.add_argument('--start', type=int, default=0,
                    help='start entry to operate on')
parser.add_argument('--stop', type=int, default=155,
                    help='stop entry to operate on')
parser.add_argument('--file', default='register_values.json',
                    help='file to read or write data from or to')
args = parser.parse_args()
# print(args)
the_range = valid_range(args.start, args.stop)

rm = pyvisa.ResourceManager()
# print(rm.list_resources())

rf = rm.open_resource('GPIB0::19::INSTR')
rf.read_termination = '\n'
rf.write_termination = '\n'
rf.query(':SYST:PRES; *OPC?;')
id = rf.query('*IDN?')
print(f'Connected to: {id}')

if args.command == 'backup':
    print(f'Backing up entry {args.start} to {args.stop} into {args.file}...')
    data = {}
    for i in the_range:
        data[str(i)] = backup_entry(i, rf)
    with open(args.file, 'w') as f:
        json.dump(data, f, indent=4)
        print('Done')

elif args.command == 'restore':
    print(f'Restoring from {args.file}, entry {args.start} to {args.stop}...')
    with open(args.file, 'r') as f:
        data = json.loads(f.read())
        success = True
        rf.write(':SERV:PROD:CAL:BEGIN')
        for i in the_range:
            if str(i) in data:
                entry = data[str(i)]
                restore_entry(i, entry['frequency'], entry['offset'], rf)
            else:
                print(f'Entry {i} not found in {args.file}!')
                success = False
        if success:
            rf.write(':SERV:PROD:CAL:STORE 65')
            rf.write(':SERV:PROD:CAL:STORE 207')
            rf.write(':SERV:PROD:CAL:END')
            rf.write(':SERV:PROD:CAL:PUP')
            print('Success')
        else:
            print('Restore failed')
        rf.query(':SYST:PRES; *OPC?')

elif args.command == 'verify':
    print(f'Verifying from {args.file}, entry {args.start} to {args.stop}...')
    with open(args.file, 'r') as f:
        data = json.loads(f.read())
        success = True
        for i in the_range:
            if str(i) in data:
                file_entry = data[str(i)]
                data_entry = backup_entry(i, rf)
                if file_entry != data_entry:
                    print(f'Entry {i} does not match, file = {file_entry} data = {data_entry}')
                    success = False
            else:
                print(f'Entry {i} not found in {args.file}!')
                success = False
        print('Verify success' if success else 'Verify failed')

elif args.command == 'zero':
    print(f'Zeroing offset value entries {args.start} to {args.stop}...')
    rf.write(':SERV:PROD:CAL:BEGIN')
    for i in the_range:
        zero_entry(i, rf)
    rf.write(':SERV:PROD:CAL:STORE 207')
    rf.write(':SERV:PROD:CAL:END')
    rf.write(':SERV:PROD:CAL:PUP')
    rf.query(':SYST:PRES; *OPC?')
    print('Done')

elif args.command == 'measure':
    probe = Lab.probes[1]  # HP8482A, sensor A
    # connect to power meter, assume probe is already zeroed
    pm = rm.open_resource('GPIB0::13::INSTR')
    pm.read_termination = '\r\n'
    pm.write_termination = '\r\n'

    print(f'Measuring power offset at frequencies from entry {args.start} to {args.stop} in {args.file}')
    with open(args.file, 'r') as f:
        data = json.loads(f.read())
        success = True
        for i in the_range:
            if str(i) in data:
                entry = data[str(i)]
                freq = entry['frequency']
                rf_cmd = '*CLS; :STAT:QUES:POW:ENAB 32767;'
                rf_cmd += ' :STAT:QUES:ENAB 32767;'
                rf_cmd += f' :OUTP:MOD OFF; :FREQ:CW {freq} Hz;'
                rf_cmd += ' :POWER 0 dBm; :OUTP ON'
                rf.write(rf_cmd)
                time.sleep(0.8)
                cf = probe.get_cf(freq)
                pmCommand = 'AE KB%.1fEN LG RL0 AP TR2 TR3' % cf
                reply = pm.query_ascii_values(pmCommand)
                offset = float(reply[0])
                entry['offset'] = -offset
                print(f'{i:3} {freq:16} Hz {offset:5} dBm')
            else:
                print(f'Entry {i} not found in {args.file}!')
                success = False
        if success:
            print('Measurements done, saving...', end='')
            f.close()
            with open(args.file, 'w') as fout:
                json.dump(data, fout, indent=4)
                print('done')
        else:
            print('Measurements failed')
    pm.close()
rf.close()
