from Devices import Device
from Lab import Lab

from quantiphy import Quantity
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
    for f in frequencies:
        rf_gen.write(f'S11; POWE -20.0; CWFREQ {f}')
        print(f'Setting {Quantity(f, 'Hz')} ', end='', flush=True)
        span = 250E06
        rbw = 1E06
        spec.write('CALC:MARK1:CPEAK OFF')
        spec.write(f':SENS:FREQ:CENTER {f:12.0f}Hz')
        spec.write(f':SENS:FREQ:SPAN {span:12.0f}Hz')
        spec.write(f':SENS:BWID:RES {rbw:12.0f}Hz')
        spec.query('*OPC?')
        time.sleep(0.2)
        spec.write('SENS:POW:RF:PCEN')
        spec.query('*OPC?')
        time.sleep(0.1)
        padj = Quantity(spec.query('SENS:POW:RF:PADJ?'), 'Hz')
        print(f'Padj {padj}')

    rf_gen.close()
    spec.close()
