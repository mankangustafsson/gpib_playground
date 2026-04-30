from smp_common import (
    connect_smp, read_tp, query_options,
    detect_a9_variant, A9_TP_RANGES, A9_V_6301, A9_V_UNKNOWN,
    list_hw_modules, query_hw_modules, drain_err_queue, query_scalar,
    unlock_protect,
)

import argparse
import time

# Frequency list for deep checks: sub-2GHz, 1GHz steps, YIG boundary
DEEP_FREQS_MHZ = sorted(
    [10, 100, 500, 1000]
    + list(range(2000, 21000, 1000))
    + [9999, 10001]
)


class SmpTest:
    """Base class for SMP02 functional tests."""
    name = ""
    desc = ""
    option = None

    def __init__(self, dev, deep=False, installed=None):
        self.dev = dev
        self.deep = deep
        self.passed = True
        self.installed = frozenset(installed) if installed else frozenset()

    def __call__(self):
        print(f"\n=== {self.name}: {self.desc} ===")
        self.dev.write("*RST")
        time.sleep(0.5)
        self.run()
        std_passed = self.passed
        deep_passed = None
        if self.deep and self.has_deep():
            print("  --- deep checks ---")
            self.passed = True
            self.dev.write("*RST")
            time.sleep(0.5)
            self.run_deep()
            deep_passed = self.passed
        return std_passed, deep_passed

    @classmethod
    def has_deep(cls):
        return cls.run_deep is not SmpTest.run_deep

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

    def run_deep(self):
        pass


class TestA4(SmpTest):
    name = "A4"
    desc = "A4 Pulse Generator (SMP-B14)"
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
    desc = "A5 LF Generator (SM-B2, 1st)"
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


class TestA4LF(SmpTest):
    name = "A4LF"
    desc = "A4 LF Generator (SM-B2, 2nd)"
    option = "SM-B2"

    def run(self):
        self.dev.write("OUTP2:SOUR 2")
        self.dev.write("OUTP2:VOLT 4V")
        self.dev.write("SOUR2:FREQ:CW 0.2")
        self.dev.write("SOUR2:FUNC:SHAP SQU")
        time.sleep(0.5)

        n_samples = 30
        sample_interval = 0.2
        vals_1302 = []
        print("  Sampling TP1302 over one period (~6s)...")
        for _ in range(n_samples):
            vals_1302.append(self.tp(1302))
            time.sleep(sample_interval)

        min_1302, max_1302 = min(vals_1302), max(vals_1302)
        ok_1302 = min_1302 <= -0.8 and max_1302 >= 0.8
        self.check(ok_1302,
                   f"TP1302: {min_1302:+.2f}V .. {max_1302:+.2f}V"
                   f"  [-1, +1]")


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

    def run_deep(self):
        # Sweep TP203 (1 MHz ref) and TP210 (REF600 output) across a
        # range of RF frequencies and output levels to determine
        # whether the faults (TP0203 -2.5%, TP0210 = 0 V) are absolute
        # or operating-point dependent.
        freqs_mhz = [10, 100, 1000, 5000, 10000, 20000]
        levels = [0, -30, -100]
        print(f"  {'Freq (MHz)':>10s}  {'POW':>5s}  {'TP201':>7s}"
              f"  {'TP203':>7s}  {'TP207':>7s}  {'TP210':>7s}"
              f"  {'TP213':>7s}  {'TP215':>7s}")
        print("  " + "-" * 68)
        self.dev.write("OUTP:STAT ON")
        any_ref600 = False
        for f in freqs_mhz:
            self.dev.write(f"SOURCE:FREQUENCY:CW {f}MHz")
            for lv in levels:
                self.dev.write(f"POW {lv}")
                time.sleep(0.3)
                v201 = self.tp(201)
                v203 = self.tp(203)
                v207 = self.tp(207)
                v210 = self.tp(210)
                v213 = self.tp(213)
                v215 = self.tp(215)
                if v210 > 0.05:
                    any_ref600 = True
                print(f"  {f:>10d}  {lv:>5d}  {v201:>7.3f}"
                      f"  {v203:>7.3f}  {v207:>7.3f}  {v210:>7.3f}"
                      f"  {v213:>7.3f}  {v215:>7.3f}")
        self.check(any_ref600,
                   "TP210 REF600 non-zero at any (freq, level):")


class TestA8(SmpTest):
    name = "A8"
    desc = "Digital Synthesis — multi-band spot + DDS fine-tune sweep"

    def run(self):
        # (1) Manual test condition per band-1 p.359 §7.4: FREQ = 1 GHz.
        #     TP305 12-20V, TP303 0.5-1.5V, TP304 0.05-0.2V.
        print("  --- 1 GHz spot (band-1 p.359 test condition) ---")
        self.dev.write("SOURCE:FREQUENCY:CW 1GHz")
        time.sleep(0.5)
        v305 = self.tp(305)
        v303 = self.tp(303)
        v304 = self.tp(304)
        print(f"  TP305={v305:+6.2f}V [12.00, 20.00]   "
              f"TP303={v303:+5.2f}V [0.50, 1.50]   "
              f"TP304={v304:+5.2f}V [0.05, 0.20]")
        self.check(12.0 <= v305 <= 20.0, "TP305 @ 1 GHz in [12, 20] V: ")
        self.check(0.5 <= v303 <= 1.5, "TP303 @ 1 GHz in [0.5, 1.5] V:")
        self.check(0.05 <= v304 <= 0.2, "TP304 @ 1 GHz in [0.05, 0.2] V:")

        # (2) Cross-band DDS locking: TP303/TP304 should be in spec at every
        #     YFO band. TP305 is strongly frequency-dependent so only logged.
        print("  --- cross-band TP303/304 spot (DDS health vs YFO band) ---")
        for freq_ghz in (2.0, 10.0, 20.0):
            self.dev.write(f"SOURCE:FREQUENCY:CW {freq_ghz}GHz")
            time.sleep(0.5)
            v305 = self.tp(305)
            v303 = self.tp(303)
            v304 = self.tp(304)
            print(f"  {freq_ghz:>4.1f} GHz   "
                  f"TP305={v305:+6.2f}V (info)   "
                  f"TP303={v303:+5.2f}V [0.50, 1.50]   "
                  f"TP304={v304:+5.2f}V [0.05, 0.20]")
            self.check(0.5 <= v303 <= 1.5,
                       f"TP303 @ {freq_ghz:>4.1f} GHz in [0.5, 1.5] V:")
            self.check(0.05 <= v304 <= 0.2,
                       f"TP304 @ {freq_ghz:>4.1f} GHz in [0.05, 0.2] V:")

        # (3) Fine DDS-DAC walk at 20 GHz — exercises TP305 across its full
        #     0.4..20V tuning range in 21 steps and verifies monotonicity.
        print("  --- 20 GHz DDS fine-tune walk (TP305 DAC sweep) ---")
        f_start = 19.9887543625e9
        f_stop = 19.9939783783e9
        n_steps = 21
        step = (f_stop - f_start) / (n_steps - 1)

        prev_305 = None
        monotonic = True

        print(f"  {'Freq (GHz)':>16s}  {'TP305':>8s}  {'305 mono':>8s}")
        print("  " + "-" * 38)

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
            print(f"  {freq/1e9:16.10f}  {v305:8.2f}  {mono_str:>8s}")

        print()
        self.check(monotonic, "TP305 monotonic increase:")


