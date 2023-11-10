from Devices import Device
from Lab import Lab

import time

dev = Lab.connectByType(Device.Type.VNA)

print('Presetting the analyzer...please wait')
dev.write('OPC?;PRES;')
time.sleep(1)

dev.write('TEST53;')
dev.write('EXET;')
time.sleep(1)

dev.write('TESR2;')
print('Clearing all registers...please wait')
time.sleep(6)

input('Connect the Open to the REFL Port, then press Enter to continue.')
print('Measuring open')
dev.write('CLASS11A;OPC?;STANB;')
dev.write('OPC?;DONE')

input('Connect the Short to the REFL Port, then press Enter.')
print('Measuring short')
dev.write('CLASS11B;OPC?;STANB;')
dev.write('OPC?;DONE')

input('Connect the Load to the REFL Port, then press Enter.')
print('Measuring load')
dev.write('OPC?;CLASS11C;')
dev.write('OPC?;DONE;')
print('Computing reflection cal coefficients')
time.sleep(6)
dev.write('OPC?;SAV1;')
time.sleep(5)

input('Connect the Thru from the REFL Port to the TRANS Port, then press Enter.')
print('Measuring thru')
dev.write('OPC?;STANE;')
print('Computing transmission cal coefficients')
dev.write('OPC?;DONE;')
print('Done')

dev.close()
