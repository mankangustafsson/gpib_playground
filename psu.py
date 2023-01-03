import pyvisa
import sys

rm = pyvisa.ResourceManager()
dev = rm.open_resource('GPIB0::5::INSTR')
s = dev.query('*IDN?')
print('connected to ' + s)
dev.write('APPLY P6V, 4.5,0.2');
dev.write('APPLY P25V,10,0.3');
dev.write('OUTPUT:STATE ON');
dev.write('OUTPUT:TRACK:STATE ON');

dev.close()
rm.close()
