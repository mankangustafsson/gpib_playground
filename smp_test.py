from smp_common import connect_smp, read_tp, query_options

import argparse
import time


class SmpTest:
    """Base class for SMP02 functional tests."""
    name = ""
    desc = ""
    option = None

    def __init__(self, dev):
        self.dev = dev
        self.passed = True

    def __call__(self):
        print(f"\n=== {self.name}: {self.desc} ===")
        self.dev.write("*RST")
        time.sleep(0.5)
        self.run()
        return self.passed

    def tp(self, point):
        return read_tp(self.dev, point)

    def check(self, ok, msg):
        """Print a check result and track failures."""
        print(f"  {msg}  {'OK' if ok else 'FAIL'}")
        if not ok:
            self.passed = False
        return ok

    def run(self):
        raise NotImplementedError


class TestA4(SmpTest):
    name = "A4"
    desc = "Pulse Generator"
    option = "SMP-B14"

    def run(self):
        self.dev.write("SOUR:PULS:WIDT 80ns")
        self.dev.write("SOUR:PULS:PER 180ns")
        self.dev.write("SOUR:PULM:SOUR INT")
        self.dev.write("SOUR:PULM:STAT ON")
        time.sleep(0.5)

        v1005 = self.tp(1005)
        self.check(0.9 <= v1005 <= 1.2,
                   f"TP1005={v1005:.3f}V  [0.9, 1.2]")


class TestA5(SmpTest):
    name = "A5"
    desc = "LF Generator (SM-B2)"
    option = "SM-B2"

    def run(self):
        self.dev.write("OUTP2:SOUR 2")
        self.dev.write("OUTP2:VOLT 4V")
        self.dev.write("SOUR2:FREQ:CW 0.2")
        self.dev.write("SOUR2:FUNC:SHAP SQU")
        time.sleep(0.5)

        n_samples = 30
        sample_interval = 0.2
        vals_1202 = []
        vals_1203 = []
        print("  Sampling TP1202/1203 over one period (~6s)...")
        for _ in range(n_samples):
            vals_1202.append(self.tp(1202))
            vals_1203.append(self.tp(1203))
            time.sleep(sample_interval)

        min_1202, max_1202 = min(vals_1202), max(vals_1202)
        min_1203, max_1203 = min(vals_1203), max(vals_1203)

        ok_1202 = min_1202 <= -0.8 and max_1202 >= 0.8
        ok_1203 = min_1203 <= -3.0 and max_1203 >= 3.0
        self.check(ok_1202,
                   f"TP1202: {min_1202:+.2f}V .. {max_1202:+.2f}V"
                   f"  [-1, +1]")
        self.check(ok_1203,
                   f"TP1203: {min_1203:+.2f}V .. {max_1203:+.2f}V"
                   f"  [-4, +4]")


class TestA6(SmpTest):
    name = "A6"
    desc = "FM/ΦM Modulator — FSK polarity test"
    option = "SM-B5"

    def run(self):
        self.dev.write("SOUR:DM:TYPE FSK")
        self.dev.write("SOUR:DM:FSK:MODE PREC")
        self.dev.write("SOUR:DM:FSK:DEV 1024kHz")
        self.dev.write("SOUR:DM:STAT ON")
        time.sleep(0.5)

        self.dev.write("SOUR:DM:FSK:POL NORM")
        time.sleep(0.3)
        v505_norm = self.tp(505)
        self.check(-3.5 <= v505_norm <= 2.5,
                   f"TP505 NORM polarity: {v505_norm:+.2f}V"
                   f"  [-3.50, 2.50]")

        self.dev.write("SOUR:DM:FSK:POL INV")
        time.sleep(0.3)
        v505_inv = self.tp(505)
        self.check(2.5 <= v505_inv <= 3.5,
                   f"TP505 INV  polarity: {v505_inv:+.2f}V"
                   f"  [ 2.50, 3.50]")

        delta = abs(v505_inv - v505_norm)
        self.check(delta > 0.5,
                   f"TP505 polarity shift: {delta:.2f}V"
                   f"  (expect >0.5V)")

        v504 = self.tp(504)
        self.check(0.1 <= v504 <= 0.5,
                   f"TP504 output level:  {v504:.3f}V"
                   f"  [ 0.10, 0.50]")


