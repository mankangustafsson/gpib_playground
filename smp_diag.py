from Devices import Device
from Lab import Lab

import argparse
import time


MODULES = {
    "A2": {
            "desc": "Supply Voltages",
            211: (22, 26, "Supply voltage VA24-P"),
            300: (14, 16, "Supply voltage VA15-P"),
            306: (-16, -14, "Supply voltage VA15-N"),
            307: (7, 8, "Supply voltage VA7.5-P"),
    },
    "A3": {
            "desc": "Front Module",
            0: (-0.05, 0.05, "Reference ground"),
            1: (-15, 15, "Input DIAG-15"),
            2: (-5, 5, "Input DIAG-5"),
            3: (0, 10, "X voltage"),
            4: (-15, 15, "Voltmeter"),
            5: (None, None, "Programming voltage FLASH"),
            6: (4.9, 5.1, "Reference voltage X-D/A-Wandler"),
            7: (3.0, 3.7, "Battery voltage"),
    },
    "A4": {
            "desc": "Option SM-B2 2nd LF Generator",
            "option": "SM-B2",
            1300: (-0.01, 0.01, "Reference ground"),
            1301: (1.0, 5.0, "Level quartz oscillator"),
            1302: (-1.1, 1.1, "Output INT1"),
            # 1303 unused
            1304: (4.8, 5.2, "Supply voltage +5VA"),
            1305: (4.8, 5.2, "Supply voltage +5VDDS"),
            1306: (14.4, 15.6, "Supply voltage VA15-P"),
            1307: (-15.6, -14.4, "Supply voltage VA15-N"),
    },
    "A5": {
            "desc": "Option SM-B2 LF Generator",
            "option": "SM-B2",
            1200: (-0.01, 0.01, "Reference ground"),
            1201: (1.0, 5.0, "Level quartz oscillator"),
            1202: (-1.1, 1.1, "Output INT2"),
            1203: (-4.1, 4.1, "Output LFOUT"),
            1204: (4.8, 5.2, "Supply voltage +5VA"),
            1205: (4.8, 5.2, "Supply voltage +5VDDS"),
            1206: (14.4, 15.6, "Supply voltage VA15-P"),
            1207: (-15.6, -14.4, "Supply voltage VA15-N"),
    },
    "A6": {
            "desc": "Option SM-B5 FM/\u03a6M Modulator",
            "option": "SM-B5",
            500: (-0.01, 0.01, "Reference ground"),
            501: (2.7, 12.3, "Tuning voltage VCO"),
            502: (0.1, 0.4, "Level VCO"),
            503: (0.1, 0.4, "LO level 1st mixer"),
            504: (0.1, 0.6, "Output level FDFM"),
            505: (-4, 4, "Modulation voltage"),
    },
    "A7": {
            "desc": "Reference/Step Synthesis",
            200: (-0.01, 0.01, "Reference ground"),
            201: (0.5, 14, "Tuning voltage VCXO 100MHz"),
            202: (-10, 0, "Reference for tuning voltage DAC"),
            203: (3.5, 5, "Reference level 1MHz"),
            204: (1.8, 3.6, "Output level divider 1 MHz"),
            205: (1.8, 3.6, "External reference level"),
            206: (0.1, 0.3, "IF level 300 MHz"),
            207: (0.6, 1.2, "Output level REF50"),
            208: (-0.08, 0.08, "Frequency detector"),
            209: (0.2, 1.4, "Output level REF100"),
            210: (0.15, 0.52, "Output level REF600"),
            211: (22, 26, "Supply voltage VA24-P"),
            212: (0.5, 20, "Tuning voltage Step VCO"),
            213: (1, 2, "Level Step divider"),
            214: (0.07, 0.2, "Step IF level 3 to 17MHz"),
            215: (0.2, 1, "Output level FSTEP"),
    },
    "A8": {
            "desc": "Digital Synthesis",
            300: (14, 16, "Supply voltage VA15-P"),
            301: (-1, 10, "Tuning voltage clock VCO"),
            302: (-0.02, 0.02, "Level VCO clock DCOD"),
            303: (0.5, 1.5, "Clock for DDS_GA"),
            304: (0.05, 0.2, "Output level FDSYN"),
            305: (-5, 24, "Tuning voltage buffer VCO"),
            306: (-16, -14, "Supply voltage VA15-N"),
            307: (7, 8, "Supply voltage VA7.5-P"),
    },
    "A9": {
            "desc": "ALC Amplifier",
            1600: (-0.01, 0.01, "Reference ground"),
            1601: (4.975, 5.025, "Positive reference voltage"),
            1602: (-5.025, -4.975, "Negative reference voltage"),
            1603: (-1.01, 0, "AM depth DAC"),
            1604: (0, 3.05, "AM adder"),
            1605: (0, 2.5, "FM deviation DACs"),
            1606: (0, 1.5, "Level DACs"),
            1607: (0.7, 1.1, "Aux. oscillator emitter voltage"),
            1608: (-0.005, 0.005, "EXT ALC offset"),
            1609: (0, 15, "Test amp. (mixer isolation)"),
            1610: (10.4, 10.6, "Collector voltage V240"),
            1611: (10.4, 10.6, "Collector voltage V250"),
            1612: (-12, 12, "Diff. Amp. offset"),
            1613: (-5, 0.7, "Main loop (control voltage)"),
            1614: (-5, 0, "Limit DAC"),
            1615: (0, 0.42, "LF generator"),
    },
    "A10": {
            "desc": "YIG PLL",
            1800: (-10.02, -9.98, "Negative reference voltage"),
            1801: (4.95, 5.45, "ECL supply voltage"),
            1802: (-12.0, -0.8, "Pretune DAC"),
            1803: (0, 10, "Tracking DAC"),
            1804: (-6, -3, "Output N210-B"),
            1805: (-5.7, -0.37, "Main tuning current"),
            1806: (3.5, 4.3, "ECL gates bias voltage"),
            1807: (-12, 12, "PLL control voltage"),
            1808: (-12, 12, "FM driver"),
            1809: (-8, 8, "FM coil current"),
            1810: (-12, 12, "Tracking driver"),
            1811: (-8, 8, "Tracking coil current"),
            1812: (-12, 12, "FM adder"),
            1815: (-0.01, 0.01, "Reference ground"),
    },
    "A26": {
            "desc": "Microwave Interface",
            1900: (-0.02, 0.02, "Offset voltage correction"),
            1901: {"desc": "ID Option SMP-B11 DCNV",
                   "option": "SMP-B11",
                   "installed": (0.5, 1.5),
                   "not_installed": (-0.25, 0.25)},
            1902: (0.5, 1.5, "ID SMP02 model"),
            1903: {"desc": "ID Option SMP-B11 DCNV",
                   "option": "SMP-B11",
                   "installed": (0.5, 1.5),
                   "not_installed": (-0.25, 0.25)},
            1904: {"desc": "ID Option SMP-B11 Freq Ext",
                   "option": "SMP-B11",
                   "installed": (0.5, 1.5),
                   "not_installed": (-0.25, 0.25)},
            1905: {"desc": "ID Option SMP-B13 PUM2",
                   "option": "SMP-B13",
                   "installed": (0.5, 1.5),
                   "not_installed": (-0.25, 0.25)},
            1906: {"desc": "ID Option SMP-B12 PUM20",
                   "option": "SMP-B12",
                   "installed": (0.5, 1.5),
                   "not_installed": (-0.25, 0.25)},
            1907: (-0.25, 0.25, "ID AMP20/DBL27/DBL40"),
            1910: (7.5, 11, "Diagnosis sampling pulse gen (SMPL)"),
            1911: (0, 3, "Diagnosis detector output (DTK27/40)"),
            1914: {"desc": "ID Option SMP-B15 ATT27",
                   "option": "SMP-B15",
                   "installed": (0.5, 1.5),
                   "not_installed": (-0.25, 0.25)},
            1915: (-5.3, -4.7, "Supply voltage VA5-N for YFO"),
    },
    "A71": {
            "desc": "Option SM-B1 Reference Oscillator OCXO",
            "option": "SM-B1",
            100: (-0.01, 0.01, "Reference ground"),
            101: (None, None, "Bridge voltage thermostat (ROSC v06 only)"),
            102: (0.6, 2.5, "Output level"),
    },
}