class TestA9(SmpTest):
    name = "A9"
    desc = "ALC Amplifier — ASK modulation test"

    def __init__(self, dev, deep=False, installed=None):
        super().__init__(dev, deep, installed=installed)
        self.variant = None

    def run(self):
        self.variant = detect_a9_variant(self.dev, verbose=True)
        self.dev.write("*RST")
        time.sleep(0.3)
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

    def _check_tp(self, tp, value, short):
        """Variant-aware bounds check for an A9 diagnostic point."""
        key = self.variant if self.variant in A9_TP_RANGES else A9_V_6301
        lo, hi, desc = A9_TP_RANGES[key][tp]
        self.check(lo <= value <= hi,
                   f"TP{tp} {short}: {value:+.3f}V  [{lo}, {hi}]  ({desc})")

    def run_deep(self):
        # Reference outputs / collector voltages (variant-dependent)
        v1610 = self.tp(1610)
        self._check_tp(1610, v1610, "x93")
        v1611 = self.tp(1611)
        self._check_tp(1611, v1611, "x95")

        # LF generator toggle — requires SM-B2 (LF Generator option).
        # The SOUR2 / :AM:INT2 path drives the AM modulator from the
        # second internal LF source; without SM-B2 each write raises
        # -241 "Hardware missing" and TP1615 is stuck near 0 V.
        if "SM-B2" in self.installed:
            self.dev.write("SOUR2:FREQ:CW 1000")
            self.dev.write("SOUR2:FUNC:SHAP SIN")
            self.dev.write("SOUR:AM:INT2:FREQ 1000")
            self.dev.write("SOUR:AM:STAT ON")
            time.sleep(0.3)
            v1615 = self.tp(1615)
            self.check(0.39 <= v1615 <= 0.42,
                       f"TP1615 LF gen (on):    {v1615:+.3f}V"
                       f"  [0.39, 0.42]")
            self.dev.write("SOUR:AM:STAT OFF")
            time.sleep(0.3)
            v1615 = self.tp(1615)
            self.check(-0.02 <= v1615 <= 0.02,
                       f"TP1615 LF gen (off):   {v1615:+.3f}V"
                       f"  [≈0]")
        else:
            print("  TP1615 LF gen test: SKIPPED — requires SM-B2"
                  " (not installed)")

        # AM depth DAC — with AM on
        self.dev.write("SOUR:AM:STAT ON")
        time.sleep(0.3)
        v1603 = self.tp(1603)
        self.check(-1.01 <= v1603 <= 0.0,
                   f"TP1603 AM DAC (AM on): {v1603:+.2f}V"
                   f"  [-1.01, 0]")
        self.dev.write("SOUR:AM:STAT OFF")

        # AM adder — narrow range with AM off (variant-dependent)
        time.sleep(0.3)
        v1604 = self.tp(1604)
        self._check_tp(1604, v1604, "AM adder (off)")

        # FM deviation DAC — sweep deviation values and check the
        # full-deviation reading against spec. The SMP routes low and
        # high deviations through different DAC paths; intermediate
        # values can land in either sign at TP1605, so only the
        # 1 MHz "full deviation" reading is checked against the
        # service-manual window. Other readings are reported for
        # informational use.
        self.dev.write("SOUR:FM:STAT OFF")
        time.sleep(0.3)
        v_off = self.tp(1605)

        self.dev.write("SOUR:FM:DEV 0")
        self.dev.write("SOUR:FM:STAT ON")
        time.sleep(0.3)
        v_d0 = self.tp(1605)

        self.dev.write("SOUR:FM:DEV 100E3")
        time.sleep(0.3)
        v_d100k = self.tp(1605)

        self.dev.write("SOUR:FM:DEV 1E6")
        time.sleep(0.3)
        v_d1m = self.tp(1605)

        self.dev.write("SOUR:FM:STAT OFF")

        print(f"  TP1605 FM DAC sweep:")
        print(f"    FM off            : {v_off:+.3f}V")
        print(f"    FM on, dev 0 Hz   : {v_d0:+.3f}V")
        print(f"    FM on, dev 100kHz : {v_d100k:+.3f}V (info)")
        print(f"    FM on, dev 1 MHz  : {v_d1m:+.3f}V")

        responsive = abs(v_d1m - v_d0) > 0.05
        in_window = 0.0 <= v_d1m <= 2.5

        self.check(responsive,
                   f"TP1605 responds to deviation:"
                   f" delta(0->1MHz)={v_d1m - v_d0:+.3f}V")
        self.check(in_window,
                   f"TP1605 @ 1MHz dev:"
                   f" {v_d1m:+.3f}V  [0, 2.5]")

        # Diff amp offset and main loop across frequency range
        self.dev.write("OUTP:STAT ON")
        for freq_mhz in DEEP_FREQS_MHZ:
            freq_label = f"{freq_mhz/1000:.3f}GHz"
            self.dev.write(
                f"SOURCE:FREQUENCY:CW {freq_mhz}MHz")
            time.sleep(0.3)

            v1612 = self.tp(1612)
            self.check(-0.04 <= v1612 <= 0.04,
                       f"TP1612 @ {freq_label}:"
                       f"  {v1612:+.3f}V  [-0.04, 0.04]")

            self.dev.write("POW -140")
            time.sleep(0.3)
            v1613 = self.tp(1613)
            self.check(-5.5 <= v1613 <= -4.5,
                       f"TP1613 min @ {freq_label}:"
                       f"  {v1613:+.2f}V  [≈-5]")

            self.dev.write("POW 22")
            time.sleep(0.3)
            v1613 = self.tp(1613)
            self.check(0.3 <= v1613 <= 1.0,
                       f"TP1613 max @ {freq_label}:"
                       f"  {v1613:+.2f}V  [≈0.7]")


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

    def run_deep(self):
        # Per band-2 §7.4.2 (p.163 EN / p.143 DE) the YFO pretune
        # follows v(TP1802) = f/20GHz * U1, U1 = 8..12V at 20 GHz
        # (positive, depends on R56). v(TP1805) = f/20GHz * U2,
        # U2 = -(3.7..5.7V) at 20 GHz. The manual states: "The
        # voltages measured at 20GHz serve as reference values for
        # further measurements." — the exp1802/exp1805 columns use
        # U1/U2 window midpoints for live progress; final pass/fail
        # checks use TP1802/TP1805 at 20 GHz as the self-calibrated
        # reference and evaluate each YFO frequency against the
        # per-f window [f/20·lo, f/20·hi]. TP1800 (local -10V from
        # N1) is a separate reference for the loop driver, checked
        # on its own. TP1807/TP1809/TP1811 rail whenever A21's
        # sampling-IF is absent (cascade), so they are logged but
        # not the A10-internal verdict.
        U1_NOM = 10.0
        U2_NOM = -4.7

        print(f"{'Freq':>10s}"
              f"  {'TP1800':>7s}  {'TP1802':>7s}  {'exp1802':>8s}"
              f"  {'TP1804':>7s}  {'TP1805':>7s}  {'exp1805':>8s}"
              f"  {'TP1807':>7s}  {'TP1809':>7s}  {'TP1811':>7s}"
              f"  {'TP1812':>7s}")
        print("-" * 117)

        rows = []
        for freq_mhz in DEEP_FREQS_MHZ:
            freq_label = f"{freq_mhz/1000:.3f}GHz"
            self.dev.write(
                f"SOURCE:FREQUENCY:CW {freq_mhz}MHz")
            time.sleep(0.3)

            v1800 = self.tp(1800)
            v1802 = self.tp(1802)
            v1804 = self.tp(1804)
            v1805 = self.tp(1805)
            v1807 = self.tp(1807)
            v1809 = self.tp(1809)
            v1811 = self.tp(1811)
            v1812 = self.tp(1812)

            scale = freq_mhz / 20000.0
            in_yfo = 2000 <= freq_mhz <= 20000
            if in_yfo:
                e1802_str = f"{scale * U1_NOM:+8.2f}"
                e1805_str = f"{scale * U2_NOM:+8.2f}"
            else:
                e1802_str = "     n/a"
                e1805_str = "     n/a"

            print(f"{freq_label:>10s}"
                  f"  {v1800:+7.3f}  {v1802:+7.2f}  {e1802_str}"
                  f"  {v1804:+7.2f}  {v1805:+7.2f}  {e1805_str}"
                  f"  {v1807:+7.2f}  {v1809:+7.2f}  {v1811:+7.2f}"
                  f"  {v1812:+7.2f}",
                  flush=True)

            rows.append((freq_mhz, freq_label, v1800, v1802, v1804,
                         v1805, v1807, v1809, v1811, v1812))

        row_20g = next((r for r in rows if r[0] == 20000), None)
        u1_ref = row_20g[3] if row_20g is not None else None
        u2_ref = row_20g[5] if row_20g is not None else None

        print()

        # TP1800 reference integrity (A10-internal).
        v1800s = [r[2] for r in rows]
        v1800_min, v1800_max = min(v1800s), max(v1800s)
        v1800_span = v1800_max - v1800_min
        self.check(-10.02 <= v1800_min and v1800_max <= -9.98,
                   f"TP1800 neg reference: "
                   f"{v1800_min:+.3f}..{v1800_max:+.3f}V"
                   f"  [-10.02, -9.98]")
        self.check(v1800_span < 0.05,
                   f"TP1800 stability: {v1800_span*1000:.1f}mV span"
                   f"  (<50mV)")

        # TP1802 pretune DAC — spec U1 = 8..12V at 20 GHz, scaling
        # linearly f/20GHz across 2..20 GHz (band-2 §7.4.2 HzTest).
        yfo_rows = [r for r in rows if 2000 <= r[0] <= 20000]
        v1802_yfo = [r[3] for r in yfo_rows]
        v1802_span = max(v1802_yfo) - min(v1802_yfo)
        self.check(v1802_span > 1.0,
                   f"TP1802 DAC alive: span(2-20GHz) = {v1802_span:.2f}V"
                   f"  (>1V)")
        if u1_ref is not None:
            self.check(8.0 <= u1_ref <= 12.0,
                       f"TP1802 U1 @20GHz: {u1_ref:+.2f}V"
                       f"  [+8.00, +12.00]")
            worst_dev = 0.0
            worst_label = ""
            for r in yfo_rows:
                fm, label, _, v1802, *_ = r
                scale = fm / 20000.0
                lo, hi = scale * 8.0, scale * 12.0
                d = max(0.0, lo - v1802, v1802 - hi)
                if d > worst_dev:
                    worst_dev, worst_label = d, label
            if worst_dev == 0.0:
                self.check(True,
                           f"TP1802 scaling: all {len(yfo_rows)} pts"
                           f" in [f/20·8, f/20·12] V")
            else:
                self.check(False,
                           f"TP1802 scaling: worst {worst_dev:+.3f}V"
                           f" out of [f/20·8, f/20·12] V"
                           f"  @ {worst_label}")

        # TP1805 main tuning current — spec U2 = -(3.7..5.7V) at
        # 20 GHz, scaling f/20GHz (band-2 §7.4.2 HzTest).
        if u2_ref is not None:
            self.check(-5.7 <= u2_ref <= -3.7,
                       f"TP1805 U2 @20GHz: {u2_ref:+.2f}V"
                       f"  [-5.70, -3.70]")
            worst_dev = 0.0
            worst_label = ""
            for r in yfo_rows:
                fm, label, _, _, _, v1805, *_ = r
                scale = fm / 20000.0
                lo, hi = scale * -5.7, scale * -3.7
                d = max(0.0, lo - v1805, v1805 - hi)
                if d > worst_dev:
                    worst_dev, worst_label = d, label
            if worst_dev == 0.0:
                self.check(True,
                           f"TP1805 scaling: all {len(yfo_rows)} pts"
                           f" in [f/20·-5.7, f/20·-3.7] V")
            else:
                self.check(False,
                           f"TP1805 scaling: worst {worst_dev:+.3f}V"
                           f" out of [f/20·-5.7, f/20·-3.7] V"
                           f"  @ {worst_label}")

        # TP1807 cascade flag (from A21 sampling-IF fault, smp_diag §2).
        v1807s = [r[6] for r in rows]
        railed = sum(1 for v in v1807s if abs(v) > 12.0)
        if railed:
            print(f"  TP1807 railed at {railed}/{len(v1807s)} freqs"
                  f" (|v|>12V) — cascade from A21, see smp_diag.md §2")


