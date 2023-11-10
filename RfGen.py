from Devices import Device, Lab
from quantiphy import Quantity
import time


class RfGen:
    def __init__(self, verbose=True):
        self.dev = Lab.connectByType(Device.Type.RF_GEN, verbose)
        self.verbose = verbose

    def setCW(self, state, f=None, p=None, warn=False):
        send = '*CLS; :STAT:QUES:POW:ENAB 32767; '
        send += ':STAT:QUES:ENAB 32767; :OUTP:MOD OFF; '
        if f is not None:
            send += ':FREQ:CW %s; ' % f
        else:
            f = Quantity(self.dev.query(':FREQ:CW?'), 'Hz')

        if p is not None:
            send += ':POWER %s; ' % p
        else:
            p = Quantity(self.dev.query(':POWER?'), 'dBm')

        out = 'ON' if state else 'OFF'
        send += ':OUTP %s; ' % out
        if self.verbose:
            print('Setting RF output to %s at %s with %s...' % (out, f, p),
                  end='', flush=True)
        self.dev.write(send)
        if self.verbose:
            print('done.')
        if warn:
            status = int(self.dev.query(':STAT:QUES:COND?'))
            if status & 16 != 0:
                print('Warning: owen cold')
            if status & 0x7fef != 0:
                print('Warning: unhandled status, %d (8 is summary)' % status)

            time.sleep(0.8)  # wait a while for unlevel warning to trigger
            status = int(self.dev.query(':STAT:QUES:POW:COND?'))
            if status & 2 != 0:
                print('Warning: unlevel, try lowering the output power')
            if status & 0x7ffd != 0:
                print('Warning: unhandled power status, %d' % status)
