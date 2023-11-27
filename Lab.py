from Devices import Device
import pyvisa


class Lab:
    devices = [Device('GPIB1::11::INSTR', '53131A',
                      Device.Type.COUNTER, '*IDN?', '\n'),
               Device('GPIB0::7::INSTR', '54820A',
                      Device.Type.OSCILLOSCOPE, term='\n'),
               Device('GPIB0::13::INSTR', 'HP438A',
                      Device.Type.POWER_METER, '?ID', '\r\n'),
               Device('GPIB0::5::INSTR', 'E3631',
                      Device.Type.PSU),
               Device('GPIB0::16::INSTR', '8753',
                      Device.Type.VNA),
               Device('GPIB1::16::INSTR', '8722',
                      Device.Type.VNA),
               Device('GPIB0::19::INSTR', 'E44',
                      Device.Type.RF_GEN, term='\n'),
               Device('GPIB1::28::INSTR', 'SMP02',
                      Device.Type.RF_GEN),
               Device('ASRL1::INSTR', 'HP11713',
                      Device.Type.ATTENUATOR_DRIVER, term='\n'),
               Device('USB0::0xF4EC::0x1300::SSA3XLBC3R0195::INSTR', 'SSA3032',
                      Device.Type.SPECTRUM_ANALYZER, term='\n'),
               Device('GPIB1::18::INSTR', 'E4407',
                      Device.Type.SPECTRUM_ANALYZER)]

    @staticmethod
    def connectByType(deviceType, verbose=True, hint=None):
        for d in Lab.devices:
            if d.deviceType == deviceType:
                if hint is None or hint == d.name:
                    return d.connect(verbose)
        return None

    @staticmethod
    def isKnownDevice(address):
        for d in Lab.devices:
            if address == d.address:
                return d
        return None

    @staticmethod
    def scanDevices():
        rm = pyvisa.ResourceManager()
        devs = rm.list_resources()
        n = 0
        for address in devs:
            ld = Lab.isKnownDevice(address)
            if ld is not None:
                dev = ld.connect()
                dev.close()
                n += 1
            elif address not in ['GPIB0::17::INSTR',
                                 'GPIB1::17::INSTR',
                                 'ASRL1::INSTR', 'ASRL2::INSTR',
                                 'ASRL3::INSTR', 'ASRL4::INSTR',
                                 'GPIB1::3::1::INSTR',
                                 'GPIB1::3::2::INSTR',
                                 'GPIB1::3::3::INSTR',
                                 'GPIB1::3::4::INSTR',
                                 'GPIB1::3::5::INSTR',
                                 'GPIB1::3::6::INSTR',
                                 'GPIB1::3::7::INSTR',
                                 'GPIB1::3::8::INSTR',
                                 'GPIB1::3::9::INSTR',
                                 'GPIB1::3::10::INSTR',
                                 'GPIB1::3::11::INSTR',
                                 'GPIB1::3::12::INSTR',
                                 'GPIB1::3::13::INSTR',
                                 'GPIB1::3::14::INSTR',
                                 'GPIB1::3::15::INSTR',
                                 'GPIB1::3::16::INSTR',
                                 'GPIB1::3::17::INSTR',
                                 'GPIB1::3::18::INSTR',
                                 'GPIB1::3::19::INSTR',
                                 'GPIB1::3::20::INSTR',
                                 'GPIB1::3::21::INSTR',
                                 'GPIB1::3::22::INSTR',
                                 'GPIB1::3::23::INSTR',
                                 'GPIB1::3::24::INSTR',
                                 'GPIB1::3::25::INSTR',
                                 'GPIB1::3::26::INSTR',
                                 'GPIB1::3::27::INSTR',
                                 'GPIB1::3::28::INSTR',
                                 'GPIB1::3::29::INSTR',
                                 'GPIB1::3::30::INSTR']:
                print(f'Unknown device on GPIB bus: {address}')
        if n == 0:
            print('No known devices found')


if __name__ == "__main__":
    Lab.scanDevices()