class TestA21(SmpTest):
    name = "A21"
    desc = "Sampling Module — comb-gen diag via W216"

    def run(self):
        # A21 has no digital interface (band-3 §7.6, p.147). Two
        # A21-sourced voltages are routed to A26's MUX via cable W216
        # (band-3 p.148 FSTEP pinout):
        #   W216.9  VARSAMP  -> TP1902  0.9..1.1V   (model ID)
        #   W216.10 DIAGSAMP -> TP1910  7.5..11V    (comb-gen diag)
        # Two-witness differential diagnosis:
        #   alive OK + chain OK   -> A21 healthy
        #   alive OK + chain FAIL -> fault isolated to A21 doubler /
        #                            comb / diag-rectifier chain or to
        #                            the W216.10 conductor. Power,
        #                            ground, and cable-wide integrity
        #                            are exonerated because VARSAMP
        #                            needs the same supplies (W216.1
        #                            +15V, W216.4 +7.5V, W216.5 -15V).
        #   alive FAIL + chain FAIL -> suspect W216 supplies / ground
        #                              / cable-wide. Do not probe
        #                              board electronics until power
        #                              is confirmed.
        #   alive FAIL + chain OK -> unusual; suspect W216.9 conductor
        #                            specifically.
        v1902 = self.tp(1902)
        v1910 = self.tp(1910)

        alive = 0.9 <= v1902 <= 1.1
        chain = 7.5 <= v1910 <= 11.0
        self.check(alive,
                   f"TP1902 VARSAMP: {v1902:+.2f}V  [0.9, 1.1]"
                   f"  (A21 alive witness via W216.9)")
        self.check(chain,
                   f"TP1910 DIAGSAMP: {v1910:+.2f}V  [7.5, 11.0]"
                   f"  (comb-gen health via W216.10)")

        if alive and not chain:
            print("  => A21 is powered and grounded correctly; the"
                  " comb-generator")
            print("     diagnostic is dead. Localize to the"
                  " doubler/comb/diag-rectifier")
            print("     chain on A21 or the W216.10 conductor."
                  " Power & cable-wide")
            print("     exonerated. See smp_diag.md §2 worksheet.")
        elif not alive and not chain:
            print("  => Both A21 witnesses dead. Suspect W216"
                  " supplies (pins 1/4/5),")
            print("     ground (pins 2/3/6/7/8), or the whole cable."
                  " Do not probe")
            print("     board electronics until power is confirmed.")
        elif not alive and chain:
            print("  => Unusual: chain live but alive-witness dead."
                  " Suspect W216.9")
            print("     conductor specifically.")

    def run_deep(self):
        # Sweep freq to confirm both witnesses are frequency-flat.
        # VARSAMP is a static model-ID voltage; DIAGSAMP rectifies the
        # comb-generator amplitude, which is essentially constant
        # because A7 step synthesis holds x50 at 103..117 MHz at
        # roughly constant amplitude for all output frequencies (the
        # YIG beat must stay in the 10.3..15.6 MHz IF band — band-1
        # §6.1.10, p.92). Large freq-dependent variation on either
        # would contradict the static-fault hypothesis.
        print(f"{'Freq':>10s}  {'TP1902':>7s}  {'TP1910':>7s}"
              f"  {'alive':>6s}  {'chain':>6s}")
        print("-" * 46)
        rows = []
        for fm in DEEP_FREQS_MHZ:
            label = f"{fm/1000:.3f}GHz"
            self.dev.write(f"SOURCE:FREQUENCY:CW {fm}MHz")
            time.sleep(0.3)
            v1902 = self.tp(1902)
            v1910 = self.tp(1910)
            ws = "OK" if 0.9 <= v1902 <= 1.1 else "FAIL"
            cs = "OK" if 7.5 <= v1910 <= 11.0 else "FAIL"
            print(f"{label:>10s}  {v1902:+7.3f}  {v1910:+7.3f}"
                  f"  {ws:>6s}  {cs:>6s}", flush=True)
            rows.append((fm, v1902, v1910))

        print()
        v1902s = [r[1] for r in rows]
        v1910s = [r[2] for r in rows]
        v1902_span = max(v1902s) - min(v1902s)
        v1910_span = max(v1910s) - min(v1910s)
        w_ok = all(0.9 <= v <= 1.1 for v in v1902s)
        c_ok = all(7.5 <= v <= 11.0 for v in v1910s)
        self.check(w_ok,
                   f"TP1902 in-spec at all {len(rows)} freqs"
                   f"  (min {min(v1902s):+.2f}, max {max(v1902s):+.2f})")
        self.check(c_ok,
                   f"TP1910 in-spec at all {len(rows)} freqs"
                   f"  (min {min(v1910s):+.2f}, max {max(v1910s):+.2f})")
        self.check(v1902_span < 0.05,
                   f"TP1902 stability: {v1902_span*1000:.0f}mV span"
                   f"  (<50mV, model-ID is static)")
        self.check(v1910_span < 0.5,
                   f"TP1910 stability: {v1910_span*1000:.0f}mV span"
                   f"  (<500mV, comb amplitude is freq-flat)")


