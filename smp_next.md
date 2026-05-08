# smp_next.md — A21 / A211 next-bench-session tracker

Companion to `smp_hw_diag.md`. Tracks the LDMOS replacement plan
(V3/V4 fault confirmed 2026-05-08) and remaining deferrable bench
tasks. Full diagnostic history in `smp_hw_diag.md` + `smp_history.md`.

> **Historical / superseded content** is moved to
> [`smp_history.md`](smp_history.md). Inline supersession markers in
> this doc point to specific anchors there. The doc body itself
> always reflects current truth.


## Sourcing — §7E Replacements

Silicon-pull rebuild is **now required** (Step 8a FAILED 2026-05-08).

**Preferred approach (2026-05-08):** replace the V3/V4 MRF3866/MRF5160
push-pull pair (and possibly the BFG97 pre-driver) with a **single
LDMOS gain block** — avoids the mechanical difficulty of fitting TO-39
cans onto SO-8 pads. BFG97 confirmed working during Step 8a; keep it
as the pre-driver feeding the LDMOS replacement.

Primary candidate (**on hand**):

- **AFT05MS003NT1** — NXP Airfast wideband RF power LDMOS, SOT-89,
  1.8–941 MHz, 3 W CW, P1dB +38.4 dBm, Vdd 7.5 V / Idq 100 mA.
  Integrated stability enhancement, designed for unmatched I/O.
  Datasheet gain: 20.8 dB @ 520 MHz narrowband (tuned circuit);
  **17.1–17.5 dB @ 136–174 MHz VHF broadband (matched);
  15.1–15.5 dB @ 350–520 MHz UHF broadband (matched).**
  At 220 MHz unmatched, expect **~15–17 dB** — significantly less
  than the 20 dB narrowband figure. Gain budget is tight: whether
  the LDMOS alone reaches +26…+30 dBm depends on the BFG97 output
  level, which has not been directly measured (see budget table).
  A predriver stage between BFG97 and the LDMOS may be needed.
  Available on the +7.5 V rail (W216.4).

Alternative MMIC (**if LDMOS stability proves problematic**):

- **PMA3-43-1W+** — Mini-Circuits GaAs MMIC PA, 3×3 QFN-12,
  10–4000 MHz, P1dB +32.2 dBm, Psat +32.6 dBm, gain 21 dB,
  50 Ω internally matched (no external matching needed),
  Vcc +12 V / 190 mA. Needs breakout board + LDO or series R from
  +15 V. ~$18/pc. Unconditionally stable by design.

Legacy like-for-like substitutes (retained for reference, lower
priority due to TO-39 → SO-8 mechanical difficulty):

- **2N3866** (NPN, TO-39) — on hand. Leg-dress to SO-8.
- **2N5160** (PNP, TO-39) — Jotrin / Radio741 NOS.
- **NTE2511 / NTE2512** — NTE direct crosses, TME / Newark.

## Replacement plan — AFT05MS003NT1 gain-block substitution

Added 2026-05-08. Replaces the V3/V4 MRF3866/MRF5160 push-pull PA
with a single AFT05MS003NT1 LDMOS on a small lab PCB. BFG97
pre-driver retained.

### Signal chain (existing → replacement)

```
Existing (broken):
  BFG97 col (~+14…+17 dBm est.) → commoned V3/V4 bases
  → push-pull PA (10–13 dB gain) → L45/C49 → X21 (+26…+30 dBm)

Replacement:
  BFG97 col (~+14…+17 dBm est.) → C_dc → R_gate → AFT05MS003NT1
  → C_dc → X21 (target +26…+30 dBm)
```

### Gain / power budget

**⚠ BFG97 output level is estimated, not measured.** Back-calculated
from Step 8a (X21 = 23–24 dBm while V3/V4 were degrading) and
MRF3866/MRF5160 datasheet min 10 dB gain → push-pull ~10–13 dB →
BFG97 ≈ +14…+17 dBm. **Needs bench verification** with low-cap
probe on BFG97 collector during lab PCB bring-up.

