import pyvisa
import struct

def double_to_hex(f):
    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])
    
rm = pyvisa.ResourceManager()
#print(rm.list_resources())
dev = rm.open_resource('USB0::0x03EB::0x2065::Hewlett-Packard__ASG-A3000A__AA00000000__B.03.86::INSTR')
dev.read_termination = '\n'
dev.write_termination = '\n'
dev.query(':SYST:PRES; *OPC?;')
h = 0x43C0
for idx in range(0, 39):
    freq = float(dev.query(f':SERV:PROD:CAL? 165,{idx}'))
    print(f'Index: {idx:2} Double: {freq:15} Hex: {double_to_hex(freq):018} EEPROM: {hex(h)}')
    h += 8
dev.close()