class TestA26(SmpTest):
    name = "A26"
    desc = "Microwave Interface — sampling signal"

    def run(self):
        # TP1910 is A21-sourced (W216.10); the full A21 differential
        # diagnosis including the VARSAMP witness lives in TestA21.
        # This check verifies the value reaches A26's MUX correctly.
        v1910 = self.tp(1910)
        self.check(v1910 > 8.0,
                   f"TP1910={v1910:.2f}V  (>8V)")

    def run_deep(self):
        for freq_mhz in DEEP_FREQS_MHZ:
            freq_label = f"{freq_mhz/1000:.3f}GHz"
            self.dev.write(
                f"SOURCE:FREQUENCY:CW {freq_mhz}MHz")
            time.sleep(0.3)
            v1910 = self.tp(1910)
            self.check(v1910 > 8.0,
                       f"TP1910 @ {freq_label}:"
                       f"  {v1910:.2f}V  (>8V)")


# ---------------------------------------------------------------------------
# Standalone diagnostic actions (no module tests, SCPI-only)
# ---------------------------------------------------------------------------

def _header(title):
    print(f"\n=== {title} ===")


def _print_err_queue(errors):
    if not errors:
        print("  :SYST:ERR? queue empty (no errors)")
        return
    print(f"  :SYST:ERR? drained {len(errors)} entries:")
    for e in errors:
        print(f"    {e}")


def action_sys_info(dev):
    _header("Instrument information")
    print(f"  *IDN?             {query_scalar(dev, '*IDN?')}")
    print(f"  *OPT?             {query_scalar(dev, '*OPT?')}")
    print(f"  :DIAG:INFO:OTIM?  {query_scalar(dev, ':DIAG:INFO:OTIM?')}")
    print(f"  :DIAG:INFO:CCOUNT? {query_scalar(dev, ':DIAG:INFO:CCOUNT?')}")
    print(f"  :CAL:STAT?        {query_scalar(dev, ':CAL:STAT?')}")
    _header("Hardware modules (:DIAG:INFO:MOD?)")
    try:
        list_hw_modules(dev)
    except Exception as exc:
        print(f"  (query failed: {exc})")
    _header("Error queue")
    _print_err_queue(drain_err_queue(dev))


def action_scan_modules(dev):
    _header(":DIAG:INFO:MOD? raw")
    raw = query_scalar(dev, ":DIAG:INFO:MOD?")
    print(f"  {raw}")
    _header("Parsed modules")
    hw = query_hw_modules(dev)
    if not hw:
        print("  (none parsed)")
    else:
        for name, (var, rev) in hw.items():
            print(f"  {name:8s}  {var}  {rev}")


def action_self_test(dev):
    # SMP operating manual p.207 §3.6.15 documents the :TEST: system.
    # *TST? is the IEEE-488.2 stub and returns 0 on this firmware
    # without running anything; the real self-tests are the three
    # query-only commands :TEST:RAM?, :TEST:ROM?, :TEST:BATTery?.
    # All return "0" on pass, non-zero on fail. The :TEST:DIRect:*
    # subtree is explicitly flagged "service purposes only, improper
    # use may damage the module" and is not invoked here.
    # Also snapshot the SCPI status-register conditions before and
    # after so steady-state hardware flags (UNLOCK, OVERRANGE,
    # MODULATION_OVERLOAD, ...) are captured even if *TST? is silent.
    def _q(label, cmd, fmt=str):
        try:
            reply = dev.query(cmd).strip()
        except Exception as exc:
            print(f"  {label:28s} {cmd:20s}  ERROR: {exc}")
            return None
        try:
            val = fmt(reply)
        except ValueError:
            val = reply
        if isinstance(val, int):
            verdict = "OK" if val == 0 else f"FAIL (code {val})"
            print(f"  {label:28s} {cmd:20s}  -> {val}   {verdict}")
        else:
            print(f"  {label:28s} {cmd:20s}  -> {val}")
        return val

    _header("Status register snapshot (pre-test)")
    _q("Questionable condition", ":STAT:QUES:COND?", int)
    _q("Operable condition",     ":STAT:OPER:COND?", int)
    _q("Event status register",  "*ESR?",             int)
    _q("Status byte",            "*STB?",             int)

    _header("Pre-test error queue drain")
    _print_err_queue(drain_err_queue(dev))

    _header("*TST? (IEEE-488.2 stub)")
    t0 = time.time()
    try:
        reply = dev.query("*TST?").strip()
        dt = time.time() - t0
        val = int(reply)
        verdict = "OK" if val == 0 else f"FAIL (code {val})"
        print(f"  *TST?                                             "
              f" -> {val}   {verdict}   ({dt*1000:.0f}ms)")
        if dt < 0.1:
            print("  note: sub-100ms reply indicates stub — use"
                  " :TEST:RAM?/:ROM?/:BATTery? below for real tests.")
    except Exception as exc:
        print(f"  *TST? failed: {exc}")

    _header(":TEST: hardware self-tests (p.207 §3.6.15)")
    t0 = time.time()
    _q("RAM integrity",     ":TEST:RAM?",     int)
    _q("ROM integrity",     ":TEST:ROM?",     int)
    _q("NVRAM backup batt", ":TEST:BATT?",    int)
    dt = time.time() - t0
    print(f"  (total {dt*1000:.0f}ms)")

    _header("Status register snapshot (post-test)")
    _q("Questionable condition", ":STAT:QUES:COND?", int)
    _q("Operable condition",     ":STAT:OPER:COND?", int)
    _q("Event status register",  "*ESR?",             int)
    _q("Status byte",            "*STB?",             int)

    _header("Post-test error queue")
    _print_err_queue(drain_err_queue(dev))


def action_alc_off_a9(dev):
    """Compare A9 TPs with ALC loop closed vs open at 10 GHz, POW 0."""
    _header("A9 rail check: ALC loop closed vs open (10 GHz, 0 dBm)")
    dev.write("*RST")
    time.sleep(0.5)
    dev.write("SOURCE:FREQUENCY:CW 10GHz")
    dev.write("POW 0")
    dev.write("OUTP:STAT ON")
    dev.write("SOUR:POW:ALC:STAT ON")
    time.sleep(0.5)
    tps = [1609, 1610, 1611, 1612, 1613]
    closed = {tp: read_tp(dev, tp) for tp in tps}
    dev.write("SOUR:POW:ALC:STAT OFF")
    time.sleep(0.5)
    opened = {tp: read_tp(dev, tp) for tp in tps}
    dev.write("SOUR:POW:ALC:STAT ON")
    print(f"  {'TP':>6s}  {'ALC on':>10s}  {'ALC off':>10s}  {'delta':>10s}")
    print("  " + "-" * 42)
    for tp in tps:
        d = opened[tp] - closed[tp]
        print(f"  {tp:>6d}  {closed[tp]:+10.3f}  "
              f"{opened[tp]:+10.3f}  {d:+10.3f}")
    print("  interpretation: large delta at TP1612/TP1613 means the rails"
          " were driven by the open loop; small delta with both still"
          " railed means a hardware fault on the diff-amp/main-loop side.")