class TestA7(SmpTest):
    name = "A7"
    desc = "Reference/Step Synthesis — sweep test"

    def run(self):
        f_start = 2282e6
        f_stop = 2482e6
        n_steps = 21
        step = (f_stop - f_start) / (n_steps - 1)

        prev_212 = None
        monotonic = True
        all_pass = True

        print(f"{'Freq (MHz)':>12s}  {'TP212':>8s}  {'TP215':>8s}"
              f"  {'212 mono':>8s}  {'215>0.2':>8s}")
        print("-" * 58)

        for i in range(n_steps):
            freq = f_start + i * step
            self.dev.write(f"SOURCE:FREQUENCY:CW {freq:.0f}")
            time.sleep(0.3)

            v212 = self.tp(212)
            v215 = self.tp(215)

            if prev_212 is not None and v212 <= prev_212:
                mono_ok = False
                monotonic = False
            else:
                mono_ok = True
            prev_212 = v212

            tp215_ok = v215 > 0.2
            if not tp215_ok:
                all_pass = False

            mono_str = "OK" if mono_ok else "FAIL"
            t215_str = "OK" if tp215_ok else "FAIL"
            print(f"{freq/1e6:12.1f}  {v212:8.2f}  {v215:8.2f}"
                  f"  {mono_str:>8s}  {t215_str:>8s}")

        print()
        self.check(monotonic, "TP212 monotonic increase:")
        self.check(all_pass, "TP215 >200 mV all steps: ")


class TestA8(SmpTest):
    name = "A8"
    desc = "Digital Synthesis — sweep test"

    def run(self):
        f_start = 19.9887543625e9
        f_stop = 19.9939783783e9
        n_steps = 21
        step = (f_stop - f_start) / (n_steps - 1)

        prev_305 = None
        monotonic = True

        print(f"{'Freq (GHz)':>16s}  {'TP305':>8s}  {'305 mono':>8s}")
        print("-" * 38)

        for i in range(n_steps):
            freq = f_start + i * step
            self.dev.write(f"SOURCE:FREQUENCY:CW {freq:.4f}")
            time.sleep(0.3)

            v305 = self.tp(305)

            if prev_305 is not None and v305 <= prev_305:
                mono_ok = False
                monotonic = False
            else:
                mono_ok = True
            prev_305 = v305

            mono_str = "OK" if mono_ok else "FAIL"
            print(f"{freq/1e9:16.10f}  {v305:8.2f}  {mono_str:>8s}")

        print()
        self.check(monotonic, "TP305 monotonic increase:")


class TestA9(SmpTest):
    name = "A9"
    desc = "ALC Amplifier — ASK modulation test"

    def run(self):
        self.dev.write("SOURCE:FREQUENCY:CW 10GHz")
        self.dev.write("POW 0")
        self.dev.write("SOUR:DM:TYPE ASK")
        self.dev.write("SOUR:DM:ASK:DEPT 100")
        self.dev.write("SOUR:DM:ASK:POL NORM")
        self.dev.write("SOUR:DM:STAT ON")
        self.dev.write("OUTP:STAT ON")
        time.sleep(0.5)

        v1613 = self.tp(1613)
        self.check(-6.0 <= v1613 <= -3.5,
                   f"Step 1: 0dBm NORM  TP1613={v1613:+.2f}V"
                   f"  [≈-4.9V]")

        self.dev.write("POW 22")
        self.dev.write("SOUR:DM:ASK:POL INV")
        time.sleep(0.5)
        v1613 = self.tp(1613)
        self.check(-0.5 <= v1613 <= 1.5,
                   f"Step 2: 22dBm INV  TP1613={v1613:+.2f}V"
                   f"  [≈+0.5V]")

        level = 22.0
        while level >= -10.0:
            self.dev.write(f"POW {level:.1f}")
            time.sleep(0.3)
            status = int(self.dev.query("STAT:QUES:COND?"))
            if not (status & 2):
                break
            level -= 0.5

        v1613 = self.tp(1613)
        self.check(-0.2 <= v1613 <= 0.8,
                   f"Step 3: {level:.1f}dBm (unlevel cleared)"
                   f"  TP1613={v1613:+.2f}V  [≈+0.3V]")


