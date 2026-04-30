# SMP02 Chassis Fan — OEM identification + Noctua replacement

OEM fan removed from the SMP02 chassis during the open-case session
covered by [smp_hw_diag.md → Fan](smp_hw_diag.md#while-the-case-is-open--opportunistic-work).
Hub label reads `120x120x31mm Papst Variofan 4312 MV 12VDC 3.4W`,
three-wire harness `+RED, −BLUE, NTC/VIOLET`.

> **Historical / superseded content** is moved to
> [`smp_history.md`](smp_history.md). Inline supersession markers in
> this doc point to specific anchors there. The doc body itself
> always reflects current truth.

## OEM specs — ebm-papst 4312 MV "Variofan"

Per the ebm-papst 4312 MV datasheet
(<https://img.ebmpapst.com/products/datasheets/DC-axial-fan-4312MV-ENU.pdf>).
Hub label "120×120×31" rounds the datasheet's 119×119×32 frame; "3.4 W"
is the worst-case rating at 15 V (datasheet nominal is 3.0 W at 12 V).

| Parameter | Value |
|---|---|
| Frame | 119 × 119 × 32 mm |
| Voltage | 12 VDC nominal, 8–15 V operating |
| Rated power | 3.0 W (label 3.4 W = worst-case) |
| Speed | 2300 rpm at 12 V, full-NTC demand |
| Airflow | 140 m³/h ≈ 82 CFM (free air) |
| Static pressure | ~0.16 in H₂O at zero flow |
| Noise | 39 dB(A) |
| Bearing / L10 @ 40 °C | Ball, 70 000 h |
| Airflow direction | Exhaust over struts |
| Rotation | CW viewed toward rotor |

The "Variofan" suffix means the hub PCB integrates a closed-loop
controller that reads an external NTC thermistor (violet wire) and
ramps the rotor between idle and full speed. **In the SMP02 this
feature is unused**: only X23 pins 9 / 10 (`+12V/LÜFTER`,
`GND/LÜFTER`) are wired to the fan plug, so the violet pigtail on the
OEM Papst is left floating. R&S does its own thermal control on the
PSU board by switching the rail between ~8 V and ~12 V at 60 °C —
see [PSU-side fan-control schematic](#psu-side-fan-control-schematic-band-4-719) below.

## Replacement — Noctua NF-A12x25 FLX (3-pin)

Noctua only makes 120 mm fans in 25 mm or 38 mm depths — there is no
32 mm option. The 25 mm SKU is the sensible swap (7 mm gap is
trivially bridged by M4 nylon spacers or Noctua's bundled long
self-tapping screws). The SMP drives the fan via the two-step
8 V / 12 V `UA+12/L` rail (see schematic summary below) with no
tach feedback to the instrument, so a **3-pin voltage-controlled**
fan is the right family — not a 4-pin PWM. The Noctua's internal
voltage-driven speed loop maps directly onto the rail: ~1200 rpm
when R170 is cold, ~2000 rpm when R170 trips above 60 °C.

| Parameter | NF-A12x25 FLX | vs. Papst |
|---|---|---|
| Frame | 120 × 120 × 25 mm | 7 mm shallower |
| Voltage | 12 V (5–13.2 V usable) | matches |
| Speed | 2000 rpm max | similar |
| Airflow | 102 m³/h (60 CFM) | ~73 % — within user tolerance |
| Static pressure | 2.34 mm H₂O | higher (better through grilles) |
| Noise | 22.6 dB(A) | −16 dB |
| Power | 1.68 W | half |
| Bearing / MTTF | SSO2 magnetic, >150 000 h | 2× lifespan |
| Wiring | 3-pin DC (yellow tach unused) | red→+12, black→GND |

Box includes two inline voltage-reduction adapters (Low-Noise
1700 rpm, Ultra-Low-Noise 1300 rpm) if further detuning is wanted
once the SMP is back on the bench.

### Alternatives considered

- **NF-P12 redux-1700** (3-pin) — ~£15, 1700 rpm, 70 m³/h,
  25 dB(A), 1.1 W. Quieter and lower power, less airflow margin.
  Pick if cost matters more than headroom.
- **NF-F12 industrialPPC-2000 PWM** — closest airflow/RPM match
  (109 m³/h, 2000 rpm), IP67-rated, but 29.7 dB(A) and 1.8 W. Only
  sold as 4-pin PWM, so tie PWM to GND for full-speed-on-supply
  behaviour.

## Mechanical / wiring notes for the swap

- **Depth shortfall (7 mm)**: fit four M4 nylon spacers between fan
  and chassis, or use Noctua's longer self-tapping screws and let
  the fan sit flush against the inner face of the rear grille.
- **Connector**: cut Noctua's 3-pin header, splice red→red,
  black→blue. Tape and heat-shrink the unused yellow tach.
- **NTC harness — do not transplant the bead to the new fan**. The
  thermistor was read only by the Variofan's onboard controller PCB
  (binned with the old fan); the Noctua has no thermistor input,
  and the SMP harness does not read the NTC line either. Taping
  the bead anywhere on the Noctua leaves it electrically dangling.
- **NTC bead location**: in a Variofan installation the NTC is
  bonded to a heat source chosen by the instrument designer — for
  the SMP02, trace the violet wire back to its termination before
  assuming anything is on the old fan body. Leave the bead where
  it sits (its thermal bond is the only useful thing about it now;
  pulling it risks damaging the bond and/or the surrounding
  silkscreen / heatsink finish).
- **Violet wire termination**: cut short at the old-harness end,
  heat-shrink, tape back into the loom. SMP does not fault on an
  open NTC line — there is no consumer once the Variofan is out.
- **Rail check before splicing the Noctua**: DMM across red/blue
  at the old fan plug with the SMP running. **Expected ~8 V at cold
  start / idle, stepping to ~11.5–12 V** once the secondary main
  board passes ~60 °C — this is the R170 → N26 → V87 switchover
  described in band-4 §7.1.9 (see schematic summary below). Seeing
  only one of the two voltages across a 5–10 min warm-up indicates
  R170 / N26 / V87 has failed; tired R170 PTC is the most likely
  culprit on a 30-year-old unit.
- **Direction**: Noctua frames have airflow + rotation arrows
  moulded into the side rib. Papst 4312 MV is exhaust over struts
  — orient the Noctua so the SMP still pulls air the same direction
  through the RF block.
- **Bench test before re-installation**: free-running on the bench
  PSU at 12 V should give ~2000 rpm and ~0.14 A draw. Anything
  above 0.20 A indicates a stalled or mis-wired fan.
- **Acoustic tuning — adapters not needed**: the SMP's own R170
  switch already drops the rail to ~8 V most of the time, which puts
  the NF-A12x25 at roughly 60 % speed (~1200 rpm, very quiet).
  Stacking an L.N.A. / U.L.N.A. adapter on top of an already-reduced
  rail risks dropping below the Noctua's 5.5 V start-up minimum once
  R170 is cold; leave the adapters in the box.

## PSU-side fan-control schematic (band-4 §7.1.9)

Reconstructed from band-4
[§7.1.5 (p.224)](rs_smp_corpus/volumes/band-4/pages/p0224_715-secondary-power-unit_en.md),
[§7.1.9 (p.227)](rs_smp_corpus/volumes/band-4/pages/p0227_719-miscellaneous_en.md),
and the X23 pinout on
[p.230](rs_smp_corpus/volumes/band-4/pages/p0230_76-external-interfaces.md).
The schematic figure pages themselves (band-4 p.234 onward) were not
recovered as text — only as image references in the corpus.

Topology:

```
  N4/N5 secondary winding ── rectify+filter ── PTC R116 ──┬── X23.9  +12V/LÜFTER
  (T1 main transformer)                                   │
                                                  V87 ──┘
                                                   ↑ collector pulled
                                                   │ to ~8 V or ~12 V
                                       N26 comparator
                                                   ↑
                              R170 PTC (Sec. Main Board, internal-air sense)

  R46 NTC ── N1/1 comparator ── IREG / hickup ── main transformer kill (>80 °C)
  (Sec. Main Board, fan-failure protection — independent of fan harness)

  100 kΩ NTC ── X23.8 TSENSE  (separate output for host CPU)
```

Key components and roles:

- **UA+12/L** (X23.9): unregulated transformer rail, only PTC-fused
  by **R116**. Spec band 11.4 … 12.6 VDC / 0.4 A. Slight load sag and
  T1 switching ripple expected and tolerable.
- **GND/LÜFTER** (X23.10): **separate ground return** from logic GND
  on X23.2 / 4 / 6. Don't bond the Noctua's black wire to chassis at
  the fan end — keep it on pin 10.
- **R170** (PTC, Secondary Main Board): senses internal chassis
  temperature. Below ~60 °C → comparator **N26** output keeps **V87**
  in the low-rail state (~8 V on UA+12/L). Above ~60 °C → comparator
  flips, V87 passes the full ~12 V transformer rail. Two-step, not
  analog continuous.
- **R46** (NTC, Secondary Main Board): independent over-temperature
  sensor read by **N1/1**. Trips the IREG signal at 80 °C, putting
  the PSU into hickup mode (§7.1.7). This is the fan-failure safety
  net — survives any fan replacement.
- **TSENSE** (X23.8): 100 kΩ NTC to GND, brought out as a host-readable
  temperature output. Independent of R170 and R46. Likely the source
  for `smp_diag.py`'s temperature trace if any.

Implications for the Noctua swap, repeated for the file's TL;DR:

1. Rail is binary 8 V / 12 V, not a fixed 12 V — Noctua's voltage-
   driven speed loop maps onto this directly (≈1200 rpm cool /
   ≈2000 rpm hot), no PWM or external thermistor needed.
2. Variofan's NTC pin was always floating in this instrument; there
   is no NTC bead in the fan harness to relocate.
3. R46 over-temp protection remains active and unaffected — provides
   safety margin against the Noctua's lower airflow (60 vs 82 CFM).
4. Failure of R170 / N26 / V87 manifests as a stuck-at-8 V or
   stuck-at-12 V rail (one will be quiet-but-undercooled, the other
   loud-but-over-cooled). Trivial to confirm with a DMM at the plug
   across a warm-up.


## Bench-PSU characterisation of the OEM fan (optional, before disposal)

Recommended in [smp_hw_diag.md → Fan](smp_hw_diag.md#while-the-case-is-open--opportunistic-work)
as opportunistic work while the case is open. Run the OEM Papst on
the bench PSU at 8 V and at 12 V with the violet NTC line either
open (fan idle) or pulled to blue through ~5 kΩ (fan full). Record
current draw and rotor RPM (optical tach or phone slow-mo on a
single blade tip). Useful as a baseline if a future SMP unit shows
fan failure as part of a thermal symptom rather than as a noise
nuisance.