def action_ref_source(dev):
    """Read A7 TPs with ROSC INT then EXT."""
    _header("A7 reference-source comparison")
    tps = [201, 203, 204, 206, 207, 210, 213, 215]
    results = {}
    for src in ("INT", "EXT"):
        dev.write("*RST")
        time.sleep(0.3)
        dev.write(f":SOUR:ROSC:SOUR {src}")
        time.sleep(0.5)
        results[src] = {tp: read_tp(dev, tp) for tp in tps}
    print(f"  {'TP':>6s}  {'INT':>10s}  {'EXT':>10s}  {'delta':>10s}")
    print("  " + "-" * 42)
    for tp in tps:
        d = results["EXT"][tp] - results["INT"][tp]
        print(f"  {tp:>6d}  {results['INT'][tp]:+10.3f}"
              f"  {results['EXT'][tp]:+10.3f}  {d:+10.3f}")
    _header("Error queue after ROSC toggling")
    _print_err_queue(drain_err_queue(dev))


def action_att_sweep(dev):
    """Sweep output level and manual attenuator positions, polling TP1914."""
    _header("ATT27 ribbon connector: level sweep polling TP1914")
    dev.write("*RST")
    time.sleep(0.3)
    dev.write("SOURCE:FREQUENCY:CW 10GHz")
    dev.write(":SOUR:POW:ATT:AUTO ON")
    dev.write("OUTP:STAT ON")
    levels = [10, 0, -10, -20, -30, -40, -60, -80, -100, -120, -140]
    print(f"  AUTO attenuator; sweep POW, read TP1914 each step")
    print(f"  {'POW (dBm)':>10s}  {'TP1914':>8s}  {'status':>8s}")
    print("  " + "-" * 32)
    for lv in levels:
        dev.write(f"POW {lv}")
        time.sleep(0.4)
        v = read_tp(dev, 1914)
        ok = "OK" if 0.5 <= v <= 1.5 else "FAIL"
        print(f"  {lv:>10d}  {v:>8.3f}  {ok:>8s}")
    _header("ATT27: manual attenuator positions")
    dev.write(":SOUR:POW:ATT:AUTO OFF")
    dev.write("POW 0")
    time.sleep(0.3)
    print(f"  {'ATT (dB)':>10s}  {'TP1914':>8s}  {'status':>8s}")
    print("  " + "-" * 32)
    for att in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 110]:
        try:
            dev.write(f":OUTP:ATT {att}")
        except Exception:
            pass
        time.sleep(0.4)
        v = read_tp(dev, 1914)
        ok = "OK" if 0.5 <= v <= 1.5 else "FAIL"
        print(f"  {att:>10d}  {v:>8.3f}  {ok:>8s}")
    dev.write(":SOUR:POW:ATT:AUTO ON")
    _header("Error queue after attenuator sweep")
    _print_err_queue(drain_err_queue(dev))


# SMP-B15 ATT27 switch-over table (band-3 §7.4.3, p.63 — SMP02 + SMP-B15).
# Each row: (POW setpoint dBm inside that 10-dB level band, per-section
# state, total attenuation dB). Sections in order: 10 dB, 20 dB, 40 dB A,
# 40 dB B. T = THRU (section bypassed), A = ATT (section engaged).
ATT27_BANDS = [
    ( 10,  "TTTT",   0),
    ( -5,  "ATTT",  10),
    (-15,  "TATT",  20),
    (-25,  "AATT",  30),
    (-35,  "TTTA",  40),
    (-45,  "ATTA",  50),
    (-55,  "TATA",  60),
    (-65,  "AATA",  70),
    (-75,  "TTAA",  80),
    (-85,  "ATAA",  90),
    (-95,  "TAAA", 100),
    (-110, "AAAA", 110),
]
ATT27_SECTIONS = ("10", "20", "40A", "40B")


def _att_toggles(prev, curr):
    """Section names whose state differs between consecutive bands."""
    if prev is None:
        return ()
    return tuple(name for name, p, c in zip(ATT27_SECTIONS, prev, curr)
                 if p != c)


def action_att_exercise(dev, cycles=20):
    """Cycle POW through every ATT27 band, polling TP1914 each step.

    One cycle walks all 12 level bands from 0 dB attenuation down to 110 dB
    and back up, so every one of the four physical sections (10, 20, 40A,
    40B) toggles at least once per direction. For each step the sections
    that should have just switched are printed alongside the new per-section
    state, so a stuck section can be identified by comparing audible relay
    clicks to the printed toggle pattern.
    """
    _header(f"ATT27 mechanical exercise: {cycles} POW down-up cycles"
            f" across 12 bands")
    print("  sections: 10=10dB  20=20dB  40A=40dB-A  40B=40dB-B"
          "   state: T=THRU (bypass)  A=ATT (engaged)")
    dev.write("*RST")
    time.sleep(0.3)
    dev.write("SOURCE:FREQUENCY:CW 10GHz")
    dev.write("OUTP:STAT ON")
    time.sleep(0.3)

    # Walk 0..110 dB then back 100..0 dB (skip duplicated 110 dB endpoint).
    sequence = list(ATT27_BANDS) + list(reversed(ATT27_BANDS[:-1]))
    down_len = len(ATT27_BANDS)

    header = (f"  {'cyc':>3s} {'dir':>3s} "
              f"{'POW':>5s} {'Att':>3s}  "
              f"{'10':>2s} {'20':>2s} {'40A':>3s} {'40B':>3s}  "
              f"{'toggle':<10s} "
              f"{'TP1914':>7s} {'id':>4s}")
    print(header)
    print("  " + "-" * (len(header) - 2))

    ok_count = {att: 0 for _, _, att in ATT27_BANDS}
    total_count = {att: 0 for _, _, att in ATT27_BANDS}
    prev_state = None

    for c in range(1, cycles + 1):
        for i, (lv, states, att_db) in enumerate(sequence):
            direction = "dn" if i < down_len else "up"
            dev.write(f"POW {lv}")
            time.sleep(0.25)
            v = read_tp(dev, 1914)
            toggles = _att_toggles(prev_state, states)
            tog_str = ",".join(toggles) if toggles else "-"
            ok = 0.5 <= v <= 1.5
            total_count[att_db] += 1
            if ok:
                ok_count[att_db] += 1
            print(f"  {c:>3d} {direction:>3s} "
                  f"{lv:>+5d} {att_db:>3d}  "
                  f"{states[0]:>2s} {states[1]:>2s} {states[2]:>3s}"
                  f" {states[3]:>3s}  "
                  f"{tog_str:<10s} "
                  f"{v:>7.3f} {'OK' if ok else 'FAIL':>4s}")
            prev_state = states
        prev_state = None

    _header("Per-band TP1914 pass rate")
    print(f"  {'Att (dB)':>8s}  {'OK / tot':>10s}  {'rate':>6s}")
    print("  " + "-" * 32)
    for _, _, att_db in ATT27_BANDS:
        ok = ok_count[att_db]
        tot = total_count[att_db]
        rate = ok / tot if tot else 0
        print(f"  {att_db:>8d}  {ok:>4d} / {tot:<3d}  {rate*100:>5.0f}%")
    _header("Error queue after exercise")
    _print_err_queue(drain_err_queue(dev))