```
┌────────────────────────┬───────────────────────────────────────┐
│ Parameter              │ Value                                 │
├────────────────────────┼───────────────────────────────────────┤
│ BFG97 output           │ ~+14…+17 dBm @ 220 MHz (ESTIMATED)   │
│ R_gate loss             │ −1…−3 dB (depends on value chosen)   │
│ LDMOS gain @ 220 MHz   │ ~13–16 dB (unmatched, estimated from │
│   (unmatched, all-in)  │  17 dB matched datasheet minus I/O   │
│                        │  mismatch — no separate deduction)    │
│ LDMOS output            │ +24…+30 dBm (optimistic)             │
│                        │ +20…+24 dBm (pessimistic)             │
│ Target at X21           │ +26…+30 dBm                          │
│ P1dB @ 7.5 V           │ +38.4 dBm                            │
├────────────────────────┼───────────────────────────────────────┤
│ VERDICT                │ Marginal. Optimistic end reaches      │
│                        │ target. Pessimistic end is 2–6 dB     │
│                        │ short. Predriver may be needed —      │
│                        │ decide after lab PCB bring-up.        │
└────────────────────────┴───────────────────────────────────────┘
```

**If gain is insufficient**, options (decide after lab PCB bring-up):

1. **Add a predriver** between BFG97 and AFT05MS003NT1 — needs
   to deliver ~+12…+16 dBm to the LDMOS gate. Options:
   GALI-84+ (P1dB +21.3 dBm, gain ~12 dB, SOT-89 — same
   footprint as AFT05MS003NT1, plenty of headroom), MAV-11SM+
   (P1dB +17.5 dBm, gain ~12 dB, SOT-86 — adequate for this
   drive level), or a discrete stage (BFG97 / 2N3866 class A).
2. **Add input/output matching** to the AFT05MS003NT1 — recovers
   3–6 dB of mismatch loss, may be enough without a predriver.
3. **Use the PMA3-43-1W+ MMIC** instead (21 dB gain, internally
   matched, 50 Ω — no matching or predriver needed, but needs
   +12 V supply).

Output power is adjusted by Vdd (reduce gain + Psat together) —
but only useful if the budget has margin. If budget is tight,
run at full Vdd 7.5 V and rely on the P1dB headroom.

### Lab PCB layout

```
                          Vgg (bench PSU, ~2.5–3.5 V)
                            │
                       R_bias (100 Ω ¼W, or 2 × 22 Ω 1/10W series)
                            │
SMA in ── C_dc ── R_gate ── GATE    DRAIN ── RFC ── Vdd (bench PSU)
                                      │         │
                                     C_dc    100nF ┤├ GND
                                      │      10µF ┤├ GND
                                   SMA out
```

SOT-89 footprint, ground plane on back, short traces, SMA edge-launch
connectors. R_gate on a 0805 pad for easy swapping. Gate bias via
R_bias (100 Ω per datasheet) from a separate bench PSU (Vgg) to set
Idq ≈ 100 mA at the chosen Vdd. The RF input couples through C_dc
onto the gate bias point. Vdd also adjustable on bench PSU — start
low (3 V), sweep up to find the operating point for +26…+28 dBm
output.

### Bring-up sequence

