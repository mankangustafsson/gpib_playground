import pyvisa
from datetime import datetime

rm = pyvisa.ResourceManager()
print(rm.list_resources())

#dev = rm.open_resource('USB0::0x03EB::0x2065::Hewlett-Packard__E4407B__MY41440643__A.14.06::INSTR')
dev = rm.open_resource('GPIB1::18::INSTR')
dev.timeout = 8000

#dev.read_termination = '\n' 
#dev.write_termination = '\n'

s = dev.query('*IDN?')
print('connected to ' + s)

dev.write(":MMEM:DEL 'R:SCREEN.GIF';*CLS")
for i in range(1):
    dev.write(":MMEM:STOR:SCR 'R:SCREEN.GIF'")
    data = dev.query_binary_values(":MMEM:DATA? 'R:SCREEN.GIF'",
                                   is_big_endian=True, datatype='c')
    filename = datetime.now().strftime('%Y-%m-%d_%H%M%S_') + str(i) + '-SCREEN.GIF'
    try:
        with open(filename, "wb") as im:
            im.write(b''.join(data))
            im.close()
    except OSError:
        print('failed to save file, %s' %filename)
    print(filename)
    dev.write(":MMEM:DEL 'R:SCREEN.GIF'")
dev.close()
rm.close()
