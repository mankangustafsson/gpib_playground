from Devices import Device
from Lab import Lab
from RfGen import RfGen

from quantiphy import Quantity
from time import time

if __name__ == "__main__":
    try:
        rf = RfGen(verbose=False)
        pm = Lab.connectByType(Device.Type.POWER_METER, verbose=False)
        if rf is None or pm is None:
            exit(1)
        probe = Lab.probes[0]  # HP8481A, sensor A

        for p in range(-30, 20):
            if p % 10 == 0 or p % 3 == 0:
                power = Quantity(p, "dBm")
                print("Results at %s; Probe %s" % (power, probe.name))
                for f in range(2000000000, 4100000000, 100000000):
                    rf.setCW(True, f, p)
                    time.sleep(0.2)
                    freq = Quantity(f, "Hz")
                    cf = probe.get_cf(freq)
                    pmCommand = "AE KB%.1fEN LG RL0 AP TR2 TR3" % cf
                    # print(pmCommand)
                    reply = pm.query_ascii_values(pmCommand)
                    print("{:7q};{:3.2f}".format(freq, reply[0]))
    except:
        pass
    finally:
        try:
            rf.setCW(False)
            pm.close()
        except:
            pass
