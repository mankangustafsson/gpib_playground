import pyvisa

if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())
    n = 0
    for r in rm.list_resources(query='(GPIB|USB)(0|1|2)::?*::INSTR'):
        if r not in ['GPIB0::17::INSTR', 'GPIB1::17::INSTR',
                     'GPIB1::3::1::INSTR',
                     'GPIB1::3::2::INSTR',
                     'GPIB1::3::3::INSTR',
                     'GPIB1::3::4::INSTR',
                     'GPIB1::3::5::INSTR',
                     'GPIB1::3::6::INSTR',
                     'GPIB1::3::7::INSTR',
                     'GPIB1::3::8::INSTR',
                     'GPIB1::3::9::INSTR',
                     'GPIB1::3::10::INSTR',
                     'GPIB1::3::11::INSTR',
                     'GPIB1::3::12::INSTR',
                     'GPIB1::3::13::INSTR',
                     'GPIB1::3::14::INSTR',
                     'GPIB1::3::15::INSTR',
                     'GPIB1::3::16::INSTR',
                     'GPIB1::3::17::INSTR',
                     'GPIB1::3::18::INSTR',
                     'GPIB1::3::19::INSTR',
                     'GPIB1::3::20::INSTR',
                     'GPIB1::3::21::INSTR',
                     'GPIB1::3::22::INSTR',
                     'GPIB1::3::23::INSTR',
                     'GPIB1::3::24::INSTR',
                     'GPIB1::3::25::INSTR',
                     'GPIB1::3::26::INSTR',
                     'GPIB1::3::27::INSTR',
                     'GPIB1::3::28::INSTR',
                     'GPIB1::3::29::INSTR',
                     'GPIB1::3::30::INSTR']:
            dev = rm.open_resource(r)
            dev.timeout = 1000
            dev.read_termination = '\r\n'
            dev.write_termination = '\r\n'
            try:
                print('Connecting to ' + r + '...', end='', flush=True)
                s = dev.query('ID')
                try:
                    float(s)
                    s = dev.query('?ID')
                except ValueError:
                    pass
            except:
                dev.read_termination = '\n'
                dev.write_termination = '\n'
                s = dev.query('*IDN?')
            finally:
                print('connected to ' + s)
                n += 1
                dev.close()
                rm.close()
                if n == 0:
                    print('No devices available on bus (GPIB|USB)(0|1)')
