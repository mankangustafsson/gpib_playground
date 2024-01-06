from Devices import Device
from Lab import Lab

from datetime import datetime


if __name__ == '__main__':
    dev = Lab.connectByType(Device.Type.SPECTRUM_ANALYZER, hint='E4407',
                            verbose=True)
    if dev is None:
        exit(1)

    menu_on = dev.query(':DISP:MENU:STAT?').strip() == '1'
    if menu_on:
        dev.write(':DISP:MENU:STAT 0')

    dev.write(':DISP:WIND:ANN:ALL 1')
    dev.write(":DISP:ANN:TITL:DATA 'GPIB Playground by Mankan Gustafsson'")

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
            print(f'failed to save file: {filename}')
        print(filename)
        dev.write(":MMEM:DEL 'R:SCREEN.GIF'")

    if menu_on:
        dev.write(':DISP:MENU:STAT 1')
    dev.close()
