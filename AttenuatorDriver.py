from Devices import Device
from Lab import Lab


class AttenuatorDriver:
    def __init__(self, verbose=True):
        self.dev = Lab.connectByType(Device.Type.ATTENUATOR_DRIVER, verbose)
        self.verbose = verbose

    def preset(self):
        self.dev.write("PR")

    def setAttenuation(self, db):
        if db < 0 or db > 121:
            raise ValueError("Attenuation out of range: %u" % db)
        x = (db // 10) * 10
        if x == 120:
            x = 110
        y = db - x
        self.dev.write(f"ATT:BANK1:X{x};ATT:BANK1:Y{y}")

    def getAttenuation(self):
        x = self.dev.query("ATT:BANK1:X?")
        y = self.dev.query("ATT:BANK1:Y?")
        return int(x.split(":")[1]) + int(y.split(":")[1])

    def __setRelay(self, op, relay):
        if relay not in [0, 9, 10]:
            raise ValueError(f"Invalid relay: {relay}")
        if relay == 0:
            relay = 10
        r = relay + 100
        self.dev.write(f":ROUTe:{op} (@{r})")

    def openRelay(self, relay):
        self.__setRelay("OPEn", relay)

    def closeRelay(self, relay):
        self.__setRelay("CLOSe", relay)