def action_att_40_exercise(dev, cycles=20):
    """Walk the ATT27 through 0 / 40 / 80 dB, isolating 40 dB toggles.

    The three level bands 0 dB (POW +10, state TTTT), 40 dB (POW -35,
    state TTTA) and 80 dB (POW -75, state TTAA) all share 10=THRU and
    20=THRU. Stepping between adjacent members of this triplet toggles
    exactly one 40 dB section:

      0 dB  →  40 dB  : 40 B engages  (TTTT → TTTA)
     40 dB  →  80 dB  : 40 A engages  (TTTA → TTAA)
     80 dB  →  40 dB  : 40 A releases (TTAA → TTTA)
     40 dB  →   0 dB  : 40 B releases (TTTA → TTTT)

    Per cycle the sequence 0 → 40 → 80 → 40 gives one 40 B engage,
    one 40 A engage, and one 40 A release; the 40 B release happens
    on the wraparound into the next cycle. Over N cycles: 2N 40 B
    and 2N 40 A clicks total, with no 10 dB or 20 dB relay activity.
    """
    _header(f"ATT27 isolated 40 dB exercise: {cycles} cycles"
            f" (0 → 40 → 80 → 40 dB)")
    print("  sections: 10=10dB  20=20dB  40A=40dB-A  40B=40dB-B"
          "   state: T=THRU (bypass)  A=ATT (engaged)")
    dev.write("*RST")
    time.sleep(0.3)
    dev.write("SOURCE:FREQUENCY:CW 10GHz")
    dev.write("OUTP:STAT ON")
    time.sleep(0.3)

    s0 = ( 10, "TTTT",  0)
    s1 = (-35, "TTTA", 40)
    s2 = (-75, "TTAA", 80)
    sequence = [s0, s1, s2, s1]

    header = (f"  {'cyc':>3s} {'POW':>5s} {'Att':>3s}  "
              f"{'10':>2s} {'20':>2s} {'40A':>3s} {'40B':>3s}  "
              f"{'toggle':<6s} "
              f"{'TP1914':>7s} {'id':>4s}")
    print(header)
    print("  " + "-" * (len(header) - 2))

    ok_count = {att: 0 for _, _, att in (s0, s1, s2)}
    total_count = {att: 0 for _, _, att in (s0, s1, s2)}
    prev_state = None

    for c in range(1, cycles + 1):
        for lv, states, att_db in sequence:
            dev.write(f"POW {lv}")
            time.sleep(0.25)
            v = read_tp(dev, 1914)
            toggles = _att_toggles(prev_state, states)
            tog_str = ",".join(toggles) if toggles else "-"
            ok = 0.5 <= v <= 1.5
            total_count[att_db] += 1
            if ok:
                ok_count[att_db] += 1
            print(f"  {c:>3d} {lv:>+5d} {att_db:>3d}  "
                  f"{states[0]:>2s} {states[1]:>2s} {states[2]:>3s}"
                  f" {states[3]:>3s}  "
                  f"{tog_str:<6s} "
                  f"{v:>7.3f} {'OK' if ok else 'FAIL':>4s}")
            prev_state = states

    _header("Per-state TP1914 pass rate")
    print(f"  {'Att (dB)':>8s}  {'OK / tot':>10s}  {'rate':>6s}")
    print("  " + "-" * 32)
    for _, _, att_db in (s0, s1, s2):
        ok = ok_count[att_db]
        tot = total_count[att_db]
        rate = ok / tot if tot else 0
        print(f"  {att_db:>8d}  {ok:>4d} / {tot:<3d}  {rate*100:>5.0f}%")
    _header("Error queue after 40 dB exercise")
    _print_err_queue(drain_err_queue(dev))


def action_a21_probe(dev):
    """Live SCPI witnesses while physically probing A21 with scope/DMM.

    Parks SMP at 3 GHz CW, POW -30 dBm, output ON, then loops reading
    TP1902 / TP1910 / TP1915 once per second. Intended to run with the
    instrument cover off and a scope/DMM on A21 connectors x21, x50,
    x75, x95, x96. Ctrl-C to exit; a final *RST / OUTP OFF is issued
    by the outer try/finally.
    """
    _header("A21 live probe — 3 GHz CW, POW -30, OUTP ON")
    dev.write("*RST")
    time.sleep(0.3)
    dev.write("SOURCE:FREQUENCY:CW 3GHz")
    dev.write("POW -30")
    dev.write("OUTP:STAT ON")
    time.sleep(0.3)

    print()
    print("  Physical probe reference (band-3 §7.1/§7.4, p.144-148):")
    print("    W216.1   +15V supply       +14.75..+15.25V  (from A26)")
    print("    W216.4   +7.5V supply      +7.25..+7.75V    (from A26)")
    print("    W216.5   -15V supply       -15.25..-14.75V  (from A26)")
    print("    x50      FSTEP-IN          103..117MHz  +4..+6dBm"
          " (from A7)")
    print("    x21      LO out (doubled)  206..234MHz  +26..+30dBm")
    print("    x216     comb LO to mixer  2..20GHz")
    print("    x211     YIG RF-IN         2..20GHz     0..+7dBm"
          " (from A20)")
    print("    x75      IF-OUT            10..80MHz    -5..+15dBm"
          " (to A10)")
    print("    x95      bias (gate)       -0.5V ±10%")
    print("    x96      bias (drain)      +6.3V ±10%")
    print()
    print("  SCPI witnesses (live below):")
    print("    TP1902  VARSAMP   0.9..1.1V     A21 alive (model ID)")
    print("    TP1910  DIAGSAMP  7.5..11V      comb-gen amplitude")
    print("    TP1915  VA5-N     -5.3..-4.7V   A26 local -5V rail")
    print()
    print("  Ctrl-C to exit.")
    print()
    print(f"  {'#':>5s}  {'TP1902':>8s}  {'TP1910':>8s}  {'TP1915':>8s}"
          f"  {'alive':>6s}  {'chain':>6s}  {'VA5-N':>6s}")
    print("  " + "-" * 62)
    i = 0
    try:
        while True:
            i += 1
            v1902 = read_tp(dev, 1902)
            v1910 = read_tp(dev, 1910)
            v1915 = read_tp(dev, 1915)
            w = "OK" if 0.9 <= v1902 <= 1.1 else "FAIL"
            c = "OK" if 7.5 <= v1910 <= 11.0 else "FAIL"
            r = "OK" if -5.3 <= v1915 <= -4.7 else "FAIL"
            print(f"  {i:>5d}  {v1902:+8.3f}  {v1910:+8.3f}"
                  f"  {v1915:+8.3f}"
                  f"  {w:>6s}  {c:>6s}  {r:>6s}", flush=True)
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n  (exit)")


# STATus:QUEStionable bit map — SMP operating manual p.222 Table 3-7
_QUES_BITS = {
    0: "VOLT",  # level-limit / overvoltage / output voltage out of spec
    5: "FREQ",  # RF output frequency not correct / out of spec
    7: "MOD",   # modulation not correct / operated outside spec
    8: "CAL",   # calibration not performed properly
}


def _decode_ques(val):
    if val == 0:
        return "-"
    names = [n for b, n in sorted(_QUES_BITS.items()) if val & (1 << b)]
    extra = val & ~sum(1 << b for b in _QUES_BITS)
    if extra:
        names.append(f"?{extra:#x}")
    return "+".join(names) if names else f"raw{val}"