```
┌────┬───────────────────────────────────────────────────────────┐
│  # │ Step                                                      │
├────┼───────────────────────────────────────────────────────────┤
│  1 │ Assemble lab PCB. R_gate = 47–100 Ω initial (high, for   │
│    │ stability margin). Bypass caps close to drain pad.        │
├────┼───────────────────────────────────────────────────────────┤
│  2 │ No RF in. Vdd = 3 V. Check Idd quiescent (~100 mA at     │
│    │ nominal Idq bias). Watch for oscillation on scope /       │
│    │ wideband SA.                                              │
├────┼───────────────────────────────────────────────────────────┤
│  3 │ Apply 220 MHz CW. Start at 0 dBm, sweep up to +15 dBm    │
│    │ (simulating BFG97 range). At each drive level, sweep Vdd  │
│    │ (3 → 5 → 7.5 V). Record gain vs Pin and Vdd. This        │
│    │ characterises whether the LDMOS alone can reach target.   │
├────┼───────────────────────────────────────────────────────────┤
│  4 │ If output reaches +26…+28 dBm at some Pin/Vdd combo →    │
│    │ that is the operating point. If not → predriver needed    │
│    │ (see gain budget "options" above).                        │
├────┼───────────────────────────────────────────────────────────┤
│  5 │ At that Vdd, check for out-of-band oscillation: wideband  │
│    │ SA sweep 1 MHz – 1 GHz, scope on drain. Vary input power  │
│    │ from −10 dBm to +10 dBm — confirm no parametric           │
│    │ oscillation under varying drive.                          │
├────┼───────────────────────────────────────────────────────────┤
│  6 │ If stable: reduce R_gate (47 → 22 → 10 → 0 Ω) to find   │
│    │ the minimum value that maintains unconditional stability.  │
│    │ Lower R_gate = less input loss = more gain budget.        │
├────┼───────────────────────────────────────────────────────────┤
│  7 │ If unstable at any point: increase R_gate, add small      │
│    │ drain-to-gate feedback R (470 Ω–1 kΩ), or add ferrite    │
│    │ bead on drain bias feed. Re-check from step 5.            │
├────┼───────────────────────────────────────────────────────────┤
│  8 │ Record final: Vdd, R_gate, Idd, gain @ 220 MHz, Pout     │
│    │ @ +15 dBm drive, any spurs. These are the integration     │
│    │ parameters for the A211 bodge.                            │
└────┴───────────────────────────────────────────────────────────┘
```

### Integration into A211

After lab PCB characterisation, the final bodge connects into the
existing A211 signal chain:

- **Input:** pick up the BFG97 collector signal at the existing
  V3/V4 commoned base node (or at the BFG97 collector pad directly).
  Short coax or wire to the lab PCB input SMA.
- **Output:** connect lab PCB output SMA to the existing L45/C49
  output match pads (if intact) or directly to X21. The comb
  generator S11 is already poor (2.3–7.6 dB RL measured 2026-05-08),
  so no additional output matching needed.
- **Supply:** Vdd from W216.4 (+7.5 V) through a series R or small
  LDO to the operating voltage found in step 4. If operating Vdd
  is close to 7.5 V, a direct connection with just the bypass
  caps may suffice.
- **Decommission V3/V4 bias:** with V3/V4 desoldered, the ±15 V
  base-bias paths (R43/R44 + L41/L43) and emitter paths (R40/R41)
  are open — no current draw, no interference. Leave as-is.

## Files / sections to read on session resume

- `smp_hw_diag.md` §7E rebuild steps 2 / 2a — **now unblocked**.
- `smp_hw_diag.md` Step 8a/8b run results (2026-05-08) — V3/V4
  failure confirmed, casing exonerated.

## Status

Completed / superseded items moved to `smp_history.md`.
Bench diagnostic session (D.5, Step 10a, Step 8a, Step 8b) all done
2026-05-03 / 2026-05-05 / 2026-05-08. Result: V3/V4 PA = root cause;
doubler, BFG97, IF chain, milled casing all healthy.

