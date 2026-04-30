# SMP02 Physical Probe Worksheet — A21 Sampling Module

Bench procedure for localising the A21 fault (TP1910 dead). Companion:
[smp_diag.md](smp_diag.md).

> **Historical / superseded content** is moved to
> [`smp_history.md`](smp_history.md). Inline supersession markers in
> this doc point to specific anchors there. The doc body itself
> always reflects current truth.

Instrument open, RF block accessible, A21 in place. Run `python
smp_test.py --a21-probe` in a parallel window throughout (parks SMP at
3 GHz CW / POW −30 / OUTP ON, streams TP1902 / TP1910 / TP1915 once
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
  at 8 V / 12 V on the bench PSU recording current + RPM. OEM
  identification and Noctua replacement spec captured in
  [smp_fan.md](smp_fan.md).

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

Internal A211 ports (X50, X21, X70, X72, X75, X95, X96) are SMB
snap-on per §7 p.144. External X211 RF-IN is 3.5 mm female.

Roles per drawing 1035.8840.01 (band-3 p.156 schematic):

| Connector | Direction | Role / net | Carrier |
|-----------|-----------|------------|---------|
| X50 | A7 → A211 | Step-synth drive (103–117 MHz, +4…+6 dBm) | RF |
| X211 | A20 → A21 | YIG RF in (2–20 GHz, 0…+7 dBm) | RF |
| X21 | A211 → milled casing | **LO in** to casing comb generator, fed from on-PCB LO chain (doubler V50/V60 → LO amps V2/V3/V4 → step-recovery V4) | RF, +26…+30 dBm @ 206–234 MHz |
| X95 | A211 → milled casing | **VG** — gate-voltage bias to **A214** (pre-mixer RF amplifier on the X211 → mixer RF path; *not* the sampling mixer itself, which is a passive Schottky bridge) | DC, −0.5 V ±10 % in-circuit |
| X96 | A211 → milled casing | **VD** — drain-voltage bias to **A214** pre-mixer RF amplifier | DC, +6.3 V ±10 % in-circuit |
| X72 | A211 → milled casing | **VA15-IF** — +15 V analog supply / bias to the **A212 IF amplifier** (post-mixer, inside casing) | DC |
| X70 | milled casing → A211 | **IF out** from the in-casing A212 IF amplifier (mixer-IF after in-casing amplification — the §7.4.2 +27 dB passband spec is most plausibly the **combined casing-A212 + on-A211-A08 IF chain gain**, not A212 alone, see §7G A08 bullet for bench finding) | IF |
| X75 | A211 → A10 (W210) | IF to YIG-PLL phase detector (10–80 MHz, −5…+15 dBm), driven by the on-A211 A08 (MAR-8) IF post-amp; see §7G A08 bullet | IF |

This unit's symptom (X75 dead while X50/X211 are present) is therefore
consistent with any failure that breaks the casing-internal **A214**
pre-mixer amp / sampling mixer / **A212** IF amp chain or its
X95/X96/X72 bias feeds, or the on-PCB LO chain (X50 → X21) feeding the
casing comb generator, or the on-PCB IF chain between X70 and X75
(per §7G bench finding 2026-04-29: **L72 LP filter → DC-block cap →
A08 MAR-8 IF post-amp on its 195 Ω +15 V bias R → DC-block cap →
X75**, *not* a passive impedance transformer as earlier revisions of
this paragraph stated). Step 7's bias measurements at X95/X96 (and
implicitly X72 once the IF chain is in scope) probe the A214 /
A212-IF-amp bias feeds at the A211 side of the SMB; the A08 bias is
verified separately via DMM ohms on pin 4 to +15 V (~195 Ω expected,
see §7G A08 bullet).

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

Run results — this unit (microwave module in service position; W216
viewed from the bottom of the A21 PCB):

```
 1 3 5 7  9   -> Up
 2 4 6 8 10
```

- **1a — ground-return** ✅ pins 2/3/6/7/8 confirmed shorted to chassis,
  pins 1/4/5/9/10 confirmed open. Pin-1 location agrees with the
  layout above (upper row, leftmost when looking up at the W216 header
  from beneath the A21 PCB).
- **1b — W216.10 end-to-end** — not yet measured.

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

Run results — this unit (W216 at A21 end, ground on W216.2/3/6/7/8,
instrument on with `--a21-probe` parking at 3 GHz / POW −30):

| Pin | Signal | Expected | Measured | Verdict |
|-----|--------|----------|----------|---------|
| 1 | +15 V supply | +14.75 … +15.25 V | **+15.28 V** | OK (30 mV over upper limit) |
| 4 | +7.5 V supply | +7.25 … +7.75 V  | **+7.55 V**  | OK |
| 5 | −15 V supply | −15.25 … −14.75 V | **−15.35 V** | OK (100 mV more negative than lower limit) |
| 9 | VARSAMP (model ID) | 0.9 … 1.1 V | **+0.963 V** | OK |
| 10 | DIAGSAMP (LO detector) | 7.5 … 11 V | **+0.262 V** | **FAIL** |

> ⚠ **VARSAMP open question 2026-04-30 — schematic-vs-bench mismatch.**
> The recovered Var.02 schematic (sheet 02/02) shows the VARSAMP
> divider as `R30 = 8K25` / `R31 = 562 R` between +7,5 V and GND,
> predicting V_VARSAMP ≈ 7.5 × 562 / (8250 + 562) ≈ **0.479 V** at
> nominal +7,5 V — inconsistent with both the spec window above and
> the bench-measured **+0.963 V**. Possible explanations: (a) the
> schematic read of `R30` is wrong (image is grainy); (b) the +7,5 V
> net at this divider is actually ≈ 15 V on the variant; (c)
> different divider values on the bench unit vs the schematic. **No
> values are changed pending a higher-res schematic re-check** — see
> §7D DEEPER SCHEMATIC RE-READ banner final paragraph and the
> `smp_next.md` planning block "Comparator inputs + X21 last stage".