def action_boot_snap(dev):
    """Preserve and display the boot-time error queue and status
    registers. Intended as the very first SCPI action after a power
    cycle — no *RST, no writes beyond the connect-time *IDN? and *OPT?.

    Reads are ordered so that destructive reads (:SYST:ERR?, :EVEN?,
    *ESR?) happen AFTER non-destructive reads (:COND?, *STB?). This
    lets the condition snapshot reflect boot state even if the event
    register has accumulated bits that would otherwise be shadowed.
    """
    _header("Boot-time snapshot (no *RST)")

    # Non-destructive reads first.
    qc = int(dev.query(":STAT:QUES:COND?").strip())
    oc = int(dev.query(":STAT:OPER:COND?").strip())
    stb = int(dev.query("*STB?").strip())
    print(f"  :STAT:QUES:COND?      -> {qc}   [{_decode_ques(qc)}]")
    print(f"  :STAT:OPER:COND?      -> {oc}")
    print(f"  *STB?                 -> {stb}")

    # Destructive (read-clears) — intentionally last so their contents
    # represent everything accumulated from power-up to now.
    qe = int(dev.query(":STAT:QUES:EVEN?").strip())
    oe = int(dev.query(":STAT:OPER:EVEN?").strip())
    esr = int(dev.query("*ESR?").strip())
    print(f"  :STAT:QUES:EVEN?      -> {qe}   [{_decode_ques(qe)}]"
          f"  (latched since power-up)")
    print(f"  :STAT:OPER:EVEN?      -> {oe}   (latched since power-up)")
    print(f"  *ESR?                 -> {esr}   (latched since power-up)")
    if esr:
        esr_bits = []
        if esr & 0x80: esr_bits.append("PON(7)")
        if esr & 0x40: esr_bits.append("URQ(6)")
        if esr & 0x20: esr_bits.append("CME(5)")
        if esr & 0x10: esr_bits.append("EXE(4)")
        if esr & 0x08: esr_bits.append("DDE(3)")
        if esr & 0x04: esr_bits.append("QYE(2)")
        if esr & 0x02: esr_bits.append("RQC(1)")
        if esr & 0x01: esr_bits.append("OPC(0)")
        print(f"                            bits: {'+'.join(esr_bits)}")

    _header("Boot-time error queue (:SYST:ERR?)")
    errors = drain_err_queue(dev)
    if not errors:
        print("  queue empty — no boot-time errors reported")
    else:
        print(f"  {len(errors)} entries latched at power-up:")
        for e in errors:
            print(f"    {e}")

    _header("Notes")
    print("  Preserved state. Run `--quest-probe --fresh-boot` for the")
    print("  full 16-step walk (will issue *RST; re-power-cycle first")
    print("  if you want another clean boot snapshot).")


def action_quest_probe(dev, fresh_boot=False):
    """Walk the instrument through a set of states to attribute the
    persistent :STAT:QUES:COND flag (seen as 128 = MOD on this unit).

    After each state change, settle briefly and snapshot the status
    registers and error queue. QUES:EVENt is read after QUES:CONDition
    so the latched bits reflect transitions since the prior step.
    No physical probing is needed; the whole sequence runs in ~20s.

    When ``fresh_boot`` is True, an extra "step 00" snapshot is taken
    before *RST / any register-clearing read, to capture the raw
    post-power-up state of QUES:COND / QUES:EVEN / *ESR. Intended to
    be run as the first SCPI action after a power cycle.
    """
    _header("Questionable-register attribution probe"
            + (" (fresh-boot)" if fresh_boot else ""))

    def snap(label):
        time.sleep(0.4)
        try:
            qc = int(dev.query(":STAT:QUES:COND?").strip())
            qe = int(dev.query(":STAT:QUES:EVEN?").strip())
            oc = int(dev.query(":STAT:OPER:COND?").strip())
            esr = int(dev.query("*ESR?").strip())
            stb = int(dev.query("*STB?").strip())
        except Exception as exc:
            print(f"  {label:32s}  register read FAILED: {exc}")
            return
        errs = drain_err_queue(dev)
        n_err = len(errs)
        bits = _decode_ques(qc)
        print(f"  {label:32s}  QC={qc:<4d} QE={qe:<4d} OC={oc:<3d}"
              f"  ESR={esr:<3d} STB={stb:<3d}  [{bits}]  err={n_err}")
        for e in errs:
            print(f"      err: {e}")

    print()
    print("  columns: QC=QUES:COND  QE=QUES:EVEN (latched, clears on read)")
    print("           OC=OPER:COND  ESR=*ESR?    STB=*STB?")
    print(f"  QUES bit map: {_QUES_BITS}")
    print()

    if fresh_boot:
        # No *RST, no clearing reads — capture whatever the instrument
        # latched during power-up self-configuration. The snap itself
        # will read (and therefore clear) QUES:EVEN and *ESR, so any
        # subsequent snap can only see re-asserted bits.
        snap("00 fresh-boot raw (pre-*RST)")

    # Start from a clean state so QE reflects transitions caused by the
    # probe rather than anything the user left set. *RST does not clear
    # hardware condition registers, so a persistent fault will survive.
    dev.write("*RST")
    time.sleep(0.8)
    drain_err_queue(dev)  # discard anything *RST raised
    dev.query(":STAT:QUES:EVEN?")  # clear latched event bits

    snap("01 baseline after *RST")

    dev.write("SOURCE:FREQUENCY:CW 10GHz")
    dev.write("POW -30")
    snap("02 freq=10GHz POW=-30 OUTP=OFF")

    dev.write("OUTP:STAT ON")
    snap("03 OUTP ON  (10 GHz)")

    dev.write("SOURCE:FREQUENCY:CW 20GHz")
    snap("04 freq=20GHz OUTP=ON")

    dev.write("SOURCE:FREQUENCY:CW 1GHz")
    snap("05 freq=1GHz  OUTP=ON  (below A10 band)")

    dev.write("SOURCE:FREQUENCY:CW 10GHz")
    dev.write("OUTP:STAT OFF")
    snap("06 OUTP OFF (10 GHz)")

    # AM — the SOUR2 / :AM:INT2 path requires SM-B2 (LF Generator).
    # When absent, skip the internal-source setup and fall back to
    # driving the AM modulator with its primary internal source so
    # bit 7 (MOD) is still exercised without spewing -241 errors.
    installed = query_options(dev)
    if "SM-B2" in installed:
        dev.write("SOUR2:FREQ:CW 1000")
        dev.write("SOUR2:FUNC:SHAP SIN")
        dev.write("SOUR:AM:INT2:FREQ 1000")
    dev.write("SOUR:AM 30PCT")
    dev.write("SOUR:AM:STAT ON")
    snap("07 AM ON  30% 1kHz")
    dev.write("SOUR:AM:STAT OFF")
    snap("08 AM OFF")

    # FM — SM-B5 required; installed on this unit.
    dev.write("SOUR:FM:DEV 100E3")
    dev.write("SOUR:FM:STAT ON")
    snap("09 FM ON  100kHz dev")
    dev.write("SOUR:FM:STAT OFF")
    snap("10 FM OFF")

    # PM — SM-B5.
    try:
        dev.write("SOUR:PM:DEV 1")
        dev.write("SOUR:PM:STAT ON")
        snap("11 PM ON  1rad")
        dev.write("SOUR:PM:STAT OFF")
        snap("12 PM OFF")
    except Exception as exc:
        print(f"  PM section skipped: {exc}")

    # Pulse modulation (external source; SM-B4 internal pulser is not
    # installed on this unit, but PULM:STAT only requires the modulator).
    try:
        dev.write("SOUR:PULM:STAT ON")
        snap("13 PULM ON (ext src)")
        dev.write("SOUR:PULM:STAT OFF")
        snap("14 PULM OFF")
    except Exception as exc:
        print(f"  PULM section skipped: {exc}")

    dev.write("OUTP:STAT ON")
    snap("15 OUTP ON all-mod-off  (10 GHz)")
    dev.write("OUTP:STAT OFF")
    snap("16 OUTP OFF final")

    _header("Interpretation")
    print("  - If MOD (bit 7) is constant across every step including")
    print("    baseline after *RST, the flag is a static hardware")
    print("    integrity check (leading candidate: A9 aux-osc rail).")
    print("  - If MOD toggles with AM/FM/PM/PULM STAT, the flag is")
    print("    dynamic and tied to the modulator being armed.")
    print("  - FREQ (bit 5) appearing on OUTP ON confirms the PLL-")
    print("    unlock detector is armed and independently witnesses")
    print("    the A21 cascade fault.")
    if fresh_boot:
        print("  - Fresh-boot: if step 00 shows MOD=1 but step 01")
        print("    (after *RST and :EVEN? read) shows MOD=0, the bit")
        print("    was a power-up latch consumed by register-clearing")
        print("    reads, NOT a continuous hardware monitor — i.e.,")
        print("    it does not corroborate any live hardware fault.")


