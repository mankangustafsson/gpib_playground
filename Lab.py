from CalKit import CalKit, Standard
from Devices import Device
from Probe import Probe

import pyvisa


class Lab:
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
            elif address not in [
                "GPIB0::17::INSTR",
                "GPIB1::17::INSTR",
                "ASRL1::INSTR",
                "ASRL2::INSTR",
                "ASRL3::INSTR",
                "ASRL4::INSTR",
                "GPIB1::3::1::INSTR",
                "GPIB1::3::2::INSTR",
                "GPIB1::3::3::INSTR",
                "GPIB1::3::4::INSTR",
                "GPIB1::3::5::INSTR",
                "GPIB1::3::6::INSTR",
                "GPIB1::3::7::INSTR",
                "GPIB1::3::8::INSTR",
                "GPIB1::3::9::INSTR",
                "GPIB1::3::10::INSTR",
                "GPIB1::3::11::INSTR",
                "GPIB1::3::12::INSTR",
                "GPIB1::3::13::INSTR",
                "GPIB1::3::14::INSTR",
                "GPIB1::3::15::INSTR",
                "GPIB1::3::16::INSTR",
                "GPIB1::3::17::INSTR",
                "GPIB1::3::18::INSTR",
                "GPIB1::3::19::INSTR",
                "GPIB1::3::20::INSTR",
                "GPIB1::3::21::INSTR",
                "GPIB1::3::22::INSTR",
                "GPIB1::3::23::INSTR",
                "GPIB1::3::24::INSTR",
                "GPIB1::3::25::INSTR",
                "GPIB1::3::26::INSTR",
                "GPIB1::3::27::INSTR",
                "GPIB1::3::28::INSTR",
                "GPIB1::3::29::INSTR",
                "GPIB1::3::30::INSTR",
            ]:
                print(f"Unknown device on GPIB bus: {address}")
        if n == 0:
            print("No known devices found")

    @staticmethod
    def printKits():
        for ck in Lab.calkits:
            ck.print_kit()
            if not ck.verify():
                print("Calkit {ck} has duplicate standards!")

    @staticmethod
    def printProbes():
        n = 0
        for p in Lab.probes:
            print(f"Probe {n}: {p}")
            p.print_cal_table()
            n += 1

    devices = [
        Device("GPIB1::11::INSTR", "53131A", Device.Type.COUNTER, "*IDN?", "\n"),
        Device("GPIB0::7::INSTR", "54820A", Device.Type.OSCILLOSCOPE, term="\n"),
        Device("GPIB0::13::INSTR", "HP438A", Device.Type.POWER_METER, "?ID", "\r\n"),
        Device("GPIB0::5::INSTR", "E3631", Device.Type.PSU),
        Device("GPIB0::16::INSTR", "8753", Device.Type.VNA),
        Device("GPIB1::16::INSTR", "8722", Device.Type.VNA),
        Device("GPIB0::19::INSTR", "E44", Device.Type.RF_GEN, term="\n"),
        Device("GPIB1::28::INSTR", "SMP02", Device.Type.RF_GEN),
        Device("ASRL4::INSTR", "HP11713", Device.Type.ATTENUATOR_DRIVER, term="\n"),
        Device(
            "USB0::0xF4EC::0x1300::SSA3XLBC3R0195::INSTR",
            "SSA3032",
            Device.Type.SPECTRUM_ANALYZER,
            term="\n",
        ),
        Device("GPIB1::18::INSTR", "E4407", Device.Type.SPECTRUM_ANALYZER),
    ]

    calkits = [
        CalKit(
            name="Rosenberger",
            short_name="SMA",
            max_freq="6E+9",
            standards=[
                Standard(
                    Standard.Type.SHORT,
                    Standard.Sex.MALE,
                    [
                        "DEFS 1",
                        "STDTSHOR",
                        "OFSZ 50",
                        "OFSD 26.296763E-12",
                        "OFSL 0.0E+9",
                        "C0 1.972678",
                        "C1 6613.309399",
                        "C2 -1625.587777",
                        "C3 94.519818",
                    ],
                ),
                Standard(
                    Standard.Type.OPEN,
                    Standard.Sex.MALE,
                    [
                        "DEFS 2",
                        "STDTOPEN",
                        "OFSZ 50",
                        "OFSD 43.059930E-12",
                        "OFSL 1.818363E+9",
                        "C0 -14.992043",
                        "C1 -1009.382660",
                        "C2 1377.725656",
                        "C3 -138.223997",
                    ],
                ),
                Standard(
                    Standard.Type.LOAD,
                    Standard.Sex.MALE,
                    [
                        "DEFS 3",
                        'LABS "LOAD"',
                        "STDTLOAD",
                        "OFSZ 52.383099",
                        "OFSD 17.961624E-12",
                    ],
                ),
                Standard(
                    Standard.Type.LOAD,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 3",
                        'LABS "LOAD"',
                        "STDTLOAD",
                        "OFSZ 50.589652",
                        "OFSD 29.614480E-12",
                    ],
                ),
                Standard(
                    Standard.Type.THRU,
                    Standard.Sex.MALE,
                    ["DEFS 4", "STDTDELA", "OFSZ 50.747533", "OFSD 42.264620E-12"],
                ),
                Standard(
                    Standard.Type.THRU,
                    Standard.Sex.FEMALE,
                    ["DEFS 4", "STDTDELA", "OFSZ 50", "OFSD 76.991933E-12"],
                ),
                Standard(
                    Standard.Type.SHORT,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 7",
                        "STDTSHOR",
                        "OFSZ 50",
                        "OFSD 0.0E-12",
                        "OFSL 962.266512E+9",
                        "C0 28.454226",
                        "C1 2380.746494",
                        "C2 -3135.518359",
                        "C3 358.471292",
                    ],
                ),
                Standard(
                    Standard.Type.OPEN,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 8",
                        "STDTOPEN",
                        "OFSZ 50",
                        "OFSD 0.0E-12",
                        "OFSL 0.0E+9",
                        "C0 0",
                        "C1 0",
                        "C2 0",
                        "C3 0",
                    ],
                ),
            ],
        ),
        CalKit(
            name="R&S, HP, Pasternack",
            short_name="3.5mm",
            max_freq="40E+9",
            standards=[
                Standard(
                    Standard.Type.SHORT,
                    Standard.Sex.MALE,
                    [
                        "DEFS 1",
                        "STDTSHOR",
                        "OFSZ 50",
                        "OFSD 30.52E-12",
                        "OFSL 0.0E+9",
                        "C0 14",
                        "C1 -80",
                        "C2 3",
                        "C3 -0.02",
                    ],
                    "ZV-Z132",
                ),
                Standard(
                    Standard.Type.OPEN,
                    Standard.Sex.MALE,
                    [
                        "DEFS 2",
                        "STDTOPEN",
                        "OFSZ 50",
                        "OFSD 28.385E-12",
                        "OFSL 0.0E+9",
                        "C0 50",
                        "C1 150",
                        "C2 -8",
                        "C3 0.36",
                    ],
                    "ZV-Z132",
                ),
                Standard(
                    Standard.Type.LOAD,
                    Standard.Sex.MALE,
                    [
                        "DEFS 3",
                        'LABS "LOAD"',
                        "STDTLOAD",
                        "OFSZ 50.0",
                        "OFSD 0.0E-12",
                        "OFSL 0.0E+9",
                    ],
                    "ZV-Z132",
                ),
                Standard(
                    Standard.Type.LOAD,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 3",
                        'LABS "LOAD"',
                        "STDTLOAD",
                        "OFSZ 50.477326",
                        "OFSD 41.152171E-12",
                        "OFSL 4.235188E+9",
                    ],
                    "PE5510",
                ),
                Standard(
                    Standard.Type.THRU,
                    Standard.Sex.MALE,
                    ["DEFS 4", "STDTDELA", "OFSZ 50", "OFSD 127.1E-12", "OFSL 0.0E+9"],
                    "ZV-Z132",
                ),
                Standard(
                    Standard.Type.THRU,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 4",
                        "STDTDELA",
                        "OFSZ 50.082562",
                        "OFSD 92.998892E-12",
                        "OFSL 1.249549E+9",
                    ],
                    "HP",
                ),
                Standard(
                    Standard.Type.SHORT,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 7",
                        "STDTSHOR",
                        "OFSZ 49.353623",
                        "OFSD 32.835135E-12",
                        "OFSL 4.713050E+9",
                        "C0 -327.739423",
                        "C1 -634.415666",
                        "C2 -259.364278",
                        "C3 -1,908106",
                    ],
                    "PE5510",
                ),
                Standard(
                    Standard.Type.OPEN,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 8",
                        "STDTOPEN",
                        "OFSZ 49.514479",
                        "OFSD 26.736348E-12",
                        "OFSL 0.0E+9",
                        "C0 -9.957332",
                        "C1 -19.815771",
                        "C2 50.499163",
                        "C3 -1.831400",
                    ],
                    "PE5510",
                ),
            ],
        ),
        CalKit(
            name="R&S, HP, Pasternack",
            short_name="3.5mm 6",
            max_freq="6E+9",
            standards=[
                Standard(
                    Standard.Type.SHORT,
                    Standard.Sex.MALE,
                    [
                        "DEFS 1",
                        "STDTSHOR",
                        "OFSZ 50",
                        "OFSD 30.52E-12",
                        "OFSL 0.0E+9",
                        "C0 14",
                        "C1 -80",
                        "C2 3",
                        "C3 -0.02",
                    ],
                    "ZV-Z132",
                ),
                Standard(
                    Standard.Type.OPEN,
                    Standard.Sex.MALE,
                    [
                        "DEFS 2",
                        "STDTOPEN",
                        "OFSZ 50",
                        "OFSD 28.385E-12",
                        "OFSL 0.0E+9",
                        "C0 50",
                        "C1 150",
                        "C2 -8",
                        "C3 0.36",
                    ],
                    "ZV-Z132",
                ),
                Standard(
                    Standard.Type.LOAD,
                    Standard.Sex.MALE,
                    [
                        "DEFS 3",
                        'LABS "LOAD"',
                        "STDTLOAD",
                        "OFSZ 50.0",
                        "OFSD 0.0E-12",
                        "OFSL 0.0E+9",
                    ],
                    "ZV-Z132",
                ),
                Standard(
                    Standard.Type.LOAD,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 3",
                        'LABS "LOAD"',
                        "STDTLOAD",
                        "OFSZ 50.000000",
                        "OFSD 35.989092E-12",
                        "OFSL 7.695883E+9",
                    ],
                    "PE5510",
                ),
                Standard(
                    Standard.Type.THRU,
                    Standard.Sex.MALE,
                    ["DEFS 4", "STDTDELA", "OFSZ 50", "OFSD 127.1E-12", "OFSL 0.0E+9"],
                    "ZV-Z132",
                ),
                Standard(
                    Standard.Type.THRU,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 4",
                        "STDTDELA",
                        "OFSZ 50.000000",
                        "OFSD 92.908705E-12",
                        "OFSL 2.543030E+9",
                    ],
                    "HP",
                ),
                Standard(
                    Standard.Type.SHORT,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 7",
                        "STDTSHOR",
                        "OFSZ 50.000000",
                        "OFSD 38.314812E-12",
                        "OFSL 2.266649E+9",
                        "C0 -618.525397",
                        "C1 1033.062788",
                        "C2 -1489.310519",
                        "C3 7.283440",
                    ],
                    "PE5510",
                ),
                Standard(
                    Standard.Type.OPEN,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 8",
                        "STDTOPEN",
                        "OFSZ 50.000000",
                        "OFSD 28.716084E-12",
                        "OFSL 0.186614E+9",
                        "C0 -43.253770",
                        "C1 -593.519371",
                        "C2 39.854642",
                        "C3 -4.119794",
                    ],
                    "PE5510",
                ),
            ],
        ),
        CalKit(
            name="Rosenberger",
            short_name="SMAnew",
            max_freq="6E+9",
            standards=[
                Standard(
                    Standard.Type.SHORT,
                    Standard.Sex.MALE,
                    [
                        "DEFS 1",
                        "STDTSHOR",
                        "OFSZ 50",
                        "OFSD 0.0E-12",
                        "OFSL 1366.139379E+9",
                        "C0 -1.179818",
                        "C1 8382.440303",
                        "C2 -3415.291042",
                        "C3 379.941071",
                    ],
                ),
                Standard(
                    Standard.Type.OPEN,
                    Standard.Sex.MALE,
                    [
                        "DEFS 2",
                        "STDTOPEN",
                        "OFSZ 50",
                        "OFSD 82.529419E-12",
                        "OFSL 0.647714E+9",
                        "C0 12.950503",
                        "C1 19001.215672",
                        "C2 -8911.731027",
                        "C3 895.117913",
                    ],
                ),
                Standard(
                    Standard.Type.LOAD,
                    Standard.Sex.MALE,
                    ["DEFS 3", 'LABS "LOAD"', "STDTLOAD", "OFSZ 50.0", "OFSD 0.0E-12"],
                ),
                Standard(
                    Standard.Type.LOAD,
                    Standard.Sex.FEMALE,
                    ["DEFS 3", 'LABS "LOAD"', "STDTLOAD", "OFSZ 50.0", "OFSD 0.0E-12"],
                ),
                Standard(
                    Standard.Type.THRU,
                    Standard.Sex.MALE,
                    ["DEFS 4", "STDTDELA", "OFSZ 50.0", "OFSD 44.398355E-12"],
                ),
                Standard(
                    Standard.Type.THRU,
                    Standard.Sex.FEMALE,
                    ["DEFS 4", "STDTDELA", "OFSZ 50", "OFSD 43.043948E-12"],
                ),
                Standard(
                    Standard.Type.SHORT,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 7",
                        "STDTSHOR",
                        "OFSZ 50",
                        "OFSD 55.375902E-12",
                        "OFSL 4.421873E+9",
                        "C0 -840.413037",
                        "C1 15513.882390",
                        "C2 -5988.890460",
                        "C3 -21.139021",
                    ],
                ),
                Standard(
                    Standard.Type.OPEN,
                    Standard.Sex.FEMALE,
                    [
                        "DEFS 8",
                        "STDTOPEN",
                        "OFSZ 50",
                        "OFSD 32.565610E-12",
                        "OFSL 0.0E+9",
                        "C0 183.082272",
                        "C1 31605.595064",
                        "C2 2570.475809",
                        "C3 1579.486689",
                    ],
                ),
            ],
        ),
    ]

    probes = [
        Probe(
            "8481A",
            100.0,
            0.0,
            dict(
                [
                    (00.01e9, 98.2),  # HP E4436B/8482A
                    (00.03e9, 99.5),  # HP E4436B/8482A
                    (00.1e9, 98.9),
                    (00.3e9, 98.5),  # HP E4436B/8482A
                    (01.0e9, 97.2),  # HP E4436B/8482A
                    (01.5e9, 97.0),  # HP E4436B/8482A
                    (02.0e9, 99.2),
                    (03.0e9, 98.5),
                    (04.0e9, 98.1),
                    (05.0e9, 96.4),
                    (06.0e9, 96.0),
                    (07.0e9, 97.2),
                    (08.0e9, 95.5),
                    (09.0e9, 94.5),
                    (10.0e9, 92.8),
                    (11.0e9, 93.3),
                    (12.4e9, 93.2),
                    (13.0e9, 92.2),
                    (14.0e9, 92.5),
                    (15.0e9, 91.4),
                    (16.0e9, 92.5),
                    (17.0e9, 94.3),
                    (18.0e9, 93.5),
                ]
            ),
        ),
        Probe(
            "8482A",
            98.0,
            0.0,
            dict(
                [
                    (0000.1e6, 96.7),
                    (0000.3e6, 97.9),
                    (0001.0e6, 99.3),
                    (0003.0e6, 98.9),
                    (0010.0e6, 98.3),
                    (0030.0e6, 98.4),
                    (0100.0e6, 98.1),
                    (0300.0e6, 97.6),
                    (1000.0e6, 97.3),
                    (2000.0e6, 96.2),
                    (3000.0e6, 90.3),
                    (4000.0e6, 89.5),
                    (4200.0e6, 88.2),
                    (5000.0e6, 82.4),  # HP8753D
                    (5400.0e6, 77.4),  # HP8753D
                    (6000.0e6, 77.0),
                ]
            ),
        ),  # HP8753D
        Probe(
            "8482Auc",
            96.1,
            0.0,
            dict(
                [
                    (0000.1e6, 94.7),  # HP8753D/Probe 2
                    (0000.3e6, 95.6),  # HP8753D/Probe 2
                    (0001.0e6, 96.0),  # HP8753D/Probe 2
                    (0003.0e6, 96.0),  # HP8753D/Probe 2
                    (0010.0e6, 95.1),  # HP8753D/Probe 2
                    (0030.0e6, 96.2),  # HP8753D/Probe 2
                    (0100.0e6, 95.8),  # HP8753D/Probe 2
                    (0300.0e6, 96.3),  # HP8753D/Probe 2
                    (0500.0e6, 96.8),  # HP8753D/Probe 2
                    (1000.0e6, 97.0),  # HP8753D/Probe 2
                    (1500.0e6, 93.6),  # HP8753D/Probe 2
                    (2000.0e6, 91.0),  # HP8753D/Probe 2
                    (2600.0e6, 98.0),  # HP8753D/Probe 2
                    (3000.0e6, 96.9),  # HP8753D/Probe 2
                    (4000.0e6, 79.2),  # HP8753D/Probe 2
                    (4200.0e6, 80.3),  # HP8753D/Probe 2
                    (5000.0e6, 97.8),  # HP8753D/Probe 2
                    (5400.0e6, 89.4),  # HP8753D/Probe 2
                    (6000.0e6, 75.2),
                ]
            ),
        ),  # HP8753D/Probe 2
        Probe(
            "8484A",
            90.6,
            -30.0,
            dict(
                [
                    (00.1e9, 89.1),
                    (00.3e9, 89.9),
                    (00.5e9, 90.3),
                    (01.0e9, 90.2),
                    (02.0e9, 89.9),
                    (03.0e9, 87.4),
                    (04.0e9, 89.9),
                    (05.0e9, 89.3),
                    (06.0e9, 87.9),
                    (07.0e9, 87.6),
                    (08.0e9, 88.1),
                    (09.0e9, 88.7),
                    (10.0e9, 88.9),
                    (11.0e9, 87.8),
                    (12.0e9, 89.5),
                    (12.4e9, 91.0),
                    (13.0e9, 90.1),
                    (14.0e9, 94.5),
                    (15.0e9, 93.6),
                    (16.0e9, 97.0),
                    (17.0e9, 98.4),
                    (18.0e9, 100),
                ]
            ),
        ),
        Probe(
            "8487A",
            96.1,
            0.0,
            dict(
                [
                    (00.3e9, 99.7),
                    (02.0e9, 98.2),
                    (10.0e9, 97.9),
                    (14.0e9, 96.2),
                    (18.0e9, 95.0),
                    (22.0e9, 94.9),
                    (24.0e9, 94.0),
                    (26.0e9, 94.8),
                    (28.0e9, 94.3),
                    (30.0e9, 92.9),
                    (32.0e9, 93.2),
                    (34.0e9, 93.4),
                    (36.0e9, 95.1),
                    (38.0e9, 93.0),
                    (40.0e9, 92.2),
                    (42.0e9, 93.0),
                    (44.0e9, 92.9),
                    (46.0e9, 90.5),
                    (48.0e9, 93.5),
                    (50.0e9, 88.2),
                ]
            ),
        ),
    ]


if __name__ == "__main__":
    Lab.scanDevices()
    Lab.printKits()
    Lab.printProbes()