```
[ ] (5) AFT05MS003NT1 lab PCB bring-up — build SOT-89 test
    board with SMA in/out, R_gate (start 47–100 Ω), drain
    bypass caps. Characterise at 220 MHz: sweep Vdd 3–7.5 V,
    find operating point for +26…+28 dBm output, check
    stability. See "Replacement plan" section above.
[ ] (6) Integrate into A211 — connect lab PCB between BFG97
    collector and X21 (via existing L45/C49 or direct). Vdd
    from W216.4 (+7.5 V) via series R or LDO to operating
    voltage from step 5. Re-run `--a21-probe` to verify
    TP1910 climbs to 7.5–11 V and X75 comes alive.
[ ] Re-read band-3 p.145 §7.1.5 / §7.1.6 + p.146 §7.4.2 to
    nail down the §7.4.2 +27 dB gain attribution (A212 alone
    vs. A212 + A08 combined chain) — non-blocking
[ ] Schematic re-read open items 2026-04-30 — see
    "Comparator inputs + X21 last stage" planning block below.
    [ ] Find the still-fitted N80 input-divider stub destination
    [ ] Trace the X21 last stage past L45/C49 (off-image strip)
    [ ] Resolve the VARSAMP divider mismatch (R30 = 8K25 read?)
[ ] X95 / X96 / V95 / R98 bias-network re-trace 2026-04-30 — see
    "Target 3 — X95 / X96 bias-network topology re-trace" below.
    [ ] Locate R98 (sub-Ω SMD) on the +V_unreg → BUZ71-D path
    [ ] Identify the two "4F" SOT-23s on the X95 fan-out
    [ ] Decide α vs β (see Target 3 section)
    [ ] Search for V95 ("A0" SOT-23) upstream of X95 brass pin
    [ ] Coordinated §7C / §7B edit pass once trace is complete
```

## Deferrable bench-trace targets (Targets 1–3)

Three areas of the recovered Var.02 schematic still need bench
follow-up (added 2026-04-30, deferrable — none gate the LDMOS
replacement).

### Target 1 — N80 input-divider stub (CONTROL-/BIAS C block)

Per the §7D DEEPER SCHEMATIC RE-READ banner item 3 in
`smp_hw_diag.md`, the LP365M comparator chip itself (N80-E),
its input-divider ladder R80–R85, and the ISET R109 are all
marked N.F. on this Var.02. **What remains populated** is a
divider stub:

```
+15 V (VR15-P)
   │
   ├── R102 100 K ── (node X) ── R103 56 K2 ── ?
   │
   └──  ...  R86 100 K ── R87 61 K9 ── R88 3 K92 ── −15 V (VR15-N)
```

Open questions:

```
+---+-----------------------------------------------------------+
| # | Question                                                  |
+---+-----------------------------------------------------------+
| 1 | Where does the R102 / R103 mid-tap go on the actual PCB?  |
|   | On the schematic it would feed an LP365M input — which is |
|   | depopulated. The trace must terminate somewhere physical: |
|   | (a) deadhead test pad, (b) re-purposed sense node for      |
|   | something else on Var.02, (c) actually tied to a populated |
|   | downstream component the schematic shows as N.F.           |
| 2 | Same question for the R86 / R87 / R88 chain on the −15 V  |
|   | leg (still populated — would have set the LP365M low-      |
|   | window threshold on the populated variant).                |
| 3 | Whether **any** of the four LP365M outputs has a populated |
|   | downstream load (the wired-OR / V85 / V89 cut-off chain    |
|   | all schematic-N.F. — but a single output could feed an     |
|   | LED, a CMOS gate, etc. as a leftover monitor).             |
+---+-----------------------------------------------------------+
```

Bench plan (instrument off, A211 in or out — non-destructive):

```
+---+-----------------------------------------------------------+
| # | Probe                                                     |
+---+-----------------------------------------------------------+
| 1 | DMM ohm: R102 / R103 mid-tap pad → nearest test pad,     |
|   |   nearest LP365M input pin footprint (4, 5, 6, 9 of N80   |
|   |   per LP365M-L pinout), and the W216 header pins.         |
| 2 | DMM ohm: R86 / R87 / R88 mid-tap pad → same set as #1.    |
| 3 | Visual + multimeter buzz: from each of the four LP365M    |
|   |   output pins (1, 2, 13, 14 of N80) trace to wherever the |
|   |   PCB takes them (probable: deadhead at the chip pad on   |
|   |   this variant; possible: a single LED + R footprint).    |
| 4 | Instrument-on DC voltage at the R102 / R103 mid-tap and   |
|   |   the R87 / R88 mid-tap, with `--a21-probe` running. The  |
|   |   schematic predicts ≈ +5.4 V (R103 / (R102+R103) × 15 V) |
|   |   and ≈ −14.1 V respectively — divergence implies the     |
|   |   trace is loaded by something else on the actual PCB.    |
+---+-----------------------------------------------------------+
```

