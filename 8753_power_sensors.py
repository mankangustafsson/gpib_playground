from Devices import Device
from Lab import Lab

from quantiphy import Quantity

dev = Lab.connectByType(Device.Type.VNA, hint="8753")

for p in [Lab.probes[0], Lab.probes[1]]:
    sensor = "A" if p.name == "8482A" else "B"
    print("Adding probe %s as sensor %s" % (p.name, sensor))
    cmd = "CALFSEN%s CLEL" % sensor
    #    print(cmd)
    dev.write(cmd)
    entries = 0
    for f, cf in p.cf_table.items():
        if f <= 6.0e9:
            cmd = "SADD CALFFREQ %s CALFCALF %.1f" % (str(Quantity(f, "Hz")), cf)
            # print(cmd)
            s = dev.write(cmd)
            entries += 1
    dev.write("EDITDONE")
    print("Added %u entries" % entries)
dev.write("EMIB; SOFR")
dev.close()
