from Devices import Device
from Lab import Lab

from quantiphy import Quantity
import numpy
import time

if __name__ == "__main__":
    spec = Lab.connectByType(Device.Type.SPECTRUM_ANALYZER, hint='E4407',
                             verbose=True)
    rf_gen = Lab.connectByType(Device.Type.VNA, hint='8722', verbose=True)
    if spec is None or rf_gen is None:
        exit(1)
    freq_base = [3.2E9, 26.4E9]
    for f in range(4, 27):
        freq_base.append(f * 1E9)
    frequencies = sorted(freq_base)

    poly = []
    for a in range(0, 4):
        a = float(spec.query(f'DIAG:CAL? 132,{a}'))
        poly.append(a)
    print(f'Current polynom coefficients: {poly}')
    print('Current preselector table')
    print('HZ; DAC value')
    print('=============')
    for f in frequencies:
        dac = int(poly[0] + f * poly[1] + f ** 2 * poly[2] + f ** 3 * poly[3])
        print(f'{f:12.0f}; {dac:5}')
    print('=============\n')

    adjusted_frequencies = []
    for f in frequencies:
        rf_gen.write(f'S11; POWE -20.0; CWFREQ {f}')
        print(f'Setting {Quantity(f, 'Hz')} ', end='', flush=True)
        span = 250E06
        rbw = 1E06
        spec.write(':CALC:MARKER1:MAX')
        spec.write(':CALC:MARKER1:CPEAK:STATE ON')
        spec.write(':CALC:MARKER1:FCOUNT:STATE ON')
        spec.query('*OPC?')
        time.sleep(0.1)
        spec.write('CALC:MARK1:CPEAK OFF')
        spec.write(f':SENS:FREQ:CENTER {f:12.0f}Hz')
        spec.write(f':SENS:FREQ:SPAN {span:12.0f}Hz')
        spec.write(f':SENS:BWID:RES {rbw:12.0f}Hz')
        spec.query('*OPC?')
        time.sleep(0.1)
        spec.write('SENS:POW:RF:PCEN')
        spec.query('*OPC?')
        time.sleep(0.1)
        padj = float(spec.query('SENS:POW:RF:PADJ?'))
        print(f'Padj {Quantity(padj, 'Hz')}')
        adjusted_frequencies.append(f + padj)
    rf_gen.close()
    print('\nAdjusted preselector table')
    print('HZ; DAC value')
    print('=============')
    new_dac = []
    for f in adjusted_frequencies:
        dac = int(poly[0] + f * poly[1] + f ** 2 * poly[2] + f ** 3 * poly[3])
        new_dac.append(dac)
        print(f'{f:12.0f}; {dac:5}')
    print('=============\n')

    new_poly = numpy.polyfit(frequencies, new_dac, deg=3).tolist()
    new_poly.reverse()
    print(f'New polynom coefficients: {new_poly}')
    print('New preselector table')
    print('HZ; DAC value')
    print('=============')
    for f in frequencies:
        dac = int(new_poly[0] + f * new_poly[1] + f ** 2 * new_poly[2]
                  + f ** 3 * new_poly[3])
        print(f'{f:12.0f}; {dac:5}')
    print('=============\n')

    print('Writing new polynom to RAM...')
    for a in range(0, 4):
        cmd = f'DIAG:CAL 132,{a},{new_poly[a]}'
        print(cmd)
        spec.write(cmd)
    print('done')
    # print('Writing new polynom to EEPROM...', end='', flush=True)
    # cmd = 'DIAG:CAL:STORE 132'
    # print(cmd)
    # spec.write(cmd)
    # print('done')
    spec.close()
