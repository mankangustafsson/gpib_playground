# AG302‑86G Screening Plan

Procedure for screening **4 AG302‑86G units** drawn from the 50 in
stock before one is committed to the A21 IF LNA slot (see
`smp_a21_modernization.md`, compartment‑2 IF chain). Goal is to
filter storage‑/handling‑damaged parts and end up with a primary +
spare pair by Id match, using existing "MMIC Amplifier WW107 blue PCB
v1.0" (silkscreen VV105) fixtures.

Sample size rationale: target is 1 primary + 1 spare (2 keepers). At
an assumed 70–80 % yield on untested stock (device spread + possible
storage damage + occasional rework loss on the fixture), testing 4
gives ~92–97 % probability of ending with ≥ 2 keepers (91.6 % at 70 %
yield; 97.3 % at 80 % yield). Going to 3 drops confidence to ~78–90 %;
going to 5 is diminishing returns.

## Why WW107 PCBs

The WW107 blue boards were laid out for Mini‑Circuits ERA‑xSM+ /
MSA‑0486 parts (case WW107, "Micro‑X", 4‑lead). The AG302‑86G is a
SOT‑86 part on the same Micro‑X outline (Pin 1 = RFin, Pin 2 = GND,
Pin 3 = RFout/bias, Pin 4 = GND) — a drop‑in footprint match with
the same biasing topology (Pin 3 Vd + Rbias + RFC, ERA‑style).

## PCB preparation (one fixture, reused for all 4 units)

The WW107 fixtures were previously populated for a > 1 GHz screening
band and may carry small-value DC blocks. Refit the input/output DC
blocks with **1 nF NP0/C0G** parts to keep the coupling capacitors
transparent across the A21 IF band while preserving cleaner RF
behaviour than X7R:

| Ref (on board) | As shipped | Replace with | Reason |
|---|---|---|---|
| Cblock_in, Cblock_out | as fitted on fixture | **1 nF 1206 NP0/C0G** | Xc at 10 MHz: 159 Ω (100 pF) → 15.9 Ω (1 nF); low-loss across the A21 IF band |
| Rbias (if fitted) | typical 402 Ω @ 12 V rail | **200 Ω 0805, 0.5 W min** | See bias calculation below |
| RFC | keep as shipped (likely ≥ 1 µH) | — | Datasheet recommends 0.33–1 µH; either works |

## Bias setup

Target operating point (AG302‑86G datasheet): **Vd = 5 V, Id = 35 mA**.
Using a 12 V bench supply:

```
  R_bias = (V_supply − V_d) / I_d = (12 − 5) / 0.035 = 200 Ω
  P_bias = (12 − 5) × 0.035 = 245 mW  →  0.5 W resistor minimum
```

Confirm with the PSU current meter on the first unit; trim R_bias by
±20 Ω if the first part lands outside 33–37 mA, and probe the Pin-3
bias/RF-out node with a high-impedance DMM to confirm it sits near the
nominal 5 V operating point (target ≈ 5 V, accept ~4.5–5.5 V for the
fixture). After the first unit locks in a final R_bias, keep that value
for the remaining 3 units so fixture current is the primary screening
variable.

## Test procedure (per unit)

1. **Solder part** onto the fixture with hot air or fine iron. Pin 1
   (RF in) is marked by a bevel / dot on the package body; the WW107
   silkscreen marks pin 1 with a dot at the RF‑in SMA end. The package
   is symmetric enough to fit rotated — verify orientation before each
   reflow.
2. **Power up**: ramp bench PSU 0 → 12 V over ~1 s. Record Id at 12 V.
3. **Quiescent‑current pass/fail**: reject any unit outside **30…40 mA**.
   Expected mean ≈ 35 mA; ±15 % is the screening window referenced to
   the nominal Vd = 5 V operating point established on the first unit.
