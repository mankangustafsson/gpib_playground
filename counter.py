from Devices import Device
from Lab import Lab

from quantiphy import Quantity
import time

dev = Lab.connectByType(Device.Type.COUNTER)
dev.write('*RST')
dev.write('*CLS')
dev.write('*SRE 0')
dev.write('*ESE 0')
dev.write(':STAT:PRES')
dev.write('FUNC \'FREQ 3\'')
dev.write(':FREQ:ARM:STAR:SOUR IMM')
dev.write(':FREQ:ARM:STOP:SOUR TIM')
dev.write(':FREQ:ARM:STOP:TIM 1.0')
f = Quantity(float(dev.query(':READ:FREQ?')[1:]), 'Hz')
print('{:3.14q}'.format(f))