# (description, test class, required option or None)
MODULES = {
    "A4":  TestA4,
    "A4LF": TestA4LF,
    "A5":  TestA5,
    "A6":  TestA6,
    "A7":  TestA7,
    "A8":  TestA8,
    "A9":  TestA9,
    "A10": TestA10,
    "A21": TestA21,
    "A26": TestA26,
}


def list_modules(installed):
    """Print available test modules with option requirements."""
    for key, cls in MODULES.items():
        tags = []
        if cls.option:
            if cls.option in installed:
                tags.append("installed")
            else:
                tags.append("not installed")
        if cls.has_deep():
            tags.append("deep")
        tag = f" [{', '.join(tags)}]" if tags else ""
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
    parser.add_argument(
        "-d", "--deep",
        action="store_true",
        help="run extended state-dependent checks",
    )
    parser.add_argument(
        "--detect-a9",
        action="store_true",
        help="detect A9 board variant (1035.6301.02 vs 1035.6199.02) and exit",
    )
    parser.add_argument(
        "--sys-info",
        action="store_true",
        help="print *IDN?, *OPT?, operating hours, cycle count, cal status,"
             " hw modules, and drain :SYST:ERR?",
    )
    parser.add_argument(
        "--scan-modules",
        action="store_true",
        help="print :DIAG:INFO:MOD? raw + parsed for all slots",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run *TST? plus :TEST:RAM?/:ROM?/:BATT? (p.207 §3.6.15)"
             " with :STAT:QUES:COND?/:OPER:COND? snapshots and"
             " full error-queue drain",
    )
    parser.add_argument(
        "--alc-off-a9",
        action="store_true",
        help="re-read A9 rails TP1609/1610/1611/1612/1613 with ALC on vs off",
    )
    parser.add_argument(
        "--ref-source",
        action="store_true",
        help="compare A7 TPs under ROSC INT vs EXT",
    )
    parser.add_argument(
        "--att-sweep",
        action="store_true",
        help="sweep POW and manual attenuator positions, polling TP1914",
    )
    parser.add_argument(
        "--att-exercise",
        action="store_true",
        help="repeatedly cycle POW across the ATT27 transition zone,"
             " polling TP1914 each cycle (mechanical exercise)",
    )
    parser.add_argument(
        "--att-40-exercise",
        action="store_true",
        help="walk POW through 0/40/80 dB attenuation to isolate the"
             " 40 dB A and 40 dB B toggles (10/20 dB sections stay"
             " fixed); polls TP1914 each step",
    )
    parser.add_argument(
        "--att-cycles",
        type=int,
        default=20,
        help="number of cycles for --att-exercise / --att-40-exercise"
             " (default 20)",
    )
    parser.add_argument(
        "--a21-probe",
        action="store_true",
        help="park SMP at 3 GHz POW -30 OUTP ON and stream A21"
             " witnesses TP1902/TP1910/TP1915 once per second for"
             " physical probing with scope/DMM (Ctrl-C to exit)",
    )
    parser.add_argument(
        "--quest-probe",
        action="store_true",
        help="walk OUTP / AM / FM / PM / PULM through a state sequence"
             " while snapshotting :STAT:QUES:COND? / :EVEN? to attribute"
             " the persistent MOD bit (p.222 Table 3-7)",
    )
    parser.add_argument(
        "--fresh-boot",
        action="store_true",
        help="with --quest-probe, take an extra step-00 snap BEFORE"
             " any *RST / :EVEN? read to capture the raw post-power-up"
             " QUES state (intended as the first SCPI action after a"
             " power cycle)",
    )
    parser.add_argument(
        "--boot-snap",
        action="store_true",
        help="read :SYST:ERR? + status registers and exit immediately,"
             " with no *RST or other writes — preserves the boot-time"
             " error queue from being flushed (first command after"
             " every power cycle)",
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


ACTION_FLAGS = [
    "list_modules", "detect_a9",
    "sys_info", "scan_modules", "self_test",
    "alc_off_a9", "ref_source", "att_sweep", "att_exercise",
    "att_40_exercise", "a21_probe", "quest_probe", "boot_snap",
]


if __name__ == "__main__":
    args = parse_args()

    any_action = any(getattr(args, a) for a in ACTION_FLAGS)
    if not args.module and not any_action:
        print("specify module(s) with -m"
              " or use --list-modules / --detect-a9 / --sys-info /"
              " --scan-modules / --self-test / --alc-off-a9 /"
              " --ref-source / --att-sweep / --att-exercise /"
              " --att-40-exercise / --a21-probe / --quest-probe /"
              " --boot-snap")
        exit(1)

    try:
        dev = connect_smp()
    except ConnectionError:
        exit(1)

    try:
        # --boot-snap runs BEFORE *OPT? so that the MAV / queue state
        # reflects only what the instrument and connect_smp()'s *IDN?
        # have produced. This is the closest we can get to a virgin
        # post-power-up snapshot over the GPIB session.
        if args.boot_snap:
            action_boot_snap(dev)
            exit(0)

        if args.unlock is not None:
            errs = unlock_protect(dev, args.unlock)
            if errs:
                print(f"LOCK LEVEL {args.unlock}: unlock FAILED ({errs})")
            else:
                print(f"LOCK LEVEL {args.unlock}: unlocked")

        installed = query_options(dev)
        print(f"Installed options: {', '.join(sorted(installed))}")

        if args.list_modules:
            list_modules(installed)
            exit(0)

        if args.detect_a9:
            stock = detect_a9_variant(dev, verbose=True)
            print(f"  verdict: {stock}")
            exit(0 if stock != A9_V_UNKNOWN else 2)

        if args.sys_info:
            action_sys_info(dev)
            exit(0)

        if args.scan_modules:
            action_scan_modules(dev)
            exit(0)

        if args.self_test:
            action_self_test(dev)
            exit(0)

        if args.alc_off_a9:
            action_alc_off_a9(dev)
            exit(0)

        if args.ref_source:
            action_ref_source(dev)
            exit(0)

        if args.att_sweep:
            action_att_sweep(dev)
            exit(0)

        if args.att_exercise:
            action_att_exercise(dev, cycles=args.att_cycles)
            exit(0)

        if args.att_40_exercise:
            action_att_40_exercise(dev, cycles=args.att_cycles)
            exit(0)

        if args.a21_probe:
            action_a21_probe(dev)
            exit(0)

        if args.quest_probe:
            action_quest_probe(dev, fresh_boot=args.fresh_boot)
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
        deep_passed = []
        deep_failed = []

        for name in selected:
            cls = MODULES[name]
            if cls.option and cls.option not in installed:
                print(f"\n=== {name}: {cls.desc} ==="
                      f"\n  SKIPPED — requires {cls.option}"
                      f" (not installed)")
                skipped.append(name)
                continue
            std_ok, deep_ok = cls(dev, deep=args.deep,
                                  installed=installed)()
            if std_ok:
                passed.append(name)
            else:
                failed.append(name)
            if deep_ok is True:
                deep_passed.append(name)
            elif deep_ok is False:
                deep_failed.append(name)

        print("\n" + "=" * 40)
        print(f"PASSED:    {len(passed):2d}  {', '.join(passed)}")
        if failed:
            print(f"FAILED:    {len(failed):2d}  {', '.join(failed)}")
        if skipped:
            print(f"SKIPPED:   {len(skipped):2d}  {', '.join(skipped)}")
        if deep_passed:
            print(f"DEEP OK:   {len(deep_passed):2d}"
                  f"  {', '.join(deep_passed)}")
        if deep_failed:
            print(f"DEEP FAIL: {len(deep_failed):2d}"
                  f"  {', '.join(deep_failed)}")

    finally:
        dev.write("*RST")
        dev.write("POW -30")
        dev.write("OUTP:STAT OFF")
        dev.close()