### Target 2 — X21 last stage (off-image right margin of sheet)

Per banner item 2: the V3 / V4 collectors tie together, feed
**L45 54 nH + C49 10 P** as the output match, and exit the
LO-AMPLIFIER block to the right; the X21 connector itself, the
DIAGSAMP rectifier, and the W216.10 termination are **not visible**
on the available JPEG (right margin appears cropped). Same for
the comparator outputs of N80, which also disappear past the
right edge.

Open questions:

```
+---+-----------------------------------------------------------+
| # | Question                                                  |
+---+-----------------------------------------------------------+
| 1 | Is the JPEG cropped (most likely) or is the column-9      |
|   | strip genuinely missing on the sheet?  → re-scan the      |
|   | original PDF / hard copy at full sheet width.             |
| 2 | What is the DC-block / bias topology between L45 / C49    |
|   | and the X21 brass pin?  (Bench tracing has C49 as the     |
|   | DC-block, then a passive cap pickoff that taps the X21    |
|   | RF tap node and feeds an "A0" SOT-23 Schottky → 10 kΩ →   |
|   | shunt cap → W216.10 — unconfirmed against schematic.)     |
| 3 | Where exactly does W216.10 (DIAGSAMP) join the W216       |
|   | header on the schematic?  The visible W216 connector      |
|   | enumerates pins 1–9 only; is W216.10 drawn on the off-    |
|   | image strip, or on a different sheet (sheet says 02/02 —  |
|   | this is supposed to be the last sheet)?                   |
| 4 | Are there any **other** components on the X21 net beyond  |
|   | the bench-traced rectifier — e.g. an X21-side AC clamp,   |
|   | a load resistor for the L45 / C49 match, or a bias-tee    |
|   | for an LO sense return?                                   |
+---+-----------------------------------------------------------+
```

Bench plan (instrument off):

```
+---+-----------------------------------------------------------+
| # | Probe                                                     |
+---+-----------------------------------------------------------+
| 1 | Re-scan or re-photograph sheet 02/02 of drawing             |
|   |   1035.8840.01 at full sheet width (right edge of A3) —    |
|   |   covers questions 1, 3, 4.                                |
| 2 | DMM ohm: V3 / V4 collector tie → X21 brass pin at the     |
|   |   PCB.  Expected behaviour:                                |
|   |   - DC OL through C49 10 P (DC-block)                      |
|   |   - sub-Ω at the cold side of L45 (= V3/V4 collector tie)  |
|   |   - whatever the X21-side network presents (passive A0     |
|   |     cathode is GND, so X21 → A0 anode → A0 cathode = GND   |
|   |     should read OL through the diode in reverse and a few  |
|   |     hundred mV in the diode-test-forward direction).       |
| 3 | DMM ohm: X21 brass pin → W216.10 with the bench-traced     |
|   |   "A0 + 1002 + cap" path expected — should read 10 kΩ +    |
|   |   parallel-cap-leakage on a slow ramp (RC charge curve     |
|   |   on the DMM during the read).                             |
| 4 | DMM ohm: W216.10 conductor on the cable (already done in  |
|   |   §1 Step 2 — confirmed conducting under load).            |
| 5 | Instrument-on AC: scope at the X21 brass pin (low-cap     |
|   |   probe) under `--a21-probe` — the LO is dead on this     |
|   |   unit so this is a confirmation rather than a level       |
|   |   measurement; can be combined with Step 8a SA capture.   |
+---+-----------------------------------------------------------+
```

### Sequencing

Targets 1–3 are **deferrable** — they do not block the LDMOS
replacement. Best run **opportunistically** during the next
out-of-casing session (e.g. during LDMOS integration).

### Target 3 — X95 / X96 bias-network topology re-trace

Added 2026-04-30 from a Side-B trace session that contradicts
the §7C Table B and §7B layout-list wording in `smp_hw_diag.md`.
The §7C bias-chain decision matrix still PASSED end-to-end on
this unit (X95 / X96 in spec, OP97 mid-rail, BUZ71 in active
region, I_drain ≈ 74 mA), so this is a **documentation-topology
correction, not a fault investigation** — same class of cleanup
as the §7D V95 OPEN item.