class TestA10(SmpTest):
    name = "A10"
    desc = "YIG PLL — sweep test"

    def run(self):
        f_start = 2e9
        f_stop = 20e9
        n_steps = 21
        step = (f_stop - f_start) / (n_steps - 1)

        prev_1805 = None
        monotonic_dec = True
        all_1807_ok = True

        print(f"{'Freq (GHz)':>12s}  {'TP1805':>8s}  {'TP1807':>8s}"
              f"  {'1805 dec':>8s}  {'1807 ok':>8s}")
        print("-" * 58)

        for i in range(n_steps):
            freq = f_start + i * step
            self.dev.write(f"SOURCE:FREQUENCY:CW {freq:.0f}")
            time.sleep(0.3)

            v1805 = self.tp(1805)
            v1807 = self.tp(1807)

            if prev_1805 is not None and v1805 >= prev_1805:
                mono_ok = False
                monotonic_dec = False
            else:
                mono_ok = True
            prev_1805 = v1805

            t1807_ok = -3.0 <= v1807 <= 3.0
            if not t1807_ok:
                all_1807_ok = False

            mono_str = "OK" if mono_ok else "FAIL"
            t1807_str = "OK" if t1807_ok else "FAIL"
            print(f"{freq/1e9:12.1f}  {v1805:8.2f}  {v1807:8.2f}"
                  f"  {mono_str:>8s}  {t1807_str:>8s}")

        print()
        self.check(monotonic_dec, "TP1805 monotonic decrease:")
        self.check(all_1807_ok, "TP1807 in [-3V, +3V]:    ")


class TestA26(SmpTest):
    name = "A26"
    desc = "Microwave Interface — sampling signal"

    def run(self):
        v1910 = self.tp(1910)
        self.check(v1910 > 8.0,
                   f"TP1910={v1910:.2f}V  (>8V)")


# (description, test class, required option or None)
MODULES = {
    "A4":  TestA4,
    "A5":  TestA5,
    "A6":  TestA6,
    "A7":  TestA7,
    "A8":  TestA8,
    "A9":  TestA9,
    "A10": TestA10,
    "A26": TestA26,
}


def list_modules(installed):
    """Print available test modules with option requirements."""
    for key, cls in MODULES.items():
        opt = cls.option
        if opt is None:
            tag = ""
        elif opt in installed:
            tag = " [installed]"
        else:
            tag = " [not installed]"
        print(f"  {key:4s}  {cls.desc:40s}{tag}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="SMP02 functional module tests"
    )
    parser.add_argument(
        "-m", "--module",
        nargs="+",
        type=str.upper,
        choices=[*MODULES.keys(), "ALL"],
        help="module(s) to test",
    )
    parser.add_argument(
        "-lm", "--list-modules",
        action="store_true",
        help="list available test modules and exit",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if not args.module and not args.list_modules:
        print("specify module(s) with -m"
              " or use --list-modules")
        exit(1)

    try:
        dev = connect_smp()
    except ConnectionError:
        exit(1)

    try:
        installed = query_options(dev)
        print(f"Installed options: {', '.join(sorted(installed))}")

        if args.list_modules:
            list_modules(installed)
            exit(0)

        if "ALL" in args.module:
            selected = list(MODULES.keys())
        else:
            order = list(MODULES.keys())
            selected = sorted(
                args.module, key=order.index
            )

        passed = []
        failed = []
        skipped = []

        for name in selected:
            cls = MODULES[name]
            if cls.option and cls.option not in installed:
                print(f"\n=== {name}: {cls.desc} ==="
                      f"\n  SKIPPED — requires {cls.option}"
                      f" (not installed)")
                skipped.append(name)
                continue
            if cls(dev)():
                passed.append(name)
            else:
                failed.append(name)

        print("\n" + "=" * 40)
        print(f"PASSED:  {len(passed):2d}  {', '.join(passed)}")
        if failed:
            print(f"FAILED:  {len(failed):2d}  {', '.join(failed)}")
        if skipped:
            print(f"SKIPPED: {len(skipped):2d}  {', '.join(skipped)}")

    finally:
        dev.write("*RST")
        dev.write("POW -30")
        dev.write("OUTP:STAT OFF")
        dev.close()