READS_PER_POINT = 3
READ_DELAY = 0.05
POINT_DELAY = 0.15


def measure_interval(dev, interval, installed, verbose=False):
    for x, entry in interval.items():
        if not isinstance(x, int):
            continue
        if isinstance(entry, dict):
            opt = entry["option"]
            desc = entry["desc"]
            if opt in installed:
                lo, hi = entry["installed"]
                desc += " [installed]"
            else:
                lo, hi = entry["not_installed"]
                desc += " [not installed]"
        else:
            lo, hi, desc = entry
        info_only = lo is None
        time.sleep(POINT_DELAY)

        values = []
        for i in range(READS_PER_POINT):
            if i > 0:
                time.sleep(READ_DELAY)
            reply = dev.query(f":DIAG:MEAS:POINT{x}?")
            values.append(float(reply))

        avg = sum(values) / len(values)
        label = f"TP{x:04d}  {desc:50s}"
        if info_only:
            result = f"val={avg:8.2f}{'':22s}INFO"
        elif abs(avg - x) < 0.01 and not (lo <= avg <= hi):
            result = f"val={avg:8.2f}{'':22s}ECHO"
        else:
            if avg < lo:
                d = avg - lo
                pct = abs(d / lo) * 100 if lo != 0 else 0
                diff = f"FAIL ({d:+.2f}, {pct:.1f}%)"
            elif avg > hi:
                d = avg - hi
                pct = abs(d / hi) * 100 if hi != 0 else 0
                diff = f"FAIL ({d:+.2f}, {pct:.1f}%)"
            else:
                diff = "OK"
            result = (
                f"avg={avg:8.2f}  [{lo:8.2f},{hi:8.2f}] {diff}"
            )
        if verbose:
            cols = "".join(f"{v:8.2f}" for v in values)
            print(f"{label}\n  {cols}  {result}")
        else:
            print(f"{label} {result}")


