from smp_common import (
    connect_smp, query_options, list_hw_modules,
    detect_a9_variant, A9_TP_RANGES, A9_V_6301, A9_V_UNKNOWN,
    READS_PER_POINT, READ_DELAY, POINT_DELAY,
    unlock_protect,
)

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
            "desc": "A4 Pulse Generator (SMP-B14)",
            "option": "SMP-B14",
            1005: (0.9, 1.2, "Pulse generator level"),
    },
    "A4LF": {
            "desc": "A4 LF Generator (SM-B2, 2nd)",
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
            "desc": "A5 LF Generator (SM-B2, 1st)",
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
            200: (-0.02, 0.02, "10-kOhm reference impedance"),
            201: (2, 12, "Control voltage 100-MHz xtal VCO"),
            202: (-10.1, 0.01, "Output D/A converter tuning voltage"),
            203: (1.8, 5.2, "1-MHz reference signal for reference PLL"),
            204: (2.0, 3.0, "1-MHz relational signal for reference PLL"),
            205: (0.8, 3.5, "External reference I/O"),
            206: (0.1, 0.4, "300-MHz IF in multiplier"),
            207: (0.3, 1.3, "50-MHz output REF50"),
            208: (-0.04, 0.04, "Frequency detector (Step PLL locked)"),
            209: (0.18, 0.60, "100-MHz output REF100"),
            210: (-0.02, 0.6, "600-MHz output REF600 (0.2-0.6V <93.75MHz / +/-20mV >=93.75MHz)"),
            211: (22.5, 25.5, "24V supply voltage"),
            212: (1, 20, "Control voltage Step VCO"),
            213: (0.4, 2.5, "Output signal step divider"),
            214: (0.10, 0.25, "Down-converted VCO signal 3-17MHz"),
            215: (0.2, 0.6, "Output step frequency FSTEP 103-117MHz"),
    },
    "A8": {
            "desc": "Digital Synthesis",
            300: (14, 16, "Supply voltage VA15-P"),
            301: (-0.1, 0.1, "DCOD oscillator tuning voltage"),
            302: (-0.02, 0.02, "DCOD oscillator level"),
            303: (0.5, 1.5, "DDS-GA clock level"),
            304: (0.05, 0.2, "Level at output FDDS"),
            305: (12, 20, "Oscillator tuning voltage"),
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
            1802: (0.8, 12.0, "Pretune DAC"),
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
    "A21": {
            "desc": "Sampling Module (via A26 MUX over W216)",
            1902: (0.9, 1.1, "VARSAMP model ID via W216.9"),
            1910: (7.5, 11, "DIAGSAMP comb-gen diag via W216.10"),
    },
    "A26": {
            "desc": "Microwave Interface",
            1900: (-0.02, 0.02, "Offset voltage correction"),
            1901: {"desc": "ID Option SMP-B11 DCNV",
                   "option": "SMP-B11",
                   "installed": (0.5, 1.5),
                   "not_installed": (-0.25, 0.25)},
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


def iter_points(interval):
    for tp, entry in interval.items():
        if isinstance(tp, int):
            yield tp, entry


def read_point(dev, tp):
    time.sleep(POINT_DELAY)
    values = []
    for i in range(READS_PER_POINT):
        if i > 0:
            time.sleep(READ_DELAY)
        reply = dev.query(f":DIAG:MEAS:POINT{tp}?")
        values.append(float(reply))
    avg = sum(values) / len(values)
    return values, avg


def evaluate_point(dev, tp, entry, installed):
    values, avg = read_point(dev, tp)
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
    label = f"TP{tp:04d}  {desc:50s}"
    if info_only:
        result = f"val={avg:8.2f}{'':22s}INFO"
        status = "INFO"
    elif abs(avg - tp) < 0.01 and not (lo <= avg <= hi):
        result = f"val={avg:8.2f}{'':22s}ECHO"
        status = "ECHO"
    else:
        if avg < lo:
            d = avg - lo
            pct = abs(d / lo) * 100 if lo != 0 else 0
            diff = f"FAIL ({d:+.2f}, {pct:.1f}%)"
            status = "FAIL"
        elif avg > hi:
            d = avg - hi
            pct = abs(d / hi) * 100 if hi != 0 else 0
            diff = f"FAIL ({d:+.2f}, {pct:.1f}%)"
            status = "FAIL"
        else:
            diff = "OK"
            status = "OK"
        result = f"avg={avg:8.2f}  [{lo:8.2f},{hi:8.2f}] {diff}"
    return label, values, result, status


def measure_interval(dev, interval, installed, verbose=False):
    summary = {"OK": 0, "FAIL": 0, "ECHO": 0, "INFO": 0}
    for tp, entry in iter_points(interval):
        label, values, result, status = evaluate_point(dev, tp, entry, installed)
        summary[status] += 1
        if verbose:
            cols = "".join(f"{v:8.2f}" for v in values)
            print(f"{label}\n  {cols}  {result}")
        else:
            print(f"{label} {result}")
    return summary


def is_installed(interval, installed_options):
    """Check if a module is installed (no option or option present)."""
    opt = interval.get("option")
    return opt is None or opt in installed_options


def list_modules(installed):
    """Print all diagnostic modules with install status."""
    for key, interval in MODULES.items():
        desc = interval.get("desc", key)
        count = sum(1 for k in interval if isinstance(k, int))
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


def apply_a9_variant(dev):
    """Replace MODULES['A9'] with the detected variant's range table."""
    stock = detect_a9_variant(dev, verbose=True)
    key = stock if stock in A9_TP_RANGES else A9_V_6301
    MODULES["A9"] = A9_TP_RANGES[key]
    if stock not in A9_TP_RANGES:
        print(f"  variant unresolved; falling back to {A9_V_6301} ranges")


def apply_a8_freq(dev):
    """Park the instrument at FREQ = 1 GHz so A8 TP305 matches band-1 p.359."""
    dev.write(":FREQ 1 GHz")
    time.sleep(0.3)


def run_diagnostics(dev, modules, installed, verbose=False, ignore_opt=False):
    """Measure selected modules, skipping uninstalled ones unless forced."""
    if "A9" in modules:
        apply_a9_variant(dev)
    for name in modules:
        interval = MODULES[name]
        desc = interval.get("desc", name)
        installed_now = is_installed(interval, installed)
        if not installed_now and not ignore_opt:
            print(f"\n=== {name}: {desc} [not installed] ===")
            continue
        if not installed_now and ignore_opt:
            print(f"\n=== {name}: {desc} [not installed by *OPT?; probing anyway] ===")
        else:
            print(f"\n=== {name}: {desc} ===")
        if name == "A8":
            apply_a8_freq(dev)
        measure_interval(dev, interval, installed, verbose=verbose)


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
    parser.add_argument(
        "--detect-a9",
        action="store_true",
        help="detect A9 board variant (1035.6301.02 vs 1035.6199.02) and exit",
    )
    parser.add_argument(
        "--ignore-opt",
        dest="ignore_opt",
        action="store_true",
        help="probe requested modules even if *OPT? says they are not installed",
    )
    parser.add_argument(
        "--unlock",
        type=int,
        choices=[1, 2, 3],
        nargs="?",
        const=1,
        default=None,
        metavar="LEVEL",
        help="clear the UTILITIES/PROTECT lock flag on connect"
             " (:SYST:PROT<n>:STAT OFF, <password>)."
             " L1 (default) = PULSE GEN / YFOM / ALC AMP / LEVEL view menus;"
             " L2 = REF OSC menu; L3 = UTILITIES/DIAG/PARAM menu."
             " Note: firmware 3.70 does NOT gate GPIB access on this flag —"
             " all SCPI commands work regardless of state. The flag only"
             " hides the corresponding front-panel menu items. Kept for"
             " forward-compatibility and for clearing the on-screen"
             " 'password required' indicator while scripting",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    try:
        dev = connect_smp()
    except ConnectionError:
        exit(1)

    try:
        if args.unlock is not None:
            errs = unlock_protect(dev, args.unlock)
            if errs:
                print(f"LOCK LEVEL {args.unlock}: unlock FAILED ({errs})")
            else:
                print(f"LOCK LEVEL {args.unlock}: unlocked")

        installed = query_options(dev)

        if args.hw_info:
            list_hw_modules(dev)
            exit(0)

        if args.detect_a9:
            stock = detect_a9_variant(dev, verbose=True)
            print(f"  verdict: {stock}")
            exit(0 if stock != A9_V_UNKNOWN else 2)

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
                        verbose=args.verbose,
                        ignore_opt=args.ignore_opt)
    finally:
        dev.close()
