# SMP02 Diagnostic Investigation Task List

Instrument: Rohde&Schwarz SMP02, S/N 848985/012, Firmware 3.70

Installed options (via `*OPT?`):
SM-B1 (OCXO), SM-B5 (FM/ΦM Modulator), SMP-B11 (DCNV), SMP-B15 (ATT27)

Not installed: SM-B2 (LF Generator), SMP-B12 (PUM20), SMP-B13 (PUM2), SMP-B14 (Pulse Gen)

> **Historical / superseded content** is moved to
> [`smp_history.md`](smp_history.md). Inline supersession markers in
> this doc point to specific anchors there. The doc body itself
> always reflects current truth.

## Next actions

> Superseded 2026-04-30 — full NEXT-ACTIONS-ITEM-1 banner moved to
> [`smp_history.md#H-2026-04-30-next-actions-item-1-superseded`](smp_history.md#h-2026-04-30-next-actions-item-1-superseded).
> **Updated 2026-05-08** — Step 8a bench test confirmed V3/V4
> MRF3866/MRF5160 push-pull PA as the root cause (chips failed under
> RF drive on the bench). Step 8b confirmed A21 milled casing healthy.
> "Chips alive" verdict from D.5 is now overturned. §7E silicon-pull
> rebuild is **unblocked**. Next action: test MRF transistors in a
> higher-current test rig, then replace.

1. **Bench — MRF transistor characterisation + replacement.** Step 8a
   (2026-05-08) confirmed the V3/V4 MRF3866/MRF5160 push-pull PA as
   the fault — chips worked initially then broke under RF drive at
   close to rated output (23–24 dBm at 220 MHz before failure).
   Desoldered parts tested in component tester: MRF3866 shows NPN,
   no h_FE, B-E ≈ 6.4 MΩ; MRF5160 shows PNP, h_FE 70, V_BE 992 mV.
   Spare 2N3866A (TO-39) behave similarly (no h_FE, B-E ≈ 2 MΩ).
   **Next action:** mount MRF transistors in a test rig and test
   with higher currents than the component tester to determine
   whether they are truly damaged or the tester cannot characterise
   high-f_T RF power BJTs. Then proceed to §7E rebuild with
   replacement transistors.
   See [`smp_next.md`](smp_next.md) Status section and
   [Physical probe worksheet → Step 8a](smp_hw_diag.md#step-8a--on-a211-lo-chain-bench-psu-standalone-sa-board-out-no-casing).
2. **Bench — opportunistic work while the case is open** (same
   teardown): A9 TP1607 aux-osc scope probe, SMP-B15 40 B attenuator
   diagnosis, fan part-number capture. See
   [Physical probe worksheet → While the case is open](smp_hw_diag.md#while-the-case-is-open--opportunistic-work).
3. **Blocked on A21 repair**: A10 downstream revalidation
   (`smp_test.py -m A10 -d` — expect TP1807 to leave its −13.6 V rail
   once sampling pulses return), and SMP-B15 40 B root-cause
   mechanical fix.

## Per-module status

Numbering (§1…§6) is the order modules were investigated historically,
not a priority list. Priority lives in [Next actions](#next-actions);
the blocks below are a per-module status register.

### 1. A9 ALC Amplifier — variant 1035.6199.02 (reclassified)

**Manual references (A9 §7, band-2):**

- Full section (DE+EN): [band-2 §7 A9 ALC Amplifier — variant 1035.6199.02](rs_smp_corpus/volumes/band-2/sections/05_ch7-a9-alc-amplifier-variant-1035619902.md) — authoritative for this instrument
- Other variant for contrast: [band-2 §7 A9 ALC Amplifier — variant 1035.6301.02](rs_smp_corpus/volumes/band-2/sections/04_ch7-a9-alc-amplifier-variant-1035630102.md) — the V240/V250 buffer-transistor variant this instrument does **not** have

**Current status:**

- One A9-internal fault: **TP1607 aux-osc emitter = +1.86 V** (spec
  0.7–1.6 V). Single-witness analog, not reflected in SCPI. Next
  action: scope during case-open (see [Next actions](#next-actions) → 2).
- TP1612 / TP1613 rails ≥2 GHz are **cascade symptoms** of the A21/A10
  fault (no stable RF at the ALC detector), not A9 faults. Re-evaluate
  after A21 + A10 repair.
- QUES:MOD bit 7 is a **third-party witness** for the A21/A10 cascade
  via A10 FM-input overdrive (boot error 134), not for A9 TP1607.
- Board variant confirmed `1035.6199.02` (Var04 Rev03); variant-aware
  specs pinned in `smp_common.A9_SCPI_VAR_MAP`.

> Superseded 2026-04-30 — earlier A9 TP1605/TP1603/QC=128/V240-V250
> retractions moved to
> [`smp_history.md#H-2026-04-30-tp1605-wrong-sign-retracted`](smp_history.md#h-2026-04-30-tp1605-wrong-sign-retracted).
> Current verdict: multi-path DAC within zero-scale tolerance; QC=128 live;
> 6199 board has no V240/V250.

**Board variant:** `1035.6199.02` — confirmed via both SCPI
(`:DIAG:INFO:MOD?` → `ALCA Var04 Rev03`) and TP1604 discriminator
(+1.002 V, centre of the 0.995–1.005 V spec window).

Variant mapping now pinned in `smp_common.A9_SCPI_VAR_MAP` and applied
automatically by `smp_test.py -m A9` and `smp_diag.py -m A9`.

The 6199 board has **no V240/V250 buffer transistors** (those are a
6301-only feature). On this variant TP1610 and TP1611 are the reference
level outputs themselves: one is active (0 to +2.7 V) and the other is
at 0 V depending on whether the RF frequency is below or above 2 GHz.

Most of the original §1 FAILs were 6301-spec artifacts — they
reclassify as OK against the 6199 spec.

Full 16-point A9 sweep against 6199 spec
(`smp_diag.py -m A9 --verbose`, RF output OFF, preset 10 MHz):

| TP | Description (6199) | Reading | Expected | Status |
|----|--------------------|---------|----------|--------|
| 1600 | Reference ground | 0.00 V | 0 V ±10 mV | **OK** |
| 1601 | +5 V reference | +5.00 V | +4.975…+5.025 V | **OK** |
| 1602 | −5 V reference | −4.98 V | −5.025…−4.975 V | **OK** |
| 1603 | AM depth DAC (AM off) | 0.00 V | (spec window for AM on) | OK rest state |
| 1604 | AM adder (AM off) | +1.002 V | 0.995–1.005 V | **OK** |
| 1605 | FM DAC (FM off) | −0.64 V | (spec window for FM on) | OK idle (multi-path summing node, see deep-test sweep) |
| 1606 | AM modulator IF port | +0.11 V | ~0.1 V | **OK** |
| 1607 | Aux. osc. emitter | +1.86 V | 0.7–1.6 V | **FAIL** — 260 mV over |
| 1608 | EXT ALC offset | −0.05 V | ±0.005 V | FAIL by 10× spec, 50 mV absolute |
| 1609 | Log Atten control | 0.00 V | 0–0.95 V (level-dep) | OK (RF off → min) |
| 1610 | Ref level x93 | −0.02 V | level-dependent | OK (RF off → both at 0) |
| 1611 | Ref level x95 | −0.02 V | level-dependent | OK (RF off → both at 0) |
| 1612 | Diff. amp. offset | +0.06 V | ±40 mV when ALC active | OK (RF off — relaxed) |
| 1613 | Main loop | −5.36 V | −5…+0.7 V | spurious — pegged with no RF feedback |
| 1614 | Limit DAC | −0.79 V | −5…0 V | **OK** |
| 1615 | LF generator (off) | 0.00 V | ≈0 V | **OK** |

Plus deep-test results from `smp_test.py -m A9 -d` (RF output ON):

| TP | Description | Reading | Status |
|----|-------------|---------|--------|
| 1603 | AM depth DAC (AM on) | +0.07 / −0.04 V (drifts run-to-run) | OK — within DAC zero-scale tolerance |
| 1605 | FM DAC @ 1 MHz dev | +0.78 V | **OK** (was −1.05 V at default dev — see FM sweep below) |
| 1615 | LF gen (AM on) | +0.385 V | OK vs spec; 5–6 mV under regression window |

FM DAC response sweep (`smp_test.py -m A9 -d`, single representative run):

| Condition | TP1605 |
|-----------|--------|
| FM off | −0.643 V |
| FM on, dev 0 Hz | −0.658 V (idle position) |
| FM on, dev 100 kHz | −1.710 V (info — low-dev path) |
| FM on, dev 1 MHz | +0.781 V (in-spec — high-dev path) |

The DAC is alive and responding. SMP02 routes low and high
deviations through different DAC paths summed at TP1605 with
opposite signs, so intermediate values land negative and full
deviation lands positive. Only the 1 MHz reading is checked
against the service-manual 0–2.5 V window.

**Functional test (`smp_test.py -m A9`):** ✅ PASS —
ASK modulation at 10 GHz works:
TP1613 = −4.98 V at 0 dBm NORM, +0.55 V at 22 dBm INV, unlevel clears.

**Deep test (`smp_test.py -m A9 -d`):** ❌ DEEP FAIL,
but only one A9-internal fault remains after re-classification.

- **Confirmed A9-internal fault:**

  - **TP1607 aux. oscillator emitter = +1.86 V** (spec 0.7–1.6 V).
    260 mV above upper bound, ~16% over, stable across all reads
    and across runs. The aux oscillator generates the four-
    fixed-frequency NF source used to linearise the
    level-detector characteristic. An emitter sitting 260 mV
    high points at:
    - bias resistor out of tolerance, or
    - a partially failed oscillator transistor (no AC swing, bias
      resistor alone setting the DC), or
    - a shorted bypass cap pulling the emitter up

    Confirm with a scope on TP1607 — a healthy oscillator shows
    AC swing on top of the DC bias.

- **Reclassified as not-a-fault:**

  - **TP1605 FM DAC** — earlier "wrong sign" diagnosis was
    incorrect. The FM DAC response sweep showed:
    +0.78 V at 1 MHz deviation (in spec), −1.71 V at 100 kHz
    deviation (info). SMP02 routes low and high deviations
    through different DAC paths summed at TP1605 with opposite
    signs. The DAC is alive; the previously-reported −1.05 V
    reading was the low-dev path output, which is normal.

  - **TP1603 AM DAC** — drifts between +0.07 V and −0.04 V
    around the 0 V upper bound across runs. Within DAC
    zero-scale tolerance, not a fault.

  - **TP1608 EXT ALC offset = −0.05 V** (spec ±5 mV) — 10× over
    spec but only 50 mV absolute, on an unused EXT ALC input.
    Academic unless EXT ALC is used.

  - **TP1615 LF-gen-on = +0.385 V** — 5–6 mV below the 0.39 V
    regression window; within service-manual spec (0–0.42 V).
    Script tolerance nit.

- **TP1612 diff-amp offset — band-boundary rail (cascade, not a primary A9 fault):**

  - 10 MHz to 1 GHz: +0.002 to +0.005 V — in spec (±40 mV),
    except an intermittent rail at 0.5 GHz seen on one run
    (+0.446 V) but not the next. Worth re-checking later.
  - 2 to 20 GHz: +0.5 to +14.4 V — all railed positive.
  - TP1612 flips from clean zero to railed at the 2 GHz band
    switch, exactly where the RF path transitions from the
    0.01–2 GHz downconverter (A26) to the YIG output (A10/YFO).

- **TP1613 main-loop control — not tracking (cascade):**

  - <2 GHz: reads −0.5 to −2.7 V regardless of commanded level
    (POW −140 and POW 22 give identical readings at each frequency).
  - ≥2 GHz: stuck at ~+0.4 V regardless of level — pegged high,
    consistent with no RF at the detector.

The TP1612 / TP1613 patterns above 2 GHz are **secondary to the A10 YIG
PLL fault and the A26 sampling-pulse-generator fault** — the ALC diff
amp rails because there is no stable microwave RF at the detector for
it to regulate against. Below 2 GHz the loop is also mis-tracking, but
less severely; re-evaluate after A10/A26 are repaired.

**Hypotheses ruled out by the full sweep:**

- ±5 V reference rails: ruled out. TP1601 = +5.00 V and
  TP1602 = −4.98 V both clean.
- Reference ground offset: ruled out. TP1600 = 0.00 V clean.
- Limit DAC corruption: ruled out. TP1614 = −0.79 V, in spec.
- FM DAC polarity inversion: ruled out by the response sweep —
  multi-path circuit behaviour explains the negative readings
  at low deviation.
- AM DAC offset as a fault: ruled out — drifts inside zero-scale
  tolerance across runs.

**SCPI-level check — MOD bit is NOT about A9 TP1607.** A fresh-boot
`--quest-probe --fresh-boot` capture (first SCPI action after a clean
power cycle) resolves the prior ambiguity: `QC=128` (bit 7 MOD) is a
**live, continuous hardware monitor** that survives `*RST` and
persists across all 16 probe states. Crucially, the boot error queue
also contained **error 134 "FM input of YFO module overdriven"** —
which is almost certainly what the firmware's QUES:MOD monitor is
reflecting. The FM input to A10 is being overdriven because the A10
FM adder (TP1812) is pegged high at +9.03 V as part of the A21
cascade (see §4). So QUES:MOD bit 7 is a **third-party witness for
the A21/A10 cascade, not for A9 TP1607**. The TP1607 aux-osc
emitter fault (+1.86 V vs. 0.7–1.1 V spec) remains a **single-witness
analog fault** that the SCPI layer does not surface.

(Note: an intermediate `--quest-probe` run in a long session once
returned `QC=0` throughout, which triggered a transient "power-up
latch" hypothesis — now retracted. The fresh-boot data dominates;
the QC=0 run reflected a momentarily non-railed A10 FM integrator
state during an unusually quiet command sequence, not a latch
clear.)

**Next steps:**

- Scope-probe TP1607 with the **4-channel 100 MHz scope** (the aux
  osc drives NF level-detector linearization tones in the kHz–low-MHz
  range; BW is massive overkill, pick this scope for the channel
  count so you can add a ground-reference probe easily). Look for
  AC swing on top of the +1.86 V DC bias. If no AC swing, investigate
  bias resistor and oscillator transistor.
- After A10/A26 are repaired, re-run `smp_test.py -m A9 -d` to
  re-check TP1612/TP1613 frequency sweep — expected to clear once
  upstream RF path is intact. Also re-check the intermittent
  TP1612 @ 0.5 GHz rail.
- Optional: loosen `smp_test.py` TP1615 lower bound from 0.39 V
  to ~0.36 V (0.385 V is in-spec per service manual).
- After A21 + A10 repair, re-run `--quest-probe --fresh-boot` on a
  clean boot: if `QC=128` persists and error 134 "FM input of YFO
  module overdriven" is still in the boot queue, the A10 FM-input
  fault extends beyond the A21 cascade and needs its own treatment.
  If both clear, MOD bit 7 was purely a cascade symptom.

### 2. A21 Sampling Module — sampling pulse generator dead

**Current status:**

- TP1910 DIAGSAMP flat at **0.22 V** across 10 MHz–20 GHz (spec
  7.5–11 V). TP1902 VARSAMP ≈ 1.0 V (OK). DIAGSAMP is a diagnostic-
  rectifier witness of the A21 LO chain, so the reading
  implicates the **sampling-pulse generator's LO chain or its
  diagnostic rectifier**; the sampling mixer (V1.1/V1.2) and IF amp
  (V75) are **not** implicated by this telemetry alone and remain to
  be checked on the bench worksheet. Fault is static (not
  frequency-dependent).
- A26 MUX **exonerated** (all other A26 channels in-spec). A21 power
  is **exonerated** and W216 is broadly healthy: VARSAMP in spec on
  W216.9, and the W216.10 conductor itself is **exonerated** by
  Step 2 (DMM at the A21 end of W216.10 reads 0.262 V, matching the
  SCPI TP1910 reading at the A26 end within meter noise — pin 10 is
  conducting under load, the dead reading is sourced on A21/A211).
- Bench Step 4 (`--a21-probe` at 3 GHz CW / POW −30, Siglent SSA):
  X50 present (+3.75 dBm @ 106.56 MHz, in band-3 §7.1.1 window after
  cable + DC-block losses), X211 present at the A20/X202 jack
  (+0.22 dBm @ 2.912533 GHz — off-frequency / bottom-of-spec readings
  are downstream cascade symptoms of the X75-dead fault per §4, not
  independent issues), **X75 dead** (< −55 dBm, 0–100 MHz). Decision
  tree → A21-internal.
- Bench Step 4.5 (X202↔X211 cable re-torqued at both ends, X50/X75
  SMBs reseated): X75 **still dead** post-retorque → X202 cable /
  connector **excluded**.
- Fault now localised to one of: A21 on-PCB LO chain (V50/V60
  doubler, LO amps V2/V3/V4, V4 step-recovery) feeding **X21** into
  the milled casing's comb generator (sub-assembly **A212**);
  in-casing **A214** pre-mixer RF amplifier (biased by X95 / VG and
  X96 / VD); the passive Schottky-bridge sampling mixer inside
  **A212**; in-casing **A212 IF amplifier** (biased by X72 /
  VA15-IF) whose output leaves on **X70**; on-PCB IF impedance
  transformer / matching between X70 and X75; A21 diag rectifier on
  A211; or an A211 bias-control crowbar (N80A–D / V85 / V89 / V90 /
  V95) having tripped and shut the A214 MMIC supply off.
- **Bench result — Step 7 A/B passed.** §7.1.7 bias chain is healthy:
  X95 = −0.72 V (within device-spread tolerance for the A214 GaAs-FET),
  X96 = +6.17 V, X72 = +14.98 V; OP97 (N90) supplies clean ±15 V with
  pin 6 at +9.32 V (mid-rail, loop active not saturated); BUZ71 (V90)
  V_GS ≈ +3.1 V (active region); R98 ≈ 0.1 Ω with V_R98 ≈ 7.4 mV → I_drain
  ≈ 74 mA, within 7 % of the §7.4.4 80 mA target. No §7.1.7 crowbar
  tripped. Bias chain is **not** the source of the X75 / TP1910 dead
  symptom.
- **Bench result — Step 8a FAILED (2026-05-08).** LO chain bench test
  with sig-gen (110 MHz −30 dBm) → X21, SA + 25 dB attenuator + DC
  block. Doubler, filters, and V2 (BFG97) pre-driver all working.
  V3/V4 push-pull PA initially produced signal at X21 (DIAGSAMP rose
  to 4–5 V, SA peak at 220 MHz reached 23–24 dBm), then output
  dropped ~3 dB and collapsed to near-noise — power lost at V3/V4.
  Desoldered MRF3866/MRF5160 tested in component tester: MRF3866
  shows NPN, no h_FE, B-E ≈ 6.4 MΩ; MRF5160 shows PNP, h_FE 70,
  V_BE 992 mV. 2N3866A spares behave similarly. **V3/V4 push-pull PA
  confirmed as the root cause** of the X75-dead symptom.
- **Bench result — Step 8b PASSED (2026-05-08).** A21 milled casing
  tested standalone: SMA coax soldered to V3/V4 trace, fed 220 MHz
  27 dBm, A211 powered (+15 V 120 mA, −15 V 70 mA), X211 fed 3 dBm
  2–6 GHz. Good IF output at X75, up to 18 dBm. S11 at X21/X216
  poor (2.3 dB @ 206 MHz, 5.2 @ 234 MHz, 7.6 dB dip @ 254 MHz) but
  not shorted. **A21 milled casing (A212/A213/A214) working as
  expected — casing exonerated.**
- **Bench result — Step 10a PASSED (2026-05-05).** X70 → X75 on-A211
  IF path exonerated (|S21| passband +31.4 … +31.6 dB, L72 notch at
  −39.5 dB @ 103 MHz).
- **Fault definitively isolated (2026-05-08):** V3/V4 MRF3866/MRF5160
  push-pull LO PA on A211. All other A21 signal paths exonerated
  (doubler, BFG97, IF chain, milled casing). Next: test MRF
  transistors in a higher-current rig, then replace.
> Superseded 2026-05-08 — Step 7D "R4D failure-chain" narrative
> (doubly superseded: first 2026-04-30 as expected push-pull bias,
> then 2026-05-08 when Step 8a confirmed V3/V4 as the actual root
> cause) moved to
> [`smp_history.md#H-2026-05-08-step-7d-r4d-failure-chain-narrative`](smp_history.md#h-2026-05-08-step-7d-r4d-failure-chain-narrative).
> Earlier 2026-04-30 supersession note also archived there.

> Superseded 2026-04-30 — "A7 step-synth marginal → A21 cascade"
> retraction moved to
> [`smp_history.md#H-2026-04-30-a7-step-synth-marginal-retired`](smp_history.md#h-2026-04-30-a7-step-synth-marginal-retired).
> Current verdict: A7 re-measured all-in-spec against band-2 p.115 ranges (see §3).

Measured on A26's diagnostic multiplexer via cable W216.10. Per band-3
§7.6 (p.147), A21 has no digital interface of its own; all A21
diagnostic voltages are routed to A26 and sampled there.

**Two SCPI witnesses available** (per band-3 §7.6 p.147 and the FSTEP
pinout table on p.148, A21 has no digital interface of its own; two
A21-sourced voltages are routed to A26's MUX via cable W216):

| TP (on A26) | W216 pin | Description | Reading | Expected | Status |
|----|--------|-------------|---------|----------|--------|
| 1902 | W216.9 | VARSAMP — model-ID from A21 | ~1.0 V | 0.9–1.1 V | **OK** |
| 1910 | W216.10 | DIAGSAMP — comb-gen diag from A21 | 0.22 V | 7.5–11 V | **FAIL** — dead |

**Functional test (`smp_test.py -m A21`):** ❌ FAIL — TP1910 dead,
TP1902 OK → differential verdict **"A21 powered and grounded; A21
LO chain (comb-gen / mixer / IF amp) or A211 diag rectifier /
comparator is the fault"** (W216.10 originally on this list, now
exonerated by Step 2 bench measurement).

**Deep test (`smp_test.py -m A21 -d`):** ❌ DEEP FAIL — TP1910 flat at
0.21–0.25 V across all 25 frequencies (10 MHz to 20 GHz), TP1902 flat
at ~1.0 V. The ~30 mV spread on TP1910 is diagnostic-MUX noise floor.
Fault is not frequency-dependent, consistent with a static-chain
failure (power, comb diode, diag rectifier, or conductor).

**Differential diagnosis — A26 MUX and A21 power are both exonerated.**

- **A26 MUX is not the fault.** The full A26 sweep
  (`smp_diag.py -m A26 -v`) finds TP1900 offset = 0.00 V (zero-point
  OK), TP1901/1903–1907/1914 option/model IDs in-range (D60-A/D62-A
  MUX selection and shift register D45-A work), TP1915 VA5-N for YFO
  = −4.93 V (local −5 V regulator alive), and A2 rails all clean. If
  the MUX were faulty, multiple channels would fail together; only
  TP1910 fails.
- **A21 supply rails are not the fault, and W216 is broadly healthy.**
  TP1902 VARSAMP is sourced from the same A21 card and arrives via
  W216.9 in spec at 0.9–1.1 V. VARSAMP needs W216.1 (+15 V), W216.4
  (+7.5 V), W216.5 (−15 V) and the ground pins (2/3/6/7/8). If any
  of these were broken, both witnesses would fail. **W216.10 is
  exonerated** by Step 2: DMM at the A21 end reads 0.262 V vs. SCPI
  TP1910 at the A26 end at 0.21–0.25 V — the conductor is intact
  under load, the dead reading is sourced on A21/A211.
  - **Follow-up — W216 supply-rail marginality.** Bench DMM at the
    A21 end of W216 reads pin 1 = **+15.28 V** (band-3 p.148 limit
    +15.25 V, +30 mV over) and pin 5 = **−15.35 V** (limit −15.25 V,
    −100 mV beyond). A2's own TPs read clean (+15.02 V / −15.05 V at
    TP300 / TP306, see [A2 Supply Voltages](#a2-supply-voltages--definitively-healthy)),
    so the skew is introduced between A2 and the W216 A21 end (A26
    distribution / connector drops, or DMM-vs-SCPI calibration offset).
    No fault witness currently depends on it; revisit only if another
    A26-fed board shows the same A2-clean / W216-end-skewed pattern.
    See [smp_hw_diag.md Step 2 run results](smp_hw_diag.md#step-2--w216-rail-voltages-measure-dc-voltage-instrument-on).

The fault is therefore localized to **one of** (post Step 4 / 4.5,
A21-internal):

1. A21 doubler (V50/V60) / LO amplifier (V2/V3/V4) / comb generator
   (V4 step-recovery) chain — verifiable at X21 (Step 8, expected
   +26…+30 dBm @ 206–234 MHz)
2. Sampling mixer (V1.1/V1.2 Schottky pair) or IF amp V75 /
   impedance transformer — verifiable by re-reading X75 once X21 is
   confirmed at spec (Step 9), or VNA S21 X70→X75 (Step 10)
3. A21 diag rectifier on A211 feeding DIAGSAMP — covered by Step 11
   (DC at the rectifier output should track X21 spec)
4. A211 bias-control crowbar tripped (N80A–D / V85 / V89 / V90 / V95)
   shutting the MMIC supply off on a failed controlled-supply voltage
   — covered first by Step 7 (X95 / X96 bias + comparator logic state)

**Excluded** by bench Steps 1, 2, 4, 4.5: W216 cable (all pins,
including pin 10 under load), A20 / X211 cable (X211 present at YIG
output, X202 cable re-torqued without effect), A7 → A21 X50 path
(X50 +3.75 dBm @ 106.56 MHz at the A21 connector — in spec after
test-cable + DC-block losses, leaving A7 in the clear corroborated
by §3 retraction).

→ **Bench procedure: [Physical probe worksheet (smp_hw_diag.md)](smp_hw_diag.md)** — current entry point [Step 7 (A21 bias + A211 comparators)](smp_hw_diag.md#step-7--a21-bias--a211-comparator-state-measure-dc-voltage-only-if-step-4-shows-x75-dead-with-inputs-present).

**A21 signal chain** (band-3 §7.1, p.144; A211 daughter board sits on
top of a milled casing that contains sub-assemblies **A212** (comb
generator + passive Schottky sampling mixer + IF amplifier), **A213**
(LPF on the X211 RF path), and **A214** (pre-mixer RF amplifier);
PCB ↔ casing connectors per drawing 1035.8840.01, band-3 p.156):

1. A7 step synthesis (103–117 MHz, +4…+6 dBm, p.148 FSTEP) → A21 **X50**
2. On-PCB LO chain: doubler V50/V60 → LO amplifiers V2, V3, V4 →
   step-recovery V4 → **X21 (LO into milled casing's A212 comb
   generator)** (spec +26…+30 dBm in the 206–234 MHz band at the
   doubler tap, p.146 §7.4.1)
3. Inside casing: **A212** comb generator forms the 2–20 GHz LO comb
   driving the passive Schottky-bridge sampling mixer (V1.1 / V1.2);
   in parallel, **A214** is the pre-mixer RF amplifier on the X211
   path, biased via **X95 (VG, −0.5 V)** and **X96 (VD, +6.3 V)**
   from A211 (the sampling mixer itself is passive — no DC bias)
4. **X211** (YIG RF from A20, 2–20 GHz) → **A213** LPF → **A214**
   pre-mixer amp → A212 sampling mixer RF port; mixer IF → **A212
   IF amplifier** (≈ +27 dB, biased via **X72 / VA15-IF** from A211)
   → **X70 (IF out of casing → A211)** (p.144 §7.1.4)
5. On-PCB IF impedance transformer / matching between X70 and X75
   (L72 LP filter + decoupling; V75's role on the PCB pending
   physical confirmation against p.156) → **X75** (10–80 MHz,
   −5…+15 dBm → A10 YIG-PLL, p.145 §7.1.6, p.148 FSTEP)
6. Bias control on daughter board A211 (1035.8840.02): N80A–D / V85 /
   V89 / V90 / V95 — comparators shut the A214 MMIC supply off
   (X95/X96) on failure of a controlled supply voltage (p.145 §7.1.7)

### 3. A7 Reference/Step Synthesis — RETRACTED (all in spec)

Both prior "A7 faults" were spec-window artefacts from the
band-1 p.102 functional-description ranges, not real hardware
issues. With the authoritative band-2 p.115 "Testing & Repair"
ranges now applied in `smp_diag.py` and verified against a
freshly-booted unit:

| TP | Description | Reading | Spec (band-2 p.115) | Status |
|----|-------------|---------|---------------------|--------|
| 0203 | 1-MHz reference signal for PLL | 3.39 V | 1.80–5.20 V | ✅ OK |
| 0205 | External reference I/O | 2.22 V | 0.80–3.50 V | ✅ OK |
| 0210 | REF600 (RF ≥ 93.75 MHz regime) | −0.00 V | ±20 mV | ✅ OK |

**Explanation.** Band-1 p.102 gives a single window `0.15–0.52 V`
for TP0210; band-2 p.115 reveals it's split by RF frequency:
`0.2–0.6 V` only applies at RF < 93.75 MHz (where the REF600
divider is actually used). At RF ≥ 93.75 MHz (any normal operating
point) REF600 is bypassed and the expected reading is `±20 mV`.
The preset/default ≥ 93.75 MHz gave `−0.00 V` which is in-spec.
Similarly the 1-MHz reference at 3.39 V is fine against p.115's
`1.8–5.2 V`; the old `3.5–5.0 V` window was the narrower range
listed further down in the functional-description section of
band-1, not the ATP limit.

**Functional test (`smp_test.py -m A7`):** ✅ PASS —
TP212 monotonic 2.28 → 12.64 V across 2282–2482 MHz step, TP215
`0.27–0.29 V` all steps.

**Action:** none. A7 is healthy; previously-reported REF600 and
1-MHz marginality claims in earlier revisions of this document are
hereby retracted. (Note: this also partially defuses the §6 "A7
marginality is driving A8 buffer-VCO intermittency" hypothesis.)

### 4. A10 YIG PLL — pretune DAC OK, PLL cascade from A21 remains

**Manual references (A10 §7, band-2):**

- Full section (DE+EN): [band-2 §7 A10 YIG-PLL](rs_smp_corpus/volumes/band-2/sections/03_ch7-a10-yig-pll.md)
- [p.158 §7.1.1 — YFO control](rs_smp_corpus/volumes/band-2/pages/p0158_71-functional-description_en.md) — TP1800 −10 V reference derivation
- [p.159 §7.1.2 — PLL](rs_smp_corpus/volumes/band-2/pages/p0159_712-pll_en.md) — N500 PI controller; cascade pathway from A21 sampling IF
- [p.163 §7.4 — DC voltage / HzTest tables](rs_smp_corpus/volumes/band-2/pages/p0163_741-dc-voltage-test_en.md) — TP1802 / TP1805 scaling formula (U1 = 8…12 V, U2 = −(3.7…5.7 V) at 20 GHz)
- [band-1 p.113 §6.3.2.1.6 — A10 YIG-PLL spec](rs_smp_corpus/volumes/band-1/pages/p0113_63216-a10-yig-pll_en.md) — TP1807 ±3 V PLL-control-voltage window

**Current status:**

- **Pretune DAC, main tuning driver, local reference all in spec** at
  every sampled frequency: TP1802 +1.00 V → +10.44 V (2 → 20 GHz,
  matches p.163 `U1 · f/20 GHz` with U1 = 8…12 V); TP1805, TP1804,
  TP1800 all clean.
- **PLL railed as a cascade from A21**: TP1807 = −13.62 V flat across
  25 frequencies (spec ±3 V). With A21's sampling pulse generator dead
  the phase detector sees a static error and N500 integrator rails
  negative; TP1809 / TP1811 / TP1812 clip alongside. Not an A10-internal
  fault.
- **SCPI witnesses confirming the cascade**: `QE=160` at fresh boot
  (MOD + FREQ latched), `QC=128` continuous (MOD via A10 FM-input
  overdrive), boot error 134, boot error −313 (YFOM cal-mem lost).
- **YFOM cal-memory loss (err −313)** is a separate, unresolved
  A10-internal or on-module-NVRAM issue — will need `:CAL:ALL?` or
  service-menu re-calibration after A21 is back.
- **Next action:** re-run `smp_test.py -m A10 -d` after A21 repair;
  expect TP1807 → ±3 V window. TP1800 +12 mV marginality: no action.

> Superseded 2026-04-30 — earlier TP1802 "sign-inversion / summing-stage"
> retraction moved to
> [`smp_history.md#H-2026-04-30-tp1802-sign-inversion-retracted`](smp_history.md#h-2026-04-30-tp1802-sign-inversion-retracted).
> Current verdict: TP1802 is positive per §7.4.2 `U1 = 8…12 V` and in spec
> on this unit; §7.4.2 is the measurement-procedure authority. Spec-window
> bugs in `smp_diag.py` / `smp_test.py` TP1802 checks are follow-up cleanup
> (details below).

**Summary after extended deep sweep** (`smp_test.py -m A10 -d`,
25 frequencies 10 MHz–20 GHz):

| TP | Description | Reading | Spec source | Status |
|----|-------------|---------|-------------|--------|
| 1800 | Negative reference (filtered) | −9.968 V (span 0.7 mV) | band-2 p.163 table: −10.02…−9.98 V | marginal (+12 mV positive of spec lower bound; stability excellent) |
| 1802 | Pretune DAC | +1.00 V @ 2 GHz → +10.44 V @ 20 GHz, linear | band-2 p.163 HzTest table: U1 = 8…12 V @ 20 GHz, linear f/20 GHz scaling | **OK** at every sampled frequency |
| 1804 | Output N210-B | −3.85 V @ 2 GHz → −4.81 V @ 20 GHz | smp_diag.py (−6…−3 V), Typical §4 | OK |
| 1805 | Main tuning current | −0.47 V @ 2 GHz → −4.89 V @ 20 GHz, linear | band-2 p.163 HzTest table: U2 = −(3.7…5.7 V) @ 20 GHz, linear f/20 GHz scaling | **OK** at every sampled frequency |
| 1807 | PLL control voltage | −13.62 V flat across all 25 freqs | band-1 p.113 §6.3.2.1.6: −3…+3 V | **FAIL — railed** (cascade from A21) |
| 1809 | FM coil current | −9.08…−9.12 V | smp_diag.py (−8…+8 V) | FAIL — clipping (cascade) |
| 1811 | Tracking coil current | −9.06 V | smp_diag.py (−8…+8 V) | FAIL — clipping (cascade) |
| 1812 | FM adder | +9.03 V | smp_diag.py (−12…+12 V) | OK but saturated high (cascade) |

**Service-manual reference (double-check in the original PDFs):**
- **Band 2, page 163 (EN)** — §7.4.2 "Checking the YFO Pretune" —
  contains the HzTest table giving nominal values for TP1802 and
  TP1805 at 20, 10, 5, 2 GHz, plus the scaling formula
  `v(x5) = f/20 GHz · V1`.
- **Band 2, page 143 (DE)** — §7.4.2 "Prüfen der YFO Voreinstellung"
  — identical table ("HzMeßpunkt"), with `U1 = 8...12V` and
  `U2 = −(3.7...5.7V)` at 20 GHz.
- **Band 2, page 158 (EN) / 138 (DE)** — §7.1.1 "YFO Control":
  "the integrated precision voltage source N1 is wired such that a
  negative voltage of −10 V is generated" — sampled on TP1800 / P1.
  This is the reference for the PLL and tuning driver, **not** the
  per-unit U1 constant used in the TP1802/TP1805 scaling formula on
  p.163; the two "V1"s in the manual refer to different quantities.

**Measured vs spec (confirms TP1802 is healthy):**

| Freq  | TP1802 measured | Spec window (U1 · f/20 GHz) | TP1805 measured | Spec window (U2 · f/20 GHz) |
|-------|-----------------|-----------------------------|-----------------|-----------------------------|
| 20 GHz | +10.44 V | 8.00 … 12.00 V ✅ | −4.89 V | −5.70 … −3.70 V ✅ |
| 10 GHz |  +5.17 V | 4.00 …  6.00 V ✅ | −2.44 V | −2.85 … −1.85 V ✅ |
|  5 GHz |  +2.58 V | 2.00 …  3.00 V ✅ | −1.21 V | −1.425 … −0.925 V ✅ |
|  2 GHz |  +1.00 V | 0.80 …  1.20 V ✅ | −0.47 V | −0.57 … −0.37 V ✅ |

Pretune DAC, main tuning driver, and local reference are intact.
Sub-2 GHz TP1802 readings (+3.1…+3.6 V at 10 MHz–1 GHz) track the
YIG's park frequency (~6–7 GHz pretune equivalent) while the A26
downconverter provides the RF output; not a fault.

**Cascade from A21 (unchanged).** Per band-2 §7.1.2 (p.139 EN /
p.119 DE), A10's PI controller N500 integrates the phase-discriminator
output comparing the sampling-mixer IF against the DDS reference.
Under the parsimony hypothesis that one upstream LO-chain fault on
A21 explains both DIAGSAMP = 0.22 V and TP1807 = −13.62 V, no IF
arrives at A10, the phase detector sees a static error, and N500
rails to the negative supply — TP1807 flat across all 25 frequencies,
with TP1809 / TP1811 / TP1812 clipping alongside it. The bench
worksheet confirms by observing X75 and the downstream branches; if
X75 is healthy on the bench while TP1910 still dead, only the diagnostic rectifier is broken and
the A10 cascade needs a separate explanation. Band-2 §7.3.1
troubleshooting ("Frequency error without synchronization too high")
maps this class of fault upstream to the sampling-IF path (x16),
not to A10 itself.

**SCPI witnesses for the A10 cascade.** A `--quest-probe --fresh-boot`
run (first SCPI action after power cycle) produces:

- `QE=160` at step 00 = bits 7+5 = **MOD + FREQ** both latched at
  boot, so the firmware *does* see the PLL as frequency-unlocked at
  power-up — but FREQ bit 5 does not re-assert after the first
  `:EVEN?` read. QUES:FREQ is edge-driven, not continuous.
- `QC=128` persists across all 16 probe steps = **MOD bit 7 is a
  live, continuous witness**. Boot error **134 "FM input of YFO
  module overdriven"** is the likely source: the A10 FM adder
  (TP1812) pegged at +9.03 V drives the YFO FM-input detector into
  its overdrive threshold, which the firmware reflects as QUES:MOD.
- Boot error **−313 "Calibration memory lost; YFOM - run internal
  calibration"** also present — see the YFOM cal-memory subsection
  below.

Together these three SCPI signals (QUES:MOD live, error 134, error
−313) cross-check TP1807 and TP1812 as the primary analog witnesses
of the cascade. TP1807 is no longer the only indicator.

**YFOM calibration memory lost (error −313).** The A10 YFO-module
carries its own on-board NVRAM with per-module calibration data
(factory-written YIG tuning coefficients for pretune, tracking,
and FM-sensitivity). On this unit that data is reported lost at
every power-up, distinct from the main A3 battery-backed calibration
(TP7 = +3.67 V, confirmed healthy). Consequences:

- The YFO pretune transfer function may default to a generic
  fallback curve, which could contribute to TP1802 / TP1805 sitting
  at the bottom of spec rather than mid-window, and to the PLL's
  inability to capture even if A21's IF were present.
- Even after A21 repair restores the sampling IF, `:CAL:ALL?` or
  the equivalent service-menu "internal calibration" will need to
  run to regenerate YFOM coefficients before A10 locks reliably.
- The cal-data loss mechanism is unresolved — possibilities include
  a dead on-module backup cell distinct from A3 TP7, a write-cycle
  wear-out on the module's EEPROM, or a bus-level comms fault on
  the digital interface that prevents the firmware from reading
  the module's NVRAM at boot.

Action items:
1. After A21 is repaired and the sampling IF is confirmed alive,
   attempt `:CAL:ALL?` (SMP operating manual p.200 §3.6.9) and
   observe whether error −313 clears on subsequent power cycles.
2. If error −313 re-appears at every power-up regardless of
   `:CAL:ALL?` success, inspect the A10 board for an on-module
   backup battery or NVRAM EEPROM (M48Zxx / DS1225 family) and
   its write-protect / chip-select lines.

**Correction — earlier "sign-inversion / summing-stage" hypothesis
retracted.** An earlier revision of this section read TP1802 against
`v(x5) = f/20 GHz · (−10 V)` and concluded the DAC output polarity
was flipped. That was a mis-binding of the formula's `V1`: the
p.163 HzTest table uses `U1 = 8…12 V` (positive) as the per-unit
reference for TP1802, with `U2 = −(3.7…5.7 V)` (negative) for
TP1805. Both test points are in spec at every sampled frequency
on this instrument.

**Caveat — unresolved sign contradiction in the manual itself.**
Two independent TP tables (**band-1 p.108** and **band-2 p.168**,
de+en) both list TP1802 as `−12.0 … −0.8 V`, typ. `−1 V @ 2 GHz`,
typ. `−10 V @ 20 GHz` — i.e. **negative** for the internal
`:DIAG:TPOINT? 1802` reading. The §7.4.2 HzTest procedure on p.163,
by contrast, describes TP1802 as the diagnostic alternative to the
multimeter point `x5 / P202` with `v(x5) = f/20 · V1`, `V1 = 8…12 V`
(**positive**). Our measurements across 25 frequencies (+1.00 V @
2 GHz → +10.44 V @ 20 GHz) agree exactly with the §7.4.2 positive
formula. Working interpretation (script enforces this): §7.4.2 is
the measurement-procedure authority and the TP-table sign is either
a consistent OCR artefact or refers to a signal tap upstream of a
buffer inversion. If a future SMP02 shows TP1802 **negative** with
the same linear scaling, revisit this — the TP-table reading may
be correct on that unit. Cannot be resolved without a scope probe
at the actual test-pin (multimeter point x5) vs the diagnostic ADC
output simultaneously.

**Known bugs in the checking scripts (for future repair sessions):**
- `smp_diag.py` previously had `1802: (-12.0, -0.8, "Pretune DAC")`
  following the TP-table spec. Script currently enforces the p.163
  positive interpretation as the default (matches this unit's
  measurements); see caveat above.
- `smp_test.py` `TestA10.run_deep` has a `TP1802 sign: max <= 0V`
  check and a `[-12, -0.8] V` spec check based on the same
  mis-bound formula; both will FAIL on a healthy instrument. The
  per-frequency "expect" column is computed as `f/20 · TP1800`
  (uses the −10 V reference), also wrong — it should be computed
  against U1 ≈ 10 V (midpoint) or against the measured TP1802 at
  20 GHz for self-calibration.

**Next steps:**
- After A21 is repaired (item 2 — see [Physical probe worksheet](smp_hw_diag.md)), re-run `smp_test.py -m A10 -d`
  — expected TP1807 to drop into the ±3 V window, TP1809 / TP1811
  / TP1812 out of clipping, with TP1800 / TP1802 / TP1804 / TP1805
  unchanged (already OK).
- Optional: fix the `smp_diag.py` / `smp_test.py` TP1802 spec
  windows per the §7.4.2 table so future A10 runs pass cleanly.
- TP1800 marginality (+12 mV) is within typical precision-reference
  aging; no action unless it drifts further.

### 5. SMP-B15 ATT27 — TP1914 pulled low by 40 dB B relay state

**Manual references (SMP-B15 / A14, band-4 §7):**

- Full section (DE+EN): [band-4 §7 A14 RF Attenuator 27/40 GHz (SMP-B15 / B17)](rs_smp_corpus/volumes/band-4/sections/02_ch7-a14-rf-attenuator-2740-ghz-option-sm.md) — mechanical / relay theory, W244 pinout
- [band-3 p.63 §7.4.3 — Attenuator-driver level-to-state mapping](rs_smp_corpus/volumes/band-3/pages/p0063_to-check-the-attenuator-drivers-either-t_en.md) — 10 / 20 / 40 A / 40 B engagement vs. total attenuation

**Current status:**

- **Deterministic fault**: TP1914 pulled from ~0.95 V to ~0.005 V
  whenever the 40 B section is in ATT (engages at 40 dB total and up).
  Snaps cleanly on every 40 B toggle; 10 dB / 20 dB toggles have no
  effect.
- **40 A unevaluable from TP1914 alone** until 40 B is repaired —
  a parallel 40 A fault would be masked. Post-repair, the same
  `--att-40-exercise` run becomes the 40 A check.
- **Secondary effect**: firmware classifies SMP-B15 as not-installed
  (TP1914 < 0.25 V threshold), producing err −222 "Data out of range"
  on high-attenuation POW setpoints. Expected to clear after 40 B fix.
- **Next action**: scope-probe + measure resistance on W244 / V67 / V68 (see
  [Next actions](#next-actions) → 2). Localised to 40 B section, not a
  generic ribbon issue.

> Superseded 2026-04-30 — earlier A19 "reseat helps, regresses"
> retraction moved to
> [`smp_history.md#H-2026-04-30-att-reseat-helps-retired`](smp_history.md#h-2026-04-30-att-reseat-helps-retired).
> Current verdict: 40 B section couples deterministically to TP1914 ID line
> when in ATT (drives it to ground); not intermittent.

| Condition | Reading | Expected | Status |
|-----------|---------|----------|--------|
| 40 B section THRU (total att 0/10/20/30 dB) | 0.94–0.96 V | 0.5–1.5 V | **OK** |
| 40 B section ATT  (total att 40…110 dB)     | 0.005–0.009 V | 0.5–1.5 V | **FAIL — pulled to ground** |

**Deterministic, not intermittent.** `smp_test.py --att-exercise
--att-cycles 1` walks every one of the 12 level bands in both
directions and annotates each step with the sections that should have
just toggled (10, 20, 40 A, 40 B). One round showed:

- TP1914 ≈ 0.95 V on both sweep directions while 40 B is in THRU.
- TP1914 ≈ 0.005 V on both sweep directions while 40 B is in ATT.
- The drop is exact at the 30↔40 dB boundary (step labelled
  `10,20,40B`), on both down-sweep and up-sweep.
- The 40 A toggle at the 70↔80 dB boundary, and the ~20 10 dB / 20 dB
  toggles across a round, have **no** visible effect on TP1914.

**Cannot distinguish 40 A from 40 B from this run alone.** The
standard level-to-state mapping (band-3 §7.4.3, p.63) never puts 40 A
in ATT while 40 B is in THRU: 40 B engages first at 40 dB total, 40 A
adds on at 80 dB total. As soon as 40 B pulls TP1914 low, any similar
contribution from 40 A is masked. The data is fully consistent with
"only 40 B couples to the ID line" but does not rule out a parallel
40 A coupling.

**Hypothesis.** A conductor or trace carrying the SMP-B15 ID voltage
is shorted to ground whenever the 40 B coil is driven or the 40 B
armature sits in its ATT position. The earlier "reseat helps, regresses"
observations were misread as random intermittency — the reseat only
"helped" because preceding operations left the attenuator at 0 dB
(40 B in THRU), and any subsequent high-attenuation use drove 40 B
back into ATT and the ID line back to ground.

**Confirmed by isolated-toggle exercise.** `smp_test.py
--att-40-exercise --att-cycles 2` walks three states that share
`10=THRU, 20=THRU` — 0 dB (POW +10, TTTT), 40 dB (POW -35, TTTA),
80 dB (POW -75, TTAA) — so each transition toggles exactly one
40 dB section with no 10 dB / 20 dB cross-talk. Results:

| State | POW | Att | TP1914 | Status |
|-------|-----|-----|--------|--------|
| TTTT | +10 dBm |   0 dB | 0.951 / 0.954 V | **OK** (2/2) |
| TTTA | −35 dBm |  40 dB | 0.005 – 0.010 V | **FAIL** (0/4) |
| TTAA | −75 dBm |  80 dB | 0.005 / 0.006 V | **FAIL** (0/2) |

The 40 B `engage` / `release` transitions flip TP1914 0.95 ↔ 0.005 V
cleanly every time; the 40 A transitions at the TTTA↔TTAA boundary
produce no change because 40 B is already ATT in both states. 40 A
therefore remains unevaluable from TP1914 alone until 40 B is
repaired — post-repair the same exercise becomes the 40 A check.

**Error-queue entries observed.** `--att-exercise` logged `-313
Calibration memory lost; YFOM` and `134 FM input of YFO module
overdriven` (known A10 / A21 cascade, unrelated to ATT27).
`--att-40-exercise` logged `-222 Data out of range` on the `POW -75`
step; this is almost certainly a secondary effect of the 40 B fault
itself — with TP1914 < 0.25 V the firmware classifies the SMP-B15 as
**not installed** (0.5 V / 0.25 V thresholds from `smp_diag.py`), and
any POW setpoint that can only be reached via the step attenuator is
then rejected. Expected to clear once 40 B is fixed.

**Next steps (physical, in order of cost):**

1. With the instrument on and `--att-40-exercise --att-cycles 1000`
   (or similar long run) providing a clean repetitive 40 B stimulus,
   scope the SMP-B15 ID line on the W244 / A26 connector and V67
   (THRU40B) / V68 (ATT40B) cathodes on the same time base. Use the
   **4-channel 100 MHz scope** — channel count beats BW here (driver
   edges are TTL-speed, ~10–100 ns rise time, 100 MHz is plenty);
   you want three signals (TP1914, V67 cathode, V68 cathode) on one
   acquisition for clean time-correlation, with channel 4 free as
   trigger or ground reference. Healthy drivers: one cathode <0.8 V,
   the other >2 V, swapping on each toggle (band-3 §7.4.3, p.63).
   Correlate the edge on TP1914 with the driver edge versus the
   ~15 ms relay travel (band-4 §7.1): electrical-edge-aligned short
   ⇒ driver / trace fault; delayed short aligned with armature
   travel ⇒ mechanical / contact fault
   inside the attenuator.
2. With the instrument off, measure resistance between the SMP-B15 ID pin on
   the A14/A26 ribbon header and each of V67 / V68 cathodes, with the
   attenuator manually cycled between its two 40 B positions. A
   low-resistance path that only appears in the 40 B = ATT position
   is the smoking gun.
3. Inspect the W244 ribbon specifically at the pins associated with
   the 40 B section — the fault is localised, not a generic ribbon
   issue. The previous full-header reseat treated the wrong area.
4. After a 40 B repair, re-run `--att-40-exercise --att-cycles 2`.
   The TTTA row should read ~0.95 V; if the TTAA row still reads
   low, a parallel 40 A coupling is present and the same physical
   workflow is repeated against V64 (THRU40A) / V65 (ATT40A).

### 6. A8 DSYN — intermittent boot err 221 (TP0305 retracted)

**Manual references (A8 §7, band-1):**

- Full section (DE+EN): [band-1 §7 A8 Digital Synthesis (DDS)](rs_smp_corpus/volumes/band-1/sections/06_ch7-a8-digital-synthesis-direct-digital.md) — DDS + buffer-VCO sub-loop theory, err 221 source
- [p.359 §7.4.10 — Testing the diagnosis](rs_smp_corpus/volumes/band-1/pages/p0359_7410-testing-the-diagnosis_en.md) — TP0305 `12–20 V @ :FREQ 1 GHz` window
- Downstream A21 X50 input (for the §2 cross-check): [band-3 p.144 §7.1 — A21 function description](rs_smp_corpus/volumes/band-3/pages/p0144_71-function-description_en.md)

**Current status:**

- **Err 221 "Digital synthesis buffer VCO unlocked" is intermittent**
  (1/3 fresh boots on current tally, perfectly correlated with QE
  bit 5 FREQ at boot). Signature of a threshold-marginal buffer-VCO
  lock detector — A8-local, not A7-driven.
- **Main DDS loop healthy.** TP0305 = 17.54 V at `:FREQ 1 GHz` (spec
  12–20 V), TP0303 / TP0304 both in-spec. Script fix applied: A8
  interval now parks the instrument at `:FREQ 1 GHz` before
  evaluation.
- **Cross-check with §2 A21**: A8's buffer VCO feeds A7 step-synth,
  which drives A21 X50. If the buffer VCO is marginal at boot, A21
  may be healthy with a degraded upstream drive. On the bench
  worksheet, Step 4 checks the live X50 path, Step 5 bypasses
  upstream drive, and Step 6 checks the A7 → A21 X50 path; run these
  before probing A8 directly.
- **Next action (desk)**: re-run `--boot-snap` across additional power
  cycles to firm up the err-221 rate statistics.

> Superseded 2026-04-30 — earlier A8 TP0305 / A7 marginality / A8-OK
> retractions moved to
> [`smp_history.md#H-2026-04-30-tp0305-and-a7-marginality-retired`](smp_history.md#h-2026-04-30-tp0305-and-a7-marginality-retired).
> Current verdict: TP0305 in spec at manual's test condition (`:FREQ 1 GHz`);
> A7 re-measures all-in-spec; A8 boot err 221 is on a separate sub-loop
> (intermittent, see 6a below).

**6a. Err 221 "Digital synthesis buffer VCO unlocked" at power-up —
intermittent.** `--boot-snap` captures across fresh boots:

| Boot | err 221 | QE boot bits | err 134 | err −313 |
|------|---------|--------------|---------|----------|
| 1 | present | 160 = MOD+FREQ | present | present |
| 2 | **absent** | 128 = MOD only | present | present |
| 3 | **absent** | 128 = MOD only | present | present |

2/3 recent boots locked cleanly. Err 221 is genuinely intermittent.

**6b. TP0305 — RETRACTED (in spec at manual's test condition).**
An earlier revision of this section flagged TP0305 = 11.24 V as
below the band-1 p.359 `12–20 V` window. Re-measured at the
manual's specified test setting (`:FREQ 1 GHz`):

| Freq setting | TP0305 reading | Spec (p.359) | Verdict |
|--------------|----------------|--------------|---------|
| preset (post-*RST)     | 11.24 V  | — (wrong condition) | not applicable |
| **`:FREQ 1 GHz`**      | **17.54 V** | 12–20 V | ✅ OK |
| `smp_test.py` 19.988 GHz | 1.80 V | — | (bottom of RF sweep) |
| `smp_test.py` 19.994 GHz | 17.71 V | — | (top of RF sweep) |

The A8 DDS-VCO tuning voltage (TP0305) is a strong function of RF
frequency; the manual's `12–20 V` window is the nominal at
FREQ = 1 GHz. At the preset frequency (whatever that happened to be
on this unit) TP0305 was outside that window but not out of spec —
the spec simply does not apply. TP0303 (0.89 V, spec 0.5–1.5 V) and
TP0304 (0.095 V, spec 0.05–0.2 V) are also both in-spec at 1 GHz.
The main DDS loop is fully healthy.

**Diag-script fix applied.** `smp_diag.py` now parks the
instrument at `:FREQ 1 GHz` via `apply_a8_freq()` immediately
before the A8 interval is measured, so the TP0305 `12–20 V` limit
is evaluated under the manual's test condition. Post-fix reading:
TP0305 = 17.54 V ✅ (all other A8 TPs also OK).

**The "buffer VCO" (PufferSchleife) is a separate PLL** on A8 that
conditions the DDS output before it is distributed to A7, A10 (for
the FM reference), and A21 (for the sampling-IF reference via X50).
Err 221 is raised against that loop, not the main DDS.

**Why this matters for the main cascade.** A8's DDS output is the
reference the A7 step synthesis locks to, and ultimately the
103–117 MHz signal that reaches A21 X50. If the **buffer VCO** on
A8 is not locked at boot, the signal reaching A21 X50 may be
degraded in amplitude, spectral purity, or completely absent — in
which case A21 has no comb-gen drive, which is exactly what we've
observed as "TP1910 dead" in §2. This reframes the A21 diagnosis:

- **Before this finding** — TP1910 dead was attributed to A21
  comb-gen hardware or W216.10 conductor.
- **With this finding** — A21 may be healthy; the upstream buffer
  VCO on A8 may simply not be providing a usable X50 input.

**Action item (revised [Physical probe worksheet](smp_hw_diag.md) entry):** before opening A21,
check the 103–117 MHz drive path in two places: (a) A8's buffer-VCO
output at the A8 → A7 connector, and (b) the 103–117 MHz signal
arriving at A21 X50 (sourced from A7 per band-3 §7.1 p.144 — there
is no direct A8 → A21 cable). **Primary tool: spectrum analyzer**
— you want spectral purity, sidebands, and lock-glitch visibility,
not just a time-domain waveform; scope would miss the exact failure
mode for a threshold-marginal lock. Acceptable fallback if the SA
is unavailable: the 500 MHz scope at 50 Ω input (max 5 Vrms =
+27 dBm, safe direct at ≤+6 dBm drive levels) for a level-only
pass/fail, but interpret spectral content as "sine vs. mush" only.
If the signal at A21 X50 is weak or absent, work upstream: if A8
→ A7 is also weak, A8 repair precedes A21 repair; if A8 → A7 is
clean but A7 → A21 X50 is degraded, the fault is on A7 or the X50
cable. If A21 X50 has a clean 103–117 MHz @ +4…+6 dBm per §7.4
p.148, A8 is exonerated from this failure mode and the original
A21 diagnosis holds.

Note: [Step 4](smp_hw_diag.md) is the primary branch for live-path
checks. [Step 5](smp_hw_diag.md) bypasses the upstream drive and
confirms A21 end-to-end if Step 4 shows X211 absent — run the
worksheet first if you already have the A21 cover off.

**Intermittent nature re-interpretation.** The boot-to-boot err 221
variability (1/3 boots) correlates with QE bit 5 (FREQ) being
latched (present only when err 221 is also present). Classic
signature of a **threshold-marginal lock detector** — A8's buffer
VCO is locking close enough to spec that the lock-detect comparator
flips on some boots. Earlier drafts proposed A7 reference
marginality as the driver; with §3 now retracted (A7 is fully in
spec) and 6b also retracted (TP0305 is in spec at 1 GHz), the
remaining hypothesis is A8-local: aging loop-filter capacitor or
marginal lock-detect comparator on the buffer-VCO sub-loop. No
A8 DC test point currently on record is out of spec.

**Repair-order implication.** Persistent faults (err 134, err −313)
are A10-local and will not be cured by upstream repair; intermittent
err 221 is A8-local, not A7-driven.

1. Re-boot and re-run `--boot-snap` several more times to firm up
   the err-221 rate statistics.
2. Check the buffer-VCO output at the A8 → A21 X50 path per
   [Step 6](smp_hw_diag.md) (SA on X50, expected +4…+6 dBm @
   103–117 MHz).
3. err 134 (A10 FM overdriven) and err −313 (YFOM cal lost) will
   **remain** — they are A10-local and require A21 cascade repair
   plus an internal calibration re-run, not upstream fixes.

**Supersedes** the prior "A8 OK" classification in the "Modules OK"
section below. A8 standard test (DDS sweep) still passes; the boot
error 221 is on a separate sub-loop not covered by that test.

**Statistical note.** `--boot-snap` should be run after every power
cycle during the diagnostic campaign to build a sample set for the
intermittent signals. Current tally: err 221 rate 1/3, QE-FREQ
rate 1/3, perfect correlation between the two.


## Implemented Deep Checks (smp_test.py --deep)

State-dependent checks now implemented for A9, A10, A26 via `--deep` flag.

### A9 deep — state-dependent multi-range test points

A9 is variant-aware: `TestA9` calls `detect_a9_variant()` at start of
`run()` and `_check_tp()` selects the per-variant window from
`smp_common.A9_TP_RANGES`.

| TP | Check | Condition | Variant range |
|----|-------|-----------|---------------|
| 1610/1611 | Reference outputs (6199) or collector voltages (6301) | Static | 6199: ±2.75 V ; 6301: +10.4–10.8 V |
| 1615 | LF generator toggle | AM on/off | same both variants |
| 1603 | AM depth DAC | AM enabled | same both variants |
| 1604 | AM adder narrow range | AM off | 6199: 0.995–1.005 V ; 6301: 1.495–1.505 V |
| 1605 | FM DAC sweep — only the dev-1 MHz reading is checked against spec; intermediate values are reported as info because SMP02 sums low and high deviation paths with opposite signs | FM enabled at 0 / 100 kHz / 1 MHz | same both variants |
| 1612 | Diff amp offset | ALC on, sweep 10 MHz–20 GHz | same both variants |
| 1613 | Main loop min/max | POW −140/+22, sweep 10 MHz–20 GHz | same both variants |

### A10 deep — extended frequency sweep

TP1805/TP1807 at 25 frequencies: 10, 100, 500, 1000 MHz, 2–20 GHz,
plus YIG boundary (9.999/10.0/10.001 GHz).

### A26 deep — TP1910 (A21 sampling pulse gen via W216.10)

TP1910 at same 25 frequencies as A10. The reading originates on the
A21 Sampling Module daughter board A211 and is routed to A26 via cable
W216.10; A26 itself only samples it through its diagnostic
multiplexer. A freq-independent flat reading therefore indicates a
fault on A21 or in W216, not on A26.


## Functional Tests (smp_test.py)

| Test | Module | Status | Notes |
|------|--------|--------|-------|
| A4 | A4 Pulse Generator (SMP-B14) | SKIPPED | Option not installed |
| A4LF | A4 LF Generator (SM-B2, 2nd) | SKIPPED | Option not installed |
| A5 | A5 LF Generator (SM-B2, 1st) | SKIPPED | Option not installed |
| A6 | FM/ΦM Modulator (SM-B5) | ✅ PASS | TP505 NORM −2.98V, INV +2.98V, shift 5.96V; TP504 0.182V |
| A7 | Reference/Step Synthesis | ✅ PASS | TP212 monotonic 2.42→12.77V; TP215 >200mV all steps |
| A8 | Digital Synthesis | ⚠️ PASS but boot-err 221 | TP305 monotonic 1.83→17.74V (main DDS loop OK); buffer VCO reported unlocked at power-up — see §6 |
| A9 | ALC Amplifier (1035.6199.02) | ✅ PASS / ❌ DEEP | Standard OK; deep: only TP1607 aux-osc emitter (1.86V vs 1.6V max) is a real A9 fault; TP1612/1613 rails ≥2 GHz are cascade from A10 (which is itself a cascade from A21) |
| A10 | YIG PLL | ❌ FAIL / ❌ DEEP | TP1807 railed −13.61V all freqs incl. sub-2 GHz and YIG boundary — primarily a cascade from A21 (no sampling-IF); TP1802 pretune DAC is a separate A10-internal issue |
| A26 | Microwave Interface | ❌ FAIL / ❌ DEEP | TP1910 flat 0.21–0.25V across 10 MHz–20 GHz — diagnosed as A21/W216 fault, not A26 (see item 2) |

### Instrument-wide SCPI probes

| Action | What it runs | Result on this unit |
|--------|--------------|---------------------|
| `--self-test` | `*TST?` + `:TEST:RAM?` + `:TEST:ROM?` + `:TEST:BATT?` with status-register snapshots before/after (p.207 §3.6.15) | `*TST?`=0 (stub, 12 ms); `RAM`/`ROM`/`BATT`=0 OK. `QC=128` (MOD) persistent across pre/post snapshots. See `--boot-snap` / `--quest-probe --fresh-boot` for the underlying cause |
| `--quest-probe` | 16-step OUTP / AM / FM / PM / PULM walk with `:STAT:QUES:COND?` / `:EVEN?` snapshots | `QC=128` (MOD) latched across all 16 steps including `*RST` baseline — **live continuous monitor**, driven by the A10 FM-input-overdrive detector (boot error 134). Not related to A9 TP1607. `FREQ` bit 5 never re-asserts after boot — it is edge-driven only. No errors at any step (SM-B2 gating confirmed ✅) |
| `--quest-probe --fresh-boot` | Same as above plus a pre-`*RST` step-00 snapshot | **Definitive capture** — at step 00: `QE=160` (MOD+FREQ latched at boot), `ESR=136` (PON+DDE), three errors in the queue: `221 "Digital synthesis buffer VCO unlocked"`, `-313 "Calibration memory lost; YFOM"`, `134 "FM input of YFO module overdriven"`. Steps 01–16 retain `QC=128`. Resolves all prior ambiguity about QUES:MOD — see §1 retraction |
| `--boot-snap` | Read `:SYST:ERR?` queue + status registers and exit immediately on connect, no `*RST` or other writes | Preserves the boot-error queue from being flushed by any downstream action. Intended as the very first command after every power cycle |

### ✅ `TestA9.run_deep` / `--quest-probe` SOUR2 / INT2 path gated on SM-B2

The A9 deep test (and `--quest-probe` step 07) previously issued three
writes against the second internal source:

```
SOUR2:FREQ:CW 1000
SOUR2:FUNC:SHAP SIN
SOUR:AM:INT2:FREQ 1000
```

On this unit (SM-B2 LF generator option not installed) each raised
`-241 "Hardware missing"`. `SmpTest` now receives the installed-option
set at construction time (passed through from `query_options(dev)` in
the main dispatcher), and both call sites skip the SOUR2/INT2 setup
when SM-B2 is absent:

- `TestA9.run_deep` — prints `TP1615 LF gen test: SKIPPED — requires
  SM-B2 (not installed)` and proceeds to the AM DAC / AM adder / FM
  DAC tests unchanged.
- `action_quest_probe` — skips the SOUR2 setup but still arms the
  AM modulator via the default `INT1` source, so step 07 still
  exercises bit 7 (MOD) without spewing errors. Confirmed `err=0`
  at step 07 on the re-run.


## Modules OK

### A2 Supply Voltages — definitively healthy

Full sweep (`python smp_diag.py -m A2 -v`, zero jitter across three
consecutive reads on every rail):

| TP | Supply | Reading | Spec | Status |
|----|--------|---------|------|--------|
| 211 | VA24-P | +24.54 V | +22…+26 V | OK |
| 300 | VA15-P | +15.02 V | +14…+16 V | OK |
| 306 | VA15-N | −15.05 V | −16…−14 V | OK |
| 307 | VA7.5-P | +7.48 V | +7…+8 V | OK |

Closes the last loose end on A21 Step 2 ("W216 rail voltages") — W216
supply rails are being fed from known-good sources, so the A21
diagnosis of "powered and grounded correctly" stands firm.

### A3 Front Module — OK, battery fresh

Full sweep (`python smp_diag.py -m A3 -v`):

| TP | Description | Reading | Spec | Status |
|----|-------------|---------|------|--------|
| 0 | Reference ground | +0.02 V | ±0.05 V | OK |
| 1 | Input DIAG-15 | +0.22 V (jitter 0.04…0.44 V) | ±15 V | OK — floating input pickup |
| 2 | Input DIAG-5 | +0.03 V (jitter −0.03…+0.13 V) | ±5 V | OK — floating input pickup |
| 3 | X voltage | +0.02 V | 0…+10 V | OK |
| 4 | Voltmeter | +0.02 V | ±15 V | OK |
| 5 | Programming voltage FLASH | +0.02 V | no spec | INFO (only active during FLASH programming) |
| 6 | Reference voltage X-D/A | +5.02 V | +4.9…+5.1 V | OK |
| 7 | **Battery voltage** | **+3.67 V** | +3.0…+3.7 V | **OK — essentially fresh** |

TP7 at +3.67 V is 30 mV below the upper bound — the NVRAM/cal backup
battery is fresh or recently replaced, so stored calibration data
is safe and aging of the battery is not a factor in any observed
fault. TP1 / TP2 jitter is expected on unconnected front-panel DIAG
inputs (floating high-Z, mains pickup).

### A71 SM-B1 OCXO — master reference healthy

Full sweep (`python smp_diag.py -m A71 -v`, Var02 Rev01):

| TP | Description | Reading | Spec | Status |
|----|-------------|---------|------|--------|
| 100 | Reference ground | 0.00 V | ±0.01 V | OK |
| 101 | Bridge voltage thermostat | −0.09 V | no spec | INFO — ROSC v06 only, not populated on this variant |
| 102 | Output level | +2.49 V | +0.6…+2.5 V | OK (10 mV from upper bound) |

Master frequency reference is alive and within spec. TP102 sits at
the top of the window rather than drooping toward the bottom, which
is the opposite of what OCXO aging would produce — rules out a weak
reference as a contributing factor to any downstream synthesis or
PLL symptom. TP101 reading confirms this is not a ROSC v06 variant
(the `None` / INFO classification in the table is intentional).

### Other modules previously verified OK

- **A6** FM/ΦM Modulator (SM-B5) — diagnostics and functional test OK
- **A8** Digital Synthesis — partial. Standard + deep tests PASS
  (TP0305 buffer loop on at 17 V); TP0301/0302 echo point numbers
  is a known quirk. However, boot error **221 "Digital synthesis
  buffer VCO unlocked"** surfaces on `--quest-probe --fresh-boot`,
  indicating a sub-function not covered by the TP sweep. See §6.


## Resolved / Script Issues

### ✅ A9 board variant identified as 1035.6199.02

- `smp_diag.py` and `smp_test.py` originally used 6301 expected ranges
  for all A9 test points, producing false FAILs on TP1604, TP1606,
  TP1609, TP1610, TP1611 on this instrument.
- `smp_common.py` now contains a per-variant range table
  (`A9_TP_RANGES`) and dual detection: SCPI (`:DIAG:INFO:MOD?` →
  `ALCA Var04 Rev03`) and a TP1604 functional discriminator
  (6301: +1.5 V ; 6199: +1.0 V).
- `smp_test.py --detect-a9` and `smp_diag.py --detect-a9` report the
  detected variant; the variant-specific ranges are auto-applied
  when A9 is tested.
- Mapping `Var04 → 1035.6199.02` recorded in `A9_SCPI_VAR_MAP`.

### ✅ Module naming and echoed test point numbers

- `A4` remains the `SMP-B14` pulse generator slot entry
- `A4LF` models `SM-B2` fitted in slot `A4` as the 2nd LF generator,
  using TP bank `1300..1307`
- `A5` models `SM-B2` fitted in slot `A5` as the 1st LF generator,
  using TP bank `1200..1207`
- `--a5-bank` is no longer needed because the bank is now determined by
  the selected slot/module entry; `--ignore-opt` remains useful
  for explicit service probing even when `*OPT?` says an option is absent
- A8 TP0301/0302: instrument echoes point number instead of voltage
  — now detected and displayed as `ECHO` instead of misleading FAIL


## Open questions

Questions the current data cannot answer; re-evaluate after A21 +
SMP-B15 repair.

- **A10 FM-input overdrive (err 134) — cascade or independent?** After
  A21 is repaired, re-run `--quest-probe --fresh-boot`. If `QC=128` and
  err 134 clear, the A10 FM-input fault was purely a cascade symptom.
  If either persists, A10 has its own FM-adder issue (TP1812 investigation).
- **YFOM cal-memory loss (err −313) — mechanism?** Possibilities: A10
  on-module backup cell (distinct from A3 TP7), EEPROM write-cycle
  wear-out, or digital-bus comms fault preventing boot-read. Expected
  follow-up: `:CAL:ALL?` after A21 repair (SMP op. manual p.200 §3.6.9)
  and inspect for on-module M48Zxx / DS1225-family NVRAM.
- **SMP-B15 40 A section — also faulty?** Unevaluable from TP1914 alone
  while 40 B is stuck ATT. Post-40 B repair, `--att-40-exercise
  --att-cycles 2` on the TTAA row becomes the 40 A check (against V64
  THRU40A / V65 ATT40A).
- **A8 buffer-VCO lock-detect marginality — source?** Threshold-marginal
  comparator vs. aging loop-filter capacitor. No A8 DC TP currently
  out-of-spec. Await longer `--boot-snap` rate statistics and, if
  possible, scope the buffer-VCO output during an err 221 boot.
- **A9 TP1608 EXT ALC offset = −50 mV** (spec ±5 mV, 10× over). Real
  component drift or script-spec nit on an unused EXT ALC input? Defer
  unless EXT ALC use is ever required.
- **Manual sign contradiction for TP1802**: band-1 p.108 / band-2 p.168
  TP tables list `−12…−0.8 V`; §7.4.2 p.163 implies positive (`U1 = 8…
  12 V`). This instrument matches §7.4.2. If a future SMP02 reads TP1802
  negative with the same linear scaling, revisit — the TP-table sign
  may be correct on that unit.

## Open-case (physical) tasks

These require the top cover off and cannot be completed over GPIB.
Logged here so they get picked up next time the case is open.

### Fan — capture manufacturer part number

The service manual describes only the drive circuit: band-4
§7.1 p.224 confirms the `UA+12/L` fan rail is derived directly
from the transformer with no regulator, current-limited via PTC
**R170** in series. Additional designators cited in earlier drafts
of this section (N26 / V87 in the drive path; NTC R46 / comparator
N1/1 for an 80 °C overtemperature cut-off) are **per schematic
p.270 only and not verified against section text** — the scanned
band-4 PSU schematic OCRs as scrambled resistor designators
(R170, R186, R214 etc.), so those specific part references should
be treated as tentative. The manual does **not** give the fan's
manufacturer, dimensions, airflow, or current draw, and contains
no BOM or spare-parts table anywhere; the parts list simply is not
in our source PDFs.

Web search (eBay listing 255059302399 for a shared SMIQ / SME /
SMT / SMP fan assembly) confirms the fan is shipped by R&S as a
motor + control-board unit, and that the same assembly fits the
whole 02/03/04/06 generation chassis, but did not surface a part
number. Best-educated guess is an 80×80×25…32 mm ebm-papst axial
from the 8400-series (12 V, ~50–80 m³/h, ~100–250 mA) but this is
**not confirmed**.

**To capture when the case is open** (9 screws around the top
cover, unplug fan cable, lift — per band-4 §7.5 p.229):

1. Label on the fan hub — manufacturer, model, voltage, current
   (phone-camera shot is fine; hub print is usually low-contrast).
2. Frame dimensions (mm) and blade depth — calipers.
3. Connector / pinout (2-wire expected, red = +, black = 0 V).
4. Free-running speed and quiescent current at the two operating
   points: drive the unplugged fan from the **15 V current-limited
   bench PSU** at 8 V and 12 V, read current off the PSU display
   and RPM off the **tachometer**. Record both values at both
   set-points; the 8 V / 12 V pair plus the corresponding current
   draw is enough to identify the fan by catalogue cross-reference
   even without the hub label.

Matching these against an ebm-papst / Sunon catalogue will give a
concrete like-for-like replacement so the fan can be replaced
without a full R&S spares order if it ever fails. The R&S stock
number will only be obtainable from the R&S parts desk (quote
instrument S/N 848985/012) since the scanned manual does not
include it.


## Calibration investigation — closed

Question: can we back up the SMP's calibration constants to JSON and
restore them later, and are there calibration sequences worth scripting?

**Answer: no, and no.** Recorded here so this thread is not re-opened.

**SCPI `:CAL` subtree on firmware 3.70 is exactly two commands**
(Annex C, user-manual p.270):

- `:CALibration:PULSe[:MEASure]?` — triggers pulse-gen auto-cal
- `:CALibration:PULSe:DATA?` — returns fine, coarse correction pair

Both are SMP-B14-only, both are read-only. There is no `:CAL:...:DATA`
write counterpart, so even if every routine exposed a reader there
would be no path back in.

**B14 is not fitted on this unit.** Confirmed 2026-04-19 via the
on-instrument probe:

| Query | Response |
|-------|----------|
| `*OPT?` | `SM-B1, SM-B5, SMP-B11, SMP-B15` (no SMP-B14) |
| `:CAL:PULS:DATA?` | GPIB timeout → `-241 "Hardware missing"` |
| `:CAL:PULS:MEAS?` | GPIB timeout → `-241 "Hardware missing"` |

**What the customer-accessible calibration routines are** (band-1
§6.4.1, behind PASSWORD 123456 on LOCK LEVEL 1):

| Routine | Remote trigger? | Verdict |
|---------|----------------|---------|
| PULSE GEN (B14) | `:CAL:PULS:MEAS?` | n/a — option absent |
| YFOM start values | none | Front-panel only; needs ext. counter/analyser |
| ALC AMP | none | Front-panel only |
| REF OSC | `:SOUR:ROSC:INT:ADJ:VAL` + `:STATe` | DAC writable but value does not persist as cal data via SCPI |

Factory-level LEVEL, ALC LIMIT, LOOPGAIN correction tables live in
Flash EPROM on A3 and are **not reachable from SCPI at all** — the
manual states they can only be written by R&S or equipped service
centres. See also YFOM on-module NVRAM discussion in §4 above
(loss mechanism unresolved, distinct from A3 TP7).

**Conclusion.** No `smp_cal.py` is warranted. When A21/A10 are
repaired, YFOM and ALC AMP are to be re-run from the front panel;
nothing in this workflow can be automated without physically adding
the B14 option, which is unrelated to the current repair.

### Can YFOM be driven by "walking the menus" over GPIB?

No. Follow-up investigation confirmed:

- No `:KEY`, `:DISPlay:MENU`, `:SIMulate`, or equivalent key-press /
  menu-navigation SCPI exists on SMP02. The full command tree is
  Annex C (user-manual p.270–281); YFOM appears only in the
  front-panel menu description, never as a SCPI header.
- `:TEST:DIRect:YPLL` can write raw hex data to A10 subaddresses but
  (a) the subaddress map is undocumented in our scans, (b) any
  pretune DAC values we force from outside have no persistence path
  into battery-backed YFOM RAM, and (c) the manual warns it may
  damage the module.
- Operating manual p.226 explicitly directs the operator to use the
  front-panel menu after a Li-battery swap: "a calibration must be
  performed for PULSE GEN, YFOM and ALC AMP." R&S assumed manual use.

### UTILITIES/PROTECT lock is a front-panel UI gate only

Finding logged 2026-04-19 while implementing `--unlock` in
`smp_test.py` / `smp_diag.py`:

- Passwords (band-1 §6.4.1.1): L1=123456, L2=520805, L3=490727.
- FW 3.70 does **not** validate the password over GPIB. Sending
  `:SYST:PROT1:STAT OFF, 000000` (wrong pwd) sets `:STAT?` to 0 with
  an empty error queue. The manual-claimed `-224 "Illegal parameter
  value"` response is never emitted.
- With all three locks ON, the L2-gated `:SOUR:ROSC:INT:ADJ:VAL 1000`
  and `:ADJ:STAT ON` both succeeded silently. `:VAL?` returned 1000,
  `:STAT?` returned 1, no `-221` or equivalent in the queue.
- Interpretation: `:SYST:PROT<n>:STAT` only hides the corresponding
  front-panel menu items. SCPI access is not gated by it. The
  `--unlock` flag is kept in both CLIs for forward-compatibility and
  to clear the on-screen "password required" indicator, but over
  GPIB it is effectively cosmetic.


## Future Plans

### `:TEST:DIRect:*` direct-hardware subtree — deferred, service use only

The SMP02 operating manual p.207 §3.6.15 documents a `:TEST:DIRect:*`
command subtree that writes hex data strings to subaddresses on
specific hardware modules, bypassing firmware protection. Per the
manual (verbatim):

> The commands under node `:TEST:DIRect` directly act on the
> respective hardware module circumventing any security mechanisms.
> They are provided for service purposes and should not be used by
> the user. Improper use of the commands may damage the module.

Syntax: `:TEST:DIRect:<module> <subaddress>, "<hex data string>"`.

Documented module handles (p.207 ALCAS spec table):

| Handle | Module on this instrument | Potential use |
|--------|---------------------------|---------------|
| `ALCA`     | A9 ALC Amplifier (1035.6199.02) | DAC force for TP1607 aux-osc emitter regression |
| `AXIFC`    | (unknown — possibly aux interface) | needs identification |
| `DSYN0MUX` | A8 DDS0 mux / bank select | force specific synthesis path |
| `DSYN1MUX` | A8 DDS1 mux / bank select | force specific synthesis path |
| `FMOD`     | A6 FM/ΦM Modulator (SM-B5) | force VCO tune / modulator bias |
| `LFGENA`   | A5 LF Generator (SM-B2, not installed) | n/a |
| `LFGENB`   | A4LF LF Generator (SM-B2, not installed) | n/a |
| `MWIFC`    | A26 Microwave Interface | force MUX channel for live-probe |
| `PUM`      | SMP-B12/B13 pulse modulator (not installed) | n/a |
| `REFSS`    | A7 Reference/Step Synthesis | force step-synth frequency bank |
| `ROSC`     | A71 OCXO (SM-B1) | force reference path |
| `YPLL`     | A10 YIG PLL | **force YFO pretune DAC and/or tracking DAC to test A10 independently of A21 sampling-IF** |

**Why this is deferred:** the subaddress space and hex data string
semantics are not published in the operating manual. Each module's
internal register map would have to be either reverse-engineered or
obtained from a service-level document (R&S internal service
procedure, not distributed with the instrument). Running these
commands blind risks:

- Forcing a DAC beyond its valid range (damages driver stage or coil)
- Enabling an RF output or modulator with ALC bypassed (damages output
  stage or device under test)
- Corrupting non-volatile calibration data on modules with EEPROMs
  (irreversible without factory intervention)
- Driving the YIG PLL into a non-synchronized state that could stress
  the main tuning coil

**What we would use it for if the maps were available:**

1. **`YPLL` force-pretune to exonerate A10 independently of A21.** The
   current A10 DEEP FAIL is a cascade from A21 (TP1807 railed because
   the sampling IF is absent). A direct `YPLL` subaddress that sets
   the pretune DAC to a specific digital code would let us sweep
   TP1802 / TP1805 / TP1804 under commanded control and confirm A10's
   internal D/A and summing/inversion paths are healthy end-to-end,
   without relying on the PLL actually locking. This is the cleanest
   way to separate "A10 is fine, just starved" from any residual
   A10-internal fault before committing to A21 board repair.

2. **`MWIFC` force-channel on A26 MUX.** Currently `:DIAG:MEAS:POINT?`
   iterates through the diagnostic MUX in the firmware's prescribed
   order. `MWIFC` direct access would let us hold the MUX on a single
   channel for extended scope observation — useful for catching
   intermittent glitches on TP1910 that could otherwise hide between
   samples.

3. **`ALCA` force-DAC for TP1607.** The A9 deep test has TP1607 aux-
   oscillator emitter sitting at +1.86 V against a 0.7–1.1 V spec. A
   direct ALCA write could sweep the aux-osc bias DAC to see whether
   the fault is in the DAC (fixed output regardless of command) or in
   the aux-osc stage itself (responds to DAC but at wrong voltage).

4. **`REFSS` force-step to verify A7 → A21 X50 link.** ~~A7 passes all
   its internal TPs, but the signal reaching A21 X50 has not been
   independently confirmed.~~ Superseded — bench Step 4 confirmed X50
   at +3.75 dBm @ 106.56 MHz at the A21 connector (in spec after
   test-cable + DC-block losses), so A7 → A21 X50 no longer needs
   independent verification.

**When to revisit:**

- If and when R&S internal service documentation for subaddress maps
  surfaces (used-equipment re-seller service bundles, preserved
  field-service laptops, factory CD-ROMs).
- If and when an identical-revision SMP02 becomes available as a
  sacrificial unit for subaddress discovery — individual writes can
  be bisected with a current-meter on the rails to detect "this
  subaddress enables a DAC/opamp that draws +N mA".
- Alternative: traffic-sniff a genuine factory service session over
  IEC/IEEE bus to capture the actual hex-string sequences used during
  adjustment — this is the lowest-risk path but requires access to a
  functional factory service environment.

**Until then**, the `:TEST:DIRect:*` subtree is **out of scope** for
this repair. Continue with:
- Physical probing per [Physical probe worksheet](smp_hw_diag.md) (Steps 1–11) for A21
- Mechanical repair / replacement of SMP-B15 40 B section
- Re-run of all `smp_test.py -m <M> -d` tests post-A21-repair to
  confirm cascade failures clear