Findings already on the bench (2026-04-30):

```
+----+----------------------------------------------------------+
| #  | Bench observation                                        |
+----+----------------------------------------------------------+
| F1 | X96 brass pin lands directly on BUZ71 source pin.        |
|    | NO discrete SMD between BUZ71-S and X96.                 |
+----+----------------------------------------------------------+
| F2 | R98 (≈ 0.1 Ω current-sense) is therefore NOT in series   |
|    | between BUZ71-S and X96, contradicting `smp_hw_diag.md`  |
|    | line 388 + lines 390–393 + §7C Table B row 5 wording.    |
|    | R98 location currently unknown on this unit (could not   |
|    | be located in the same trace session).                   |
+----+----------------------------------------------------------+
| F3 | OP97 (N90) pin 3 (+) lands on BUZ71 drain pin.           |
|    | Combined with F1/F2, this is consistent with a high-     |
|    | side current-source topology with R98 between +V_unreg   |
|    | and BUZ71 drain (pin 3 sensing the BUZ71-drain side of   |
|    | R98). The current `smp_hw_diag.md` line 380–382 wording  |
|    | only specifies pin 6 (out → BUZ71 G) and pin 2 (− →      |
|    | X96 side of R98); pin 3 is implied as a divider          |
|    | reference but never explicitly bench-confirmed before.   |
+----+----------------------------------------------------------+
| F4 | X95 brass pin → series passive network (some R + some D) |
|    | → fans out to TWO SOT-23, both top-marked "4F".          |
|    | Contradicts the §7C Table B row 6 / row 7 + §7D V95      |
|    | OPEN item assumption that V95 is a single "A0" SOT-23    |
|    | sitting on / generating the X95 rail.                    |
+----+----------------------------------------------------------+
| F5 | Schematic scan 2026-04-30 of sheet 02/02 for the +7,5V   |
|    | net: enters at W216.4, passes L22 supply-block filter +  |
|    | decoupling caps, exits as labeled net "+7,5V" running    |
|    | right, and DOES NOT visibly terminate anywhere on this   |
|    | sheet (FREQUENCY DOUBLER / LO AMPLIFIER / IF / CONTROL-  |
|    | BIAS-C blocks all sit on VR15-P / VR15-N rails, not on   |
|    | +7,5V). N90 (OP97) is on this sheet but V90 (BUZ71),     |
|    | R98, X95, X96 are not — the whole regulator sub-block    |
|    | lives on sheet 01/02 (NOT in the recovered corpus).      |
|    | Most-likely reading consistent with the bench (W216.4    |
|    | = +7.55 V, X96 = +6.18 V at BUZ71-S directly): the on-   |
|    | board "+7,5V" net is the +V_unreg input to the BUZ71     |
|    | regulator on sheet 01/02. See §7D banner + filed         |
|    | 2026-04-30 doc-vs-schematic mismatch flag.               |
+----+----------------------------------------------------------+
```

Open questions:

```
+---+-----------------------------------------------------------+
| # | Question                                                  |
+---+-----------------------------------------------------------+
| 1 | Where does R98 actually sit?  Hypothesis from F1+F3:      |
|   | between +V_unreg input rail and BUZ71 drain (high-side    |
|   | current-sense). Three candidate positions a/b/c per       |
|   | session log: (a) drain-side (favored), (b) downstream of  |
|   | X96 in load path, (c) in OP97 feedback only (would        |
|   | falsify the I = V_R98 / R98 = 74 mA reading in row 5).    |
| 2 | What is "4F" as an SMD top-mark?  Strongest candidate is  |
|   | BCW68F (Infineon SOT-23 PNP small-signal, 45 V, gain      |
|   | bin F); MMBT3906-class PNPs are also stamped "4F" on      |
|   | some date codes. Whatever it is, "4F" is a Si BJT, NOT    |
|   | a GaAs FET and NOT a Schottky diode.                      |
| 3 | Are the two "4F" SOT-23s V85 / V89 themselves             |
|   | (interpretation α — V85 / V89 are Si PNPs on this Var.02, |
|   | NOT A214 GaAs FETs as currently in §7B / §7D), or are     |
|   | they a separate bias generator upstream of the actual     |
|   | cascade amp (interpretation β — V85 / V89 are still       |
|   | downstream and the 4F pair drives them)?                  |
| 4 | Where is V95 ("A0" SOT-23) physically?  Two options:      |
|   | (i) upstream of the X95 brass pin (between whatever       |
|   | generates the bias and the brass pin) — would make V95    |
|   | a clamp diode on the X95 rail, matching §7D OPEN          |
|   | reading (i); (ii) doesn't exist as a discrete part on     |
|   | Var.02 — X95 rail is generated by a passive divider from  |
|   | one of the supply rails, no V95 anywhere.                 |
| 5 | What does OP97 pin 2 (−) actually connect to?  Current    |
|   | doc (line 382) says "pin 2 ties to the X96 side of R98"   |
|   | — but with R98 on the drain side, pin 2 must be on the    |
|   | reference side instead. Re-trace pin 2 copper to confirm. |
+---+-----------------------------------------------------------+
```

Bench plan (instrument off; A211 in or out — non-destructive):

```
+---+-----------------------------------------------------------+
| # | Probe                                                     |
+---+-----------------------------------------------------------+
| 1 | Visual scan of the +V_unreg input copper from N90 power   |
|   |   pin / BUZ71 drain pad, looking for a sub-Ω 0805/1206    |
|   |   SMD marked "R100" / "0R10" / "100" with milliohm        |
|   |   decimal — that's R98. Measure DC across it; expect      |
|   |   ≈ 7.4 mV at the §7C row 5 reading.                      |
| 2 | DMM continuity: confirm OP97 pin 2 (−) trace destination. |
|   |   Should land on the reference-side of R98 (high side, on |
|   |   +V_unreg) under the high-side current-source            |
|   |   hypothesis, or somewhere on the 750 Ω / 10 kΩ ladder.   |
| 3 | Microscope read of BOTH "4F" SOT-23s' full top-mark       |
|   |   (count characters: 2 = pure "4F" → BCW68F-class PNP;    |
|   |   3 = "4Fx" → other variants). Note manufacturer logo if  |
|   |   visible.                                                |
| 4 | DMM continuity on each "4F" SOT-23: which pad → X95,      |
|   |   which → GND, which → +V_unreg / +15 V / other rail.     |
|   |   Confirm whether the two are wired identically (parallel |
|   |   / matched pair) or rotated (complementary pair).        |
| 5 | Count + identify the "R + D" series elements between the  |
|   |   X95 brass pin and the 4F pair: how many R, what value;  |
|   |   how many D, what marking, what polarity. Determines     |
|   |   whether X95 is feeding bias INTO the 4F pair (X95 →     |
|   |   base/gate) or being generated BY them (collector/drain  |
|   |   → X95).                                                 |
| 6 | Visual + DMM: search for any SOT-23 marked "A0" on the    |
|   |   upstream side of the X95 trace (between the brass pin   |
|   |   and the +15 V / −15 V supply rails). If found → V95     |
|   |   exists as a clamp diode (§7D OPEN reading (i)); if not  |
|   |   found anywhere on the X95 / supply traces → V95 doesn't |
|   |   exist as a discrete part on Var.02 (new resolution).    |
| 7 | (instrument on, `--a21-probe` running) DMM at the BUZ71   |
|   |   drain pad: under the drain-side R98 hypothesis with     |
|   |   +V_unreg = on-board "+7,5V" net (per F5 schematic       |
|   |   scan), should read **≈ +7.49 V** (= W216.4 nominal      |
|   |   +7.55 V minus 7.4 mV across R98 at I_drain ≈ 74 mA).    |
|   |   A reading of +7.49 ± 0.02 V both confirms the drain-    |
|   |   side R98 placement AND confirms +V_unreg = +7.5 V.      |
|   |   A reading of ≈ +7.55 V (no offset) → R98 is elsewhere.  |
|   |   A reading much above +7.55 V → +V_unreg is a different  |
|   |   rail (re-trace from BUZ71-D backwards).                 |
| 8 | (instrument off) DMM continuity: follow the +7.5 V        |
|   |   copper from the L22 supply-block filter inductor (near  |
|   |   the W216.4 brass pin) forward across the PCB. Expected  |
|   |   destination per F5 hypothesis: lands on R98 → BUZ71-D.  |
|   |   If yes, the on-board "+7,5V" net = +V_unreg confirmed,  |
|   |   and the §7D banner +7.5V doc-vs-schematic mismatch flag |
|   |   resolves cleanly (line 3304 / 3669 wording = topology   |
|   |   shortcut, BUZ71 regulator stage elided). If no, follow  |
|   |   wherever it does land — that destination is the real    |
|   |   "420 cascade collector" feed claimed in line 3304.      |
+---+-----------------------------------------------------------+
```

