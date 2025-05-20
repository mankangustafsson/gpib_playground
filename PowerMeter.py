from Devices import Device
from Lab import Lab

from quantiphy import Quantity
import time


class PowerMeter:
    def __init__(self, verbose=True):
        self.dev = Lab.connectByType(Device.Type.POWER_METER, verbose)
        self.verbose = verbose

    @staticmethod
    def _checkSensor(sensor):
        if sensor != "A" and sensor != "B":
            raise ValueError("Invalid sensor")

    @staticmethod
    def _checkProbe(probe):
        if probe < 0 or probe >= len(Lab.probes):
            raise ValueError("Invalid probe")

    def preset(self):
        self.dev.write("PR")

    def test_port(self, enable=True):
        self.dev.write("OC1" if enable else "OC0")

    def zero(self, sensorPort, probe):
        sensor = sensorPort.upper()
        self._checkSensor(sensor)
        self._checkProbe(probe)
        if self.verbose:
            print(
                "Zeroing and cal adjust of probe %u (%s) at sensor "
                "port %s..." % (probe, Lab.probes[probe].name, sensor),
                end="",
                flush=True,
            )
        ref_cf = Lab.probes[probe].ref_cf
        send = "DE %sE ZE CL%.1fEN KB%.1fEN OC1 LG %sP TR2 TR3" % (
            sensor,
            ref_cf,
            ref_cf,
            sensor,
        )
        self.dev.timeout = 20000
        dbm = self.dev.query_ascii_values(send)
        self.dev.timeout = 5000
        while dbm[0] != Lab.probes[probe].cal_read:
            time.sleep(0.100)
            dbm = self.dev.query_ascii_values("TR2")
        self.dev.write("TR3 OC0")
        if self.verbose:
            print(
                "Probe %u at sensor port %s "
                "calibrated %.2f" % (probe, sensor, dbm[0]) + " dBm"
            )

    def _doRead(self, command, sensorOp, unit):
        if self.verbose:
            print("%s reads: " % sensorOp, end="", flush=True)
        command += "TR2 TR3"
        power = self.dev.query_ascii_values(command)
        if unit == "dBm":
            value = "%.2f dBm" % power[0]
        else:
            value = str(Quantity(power[0], "%" if "/" in sensorOp else "W"))
        print(value, end="", flush=True)
        return value

    def read(
        self,
        sensorList,
        probesList,
        frequencyList,
        offsetList=[0, 0],
        operation=None,
        unit="dBm",
    ):
        if len(sensorList) > 2 or len(sensorList) == 0:
            raise ValueError("Invalid number of sensor ports")
        if len(probesList) > 2 or len(probesList) == 0:
            raise ValueError("Invalid number of sensor ports")
        if len(sensorList) != len(probesList):
            raise ValueError("Unmatched number of sensor ports and probes")
        if len(frequencyList) > 2:
            raise ValueError("More than two frequencies supplied")
        if len(offsetList) > 2:
            raise ValueError("More than two offsets supplied")
        for s in sensorList:
            self._checkSensor(s)
        for p in probesList:
            self._checkProbe(p)
        if len(offsetList) == 1:
            # if only one offset is supplied, use same for both sensor ports
            offsetList.append(offsetList[0])
        send = ""
        # Set cal factors
        if len(frequencyList) > 0:
            for n in range(0, len(sensorList)):
                fi = n
                if len(sensorList) > len(frequencyList):
                    fi -= 1
                cf = Lab.probes[probesList[n]].get_cf(frequencyList[fi])
                if self.verbose:
                    print(
                        "Set cal factor %.1f for probe %u in sensor %s at "
                        "frequency %s"
                        % (
                            cf,
                            probesList[n],
                            sensorList[n],
                            str(Quantity(frequencyList[fi], "Hz")),
                        )
                    )

                send += "%sE KB%.1fEN " % (sensorList[n], cf)
        send += "AP OS%.2fEN " % offsetList[0]
        send += "BP OS%.2fEN " % offsetList[1]
        # Unit
        if unit == "dBm":
            send += "LG "
        else:
            send += "LN "
        # Always absolute
        send += "RL0 "
        # Operation
        if operation == "A-B":
            send += "AD "
        elif operation == "B-A":
            send += "BD "
        elif operation == "A/B":
            send += "AR "
        elif operation == "B/A":
            send += "BR "
        elif operation is not None:
            raise ValueError("Invalid read operation: %s" % operation)
        else:
            # Read each sensor
            for s in sensorList:
                send += "%sP " % s
                self._doRead(send, s, unit)
        if operation is not None:
            self._doRead(send, operation, unit)
