# SMP02 Physical Probe Worksheet — A21 Sampling Module

Bench procedure for localising the A21 fault (TP1910 dead). Companion:
[smp_diag.md](smp_diag.md).

Instrument open, RF block accessible, A21 in place. Run `python
smp_test.py --a21-probe` in a parallel window throughout (parks SMP at
10 GHz CW / POW −30 / OUTP ON, streams TP1902 / TP1910 / TP1915 once
per second). **Step 4 is the decisive branch point**; Steps 1–3
establish prerequisites, Steps 5–11 localise per Step 4's verdict.

## While the case is open — opportunistic work

- **A9 TP1607 aux-osc scope probe** — see [smp_diag.md §1 A9](smp_diag.md#1-a9-alc-amplifier--variant-1035619902-reclassified).
  4-channel 100 MHz scope on TP1607 looking for AC swing on the
  +1.86 V DC bias.
- **SMP-B15 40 B attenuator diagnosis** — see [smp_diag.md §5 SMP-B15](smp_diag.md#5-smp-b15-att27--tp1914-pulled-low-by-40-db-b-relay-state).
  Scope on TP1914 / V67 / V68 cathodes during `smp_test.py
  --att-40-exercise`, plus measure resistance on W244 ribbon with
  instrument off.
- **Fan part-number capture** — see [smp_diag.md → Fan](smp_diag.md#fan--capture-manufacturer-part-number).
  Photograph hub label, caliper frame/blade, run free-running test
  at 8 V / 12 V on the bench PSU recording current + RPM.

## Decision tree

```
Step 4  X50 / X211 / X75       DECISIVE branch point
                                all three present → rectifier only → Step 11
                                X75 dead, inputs OK → A21 internal → Step 7
                                X50 absent, X211 absent → Step 5, then Step 6
                                X50 absent → A7 / X50 cable → Step 6
                                X211 absent → A20 / X211 cable → Step 5

Step 5  Dual-drive → X75       only if A20/YFO suspect (§7.4.4)
                                X75 pass, TP1910 pass → A21 + upstream OK; fault is X211 harness
                                X75 pass, TP1910 dead → rectifier only → Step 11
                                X75 dead → A21 internal → Step 7
```

## A21 connector interfaces

Internal A211 ports (X50, X21, X70, X75, X95, X96) are SMB snap-on
per §7 p.144. External X211 RF-IN is 3.5 mm female.

X72 appears on the p.152 placement map but is not referenced in §7.4
procedures — do not drive unless the schematic confirms role.

## Steps

### Step 1 — W216 resistance checks *(measure resistance, instrument OFF)*

Pin 1 identification first:

1. Look for a "1" silkscreen or triangle mark on the A21 board next to
   the W216 header, or a chamfer / notch on the shell.
2. The ground-return check below doubles as pin-group ID — the five
   shorts to chassis are 2/3/6/7/8, the five opens are 1/4/5/9/10.
3. Individual signal pins (1/4/5/9/10) get resolved later by polarity
   in Step 2.

Instrument OFF throughout. Two resistance checks:

**1a — W216 ground-return (< 0.2 Ω each)**. Each of W216.2/3/6/7/8 to
chassis at the A21 end should read < 0.2 Ω. Fail → broken GND pin in
W216.

**1b — W216.10 conductor (< 1 Ω end-to-end)**. A21 end of pin 10 to
TP1910 input at A26 end. Reseat both connectors while the cable is
open. Fail → repair / replace W216.

### Step 2 — W216 rail voltages *(measure DC voltage, instrument on)*

Measure DC voltage at the W216 connector on the A21 end per band-3
p.148 FSTEP, using any of W216.2/3/6/7/8 as ground reference.

Pin polarity doubles as the final pin-1 confirmation: +15 V is pin 1,
+7.5 V is pin 4, −15 V is pin 5, ~1 V is pin 9 (VARSAMP), 7.5…11 V is
pin 10 (DIAGSAMP).

Expected readings — supply pins (A26 → A21):

- **W216.1** → +15 V (+14.75…+15.25 V)
- **W216.4** → +7.5 V (+7.25…+7.75 V)
- **W216.5** → −15 V (−15.25…−14.75 V)

Expected readings — signal outputs (A21 → A26):

- **W216.9** VARSAMP → 0.9…1.1 V (A211 model-identification output,
  per p.148)
- **W216.10** DIAGSAMP → 7.5…11 V spec; **on this unit reads ~0.22 V**.
  A value in spec here means the fault has cleared between
  power-cycles; stop and re-verify the whole chain before touching
  anything else.

Failure verdicts:

- Supply rail (1/4/5) out of range → A2/A26 supply distribution is the
  fault, not A21; cross-check `smp_diag.py -m A2` (all rails OK on
  this unit).
- W216.9 out of range → VARSAMP driver problem on A211; continue.
- Significant delta A21-end vs. A26-end under load → Step 11
  (wiggle-test / W216.10 intermittent).

### Step 3 — IR thermal / rail current draw *(instrument on, optional)*

Soak at 10 GHz CW POW −30 OUTP ON for 5 min, then IR-probe A21 and
the milled casing. Any spot > 55 °C or ≥ 20 °C above A21 board
average is a hot component. Optional: break W216 at a convenient point
and measure DC current in-line on each rail. Nominal per-rail currents
are not published; > 2× a known-good A21 is abnormal.

### Step 4 — A21 I/O sanity *(SA)*

- **X50** (FSTEP from A7 via A26 distribution) — disconnect at A21
  end, SA on the free cable. Span 80–140 MHz, expected **+4…+6 dBm at
  103–117 MHz** (p.148); carrier tracks the SMP step-synth.
- **X211** (RF-IN from A20 YFO) — disconnect at A21 end, SA on the
  free cable. Command the SMP RF output to fixed CW (e.g. 10 GHz),
  expected **0…+7 dBm at
  f_RF** (p.148).
- **X75** (IF out from A21) — reconnect X50 and X211, disconnect X75
  at its A211 SMB, route to SA. Command the SMP RF output to 10 GHz CW via
  `--a21-probe`, expected **−5…+15 dBm** around 13 MHz. Re-seat the
  X50 SMB on A21 and repeat before concluding "X75 dead".

Verdicts:

- **All three present** → diag rectifier on A211 or W216.10 under load.
  **Jump to Step 11.**
- **X50 + X211 present, X75 dead** → A21-internal fault (LO chain,
  mixer, or IF amp). **Jump to Step 7.**
- **X50 absent, X211 absent** → **Run Step 5, then Step 6.**
- **X50 absent** → upstream A7 / X50-cable fault. **Jump to Step 6.**
- **X211 absent** → upstream A20 / X211-cable fault. **Run Step 5.**

### Step 5 — Dual-drive exoneration *(SA + DC–4 GHz sig-gen + 2–20 GHz sig-gen, optional)*

Per band-3 §7.4.4 p.147. Disconnect X50 and X211 at A21 and drive
both from bench sources:

- **X50** ← DC–4 GHz sig-gen at +5 dBm / 117 MHz
- **X211** ← 2–20 GHz sig-gen at 0 dBm (set 10 GHz CW or sweep the
  source slowly across 2–20 GHz)

Dual witness:

- **X75 on SA** — pass ≥ −5 dBm at fIF = 50 MHz
- **TP1910 via `--a21-probe`** — pass 7.5…11 V (DIAGSAMP at spec)

Verdicts:

- X75 pass, TP1910 pass → A20 / X211 harness fault. Swap / repair A20.
- X75 pass, TP1910 dead → rectifier only. Jump to Step 11.
- X75 dead → A21 internal fault. Go to Step 7.

### Step 6 — Internal-drive X50 check *(SA, only if Step 4 shows X50 absent)*

Reconnect X50 at the A21 end, disconnect at the other end of the X50
cable, route the free cable jack to the SA. Sweep the commanded SMP RF
frequency 2 → 20 GHz; the step-synth output will step through 103–117 MHz at
**+4…+6 dBm** (FSTEP p.148).

Pass → A7 and the X50 cable are OK end-to-end; see [smp_diag.md §6 A8](smp_diag.md#6-a8-dsyn--intermittent-boot-err-221-tp0305-retracted).
Fail → A7 step-synth output or X50 cable.

### Step 7 — A21 bias + A211 comparator state *(measure DC voltage, only if Step 4 shows X75 dead with inputs present)*

Measure DC voltage at X95 and X96 — **X95 −0.5 V ±10 %, X96 +6.3 V
±10 %** with the milled casing on (§7.4.4 p.147). Then read the A211
§7.1.7 bias-control comparator outputs (N80A–D / V85 / V89 / V90 /
V95): logic high = crowbar OK; logic low = crowbar has tripped.

- Any comparator tripped, power-cycle, re-read. Comes back nominal →
  transient, re-run Step 4 and see whether the symptom recurs.
- Re-trips immediately → the watched supply is genuinely bad
  (regulator / decoupling cap) or the MMIC that comparator protects
  has failed short.

Pass (bias nominal, no crowbar tripped) → passive RF chain downstream
of the bias is the fault → Step 8.

Alt configs (band-3 §7.4.4 / §7.5 p.147): milled casing off gives X95
≈ +0.75 V ±10 %, X96 > +6.80 V; with 68.1 Ω / 2 W / 1 % series R at
X96, X95 = −4.5 … −3 V at |I| = 80 mA.

### Step 8 — Internal-drive X21 doubler output *(SA + ≥30 dB / ≥1 W pad)*

Disconnect X21 at A211, route to SA through the mandatory ≥30 dB /
≥1 W pad. Sweep the commanded SMP RF frequency 2 → 20 GHz; expected
spectrum at X21 (§7.4.1 p.146):

- **< 0 dBm @ 103–117 MHz** (fundamental leak)
- **+26…+30 dBm @ 206–234 MHz** (doubler output, band of interest)
- **< +5 dBm @ 309–351 MHz** (3rd harmonic)

Concurrent witness: TP1910 should climb to 7.5…11 V when X21 is at
spec. If X21 meets spec but TP1910 stays at 0.22 V, jump to Step 11.
Fail (X21 dead) → doubler V50/V60 or LO amp V2/V3/V4; board swap /
factory repair.

### Step 9 — Re-read X75 after Step 8 *(SA, only if Step 8 X21 passes)*

Repeat Step 4's X75 measurement once Step 8 has confirmed X21 is at
spec. Fail → mixer V1.1/V1.2 Schottky pair, IF amp V75, or impedance
transformer; board swap / factory repair.

### Step 10 — IF-chain S21 via VNA *(optional, no LO drive needed)*

Per band-3 §7.4.2 p.146. Disconnect the internal cables at X70 (IF
amp input) and X75 (IF amp output), connect VNA port 1 → X70, port 2
→ X75, VNA output −30 dBm, measure S21 from 1 to 300 MHz.

- 10–80 MHz: |S21| > +27 dB (flat passband)
- 105–110 MHz: |S21| < −20 dB (1st LP notch, set by L72)
- 240–300 MHz: |S21| < −20 dB (2nd LP rejection)

Pass clears the IF chain only. If X21 / X75 are at spec and TP1910
remains low, continue to Step 11.

Passband low → IF amp V75 or impedance transformer. LP notch missing
or mis-centred → L72 ferrite-core trim (rotate so the 1st attenuation
peak lands at 103 MHz, per §7.4.2).

### Step 11 — Diag rectifier / W216.10 under load *(measure DC voltage + wiggle test)*

Reached when all RF chains pass but TP1910 still reads 0.22 V in
`--a21-probe`. Two possibilities left:

- Diag rectifier on A211 feeding DIAGSAMP is broken: measure DC
  voltage directly at the rectifier output on A211 (should read
  7.5…11 V when X21 is at spec).
- W216.10 conductor intermittent under load (passed Step 1b's unloaded
  resistance check but opens at operating current): wiggle-test the W216
  cable while `--a21-probe` is streaming; any TP1910 glitch confirms
  the conductor.

If both come back clean, re-run `smp_test.py -m A10 -d`; TP1807 should
leave its −13.6 V rail.

## Manual references (A21 §7, band-3)

- [p.144 §7.1 — Function description](rs_smp_corpus/volumes/band-3/pages/p0144_71-function-description_en.md) — signal chain, LO comb generation
- [p.145 §7.1.5–7.1.7 — Impedance transformer, IF amp, bias control](rs_smp_corpus/volumes/band-3/pages/p0145_715-impedance-transformer_en.md) — A211 comparator reference for Step 7
- [p.146 §7.4 / §7.4.1 / §7.4.2 — Testing and adjustment, X21 doubler spec, IF-amp S21](rs_smp_corpus/volumes/band-3/pages/p0146_74-testing-and-adjustment_en.md) — Step 8 (§7.4.1) and Step 10 (§7.4.2) spec source
- [p.147 §7.4.3 / §7.4.4 / §7.5 — Sampling module microwave tests](rs_smp_corpus/volumes/band-3/pages/p0147_744-testing-the-sampling-module-microwav_en.md) — Step 5 (§7.4.4 dual-drive) and Step 7 procedures
- [p.148 — FSTEP pinout table](rs_smp_corpus/volumes/band-3/pages/p0148_page0148.md) — W216 pin definitions, X50 / X75 level specs
- Full section (DE+EN): [band-3 §7 A21 Sampling Module](rs_smp_corpus/volumes/band-3/sections/03_ch7-a21-sampling-module.md)