def query_options(dev):
    """Query *OPT? and return set of installed option names."""
    reply = dev.query("*OPT?").strip()
    return {o for o in reply.split(",") if o != "0"}


def is_installed(interval, installed_options):
    """Check if a module is installed (no option or option present)."""
    opt = interval.get("option")
    return opt is None or opt in installed_options


def query_hw_modules(dev):
    """Query :DIAG:INFO:MOD? and return dict of module info."""
    reply = dev.query(":DIAG:INFO:MOD?").strip()
    modules = {}
    for entry in reply.split(","):
        parts = entry.strip().split()
        if len(parts) >= 3:
            name = parts[0]
            var = parts[1]
            rev = parts[2]
            modules[name] = (var, rev)
    return modules


def list_hw_modules(dev):
    """Print hardware modules from :DIAG:INFO:MOD?."""
    hw = query_hw_modules(dev)
    for name, (var, rev) in hw.items():
        print(f"  {name:8s}  {var}  {rev}")


def list_modules(installed):
    """Print all diagnostic modules with install status."""
    for key, interval in MODULES.items():
        desc = interval.get("desc", key)
        count = sum(
            1 for k in interval if isinstance(k, int)
        )
        opt = interval.get("option")
        if opt is None:
            tag = ""
        elif is_installed(interval, installed):
            tag = " [installed]"
        else:
            tag = " [not installed]"
        print(
            f"  {key:4s}  {desc:40s}"
            f" {count:2d} points{tag}"
        )


def run_diagnostics(dev, modules, installed, verbose=False):
    """Measure selected modules, skipping uninstalled ones."""
    for name in modules:
        interval = MODULES[name]
        desc = interval.get("desc", name)
        if not is_installed(interval, installed):
            print(
                f"\n=== {name}: {desc}"
                " [not installed] ==="
            )
            continue
        print(f"\n=== {name}: {desc} ===")
        measure_interval(dev, interval, installed,
                         verbose=verbose)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SMP02 test point diagnostics"
    )
    parser.add_argument(
        "-m", "--module",
        nargs="+",
        type=str.upper,
        choices=[*MODULES.keys(), "ALL"],
        help="module(s) to measure",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="show individual readings",
    )
    parser.add_argument(
        "-lm", "--list-modules",
        action="store_true",
        help="list diagnostic modules and exit",
    )
    parser.add_argument(
        "-hw", "--hw-info",
        action="store_true",
        help="list hardware modules and exit",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    dev = Lab.connectByType(
        Device.Type.RF_GEN, hint="SMP02", verbose=True
    )
    if dev is None:
        exit(1)

    try:
        installed = query_options(dev)

        if args.hw_info:
            list_hw_modules(dev)
            exit(0)

        if args.list_modules:
            list_modules(installed)
            exit(0)

        if not args.module:
            print("specify module(s) with -m"
                  " or use --list-modules")
            exit(1)

        if "ALL" in args.module:
            selected = list(MODULES.keys())
        else:
            order = list(MODULES.keys())
            selected = sorted(
                args.module, key=order.index
            )

        run_diagnostics(dev, selected, installed,
                        args.verbose)
    finally:
        dev.close()
