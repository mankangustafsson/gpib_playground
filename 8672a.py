import pyvisa
import time

rm = pyvisa.ResourceManager()
print(rm.list_resources())

dev = rm.open_resource('GPIB0::5::INSTR')  # Change this to one printed above

# experiment with these if instrument reports errors on commands
# dev.read_termination = '\r\n'  # or '\n'
# dev.write_termination = '\r\n' # or '\n'

# Not sure 8672A answers to ID commands
# which can be a problem for the USB adapter as well see
# https://github.com/xyphro/UsbGpib Setting Parameters section
# s = dev.query('ID') # Other strings to try '?ID' and '*IDN?'
# print('connected to ' + s)
# time.sleep(0.2)

print('Setting frequency')
dev.write('P12345678Z1')  # Frequency to 12345.678MHz
time.sleep(0.2)

print('Setting power')
dev.write('K1L7')         # Power level to -14dBm
time.sleep(0.2)

print('Setting modulation')
dev.write('M0N6')         # AM off, FM off
time.sleep(0.2)

print('Setting output')
dev.write('01')           # Output on, internal ALC
time.sleep(2)

print('RF off')
dev.write('O0')
time.sleep(2)

print('Setting everything at once')
dev.write('P1036800Z1K0L3M0N6O1')  # 10.368GHz, 0 dBm, no modulation

dev.close()
rm.close()