Documentation edits gated on this trace:

```
+---+-----------------------------------------------------------+
| # | Edit (deferred until trace is complete — coordinated pass)|
+---+-----------------------------------------------------------+
| 1 | `smp_hw_diag.md` lines 388 + 390–393: R98 topology flips  |
|   | from "BUZ71 source → X96" to "+V_unreg → BUZ71 drain"     |
|   | (or wherever F1/F2/probe 1 actually find it).             |
| 2 | `smp_hw_diag.md` line 380–382: add explicit OP97 pin 3    |
|   | (+) → BUZ71 drain wiring; revise pin 2 (−) wording to     |
|   | match wherever probe 2 finds it.                          |
| 3 | `smp_hw_diag.md` §7C Table B row 5 description: revise    |
|   | "V across R98 (BUZ71 source → X96)" to "V across R98      |
|   | (drain-side current sense, +V_unreg → BUZ71 drain)" or    |
|   | equivalent.                                               |
| 4 | `smp_hw_diag.md` §7C Table B rows 6–7 + decision-matrix   |
|   | row 5: rewrite from "V95 = single A0 SOT-23" to whatever  |
|   | the 4F pair + R+D + (V95 absent OR upstream clamp)        |
|   | actually is, per α/β resolution.                          |
| 5 | `smp_hw_diag.md` §7B layout list lines 412–416: update    |
|   | the "V95 location unknown" wording with the bench-        |
|   | confirmed location (or absence) on this Var.02.           |
| 6 | `smp_hw_diag.md` §7D OPEN item lines 3177–3212: resolve   |
|   | (i) / (ii) / new outcome (iii — no discrete V95) per the  |
|   | trace, and rewrite or close the bullet.                   |
| 7 | `smp_hw_diag.md` §7B layout list V85 / V89: if α holds,   |
|   | flip "A214 GaAs FET cascade amp" to "Si PNP cascade amp"  |
|   | with the BCW68F / MMBT3906-class device class — same      |
|   | class of correction as the AT-42085 GaAs→NPN flip done    |
|   | 2026-04-30 for V50 / V60.                                 |
| 8 | `smp_hw_diag.md` §7D banner +7.5V doc-vs-schematic        |
|   | mismatch flag (filed 2026-04-30, ~lines 650–685): if      |
|   | probe 8 confirms +7,5V → R98 → BUZ71-D, resolve the flag  |
|   | by rewording line 3304 and line 3669 to say "+7.5 V →     |
|   | BUZ71 / OP97 regulator → ≈ +6 V at X96 → 420 cascade      |
|   | bias" (full chain, no shortcut). If probe 8 finds +7,5V   |
|   | landing somewhere else, instead reword the §7D flag to    |
|   | document the actual +7,5V destination and leave the line  |
|   | 3304 / 3669 wording alone.                                |
+---+-----------------------------------------------------------+
```

Sequencing: see "Sequencing" note above (deferrable, run during
LDMOS integration session). ~30 min for probes 1–6 + ~5 min for
probes 7 + 8. Doc edit pass batched to avoid partial-information
thrashing.
