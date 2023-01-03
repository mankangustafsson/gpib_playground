from enum import Enum, auto
import pyvisa
import time

class Device:
    class Type(Enum):
        COUNTER = auto(),
        POWER_METER = auto(),
        OSCILLOSCOPE = auto(),
        RF_GEN = auto(),
        VNA = auto(),
        SPECTRUM_ANALYZER = auto(),
        ATTENUATOR_DRIVER = auto()
        
    def __init__(self, address, name, deviceType,
                 idQuery = '*IDN?', term = None):
        self.address = address
        self.name = name
        self.deviceType = deviceType
        self.idQuery = idQuery
        self.term = term
            
    def connect(self, verbose = True):
        rm = pyvisa.ResourceManager()
        baudRate = None
        dev = None
        if self.address.startswith('ASRL'):
            dev = rm.open_resource(self.address, baud_rate = 115200)
        else:
            dev = rm.open_resource(self.address)
            
        dev.timeout = 5000
        if self.term is not None:
            dev.read_termination = self.term
            dev.write_termination = self.term
        if verbose:
            print('Connecting to ' + self.address + '...',
                  end ='', flush = True)
        name = dev.query(self.idQuery)
        while not self.name in name:
            time.sleep(0.1)
            name = dev.query(self.idQuery)
        if verbose: print('connected to ' + name)
        return dev

class Lab:    

    devices = [Device('GPIB1::11::INSTR', '53131A',
                      Device.Type.COUNTER, '*IDN?', '\n'),
               Device('GPIB0::7::INSTR', '54820A',
                      Device.Type.OSCILLOSCOPE, term = '\n'),
               Device('GPIB0::13::INSTR', 'HP438A',
                      Device.Type.POWER_METER, '?ID', '\r\n'),
               Device('GPIB0::16::INSTR', '8753',
                      Device.Type.VNA),
               Device('GPIB0::19::INSTR', 'E44',
                      Device.Type.RF_GEN, term = '\n'),
               Device('ASRL51::INSTR', 'HP11713',
                      Device.Type.ATTENUATOR_DRIVER, term = '\n'),
               Device('USB0::0xF4EC::0x1300::SSA3XLBC3R0195::INSTR', 'SSA3032',
                      Device.Type.SPECTRUM_ANALYZER, term = '\n')]
    
    @staticmethod
    def connectByType(deviceType, verbose = True):
        for d in Lab.devices:
            if d.deviceType == deviceType:
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
                print('Unknown device on GPIB bus: %s' %address)
        if n == 0:
            print('No known devices found')
