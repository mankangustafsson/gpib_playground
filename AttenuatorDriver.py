from Devices import *

class AttenuatorDriver:
    def __init__(self, verbose = True):
        self.dev = Lab.connectByType(Device.Type.ATTENUATOR_DRIVER, verbose)
        self.verbose = verbose
        
    def __del__(self):
        self.dev.close()
 
    def preset(self):
        self.dev.write('PR')

    def setAttenuation(self, db):
        if db < 0 or db > 121:
            raise ValueError('Attenuation out of range: %u' %db)
        x = (db // 10) * 10
        if x == 120:
            x = 110
        y = db - x
        cmd = 'ATT:BANK1:X%d' % x
        cmd += ';ATT:BANK1:Y%d' % y
        self.dev.write(cmd)

    def getAttenuation(self):
        x = self.dev.query('ATT:BANK1:X?');
        y = self.dev.query('ATT:BANK1:Y?');
        return int(x.split(':')[1]) + int(y.split(':')[1])

    def __setRelay(self, op, relay):
        if relay not in [0, 9, 10]:
            raise ValueError('Invalid relay: %d' %relay)
        r = relay + 100
        if r == 100:
            r += 10
        self.dev.write(':ROUTe:%s (@%d)' %(op, r))

    def openRelay(self, relay):
        self.__setRelay('OPEn', relay)

    def closeRelay(self, relay):
        self.__setRelay('CLOSe', relay)

        