4. **S‑parameter sweep** (2‑port, VNA, 10 MHz – 1 GHz, 0 dBm drive):
   - **|S21| at 15 MHz (the A21 operating point)** — expect
     +15.5 dB ±0.5 dB. This is the primary pass/fail reading.
   - **|S21| flatness 10 MHz – 100 MHz** — expect ≤ ±0.5 dB ripple.
     Wider sweep up to 1 GHz is for anomaly‑spotting only (any sharp
     resonance hints at bond‑wire or package damage).
   - **|S11|, |S22| 10 MHz – 100 MHz** — expect ≤ −15 dB.
     Reject > −10 dB (indicates bond‑wire / package damage).
5. **Label and bin** — record:
   `SN=xx, Id=yy.y mA, |S21|@15MHz=zz.z dB`.
6. **De‑solder** the unit and reset the fixture for the next part.

## P1dB verification (top 2 candidates only)

P1dB screening adds limited information at the full sample level: the
A21 LNA operates at ~−15 to −20 dBm input / ~−1 to −4 dBm output,
which is ≥ 14 dB below the +13.5 dBm typ P1dB. Idq and small‑signal
S21 already catch the failure modes that matter (bond‑wire damage,
gain droop, instability).

After S‑parameter sweeps on all 4 units, rank by Id match to 35 mA
and passband flatness, then run a P1dB spot check at **15 MHz** (mid‑
A21 IF band) on the top 2 to confirm the primary + spare selection:

- Sweep Pin from −20 to +5 dBm at 15 MHz; record Pout.
- Expect output compression at Pout ≈ +13.5 dBm typ.
- **Reject** units that compress > 1.5 dB below spec (i.e., 1 dB
  compression point < +12 dBm).

Reason for 15 MHz rather than a higher "datasheet‑like" frequency: it
is the actual A21 IF operating band, so the measured P1dB is the
number that directly bounds X75 linearity. Low-frequency P1dB can be
somewhat different from the datasheet's mid-band spec point, so a
15 MHz pass should be interpreted as an operating-band acceptance check,
not as a guarantee of datasheet-frequency compression performance.

## Pass / fail criteria summary

Borderline results (between the pass and reject bands below) get **one
retest** after confirming VNA calibration / reference plane and fixture
integrity. If the repeat result is still borderline, classify the part as
**non-keeper for A21** (may still be labelled and returned to stock).

| Test | Scope | Pass | Borderline / retest once | Reject |
|---|---|---|---|---|
| Fixture current @ 12 V bench supply, fixed R_bias | all 4 | 30…40 mA | — | <30 mA or >40 mA |
| \|S21\| at 15 MHz | all 4 | 15.0…16.0 dB | 14.5…<15.0 dB or >16.0…16.5 dB | <14.5 dB or >16.5 dB |
| Passband ripple 10–100 MHz | all 4 | ≤ ±0.5 dB | — | > ±0.5 dB |
| \|S11\|, \|S22\| 10–100 MHz | all 4 | ≤ −15 dB | > −15 dB to ≤ −10 dB | > −10 dB |
| P1dB @ 15 MHz | top 2 only | ≥ +12 dBm | — | < +12 dBm |

## Outcome and downstream selection

- **A21 primary fit**: pick the single unit with Id closest to 35.0 mA
  and best passband flatness. Mark as "A21‑IF‑LNA‑P".
- **A21 spare**: pick the next best unit. Mark as "A21‑IF‑LNA‑S".
- **Other 2 tested units**: label with Id / S21 summary and return to
  stock (usable as documented spares for future projects).
- **If fewer than 2 keepers**: test 2–3 more from stock; if systemic
  failure, fall back to GALI‑52+/‑84+ adapter PCB per
  `smp_a21_modernization.md` alternatives‑considered section.

## What this screening does *not* tell you

- **Noise figure on FR‑4** (WW107 fixture) ≠ NF in the Rogers‑daughter
  A21 compartment. Use the S21 / Id pass as a device‑level sanity
  bound, not a design‑value number.
- **IF‑band (10–80 MHz) flatness in the A21 sense** only shows up
  after the SAW notch and LPF‑105+ are in the signal path, so final
  verification still happens in Build 3 of the A21 main‑board
  bring‑up plan.
- **Compartment‑2 P1dB** is set by the combined IF‑chain losses; the
  fixture P1dB is a device‑level go/no‑go for the selected candidates,
  not the in‑situ operating value.