DIAGSAMP at the A21 end agrees with the SCPI TP1910 reading
(0.21–0.25 V across all 25 deep-sweep frequencies in
[smp_diag.md §2](smp_diag.md#2-a21-sampling-module--sampling-pulse-generator-dead)),
so W216.10 is conducting under load and the dead reading is sourced on
A21/A211 — not a broken pin-10 wire. VARSAMP healthy in spec confirms
W216 supply pins, ground returns, and the A211 model-ID rectifier are
all functional. **Forward reference (per §7D revised topology, with
caveat per §7D DEEPER SCHEMATIC RE-READ banner item 2):** the
DIAGSAMP signal path is **bench-traced as passive** (A0 + 1002 +
shunt cap, no op-amp involvement), although the rectifier itself
sits on the off-image right-margin strip of the recovered Var.02
sheet 02/02 (W216 enumerates pins 1–9 only on the visible portion;
W216.10 is absent from the visible pinlist). Taking the bench trace
as correct, the dead reading is **upstream LO collapse**, not a
broken DIAGSAMP rectifier; DIAGSAMP would recover automatically
once the LO chain is restored and X21 comes back. (Note that the
§7E rebuild premise has itself been shifted by the schematic — see
§7D DEEPER SCHEMATIC RE-READ banner; chips are presumed alive
pending Step D.5 / Step 8a.) Supply rails are marginal-high (pin 1 +30 mV, pin 5
−100 mV outside the band-3 p.148 window) but well within A2's own
rated tolerance on this unit and not implicated by any other fault
witness; classified OK pending corroboration if other A26-fed boards
ever show the same skew.

### Step 3 — IR thermal / rail current draw *(instrument on, optional)*

Soak at 3 GHz CW POW −30 OUTP ON for 5 min, then IR-probe A21 and
the milled casing. Any spot > 55 °C or ≥ 20 °C above A21 board
average is a hot component. Optional: break W216 at a convenient point
and measure DC current in-line on each rail. Nominal per-rail currents
are not published; > 2× a known-good A21 is abnormal.

### Step 4 — A21 I/O sanity *(SA)*

- **X50** (FSTEP from A7 via A26 distribution) — disconnect at A21
  end, SA on the free cable. Span 80–140 MHz, expected **+4…+6 dBm at
  103–117 MHz** (p.148); carrier tracks the SMP step-synth.
- **X211** (RF-IN from A20 YFO) — disconnect at A21 end, SA on the
  free cable. Command the SMP RF output to fixed CW (e.g. 3 GHz, the
  `--a21-probe` default), expected **0…+7 dBm at f_RF** (p.148).
- **X75** (IF out from A21) — reconnect X50 and X211, disconnect X75
  at its A211 SMB, route to SA. Command the SMP RF output to 3 GHz CW via
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

Run results — this unit (Siglent SSA, 2 m lossy SMB cable + DC block on
SA input; SMP via `--a21-probe` at 3 GHz CW / POW −30):

- **X50 free cable** — peak **+3.75 dBm @ 106.56 MHz**. Carrier in band
  and level consistent with +4…+6 dBm spec after cable + pigtail +
  DC-block losses → **present**.
- **X75 free cable** — no signal 0–100 MHz, floor < −55 dBm → **dead**.
- **X211 measured at A20 X202 jack** (cable disconnected at A20, SA on
  the free X202 connector) — **+0.22 dBm @ 2.912533 GHz**. This is the
  YIG output unloaded; both deviations (level at the bottom of spec,
  ~87 MHz below the commanded 3 GHz) are **expected downstream
  consequences of the X75-dead fault**: with X75 dead the A10 YIG-PLL
  has no sampling-IF, N500 rails (TP1807 = −13.62 V), the FM / tracking
  coils saturate (TP1809 / TP1811 clipping, TP1812 = +9.03 V → boot
  error 134 "FM input of YFO module overdriven", error −313 YFOM cal
  lost), and the YIG (A20) cannot lock to the commanded f_RF. See
  [smp_diag.md §4](smp_diag.md#4-a10-yig-pll--pretune-dac-ok-pll-cascade-from-a21-remains)
  for the cascade analysis. **Mechanical note:** the X202 nut at A20
  was finger-loose; the disconnected-end measurement above does not
  depend on in-circuit nut torque, but a loose X202 in normal operation
  could still attenuate the RF arriving at A21 X211 enough to starve
  the sampling mixer and produce the X75-dead symptom on an otherwise
  healthy A21.

Per the decision tree this maps to *X50 + X211 present, X75 dead →
A21-internal* → **Step 7**. The cable-torque exclusion in Step 4.5
below was run first as a $0 sanity check; it did **not** cure X75
(see Step 4.5 run result), so the A21-internal verdict stands.

#### Step 4.5 — re-torque X202↔X211, re-measure X75 *(complete)*

Procedure:

1. Power off. Disconnect both ends of the X202↔X211 cable, inspect the
   3.5 mm centre pins, finger-engage and torque each nut to the 3.5 mm
   spec (≈8 in-lb / 0.9 N·m). While the case is open, re-seat the X50
   and X75 SMBs on A21 the same way.
2. Power back up, start `smp_test.py --a21-probe` (3 GHz CW / POW −30).
3. Repeat the Step 4 **X75** measurement: disconnect X75 at its A211
   SMB, route through the same Siglent SSA + 2 m cable + DC block, span
   0–100 MHz, look for −5…+15 dBm peak around 13 MHz.

Verdicts:

- **X75 now in spec** → loose X202 was the root cause. A10 PLL should
  re-lock once IF is restored — re-run `smp_test.py -m A10 -d` and
  `smp_test.py --quest-probe --fresh-boot` to confirm TP1807 leaves
  its −13.62 V rail and boot errors 134 / −313 clear. Updates to
  [smp_diag.md §2 / §4](smp_diag.md#2-a21-sampling-module--sampling-pulse-generator-dead) once observed.
- **X75 still dead** → cable / connector excluded; A21-internal fault
  candidate stands. Proceed to **Step 7**.

Run result — this unit: X202↔X211 cable re-torqued at both ends,
X75 **still dead** (no signal 0–100 MHz, floor < −55 dBm, unchanged
from the pre-retorque trace). X202↔X211 connector / cable is therefore
**excluded** as a root cause. Combined with Step 1/2 results (W216.10
conducting under load, VARSAMP healthy → A21 supplies and ground
returns OK) and Step 4 (X50 present, X211 present at YIG output), the
fault is now firmly localised to **A21-internal**. **Next: Step 7
(A21 bias + A211 comparator state).**

### Step 4-X50 — In-instrument X50 → X21 LO-chain probe *(SA + low-cap probe; planned 2026-05-03)*

Stage-by-stage in-circuit validator for the X50 → X21 LO chain,
intended as the next move after Step 4.5 excluded the X202↔X211
cable. Splits the chain at **R65** (0 Ω jumper at the FREQUENCY
DOUBLER ↔ LO AMPLIFIER boundary on sheet 02/02 of drawing
1035.8840.01). Lifting one end of R65 gives a clean, reversible
hard break between the two halves of the chain — pickoff *or*
injection, both into 50 Ω, no high-Z probing concerns. R67 121 Ω
sits immediately right of R65 as the series match into V2 BFG97
base; R66 750 Ω is the shunt that completes the V2 input divider.

In-instrument alternative to Step 8a: keeps A211 mounted, no bench
PSUs on W216, no §7G LP365M / V85 / V89 supervisor caveats (those
apply only to bench-PSU cold bring-up of +7.5 V). A pass at Stage 5
closes the §7D D.3 silicon question by exclusion the same way Step
8a does.

Topology (left → right on the schematic, X50 to X21):

```
X50  → R49 8R25 → C50 → V50 (AT-42085-B 420 #1)
                          → R51 / interstage → V60 (AT-42085-B 420 #2)
                          → V61 / V62 (HSMS-2800-B Schottky doubler pair)
                          → L62 / L65 / caps   (post-doubler LP filter)
                          → R65 0R   ◄── lift here for the patch
                          → R67 121R (series match)
                          → V2 BFG97-B (LO pre-driver)
                          → V3 / V4 MRF3866-B / MRF5160-B (class-AB push-pull)
                          → L45 54nH / C49 10pF (output match, DC-block)
                          → X21 (+26..+30 dBm @ 206–234 MHz, into casing)
```

Setup throughout: instrument on, `python smp_test.py --a21-probe`
running (parks SMP at 3 GHz CW / POW −30 / OUTP ON, FSTEP carrier
≈ 110 MHz at X50). SA = Siglent SSA + 2 m cable + DC-block as in
Step 4. Stages 1, 2, 4, 5 use a low-cap probe (FET probe, active
probe, or a soldered-on 1–2 cm tail wire to short coax + 100 nF
DC-block). Stage 3 uses a hard coax connection at the lifted R65
pad — no probe loading concerns.

**Procedure:**

```
+---+--------------------------------------------------------+----------+
| # | Stage                                                  | Time     |
+---+--------------------------------------------------------+----------+
| 0 | Pre-flight — re-confirm Step 4 X50 reading reproduces  |   2 min  |
|   | (+3.5..+5 dBm peak ~106 MHz on the disconnected free   |          |
|   | cable into SA). If drifted, re-Step-4 first.           |          |
| 1 | X50 *into* A21 — low-cap probe at A21-side pad of R49  |   5 min  |
|   | (8R25 input series R, next to X50 SMB). Sweep SMP RF   |          |
|   | 2 → 20 GHz; FSTEP sweeps 103 → 117 MHz. Expect         |          |
|   | −5..0 dBm at swept f_FSTEP (≈ −5..−6 dB below the      |          |
|   | free-cable reading, lost to R49 + V50 input match).    |          |
| 2 | V50 / V60 cascade output — low-cap probe at V60        |   5 min  |
|   | collector pad. Expect clean fundamental at f_FSTEP,    |          |
|   | level ≈ +10..+18 dBm depending on cascade gain. Drop   |          |
|   | to V50 collector pad if weak to localise which 420.    |          |
| 3 | **R65 patch — hard break at the doubler/LO-amp**       |  10 min  |
|   | boundary. Power off. **Lift the right (R67-side) end   |          |
|   | of R65** with iron + tweezers. Solder a short 50 Ω     |          |
|   | coax tail to the still-attached (doubler-side) pad,    |          |
|   | route to SA via 100 nF DC-block; SA in 50 Ω input,     |          |
|   | span 50–500 MHz, RBW 100 kHz. Power on, `--a21-probe`  |          |
|   | running, capture trace at f_FSTEP = 110 MHz commanded. |          |
|   | Expected at the doubler-side pad of R65 (post-LPF, no  |          |
|   | V2 base loading because R65 is open):                  |          |
|   |   • **2f = 220 MHz dominant**, several dB above        |          |
|   |     residual fundamental                               |          |
|   |   • Fundamental leak at 110 MHz visible but            |          |
|   |     suppressed                                         |          |
|   |   • 3f at 330 MHz lower still                          |          |
|   | Power off after capture. Leave R65 lifted for Stage 3b |          |
|   | if running, otherwise re-flow before Stage 4.          |          |
| 3b| (optional) **R65 patch — bench injection** into LO-amp |  10 min  |
|   | half only. Re-flow R65 onto the V2 / R67 side only     |          |
|   | (jumper now hangs free on the doubler side). Solder    |          |
|   | a coax tail to the V2-side pad of R65, drive from      |          |
|   | bench source at +0 dBm CW / 220 MHz (mid-band 2f).     |          |
|   | Power on. Capture at X21 (Stage 5 method). A clean     |          |
|   | +26..+30 dBm at X21 confirms LO-amp half (V2/V3/V4 +   |          |
|   | match) is healthy and the dead chain is *upstream*     |          |
|   | (doubler / cascade / X50 input network).               |          |
| 4 | R67 right pad and BFG97 collector tab — re-flow R65    |   5 min  |
|   | back across both pads. Low-cap probe at R67's V2-side  |          |
|   | pad (= V2 base node): expect 2f at 220 MHz, ~2..4 dB   |          |
|   | lower than Stage 3 reading (R65/R67 + R66 750R bias    |          |
|   | divider loss). Then move probe to BFG97 collector tab  |          |
|   | (cold side of L70 220nH RFC pickoff): expect 2f at     |          |
|   | 220 MHz, **~+5..+10 dBm** (BFG97 ≈ +10 dB driver gain  |          |
|   | into V3/V4 base node).                                 |          |
| 5 | V3 / V4 commoned collector node — low-cap probe at the |   5 min  |
|   | cold side of L45 54 nH (before C49 DC-block). Expect   |          |
|   | 2f at 220 MHz, **+26..+30 dBm**. **Use a ≥30 dB /      |          |
|   | ≥1 W in-line pad on the SA input** — equivalent to the |          |
|   | Step 8 / 8a X21-brass-pin SA capture, but reachable    |          |
|   | in-instrument without unmating X21 from the casing.    |          |
+---+--------------------------------------------------------+----------+
```

**Decision matrix (Stages 1–3):**

```
+---------------------------+---------------------------+--------------+
| Stage 1 / 2 result        | Stage 3 result            | Verdict      |
+---------------------------+---------------------------+--------------+
| f_FSTEP present at R49    | 2f dominant at R65 left   | LO-amp half  |
| and V60 collector         | pad (~210–230 MHz)        | suspect →    |
|                           |                           | Stages 4+5;  |
|                           |                           | 3b optional  |
|                           |                           | confirms by  |
|                           |                           | exclusion    |
| f_FSTEP present at R49    | Only fundamental at R65   | Doubler half |
| and V60 collector         | left pad, no 2f           | dead — V61/  |
|                           |                           | V62 HSMS-    |
|                           |                           | 2800 pair or |
|                           |                           | post-doubler |
|                           |                           | LPF (L62/L65 |
|                           |                           | / caps)      |
|                           |                           | collapsed.   |
|                           |                           | Power off,   |
|                           |                           | OOC junction |
|                           |                           | sweep on     |
|                           |                           | V61/V62;     |
|                           |                           | DMM ohm on   |
|                           |                           | L62/L65.     |
| f_FSTEP present at R49    | Nothing at R65 left pad   | V60 → R65    |
| and V60 collector         | (neither f nor 2f)        | trace open;  |
|                           |                           | re-check     |
|                           |                           | Stage 2 then |
|                           |                           | DMM-ohm the  |
|                           |                           | post-doubler |
|                           |                           | filter chain |
|                           |                           | with         |
|                           |                           | instrument   |
|                           |                           | off.         |
| f_FSTEP present at R49,   | n/a                       | V50 or V60   |
| weak / absent at V60      | (skip Stage 3 until       | dead. Power  |
| collector                 | cascade restored)         | off, OOC     |
|                           |                           | junction +   |
|                           |                           | bias-net     |
|                           |                           | check on     |
|                           |                           | the dead     |
|                           |                           | 420.         |
| f_FSTEP absent at R49     | n/a                       | Bad SMB      |
|                           |                           | centre pin / |
|                           |                           | cracked R49  |
|                           |                           | / lifted     |
|                           |                           | C50. Power   |
|                           |                           | off, repair, |
|                           |                           | re-test from |
|                           |                           | Stage 1.     |
+---------------------------+---------------------------+--------------+
```

**Decision matrix (Stages 4–5, only if Stage 3 confirms 2f at R65 left pad):**

```
+--------------------------+--------------------------+----------------+
| Stage 4 result           | Stage 5 result           | Verdict        |
+--------------------------+--------------------------+----------------+
| 2f at R67 V2-side and    | +26..+30 dBm 2f at V3/V4 | LO chain end-  |
| at BFG97 collector       | collector tie node       | to-end healthy |
| (~+5..+10 dBm)           |                          | → re-check X75 |
|                          |                          | dead premise;  |
|                          |                          | fault is IF /  |
|                          |                          | casing side.   |
|                          |                          | Pivot to       |
|                          |                          | Step 8b /      |
|                          |                          | Step 10a.      |
| 2f at R67 V2-side, BFG97 | n/a (skip — Stage 4      | V2 BFG97 dead  |
| collector dead           | already isolates)        | or its bias /  |
|                          |                          | L70 collector  |
|                          |                          | RFC open.      |
|                          |                          | Power off,     |
|                          |                          | DMM-ohm L70    |
|                          |                          | + V2 base      |
|                          |                          | bias divider.  |
| Nothing at R67 V2-side   | n/a                      | R67 121R open  |
| despite Stage 3 pass     |                          | or R66 750R    |
|                          |                          | shorted to     |
|                          |                          | GND. Power     |
|                          |                          | off, ohm both. |
| 2f at R67 V2-side and    | < +13 dBm at V3/V4       | V3 / V4 push-  |
| BFG97 collector clean    | collector tie node       | pull stage is  |
|                          |                          | the fault →    |
|                          |                          | §7D D.3 stands |
|                          |                          | for *this*     |
|                          |                          | unit. Commit   |
|                          |                          | to §7E rebuild |
|                          |                          | (3866 + 5160)  |
|                          |                          | with the D.5   |
|                          |                          | ohm gate.      |
+--------------------------+--------------------------+----------------+
```

**Risks and mitigations:**

- **R65 pad lift on rework.** R65 is a 0R 0603/0805 — single iron
  pass + tweezers on the V2 side. Use flux, low-temp solder for
  the patch coax tail, re-flow back to original position when
  done. If a pad lifts, jumper across the lift with 30 AWG wire
  before powering up.
- **Hot RF on Stage 5.** V3 / V4 collector tie node is at
  +26..+30 dBm. **Always** insert ≥30 dB / ≥1 W in-line pad
  *before* connecting to the SA front end. Same rule that applies
  to direct X21 / X75 SA captures applies here.
- **Probe loading on Stages 4 / 5.** A standard ÷10 passive scope
  probe (10–15 pF tip) loads the 220 MHz nodes by 3+ dB and can
  detune the L45 / C49 output match enough to mask a real fault.
  FET / active probe or a soldered tail wire only.
- **Bench source for Stage 3b.** Needs a clean +0 dBm CW at
  220 MHz; any spectrally dirty source (harmonics within 20 dB
  of fundamental) confounds the X21 verdict. 8648-class sig-gen
  or better.

**Sequencing vs Step 8a:** Step 4-X50 is the in-instrument
counterpart — pick it if you want to keep A211 mounted and avoid
bench-PSU wiring on W216; pick Step 8a if you want the most
thorough silicon-question closure with the board out of casing.
A pass at Stage 5 closes §7D D.3 / §7F doubler-location / §7G
push-pull-vs-detector by exclusion the same way Step 8a does.
Total time ~30–40 min for Stages 0–3 (decisive split); add ~15 min
for Stages 4+5 if LO-amp half is the suspect; add ~15 min for
Stage 3b if running the injection confirmation.

Run results — this unit: *(not yet run; bench session pending —
see [`smp_next.md`](smp_next.md) tracker entry)*

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

Schematic: **drawing 1035.8840.01** = band-3 p.156 *Sampling Modul*
schematic (figure `p0156_stromlauf-gilt-fuer-var02.jpg`, valid for
Var.02 → matches A211 1035.8840.02 on this unit) + band-3 p.152
parts XY-list (positions of N80, V85/89/90/95, R98, X95/X96).

⚠ **Instrument off whenever A211 is split from or re-mated to the
milled casing** (§7.4 p.146 explicit: *"Disconnection or connection
of the two components is only allowed with the current supply cut
off!"*). Powering up half-mated risks driving the GaAs-FET MMIC
outside its bias window and tripping crowbars you are trying to read.

Measure DC voltage at X95 (**VG**, gate-bias to **A214** — the
in-casing pre-mixer RF amplifier on the X211 → sampling-mixer RF
path; the sampling mixer itself is drawn as a passive Schottky bridge
with no DC bias) and X96 (**VD**, drain-bias to A214) — **X95 −0.5 V
±10 %, X96 +6.3 V ±10 %** with the milled casing on (§7.4.4 p.147,
in-circuit). Optional but useful: also spot-check X72 (**VA15-IF**,
+15 V analog supply / bias to the in-casing **A212 IF amplifier**) —
should track the A26 +15 V rail (≈ +15.28 V on this unit per Step 2).
Then read the A211 §7.1.7 bias-control state — but on A211 var.02
**N80 (quad comparator), V85 and V89 (cut-off switches) live on Side A
and are *not* reachable through the cover cut-out** (no silkscreen on
this PCB; component IDs below were determined by package + topology
tracing, not by silkscreen). Step 7B is therefore staged: Side B
checks first (N90 / V90 / V95 / R98 reachable through the cut-out),
escalate to Side A only if both X95 and X96 read dead.

> ⚠ **LP365M N.F. on Var.02 — caveat 2026-04-30.** Per the recovered
> schematic ([sheet 02/02](rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg)),
> on this Var.02 PCB the LP365M chip itself (N80-E), the input-divider
> ladder R80–R85, and the ISET R109 274 K are **all marked N.F. (nicht
> bestückt / not fitted)**. The "any comparator tripped" rule below
> therefore has **no LP365M to trip** on this variant — Side-A
> escalation is moot, and the §7.1.7 supervisor / V85 / V89 crowbar
> chain applies to a different sub-variant of A211. The Side-B bias
> chain probed by Table B (N90 OP97FS + V90 BUZ71 + R98 + X95/X96)
> is independent of LP365M and remains the operative test on this
> unit. See §7D DEEPER SCHEMATIC RE-READ banner item 3 for the full
> N.F. inventory.

- Any comparator tripped, power-cycle, re-read. Comes back nominal →
  transient, re-run Step 4 and see whether the symptom recurs.
- Re-trips immediately → the watched supply is genuinely bad
  (regulator / decoupling cap) or the MMIC that comparator protects
  has failed short.

Pass (bias nominal, no crowbar tripped) → passive RF chain downstream
of the bias is the fault → Step 7D (X21 LO ALC sanity check, DMM only)
→ Step 8 (X21 SA sweep with the ≥30 dB / ≥1 W pad).

Alt configs (band-3 §7.4.4 / §7.5 p.147, **A211 PCB withdrawn from
the milled casing** — power off the instrument before separating):
open-circuit X95 ≈ +0.75 V ±10 %, X96 > +6.80 V; with 68.1 Ω / 2 W /
1 % series R at X96, X95 = −4.5 … −3 V at |I| = 80 mA.

**A211 var.02 component layout (this unit, bench-confirmed via package
+ topology — no silkscreen present)**

Side B (heavily populated, the side facing the cover cut-out — what
Step 7B probes through the open shield):

- **N90 = OP97FS** (PMI/AD precision low-power op-amp, SOIC-8) —
  drain-current control loop, supplied from ±15 V (pin 7 / pin 4).
  Pin 3 (+) ties to the BUZ71 drain net (= unregulated +V input rail
  to the pass element); pin 6 (out) → BUZ71 gate; pin 2 (−) ties to
  the X96 side of R98 (load-voltage sense). Loop reference / set-point
  is built from the **750 Ω** (marked `7500`) and **10 kΩ** (marked
  `1002`) precision resistors in the cluster — these are *not* the
  current sense and would be impossible at 80 mA across them.
- **V90 = BUZ71** (Siemens N-channel power MOSFET, TO-220, "M" logo +
  date code, marked `V430`) — high-side pass element. Bench-confirmed
  topology: D = +V_unreg input rail, S = R98 → X96 output side, G
  driven from OP97 pin 6 (V_GS ≈ +3.1 V in active region).
- **R98** — drain-current sense, in series between BUZ71 **source**
  and X96 brass pin. Bench-measured **≈ 0.1 Ω** (sub-ohm precision,
  in-circuit DMM reading inflated to 0.2 Ω by test-lead resistance).
  Target current 80 mA per §7.4.4 → V_R98 ≈ 8 mV at spec.
- **SOT-23 marked "A0"** — the only SMD diode visible in the
  Side-B cut-out. Bench-traced to the **passive DIAGSAMP rectifier**
  on the X21 RF tap, **not** the X21 LO ALC envelope detector as
  earlier inference had it. Pin 3 = anode, sitting on the X21 RF
  tap node (same node as the top of the 10 kΩ `1002` series
  isolation R); pin 1 = cathode, hard to GND (same GND as the
  shunt cap on the W216.10 / DIAGSAMP node downstream of `1002`);
  pin 2 truly NC. The trio A0 + 1002 + shunt cap forms a passive
  envelope rectifier whose filtered DC output is W216.10
  (DIAGSAMP); there is **no AGC op-amp on this path**. Two-terminal
  Schottky single (low-barrier family) — identity confirmed by
  comparison against two other "A0"-marked SOT-23 parts elsewhere
  on the PCB, all three reading pin 1↔pin 2 OL and pin 2↔pin 3 OL,
  with Vf ≈ 0.23 … 0.27 V forward at DMM diode-test current on the
  two healthy refs. The 3866 / 5160 AGC loop's envelope sense path
  taps the X21 RF node through a separate cap + L1-Cshunt-L2 LPF
  onto the commoned base node of both chips — see §7D revised
  topology. Detail in Step 7D below.
- **V95** (X95 gate-bias generator) is **not** in the Side-B cut-out;
  location unknown (likely Side A, or implemented as a divider from
  −15 V rather than a discrete transistor). Verified working in-
  circuit by Table A row 1 (X95 = −0.72 V at the brass pin, within
  device-spread tolerance for an A214 GaAs-FET).

Side A (component side per p.152, **not visible** through the cover
cut-out — only reachable by separating A211 from the casing per §7.4 /
§7.5, instrument off):

- **N80** at A / 41 / 17 — **LP365M-L** quad comparator (per recovered
  schematic, confirmed 2026-04-30; the earlier LM339-class generic
  reading is withdrawn — LP365M is a low-power LinCMOS quad
  comparator, pin-compatible with LM339 but with µA-class quiescent).
  §7.1.7 crowbar comparators on the controlled supplies.
  **N.F. on Var.02 (per schematic 2026-04-30):** the schematic marks
  N80-E itself, the input-divider ladder R80–R85, and the ISET R109
  274 K all "N.F." (nicht bestückt / not fitted). Two top divider
  resistors R102 100 K + R103 56 K2 and the −15 V leg R86 100 K +
  R87 61 K9 + R88 3 K92 remain populated as a divider stub of unknown
  destination (one of the still-fitted-divider candidates is whatever
  net the comparator inputs would have monitored — probably a sense
  divider on a controlled supply, see §7D DEEPER SCHEMATIC RE-READ
  banner item 3 and the next-bench-trace plan in `smp_next.md`). Net
  consequence: on this Var.02 PCB there is **no LP365M wired-OR
  fault node**, and the §7.1.7 crowbar / V85 / V89 cut-off chain
  applies to a different sub-variant.
- **V85 / V89** — supply cut-off switches in series with the MMIC bias
  rails, gates driven from N80 outputs (logic high = OK, low = tripped).
  Likely clustered around N80 on Side A. **N.F. on Var.02 by extension**
  (gates would be driven by the N.F. LP365M outputs).

Practical consequence: **all of Step 7B can be done from Side B alone
unless both X95 and X96 read out of spec at the brass pins** — that's
the only case that needs Side A access to distinguish "Side-A cut-off
latched" from "Side-B N90 / BUZ71 / R98 broken".

**Pin labelling — the 5 right-edge brass casing-side pins on Side B
carry no silkscreen on this PCB.** Use DC voltage to label them
(instrument on, `--a21-probe` running, ground on chassis or
W216.2/3/6/7/8) **before** any RF probing — X21 carries +26…+30 dBm LO
and must not be SA-probed bare:

| DMM reading on the brass pin | Pin identity | Role |
|---|---|---|
| **−0.5 V ±10 %** | **X95** | VG to A214 pre-mixer amp (gate bias) |
| **+6.3 V ±10 %** | **X96** | VD to A214 pre-mixer amp (drain bias) |
| **≈ +15 V** (tracks W216.1) | **X72** | VA15-IF to A212 IF amp |
| **≈ 0 V DC**, AC content present | **X70** | IF return from A212 |
| **≈ 0 V DC, do NOT SA-probe bare** | **X21** | LO into casing comb gen, +26…+30 dBm |

Run results — this unit (fill in at the bench; ground reference =
W216.2/3/6/7/8 or A21 chassis):

**A. Bias DC at the brass casing-side pins** *(in-circuit, casing on,
`--a21-probe` running at 3 GHz / POW −30; pin labels assigned by the
DC-sweep table above)*

| Node | Brass pin identified by | Role | Expected | Measured | Verdict |
|------|-------------------------|------|----------|----------|---------|
| X95 (VG) | DC ≈ −0.5 V | Gate-voltage bias to **A214** pre-mixer RF amp (NOT the sampling mixer — passive Schottky), A211 → casing | −0.5 V ±10 % (−0.55 … −0.45 V) | **−0.72 V** | slightly past nominal (−31 %); loop *is* regulating; consistent with A214 GaAs-FET on the high-pinch-off / high-Idss tail of the device-spread, not a circuit fault → **accept** |
| X96 (VD) | DC ≈ +6.3 V | Drain-voltage bias to **A214** pre-mixer RF amp, A211 → casing | +6.3 V ±10 % (+5.67 … +6.93 V) | **+6.173 V** | in spec → **OK** |
| X72 (VA15-IF) | DC ≈ +15 V | +15 V analog supply / bias to in-casing **A212 IF amplifier** (post-mixer), A211 → casing | ≈ +15 V (tracks A26 +15 V supply, currently +15.28 V at W216.1) | **+14.98 V** | tracks W216.1 (≈ 300 mV drop across casing-side decoupling) → **OK** |

**B. A211 Side-B bias-chain probe sequence** *(instrument on,
`--a21-probe` running, casing on; component IDs per the A211 var.02
layout above — N90 = OP97FS, V90 = BUZ71, V95 = SOT-23 "A0")*

| # | Probe point | Expected (nominal op) | Measured | Verdict |
|---|-------------|-----------------------|----------|---------|
| 1 | OP97 pin 7 (V+ supply) | ≈ +V_supply rail | **+15.08 V** | clean +15 V rail → **OK** |
| 2 | OP97 pin 4 (V− supply) | 0 V or −V_supply rail | **−15.25 V** | clean −15 V rail (bipolar supply) → **OK** |
| 3 | OP97 pin 6 (output → BUZ71 gate) | mid-range, **NOT** railed to either supply | **+9.32 V** | well clear of both rails → loop active, NOT saturated → **OK** |
| 4 | BUZ71 V_GS (gate − source) | a few volts above V_th (≈ 3 … 5 V) → V90 in active region | **≈ +3.14 V** (V_G = +9.32 V, V_S ≈ +6.18 V) | above V_th → V90 in active region → **OK** |
| 5 | V across R98 (BUZ71 source → X96) | I_drain × R98, mV-scale; I = V/R98 ≈ 80 mA target (§7.4.4) | **7.4 mV** across R98 ≈ 0.1 Ω → **I_drain ≈ 74 mA** | within ~7 % of the 80 mA target → **OK** |
| 6 | "A0" SOT-23 base/gate | driven from upstream gate-voltage reference | *(not probed — X95 net at brass pin already characterised, see row 7)* | n/a |
| 7 | "A0" SOT-23 collector/drain (= X95 net) | −0.5 V ±10 % (matches X95 brass pin) | **−0.72 V** (= X95 brass-pin reading) | as Table A row 1 → device-spread, accept |

**B.1 Decision matrix** — read after Tables A and B are filled:

| X95 / X96 (Table A) | OP97 pin 6 (B#3) | Verdict |
|---------------------|------------------|---------|
| both in spec | mid-range | bias chain OK → fault is downstream RF/IF → **Step 7D** (X21 LO ALC, DMM only) before **Step 8** |
| X96 dead | railed high (≈ +V_supply) | loop driving hard, no current flowing: BUZ71 open, R98 open, **or** Side-A cut-off (V85/V89) tripped → **escalate to Side A** |
| X96 dead | railed low (≈ 0 V / −V_supply) | overcurrent shutdown: R98 shorted, BUZ71 D–S short, or MMIC short → power off, ohm-out R98 + BUZ71 |
| X96 dead | mid-range *and* OP97 pin 7 / 4 also 0 V | N90 itself unpowered / dead → trace OP97 supply rails upstream |
| X96 in spec, X95 dead | any | V95 ("A0" SOT-23) or its drive path → measure V_BE / V_GS on "A0", trace base/gate to upstream reference |

**Run verdict (this unit):** Tables A & B match decision-matrix row 1 —
X96 in spec, X95 within device-spread tolerance, OP97 pin 6 mid-rail at
+9.32 V, BUZ71 in active region, I_drain ≈ 74 mA across R98 ≈ 0.1 Ω.
**§7.1.7 bias chain PASSED end-to-end** — fault is *not* in N90 / V90 /
R98 / V95. Side-A escalation **not** required. Proceed to **Step 7D**
(X21 LO ALC, DMM only) before Step 8.

**Side-A escalation rule** — only required when both X95 and X96 read
dead *and* OP97 pin 6 is railed high. Power down, separate A211 from
the milled casing per §7.4 / §7.5, access N80 outputs + V85/V89 on
Side A. Any N80A–D output low or V85/V89 in cut-off → a crowbar has
tripped; identify which controlled supply per p.156 net labels, then
power-cycle and re-read (transient → re-run Step 4; re-trips
immediately → genuine bad supply or shorted MMIC).

**C. Side-A fallback — PCB withdrawn from milled casing** *(§7.4.4 /
§7.5 p.147, instrument **off** before separating, supplies via
X95/X96 from a bench DMM/PSU rig per the manual; only needed when the
Side-A escalation rule above is hit)*

| Config | Node | Expected | Measured | Verdict |
|--------|------|----------|----------|---------|
| Open-circuit | X95 | +0.75 V ±10 % | | |
| Open-circuit | X96 | > +6.80 V | | |
| 68.1 Ω / 2 W / 1 % between X96 and bench load | X95 | −4.5 … −3 V | | |
| 68.1 Ω / 2 W / 1 % between X96 and bench load | I via X96 | \|I\| = 80 mA | | |

**D. X21 LO ALC sanity check — Side B lower cluster** *(in-circuit,
casing on, `--a21-probe` running; DMM only, no SA yet)*

**D.0 Current verdict (recovered schematic 2026-04-30) — Side B
lower cluster is a class-AB push-pull RF power-amp, chips presumed
alive.** Sheet 02/02 of A211 var.02 (drawing 1035.8840.01;
[`A211_var02_schematic_sheet_02_02.jpg`](rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg))
shows V3 (MRF3866-B, NPN) and V4 (MRF5160-B, PNP) drawn as a
**class-AB push-pull RF power-output stage** driven by V2 (BFG97-B)
acting as the LO pre-driver. The previous "3866 / 5160 complementary
collector-modulated AGC" reading and the "mirror-rail latch-up"
fault verdict are both fully SUPERSEDED — see history H3 ([H-2026-04-30-7d-d0-d4-failure-chain-narrative](smp_history.md#h-2026-04-30-7d-d0-d4-failure-chain-narrative)) and the marker quote-block below.

Bias-network topology per the schematic:

- **Base bias:** L41 / L43 (470 nH RF chokes) sit between the ±15 V
  rails and the V3 / V4 base nodes, in series with R43 / R44 100 Ω.
  R43 / R44 are base-series isolation resistors — **not** collector
  summing resistors as the original §7D narrative inferred.
- **Emitter bias:** R40 / R41 (3R92 each) tie the V3 / V4 emitter
  pours **directly** to ∓15 V (3866 NPN emitter pour → −15 V;
  5160 PNP emitter pour → +15 V). No choke in series.
- **Collector output:** the V3 / V4 collectors (pins 2 / 3 of each
  SO-8) are tied together and feed L45 (54 nH) + C49 (10 pF) as the
  output match, then exit the LO-AMPLIFIER block to the right of
  the schematic page (toward X21).
- **Pre-driver:** V2 (BFG97-B) base-drives the commoned V3 / V4
  base node; its collector goes to +15 V via collector-load choke
  L70 and a small base-divider biases the pair into class-AB.

The in-circuit "−14.72 V on 3866 pin 6/7" / "+14.47 V on 5160
pin 6/7" Side-B-trace readings (Table D rows 1 / 4a in history H3)
are the **expected DC paths through this bias network on healthy
silicon**, not on-die C-E latch-up. The bench-measured ≈ 105 Ω
"C-E" reading is consistent with a base-pin-to-rail measurement
(R44 + L43 DCR + R41 ≈ 100 + ~1 + 4 ≈ 105 Ω) on a base pin, not a
collector path. **Chips bench-confirmed alive 2026-05-03 by the D.5
ohm cross-check** (7-probe in-circuit sweep, all readings on the
"all as expected" branch — see [`smp_next.md` "Bench results —
2026-05-03 (D.5 PASSED)"](smp_next.md#bench-results--2026-05-03-d5-passed)).
Step 8a (out-of-casing bench-PSU) and Target 4 (in-instrument R65
split-test) remain the RF validators that can falsify the chips-
alive verdict by exclusion; until one of them fails, the §7E
silicon-pull rebuild stays on hold.

Other parts in the same cluster, locked by the recovered schematic:

- **V50, V60 = AT-42085-B** (Avantek/HP NPN Si bipolar, "420"
  top-mark; f_T 8 GHz, 8 V / 35 mA class-A bias, P1dB ≈ +20.5 dBm
  @ 1 GHz). The §7F cascade-amp ID is locked.
- **V61, V62 = HSMS-2800-B** (Avago Schottky pair) form the
  **frequency doubler** inside the FREQUENCY DOUBLER block,
  driven by V50 / V60 across L50 / L60 = 1 µH chokes. The §7F
  doubler-location open question is RESOLVED — see §7F banner.
- **V75 = MAR-8** (Mini-Circuits; Avantek house-code top-mark `A08`; see §7G A08 bullet).
- **N80-E = LP365M-L**, **N90-B = OP97FS-B** — but the LP365M
  itself, the input-divider ladder R80–R85, and ISET R109 274 K
  are all marked **N.F. (nicht bestückt / not fitted)** on Var.02.
  R102 100 K + R103 56 K2 (top divider) and R86 100 K + R87 61 K9
  + R88 3 K92 (−15 V leg) remain populated. **No LP365M wired-OR
  fault node to verify on Var.02** — the §7G supervisor / V85 / V89
  crowbar analysis applies to a different variant. See §7G LP365M
  N.F. callout, Step 7B note, and Step 8a "Supervisor handling"
  caveat for downstream consequences.

> **History — superseded since 2026-04-30:**
> - [H1: SCHEMATIC RECOVERED banner](smp_history.md#h-2026-04-30-7d-schematic-recovered-banner) — original supersession announcement.
> - [H2: DEEPER SCHEMATIC RE-READ — three corrections on top of H1](smp_history.md#h-2026-04-30-7d-deeper-schematic-reread) — corrections #1 (bias-network topology) and #3 (LP365M N.F.) are restated above as positive truth; correction #2 (DIAGSAMP / W216.10 not visible on sheet 02/02) is preserved as §D.2 below.
> - [H3: D.0 part-ID + Table D + D.1–D.4 failure-chain narrative](smp_history.md#h-2026-04-30-7d-d0-d4-failure-chain-narrative) — verbatim record of the original mirror-rail latch-up analysis (D.0 part-ID + topology, Table D rows including pre-rebuild ohm probes 5d-5g and 7a-7e, D.1 Decision matrix, D.2 off-line confirmation, D.3 verdict, D.4 reconciliation). The pre-rebuild ohm probes themselves are still useful as continuity checks once reframed against the corrected bias network — recapture in §D.3 below.

**D.1 Open question — VARSAMP divider readback inconsistency.**
The schematic shows `R30 = 8K25 L` and `R31 = 562 R L` between
+7,5 V and GND (tap = VARSAMP), predicting V_VARSAMP ≈ 7.5 ×
562 / (8250 + 562) ≈ **0.479 V** at nominal +7,5 V. This is
inconsistent with both the spec window (0.9–1.1 V) and the bench-
measured **+0.963 V** in §1 below. Possible: (a) my schematic read
of `R30` is wrong (image is grainy at this part of the sheet);
(b) the +7,5 V net at this divider is actually ≈ 15 V; (c)
different divider on the bench unit vs the schematic. **No values
are changed in the doc pending a higher-res schematic re-check**
(see `smp_next.md` planning block "Comparator inputs + X21 last
stage").

**D.2 Open question — +7.5 V destination, doc-vs-schematic
mismatch.** The §Step 8a bench-PSU procedure (line ~3304 below) +
the Step 10a skip-list (line ~3669 below) both state that
**+7.5 V (W216.4) biases the §7F 420 NPN cascade collector**
(V50 / V60), supervisor-gated through the V85 / V89 cut-off
switches. A direct line-by-line scan of sheet 02/02 for the
+7,5 V net **does not corroborate this**. On the schematic:
+7.5 V enters at W216.4, passes the L22 supply-block filter
inductor + decoupling caps, exits as a labeled net "+7,5V"
running right, and **does not visibly terminate anywhere on
sheet 02/02**. Specifically, the FREQUENCY DOUBLER block (V50 /
V60 AT-42085-B + V61 / V62 HSMS-2800-B) shows the V50 / V60
collector supply rails labeled **VR15-P (+15 V)**, not +7,5 V;
the LO AMPLIFIER block (V2 BFG97 + V3/V4 push-pull) is also on
+15 V / −15 V; the IF block uses VR15-IF (separate +15 V branch);
the CONTROL-/BIAS-C populated divider stub (R102 / R103) ties to
VR15-P. **No +7,5V tap on the V50 / V60 collector net is visible
on sheet 02/02.** Also: V90 (BUZ71 TO-220 MOSFET symbol), R98,
X95, X96 — none of these are on sheet 02/02 either; only N90
(DP97FS-B = OP97) sits on this sheet, in the bottom-right region
near the (N.F.) N80 LP365M, with no regulator-loop devices around
it. The whole BUZ71 / R98 / X95 / X96 sub-block must therefore
live on **sheet 01/02**, which is **not in the recovered corpus**.
Most-likely reading consistent with the bench (W216.4 = +7.55 V;
X96 ≈ +6.18 V at BUZ71-S directly per Side-B trace 2026-04-30):
the on-board "+7,5V" net is the **+V_unreg input to the BUZ71
high-side regulator on sheet 01/02**, and the regulator output
(X96 ≈ +6 V) is what actually feeds the 420 cascade — the
line-3304 / 3669 "+7.5 V → 420 cascade collector" wording is then
a topology shortcut that elides the BUZ71 regulator stage.
Resolution path: Target 3 in `smp_next.md` (X95 / X96 / V95 / R98
bench re-trace) includes a probe to follow the +7.5 V copper from
L22 forward; if it lands on R98 → BUZ71-D, the shortcut is
confirmed and the two doc lines need rewording (not deletion).
**No values changed pending the bench trace and/or sheet 01/02
recovery.**

**D.3 Pre-rebuild bench gate — DMM ohm cross-check (chips-out, run
instrument off).** Discriminates "silicon damage" from "external
network reading" on the suspicious in-circuit ohm captures recorded
in history H3 Table D. Probe set updated to match the corrected
bias-network topology of §D.0 (R43 / R44 are base-series, R40 / R41
are emitter-to-rail, V3 / V4 collectors are tied and feed L45 / C49
to off-page, no per-chip 100 Ω collector summing R):

```
+---+--------------------------------+-----------+--------------------+
| # | Probe (instrument off, ohm)    | Expected  | Tells us           |
+---+--------------------------------+-----------+--------------------+
| 1 | V3 (3866) base pin → −15 V     | ≈ 105 Ω   | confirms R44 +     |
|   | (R44 + L43 DCR + R41 path)     |           | L43 DCR + R41 path |
| 2 | V4 (5160) base pin → +15 V     | ≈ 105 Ω   | mirror of probe 1  |
|   | (R43 + L41 DCR + R40 path)     |           |                    |
| 3 | V3 emitter pour → −15 V        | ≈ 3.92 Ω  | R41 emitter R      |
| 4 | V4 emitter pour → +15 V        | ≈ 3.92 Ω  | R40 emitter R      |
| 5 | V3 / V4 joined collector node  | reads     | tied collectors    |
|   | → output L45 (54 nH)           | sub-Ω +   | feed off-page      |
|   |                                | inductor  | through L45 / C49  |
|   |                                | DCR       | to X21             |
| 6 | V3 / V4 emitter pours → ±15 V  | sub-Ω     | doubled-emitter    |
|   | by visual + ohm to all four    | short to  | bonds intact       |
|   | pins (1, 4, 5, 8) on each pad  | all four  |                    |
+---+--------------------------------+-----------+--------------------+
```

Outcome decision:

```
+----------------------------+---------------------------------------+
| Cross-check result         | Verdict                               |
+----------------------------+---------------------------------------+
| All as expected            | The bench-measured ≈ 105 Ω is the     |
|                            | base-pin-to-rail path (probes 1 / 2). |
|                            | Silicon presumed alive on both chips. |
|                            | Skip rebuild step 2 (no desolder).    |
|                            | Proceed to Step 8a bench-PSU LO RF    |
|                            | validation.                           |
| Probe 1, 2, 3 or 4 off     | Real fault site IS in the bias        |
|                            | network (open RFC L41 / L43, blown    |
|                            | base-series R43 / R44, blown emitter  |
|                            | R40 / R41, broken pour bond). Repair  |
|                            | the network before any silicon work.  |
| Probe 5 OL                 | Output match L45 open or trace        |
|                            | broken between V3 / V4 collectors     |
|                            | and X21. Repair before silicon work.  |
| Probe 6 not sub-Ω on any   | Lifted pad / cracked bond on the      |
| of the eight emitter pins  | doubled-emitter group — repair        |
|                            | before any silicon refit.             |
+----------------------------+---------------------------------------+
```

**D.4 Optional confirmation by desolder.** If D.3 ohm cross-check
passes but the Step 8a bench-PSU LO-RF validation still fails to
recover X75, pull the V4 (5160) only (cheaper, smaller of the two
MRF chips) and re-run a full diode-mode junction sweep
out-of-circuit. If it reads as a clean PNP, the chips-alive verdict
holds and the fault is upstream of V3 / V4 (BFG97 pre-driver, X21
input LPF, supply rail collapse, supervisor cut-off). If V4 reads
damaged out-of-circuit, the chips-alive verdict is overturned and
both MRF parts get replaced.

**Status (updated 2026-05-03):** chips **bench-confirmed alive** by
the D.5 ohm cross-check (7-probe in-circuit sweep, all on the "all
as expected" branch — see [`smp_next.md` "Bench results — 2026-05-03
(D.5 PASSED)"](smp_next.md#bench-results--2026-05-03-d5-passed); per-
probe readings 5.3 Ω / 5.4 Ω / 102.6 Ω / 102.3 Ω / 0.2 Ω / OL /
2.64 kΩ). The bias network around V3 / V4 (R40 / R41 3R92, R43 /
R44 100 Ω + L41 / L43 470 nH base-bias path, R42 4K75 inter-base,
L45 / C49 output match) is intact end-to-end, and the L45 / C49
output is correctly DC-blocked off the rails. The historical
"replace A0 + 3866 + 5160" rebuild trigger in Step 7E below is
therefore **formally on hold**. The remaining open question on the
LO-amp half of the chain is RF-only and is settled by exclusion at
Step 8a (out-of-casing bench-PSU) or Target 4 (in-instrument R65
split-test); a pass at either step closes the silicon question with
no rebuild required. A fail at either RF step would re-open the
chips-alive verdict and trigger D.6 (5160 desolder + OOC re-probe)
before any silicon replacement is committed.


### Step 7E — rebuild and post-rebuild verification *(replace A0, MRF3866, MRF5160; verify the BFG97 collector network, the two 3R92 emitter-bias resistors, and L1/L2 of the input LPF in place)*

⚠ **Power off A211 before any soldering.** Per §7.4 / §7.5, separate
the PCB from the casing first if board-level rework is easier with
the casing removed.

**§7E-bench — A211 loose-on-bench unpowered trace session** *(single
DMM-ohm session on the loose A211 board, instrument off, milled
casing still in the instrument; ~45 min total; gates the rebuild
solder work)*:

This worksheet collects every unpowered ohm trace that needs to be
captured **before** any soldering, in run-order. The detailed probe
tables live in their original sections (cross-referenced below) — this
is the session checklist + summary, not a re-statement of those tables.
Run all five blocks in one sitting; the DMM stays in ohm mode
throughout, the board stays disconnected throughout, and the verdicts
feed directly into either the §7E rebuild sequence or one of two
escalation paths.

Session prep (2 min):

- A211 PCB on an ESD mat, no cables connected, **W216 ribbon free**
  (gives clean access to W216.1 / W216.5 / W216.10 pads).
- DMM in ohm mode, low range (200 Ω / 2 kΩ / 20 kΩ as appropriate);
  diode-test mode for one optional secondary check on the new A0 pad
  if the dead one comes off cleanly.
- Have the §7G LP365M V_E (pin 16), ISET (pin 1), and the four OUT
  pins (2, 3, 14, 15) pre-located on the back-face photo before
  starting (saves probe-fishing time during block 5).

Run-order:

| # | Block | What it answers | Detail table | Time |
|---|-------|-----------------|--------------|------|
| A1 | **DIAGSAMP path sanity (settled-passive)** | Confirms the bench-traced passive A0 + 1002 + shunt-cap rectifier is electrically intact between the rectifier filter and W216.10 — i.e. that DIAGSAMP will recover by itself once the ALC rebuild restores LO at X21 | §7E "Pre-rebuild — DIAGSAMP path settled" (single ohm check D1′ immediately below this worksheet) | 2 min |
| A2 | **N90 sanity only (r5/r6)** | Whether the N90 (OP97FS) supply rails are intact, as a global ±15 V sanity check (the OP97 next door reading clean ±15 V is independent confirmation that the global rails are healthy and the failure scope is local to A21's RF cluster). **Note (§7D γ):** rows r1 and r2 (3866 / 5160 pin 7 → W216.1 / +15 V) are now **superseded** — pin 7 is the doubled collector node to the BFG97 summing junction, not a +V supply pin; the in-circuit pin 7 readings are diagnosed under §7D.3 site 1/3 (chip-internal C-E damage), not as supply-path opens. Rows r3 and r4 (3866 / 5160 pin 4 → W216.5) remain superseded by Table D rows 5d–5g (pour↔rail ohm check across the 3R92). | §7E "Pad-to-rail check" table (rows r5/r6 only) + Table D rows 5d–5g for the pour-rail check | 4 min |
| A3 | **3866 / 5160 input network sanity (LPF L1/L2 + both 3R92 emitter-bias resistors) + collector network → BFG97 integrity** | Whether the X21 → cap → L1-Cshunt-L2 LPF → commoned base node path is continuous (an open L1 or L2 floats both pin 2/3 base groups and is a leading trigger candidate per §7D.3); whether the two 3R92 emitter-bias resistors (3866 emitter pour → −15 V; 5160 emitter pour → +15 V) read close to 3.92 Ω; **and (new under §7D γ)** whether the collector network is intact: pin 6 ≡ pin 7 short on each chip footprint (visual + Table D rows 7a/7b), continuity from each chip's joined pin 6/7 collector node through the 100 Ω + LC summing path to the BFG97 collector tab (Table D rows 7c/7d), and BFG97 collector-load inductor integrity to the +V rail (Table D row 7e). The BFG97 collector path is the **secondary fault site** added in §7D.3 site 5 — sustained back-drive from the latched 3866 / 5160 into the BFG97 collector may have fused the collector-load inductor or stressed the 100 Ω summing resistors. The pin 1↔pin 5 short on each chip is part of the doubled-emitter pour group (visible top-side trace plus pour underneath, per §7D β), so chips-out ohm checks on the pour↔pin 1/4/5/8 bonds (Table D rows 5f, 5g) are visual-first; only ohm-probe if the bond looks suspect. | §7D revised topology paragraph + §7D.3 trigger candidates 3, 4 & 5 + Table D rows 5d–5g + 7a–7e | 12 min |
| A4 | **G3 + G8 LP365M V_E + OUT-pin topology trace — RESOLVED (R1 non-latching).** Topology question is closed by the bench session: V_E = GND, OUTs commoned (wired-OR), inputs commoned across mixed polarity onto Zener-derived VREF, ISET fixed-bias to +15 V via 274 kΩ, wired-OR pulled to +15 V via 15 kΩ driving SOT-23 'A2' base directly. R2 / R3 eliminated; the previous "self-disabling ISET feedback latch" sub-reading is also withdrawn (1502 / 2743 are independent +15 V pull-ups, not a feedback chain). Remaining §7G work (G-IN sense-pin assignment, G-Z Zener voltage, G-REFvia, G-SOT top-mark decode) is non-blocking for the §7E rebuild. | §7G "Topology — CONFIRMED R1" table + Bench-checks G-row table | 0 min (pre-rebuild — resolved) |

Session exit — single decision matrix:

| A1 result | A2 result | A3 result | A4 result | Verdict |
|-----------|-----------|-----------|-----------|---------|
| D1′ short / sub-ohm (passive DIAGSAMP path intact) | r5/r6 finite (N90 supply intact, global ±15 V healthy) | L1 and L2 both continuous (sub-ohm to a few ohms each); both 3R92s read ≈ 3.92 Ω; pour↔pin 1/4/5/8 emitter bonds visually intact on both footprints; **pin 6 ≡ pin 7 collector short visually intact on both footprints (rows 7a/7b); 100 Ω + LC summing path continuous on both chips, ≈ 100 Ω + small DCR (rows 7c/7d); BFG97 collector-load inductor finite (a few Ω + pull-up R) to +V rail with no rail short to ±15 V or GND (row 7e)** | V_E (pin 16) lands on GND or on a single pull-up node toward a logic-level rail; all four OUTs (pins 2, 3, 14, 15) commoned through external pull-ups onto a single fault-flag net; no OUT pin DC-coupled to any SOT-23 base (R1 multi-channel-monitor topology confirmed) | **Proceed to rebuild step 2.** Trigger candidates 3 (3R92 open), 4 (LPF inductor open), and 5 (BFG97 collector-network fault) are all eliminated by the A3 readings; the remaining trigger candidates are the two transient hypotheses (1, 2), neither discriminable by ohm checks. Part identity is **resolved** (MRF3866 NPN + MRF5160 PNP, top marks `R4D ∥ 3866` / `R4N ∥ 5160` per §7D bind line); fit per §7E rebuild step 7. |
| D1′ open between rectifier filter and W216.10 | any | any | any | **Stop**. Passive DIAGSAMP path has a trace break independent of the AGC failure — locate (1002 pad lift, shunt-cap pad lift, broken via, broken connector pin) and repair before rebuild; otherwise post-rebuild DIAGSAMP will still read 0 V even with LO restored. |
| any | r5 or r6 also open | any | any | **Stop**. Fault scope wider than the 3866 / 5160 pair — broken trace or shorted bulk bypass on the OP97 supply path. Escalate before any silicon goes back. |
| any | as expected | L1 or L2 reads OL (open) | any | **Confirmed trigger = LPF inductor open** (§7D.3 candidate 4). Flag the open inductor for replacement at rebuild alongside the 3866 / 5160; re-run A3 after the inductor is fitted to confirm continuity before powering the rebuilt board. |
| any | as expected | one or both 3R92 reads OL (open) or grossly off-value (>> 4 Ω), **or** a pour↔pin 1/4/5/8 emitter bond reads non-zero on either footprint | any | **Confirmed trigger = pour / 3R92 emitter-bias path failure** (§7D.3 candidate 3, revised). Flag the failed 3R92(s) and/or the broken pour bond for repair at rebuild alongside the 3866 / 5160; re-run A3 after to confirm. |
| any | as expected | one or both 100 Ω summing resistors read OL or grossly off-value, **or** the BFG97 collector reads a hard short to ±15 V or to GND (row 7e), **or** the collector-load inductor reads OL to +V | any | **Confirmed trigger / secondary damage = BFG97 collector-network fault** (§7D.3 candidate 5). Flag the failed 100 Ω resistor / inductor / damaged BFG97 for repair at rebuild alongside the 3866 / 5160; re-run A3 after to confirm. **Critical gate:** without the BFG97 collector network restored to known-good state, fitting fresh 3866 / 5160 silicon may fail again immediately on power-up via the same back-drive mechanism that triggered the original failure. |
| any | as expected | as expected | G3 + G8 reveal an OUT pin DC-coupled (via base R) to a SOT-23 base, **or** two channels' (+) / (−) inputs share a single sense node via paired threshold dividers | **Proceed to rebuild step 2 AND** flag §7G for a topology revision — the LP365M is acting as a hysteretic switching pass-element controller (R2) or a window-comparator pair (R3) rather than a wired-OR multi-channel monitor (R1); promote the matching alternative reading in the §7G "Topology — what we have / haven't confirmed" paragraph to primary after the rebuild verifies. |

Worksheet rows (fill in during the session):

| Block | Probe / pad | Reading | Verdict (per detail table) |
|-------|-------------|---------|----------------------------|
| A1 D1′ | DIAGSAMP node (bottom of `1002` / top of shunt cap) → W216.10 | **confirmed by §7D bench-trace** (1002 → shunt cap → W216.10 walked end-to-end on the copper) | **PASS** — passive DIAGSAMP path intact; no separate ohm re-check required |
| A2 r5 | W216.1 → N90 pin 7 | **N90 pin 7 = +15 V** (powered DC at the OP97 V+ pin, supersedes the unpowered ohm check — clean rail at the chip implies an intact W216.1 → N90 pin 7 supply path) | **PASS** |
| A2 r6 | W216.5 → N90 pin 4 | **N90 pin 4 = −15 V** (powered DC at the OP97 V− pin, supersedes the unpowered ohm check — clean rail at the chip implies an intact W216.5 → N90 pin 4 supply path) | **PASS** |
| A3 L1 | LPF L1 (X21-cap side) terminals | | continuity expected (sub-ohm to a few Ω) |
| A3 L2 | LPF L2 (commoned-base-node side) terminals | | continuity expected (sub-ohm to a few Ω) |
| A3 3866 3R92 | 3866 emitter pour → −15 V rail (across the 3R92) — same measurement as Table D row 5d | | ≈ 3.92 Ω expected |
| A3 5160 3R92 | 5160 emitter pour → +15 V rail (across the 3R92) — same measurement as Table D row 5e | | ≈ 3.92 Ω expected |
| A3 3866 pour bonds | 3866 emitter pour ↔ footprint pins 1 / 4 / 5 / 8 (visual: top-side trace + pour underneath; chips-out ohm only if visual is ambiguous) — same as Table D row 5f | | sub-ohm short to all four expected |
| A3 5160 pour bonds | 5160 emitter pour ↔ footprint pins 1 / 4 / 5 / 8 (visual: top-side trace + pour underneath; chips-out ohm only if visual is ambiguous) — same as Table D row 5g | | sub-ohm short to all four expected |
| A3 3866 6↔7 | 3866 footprint pin 6 ↔ pin 7 (visual: top-side trace; chips-out ohm only if visual is ambiguous) — same as Table D row 7a | | sub-ohm short expected |
| A3 5160 6↔7 | 5160 footprint pin 6 ↔ pin 7 (visual: top-side trace; chips-out ohm only if visual is ambiguous) — same as Table D row 7b | | sub-ohm short expected |
| A3 3866→BFG97 | 3866 joined pin 6/7 collector node → BFG97 collector tab (pin 4) through the 100 Ω + LC summing network — same as Table D row 7c | | ≈ 100 Ω + small inductor DCR expected |
| A3 5160→BFG97 | 5160 joined pin 6/7 collector node → BFG97 collector tab (pin 4) through the 100 Ω + LC summing network — same as Table D row 7d | | ≈ 100 Ω + small inductor DCR expected |
| A3 BFG97 Vc | BFG97 collector tab (pin 4) → +V rail through collector-load inductor; also probe to −V and GND for short check — same as Table D row 7e | | finite (a few Ω + pull-up R) to +V; OL to −V and GND |
| A4 G3 | LP365M V_E (pin 16) → ohm to GND / ±15 V / each SOT-23 base (pin 1, std JEDEC SOT-23) / any logic-level net leaving §7G | pin 16 → GND, sub-ohm (R1 wired-OR fingerprint ✓) | |
| A4 G-IN | LP365M input pins (5 / 6 / 7 / 8 / 9 / 10 / 11 / 12) → for each, ohm to every other input pin, to ±15 V via any candidate divider tap, to GND, and to any sensed-signal net leaving §7G | Pins 6, 8, 9, 12 commoned on a single net = +IN1, +IN2, −IN3, +IN4 — bench-confirmed (partial G-REF) as a **Zener-derived shared threshold reference** VREF, fed from +15 V → 1.82 kΩ → node Y (Zener-clamped) → 56.2 kΩ / 100 kΩ divider; VREF = Vz × 0.6406. (3 channels with reference on (+) ⇒ undervoltage detectors trip when sense on −IN drops below VREF; channel 3 with reference on (−) ⇒ overvoltage detector trips when sense on +IN3 rises above VREF.) Reading: R1 multi-rail monitor topology = **3 UV + 1 OV detector with common reference**. Alternate "shared SENSE + four independent threshold taps" reading is **withdrawn** by the G-REF bench evidence. Sense pins 5 / 7 / 10 / 11 individual destinations remain TBD. | |
| A4 G8 | LP365M OUTs (pins 2, 3, 14, 15) → for each, ohm to each SOT-23 base (pin 1, std JEDEC SOT-23), to V_E (pin 16), to +15 V via any candidate pull-up R, and to any logic-level net leaving §7G | All four OUTs (pins 2, 3, 14, 15) commoned on a single net (R1 wired-OR fingerprint ✓). Net → SOT-23 'A2' base (pin 1) direct + → 1502 (15 kΩ) → +15 V (pull-up). The 2743 (274 kΩ) on LP365M ISET (pin 1) is an **independent** +15 V pull-up sharing only the V+ copper at its upper end with the wired-OR pull-up — **not** an OUT-to-ISET feedback chain. Reading: R1 multi-channel **non-latching** monitor with wired-OR fault flag driving SOT-23 'A2' as the common downstream actuator; ISET is fixed-bias, the trip releases automatically when the sense node returns to in-window. The earlier "OUT→ISET feedback / latching / relaxation-oscillator" reading is **withdrawn**. | |

Once the worksheet is complete and the decision matrix lands on
**Proceed to rebuild step 2**, the soldering work in the rebuild
sequence below can begin with confidence that no additional faults
will surprise the new silicon.



**Pre-rebuild — DIAGSAMP path settled** *(no D1–D4 ohm work needed;
left here for traceability of how the path was characterised)*: the
DIAGSAMP topology was bench-traced and is now confirmed (per §7D
revised topology) as a **passive rectifier**: A0 anode on the X21
RF tap, A0 cathode hard to GND, 10 kΩ `1002` series isolation R from
the X21 tap node to W216.10, shunt cap from W216.10 to GND. There
is **no AGC op-amp on this path**; the original D1–D4 table assumed
the 3866 or the 5160 drove DIAGSAMP and is therefore obsolete. The
"R4D-B set-point divider open" hypothesis is also **withdrawn** —
the §7D revised topology trace shows the 5160 pin 3 sits on the X21
tap node along with the 5160 pin 2 and the 3866 pins 2 / 3 (the
doubled-base group of both SO-8 RF transistors, all through the
cap + L1-Cshunt-L2 LPF); there is no W216.1 → pin 3 divider to
localise. The §7E-bench A3 block has been re-scoped to
LPF inductor continuity + 3R92 bias-resistor checks + pin 1↔pin 5
short verification on each footprint (see §7D.3 trigger candidates
3 and 4).

A single ohm check is retained as the pre-rebuild DIAGSAMP-path
sanity test:

| # | Probe | Expected | Verdict if not |
|---|-------|----------|----------------|
| D1′ | DIAGSAMP node (bottom of `1002`, also top plate of shunt cap) → W216.10 | short / sub-ohm | trace break between the rectifier filter and the connector — flag and fix before rebuild; otherwise post-rebuild DIAGSAMP will still read 0 V even with LO restored |

Run D1′ once **before** the rebuild solder work. A pass means the
passive DIAGSAMP path is fully intact and DIAGSAMP recovery is
guaranteed to follow the ALC restoration delivered by the rebuild.

**Status on this unit:** D1′ is **already confirmed PASS** via the
§7D revised-topology bench trace (the 1002 → shunt cap → W216.10
copper run was walked end-to-end during topology resolution; per
§7D the DIAGSAMP rectifier is "passive, fully bench-traced"). No
separate ohm re-check is needed; A1 is closed and the §7E-bench
session can skip directly to A2.

**Rebuild sequence (do these in order):**

1. **Power off A211.** Separate from casing if rework is easier with
   casing removed.
2. **Desolder A0, the 3866, the 5160.** Hot air ~330 °C; bag and
   label the dead parts in case post-rebuild faults drive a side-by-
   side comparison.
2a. **A0 standalone bench test** *(5 min on a perfboard, while the
   iron is cooling)*. Per §7D revised topology A0 is on the **passive
   DIAGSAMP rectifier**, not in the 3866 / 5160 ALC loop, so it is
   **not a trigger candidate** for the cascade AGC failure — its
   in-circuit diode-test readings (Vf elevated ~80 mV vs the on-board
   refs) are
   characterised here as **bystander confirmation / DIAGSAMP-detector
   health check**, not a root-cause discriminator. Run a brief I-V
   characterisation on the removed part for failure-analysis record
   and to predict whether the fitted HSMS-2800-BLKG / MA4E1340A1-287T
   co-primary (or BAT54C fallback) will land DIAGSAMP near the
   original's Vf or shifted:

   | # | Test | Setup | Healthy reading | Degraded reading |
   |---|------|-------|-----------------|------------------|
   | 2a.1 | Vf at 1 mA forward | 9 V battery, 9.1 kΩ series, DMM in V mode across A0 (anode = pin 3, cathode = pin 1) | 0.23 … 0.28 V | > 0.32 V (confirms the in-circuit reading was not a measurement artefact and DIAGSAMP would have read low even with LO restored) |
   | 2a.2 | I_R at 5 V reverse | 9 V battery via 1k/1k divider clamping ~4.5 V across A0 reverse-biased, DMM in µA mode in series | < 1 µA | > 5 µA (degraded barrier — would skew DIAGSAMP DC under LO load) |

   **Verdicts**:

   - **Both readings within healthy bracket** → A0 was healthy; the
     ~80 mV in-circuit Vf elevation was a measurement artefact (most
     likely the DIAGSAMP RC network parallel-loading the diode test
     through the shunt cap), so the DIAGSAMP path is fully intact.
     Bag and label the part as "reference healthy" — useful as a
     fourth on-board "A0" reference for any future investigation.
   - **Vf elevated AND/OR reverse leakage > 5 µA** → A0 was degraded.
     The rebuild's HSMS-2800-BLKG replacement restores DIAGSAMP
     independent of this finding; the result is recorded only to
     document the
     pre-rebuild detector state. Note: a stress event strong enough
     to degrade A0 (LO transient, ESD, mishandling) is **separately**
     consistent with the supply-rail-transient trigger candidate for
     the 3866 / 5160 cascade — see §7D.3 revised narrative — so a
     degraded A0 reading mildly raises the probability of the
     supply-transient hypothesis being the AGC trigger, without
     itself being on the AGC failure path.
   - **Test draws no current at all (open in both directions)** → A0
     was physically destroyed. Same recording note as above; same
     mild bump to the supply-transient AGC trigger hypothesis.

   This 5-min test produces failure-analysis evidence on a part you'd
   otherwise discard. It does **not** gate the rebuild — proceed to
   step 3 regardless of outcome.

3. **Run the §7E-bench A2 N90-rail sanity check** (rows r5/r6 only —
   the original r1–r4 "pin 7 / pin 4 to the rails" rows are
   **superseded** under §7D (β/γ); pin 7 is the doubled collector
   node and pin 4 is on the emitter pour, neither is a supply pin).
   The check confirms the global ±15 V rails are healthy at N90,
   which is independent confirmation that the failure scope is local
   to the AGC cluster.
4. **Verify the 3866 / 5160 input network is intact** *(replaces the
   obsolete "localise the divider open" step — per §7D revised
   topology there is no W216.1 → 5160 pin 3 set-point divider; pin
   3 sits on the X21 RF tap)*. Chips-out, ohm mode, repeat the
   §7E-bench A3 readings if not already taken: (a) **L1 and L2 of
   the input LPF** continuous (sub-ohm to a few Ω each); (b) **both
   3R92 emitter-bias resistors** read ≈ 3.92 Ω (3866 emitter pour ↔
   −15 V rail; 5160 emitter pour ↔ +15 V rail); (c) **pour↔pin 1/4/
   5/8 emitter bonds on each empty footprint** read sub-ohm to all
   four (visual check first, ohm only if the bond looks suspect).
   An open in any of these is one of the ohm-detectable trigger
   candidates for the original failure (§7D.3 candidate 3) and
   **must** be repaired before fitting fresh silicon.
5. **Verify the BFG97 collector network is intact** *(new under §7D
   γ; the previous "replace the two fused per-chip supply filters"
   step is **withdrawn** — per §7D (γ) there are no per-chip pin-7
   supply filters, the joined pin 6/7 node is the doubled collector
   feeding the BFG97 summing junction, not a +V supply leg)*. Run
   Table D rows 7a–7e: pin 6 ≡ pin 7 short visually intact on both
   footprints; ≈ 100 Ω + small DCR through each chip's 100 Ω + LC
   summing leg to the BFG97 collector tab; BFG97 collector finite to
   +V rail through its collector-load inductor with no rail short to
   ±15 V or GND. A failure here is the §7D.3 site 5 secondary fault
   site and **must** be repaired before fitting fresh silicon.
6. **Replace any failed input-network part** found in step 4 (open
   LPF inductor or open 3R92) **and any failed BFG97-network part**
   found in step 5 (open 100 Ω summing R, open or rail-shorted
   collector-load inductor, C-E-shorted BFG97) with matching-value
   substitutes. If steps 4 and 5 came up clean, this step is a no-op.
7. **Fit new silicon:** in the A0 footprint, either **HSMS-2800-BLKG**
   in **natural** orientation (part pin 1 = K → footprint pin 1,
   part pin 3 = A → footprint pin 3, part pin 2 = NC → footprint
   pin 2 NC — like-for-like drop-in, no rotation) **or** the
   co-primary **MACOM MA4E1340A1-287T rotated 180°** (the MACOM
   SOT-23 single Schottky uses pin 1 = A, pin 2 = NC, pin 3 = K per
   Mouser spec-sheet `maom-s-a0010058398-1.pdf` — opposite polarity
   convention to the HP/Avago part, so the rotation lands the part's
   pin 3 (K) on footprint pin 1 and the part's pin 1 (A) on footprint
   pin 3, with pin 2 NC on both sides so no orphan pad); the MA4E1340
   sits +70 mV in Vf (medium-barrier 0.41 V vs HSMS-2800 low-barrier
   0.34 V at 1 mA), negligible against the +7.5 … +11 V DIAGSAMP spec
   window. Then fit the **MRF3866** (NPN) in the 3866 footprint and
   the **MRF5160** (PNP) in the 5160 footprint, both in **natural**
   orientation (pin-1 dot matching the original silkscreen dot, per
   Motorola SO-8 Case 751-05 Style 1 pin-1 indexing). The
   complementary pair must not be swapped — the 3866 sits on the
   −15 V emitter pour, the 5160 on the +15 V pour; fitting them
   mirrored will instantly forward-bias both C-E junctions and
   destroy the parts on power-up. **Fallback if neither HSMS-2800-
   BLKG nor MA4E1340A1-287T is on hand:** BAT54C in the A0 footprint
   **rotated 180°** (part pin 3 = common K → footprint pin 1) per
   the §7E Replacements-table fallback paragraph; functionally
   equivalent with a ≈ 20 mV Vf-offset penalty on DIAGSAMP DC, well
   within the +7.5 … +11 V spec window.
8. **Power up.** Run `--a21-probe`, fill Table D′ (verification
   sequence below), and read X75 / TP1910 from the same probe output.
   **Pass = Table D′ all rows in spec AND TP1910 climbs to 7.5 … 11 V**
   (§7.4.1) — rebuild verified, instrument restored.

Steps 4 and 5 must complete *before* step 7 — fitting fresh silicon
into a board with an open LPF inductor, open 3R92, or damaged BFG97
collector network risks an immediate repeat of the original failure
on the new chips.

If Table D′ passes but X75 / TP1910 stays dead, drop into Step 8 (SA
on X21 with ≥30 dB / ≥1 W pad) as a **diagnostic** — it localises
whether LO is dead at X21 (an ALC fault we missed) or LO is fine and
the fault sits downstream (A212 / V1.1-V1.2 / V75 / A211 diag
rectifier). Step 8 is no longer a mandatory checkpoint after a clean
rebuild.

Replacements selected for this rebuild (instrument off, like-for-like
footprint):

| Reference | Original | Replacement fitted on this unit |
|-----------|----------|----------------------------------|
| A0 | **HP/Avago HSMS-2800** SOT-23 single low-barrier RF Schottky detector diode (top mark `A0` family code + date/lot character — sister-board photo reads `A0E` where `E` is the date/lot marker, since the HSMS-280x catalog has no `A0E` lead-code suffix). Multiple instances on this A211, all the same part: the **DIAGSAMP rectifier** in the middle compartment (anode on X21 RF tap, cathode hard to GND, 10 kΩ `1002` + shunt cap form the post-rectifier RC filter to W216.10; **not** the AGC envelope detector as previously assumed) plus **V61 and V62 (HSMS-2800-B per recovered schematic 2026-04-30)** in the FREQUENCY DOUBLER block — these are the two further A0-marked footprints used as the in-circuit Vf reference brackets in §7D (0.234 V and 0.265 V forward). All three on-PCB "A0" SOT-23 instances are HSMS-2800; if either V61 or V62 is damaged during a doubler-stage failure investigation, the same like-for-like sourcing applies. Footprint on the DIAGSAMP A0: pin 1 = cathode, pin 3 = anode, pin 2 truly NC; pinout falsifies all dual / common-anode HSMS-280x variants (HSMS-2802/3/4/5 and HSMS-280E/F all drive pin 2). Bench Vf ≈ 0.23 … 0.27 V at DMM Itest on the two healthy refs — consistent with the HSMS-2800 datasheet (Vf ≈ 0.34 V at 1 mA, lower at DMM-test currents). | **Co-primary A:** **HSMS-2800-BLKG like-for-like** (Broadcom/Avago, still in catalog 2024 — sold by Mouser / Digi-Key / Newark in 100-piece antistatic-bag (`-BLKG`), 3000-piece 7" reel (`-TR1G`), and 10000-piece 13" reel (`-TR2G`) formats); fits the SOT-23 footprint in **natural orientation** (pin 1 = K → pad 1, pin 3 = A → pad 3, no rotation), no Vf offset. The **HSMS-280B-BLKG** (SOT-323 single, electrically identical die — same Vf, VBR, IR, applications) is an acceptable bench-bodge substitute that lands on the inner edges of the SOT-23 pads — only relevant if HSMS-2800-BLKG stock-out forces it. **Co-primary B:** **MACOM MA4E1340A1-287T** (medium-barrier Si Schottky, SOT-23 case 287, single diode, V_BR 70 V, Cj ≈ 0.9 pF, P_TOT 250 mW, DC–6 GHz detector / mixer / limiter classification — currently in production at MACOM, $1.40–$2.32 in 1+ qty at Mouser / DigiKey, the `A1` suffix denotes SnPb plating which matches the 1990s SnPb-built A211; the `B1-287T` matte-Sn / RoHS variant is an acceptable Pb-free substitute). **The MA4E1340 SOT-23 pinout is pin 1 = A, pin 2 = NC, pin 3 = K** per Mouser spec-sheet `maom-s-a0010058398-1.pdf` — **opposite cathode/anode polarity convention to the HP/Avago part**, so it must be fitted **rotated 180°** in the footprint (part pin 3 (K) → pad 1, part pin 1 (A) → pad 3, part pin 2 (NC) → pad 2 NC — rotation is benign, no orphan pad). Vf ≈ 0.41 V at 1 mA (medium-barrier, +70 mV vs HSMS-2800 low-barrier 0.34 V) — negligible against the +7.5 … +11 V DIAGSAMP spec window (3.5 V / 2 % shift). The MA4E1340 wins on procurement (current production) and ties on package; HSMS-2800 wins on like-for-like Vf and natural orientation — pick whichever lands in stock first. **Fallback (on-hand stock, in case neither co-primary is available at rebuild time): BAT54C** (ON Semi / Diodes Inc / Vishay, SOT-23 common-cathode dual Schottky, marking `L43`: pin 1 = A1, pin 2 = A2, pin 3 = K), fitted **rotated 180°** in the footprint so the part's pin 3 (common K) lands on footprint pin 1 and the part's pin 1 (A1) lands on footprint pin 3; the unused D2 anode (part pin 2) sits on footprint pin 2 (NC) — completely benign. Vf ≈ 0.32 V at 1 mA vs HSMS-2800's ≈ 0.34 V — within 20 mV, no meaningful DIAGSAMP DC offset. See alternatives paragraph below. |
| **3866** (R4D position, top mark `R4D ∥ 3866`) | **MRF3866** — Motorola SO-8 RF NPN, Case 751-05 Style 1 (1/4/5/8 = doubled emitter on the −15 V pour, 2/3 = doubled base on the X21-LPF sense node, 6/7 = doubled collector on the BFG97-summing AGC drive node). The SO-8 surface-mount derivative of the classic TO-39 **2N3866** RF NPN. Specs: V_CEO 30 V, I_C 400 mA, P_TOT ≈ 1 W (with the 4-pin emitter heat-sink path), f_T ≈ 1 GHz, h_FE ≈ 100. Function in this circuit: NPN half of the complementary collector-modulated AGC pair, sourcing the BFG97 collector summing-junction current toward the −15 V rail in proportion to LO envelope sensed on the commoned base. Original failure: internal C-E latch-up pulling the joined pin 6/7 collector node to ≈ −14.72 V (Table D row 1; D.2 3866 row). | **Co-primary A: MRF3866 like-for-like** (or NOS 2N3866R / 2N3866JANTX in the SO-8 reflow-rework footprint with leg dressing). Sourcing 2024+: Motorola NOS via Microsemi / Microchip MRF-series catalog, Advanced Power Technology (APT), Advanced Semiconductor Inc. (ASI) — the MRF3866 is still on the ASI active-products list as of the 2021 datasheet refresh. **Co-primary B: NTE2511** (NTE Electronics direct cross-reference for 2N3866 — TO-39 NPN RF, V_CEO 30 V, I_C 400 mA, P_TOT 1 W, f_T ≈ 1 GHz; standard NPN TO-39 EBC pinout, leg-dress to SO-8 Case 751-05 Style 1 per the 2N3866 procedure). Datasheet: <https://www.tme.eu/Document/5321375d488a24e92c8cfb7f10d897a0/nte2511.pdf>. Stocked at TME, Newark, allied catalog channels — sustained current production, no NOS-channel risk. Acceptable substitutes: **MRF4427** (low-V variant, V_CEO 20 V, otherwise identical Case 751-05 Style 1 pinout and 200 MHz / 20 dB spec — fits the LO band), **MRF5812** (low-noise NPN, V_CEO 15–18 V, same package and pinout, slightly lower P_TOT). **Pin-1 dot must match the silkscreen dot** at fitting; do not swap the 3866 and 5160 footprints — fitting the NPN onto the +15 V pour will instantly forward-bias the C-B junction and destroy the part on power-up. |
| **5160** (R4N position, top mark `R4N ∥ 5160`) | **MRF5160** — Motorola SO-8 RF PNP, Case 751-05 Style 1 (same multi-pin pinout as the 3866 but with internal PNP polarity: 1/4/5/8 = doubled emitter on the +15 V pour, 6/7 = doubled collector on the BFG97-summing node sinking *toward* the AGC drive). The SO-8 derivative of the classic TO-39 **2N5160** PNP, explicitly designated by Motorola as the *complementary partner of the 2N3866* (the 2N5160 datasheet calls itself out as "Designed for Use in Complementary Circuits with 2N3866"). Specs: V_CEO −40 V, I_C −400 mA, f_T ≈ 100–250 MHz (PNP-equivalent of the 3866 with proportionally lower f_T per the standard NPN/PNP RF-pair mismatch). Function: PNP half of the complementary collector-modulated AGC pair, sinking BFG97 summing-junction current toward the +15 V rail. Original failure: internal C-E latch-up pulling the joined pin 6/7 collector node to ≈ +14.47 V with a ≈ 140 Ω on-die C-E path (Table D row 4a; D.2 5160 row). | **Co-primary A: MRF5160 like-for-like** (or NOS 2N5160 in TO-39 with leg dressing onto the SO-8 footprint — 1/4/5/8 emitter pour ↔ TO-39 emitter, 2/3 base pour ↔ TO-39 base, 6/7 collector pour ↔ TO-39 collector tab; known bench-bodge technique for the original Motorola SO-8 RF parts). **Co-primary B: NTE2512** (NTE Electronics direct cross-reference for 2N5160 — TO-39 PNP RF, V_CEO −40 V, I_C −400 mA, P_TOT 1 W, f_T ≈ 100–250 MHz, the explicit complementary partner of NTE2511; same NTE family / footprint / leg-dress procedure as the NTE2511 above). Stocked at TME, Newark, allied catalog channels — sustained current production, eliminates the SO-8 MRF5160 / TO-39 2N5160 NOS-channel availability risk. Listed as the Co-primary B alternative to the MRF5160 / 2N5160 NOS-only path documented below; pick whichever Co-primary lands in stock first. **Sourcing 2026 (verified, packaged TO-39 NOS)**: Jotrin Electronics (~500 in stock, Motorola / Freescale / NXP NOS, RoHS), Andysarcade.net (3 in stock @ $1.50 ea, min order 3, Motorola NOS date code 924), Radio741 (Greece, 15 in stock @ €6.60 ea, Motorola new surplus — likely the "Greek Surplus" channel referenced in the 2024 sourcing notes), Green Brook Online (20 in stock, multiple locations), Littlediode.com (3 immediate + more in 14 d, Microsemi-marked NOS); the SO-8 MRF5160 variant remains rarer than the TO-39 2N5160 — most channels stock the TO-39, fall back to the 2N5160 + leg dressing as primary execution. **Avoid**: SinLin's CP616-2N5160-CT listing (163 in stock) is **bare die only**, not packaged — skip unless die-attach capability available. **Avoid**: Central Semiconductor CP616-2N5160 family is **EOL per PDN011** (stock-only, exhaustion expected) — do not rely on Central as a future source. **Bench-bodge fallbacks (only if all of the above are exhausted):** (i) **2N5161** (Motorola PNP RF, TO-62, 60 V / 1.5 A / 500 MHz / 20 W; same Cc / fT / Tj as the 2N5160 but in a 7.85 mm stud-mount can vs TO-39's 5.84 mm — leg-dressing is mechanically awkward, the can would overhang the §7G compartment; available NOS at rfparts.com); (ii) **MRF521** (Motorola PNP RF, SOT-23 / SOT-143, fT 4.2 GHz; small-signal part rated ~200 mW / ~50 mA vs MRF5160's 1 W / 400 mA; AGC quiescent dissipation in this circuit is likely ~50–200 mW so MRF521 may survive in steady state, but no headroom for transients — a stress event that would survive the 2N5160 will likely kill the MRF521; available NOS at rfparts.com); (iii) generic SOT-23 PNP RF parts with similar small-signal envelope — BFT92 (fT 5 GHz, ~200 mW) — same caveats as MRF521. All three bench-bodge fallbacks count as **debug-only** and are not a sustainable rebuild — do not power on for extended periods. **Generic substitute spec (for any future cross-check):** complementary PNP RF transistor in the SO-8 Case 751-05 Style 1 pinout with V_CEO ≥ 20 V and f_T ≥ 100 MHz; SO-8 candidates with this footprint are essentially limited to the original Motorola RF SO-8 family. **Pin-1 dot must match the silkscreen dot** at fitting; do not swap the 3866 and 5160 footprints (same caveat as the 3866 row, mirrored polarity). |
| BFG97 (LO-buffer RF transistor, SOT-223; NXP/Philips wideband NPN, f_T ≈ 5 GHz) | Per §7D (γ), pin 4 (collector tab) is the **summing node for the 3866 / 5160 collector outputs** through 100 Ω + LC on each chip — i.e. the **actuator** of the AGC loop, gain-controlled by the complementary pair via collector-bias modulation. Bias network around the BFG97 includes: collector-load inductor (DCR a few Ω, pulled up to one of the ±15 V rails — polarity TBD by Table D row 7e), the two 100 Ω summing resistors back to the 3866 / 5160 pin 6/7 collectors, base divider, and emitter resistor(s). **Stress profile during the failure:** with both chips latched C-E (3866 collector ≈ −14.7 V, 5160 collector ≈ +14.5 V), the BFG97 collector was held near 0 V via the 100 Ω + 100 Ω summing network — saturation/cutoff edge for sustained period until power was removed; the collector-load inductor and 100 Ω summing resistors are the parts most at risk. | **Verify intact, no proactive replacement.** Run Table D rows 7c/7d (100 Ω summing path continuity, ≈ 100 Ω + small inductor DCR expected on each chip) and 7e (collector-load inductor finite to +V rail, OL to −V and GND) **before** fitting fresh 3866 / 5160 silicon. **If the BFG97 itself reads C-E shorted on diode test** (DMM red on collector tab, black on either emitter pad → near-zero both directions): replace with a like-for-like BFG97 (still in NXP catalog as of 2024, 2N3866 / BFR93A / MMBR951L are pin-incompatible RF NPN alternatives but require footprint adaptation — flag as a separate rework task). **If the collector-load inductor reads OL:** unmark its value off the surviving silkscreen / measure its resonant frequency from the LC tank and fit a like-for-like SMD wirewound inductor. **If a 100 Ω summing resistor reads OL or grossly off-value:** replace with a 100 Ω 1% SMD in the same case size. New §7G pending-work item logs the BFG97 bias-network walk-through (base divider values, emitter resistor value). |
| Per-chip supply filter (3866 / 5160 per-rail leg) | The earlier "fused open small SMD series resistor / ferrite bead" framing is **withdrawn** under §7D (γ) — pin 7 on each chip is the doubled collector node feeding the BFG97 summing junction, not a +V supply pin, so there is no "pin 7 → +V supply leg" filter to fail. Under the revised topology, the only series elements on the chips' emitter-bias path are the two 3R92s (pour ↔ rail), already covered by their own row below; there are no separate per-chip pi-filters or ferrite beads on the AGC supplies as previously assumed. **The 530 mV depression on the 5160's joined collector (pin 6/7 = +14.47 V vs +15 V pour)** is now read as the chip-internal C-E path through the damaged silicon (D.2 5160 row, ≈ 140 Ω) loading the joined collector node, not as a partial filter open. | **No replacement** — there is no part to replace at this entry. Withdrawn from the rebuild bill of materials. The original "3866 pin 7 +15 V leg" and "5160 pin 4 −15 V leg" entries are both moot under §7D (γ) and §7D (β) respectively. Row kept as a historical placeholder so the previous-revision rebuild plan can be cross-referenced. |
| 3866 / 5160 input-network LPF L1 / L2 (X21 cap-tap → commoned base node, T-section series legs per §7D revised topology) | small SMD trim inductor, value not yet measured (likely sub-µH given the LO frequency band) | **Conditional** — replace only if §7E-bench A3 / rebuild step 4 finds an open. Read value off the surviving leg of the matching pair (the network is symmetric across the cap-tap T) and fit a like-for-like SMD inductor of the same case size. If both legs are open, fall back to a wirewound 0.1 µH 1206 jumper as a debug substitute and record the post-rebuild AGC behaviour against the original spec to judge whether the substitute is acceptable. |
| 3866 / 5160 emitter-bias resistor (`3R92`, two places: 3866 emitter pour ↔ −15 V; 5160 emitter pour ↔ +15 V, per §7D revised topology) | precision 3.92 Ω SMD resistor (likely 0603 or 0805, tolerance ≤ 1%) | **Conditional** — replace only if §7E-bench A3 / Table D rows 5d/5e find an open or grossly off-value reading. Like-for-like 3.92 Ω 1% SMD resistor; tolerance matters because the resistor sets the per-chip emitter offset under the chip's quiescent draw, and a wider-tolerance part would shift the standing collector current of each AGC stage (effectively the operating point of the complementary pair's class-A bias). If 3.92 Ω 1% isn't on hand, a 3.9 Ω 1% in the same case size is acceptable as a temporary substitute; record post-rebuild joined pin 6/7 DC for FA. |

Other A0 candidates, in order of preference (kept for the future-
rebuild record — only relevant if neither co-primary, HSMS-2800-BLKG
nor MA4E1340A1-287T (and the HSMS-280B-BLKG SOT-323-on-SOT-23 bench-
bodge sister), is available at rebuild time):

- **BAS70-06** (NXP/Nexperia/Vishay, SOT-23 **common-anode** dual
  Schottky: pin 1 = K1, pin 2 = K2, pin 3 = common A) — fits the
  footprint in **natural orientation** (part pin 1 K → footprint
  pad 1 K, part pin 3 A → footprint pad 3 A, part pin 2 K2 lands
  on footprint pad 2 NC where D2's cathode floats benignly with
  D2's anode tied to the active node — no current loop, no
  behavioural impact). Vf ≈ 0.36 … 0.41 V at 1 mA, +20 … +70 mV
  vs HSMS-2800. **First-choice fallback** because the natural
  orientation eliminates one mistake-vector at rebuild time vs the
  rotated-180° BAT54C / BAS70-05 alternatives.
- **BAT54C** (ON Semi / Diodes Inc / Vishay, SOT-23 common-cathode
  dual Schottky, marking `L43`) — Vf ≈ 0.32 V at 1 mA, closest
  on-hand Vf match to the HSMS-2800 (0.34 V at 1 mA). 180°-rotation
  rule per the §7E table row above. Second-choice fallback (lower
  Vf than BAS70-06 but requires rotation).
- **BAS70-05** (Vishay/NXP, SOT-23 common-cathode dual Schottky:
  pin 1 = A1, pin 2 = A2, pin 3 = K) — also on hand. Identical
  topology and 180°-rotation rule as BAT54C; Vf ≈ 0.36 … 0.41 V at
  1 mA, identical Vf bracket to BAS70-06. Third-choice fallback
  (no advantage over BAS70-06 except possibly bench stock).
- **HSMS-286C / HSMS-286K** (Avago/Broadcom, SOT-323 series-pair /
  common-cathode pair, **low-barrier** Schottky, Vf ≈ 0.28 … 0.34 V
  at 1 mA) — best electrical match to the HSMS-2800 barrier height
  among the duals. Mechanical caveat: SOT-323 is physically smaller
  than SOT-23 (~2.0 × 1.25 mm vs 2.9 × 1.4 mm), so the part lands
  on the inner edges of the footprint pads — bench-bodge fit,
  acceptable but ugly. Use one of the two diodes; same 180°-rotation
  rule as BAT54C to put the cathode on footprint pin 1.
- **HSMS-282C / HSMS-282K** (SOT-323, **standard-barrier** pairs,
  Vf ≈ 0.34 … 0.38 V at 1 mA) — same SOT-323 mechanical bodge as
  286C/K, no Vf-match advantage.
- **BAT17-04** (Infineon, SOT-323 common-cathode dual HF Schottky:
  pin 1 = K common, pin 2 = A1, pin 3 = A2; in-stock per the
  diode-bin scan 2026-04-30) — **low-barrier**, Vf ≈ 0.31 V at
  1 mA, Cj ≈ 0.7 pF (lower than HSMS-286C/K), f_cutoff > 4 GHz.
  Best HF Cj among the on-hand SOT-323 duals; electrically a
  sibling to HSMS-286C/K with the same SOT-323 → SOT-23 mechanical
  bodge (sits on inner pad edges) and same 180°-rotation rule to
  put the cathode on footprint pin 1. **VBR 4 V minimum is the
  catch:** adequate for **V61 / V62 doubler-pair duty** (V_pk ≈
  1.5…3.5 V at +12…+16 dBm 100 MHz drive, inside spec), **NOT
  adequate for the DIAGSAMP single-A0 rectifier** (V_pk ≈ 7 V on
  the X21 RF tap at +27 dBm 200 MHz peak, exceeds VBR). Role-
  restricted substitute — V61 / V62 only, not drop-everywhere.
- **HSMS-2822** (SOT-23 series pair, standard-barrier, Vf ≈ 0.34 …
  0.38 V at 1 mA; in-stock per the ATIK-DK01 kit) — physically
  fits the SOT-23 land pattern, but the middle pin is the
  series-junction node (anode of D1 / cathode of D2) and this
  footprint has pin 2 NC, so neither diode is reachable as-fitted.
  Workaround: bridge footprint pad 2 to pad 3 with a small solder
  fillet, which shorts D2 and leaves D1 active with anode on
  pin 3 / cathode on pin 1 — correct polarity, no rotation.
  Functional but a bench bodge.
- **1N5711WS-7-F** (Diodes Inc, SOD-323 single Schottky, 70 V VBR,
  150 mW; in-stock per the diode-bin scan 2026-04-30) —
  **medium-barrier**, Vf ≈ 0.41 V at 1 mA (+70 mV vs HSMS-2800),
  Cj ≈ 2 pF, classic 1N5711 HF RF Schottky lineage. **VBR 70 V is
  the highest of any on-hand candidate** — the only on-hand single
  Schottky with comfortable headroom for the DIAGSAMP A0 site
  (V_pk ≈ 7 V vs 70 V VBR = 10× margin; vs the BAT17-04's 4 V VBR
  which fails the same site). Mechanical: SOD-323 (≈ 1.7 × 1.25 mm)
  is smaller than SOT-23 (≈ 2.9 × 1.4 mm), so it dead-bugs onto
  the SOT-23 pads — anode lead onto footprint pad 3, cathode lead
  onto pad 1, body floating over pad 2 NC. Bench-bodge fallback
  for the DIAGSAMP single-A0 site only, when SOT-23 stock-out
  forces it; +70 mV Vf offset is benign at the +7.5 … +11 V
  DIAGSAMP spec window (≤ 1 % shift).
- **HSMS-2825 / HSMS-2865** — ring-quad Schottkys in SOT-143
  (4-pin), wrong package, discount. **BAT62** (Infineon SOT-143
  dual HF Schottky, Cj ≈ 0.35 pF) and **HSMS-8202** (Avago SOT-23
  X-band mixer pair, Cj ≈ 0.3 pF, Vf ≈ 0.5 V medium-barrier) on
  hand — both fall in the same SOT-143 / mixer-pair discount class
  and are noted only for completeness; better SOT-23 single
  options exist on hand.

A0 is now confirmed as **HP/Avago HSMS-2800** (single low-barrier RF
Schottky in SOT-23, top mark `A0` family code + date/lot character)
by combining (i) the microscope top-mark read on a sister A211 board
(`A0E` decoded as `A0` family code + `E` date/lot character — the
HSMS-280x catalog has no `A0E` lead-code suffix, singles in SOT-23
are `A00` and singles in SOT-323 are `A0B`, common-anode variants
use the `A3*` prefix), (ii) the bench topology (pin 2 truly NC,
falsifying all dual / common-anode HSMS-280x variants), and (iii)
the bench Vf reading (0.23 … 0.27 V at DMM Itest, consistent with
the HSMS-2800 low-barrier family). HSMS-2800-BLKG drops directly
into the SOT-23 footprint with no rotation and no Vf-offset caveat.
The **MACOM MA4E1340A1-287T** is the co-primary alternative (single
medium-barrier Si Schottky in SOT-23, currently in production at
MACOM, current 2024 distributor stock — see §7E table A0 row for
SKU detail and `maom-s-a0010058398-1.pdf` for the datasheet); it
must be fitted **rotated 180°** because the MACOM SOT-23 single uses
pin 1 = anode, pin 3 = cathode (opposite polarity convention to
HP/Avago) and the +70 mV medium-barrier Vf offset is negligible
against the +7.5 … +11 V DIAGSAMP spec window. The BAT54C / BAS70-05
/ HSMS-28xx-pair options above remain as on-hand fallbacks for the
case where neither co-primary can be sourced in time. The DIAGSAMP
path is open-loop (no op-amp behind A0 to absorb Vf offset), but
the in-spec band on DIAGSAMP is wide (+7.5 … +11 V, a 3.5 V window)
so even the ±100 mV Vf delta of the worst-case fallback sits well
inside the in-spec range.

> ⚠ **The MC34071 / MC340xx op-amp candidate paragraphs below are
> SUPERSEDED under §7D (γ) — retained as historical FA record only.**
> The R4D / R4N positions are now identified as **MRF3866** (NPN) +
> **MRF5160** (PNP) — Motorola SO-8 RF transistors in Case 751-05
> Style 1, not op-amps. The op-amp reading is triple-falsified and
> any MC34071-class substitution into either footprint would destroy
> the part on power-up (V− pin onto +15 V pour, OUT shorted to V+
> through the doubled-collector trace). Use the §7E Replacements
> table (3866 / 5160 rows) for the resolved sourcing path.

Why MC34071 over the precision-op-amp alternatives: the original
chip was *originally hypothesised* to be a Motorola house-marked
SOIC-8 single op-amp from the early-1990s SMP02 design era — that
hypothesis is now withdrawn (see banner above). The MC340xx family
(Motorola, now ON Semi)
is the most plausible original part — Motorola was known for
issuing custom markings on this family for OEM customers like R&S,
HP, Tek and W&G in the 1985–95 period; the topology (bipolar
Darlington input with ground-sensing common-mode range, all-NPN
output stage, 13 V/µs slew rate, 0–10 nF capacitive-load tolerance)
fits an envelope-detector buffer + integrator driving a varactor
or PIN-bias node; and the ±22 V abs-max gives 7 V of rail headroom
at ±15 V operation. We do not have direct BOM proof, so this is
a strongly-supported guess rather than a confirmed identification.

Other op-amp candidates that drop in physically with the same
standard `V+ = 7 / V− = 4 / OUT = 6` pinout (kept for the future-
rebuild record, in case MC34071 isn't on hand):

- **MC33071DG / MC33071ADG** (industrial temperature range, −40 …
  +85 °C; otherwise identical to MC34071) — marginally preferred
  over MC34071DR2G if available, but the ALC cluster runs near
  ambient inside the SMP, so the temp-range upgrade is purely
  belt-and-braces.
- **OP07 / OP27 / TLE2027 / OP07CDR** — precision bipolar singles,
  ±18 … ±22 V rated. Win on DC offset (25–75 µV typ vs 1.5 mV) but
  lose on slew rate (0.3 … 2.8 V/µs vs 13 V/µs). The integrator
  set-point is trimmed by the divider after rebuild so the offset
  win is mostly absorbed; the slew-rate loss may slightly slow the
  loop's response to a frequency step. Acceptable bench substitute.
- **LT1677CS8** — pin-compatible and functional, but at the top of
  its rated supply range at ±15 V (3 V to ±15 V max recommended,
  ±22 V abs-max) with no rail headroom for transients, and its
  rail-to-rail input topology is unused (and adds an NPN/PNP
  handoff that this circuit doesn't need). Acceptable as a
  last-resort substitute if nothing else is on hand.

Avoid: any **dual** SOIC-8 op-amp (pinout has V+ on pin 8, not 7,
plus extra in/out pins on 1 / 5 / 7 — would short V+ rail to amp B's
output on power-up); any **current-feedback** RF amp (e.g. AD8008 —
wrong topology, will oscillate in this slow ALC integrator); any
**rail-to-rail-only / CMOS / zero-drift** part where the input
common-mode range or input-bias-current behaviour differs
significantly from a 1990s bipolar single-supply op-amp (functional
but may shift the ALC trim point).

**Pad-to-rail check (instrument off, all three failed parts removed —
do this BEFORE fitting new chips):**

The diagnostic is *open vs not-open*, not an absolute resistance
ceiling — R&S's per-chip filter value on this PCB isn't documented in
the §7.1.7 BOM, and from the powered reading B7 = +14.47 V vs N90
pin 7 = +15.08 V (0.61 V drop on the *intact* +15 V leg) the filter R
could plausibly sit anywhere from ~20 Ω to ~600 Ω and still be
healthy. The reliable anchors are **W216.1** (+15 V entry to A211)
and **W216.5** (−15 V entry to A211) — both available right at the
A211 cable connector and known good if Step 1 / Step 2 passed (this
unit: W216.1 = +15.28 V, W216.5 within spec):

| # | Probe (DMM ohm mode, A211 unpowered) | Expected (intact filter) | This unit |
|---|---------------------------------------|--------------------------|-----------|
| 1 | W216.1 (+15 V) → 3866 pin 7 footprint | finite, low (tens to a few hundred Ω = the 3866's +15 V filter R + trace IR) | |
| 2 | W216.1 (+15 V) → 5160 pin 7 footprint | finite, low (= the 5160's +15 V filter R; should match #1 if R&S used identical filters on both chips) | |
| 3 | W216.5 (−15 V) → 3866 pin 4 footprint | finite, low (= the 3866's −15 V filter R) | |
| 4 | W216.5 (−15 V) → 5160 pin 4 footprint | finite, low (= the 5160's −15 V filter R; should match #3) | |
| 5 | W216.1 (+15 V) → N90 pin 7 (OP97 V+) | finite, low — sanity check, OP97 reads clean +15 V powered, this confirms its DC path is unbroken | |
| 6 | W216.5 (−15 V) → N90 pin 4 (OP97 V−) | finite, low — same sanity check on the −15 V leg | |

Predicted on this unit per the D.3 mirror-symmetric analysis:

- **Row 1: OPEN** (kilo-ohms / OL — the 3866's +15 V filter is the
  fused part); Row 2: finite, low.
- **Row 4: OPEN** (the 5160's −15 V filter is the fused part); Row 3:
  finite, low.
- Rows 5 / 6: both finite, low — bonus confirmation that the W216
  ±15 V conductors and the A211 supply distribution to N90 are all
  intact. If either reads OPEN, the fault scope expands beyond the
  3866 / 5160 pair (broken trace or bulk bypass cap shorted) —
  escalate before any chip rebuild.

> ⚠ **In-circuit ohm readings are not diagnostic for this test.**
> With chips fitted, the dies offer multiple sneak paths between
> +15 V and −15 V (V+/V− internal short ≈ 140 Ω on each chip,
> substrate diodes, output-to-V+ shorts), so finite readings on all
> four legs do *not* prove the filters are intact. The earlier in-
> circuit reading of `W216.5 → 5160 pin 4 = 0 Ω` for instance can
> equally well be (a) the 5160's −V filter intact, *or* (b) the
> 5160's −V filter fused, with the 0 Ω coming via `−15 V →
> 3866-pin-4-filter → 3866-die → 3866-pin-7 → +15 V →
> 5160-pin-7-filter → 5160-die → 5160-pin-4`. The four powered-DC
> readings (3866 pin 7 = −14.72 V, 5160 pin 4 = +15.09 V, etc.)
> remain the authoritative evidence for the fused-filter hypothesis
> because the regulators clamp the rails and only a true high-
> impedance break can rail a supply pin to the *opposite* rail. The
> chips-off rerun of the four rows above is what makes the ohm test
> diagnostic again.

Once rows 1 / 4 are confirmed open, trace from each open footprint
along the copper toward the nearest +15 V / −15 V bypass cap; the
fused part sits on that run, typically a small SMD resistor or
ferrite bead. **Use the matching healthy leg (row 2 for the +15 V
filter, row 3 for the −15 V filter) to read off the original filter
value** — drop the same value into the open leg, or fall back to a
22 Ω 1206 if both ends are unreadable.

(Optional secondary cross-check, only if you want defence-in-depth:
also probe 3866 pin 7 ↔ 5160 pin 7 and 3866 pin 4 ↔ 5160 pin 4
directly — 3866-vs-5160 symmetry on the same rail. Same logic, same
verdict, just without W216 in the loop.)

Verification sequence (instrument back on, `--a21-probe` at 3 GHz /
POW −30, casing on, **still no SA on X21**):

1. Fill **Table D' (post-rebuild)** below — same probe points as the
   pre-rebuild Table D, with the failure data preserved in §7D for
   reference.
2. Pass criteria for Table D' — every row in *Expected (post-rebuild)*:
   chip supply pins clean ±V, both pin 6 outputs mid-rail (not
   railed), 3R92 dropping a few mV DC, X21 a small clean DC offset.
3. **Read X75 / TP1910 from the `--a21-probe` output.** Pass criterion:
   TP1910 climbs to **7.5 … 11 V** (§7.4.1 nominal). This is the
   ultimate alive/dead test for the LO chain — if X75 reads in spec,
   the rebuild has restored the full A21 → casing → IF path and **no
   SA work on X21 is required**.
4. Repeat Table A rows 1–3 — the bias chain should still pass exactly
   as it did pre-rebuild (X95 ≈ −0.7 V, X96 ≈ +6.2 V, X72 ≈ +15 V).

**Table D' — post-rebuild verification readings:**

| # | Probe point (Side B, lower cluster) | Expected (post-rebuild) | Measured | Verdict |
|---|--------------------------------------|--------------------------|----------|---------|
| 1 | 3866 pin 7 (joined collector node, post-rebuild expectation under §7D γ — at the BFG97-collector bias point, no longer railed) | at the BFG97-collector bias point (rail-mid range, set by the BFG97 collector load and the two 100 Ω summing resistors) | | |
| 2 | 3866 pin 4 (emitter pour, on −15 V via 3R92) | clean −V rail (≈ −15 V, ±0.5 V of N90 pin 4) | | |
| 3 | 3866 pin 6 (= pin 7 by board-level short; same as row 1) | reads identical to row 1 | | |
| 4 | 5160 pin 6 (= pin 7 by board-level short; same as row 4a) | reads identical to row 4a | | |
| 4a| 5160 pin 7 (joined collector node, post-rebuild expectation under §7D γ — at the BFG97-collector bias point) | at the BFG97-collector bias point | | |
| 4b| 5160 pin 4 (emitter pour, on +15 V via 3R92) | clean +V rail (≈ +15 V, ±0.5 V of N90 pin 7) | | |
| 5 | V across the ≈ 3R92 precision R | finite DC, mV-scale (rectified envelope present); some RF ripple normal | | |
| 6 | DC at the X21 brass pin (DMM only — **no SA until Step 8 with the ≥30 dB / ≥1 W pad**) | small clean DC offset (≈ 0 V to tens of mV) | | |

If Table D′ passes **and** TP1910 reads 7.5 … 11 V, the rebuild is
verified end-to-end — the instrument is restored. Step 8 (SA on X21)
is **not required** in this case.

If Table D′ passes but TP1910 stays dead (≈ 0.22 V as in the
pre-rebuild Step 4 reading), the ALC cluster is healthy but
something downstream of A211 is broken — proceed to Step 8 as a
**diagnostic** to localise the fault between X21 (LO drive into the
casing) and A212 / V1.1-V1.2 / V75 / A211 diag rectifier.

If any Table D′ row fails after rebuild, jump to the recurring-failure
escalation list below.

Recurring-failure escalation:

- New A0 / 3866 / 5160 die within minutes of power-up → upstream LO
  chain on the on-PCB side (V50/V60/V2/V3/V4) is over-driving X21 →
  the detector keeps getting punched through. Do **not** rebuild a
  third time until the LO-chain output is bounded; **escalate to
  Step 8 with the ≥30 dB / ≥1 W pad first** to measure the actual
  X21 power level, and if it exceeds +30 dBm, fault-find on the LO
  chain proper before another A0 fitting.
- Outputs still railed but new parts cool to the touch → trim pot /
  set-point divider drift (cermet wiper open, or 750 Ω / 10 kΩ
  resistor cracked) → re-trim per §7.4.4 or replace the network.
- Loop oscillating (visible AC ripple on the 5160 pin 6/7 collector
  node, casing audibly squealing) → bulk-bypass electrolytics on
  the cluster left edge dried out → replace both.
- Chips-off pad-to-rail check returned **all four legs finite and
  roughly equal** (no OPEN on rows 1 / 4) → the fused-filter branch
  of the failure model was wrong. This branch is now **withdrawn**
  outright under §7D γ (the per-chip pin-7 supply filters do not
  exist). Fix is then the chip swap alone — no filter parts to
  replace — and the powered-DC anomaly should clear after fitting
  the new 3866 / 5160. Re-run Table D′ rows 1 / 4a / 4b to confirm.

Pass (Step 7D after rebuild) + X75 / TP1910 in spec → ALC restored
and full chain verified, **no further steps required**. Pass but X75
still dead → proceed to **Step 8** with the SA + ≥30 dB / ≥1 W pad
as a diagnostic to verify the absolute X21 LO level (206…234 MHz at
+26…+30 dBm) and localise the downstream fault.

### Step 7F — X50 → V50/V60 LO cascade amp: bench tracing *(Side B, optional during rebuild)*

> **History:** the original "§7F ALC-actuator hypothesis" framing
> (X50 cascade-amp gate-bias as the AGC actuator, driven from
> 5160 pin 6 onto the 1501 → Node B path) is **superseded** by the
> recovered schematic — see [H-2026-04-30-7f-alc-actuator-hypothesis-superseded](smp_history.md#h-2026-04-30-7f-alc-actuator-hypothesis-superseded).
> The X50 cascade-amp topology bench-trace below remains correct as
> a description of an upstream LO-chain stage; the actuator-path
> verification belongs to Table D rows 7c/7d/7e (BFG97 collector
> network) per §7D.0.

This subsection documents the bench-traced topology of the X50
cascade amp so the rebuild can verify the upstream LO-chain stage
intact pre- and post-fit. Hypothesis flags follow the §7D convention
— **(C)** confirmed by trace, **(I)** inferred from topology,
**(H)** hypothesis pending bench verification.

**Bench-confirmed input network** (Side B, top-left of the inner
shield, all components SMD chip-style):

```
                                 ┌──[10R0]──► pin 1 LEFT 420 MMIC (no series cap)
   X50 ──[12R1]──┬──[Cblock]── A ┤
   SMB           │                │
              [82R5]              └──[1001]── B ──[1001]──[47R5]──► pin 1 RIGHT 420 MMIC
                 │                            │   │ (47R5 RF-bypassed both sides
                GND                           │   │  → DC-only feed; right pin 1
                                              │   │  is RF-grounded at the chip pad)
                                          [3571] [1501]
                                              │   │
                                             GND  W216.5 (−15 V)
```

**"420" MMIC identification — schematic-confirmed (C, 2026-04-30)**:
both chips are **AT-42085-B per the recovered Var.02 schematic**
([rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg](rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg)),
device class = **NPN silicon bipolar**, f_T = 8 GHz, P1dB ≈ +20.5
dBm @ 1 GHz, datasheet bias 8 V / 35 mA class-A. Package = 4-lead
85-mil plastic / SOT-86 footprint. Triangle logo = HP house glyph;
"420" is the AT-42085-B family digit code, not a lot / date code.

> **History:** the earlier "discrete 4-lead GaAs FET / PHEMT"
> identification (Avantek ATF-13135 / ATF-13284 / ATF-10135
> candidates) is **superseded** by the schematic AT-42085-B NPN ID
> — see [H-2026-04-30-7f-gaas-fet-id-superseded](smp_history.md#h-2026-04-30-7f-gaas-fet-id-superseded).
> The bench-trace observations originally collected under the GaAs
> FET reading are retained in the "Bench-traced observations"
> subsection below as raw data; the **OPEN device-class /
> pin-mapping reconciliation** item — the bench-traced 3570 / 1500
> / 1001 divider giving V_B ≈ −10.6 V does not reconcile with NPN
> base biasing (V_BE wants ≈ +0.7 V) — remains active and is to be
> cleared at the next bench session by DMM diode-test on V50
> in-circuit + R-value sweep against schematic R49 / R59 (see
> action items in [`smp_next.md`](smp_next.md)).

**Bench-traced observations (retained for reconciliation):**

- **NOT** a Mini-Circuits MAR / ERA / Avantek MSA Darlington — the
  left chip's **pin 4 is solder-blob-grounded (bench-confirmed)**,
  which would short the output + Vcc on a canonical Darlington
  pinout. Under the schematic-confirmed AT-42085-B NPN ID this
  observation is consistent with pin 4 = Emitter tied directly to
  GND (common-emitter); preserved here as the bench finding that
  originally ruled out the Darlington class and that still anchors
  the pin-mapping question above.
- Provisional GaAs-FET pinout originally inferred (now superseded):
  pin 1 = Gate, pin 2 = Drain, pins 3 / 4 = Source. Under the
  schematic-confirmed NPN reading, the **working pinout** is
  pin 4 = Emitter (solder-blob GND, bench-confirmed), pin 2 =
  Collector (RF output + Vcc entry through the on-board choke),
  pin 1 = Base (RF input + DC bias from the upstream divider) —
  pinout-vs-silkscreen orientation to be verified at next bench
  session per the OPEN item above.

**Architecture under schematic-confirmed NPN ID:** two-stage cascade
NPN bipolar amplifier. RF enters the LEFT chip's pin 1 DC-coupled
from Node A; the RIGHT chip's pin 1 is RF-grounded (DC-only feed
through 47R5 with bilateral RF bypass) and serves as a bias-control
input under the original bench reading. Under the NPN reading the
right MMIC's RF input must be on a non-pin-1 lead fed by an
inter-stage match from the left MMIC's pin 2 — the inter-stage
section is **not yet bench-traced** and the bias-control framing of
the right pin 1 is part of the OPEN reconciliation item above.

**Bench-traced DC divider (Side B, Node B):**
V_A = V_B (no current through the 1001 between A and B), and at B,
treating pin 1 as high-Z (correct for both GaAs gate AND NPN base
under no-current open-circuit):

```
V_B / 3570  +  (V_B + 15) / 1500  =  0   →   V_B = −10.6 V
```

Under the original GaAs reading: V_B = −10.6 V was "too negative
for normal GaAs gate bias (V_gs ≈ −0.5 to −2 V)" and was attributed
to an active control element on the 1500 → W216.5 leg lifting V_B
into the operating window under closed-loop ALC. Under the
schematic-confirmed NPN reading: V_B = −10.6 V is **not a valid
base-bias point at all** (V_BE ≈ +0.7 V required), so the divider
net itself is most likely mis-mapped against the schematic R49 /
R59 — re-trace and R-value sweep is the next-session action.

**ALC actuator hypothesis (H) — WITHDRAWN under §7D (γ).** Retained
verbatim below for FA record; the actual AGC actuator is the BFG97
LO-buffer collector, not this cascade-amp gate-bias node.

```
   5160 pin 6/7  ──►  ALC control element (TBD)  ──►  bottom of 1501  ──►  Node B
   (joined           (SOT-23 / SOT-89                                    (FET gate
    collector         transistor or FET,                                  bias)
    output)           located between the
                      1501 via and W216.5)
```

Loop polarity (as originally proposed): envelope detected > setpoint
→ the 5160 collector drives the actuator → V_B more negative → FET
gain reduced → envelope returns to setpoint. Negative feedback,
stable. **Withdrawn:** the 5160 collector node actually drives the
BFG97 collector summing junction (per §7D γ), not a separate
cascade-amp gate-bias actuator on the 1501 leg.

**Bench checks — priority order.** Run the powered DC sequence first
(rows P1–P6 below) — a single reading at Node B (P2) collapses most
of the open hypotheses without needing to identify the actuator part
first. Fall back to the unpowered ohm trace (rows U1–U3) only when
the powered readings indicate the actuator is absent / failed-open,
or when the board cannot be safely powered.

**Powered DC sequence** *(instrument on, DMM DC volts, casing or at
least the inner shield in place, commanded RF frequency in mid-band
so the LO chain is active; do this **once before** the §7E rebuild as
a baseline and **once after** as the verification)*:

| # | Probe | Expected (loop healthy) | Expected (actuator absent) | This unit |
|---|-------|-------------------------|----------------------------|-----------|
| P1 | W216.1 (+15 V), W216.4 (+7.5 V), W216.5 (−15 V) at the connector | within ±5 % | same | |
| P2 | **Node B** (junction of the two 1001s + 1501 top + 3571 top) — *most diagnostic single reading* | **−0.5 to −2 V**, *moves* when commanded RF freq / level is swept | **≈ −10.6 V** (open-circuit divider value) | |
| P3 | Node A (post-DC-block, top of inner 1001) | matches Node B (high-Z gate, no DC drop across the inter-node 1001) | matches Node B | |
| P4 | Pin 2 (drain) of LEFT 420 | +5 to +7 V (Vdd − R_drop, off W216.4 +7.5 V rail) | 0 V (no I_d) **or** full +Vdd (no R_drop drop) — either way FET pinched off | |
| P5 | Pin 2 (drain) of RIGHT 420 | same as P4 | same as P4 | |
| P6 | 5160 pin 6 (joined collector node, per §7D γ — historical: was assumed to be the AGC error-amp output driving the cascade-amp gate; superseded) | a few volts, *moves* when commanded RF level / freq is changed | rail-stuck (≈ +13 or −13 V) | |

Verdicts off **P2** (the single most diagnostic reading):

- **−0.5 to −2 V, moves with commanded freq/level** → loop active,
  actuator present and working, cascade amp healthy. The actuator
  part doesn't need to be identified to declare this section
  passing. Move on to Step 8.
- **≈ −10.6 V** (matches the open-circuit divider exactly) →
  actuator **absent or failed-open**, FETs fully pinched off →
  cascade amp dead → fall back to the unpowered ohm trace below to
  find and repair the actuator. Also the prediction if the 5160 is
  dead and its pin 6 floats high-Z, so cross-check with P6.
- **Near 0 V or going positive** → actuator over-driving the gate
  node (5160 collector output railed to −V_sat pulling V_B toward
  0 V via the actuator, or the actuator shorted bottom-to-top) →
  loop dynamics inverted or broken; cross-check P6 first.
- **Stable, anywhere else, doesn't move with freq** → loop open;
  P6 then tells you whether the break is integrator-side (P6
  rail-stuck) or actuator-side (P6 moves but P2 doesn't follow).

**Unpowered ohm trace** *(instrument off, DMM ohm mode, A211
unpowered — fallback when P2 indicates actuator absent / failed-open,
or when the board can't be safely powered)*:

| # | Probe | Expected | This unit |
|---|-------|----------|-----------|
| U1 | 1501 via → W216.5 directly (DMM ohm) | finite, **not** a hard short — at least one active part in between | |
| U2 | 1501 via → 5160 pin 6 (DMM ohm) | finite, kΩ-scale via a base / gate resistor | |
| U3 | Identify the SOT-23 / SOT-89 between 1501 and W216.5 | small 3-lead active part on that trace | |

**Probe-load caution on P2 / P3**: the gate node is the X50 LO RF
trace itself, so a long DMM probe lead at Node A / Node B can detune
the FET input match at LO frequency and the LO output level on the
SA may jump when the probe touches. That doesn't damage anything but
can mislead the reading. Prefer a short-pigtail 10× scope probe in
DC-coupled DMM mode if available; a plain DMM lead is acceptable but
treat the result as 50–100 mV optimistic.

**3866 / 5160 rebuild caveat**: if the §7E rebuild is still pending
and the original 3866 / 5160 chips are suspect, P2 will read whatever
the broken AGC pair happens to command — informative as a baseline,
but the *real* verification reading is the post-rebuild one.

**Step 8 escalation**: P2 in spec **and** P4/P5 in spec **and** X21
still dead at Step 8 → fault is downstream of the cascade amp
(V50/V60 doubler, V2/V3/V4 LO amps, or the step-recovery / comb
generator); proceed to band-3 §7.4.1 component-level fault-finding.

**Bench update — back-side rail discovery (supersedes the
"actuator-on-front-face" hypothesis above)**: the 1501 leg does **not**
go directly from Node B to W216.5. Tracing through the back face:

- The bottom-of-1501 via lands on the **back-side at the top of a
  61R9 (61.9 Ω) resistor (C)**. That same node is heavily bypassed
  with multiple shunt caps distributed across the back face — i.e. it
  is a **distributed regulated rail**, not a per-stage injection
  point.
- The other end of 61R9 is a single short trace (upside-down T) into
  **two back→front vias (C)** that come up on the front face at the
  **MMIC pins 2/3 of both chips (C)** — i.e. pins 2 and 3 of the LEFT
  and RIGHT 420 are tied together onto this rail through 61R9 + via
  inductance.
- DMM continuity: **pin 2/3 cluster → W216.5 ≈ 65 Ω (C)** ≈ 61R9 +
  trace, so the rail also reaches W216.5 via a low-Ω path on the back
  (final segment between the rail and W216.5 not yet traced — likely
  the actuator's pass element or a further filter R).
- DMM continuity: leftmost SOT-23 in the back-top compartment, **pin 3
  → W216.5 ≈ 1.9 Ω (C)**. Under standard EIA/JEDEC SOT-23 pinout
  (pin 1 = base, pin 2 = emitter, pin 3 = collector), pin 3 is the
  **collector**, so this reads as a collector tied near −15 V through
  a small load / ballast R — consistent with an NPN current-sink /
  open-collector output stage whose collector returns to the negative
  rail via the load, or a PNP common-collector follower with collector
  returned to −15 V through the ballast. (Earlier "emitter on the
  −15 V pour / PNP pass-transistor" reading required pin 3 = emitter
  per JEITA SC-59 and is **withdrawn**.)

Corrected architecture sketch:

```
  Node B (front) ──[1501]── via ─┐                           front side
  ────────────────────────────────┼─────────────────────────────────────
                                  │                          back side
                            distributed rail ──[shunt caps to GND × N]
                                  │           (decoupling spread across
                                  │            back face)
                                [61R9]                       BIAS NODE
                                  │
                            ┌─────┴─────┐
                            │           │
                          via         via
                            │           │
  ────────────────────────────────────────────────────────── front side
                            │           │
                       pins 2/3      pins 2/3
                       LEFT 420      RIGHT 420
```

W216.5 (−15 V) reaches the distributed rail through a back-side path
into the FET operating window. The earlier reading that the **back-
top compartment block** (then read as LP356M + SOT-23 cluster) acts
as the pass element of an op-amp servo lifting that rail is
**withdrawn** under the §7G re-identification of that chip as an
**LP365M quad comparator** (see §7G); the §7F rail's origin is
therefore **TBD**, with the most likely candidates being a passive
divider / Zener clamp on the −15 V pour, or a discrete pass element
located elsewhere on the board not co-located with the LP365M.
Under the revised reading the LP365M's role wrt the §7F rail is at
most monitoring (and possibly hysteretic protection switching of
whatever pass element does drive the rail, if the §7G G8 cross-
correlation lands an OUT pin on a SOT-23 base); see §7G topology
note.

**Pinout interpretation — flagged unresolved (H)**: §7F earlier
assigns pin 1 = Gate / pins 3,4 = Source / pin 2 = Drain on the GaAs-
FET reading. With pins 2 *and* 3 now confirmed as DC bias-rail inputs
(not RF drain / GND respectively), that pinout is no longer consistent
and must be revisited before the rebuild. Two readings that survive:

- pin 1 LEFT = RF input (DC + RF coupled from Node A through 10R0) — **(C)**
- pin 4 LEFT = GND (solder-blob short) — **(C)**

Open: which of pins 2 / 3 is RF-active (drain/output) vs DC-only
bias, whether pins 2 and 3 are tied at the chip pad or only via the
external rail, and where the inter-stage RF path (LEFT chip → RIGHT
chip RF input) actually leaves the LEFT package. The chips may not
be a depletion-FET cascade at all — candidates back on the table
include a **dual-gate FET** (G1 = pin 1 RF-in, G2 = pin 2 *or* 3
AGC bias), a **cascode pair** (pin 2 = upper-FET source, pin 3 =
upper-FET gate-bias), or a 4-lead **GaAs voltage-variable
attenuator / AGC IC** with two control pins. Resolution requires
either reading the part number off-board or RF-tracing pin 2 vs 3
separately on the right chip.

**Updated DC math.** With the rail at V_rail (set by the back-side
regulator, see §7G) and pins 1 / 2 / 3 all high-Z DC, no current flows
through 61R9 → **pins 2/3 sit at V_rail directly (I)**. At Node B,
KCL through 1501 (to V_rail) and 3571 (to GND) gives:

```
V_B / 3570  +  (V_B − V_rail) / 1500  =  0
   →   V_B  =  V_rail · 3570 / (3570 + 1500)
   →   V_B  ≈  0.704 · V_rail
```

Examples: V_rail = −2 V → V_B ≈ −1.4 V (healthy); V_rail = 0 V →
V_B = 0 V (regulator dead / output stuck high); V_rail = −15 V →
V_B ≈ −10.6 V (regulator bypassed / shorted, cascade pinched off).
The 0.704 factor means V_B and pin 2/3 always move together but pins
2/3 swing **harder negative** than V_B by ≈ 30 % — useful when
reading both with a DMM.

**Probe-table additions** (extend the P-sequence above):

| # | Probe | Expected (regulator healthy) | Expected (regulator absent / dead) | This unit |
|---|-------|------------------------------|------------------------------------|-----------|
| P7 | Top of 61R9 (back face) — the distributed rail node = same DC as pin 2/3 cluster | ≈ V_rail in the **−1 to −3 V** window, *stable* (regulator) — *or* slowly varying with commanded RF freq / level if the regulator turns out to be closed-loop on an LO-envelope sense path (see §7G) | ≈ −15 V (rail tied straight to W216.5) **or** 0 V (rail floating high-Z) | |
| P8 | Pin 2/3 cluster (front, either chip) | within a few mV of P7 (no DC drop across 61R9 into high-Z gates) | matches P7 | |

V_B (P2) and V_rail (P7) should track each other by the 0.704 ratio
above; if P2 ≈ 0.7 · P7 the rail-to-Node B network is intact, and
any remaining anomaly is in the regulator (§7G) or upstream of it
(5160 collector output, AGC drive if the topology turns out
closed-loop — but per §7D γ this whole back-feed is **withdrawn**;
see §7F supersession banner).

**Actuator location revised**: the actuator is **not** on the front
between the 1501 via and W216.5 (rows U1–U3 of the unpowered table
above will return *finite-but-not-active* values dominated by 61R9 +
regulator pass-element). The actuator is the **back-top compartment
bias regulator block** documented in §7G below; verify there before
chasing front-side parts.

> ✓ **DOUBLER LOCATION RESOLVED 2026-04-30** by recovered schematic
> (sheet 02/02 of A211 var.02, drawing 1035.8840.01; filed at
> [`rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg`](rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg)).
> The schematic FREQUENCY DOUBLER block lays out the full chain:
> X50 input → R49 / C57 / R59 input divider → **V50 (AT-42085-B
> NPN Si bipolar)** → C50 / L51 / L52 / R55 inter-stage match → **V60
> (AT-42085-B NPN Si bipolar)** → balanced drive → **V61 + V62 (HSMS-2800-B
> Schottky pair)** doubler → output match → L65 / C65 to BFG97 base.
> The §7F-bench-traced "420 cascade" of V50 + V60 is the **input
> stage that drives the V61 / V62 Schottky doubler** — candidate
> (a) is therefore confirmed in spirit (the cascade is the doubler
> drive), with the 2f generation happening explicitly in the V61 /
> V62 Schottky pair rather than in the BJT base-drive nonlinearity. The
> V50 / V60 / V61 / V62 cluster is the discrete frequency doubler
> the manual references — there is no separate hidden doubler
> elsewhere on the board. Candidates (b), (c), (d) are all
> falsified. The four hypotheses below are retained for FA
> traceability of how the question was originally framed.

**Doubler location — OPEN QUESTION (H)** *(historical, RESOLVED above)*: no component on this PCB
has been bench-pinned as a discrete frequency doubler. The
"V50/V60 doubler" of band-3 p.146 §7.4.1 / drawing 1035.8840.01
p.156 is a manual-side label only; the §7F bench trace above
identifies V50/V60 (per this section's own title) with the
**two-stage 420 cascade NPN bipolar amplifier**, which leaves the
doubling action itself unaccounted for. Live candidates:

| # | Hypothesis | Discriminating bench check |
|---|------------|----------------------------|
| (a) | The 420 cascade IS the doubler — second stage driven into 2nd-harmonic generation through the BJT base-drive nonlinearity. Consistent with §7F's section title equating "V50/V60" with "LO cascade amp". | SA on the RIGHT 420 collector output (low-cap probe, instrument running, `--a21-probe` 3 GHz CW): 220 MHz dominant over 110 MHz ⇒ confirmed. 110 MHz dominant ⇒ falsified, doubler is downstream. |
| (b) | A separate untraced doubler stage between the 420 cascade and the BFG97 collector summing node — discrete transistor, balanced diode pair, or SRD multiplier elsewhere on Side A or Side B not yet identified. | Visual sweep of A211 between the 420 cluster and the X21 brass pin for any untraced RF transistor / SOT-23 / SMD diode pair / wirewound choke pair (SRD signature). |
| (c) | The BFG97 itself is the doubler — driven into compression so the collector tank rings at 2f. See also the §7G "device-rating anomaly" bullet for the related power-amp re-interpretation of the 3866 / 5160 pair, which collapses (c) into a broader BFG97-pre-driver / 3866-5160-power-output reading. | SA at the BFG97 base vs. collector tab (chips fitted, instrument running, ≥ 30 dB pad if probing the collector): ratio of 110 to 220 MHz at base ≈ ratio at collector ⇒ BFG97 is linear (falsified). 220 dominant only at the collector ⇒ confirmed. |
| (d) | Doubling happens in the milled casing on the SRD comb generator — i.e. X21 actually carries 110 MHz at +26…+30 dBm and the 220 MHz spec in §7.4.1 is read at the SRD output through the connector. | Centre frequency on the X21 SA trace via the ≥ 30 dB / ≥ 1 W pad (Step 8): 110 MHz ⇒ (d) confirmed; 220 MHz ⇒ (a)/(b)/(c) survive. |

The §7F supersession banner (top of section) calls out the actuator
hypothesis as withdrawn but does not address the doubler-vs-amp
question; this bullet flags it as a separate open item to be cleared
before any third-rebuild escalation. Step 8's X21 SA sweep is the
single most informative reading — it discriminates (d) from (a/b/c)
in one trace, and the band-3 §7.4.1 spec table itself ("< 0 dBm @
103–117 MHz" fundamental leak vs. "+26…+30 dBm @ 206–234 MHz" main
output) only makes sense if the doubling has already happened
upstream of X21, which would falsify (d) by inspection.

#### V50 / V60 AT-42085 → AG303-86G substitution sketch *(repair option, only if §7F bench tracing finds V50 or V60 dead)*

Status on this unit: V50 / V60 are presumed alive — §7D D.5
cross-check still pending and the §7F bench trace below has not
falsified them. **Not in the rebuild bill of materials.** This
sketch is filed as a repair option for the case where §7F finds
either device dead (no fundamental on its collector SA capture, DC
bias absent at the collector node, or shorted on diode test).

**Original part:** Avago/HP **AT-42085-B** — NPN Si bipolar,
4-lead 85-mil plastic / SOT-86-class footprint, f_T 8 GHz, 8 V /
35 mA class-A bias, P1dB ≈ +20.5 dBm @ 1 GHz. Per the recovered
Var.02 schematic 2026-04-30, fitted in cascade as the V61 / V62
HSMS-2800 Schottky-doubler driver: V50 is the input stage off
the X50 ÷ R49 / C57 / R59 input divider; V60 follows after the
C50 / L51 / L52 / R55 inter-stage match and drives the V61 / V62
anti-parallel doubler pair through L65 / C65. Drive level
required at V60 output for the doubler is ~+12 to +16 dBm at
~100 MHz (the +26…+30 dBm at X21 is reached **after** the BFG97
pre-driver and the V3 / V4 push-pull power amp downstream).

**Stock substitute:** **Triquint AG303-86G** — Si Darlington
gain block, SOT-86 (pad-compatible with the 85-mil plastic /
SOT-86 footprint, no adapter), DC–6 GHz, gain 20.5 dB,
P1dB +14 dBm, 5 V / ≈ 50 mA single-supply current-driven via
output-pin bias-R. P1dB at 100 MHz is in the band of interest
for V60 doubler-driver duty, with no margin headroom (escalation
path below if the doubler under-drives).

**Pad / pinout mapping (SOT-86):**

```
+--------+---------------+------------------+----------------------+
| SOT-86 | Original use  | New use          | PCB rework needed?   |
| pad    | (AT-42085)    | (AG303-86G)      |                      |
+--------+---------------+------------------+----------------------+
| pin 1  | Base, DC bias | RF in (50 Ω,     | Insert a DC-block    |
|        | from upstream | DC-grounded      | cap in series if not |
|        | divider       | internally       | already present;     |
|        |               | through bias     | C57 may already      |
|        |               | feedback)        | serve.  Open R49 if  |
|        |               |                  | it carried DC bias   |
|        |               |                  | to the base node.    |
+--------+---------------+------------------+----------------------+
| pin 2  | Emitter pour  | GND              | Direct connection.   |
| pin 3  | (one of two)  |                  | If a small emitter   |
|        |               |                  | degen Re is fitted,  |
|        |               |                  | short it (or leave;  |
|        |               |                  | adds <1 Ω in GND     |
|        |               |                  | return — benign).    |
+--------+---------------+------------------+----------------------+
| pin 4  | Collector,    | RF out (50 Ω) +  | KEEP the existing    |
|        | through RFC   | Vcc              | RFC to +VR15-P;      |
|        | to +VR15-P    |                  | INSERT R_bias in     |
|        |               |                  | series with it (see  |
|        |               |                  | calculation below);  |
|        |               |                  | INSERT a DC-block    |
|        |               |                  | cap on the RF-out    |
|        |               |                  | trace to the next    |
|        |               |                  | stage (or verify     |
|        |               |                  | C50 / L51 already    |
|        |               |                  | DC-block).           |
+--------+---------------+------------------+----------------------+
```

**Bias-resistor sizing:**

```
+VR15-P = +15 V
V_pin4   = +5 V       (AG303-86G operating point)
I_d      = 50 mA      (target — comfortably below 60 mA limit)

R_bias = (15 V − 5 V) / 0.050 A  = 200 Ω

Power across R_bias = 10 V × 0.050 A = 0.5 W
  → use 0805 1 W or 1206 0.5 W metal-film  (NOT a chip thin-film
    that's only 0.125 W rated — it will scorch).

Decoupling: keep the existing C-bypass at the collector-RFC tie
to +VR15-P; add a 100 nF X7R + 10 µF tantalum at the new R_bias
junction to +VR15-P if board real estate allows.
```

**Pre-power checks (after rework, before connecting +VR15-P):**

```
+---+--------------------------------------------------------+
| # | Check                                                  |
+---+--------------------------------------------------------+
| 1 | Pin 1 of new MMIC is NOT shorted to a DC-bias node     |
|   |   (old base-bias divider R49 must be lifted on V50;    |
|   |   inter-stage match DC path must be broken on V60)     |
| 2 | Pin 4 sees +5 V (DMM measure) on power-up before any   |
|   |   RF drive — if reads <4 V or >6 V, R_bias is wrong    |
|   |   or MMIC pin 4 is shorted to GND.                     |
| 3 | Existing collector RFC DCR must be << R_bias (sub-Ω)   |
|   |   so it doesn't add to the bias drop.  L52 datasheet   |
|   |   value for the original choke — verify with DMM.      |
| 4 | DC-block cap on RF-out trace must be present and good  |
|   |   (Vcc on pin 4 must NOT propagate to the inter-stage  |
|   |   network or it will bias V60's input node).           |
+---+--------------------------------------------------------+
```

**Post-power verification (RF):**

```
+---+--------------------------------------------------------+
| # | Bench check after replace and power-up                 |
+---+--------------------------------------------------------+
| 1 | DC: pin 4 = 5 V ±0.5 V; rail current draw +50 mA per   |
|   |   replaced device.  Two devices = +100 mA on +VR15-P.  |
| 2 | RF: drive X50 with 100 MHz at +5 dBm (bench gen).      |
|   |   SA on V50 collector (low-cap probe): expect ~+18 to  |
|   |   +20 dBm fundamental (gain ~14 dB minus 1 dB compr).  |
| 3 | RF: SA on V60 collector: expect ~+12 to +14 dBm        |
|   |   fundamental (V60 driving the V61/V62 doubler is the  |
|   |   compressed stage — drives the doubler near P1dB).    |
| 4 | RF: SA at X21 with ≥30 dB / ≥1 W pad: expect 200 MHz   |
|   |   dominant, +26 to +30 dBm — nominal §7.4.1 spec.      |
| 5 | If 100 MHz dominates at X21: V61/V62 doubler not       |
|   |   driven hard enough.  Reduce R_bias (raise Id toward  |
|   |   60 mA) and re-check; or escalate per the path below. |
+---+--------------------------------------------------------+
```

**Escalation path if AG303-86G under-drives the doubler** (200 MHz
at X21 SA shows 100 MHz dominant after R_bias trim to 60 mA Id):

1. **PGA-103+ on a SOT-89 → SOT-86 adapter PCB** — same
   Vcc-fed bias scheme, R_bias ≈ (15 − 5) / 0.080 = 125 Ω 1 W;
   +22.5 dBm P1dB at 1 GHz, ~+24 dBm at 100 MHz. Best linearity
   in stock.
2. **GALI-84+ same adapter** — R_bias ≈ (15 − 4.5) / 0.075 ≈
   140 Ω 1 W; +21.7 dBm P1dB at 1 GHz.
3. **SPF5189Z same adapter** — R_bias ≈ (15 − 5) / 0.090 ≈
   110 Ω 1.5 W; exact P1dB match to original AT-42085.

The adapter is a 0.1″ × 0.1″ copper-clad scrap with the SOT-86
pad pattern milled on one side and the SOT-89 part soldered on
the other; standard rework technique for this kind of vintage
RF substitution.

**Related repair option (V61 / V62 HSMS-2800 doubler-pair
substitution):** if a V60 collector-network failure took out the
V61 / V62 HSMS-2800 anti-parallel doubler pair downstream (rare —
the doubler diodes are protected by the L65 / C65 inter-stage
match and the V60 collector-load RFC, but a V60 collector short
to +VR15-P could drive the doubler pair past its VBR), see the
**§7E "Other A0 candidates" paragraph** for the HSMS-2800
substitution table. **In-stock pick for V61 / V62 specifically =
BAT17-04** (Infineon SOT-323 dual HF Schottky, low-barrier,
Cj ≈ 0.7 pF, low-cap advantage at 200 MHz); same SOT-323 →
SOT-23 mechanical bodge as the documented HSMS-286C/K. The §7E
table also covers the DIAGSAMP single-A0 rectifier role (where
BAT17-04's 4 V VBR is inadequate and 1N5711WS-7-F's 70 V VBR is
the on-hand pick instead).




### Step 7G — Back-face top compartment: LP365M quad-comparator block *(Side A back face, behind the X50 cascade amp)*

Direct opposite of the X50 / cascade-amp area on the front, the back
face top-edge compartment carries a small-signal sub-block built
around an **LP365M micropower programmable quad voltage comparator**
plus a SOT-23 trio. The earlier "JFET op-amp / negative-rail
regulator" reading of this compartment is **withdrawn** under a
direct top-mark re-read (`[NN logo] M32AB / LP365M`) cross-checked
against the National Semiconductor LP365 datasheet (NS package
**M16A** = SO-16 wide-body); the chip is a four-channel comparator
with open-collector NPN outputs sharing a common-emitter pin V_E
and a programming-current pin ISET, **not** a single op-amp.
Functional role on this board is bench-confirmed (G3 + G4–G7 +
G8 + G2 + G-PUP + partial G-REF below) as a **four-channel non-
latching monitor with a single wired-OR fault flag, fixed-bias
ISET, and a Zener-derived shared threshold reference** — V_E =
GND, all four OUT pins commoned onto a single wired-OR node
(pulled up to +15 V through 15 kΩ) driving a SOT-23 actuator
('A2') directly, all four input pins commoned across mixed
polarity onto a shared reference / threshold net (Zener-divided
from +15 V), and ISET (pin 1) bias-programmed by a single 274 kΩ
resistor to +15 V. The block runs continuously: any channel trip
pulls the wired-OR low for as long as the sense node is out-of-
window and releases automatically when the sense recovers — there
is **no self-disabling latch**, and the previous "OUT → ISET
feedback" framing is **withdrawn** (the 1502 / 2743 resistors that
read as "in series between OUT and ISET" on a continuity walk are
in fact two independent +15 V pull-ups sharing the V+ rail at
their upper end, not a feedback divider). Per-channel sense-net
assignment (which on-board node each of pins 5 / 7 / 10 / 11
monitors), the Zener voltage Vz, and the destinations of the two
untraced vias on the reference network are TBD pending the G-IN /
G-Z / G-REFvia rows below.

**Bench-confirmed contents (C)**:

- **LP365M** (`[NN logo] M32AB / LP365M`) — National Semiconductor
  micropower programmable quad voltage comparator, SO-16 wide-body
  (NS package M16A). Four open-collector NPN channels share a
  common-emitter pin **V_E** (pin 16) and a programming-current pin
  **ISET** (pin 1) that sets the per-channel bias via one external
  resistor to a rail. Pinout from the NS datasheet connection
  diagram (saved as `lp365m.png`):

  | Pin | Function | Pin | Function |
  |-----|----------|-----|----------|
  | 1   | ISET     | 16  | V_E (common emitter) |
  | 2   | OUT2     | 15  | OUT3     |
  | 3   | OUT1     | 14  | OUT4     |
  | 4   | V+       | 13  | V−       |
  | 5   | −IN1     | 12  | +IN4     |
  | 6   | +IN1     | 11  | −IN4     |
  | 7   | −IN2     | 10  | +IN3     |
  | 8   | +IN2     | 9   | −IN3     |

  Bench-confirmed on this unit: **pin 4 = +15 V (✓)**, **pin 13 =
  −15 V (✓)**, **pin 16 (V_E) = GND (✓)**, **pins 2 / 3 / 14 / 15
  (OUT2 / OUT1 / OUT3 / OUT4) all commoned (✓)** onto a single
  wired-OR node, and **pins 6 / 8 / 9 / 12 (+IN1 / +IN2 / −IN3 /
  +IN4) all commoned (✓)** onto a single shared-reference / shared-
  threshold node (mixed polarity: three non-inverting inputs and
  one inverting input share the same net, which is the signature
  of a multi-rail monitor referencing one common threshold against
  channel-specific sense pins on 5 / 7 / 10 / 11). Sense pins 5
  (−IN1), 7 (−IN2), 10 (+IN3), 11 (−IN4) remain to be traced
  individually (G-IN row of the pending work below).
- **ISET (pin 1) → 274 kΩ → +15 V (✓)** — pin 1 is bias-programmed
  by a single resistor `2743` (274 kΩ) to V+ (= +15 V). With LP365M
  internal V_ISET ≈ 1 V_BE below V+ (≈ +14.3 V), the programming
  current is I_SET ≈ 0.7 V / 274 kΩ ≈ 2.5 µA, which sets the per-
  channel quiescent bias squarely in the LP365M's micropower band
  (the part is rated for ~1 µA–~100 µA programmable per-channel
  bias via this single resistor). ISET is therefore **fixed
  bias** — independent of the wired-OR state — and the block
  operates as a non-latching continuous monitor.
- **Wired-OR pull-up (✓)** — pin 3 (OUT1, and via the OUT-pin
  commoning above also pins 2 / 14 / 15) is pulled up to +15 V
  through `1502` (15 kΩ). No-fault wired-OR voltage = +15 V; on
  any channel trip the OC NPN saturates and pulls the wired-OR to
  V_E = GND, sinking I = 15 V / 15 kΩ = 1 mA (well within the
  LP365M OC NPN ratings). The wired-OR drives SOT-23 'A2' base
  directly and **non-latchingly** — the wired-OR releases (returns
  to +15 V) automatically when the tripped sense node returns to
  in-window. The earlier "1502 + 2743 in series as an OUT-to-ISET
  positive-feedback / self-disable chain" reading was an artifact
  of an ohm-meter continuity walk from pin 3 through the 15 kΩ +
  274 kΩ to pin 1 reading "continuous" because the two resistors
  share the +15 V copper at their upper end; the actual topology
  is two independent +15 V pull-ups, not a feedback chain. The
  self-disabling-latch reading is **withdrawn**.
- **Shared-reference / threshold-network (G-REF, partial ✓)** —
  the commoned input net (LP365M pins 6 / 8 / 9 / 12 = VREF) is
  driven from a Zener-derived reference rail. Bench-traced
  topology:
  ```
                                +15 V
                                  │
                                1821 (1.82 kΩ)
                                  │
              ┌───── via ─────── node Y ────────┐
              │     (off-                       │
              │      compt)                     │
              │                  │              │
              │              Diode (Z)          │
              │              cathode at Y       │
              │              anode at GND       │
              │                  │              │
              │              C (bypass)         │
              │              GND                │
              │                                 │
              │                                5622 (56.2 kΩ)
              │                                 │
              │                                 ▼
              ▼                            VREF (LP365M
        1001 (1 kΩ) ── via ── (off-compt)   pins 6/8/9/12)
                                                 │
                                              1003 (100 kΩ)
                                                 │
                                                GND
  ```
  Y is Zener-clamped to V_z (small-signal SOT-23 / leadless Zener,
  Vz TBD by top-mark / Vf — leading candidates 5V1 or 6V2 based on
  the Zener bias current I_Z = (15 − Vz)/1.82 kΩ landing in the
  4–5 mA textbook test-current range). The divider `5622 / 1003`
  scales Y to **VREF = Vz × 100 k / (100 k + 56.2 k) = Vz × 0.6406**
  (≈ 3.27 V at Vz = 5.1 V; ≈ 3.97 V at Vz = 6.2 V). Two untraced
  vias remain open: (i) **node Y itself** has a via leaving the
  compartment — most likely off-compartment distribution of the
  Vz reference to another sub-block on A21; (ii) the **1 kΩ
  (`1001`) on Y** terminates at a via — destination TBD, no longer
  constrained to be ISET or the wired-OR (both of which are now
  bench-resolved as +15 V pull-ups). See pending-work G-Z and
  G-REFvia rows below.
- **At least three SOT-23 transistors**, top-mark codes `4F`, `T1`,
  `2F` — leading-candidate decodes against current SMD-code refs
  (Marsen-Wittenburg / Turuta / SMD-codes.com), filtered against
  the §7G DC-monitor context (no RF / no microwave path, ±15 V
  rails, LP365M comparator block):

  | Code | Leading candidate | Polarity | Rationale | Secondary candidates |
  |------|-------------------|----------|-----------|----------------------|
  | `4F` | **BC860B** (Zetex PNP GP, 50 V, 100 mA, B=220–475, >300 MHz) | PNP | Small-signal high-β PNP; Zetex was a routine 1990s European-instrumentation supplier (R&S / HP / Tek). Fits 'A2' actuator, level-shift stage, or follower equally well. | 2SC4444 (Panasonic NPN VHF/IF, 500 MHz) **ruled out** — RF/IF part, doesn't fit DC monitor block. |
  | `2F` | **2N2907A family** (PNP GP, 60 V, 500–600 mA, B=75–300) — top-mark shared by ~10 manufacturer variants (MMBT2907A / FMMT2907A / KST2907A / MBT2907A / MBTA2907A / SBT2907A / SMBT2907A / TMPT2907A / YTS2907A / 2N2907AS) | PNP | The canonical JEDEC switching PNP and the textbook fault-flag actuator part — strongly favoured for the 'A2' role. Specific manufacturer not discriminable from top-mark alone (all read `2F`); electrically interchangeable across the family. | BC850B (Continental Device India NPN GP, 50 V, 100 mA, B=200–450) — secondary if bench polarity check shows NPN. FT510Fa LDO (3.0 V) **ruled out** — three-terminal regulator IC pin-pattern would not show transistor-junction signatures, and 3.0 V output doesn't match any node in the LP365M reference network. |
  | `T1` | **BCX17** (SGS-Thomson PNP AF-Drv, 50 V, 500 mA, B=100–600, P_TOT 300 mW) | PNP | Driver-grade PNP with high β; SGS-Thomson was a routine European supplier. Fits a load-driving stage downstream of 'A2' or a separate higher-current actuator. | BSS63 (ON Semi PNP GP, 110 V, 100 mA) — secondary; high-V rating is overkill for ±15 V context but not contraindicated. AP8822C-11 (1.1 V detector), ELM7641HCB (4.1 V), ELM9751CBB (5.1 V), R3130N44HA (4.4 V) **all ruled out for the Y-clamp role** by the µA-level supply-current signature of supervisor ICs (incompatible with the ≈ 5 mA bias current expected at node Y from the 1.82 kΩ source). BTC5181WC3 (NPN HF, 12 GHz) **ruled out** — microwave part. HSMS-2862 (dual Schottky, Vf < 0.6 V) **ruled out for the Y-clamp role** — Vf doesn't reach the 5–6 V Y-node clamp. |

  **All three leading candidates are PNP**, suggesting the SOT-23
  trio is a PNP triplet. Under that reading **none of the three
  SOT-23s is the Zener at node Y** of the reference network — the
  G-SOT bullet's "or the Zener element of the reference network
  above (if its package is SOT-23 rather than leadless)" caveat is
  superseded, and the G-Z probe scope narrows to leadless small-
  signal Zener packages (SOD-323 / SOD-523 / MELF cylindrical) on
  the §7G PCB rather than the SOT-23 trio.

  One of the three (provisionally designated **'A2'**) is bench-
  confirmed as the **single downstream actuator** for the LP365M
  wired-OR fault flag: its base (SOT-23 pin 1, EIA/JEDEC) is tied
  directly to the OUT wired-OR node (which sits at +15 V no-fault,
  GND on trip). Under the PNP-triplet reading, 'A2' acts as a
  high-side switch — base low (trip) forward-biases the B-E
  junction (assuming emitter on +15 V), turning the PNP ON and
  pulling its collector load toward +15 V; base high (no fault)
  reverse-biases B-E and the PNP is OFF. Roles for the remaining
  two SOT-23s in the trio are TBD pending bench polarity check +
  per-pin trace; candidates are a level-shift / inversion stage
  in series with 'A2', a separate bias / reference helper, or
  parts that share the compartment without interacting with the
  LP365M.
- **Leftmost SOT-23, pin 3 → W216.5 ≈ 1.9 Ω (C)** — raw observation
  unchanged. Under standard EIA/JEDEC SOT-23 pinout (pin 1 = B,
  pin 2 = E, pin 3 = C), pin 3 is the **collector**, so this is a
  collector tied near −15 V through a small load R. Under the PNP-
  triplet reading above (all three SOT-23s most likely PNP), this
  is a **PNP with collector returned to −15 V via a small (≈ 1.9 Ω)
  series element**. Sanity check: a PNP biased ON in steady-state
  with emitter on +15 V, collector through 1.9 Ω to −15 V would
  source ≈ 30 V / 1.9 Ω = 16 A, which is impossible for a small-
  signal SOT-23 — so the PNP must be **normally OFF** in the bench
  measurement (no base drive), and the 1.9 Ω is then the in-circuit
  ohm reading through a board-level series conductor (small wire-
  wound, 0 Ω jumper, or short trace to the −V pour) bonding the
  collector to −15 V independent of the silicon. Plausible
  topologies under PNP / normally-OFF: (a‴) a **PNP switch /
  inverter** whose collector is normally pulled toward −15 V
  through the ballast and lifted only when the base goes low; (b)
  an unrelated −15 V pour bond on a SOT-23 that doesn't interact
  with the LP365M wired-OR. The earlier (a′) NPN current-sink and
  (a″) PNP common-collector / emitter-follower readings remain
  viable only if the bench polarity check on this specific SOT-23
  contradicts the PNP-triplet leading reading. Re-probe under
  power: if the collector voltage swings between ≈ −15 V (OFF) and
  near 0 V or above (ON) as the wired-OR / 'A2' actuates, the
  switch-with-rail-ballast reading is confirmed; if the collector
  sits at a stable mid-rail value, an emitter-follower reading is
  more likely. The previous "PNP common-emitter / pass-transistor
  with emitter on the −15 V pour" reading required pin 3 = emitter
  (JEITA SC-59) and remains **withdrawn**.
- A precision SMD R cluster around the LP365M — under the
  comparator reading these are most plausibly **threshold-setting
  dividers** on the (+) and (−) inputs of one or more channels,
  plus the ISET programming resistor and any open-collector pull-
  ups; **not** an op-amp gain / feedback network.
- An isolated Schottky-style detector under X75 in the *middle*
  compartment of the same back face — separate sub-block, not part
  of the LP365M block, likely the X75 envelope detector feeding the
  ALC error path; track separately if encountered.
- An **MMIC marked `A08`** in the same X75 middle compartment, in
  the **identical 4-lead micro-X / SOT-86 package** as the §7F
  `420` cascade-amp chips. The recovered schematic identifies V75
  as **MAR-8** (Mini-Circuits); the `A08` top-mark is the Avantek
  house code shared by the electrically equivalent MSA-0885 (the
  qsl.net `on7pc` MMIC marking-cross-reference table cross-lists
  `MAR-8 ∥ MSA0885 ∥ A08 ∥ Blue`). The bench-inferred MSA-0885
  identity quoted in earlier revisions of this bullet was based on
  the Avantek top-mark decode alone; the Step 10a VNA S21
  measurement (2026-05-05, passband +31.4 … +31.55 dB at 10–80 MHz)
  matches the **MAR-8 datasheet figure (~32 dB at 100 MHz)** and
  falsifies the MSA-0885 figure (~22.5 dB). See
  [smp_history.md H-2026-05-05-a08-msa0885-superseded](#h-2026-05-05-a08-msa0885-superseded)
  for the original MSA-0885 identification narrative.
  **Specs (MAR-8):** DC – 1 GHz BW, **~32 dB gain @ 100 MHz**,
  ~+12.5 dBm P1dB, ~3.5 dB NF, unconditionally stable;
  **canonical pinout:** pin 1 = RF-in, pin 2/3 = GND, pin 4 = RF-
  out + Vcc (single-supply via series bias R from rail). **The
  pin-4-DC test that ruled out an MSA Darlington for the 420
  chips (pin 4 solder-blob-grounded would short Vcc to GND) goes
  the other way for this part:** if A08 pin 4 sits on a small SMD
  bias R pulled up to one of the analog rails (likely +15 V via
  ~200–470 Ω, ≈ 7–8 V across the device at ~36 mA), the MAR-8
  ID is fully consistent. **Three role hypotheses** in this X75
  compartment, distinguished by where pin 1 (RF-in) and pin 4
  (RF-out) trace:

  | # | Role hypothesis for A08 | Distinguishing test |
  |---|---|---|
  | (i) | Active IF post-amplifier on the X70 → X75 path (the §7.4.2 / §7.1.5 narrative calls this passive impedance transformer + L72 LP filter; an active stage here is a doc gap). Adds ~20 dB to bring casing-IF up to the +15 dBm headroom at X75 (−5 … +15 dBm spec). | A08 pin 1 sits on the impedance-transformer secondary; pin 4 → DC-block → toward L72 / X75. Passive S21 X70 → X75 (instrument off, A08 unpowered) shows ~−20 dB drop where the active +20 dB is missing. |
  | (ii) | Pre-detector buffer driving the X75-region envelope detector (the Schottky detector flagged in the bullet directly above), feeding the IF-level ALC error path. Loads the X70 → X75 RF line lightly via a high-impedance tap so the detector can sense without dragging the through-path. | A08 pin 1 fed via small coupling cap from a high-Z tap on the X70 / X75 RF node; pin 4 → into the Schottky detector node, **not** back into the main RF path. Cap+R tap visible on the back-face photo around the A08 footprint. |
  | (iii) | Output buffer for X75 only — isolation between A211 IF chain and the A10 PLL phase-detector cable load; modest net gain ≤ 10 dB after a series pad. | A08 pin 1 on the X75-driving node, pin 4 through DC block direct to X75 brass pin; no Schottky detector tap on either side of the device. |

  **Bench finding 2026-04-29 (✓ DC):** A08 pin 4 measured **195 Ω
  to +15 V** (DMM ohms, instrument off). The 195 Ω is the
  **parallel combination of two 392 Ω 1% resistors** (R_eff =
  196 Ω) on the back-face PCB; the +15 V trace is bench-traced
  end-to-end from **W216.1 → 2 × 392 Ω in parallel → A08 pin 4**,
  un-gated by any supervisor / V85 / V89 cut-off switch. Computes
  to V across bias R = 15 − 7.8 = 7.2 V → **I_d ≈ 36.9 mA**,
  **V_d = 7.8 V** across the MMIC — an **exact match to the
  MAR-8 datasheet operating point** (`I_d = 36 mA, V_d =
  7.8 V` typ). Power dissipation **splits to ~133 mW per
  resistor** (vs. ~266 mW in a single-R variant), a thermal-
  margin design choice consistent with running the MAR-8 at
  full datasheet I_d. The MMIC itself dissipates ~288 mW (well
  below the 500 mW absolute-max). **Locks the part ID** (only
  MAR-8 family operates at that exact bias point from
  +15 V; INA / MGA / ATF families have different operating
  points), **the bias topology** (single +15 V supply, 2 × 392 Ω
  parallel pair on pin 4, no separate RF choke), and the **+15 V
  trace integrity** from W216.1 to the MMIC.

  **Bench finding 2026-04-29 (✓ RF-trace):** A08 pin 1 (RF-in) is
  **fed from X70 through an LC filter network and a DC-block cap**.
  No high-Z sniff tap, no separate Schottky-detector branch on
  the input side. The LC network is almost certainly the **L72 LP
  filter** referenced in §7.4.2 (the one that gives the 105–110
  MHz notch in the IF passband spec). Pin 4 then drives the X75
  brass pin (presumed via DC-block cap, not yet bench-traced
  but topologically forced — pin 4 carries DC bias on the +15 V
  side of the bias R, X75 must be DC-blocked from that node).

  **Role — RESOLVED, hypothesis (i) CONFIRMED:** A08 is the
  **active IF post-amp on the X70 → X75 path**. Roles (ii) sniff
  buffer and (iii) output-only buffer are **falsified** — (ii)
  requires a high-Z tap on pin 1, which the bench trace does not
  show; (iii) requires pin 1 on the X75-side, but pin 1 is on
  the X70-side through the LP filter. Net topology of the on-PCB
  IF stage:

  ```
  X70 (IF in from in-casing A212, LP-filtered) --> L72 LP filter
       (LC network, 105-110 MHz notch per 7.4.2) --> DC-block cap
       --> A08 pin 1 (MAR-8 RF in, ~+15 dBm typ at the casing
       output of A212) --> A08 internal Darlington gain stage,
       Id 36.9 mA, Vd 7.8 V, ~+32 dB at 100 MHz, P1dB +12.5 dBm
       --> A08 pin 4 (RF out + Vcc) --> 195 Ohm bias R to +15 V
       (RF blocking + DC bias, dual purpose) + DC-block cap on
       the RF path --> X75 brass pin --> A10 PLL phase-detector
       (W210, -5 ... +15 dBm spec at X75)
  ```

  **Doc-gap implications — confirmed under (i):**

  - The §7G "isolated Schottky-style detector under X75 in the
    middle compartment" bullet directly above this one is now
    **a separate sub-block** that is **not** fed by the A08 (the
    A08 input is the through-path, not a sniff tap). The X75
    Schottky detector's source remains TBD — most plausibly a
    high-Z cap-tap somewhere on the X75-side of A08 (pin 4
    output node) rather than on the X70-side.
  - The A21-connector-interface paragraph at the top of this
    file currently describes the X70 → X75 on-PCB path as
    passive only; **revise to: "X70 → L72 LP filter → A08
    MAR-8 IF post-amp (~+32 dB at 100 MHz) → X75"**.
    Tracked as a pending doc edit; the §7.1.5 narrative on
    p.145 needs cross-checking for whether R&S documents this
    stage as part of "the impedance transformer" or omits it.
  - Step 9 fail-localization list (X75 dead with X21 at spec)
    must include **A08 MAR-8 + its 195 Ω bias R + its
    input/output DC-block caps + L72 LP filter** alongside the
    in-casing A212 IF amp. See Step 9 doc-gap note added below.
  - Step 10 config 2 ("on-PCB IF path only, passive, instrument
    off") is **broken as written** — with the instrument off,
    A08 is unpowered, the MMIC's collector-emitter path
    presents OL to the IF, and X70 → X75 transmission collapses.
    Config 2 must be re-described as "instrument **on** so A08
    is biased, X50 / X211 disabled so no LO/RF reaches the
    mixer". See Step 10 doc-gap note added below.
  - The §7.4.2 +27 dB IF-amp passband spec attribution to "the
    A212 IF amp" is now questionable — with A08 contributing
    ~32 dB at 100 MHz, the +27 dB is **less than A08 alone**
    — so the combined A212 + A08 chain gain must account for
    A212's own modest gain / insertion loss plus L72 + DC-block
    losses ahead of A08. Closing the attribution requires
    reading p.145 §7.1.5 / §7.1.6 and p.146 §7.4.2 for the
    gain block diagram.

  **Sourcing if ever needed:** like-for-like replacement is
  **Mini-Circuits MAR-8A+** (HBT, same micro-X pinout, **same
  recommended bias point of 36 mA / 7.8 V — drops in on the
  existing 195 Ω bias R without modification**, DC – 1 GHz,
  ~31 dB gain at 100 MHz — essentially the same gain as the
  original MAR-8); **MAR-6+** (~20 dB at 100 MHz) is the
  lower-gain alternative if the ~32 dB passband gain is
  undesirable in a future design context.

**Topology — CONFIRMED R1 (non-latching multi-channel monitor +
wired-OR fault flag, fixed ISET bias, Zener-derived shared
threshold)**: bench evidence has moved from "identity + supplies
only" to a complete architectural fingerprint match on R1, with
the corrected pull-up topology (1502 / 2743 are independent +15 V
pull-ups, not a feedback chain). All five R1 fingerprints are
present on this unit:

| Fingerprint | Bench finding | R1 expectation | Match |
|---|---|---|---|
| V_E (pin 16) | GND ✓ | GND or single rail (sink reference for OC outputs) | ✓ |
| OUT pins (2, 3, 14, 15) | All four commoned onto a single node ✓ | All commoned (wired-OR) onto a fault-flag net | ✓ |
| Wired-OR pull-up | 15 kΩ (`1502`) from pin 3 to +15 V ✓ | Single resistor pull-up to V+ (no-fault rail = V+) | ✓ |
| ISET bias (pin 1) | 274 kΩ (`2743`) to +15 V ✓ → I_SET ≈ 2.5 µA, micropower band | Single programming resistor to a rail (V+ or V−) | ✓ |
| Input pins (6, 8, 9, 12) | All four commoned across mixed polarity (+IN1, +IN2, −IN3, +IN4) onto VREF = Vz × 0.6406 ✓ | One reference / threshold shared across channels, sense pins on the complementary inputs | ✓ |
| OUT destination | Wired-OR node → SOT-23 'A2' base (pin 1, JEDEC) directly ✓ | One downstream actuator following the fault flag | ✓ |

Both alternative readings carried in the previous revision remain
eliminated:

- **R2 (hysteretic switching pass-element controller per channel)
  is eliminated.** R2 requires per-channel OUTs driving per-
  channel pass elements; the bench-confirmed full commoning of all
  four OUT pins onto a single wired-OR node is incompatible with
  per-channel actuation. The R2 reading is withdrawn.
- **R3 (window comparator pair(s))** is **eliminated.** A window
  pair shares one sense node across exactly two channels' (+) /
  (−) inputs via paired threshold dividers; the bench-confirmed
  four-way input commoning across mixed polarity (three (+) inputs
  and one (−) input on the same net) is incompatible with the
  paired-divider fingerprint. The R3 reading is withdrawn.

The §7F negative rail is therefore **not** servo-regulated by this
block — it is either passively derived from −15 V via the 61R9 /
divider network or generated elsewhere on the board, with the
LP365M's role being **non-latching multi-channel monitoring with
a single wired-OR fault flag** routed through SOT-23 'A2' as the
downstream actuator. ISET is fixed-bias (274 kΩ to +15 V); the
wired-OR is a clean +15 V-pulled-up node; and the trip / release
behaviour follows the sense node directly with no hysteresis or
latch built into the LP365M block itself (any hysteresis or
inrush-blanking, if needed, would be implemented downstream of
SOT-23 'A2').

**Working fault-behavior model** *(non-latching, corrected)*: in
normal operation all four sense channels read in-window against
the shared reference VREF (= Vz × 0.6406, ≈ 3.3 V or ≈ 4.0 V on
the leading Vz candidates), all four OC outputs are off (high-Z),
the wired-OR sits at +15 V through the 15 kΩ pull-up, and SOT-23
'A2' base sees +15 V (driving 'A2' to whatever steady state
corresponds to "no fault" downstream — polarity TBD per G-SOT
top-mark decode). On any single channel's sense node going out-
of-window, that channel's OC NPN turns on, the wired-OR is pulled
to V_E = GND through the 15 kΩ at I_sink ≈ 1 mA, and 'A2' base is
driven to ≈ 0 V. The remaining three channels continue to operate
on their fixed ISET bias (274 kΩ → +15 V is independent of the
wired-OR state), so multiple simultaneous sense excursions all
register on the same wired-OR but **do not collapse the block**
— the previous "self-disabling latch" model is withdrawn. Trip
**releases automatically** when the sense node returns to in-
window: the OC NPN turns off, the 15 kΩ restores the wired-OR to
+15 V, and 'A2' returns to its "no fault" state. Multi-rail
power-supply / under-voltage / over-current monitor front-end with
a single wired-OR fault flag and downstream actuator — the
classic LP365M application niche. The mixed-polarity input
commoning (one shared threshold, four sense nodes — three sensed-
against-falling on the (+IN1 / +IN2 / +IN4) channels and one
sensed-against-rising on the (−IN3) channel) jointly implies the
protected envelope is "rail-N is too low" for three of the
channels and "rail-M is too high" for the fourth. Identifying the
four sense nets (G-IN row of the pending work below) finalises
which rails are being monitored against which polarity.

**Residual ambiguity within R1** that the next bench probes resolve:

1. **Shared-reference vs shared-sense — RESOLVED (shared
   reference).** The commoned input net (pins 6, 8, 9, 12) is
   bench-confirmed (partial G-REF) as a **Zener-derived shared
   threshold reference** VREF = Vz × 0.6406, fed from the
   1.82 kΩ / Zener / 56.2 kΩ / 100 kΩ network sketched above.
   The four sense pins (5, 7, 10, 11) are therefore four
   independent monitored nodes, all compared against the same
   threshold. The "shared sense node + four independent threshold
   taps" alternative is withdrawn.
2. Which of the three SOT-23s (`4F`, `T1`, `2F`) is the 'A2'
   actuator wired to the OUT node, and what the other two SOT-23s
   do — are they a level-shift / inversion stage in series with
   'A2', the Zener element of the reference network above (if its
   package turns out to be SOT-23 rather than leadless), or
   unrelated parts sharing the compartment? Distinguished by per-
   pin trace of all three SOT-23s plus top-mark decode (G-SOT row
   below).
3. The exact **Zener voltage Vz** of the reference clamp at node Y
   — sets the absolute threshold VREF = Vz × 0.6406 the four sense
   nodes are compared against. Leading candidates 5V1 (VREF ≈
   3.27 V) and 6V2 (VREF ≈ 3.97 V) on the I_Z ≈ 4–5 mA bias-current
   argument; final value to be locked down by top-mark decode or
   in-circuit Vz measurement (G-Z row below).
4. The destinations of the **two untraced vias** on the reference
   network — the via leaving node Y itself (likely off-compartment
   distribution of Vz to another sub-block) and the via terminating
   the 1 kΩ (`1001`) stub from Y. Both are now decoupled from the
   ISET / wired-OR question (which is bench-resolved); the residual
   significance is whether Vz is shared with another comparator /
   reference user elsewhere on A21 (G-REFvia row below).

**Loop architecture — relationship to §1 / §7C / §7D**: the X21 LO
level on A21 is **autonomous** — no external level command enters
via W216. **VARSAMP (W216.9)** is the **model-ID readout** per §1
(0.9–1.1 V expected, 0.963 V on this unit), *not* a setpoint, and
**DIAGSAMP (W216.10)** is a **passive envelope-rectifier readout**
routed out to the CPU for monitoring only — bench-traced (per §7D
revised topology) as **A0 (anode on the X21 RF tap, cathode to GND)
+ 10 kΩ series isolation R `1002` + shunt-cap to GND**, with the
filtered DC node going straight to W216.10. There is **no AGC op-amp
on this path**. The coexistence of the §7D chip-level reading 5160
pin 6 = +14.46 V with the §1 connector-level reading DIAGSAMP =
0.262 V is therefore explained by a **shared upstream root cause**,
not by a broken tap-out: the 3866 / 5160 AGC failure collapses LO at
X21, which leaves A0 with no envelope to rectify, which delivers
≈ 0 V through the otherwise-intact passive 1002 + cap network to
W216.10.

The LP365M's monitored set-points (per-channel threshold dividers on
the (+) and (−) inputs, G4–G7 below) are sourced from **on-board
fixed references** — band-gap / Zener / R-divider taps off ±15 V
wholly internal to the A21 board — not from anything on W216. The
§7G **LP365M monitor block**, the §7D **3866 / 5160 AGC
loop** (X21 RF tap sensed via cap + L1-Cshunt-L2 LPF onto the
commoned bases — pins 2/3 — of the MRF3866 NPN + MRF5160 PNP
complementary RF pair, with the joined collectors — pins 6/7 — of
each chip summed through 100 Ω + LC onto the **collector tab of a
BFG97 NPN RF transistor** that buffers / level-controls the LO chain
by collector-bias modulation; full BFG97 bias-network walk-through
TBD per §7G pending work below), and the §7D / §1 **DIAGSAMP
rectifier** (A0 + 1002 + shunt cap) are **three independent sub-
blocks** sharing only the ±15 V supplies and the X21 RF tap node. A
successful §7E rebuild restores the AGC loop, which restores LO at
X21, which
**automatically** restores DIAGSAMP through the passive A0/1002/cap
network — no DIAGSAMP-specific repair needed. The rebuild does **not**
directly verify §7G LP365M monitor operation — that's a separate
sub-block confirmed by the §7F P-sequence + §7G G-sequence.

**Bench checks (to be run after the §7E rebuild and §7F P-sequence)**:

The G-sequence is a **per-channel quad-comparator trace**: with R1
now confirmed (V_E = GND, OUTs commoned, inputs commoned, ISET
fixed-bias to +15 V via 274 kΩ, wired-OR pulled to +15 V via
15 kΩ, OUT → SOT-23 'A2' base directly, shared-reference net
Zener-derived from the 1.82 kΩ / Zener / 56.2 kΩ / 100 kΩ
network), the remaining G-rows lock down the four sense nets,
the Zener voltage Vz, the off-compartment via destinations, and
the SOT-23 trio top-marks.

| # | Probe | Expected (R1 reading: multi-channel monitor) | Notes |
|---|-------|----------------------------------------------|-------|
| G1 | LP365M V+ (pin 4) and V− (pin 13), DMM DC | +15 V on pin 4, −15 V on pin 13, each within ±5 % | confirms supplies. Already bench-confirmed on this unit (✓ / ✓). |
| G2 | LP365M ISET (pin 1), DMM DC + DMM ohm to ±15 V / wired-OR node (unpowered) | single 274 kΩ (`2743`) to +15 V (V+), independent of the wired-OR rail; DC voltage on pin 1 ≈ V+ − V_BE ≈ +14.3 V; I_SET ≈ 2.5 µA (micropower band) | **bench-confirmed on this unit (✓)**: ISET is fixed-bias, not part of any OUT-to-ISET feedback chain. The continuity reading from pin 3 → 15 kΩ → 274 kΩ → pin 1 that earlier suggested a 289 kΩ feedback path is in fact two independent +15 V pull-ups joining at their upper end on the V+ copper. ISET-R open ⇒ all four channels lose bias ⇒ wired-OR floats high (no fault asserts ever) ⇒ "looks healthy, monitors nothing" silent failure. ISET-R shorted to V+ ⇒ over-bias ⇒ saturation / common-mode excursion. |
| G3 | LP365M V_E (pin 16), DMM DC + DMM ohm to GND / rails / SOT-23 bases (unpowered) | pin 16 to GND (sink reference for the four OC outputs) | **bench-confirmed on this unit: V_E = GND (✓)**. R1 fingerprint match. |
| G4–G7 | Per-channel inputs and OUT — pins 6 / 5 / 3 (ch 1), 8 / 7 / 2 (ch 2), 10 / 9 / 15 (ch 3), 12 / 11 / 14 (ch 4) | (+IN) and (−IN) of all four channels found commoned across mixed polarity (pins 6 / 8 / 9 / 12 = shared-reference net VREF; pins 5 / 7 / 10 / 11 = sense pins, individual destinations TBD); all four OUTs (pins 2, 3, 14, 15) commoned onto the wired-OR node | **partially bench-confirmed (✓ on the commoning, source of VREF locked down by partial G-REF, individual sense-pin destinations TBD — see G-IN below)**. |
| G8 | Cross-correlation: each OUT to each SOT-23 base / V_E / pull-up rail / fault-flag net leaving the compartment | all four OUTs commoned + tied to a single SOT-23 base (the 'A2' actuator) + pull-up to +15 V via 15 kΩ; no other downstream destinations | **bench-confirmed (✓)**: wired-OR drives SOT-23 'A2' base directly + 15 kΩ to +15 V. The other two SOT-23s' role TBD per G-SOT. |
| G-PUP | Wired-OR node: DMM ohm + DMM DC to +15 V, −15 V, GND, +5 V (if present), and any other on-board rail; identify the pull-up R value | one resistor from the wired-OR node to a single rail | **bench-confirmed (✓)**: 15 kΩ (`1502`) to +15 V. No-fault wired-OR = +15 V; trip pulls to GND through the 15 kΩ at I_sink = 1 mA. Pull-up missing / open ⇒ wired-OR floats ⇒ fault flag indeterminate, 'A2' base floats. |
| G-REF | Shared-reference net (pins 6, 8, 9, 12 = VREF): DMM ohm + DMM DC to ±15 V / GND / Zener cathode / divider tap | VREF derived from a Zener clamp at node Y through a 56.2 kΩ / 100 kΩ divider | **partially bench-confirmed (✓)**: VREF = Vz × 0.6406, fed from +15 V → 1.82 kΩ → node Y (Zener-clamped, bypass cap) → 56.2 kΩ → VREF → 100 kΩ → GND. Vz value and via destinations remain TBD per G-Z / G-REFvia. |
| G-Z | Zener at node Y — under the SOT-23-trio PNP-triplet decode (G-SOT below), the Zener is **not** in the SOT-23 trio and is most likely in a leadless small-signal package (SOD-323 / SOD-523) or a MELF cylindrical package elsewhere on the §7G PCB; visual sweep of the §7G compartment for a 2-pin leadless / MELF part, then top-mark decode if accessible or in-circuit Vz check (DMM diode mode + powered DMM DC on Y) | Vz ≈ 5.1 V or 6.2 V (leading candidates from the I_Z = (15 − Vz)/1.82 kΩ ≈ 4–5 mA bias-current argument); other Zener voltages possible | locks down the absolute threshold VREF = Vz × 0.6406 (≈ 3.27 V at 5V1, ≈ 3.97 V at 6V2). Critical for back-calculating which monitored rails / signals would be expected to trip at which sense-pin DC values once the G-IN trace assigns each channel. |
| G-REFvia | Two untraced vias on the reference network — (i) via from node Y itself (likely off-compartment Vz distribution); (ii) via at the far end of the 1 kΩ (`1001`) stub from Y | each via lands on an on-board node either inside §7G or off-compartment; node-Y via most plausibly distributes Vz to another reference user, the 1 kΩ stub may damp / sense / decouple | identifies whether the Zener reference is local to §7G or shared with another sub-block on A21. Has no impact on the LP365M monitoring function itself (which is fully closed by the ISET / wired-OR / VREF bench evidence above), but matters for tracking systemic-reference drift across the A21 board. |
| G-IN | Sense pins 5 (−IN1), 7 (−IN2), 10 (+IN3), 11 (−IN4): DMM ohm + DMM DC to each candidate sense net (cascade-amp drain bias / §7F rail / ±15 V / X75 envelope / other) | each sense pin lands on a distinct on-board node whose nominal DC value sits in a known band relative to VREF | identifies which four signals are being monitored. The mixed-polarity input commoning (3 × +IN + 1 × −IN on VREF) implies three channels detect "sense below VREF" (UV / undervoltage / loss-of-rail) and one channel detects "sense above VREF" (OV / overvoltage / over-temp); the channel-to-rail assignment is fixed by which sense net each pin lands on. |
| G-SOT | SOT-23 trio top-mark decode (`4F`, `T1`, `2F`) + DMM-diode polarity check (red-on-base ⇒ forward to E confirms PNP; red-on-E ⇒ forward to base confirms NPN) on each part + per-pin DMM trace of all three SOT-23s | leading-candidate decodes (per the SOT-23 trio bullet in bench-confirmed contents): `4F` = **BC860B** Zetex PNP GP, `2F` = **2N2907A-family** PNP GP, `T1` = **BCX17** SGS PNP AF-Drv — **PNP triplet** under the leading reading. One of the three is **'A2'** (base on wired-OR node, base = pin 1 JEDEC); the other two are most likely a level-shift / inversion stage in series with 'A2' and a separate driver / actuator | **partially bench-confirmed (✓ on 'A2' base on wired-OR; top-mark candidate decodes recorded above)**. Polarity check on each part is the single most discriminating bench step — confirms (or falsifies) the PNP-triplet leading reading and separates BC860B vs 2SC4444 on `4F`, 2907A-family vs BC850B on `2F`. Per-pin trace of the two non-'A2' SOT-23s + identification of which SOT-23 is the leftmost (pin 3 → −15 V via 1.9 Ω) selects between the `(a‴)` PNP-switch / `(a′)` NPN-current-sink / `(a″)` PNP-emitter-follower topologies for the leftmost-SOT-23. |

**Failure modes to expect** *(updated under the confirmed R1
non-latching monitor model — fixed ISET, +15 V wired-OR pull-up,
Zener-derived shared VREF)*:

- **OUT pin stuck low** (open-collector NPN permanently saturated)
  → wired-OR forced to V_E = GND ⇒ 'A2' driven into "fault" state
  permanently; the corresponding sense node appears out-of-window
  perpetually. The remaining three channels still operate (their
  ISET bias is independent of the wired-OR), but their fault
  output is masked by the stuck channel. Indistinguishable at the
  wired-OR node from a real persistent fault on that channel; per-
  channel diagnosis requires lifting the suspect channel's OUT pin
  off the wired-OR node so the other three channels can be
  observed individually.
- **OUT pin stuck high-Z** (open-collector NPN permanently off)
  → that channel can no longer pull the wired-OR ⇒ a real fault
  on that sense node is silently masked while the other three
  channels continue to function. "Quietly defective monitor"
  failure mode.
- **ISET-R (`2743`, 274 kΩ) open** (R missing / cracked solder, or
  on-chip ISET pad bond compromised) → all four channels lose
  bias → all OC outputs high-Z → wired-OR floats at +15 V (held
  there by the 15 kΩ pull-up) → 'A2' permanently in "no fault"
  state regardless of what any sense node is doing → "looks
  healthy, monitors nothing" silent failure.
- **ISET-R (`2743`) shorted to V+** (R fully shorted, or ISET pad
  shorted to V+) → ISET pulled to V+ → over-bias on all four
  channels → saturation of the OC outputs and / or comparator-
  input common-mode excursion → unpredictable output state,
  possibly the wired-OR pulled hard to V_E continuously
  (false-fault stuck). Distinguishable from "open" by ISET DC
  voltage at V+ rather than V+ − V_BE.
- **Wired-OR pull-up (`1502`, 15 kΩ) open** → wired-OR floats
  whenever no channel is tripping ⇒ 'A2' base floats ⇒ 'A2'
  indeterminate, monitor function lost. (Note: ISET is **not**
  affected — the bias path is independent. The earlier "ISET
  starves on cold start" failure was an artifact of the withdrawn
  feedback-chain model and no longer applies.)
- **V_E pin open or shorted to wrong rail** → OC output sink
  reference broken; with V_E = GND lost, OC outputs cannot pull
  the wired-OR down even when a channel trips ⇒ fault flag never
  asserts. With V_E shorted to V− (−15 V), the OC outputs would
  pull the wired-OR below GND, possibly damaging 'A2' base /
  emitter junction.
- **(+IN, −IN) pair swapped on one channel** (board-level wiring
  error or comparator damage) → that channel's polarity inverted
  ⇒ the corresponding monitored node is reported as opposite-of-
  truth ⇒ a healthy rail asserts the wired-OR continuously, and
  the actual fault excursion is silently masked.
- **Reference network drift / failure** — affects all four
  channels' thresholds together. Sub-modes:
    - **Zener at node Y open / shorted** ⇒ Vz collapses to 0 V
      (shorted) or floats to V+ (open through 1.82 kΩ ⇒ Y at +15 V
      under no load, or pulled toward GND through the 56.2 k +
      100 k divider ⇒ Y settles at +15 × 100/(100+56.2+0) ≈ 9.6 V
      if the Zener is open and the divider is the only load on Y).
      Either failure shifts VREF to an extreme value, making the
      block chronically hair-trigger (asserts on every rail) or
      chronically silent (no fault ever asserts).
    - **1.82 kΩ (`1821`) open** ⇒ Y floats off +15 V ⇒ pulled to
      ≈ 0 V by the divider + Zener ⇒ VREF ≈ 0 V ⇒ all (+IN)
      channels assert immediately on power-up; (−IN3) channel
      silently masks any real fault.
    - **56.2 kΩ (`5622`) or 100 kΩ (`1003`) open / shifted** ⇒
      VREF / Vz ratio shifts ⇒ trip thresholds drift uniformly on
      all four channels.
    - **Bypass cap on Y open / shorted** ⇒ Y picks up rail noise
      / glitches Vz to GND respectively ⇒ either hair-trigger
      glitch-induced trips or chronic silent (Vz lost).
  This shared-reference failure family is **the single most
  likely systemic-fault explanation** if the block is observed to
  assert / not-assert regardless of the §7F or cascade-amp state.

**Pending work** *(to be filled in next bench session)*:

- **Topology discriminator — RESOLVED (R1 confirmed, non-
  latching).** The combined G3 + G4–G7 + G8 + G2 + G-PUP +
  partial G-REF bench evidence (V_E = GND, all four OUT pins
  commoned and pulled to +15 V via 15 kΩ, all four input pins
  commoned across mixed polarity onto a Zener-derived VREF, ISET
  fixed-bias to +15 V via 274 kΩ, wired-OR drives SOT-23 'A2'
  base directly) closes the R1 / R2 / R3 question in favour of
  **R1 with non-latching continuous monitoring** (the previous
  "self-disabling ISET feedback latch" model is **withdrawn** —
  the 1502 / 2743 are independent +15 V pull-ups, not a feedback
  chain). R2 (per-channel pass-element controller) and R3
  (window-comparator pair) remain withdrawn — see the Topology
  table above. The remaining `A4 G-IN` / `A4 G-Z` / `A4 G-REFvia`
  / `A4 G-SOT` worksheet rows are R1-internal probes (which sense
  nets, what Zener voltage, where the off-compartment vias lead,
  which SOT-23 code is which), not topology discriminators.
- **Wired-OR pull-up — RESOLVED (G-PUP).** 15 kΩ (`1502`) to
  +15 V; no-fault wired-OR = +15 V; trip pulls to GND through
  the 15 kΩ at I_sink = 1 mA. No further work on this item.
- **ISET bias path — RESOLVED (G2).** 274 kΩ (`2743`) to +15 V;
  ISET DC ≈ +14.3 V (≈ V+ − V_BE); I_SET ≈ 2.5 µA in the
  micropower band. No further work on this item.
- **Shared-reference network topology — RESOLVED (partial G-REF).**
  Zener at node Y (1.82 kΩ from +15 V; bypass cap to GND) divided
  through 56.2 kΩ + 100 kΩ down to VREF on the LP365M commoned
  inputs. Vz value (G-Z) and via destinations (G-REFvia) remain
  open — see below.
- **Trace the four sense pins (5, 7, 10, 11) — G-IN.** Identify
  which on-board node each sense pin lands on (cascade-amp drain
  bias, §7F rail, ±15 V supplies, X75 envelope, or other). The
  mixed-polarity input commoning (3 × +IN + 1 × −IN on VREF)
  implies three of the four sense nets are monitored for "below
  VREF" excursion (UV / loss-of-rail) and one for "above VREF"
  excursion (OV / over-temp / over-current); per-pin trace
  assigns each channel to its monitored quantity and polarity.
  Highest-priority bench task — the channel-to-rail assignment is
  the missing piece that lets §7G be cross-referenced against the
  §7F P-sequence and the cascade-amp / §7D bias chain.
- **Identify the Zener voltage Vz at node Y — G-Z.** Under the
  SOT-23-trio PNP-triplet decode (G-SOT below), the Zener is **not**
  in the SOT-23 trio and is most likely in a leadless small-signal
  package (SOD-323 / SOD-523) or a MELF cylindrical package
  elsewhere on the §7G PCB; visual sweep of the §7G compartment
  for a 2-pin leadless / MELF part is the first step, then top-
  mark decode if accessible or in-circuit Vz / Vf measurement (DMM
  diode mode + powered DMM DC on Y). Locks down the absolute
  threshold VREF = Vz × 0.6406. Leading candidates 5V1 (VREF ≈
  3.27 V) or 6V2 (VREF ≈ 3.97 V) on the I_Z ≈ 4–5 mA bias-
  current argument; needed before the G-IN sense-pin DC values
  can be back-calculated against the design windows.
- **Trace the two untraced vias on the reference network —
  G-REFvia.** (i) The via leaving node Y itself — likely off-
  compartment distribution of Vz to another reference user
  elsewhere on A21. (ii) The via at the far end of the 1 kΩ
  (`1001`) stub from Y — destination TBD, plausibly a damping /
  decoupling tap or an additional reference user. Decoupled from
  the LP365M monitoring function (which is fully closed) but
  matters for tracking systemic-reference drift across the A21
  board.
- **Confirm SOT-23 trio top-mark decodes (`4F`, `T1`, `2F`) and
  per-pin trace — G-SOT.** Candidate decodes recorded in the
  bench-confirmed SOT-23 bullet above (`4F` = BC860B PNP, `2F` =
  2N2907A-family PNP, `T1` = BCX17 PNP) — leading reading is a
  **PNP triplet**. One of the three is **'A2'** (base on the
  wired-OR node, JEDEC pin 1) — bench-confirmed; identifying
  *which* one is 'A2' selects between the (a‴) PNP-switch /
  (a′) NPN-current-sink / (a″) PNP-common-collector readings of
  the leftmost-SOT-23 bullet above. **Single most discriminating
  bench step** is a DMM-diode polarity check on each part (red on
  base ⇒ forward to E confirms PNP; red on E ⇒ forward to base
  confirms NPN) — confirms or falsifies the PNP-triplet leading
  reading and resolves BC860B vs 2SC4444 on `4F`, 2907A-family vs
  BC850B on `2F`. The remaining two SOT-23s' role (level-shift /
  inversion stage in series with 'A2', a separate driver, or
  unrelated parts) is then resolved by per-pin trace.
- **LP365M pinout itself is fixed by the National Semi datasheet
  (NS package M16A)** — see the bench-confirmed contents above.
  The previously open "trace each of the 16 pins pad-by-pad" item
  is now reduced to G-IN (sense pins) + G-Z / G-REFvia (Zener
  reference details) + G-SOT (SOT-23 trio decode) — V+, V−, V_E,
  ISET, the four OUTs, the four (+IN, −IN) commoning pattern, the
  wired-OR pull-up, and the reference-network topology are all
  bench-confirmed.
- **3866 / 5160 → §7G cross-coupling — RESOLVED (no path).** Under
  §7D (γ) the joined pin 6/7 collector outputs of both chips sum onto
  the **BFG97 collector tab** through 100 Ω + LC, not into the §7G
  compartment. Neither chip has any role in the DIAGSAMP path
  (passive A0 + 1002 + cap, per §7D revised topology) nor in the
  §7G LP365M monitor block under the R1 reading. The actuator
  question raised by the previous revision of this bullet (5160
  collector → §7G or → cascade-amp gate?) is closed: the actuator
  is the BFG97 collector summing junction. The only residual
  relevance to §7G is the G-IN trace — if any LP365M sense pin
  (5 / 7 / 10 / 11) is found to pick up an external connection
  from outside the §7G compartment, the source of that connection
  is **not** a 3866 / 5160 collector (those go to the BFG97), and
  the trace should look elsewhere (X75 envelope detector in the
  middle compartment, the cascade-amp drain bias / Id-sense node,
  the §7F rail itself, or a separate sense pickup).
- **3866 / 5160 input sense element + demodulation mechanism —
  RESOLVED under §7D (γ).** The sense element is the **X21 RF tap →
  cap → L1-Cshunt-L2 T-section LPF → commoned bases (pins 2/3) of
  both SO-8 RF transistors**. The demodulation mechanism is
  **complementary half-wave envelope rectification by the NPN/PNP
  RF pair**: with the bases sitting on the LPF-filtered LO envelope
  and the emitters pulled to opposite rails through the per-chip
  3R92 (3866 NPN emitter pour → −15 V; 5160 PNP emitter pour →
  +15 V), each chip's joined collector output (pins 6/7) carries
  the half-wave-rectified envelope of the LO tap, mirrored across
  the rail. The two outputs sum at the BFG97 collector summing
  junction through 100 Ω + LC, yielding a **bipolar push-pull
  collector-bias modulation** of the BFG97 LO buffer that closes
  the AGC loop. The earlier "V_diff = 0 forced at both inputs ⇒
  how can the chips extract a signal" puzzle falls away — the
  RF-transistor reading does not need a differential input swing
  because the bases are commoned by design and the rectification is
  single-ended on each chip's emitter-referenced collector.
- **3866 / 5160 pin 5 — RESOLVED (doubled-emitter pour group).**
  Pins 1, 4, 5, and 8 of each chip are bonded to a per-chip copper
  pour (visible top-side trace + pour underneath, per §7D β), and
  the pour is pulled to one rail through a single 3R92 (3866 → −15
  V; 5160 → +15 V). The pin 1 ≡ pin 5 short is part of the SO-8
  Case 751-05 Style 1 doubled-emitter pattern, not an offset-null
  configuration. Closed under §7D (β/γ) and superseded by the
  resolved part-ID below.
- **Copper pour under both footprints — RESOLVED (reading ii,
  per-rail through 3R92).** The four-way pour-identity discriminator
  this bullet originally proposed has landed on **reading (ii)**:
  3866 emitter pour ↔ −15 V via 3R92, 5160 emitter pour ↔ +15 V via
  3R92, with pins 1/4/5/8 on each chip bonded to the chip's own
  pour. This is the doubled-emitter / die-attach signature of the
  Motorola SO-8 Case 751-05 Style 1 RF transistor package, not a
  thermal DAP on an op-amp. The pour-identity question is closed;
  the remaining pour-related bench check (Table D rows 5d–5g, 3R92
  ohm + pour-bond visual) is a pre-rebuild integrity check, not a
  topology-discriminator probe.
- **Confirm part identity — RESOLVED (microscope top-mark read).**
  The R4D position is **MRF3866** (Motorola SO-8 RF NPN, top mark
  `R4D ∥ 3866`, Case 751-05 Style 1) and the R4N position is
  **MRF5160** (Motorola SO-8 RF PNP, top mark `R4N ∥ 5160`, same
  case). These are the SO-8 surface-mount derivatives of the
  Motorola TO-39 **2N3866 / 2N5160 complementary RF pair** — the
  2N5160 datasheet explicitly designates itself as *"Designed for
  Use in Complementary Circuits with 2N3866"*. Pinout per Case 751-05
  Style 1: pins 1/4/5/8 = doubled emitter (on the per-chip rail
  pour via 3R92), pins 2/3 = doubled base (on the X21 cap-tap LPF),
  pins 6/7 = doubled collector (on the BFG97 summing junction via
  100 Ω + LC). The previous matched-pair / catalog-search work plan
  is closed; sourcing details are in the §7E Replacements table
  (3866 row + 5160 row). The earlier "no substitution test viable"
  caveat was correct under the unresolved hypothesis but is now
  superseded — a like-for-like MRF3866 + MRF5160 fit (or NOS 2N3866
  / 2N5160 in the SO-8 footprint with leg dressing) is the resolved
  rebuild path.
- **3866 / 5160 functional role — RESOLVED.** Per the resolved
  sense / demodulation bullet above and §7D (γ), the two chips are
  a **complementary half-wave envelope detector pair driving
  collector-modulated AGC on the BFG97 LO buffer**. Each chip
  rectifies the X21 LO envelope on its commoned bases (pins 2/3)
  into an emitter-referenced DC envelope on its commoned collectors
  (pins 6/7); the two collector currents sum at the BFG97 collector
  tab through 100 Ω + LC, modulating the BFG97 collector bias and
  hence its LO-buffering gain. The previous three-way hypothesis
  (RF detector pair / op-amps in self-rectifying mode / dummy EMC
  parts) is collapsed: hypothesis (a) is selected as the resolved
  reading, (b) is withdrawn under §7D (γ) op-amp falsification, and
  (c) is withdrawn by the failure pattern itself (dummy parts
  wouldn't drag X75 / TP1910 dead when they fail).
- **Device-rating anomaly vs. resolved-AGC role — RESOLVED
  2026-04-30 (push-pull power-output reading wins).** Recovered
  schematic (sheet 02/02 of A211 var.02; filed at
  [`rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg`](rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg))
  draws the V3 (MRF3866) / V4 (MRF5160) pair as a complementary
  class-AB push-pull stage with the BFG97 (V2) wired as the
  base-driving pre-driver (bias-network detail: L41 / L43 470 nH
  are base-bias RFCs in series with R43 / R44 100 Ω; R40 / R41
  3R92 are emitter-to-rail directly; collectors tie → L45 / C49
  → off-page → X21 — see DEEPER SCHEMATIC RE-READ banner at top
  of §7D)
  (V2 collector → bias divider → commoned MRF3866 / MRF5160 base
  node, no AGC modulation path). The combined ≈ 2 W device-rating
  envelope matches the +26…+30 dBm X21 LO drive spec. The §7G γ
  collector-modulated AGC topology and the parts of §7D D.3 that
  flowed from it are SUPERSEDED — see §7D banner. The discriminating
  bench checks below (procedure step 7 DC-across-3R92, SA at base
  vs. collector tab) are no longer needed for topology disambiguation
  but remain useful as bring-up sanity checks during Step 8a. The
  original alternative-reading text is retained for FA traceability.

- **Device-rating anomaly vs. resolved-AGC role — OPEN QUESTION (H)** *(historical, RESOLVED above)***.**
  The MRF3866 / MRF5160 are 1 W class-AB RF transistors (P_TOT
  ≈ 1 W per chip with the four-pin emitter heat-sink path, I_C
  ±400 mA, V_CEO 30 V / −40 V, f_T ≈ 1 GHz / ≈ 100–250 MHz — about
  2 W combined for the pair). Standard envelope-detector duty
  draws single-digit mW on Schottky diodes or small-signal SOT-23
  transistors; using a power-rated complementary RF pair purely
  for envelope sense is textbook overkill. Alternative reading
  consistent with the bench topology (commoned bases via cap +
  L1-Cshunt-L2 LPF, commoned collectors summed through 100 Ω + LC
  into the BFG97 collector tab): the 3866 / 5160 are the
  **class-AB push-pull LO power-output stage driving X21 directly**,
  with the BFG97 acting as the **pre-driver** rather than the
  actuator — i.e. signal flow is BFG97 → 3866 / 5160 → X21, not
  the inverse. In that reading the device ratings line up with
  the +26…+30 dBm X21 spec, the complementary NPN/PNP pair makes
  sense as a push-pull output (the original *"Designed for Use in
  Complementary Circuits"* 2N3866 / 2N5160 application class), the
  bench-traced "cap tap off X21" reads instead as the cap-coupled
  output of the power amp, and the ALC must close elsewhere — most
  plausibly via BFG97 base-bias modulation by an upstream envelope
  detector (the §7G LP365M block is one candidate locus, the
  passive A0 + 1002 + cap rectifier feeding DIAGSAMP is another
  if a re-trace finds an unobserved tap-back path). Discriminating
  bench checks (run after §7E rebuild restores LO at X21):
  (1) SA at the BFG97 collector tab vs. SA at the X21 brass pin
      (≥ 30 dB / ≥ 1 W pad on X21). If X21 reads ≈ +30 dBm and the
      BFG97 collector reads ≈ +10 dBm or less, signal flow is
      BFG97 → 3866 / 5160 → X21 (power-amp hypothesis confirmed);
      if BFG97 collector ≈ X21 minus small loss, flow is the
      inverse (resolved-AGC reading stands).
  (2) DC standing current per chip via V across the 3R92 emitter
      resistor: envelope-detector duty draws ≈ 1–10 mA per chip
      standing (4–40 mV across 3R92); class-AB power-output duty
      draws ≈ 50–200 mA per chip (200 mV – 800 mV across 3R92).
  (3) Spectrum at the 3866 / 5160 commoned base node: linear
      power-amp drive ⇒ clean LO-band fundamental at −10 to 0 dBm;
      envelope-detector sense tap ⇒ much lower level (≈ −20 dBm or
      below) with rectification products visible.
  Until these are run, the §7D γ "RESOLVED — collector-modulated
  AGC" verdict above should be read as the leading hypothesis on
  bench-topology grounds, not as a closed question — the device-
  rating argument is a real falsifier candidate. The §7E rebuild
  plan and the BFG97 collector-network integrity walk-through
  remain valid under either reading: AGC reading ⇒ BFG97 is the
  actuator; power-amp reading ⇒ BFG97 is the pre-driver; but the
  collector network connectivity (100 Ω + LC summing into the
  BFG97 collector tab) and the chip-level integrity checks
  (Table D rows 5d–5g, 7a–7e) are required either way. The
  power-amp reading also collapses §7F doubler-location candidate
  (c) into the broader question of where in the BFG97 → 3866/5160
  chain the doubling sits — if the 3866 / 5160 are the output
  power amp, the doubler is most likely *upstream* of the BFG97
  base (favoring §7F (a) — the 420 cascade as doubler).
- **BFG97 part-ID + LO-chain role confirmation — NEW.** The BFG97
  was identified by its top-mark and SOT-223 footprint (NXP/Philips
  wideband NPN RF transistor, f_T ≈ 5 GHz, intended for VHF/UHF
  amplifier and oscillator buffer applications). Confirm by:
  (a) reading the SOT-223 top-mark under magnification (NXP/Philips
      house-mark + date code);
  (b) cross-referencing against the §7.4.1 LO-chain block diagram
      (drawing 1035.8840.01 band-3 p.156) — the BFG97 should appear
      between the X50 doubler / V50 cascade-amp stages and the X21
      output as the level-controlled buffer; verify the schematic
      label matches and that the collector-tab ↔ 3866 / 5160
      connection is drawn (this is the bench-traced finding being
      cross-checked against the manufacturer's intent);
  (c) recording its base-divider and emitter-resistor values from
      the surviving silkscreen / bench trace, for the bias-network
      walk-through bullet below.
- **BFG97 bias-network integrity walk-through — NEW.** During the
  3866 / 5160 failure, the BFG97 collector was held near 0 V for an
  unknown duration by the back-drive from the latched complementary
  pair (per §7D.3 site 5 cascade analysis). This is well outside the
  BFG97's class-A operating range (collector should sit several
  volts above ground for an NPN buffer on +15 V supply) and may
  have stressed the collector-load inductor, the 100 Ω summing
  resistors, the base divider, the emitter resistor(s), or the
  BFG97 itself. Bench checks (chips-out, before fitting fresh
  3866 / 5160 silicon — partly covered by Table D rows 7c/7d/7e but
  extended here):
  (1) BFG97 diode test on the SOT-223 footprint — collector ↔ base
      and base ↔ emitter junctions both show normal Vf (~0.7 V
      forward, OL reverse); collector ↔ emitter both directions
      should be OL on a healthy NPN. C-E shorted both directions
      ⇒ replace BFG97 (still in NXP catalog as of 2024).
  (2) Collector-load inductor: ohm to +V rail (a few Ω + DCR; OL
      ⇒ inductor fused open). Same as Table D row 7e.
  (3) 100 Ω summing resistors (3866 and 5160 legs): each ≈ 100 Ω
      + small inductor DCR, end-to-end from each chip's pin 6/7
      footprint to BFG97 collector tab. Same as Table D rows 7c/7d.
  (4) Base divider: read both resistor values, compare against
      typical BFG97 application notes (base bias for class-A
      operation at the chosen quiescent collector current).
  (5) Emitter resistor: read value; OL ⇒ replace; off-value ⇒ the
      bias point will be shifted but the LO buffer will still
      function for first-power-up testing.
  Failures of (1) or (2) **must** be repaired before fitting fresh
  3866 / 5160 silicon; failures of (3)–(5) can be deferred to post-
  rebuild verification but should be recorded.
- **Catalog search task — CLOSED.** Resolved by the microscope top-
  mark read (R4D position = MRF3866 NPN, R4N position = MRF5160 PNP,
  both Motorola SO-8 Case 751-05 Style 1 — see the resolved part-
  identity bullet above and the §7E Replacements table for sourcing
  details). The original 1990s SOIC-8 dual-matched-pair / RF-
  detector-dual catalog axes are no longer load-bearing; the
  Motorola SO-8 RF-transistor family was a different product line
  from the dual-matched-pair classes those axes targeted.
- **A0 part identity — RESOLVED (HSMS-2800).** The DIAGSAMP-rectifier
  A0 SOT-23 (and at least the two further on-board A0-marked
  footprints used as in-circuit Vf reference brackets in §7D, reading
  0.234 V and 0.265 V forward) are **HP/Avago HSMS-2800** single
  low-barrier RF Schottky diodes. *(Schematic cross-check note,
  2026-04-30: on the recovered Var.02 sheet 02/02 the only HSMS-2800
  instances drawn are V61 and V62 inside the FREQUENCY DOUBLER block
  — the bench-traced "third A0 = DIAGSAMP rectifier on the X21 RF
  tap" is **not visible** on the available JPEG, almost certainly
  because the right-margin column-9 strip of the sheet is cropped
  off the image. The bench-side rectifier identification is
  downgraded to provisional pending a higher-res scan; see §7D
  DEEPER SCHEMATIC RE-READ banner item 2.)* Resolution path:
  (a) Top-mark read on a sister A211 board photo: `A0E`, decoded as
      `A0` (HSMS-2800 family code per the HP/Avago marking table)
      plus `E` (date / lot character). The HSMS-280x catalog has no
      `A0E` lead-code suffix — singles in SOT-23 are `A00`, singles
      in SOT-323 are `A0B`, common-anode variants use the `A3*`
      prefix — so `A0E` cannot be a literal three-character HSMS code
      and the `E` must be a date/lot character.
  (b) Bench topology: pin 1 = cathode (hard to GND on the DIAGSAMP
      footprint), pin 3 = anode (on the X21 RF tap), pin 2 truly NC.
      This **falsifies** all HSMS-280x dual / common-anode variants
      (HSMS-2802 / 2803 / 2804 / 2805 / 280E / 280F all drive pin 2),
      leaving only HSMS-2800 (SOT-23 single) and HSMS-280B (SOT-323
      single — same die, different package) as candidates.
  (c) Bench Vf: 0.23 … 0.27 V at DMM Itest on the two healthy A0
      reference footprints — consistent with HSMS-2800's datasheet
      Vf ≈ 0.34 V at 1 mA (low-barrier RF Schottky family).
  (d) Package size on this unit confirmed as full SOT-23 (not the
      smaller SOT-323), so HSMS-2800 over HSMS-280B for the
      procurement order.
  Resolved sourcing path: **co-primary HSMS-2800-BLKG (Broadcom/Avago,
  natural orientation, 1=K / 3=A) or MACOM MA4E1340A1-287T (current
  production, **rotated 180°** because the MACOM SOT-23 single uses
  the opposite 1=A / 3=K polarity convention per Mouser spec-sheet
  `maom-s-a0010058398-1.pdf`; +70 mV medium-barrier Vf offset
  negligible against the +7.5 … +11 V DIAGSAMP spec window)** — see
  the §7E Replacements table for the on-hand fallback ranking. The
  previous "BAT54C-primary substitution with ±100 mV Vf offset
  caveat" framing is demoted to fallback; both co-primaries land
  DIAGSAMP DC well inside spec.
- **V95 "A0" SOT-23 — three-terminal-vs-Schottky inconsistency, NEW.**
  §7C Table B (rows 6–7) and §7C decision-matrix row 5 treat V95 as
  a **three-terminal device** with "base/gate" driven from an
  upstream gate-voltage reference and "collector/drain" tied to the
  X95 brass pin (−0.72 V on this unit, in the §7F 420 cascade-amp
  bias range). A 2-terminal HSMS-2800 cannot account for this
  topology. Two possibilities to discriminate at the next bench
  session:
  (i) **V95 is genuinely HSMS-2800** (consistent with the rest of
      the A0 sites on this PCB) used as a **clamp diode** on the
      X95 gate-bias rail — anode/cathode polarity and the upstream
      "gate-voltage reference" are then a re-reading of a passive
      bias divider, and the "−0.72 V at the collector/drain" reading
      is the divider output at the diode-clamped node. Under this
      reading the §7C Table B rows 6–7 wording ("base/gate",
      "collector/drain") was an early-revision misframing inherited
      from the unresolved part-ID and needs rewriting to
      "anode / cathode" once the polarity is bench-confirmed.
  (ii) **V95 is a different "A0*"-marked SOT-23 part** — the
      s-manuals.com SMD-marking database lists `A0**` (3-character
      mark) in SOT-23 as the **AO3400** (Alpha & Omega N-channel
      MOSFET, V_GS(th) ≈ 1.4 V, R_DS(on) ≈ 30 mΩ at V_GS = 4.5 V).
      This is consistent with the active-device behaviour assumed
      in §7C and would explain why the original analysis used FET
      terminology. A microscope read of V95's full top-mark (single
      `A0` + date code → HSMS-2800; or `A0` + two more characters →
      AO3400 or similar) would discriminate.
  Bench step: read V95's full top-mark under magnification, then
  trace its three pad copper destinations (gate-bias source, drain /
  cathode → X95, source / anode → GND or another bias node) to
  decide which reading is correct. Update §7C Table B + decision
  matrix accordingly. **No rebuild action required** — the §7C bias
  chain reads in spec on this unit (X95 within device-spread, X96
  in spec) so V95 is operating correctly under whichever
  interpretation is right; this is a documentation-consistency
  cleanup, not a fault investigation.
- **DC math on the DIAGSAMP rectifier doesn't close.** With A0
  confirmed as a single HSMS-2800 (anode on the X21 RF tap, cathode
  hard to GND, pin 2 truly NC), the voltage-doubler / dual-rectifier
  hypothesis is **falsified** — the rectifier really is a single
  half-wave Schottky followed by 1002 + shunt cap. Isolated analysis
  predicts DIAGSAMP ≈ 0 V (positive RF excursions clamped at +Vf,
  shunt cap averaging to a small offset), but the §7.4.1 spec is
  +7.5 … +11 V. The remaining candidate explanations are: (a) a DC
  pull-up on the X21 RF tap node from upstream LO-chain drain bias
  not yet bench-traced, which would convert the half-wave detector
  into a peak detector referenced to a DC pedestal; or (b) a charge-
  pump cap on the X21-tap side of A0 that the bench trace missed,
  giving the same effect by AC-coupling the X21 RF onto a pedestal
  set by the 1002 + shunt-cap RC. Both are upstream of A0, not in
  the rectifier itself. Verify after the §7E rebuild restores LO at
  X21 — DMM-DC sweep on the DIAGSAMP node and the X21 tap node with
  `--a21-probe` running.


### Step 8 — X21 doubler output *(SA + ≥30 dB / ≥1 W pad — contingent diagnostic, only if X75 / TP1910 stays dead after rebuild, or recurring-failure escalation)*

Schematic: same drawing 1035.8840.01 — **band-3 p.156 (schematic) +
p.152 (XY-list)** — explicitly cited at the head of §7.4.1 p.146.
Spec table is the §7.4.1 *"Testing the Frequency Doubler with LO
Amplifier"* table on p.146.

⚠ **X21 carries up to +30 dBm = 1 W of LO drive.** Fit the ≥30 dB /
≥1 W attenuator pad **at the X21 connector and tighten before
powering the SMP back up**; a bare SA cable on X21 will destroy the
analyser front end on power-up. Use a pad with continuous (not
pulsed) 1 W rating.

⚠ **X21 is the connector between A211 and the milled casing — it
carries the LO drive *into* the casing, fed from the on-PCB
comb-generator chain (doubler V50/V60 → LO amps V2/V3/V4 →
step-recovery V4)**. The test runs with the A211 PCB withdrawn from
the casing (§7.4 p.146 / §7.5 p.147). Power down before separating,
fit the pad on the now-exposed X21, then power back up. The pad sits
between the comb-generator output and what would normally be the
casing's LO input; the SA reads the comb-gen output level and
spectrum directly.

§7.4.1 strict form drives X50 from an external bench source at
+6 dBm / 103…117 MHz. On this unit X50 is already verified in spec
at the A21 connector by Step 4 (+3.75 dBm @ 106.56 MHz at the SA
after cable + DC-block losses, A7 path exonerated), so internal
drive via `--a21-probe` is acceptable: sweep the commanded SMP RF
frequency 2 → 20 GHz and capture the SA trace at X21.

Expected spectrum at X21 (§7.4.1 table, p.146):

- **< 0 dBm @ 103–117 MHz** (fundamental leak)
- **+26…+30 dBm @ 206–234 MHz** (doubler output, band of interest)
- **< +5 dBm @ 309–351 MHz** (3rd harmonic)

Concurrent witness: TP1910 should climb to 7.5…11 V when X21 is at
spec (§7.4.1 *"Nominal value of diagnostic voltage at W216.10:
7.5…11 V"*). If X21 meets spec but TP1910 stays at 0.22 V, jump to
Step 11 (diag rectifier on A211 — components on p.152 / p.156
between X21's sense tap and W216.10). Fail (X21 dead) → doubler
V50/V60 or LO amp V2/V3/V4; identify the dead node from the p.156
schematic before deciding on board swap / factory repair.

### Step 8a — On-A211 LO chain, bench-PSU standalone *(SA, board out, no casing)*

> **Ordering:** runnable **before §7E rebuild**. In-instrument Step 7A–7D
> bias readings (the only Step-7 work that requires the board mounted)
> are the only hard prerequisite, and are already complete. 8a is the
> most direct RF validator of §7D D.5's "alive" branch — pass clears
> §7D D.3 / §7F doubler-location / §7G push-pull-vs-detector by
> exclusion without committing to the rebuild.

Bench-PSU variant of Step 8. Same X21 spectrum measurement, but the
A211 PCB is **out of the milled casing and off the backplane** —
powered from external bench supplies via W216 alone, X50 driven from
an external bench source. Exercises the full X50 → X21 LO chain
(LO amp / doubler / §7F 420 NPN cascade / §7G BFG97 + 3866 + 5160
stage / matching networks) with no dependence on the casing, the IF
chain, the DIAGSAMP rectifier, or any other A2x board. Runs in
~30 min and is the **most direct functional test of the §7D D.3 /
§7F doubler-location / §7G push-pull-vs-detector open questions** —
a pass at this step *itself* answers all three by exclusion (chain
carries signal to spec ⇒ silicon alive, doubler functional, matching
intact, regardless of what the static 105 Ω C-E reading meant).

**Power rails needed (W216, polarity / pin per closed mapping):**

- **+15 V analog** — BFG97 collector-load L return, 5160 emitter
  path, LP365M supervisor sense. Limit 200 mA initial.
- **−15 V analog** — 3866 emitter path, LP365M supervisor sense.
  Limit 200 mA initial.
- **+7.5 V** — §7F 420 NPN cascade collector. **Supervisor-gated**
  through the V85 / V89 cut-off switches. Limit 300 mA initial.
- **GND** — single-point from PSUs to W216 GND pin(s).

**Supervisor handling:** bring up ±15 V cleanly **first**, then
add +7.5 V.

> ⚠ **LP365M N.F. on Var.02 — caveat 2026-04-30.** Per the recovered
> schematic, on this Var.02 PCB the LP365M (N80-E) and its input-
> divider ladder are marked N.F., so there is **no LP365M wired-OR
> fault node to verify** before adding +7.5 V, and the V85 / V89
> cut-off path on the +7.5 V rail is also N.F. on this variant.
> The "verify wired-OR at +15 V → 1 kΩ clip-up bypass" gating below
> is **moot on this unit** — bring up +7.5 V directly after ±15 V
> with the same 300 mA limit. The legacy procedure text below is
> retained verbatim for sub-variants where N80 + V85 / V89 are
> populated; if a future bench unit shows soldered LP365M, restore
> the wired-OR-verify gate. See §7D DEEPER SCHEMATIC RE-READ banner
> item 3 for the full N.F. inventory and the §7G N80 bullet.

(Legacy procedure text, retained for populated-LP365M sub-variants:)
verify the LP365M wired-OR fault node sits at +15 V (no fault) —
the wired-OR is the commoned LP365M comparator-output node, also
driving the SOT-23 'A2' switch base, pulled up to +15 V via the
bench-confirmed "1502" 15 kΩ resistor (see §7G LP365M analysis
for physical location on the back-face PCB). **Then** add +7.5 V.
If wired-OR is pulled low after ±15 V comes up, an out-of-window
sense pin is tripping the LP365M — either bring up whatever rail
is being monitored, or **bypass** by clipping the wired-OR node up
to +15 V through a 1 kΩ test R (forces the V85 / V89 cut-off
switches closed regardless of supervisor state). Bypass is
acceptable for this test because the test does not depend on
rail-fault protection.

**Bias-monitoring interference (categories 1–3):**

Three on-board monitor blocks could in principle interfere with the
bench-PSU measurement; the procedure as written handles 1 and 2,
and 3 is a post-reassembly concern only.

1. **Supervisor crowbar (HIGH potential, fully blocking if it fires)** —
   the LP365M wired-OR fault node drives the SOT-23 'A2' switch,
   which controls the V85 / V89 cut-off path between W216.4 and the
   on-board +7.5 V net feeding the §7F 420 NPN cascade. Wired-OR
   low → A2 conducts → V85/V89 open → no +7.5 V at the cascade →
   no LO chain output regardless of how clean X50 is. Diagnostic
   signature: bench PSU on +7.5 V draws ~0 mA at 300 mA limit, and
   the wired-OR DMM probe reads ~0 V. Mitigation lives in procedure
   step 2 (verify wired-OR at +15 V before adding +7.5 V) and the
   bypass option (1 kΩ clip-up). If the 4th LP365M comparator
   monitors a rail not bench-applied (hypothetical +5 V, OCXO ref,
   etc.), the bypass takes care of it without having to identify
   which sense pin tripped.

2. **AGC loop (MEDIUM potential, conditional on §7G verdict)** —
   only relevant if the §7G "AGC reading" topology stands (3866 /
   5160 are RF envelope detectors with an OP97 N90 error-amp loop
   modulating an upstream variable-gain element). In that case the
   loop can either (a) slam to one rail if its reference is dead,
   driving X21 to compressed-flat or fully off regardless of LO
   chain health, or (b) scream at full gain if the VGA itself is
   dead, hiding the actual fault from the X21 spectrum. Mitigation:
   procedure step 7 (DC across 3R92) settles AGC-vs-power-amp **as
   part of the test** — interpret the X21 spectrum in light of the
   3R92 reading. If the AGC reading lands and X21 is far from
   spec, follow up with §7G probe 3 (BFG97 collector tab, low-cap
   probe) to localize fault upstream / downstream of the loop sense
   point.

3. **Bias decoupling cap loading (LOW)** — leaky bypass caps along
   the LO chain bias-feed network couple rail noise onto RF nodes
   through their respective chokes. Bench PSUs are typically much
   quieter than the on-board switching regulators that source +15 V
   in the assembled instrument, so any decoupling-cap leakage
   problem can **mask** here (clean X21 on the bench, degraded
   SFDR / lifted noise floor in the assembled instrument). Not a
   Step 8a pass / fail concern — flag for the post-reassembly
   in-instrument retest if SFDR is poor despite Step 8a passing.

What does **not** interfere:

- **Casing biases (X72 / X95 / X96)** are A211 outputs, not inputs.
  With the casing disconnected, the SMB pigtails are open at the
  far end and put no load on the LO chain.
- **DIAGSAMP rectifier** is a passive high-Z tap on X21. Doesn't
  load the chain; can be used as a secondary witness during 8a
  (TP1910 / W216.10 should climb to 7.5…11 V if X21 hits spec).
- **W216.10** is the DIAGSAMP rectifier output, monitor-only.


**Procedure:**

| # | Step                                                                                                                              |
|---|-----------------------------------------------------------------------------------------------------------------------------------|
| 1 | A211 board out. W216 accessible.                                                                                                  |
| 2 | Wire bench PSUs to W216: GND first; +15 V at 200 mA limit; −15 V at 200 mA limit. Verify LP365M wired-OR at +15 V.                |
| 3 | Add +7.5 V at 300 mA limit. Record steady-state I on each rail.                                                                   |
| 4 | Bench source → X50: +6 dBm CW at 110 MHz (mid-band) to start.                                                                     |
| 5 | SA on X21. Span 50–500 MHz, RBW per §7.4.1.                                                                                       |
| 6 | Sweep X50 fundamental 103–117 MHz; capture trace at each end.                                                                     |
| 7 | (Optional, settles §7G) DMM across each 3R92 while X50 driving; record DC for §7G probe 1 (200–800 mV ⇒ power-amp; 4–40 mV ⇒ AGC). |
| 8 | Power-down: X50 source off, +7.5 V off, ±15 V off, GND last.                                                                      |

**Expected spectrum at X21 (per §7.4.1):**

- **< 0 dBm @ 103–117 MHz** (fundamental leak)
- **+26…+30 dBm @ 206–234 MHz** (doubler output, band of interest)
- **< +5 dBm @ 309–351 MHz** (3rd harmonic)

Open-X21 caveat: with the brass pin un-mated to the casing, X21 sees
a low-load reflection. Expect 1–2 dB amplitude wobble vs. §7.4.1
spec — acceptable for pass/fail, not for spec-grade numerics.

**Outcome localization:**

| Result                                                              | Reads                                                                                                                                                                          |
|---------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| +26…+30 dBm @ 206–234 MHz                                           | LO chain healthy. §7D D.3 / §7F doubler-location / §7G push-pull-vs-detector all answered by exclusion: silicon alive, doubler functional, matching networks intact.           |
| +13…+25 dBm @ 206–234 MHz                                           | Chain alive but degraded. Candidates: drifted matching trim, reduced doubler conversion efficiency, partial 3866/5160 leakage, ageing 420 cascade.                             |
| < +13 dBm @ 206–234 MHz, strong fundamental at 110 MHz at X21       | Doubler stage dead. §7F (a) 420-cascade-as-doubler hypothesis lands; or V50/V60 if separate. Probe 4 (RIGHT 420 collector SA) localizes.                                      |
| No spectrum at all, fundamental absent at 110 MHz too               | Input stage dead (LO-amp ahead of doubler), or supervisor crowbar still active despite ±15 V good (re-check wired-OR), or a W216 supply path open.                            |
| DC across 3R92 in 200–800 mV range (procedure step 7)               | §7G power-amp reading confirmed; the §7G "device-rating anomaly" alternative is the correct topology. 3866/5160 are class-AB power-output, BFG97 is the pre-driver.            |
| DC across 3R92 in 4–40 mV range (procedure step 7)                  | §7G original AGC / detector reading stands.                                                                                                                                    |

**Notes:**

- Supervisor crowbar: bring up rails in the order given (±15 V →
  verify wired-OR → +7.5 V); applying +7.5 V to a tripped-clamped
  node can put a transient on the 420 cascade collector.
- §7E rebuild step 2 (3866 / 5160 reflow) is **not** required ahead
  of this test — they remain in-circuit, bench-confirmed alive by
  the D.5 ohm cross-check (PASSED 2026-05-03). Test 8a is now the
  direct RF validator of that chips-alive verdict; pass closes the
  §7D silicon question by exclusion, fail re-opens it and triggers
  D.6 (5160 desolder + OOC re-probe) before any silicon replacement.

A pass at Step 8a, combined with passes at Step 10a (IF chain on
A211) and Step 8b (casing alone), exonerates every component on the
A21 IF and LO signal paths — leaving only Step 11 territory
(DIAGSAMP rectifier, W216.10 conductor, wiring, in-instrument
supervisor) as failure surfaces if `--a21-probe` still reads X75
dead after reassembly.

### Step 8b — Milled casing, bench-PSU standalone *(SA, casing on bench, A211 disconnected)*

> **Ordering:** runnable any time the casing is unmated from A211 —
> independent of every other step on this page (Step 7, §7E rebuild,
> 8a, 10a). Pass exonerates the casing in full, leaving only the
> on-A211 LO and IF chains as fault surfaces.

Bench-PSU variant of Steps 9 / 10's casing-internal coverage.
Casing **isolated from the A211 PCB**, driven directly with bench-
PSU biases on X72 / X95 / X96, bench LO source on the casing-side
X21 brass pin, bench RF source on X211. Reads IF at X70. Exercises
**A214** pre-mixer RF amp + the **passive Schottky-bridge sampling
mixer** + **A212** in-casing IF amp with no dependence on the
on-A211 LO chain, IF chain, supervisor, bias generators, or any
other A2x board. Runs in ~30 min.

**Biases needed (all sourced from bench PSUs, no W216):**

- **X72: +15 V** — VA15-IF, A212 IF amp drain. Limit 50 mA.
- **X96: +6.3 V** — VD, A214 drain. Limit 30 mA.
- **X95: −0.5 V** — VG, A214 gate (negative; verify polarity at the
  PSU output before connecting). Limit 5 mA.
- **GND** — single-point from PSUs to casing chassis.

These bypass the A211 supervisor and bias generators entirely. The
W216 connector on A211 is **not** needed for this test — the casing
is electrically independent once the X72 / X95 / X96 SMB pigtails
are sourced from the bench.

**Bias-monitoring interference:** none of the categories that apply
to Step 8a apply here. (1) The LP365M supervisor lives on A211 and
gates A211-side rails — with A211 disconnected, the supervisor is
not in the loop at all. (2) The §7G AGC-vs-power-amp question is on
the LO chain, not on the casing's IF chain — no AGC loop traverses
the casing. (3) Decoupling-cap loading inside the casing is not a
bench-PSU artifact; bench supplies and the in-instrument supplies
are equally clean from the casing's perspective once the bypass
caps on the X72 / X95 / X96 feeds inside the casing are doing their
job. The only category-3-flavour concern is bench-PSU lead
inductance on the +15 V X72 feed acting as an unintended choke for
A212's drain — keep the bench leads short and twisted, and
verify +15 V at the casing pin (not just at the PSU) before drawing
any conclusions about A212 health from low IF level.

**Stimulus:**

- **LO at casing-side X21 brass pin: +26…+30 dBm at 206–234 MHz.**
- **RF at X211: −10…0 dBm anywhere in 2…20 GHz** (e.g. 10.000 GHz).
  Choose RF and LO such that `|RF − n·LO|` falls in the 10–80 MHz
  YIG-PLL window. Worked example: RF = 10.000 GHz, LO = 232.0 MHz
  → 43rd LO harmonic = 9.976 GHz → IF = 24 MHz.

**Procedure:**

| # | Step                                                                                                                                              |
|---|---------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Casing on bench. A211 disconnected at X70 / X75 / X95 / X96 / X72 / X21 (all SMB pigtails free at the casing side).                                |
| 2 | Wire bench PSUs to casing-side X72 / X96 / X95 / chassis GND. Bring up biases in order: GND, X72 +15 V at 50 mA limit, X96 +6.3 V at 30 mA limit, X95 −0.5 V at 5 mA limit. Record steady-state I on each. |
| 3 | LO source → casing-side X21 brass pin. Set LO to **+28 dBm at 232.0 MHz**.                                                                        |
| 4 | RF source → X211. Set RF to **0 dBm at 10.000 GHz**.                                                                                              |
| 5 | SA on X70. Span 1–200 MHz, RBW 100 kHz, ref level −10 dBm.                                                                                        |
| 6 | Find IF tone at expected frequency (24 MHz for RF=10 GHz / LO=232 MHz / n=43). Record level.                                                       |
| 7 | Step RF in 10 MHz increments around 10 GHz: IF tone should track at the same step size (confirms harmonic mixing, not a leakage path).             |
| 8 | (Optional) Disconnect RF input at X211: IF tone should drop to noise floor. Persistent IF means casing-internal LO leakage path.                   |
| 9 | Power-down: RF source off, LO source off, X95 off, X96 off, X72 off, GND last.                                                                    |

**Expected:**

- **IF level at X70: ≈ −15 … −5 dBm for 0 dBm RF at X211.**
  Sampling-mixer conversion loss at 10 GHz typ. 20–30 dB; A212 IF
  gain ≈ +15…+27 dB (the upper bound is the §7.4.2 spec, but per
  §7G bench finding the +27 dB may be A212+A08 combined — A212
  alone is more like +15…+20 dB). Net IF ≈ 0 dBm RF − 25 dB conv
  loss + 18 dB A212 gain ≈ −7 dBm, ±5 dB.
- IF tone tracks RF stepping 1:1.
- IF at noise floor with no RF input.

**Outcome localization:**

| Result                                                              | Reads                                                                                                                                                                      |
|---------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tracking IF tone at expected level (~−7 dBm)                        | A214 + sampling mixer + A212 + casing biases all healthy. Casing exonerated.                                                                                              |
| No IF tone, supply currents normal                                  | Sampling-mixer Schottky bridge dead, OR A212 dead, OR LO not actually reaching the comb generator (X21 brass-pin contact issue, comb-gen input network drift).             |
| IF tone present but very weak (−25 dBm or lower)                    | A214 RF amp dead — RF input to mixer is much lower than expected. Confirm by removing RF input and watching for self-noise change at the IF frequency.                     |
| IF tone at expected frequency but compressed / distorted            | A212 IF amp in compression. Check X72 actually at +15 V at the casing pin (not just at the PSU). If X72 < +14 V at the casing pin, A212 saturates; check the SMB pigtail.  |
| X96 supply current >> 30 mA at +6.3 V                               | A214 gate-source short or drain-source punch-through. Pull power immediately.                                                                                              |
| X72 supply current >> 50 mA at +15 V                                | A212 drain-source short. Pull power immediately.                                                                                                                           |

**Notes:**

- The casing's X21 input has a comb generator (step-recovery diode
  + impedance-transforming structure) ahead of the sampling mixer.
  Below the +26…+30 dBm LO spec range no comb teeth form and IF is
  absent — drive at spec or the test's expected outcome doesn't
  apply.

A pass at Step 8b exonerates the casing in full and isolates any
remaining X75-dead symptom to the on-A211 IF chain (covered by
Step 10a) or the on-A211 LO chain (covered by Step 8a).



### Step 9 — Re-read X75 after Step 8 *(SA, only if Step 8 X21 passes)*

Repeat Step 4's X75 measurement once Step 8 has confirmed X21 is at
spec. Fail → **A214** pre-mixer RF amplifier (X211 → sampling-mixer
RF port) / passive Schottky-bridge sampling mixer / **A212** IF
amplifier (post-mixer, in-casing) / on-PCB IF chain between X70 and
X75 (per §7G bench finding 2026-04-29: **L72 LP filter + A08 MAR-8
IF post-amp on its 195 Ω +15 V bias R + the input / output DC-block
caps**, not a passive impedance transformer as previously described);
board swap / factory repair for the casing-internal stages
(A212/A213/A214 are not field-serviceable). The on-A211 A08 stage
**is** field-serviceable (modern drop-in: Mini-Circuits MAR-8A+ on
the existing 195 Ω bias R, see §7G A08 sourcing block).

### Step 10 — IF-chain |S21| *(VNA, casing **in place** with A212 IF amp powered, A08 IF post-amp powered on A211)*

Per band-3 §7.4.2 p.146. Per drawing 1035.8840.01 the casing-internal
IF amplifier is the **A212** sub-assembly (biased via X72 / VA15-IF),
so X70 is its **output** (casing → A211). **Per §7G bench finding
2026-04-29, the on-A211 path between X70 and X75 is *not* a passive
impedance transformer + L72 LP filter as previously documented — it
is L72 LP filter + a DC-blocked MAR-8 (top-mark `A08`)
IF post-amp on a 195 Ω +15 V bias R, contributing ~+32 dB of gain
at 100 MHz**. Both active stages (A212 in-casing and A08 on-A211)
must be powered for any meaningful S21 read. The §7.4.2 +27 dB
passband spec is therefore most plausibly the **combined A212 + A08
chain gain**, not the A212 alone as previously written; closing the
attribution requires re-reading p.145 §7.1.5 / §7.1.6 (pending).

Two valid configurations:

1. **Full chain, casing in place (preferred for §7.4.2 numeric spec)**
   — instrument on, X72 / VA15-IF live (powers A212), +15 V analog
   live (powers A08 via the 195 Ω bias R), X50 / X211 disconnected
   (or their drives dead) so no active LO/RF reaches the mixer.
   Connect VNA port 1 to **a small injection coupler / DC-block
   tap at the A212 IF-amp input inside the casing** (or, if no such
   tap exists, inject at the mixer-IF node by lifting the
   appropriate casing pin), port 2 → X75 on A211. *In practice this
   is awkward — most users skip the +27 dB numeric and run config 2
   instead.*

2. **On-A211 IF path only (A08 active, A212 bypassed)** — instrument
   **on** (so the +15 V analog rail biases A08 through the 195 Ω
   bias R), X70 and X75 cables disconnected at A211, X50 / X211
   disconnected so no LO/RF reaches the mixer (A212's drive
   irrelevant once X70 is broken). VNA port 1 → X70 (A211 side, now
   driving directly into L72), port 2 → X75, VNA output −30 dBm to
   keep A08 well below its +12.5 dBm P1dB at the input, S21 from 1
   to 300 MHz. This exercises **L72 LP filter + DC-block cap +
   A08 MAR-8 + output DC-block cap** between X70 and X75. Expected:

   - 10–80 MHz: |S21| ≈ **+31 … +32 dB** (MAR-8 datasheet gain at
     100 MHz, less a small L72 + DC-block insertion loss)
   - 105–110 MHz: |S21| dips to roughly the A08 gain minus the L72
     notch depth (notch is on A08's input, so the LP rejection
     stacks with A08's flat-band gain — net |S21| **< 0 dB**, often
     well below)
   - 240–300 MHz: |S21| < 0 dB (2nd LP rejection minus A08 gain
     roll-off — A08's 3 dB BW is ~1 GHz so it's still amplifying)

   **Earlier-revision config-2 expectations (|S21| ≈ 0 dB in the
   passband, instrument-off measurement) were wrong** under the
   pre-2026-04-29 reading that the X70 → X75 path was passive.
   Anyone running an instrument-off |S21| measurement on this path
   will see ≪ 0 dB transmission across the band as A08 is unbiased
   and its collector-emitter path presents near-OL to the IF — that
   reading was a doc gap, not an A08 fault.

Pass (config 2 under the revised expectations) clears the on-PCB IF
path including A08's gain stage. The casing-internal A212 IF amp is
exercised end-to-end by Step 9's X75 re-read, so a Step 9 pass + a
Step 10 config-2 pass together cover the full path from casing-IF
input through to X75. If X21 / X75 are at spec and TP1910 remains
low, continue to Step 11.

Passband gain low (config 2, |S21| in the passband well under +28 dB)
→ A08 MAR-8 fault (failed MMIC, open 2 × 392 Ω parallel bias R,
broken pour bond on pin 2/3 GND, or open input/output DC-block cap)
— this is **field-serviceable**, modern drop-in MAR-8A+ on the
existing 2 × 392 Ω parallel pair. LP notch missing or mis-centred →
L72 ferrite-core trim (rotate so the 1st attenuation peak lands at
103 MHz, per §7.4.2).

### Step 10a — On-A211 IF chain, bench-PSU standalone *(VNA / SA, board out, no casing, no LO)*

> **Ordering:** runnable **before §7E rebuild**, in the same bench
> session as 8a. No dependence on the LO side — exercises only the
> +15 V trace + A08 + L72 + DC-block caps. Pass exonerates the
> on-A211 IF chain regardless of D.5 / D.6 outcome on the LO side.

Bench-PSU variant of Step 10 config 2. Same |S21| measurement, but
the A211 PCB is **out of the milled casing and off the
backplane** — powered from external bench supplies via W216 alone.
Exercises the full X70 → X75 path (**L72 LP filter → input DC-block
cap → A08 MAR-8 → output DC-block cap**) with zero dependence on
the casing, the LO chain, the supervisor, the rest of the
instrument, or any of the still-pending §7D/§7F/§7G rebuild work.
Runs in ~15 min and can be done **before** the LO-side rebuild,
giving an early A08 / L72 / +15 V trace verdict while the board is
already out for rework.

**Power rails needed (revised 2026-04-29 after bench bias-trace):**

- **+15 V analog at W216.1** — the only rail required. Bench-traced
  end-to-end from W216.1 → 2 × 392 Ω in parallel → A08 pin 4,
  un-gated by any supervisor / V85 / V89 cut-off switch. Steady-state
  draw is the A08 quiescent current alone, ≈ 36.9 mA. Bench supply
  current limit: 100 mA initial, relax once stable.
- **GND at the W216 ground pin(s)** — single-point reference from
  the bench supply to the A211 GND pour.

**Rails NOT needed for this test:**

- **−15 V** is *not* required. A08's bias path is single-supply
  +15 V; no negative rail enters the X70 → X75 chain. The LP365M
  supervisor *may* trip its wired-OR fault node on missing −15 V,
  but the supervisor's cut-off switches do **not** gate the A08
  bias rail (the 2 × 392 Ω pair sits directly on the un-gated
  W216.1 +15 V), so a tripped supervisor does not affect this test.
- **+5 V** — not present on A211 in any bench-confirmed form;
  earlier suggestion was unfounded. Skip.
- **+7.5 V (W216.4)** — biases the §7F 420 NPN cascade ("420" chips)
  on the LO side; irrelevant to the IF chain. Skip.

**Procedure:**

| # | Step                                                                                                                           |
|---|--------------------------------------------------------------------------------------------------------------------------------|
| 1 | A211 board out. W216 accessible.                                                                                                |
| 2 | Wire bench supply to W216.1 (+15 V) and W216 GND (per closed mapping).                                                          |
| 3 | Bring up rails: GND first, then +15 V at 200 mA limit. Record steady-state I — bench-verified **≈ 105 mA** on this unit (A08 + on-board PNP / supervisor / divider loads; the earlier "≈ 37 mA, A08 quiescent only" figure assumed A08 alone and is superseded by the 2026-05-05 run). |
| 4 | DMM at A08 pin 4: confirm ≈ +7.8 V to GND. If 0 V → bias R / +15 V trace open. If ≈ +15 V → A08 dead or pin 2/3 GND bond open. |
| 5 | VNA port 1 → X70, port 2 → X75. VNA output **−30 dBm**.                                                                         |
| 6 | Sweep |S21| 1 → 300 MHz. Capture trace.                                                                                        |
| 7 | Power-down: +15 V off, GND last.                                                                                                |

**Expected |S21|** (same as Step 10 config 2; revised against MAR-8
datasheet 2026-05-05 — the schematic identifies V75 as **MAR-8**):

- 10–80 MHz: **≈ +31 … +32 dB** (MAR-8 datasheet gain at 100 MHz
  for V_d 7.5 V / I_d 36 mA, less a small L72 + DC-block in-band
  insertion loss)
- 105–110 MHz: deep notch (L72 LP rejection stacks with MAR-8
  flat-band gain — net **≪ 0 dB**)
- 240–300 MHz: < 0 dB (2nd LP rejection minus MAR-8 roll-off)

**Outcome localization** (thresholds revised 2026-05-05 against the
MAR-8 datasheet expectation):

| Result                                                | Reads                                                                                                                                                         |
|-------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Passband ≥ +28 dB (within ~4 dB of MAR-8 datasheet), L72 notch in place | A08 (MAR-8) + L72 + both DC-block caps + 2 × 392 Ω pair + W216.1 → pin 4 +15 V trace + A08 pin 2/3 GND bond all healthy. X70 → X75 path exonerated; suspect casing or LO chain. |
| Passband +5 … +28 dB (≥ ~4 dB below datasheet, still gaining) | A08 alive but lossy: leaky output DC-block, low-Q L72 input cap, or detuned X75-side match.                                                              |
| Passband flat near 0 dB, no clear gain or notch       | A08 dead; signal coupling around package via parasitic capacitance. Replace with MAR-8A+ on the existing 2 × 392 Ω pair.                                     |
| Passband ≪ −20 dB                                     | A08 cut off (gone, or no +15 V at pin 4). Re-run step 4: if pin 4 ≠ +7.8 V despite +15 V at W216.1, the +15 V trace or one of the 392 Ω resistors is open.   |
| Notch missing or off-centre, passband OK              | L72 ferrite-core trim drifted. Rotate per §7.4.2 to land 1st attenuation peak at 103 MHz.                                                                    |

**Notes:**

- VNA drive at −30 dBm keeps the A08 input ≪ +12.5 dBm P1dB; at
  0 dBm or higher A08 compresses and the passband reads low.

Pass at this step is functionally equivalent to a Step 10 config-2
pass (it covers the same components) and exonerates the on-A211 IF
path, leaving the casing-internal stages (A212/sampling-mixer/A214)
as the only remaining suspects on the IF side.

**Run results — this unit (2026-05-05; A211 PCB out of casing,
+15 V bench PSU on W216.1 + GND, VNA drive −30 dBm at port 1, 10 dB
in-line attenuator on port 2 de-embedded by thru-cal, sweep 30 kHz
→ 300 MHz, S21 log MAG 10 dB/div, REF 0 dB):**

- **+15 V steady-state I = 105 mA** (vs. the pre-revision "≈ 37 mA
  A08 quiescent only" expectation — superseded above; the bench
  reality includes loads beyond A08 sitting on the un-gated +15 V
  rail with the LO half partially biased through its base / collector
  networks even with −15 V absent).

| Marker | f                | \|S21\|         | Notes                                                       |
|--------|------------------|-----------------|-------------------------------------------------------------|
| M1     | 10 MHz           | **+31.41 dB**   | passband low corner                                         |
| M3     | 45 MHz           | **+31.531 dB**  | passband mid                                                |
| M2     | 80 MHz           | **+31.553 dB**  | passband upper, peak in band                                |
| M4     | 103.040 696 MHz  | **−39.482 dB**  | L72 LP notch (§7.4.2 places 1st attenuation peak at 103 MHz)|
| M5     | 240 MHz          | **−56.481 dB**  | far stopband                                                |

Trace shape: passband 10–80 MHz flat at +31.4 … +31.55 dB (~0.15 dB
ripple), sharp roll-off starting ~95 MHz into the L72 notch at
103 MHz (−39.5 dB), partial recovery to ~−13 dB around 140 MHz,
then declining into broadband noise floor toward 300 MHz.

Maps to the **outcome row "Passband ≥ +28 dB, L72 notch in place"**
→ A08 (MAR-8) + L72 LP filter + both DC-block caps + 2 × 392 Ω
bias pair + W216.1 → A08 pin 4 +15 V trace + A08 pin 2/3 GND bond
all healthy. **X70 → X75 on-A211 IF path EXONERATED.** On the IF
side this leaves only the casing-internal A212 / sampling-mixer /
A214 chain as a suspect.

The LO half of A211 (X50 → X21 chain) has **not** yet been RF-
validated — §7D D.5 (2026-05-03) was a DMM ohm cross-check of the
LO-amp bias network and chip C-E topology, not an RF test. The
chips-alive verdict from D.5 still needs corroboration by **Step 8a**
(bench-PSU LO chain, board out, SA at X21) or **Target 4** (in-
instrument R65 split-test) before the LO half can be called
exonerated. **Next bench action is therefore Step 8a or Target 4
on the LO side**; Step 8b (milled-casing standalone) follows once
both halves of A211 are RF-cleared, isolating the casing as the
sole remaining suspect.

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
- [p.152 — Parts XY-list (drawing 1035.8840.01 XY)](rs_smp_corpus/volumes/band-3/pages/p0152_page0152.md) — physical positions of N80, V85/89/90/95, R98, X95/X96 for Step 7 / Step 8 / Step 11
- [p.156 — *Sampling Modul* schematic (drawing 1035.8840.01, valid for Var.02)](rs_smp_corpus/volumes/band-3/pages/p0156_page0156.md) — A211 schematic explicitly cited by §7.4.1; required for Step 7 (comparator nodes) and Step 8 (doubler / LO-amp localisation)
- Full section (DE+EN): [band-3 §7 A21 Sampling Module](rs_smp_corpus/volumes/band-3/sections/03_ch7-a21-sampling-module.md)
