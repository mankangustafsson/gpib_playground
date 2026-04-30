# smp_history.md — A21 / A211 superseded readings & historical narrative

Companion to [`smp_hw_diag.md`](smp_hw_diag.md) /
[`smp_diag.md`](smp_diag.md) / [`smp_next.md`](smp_next.md) /
[`smp_a21_modernization.md`](smp_a21_modernization.md) /
[`smp_fan.md`](smp_fan.md). Holds every SUPERSEDED reading,
withdrawn device ID, RESOLVED OPEN-question discussion, and
date-stamped reconciliation narrative that was moved out of the
truth docs to keep them readable.

**Nothing here is the current truth.** Every entry has a
"Superseded by …" link back to the truth doc. The truth doc, in
turn, has a 1-line marker quote-block at the original location of
each moved block, linking back into this file via the H3 anchor.

## How this file is organised

- One H2 (`##`) per source file, sorted in truth-doc order.
- One H3 (`###`) per migrated block, with stable anchor IDs of
  the form **`H-YYYY-MM-DD-<short-slug>`** where the date is the
  *authoring date of the now-superseded text* (NOT the date of
  the move). Slug = topic, not verdict (so anchors stay stable
  across future re-migrations).
- Each H3 block opens with two header lines:
    - `**Moved from** [`<file>` §<section>](link) **on** YYYY-MM-DD`
    - `**Superseded by:** [link to current verdict](link)`
- Original paragraph text is reproduced **verbatim** below those
  two lines. Do not edit moved content unless to fix a markdown
  rendering issue introduced by the move itself (e.g. orphaned
  list-item indentation).

## How to add a new history entry

When authoring a new SUPERSEDED / RESOLVED / withdrawn / "earlier
reading" block in a truth doc:

1. Write the new verdict directly in the truth doc — no banner,
   no "earlier reading was X" preamble.
2. Take the now-superseded paragraph(s) and paste into the
   correct H2 here, under a new H3 with anchor
   `H-YYYY-MM-DD-<slug>` (date = today; slug = 3-or-4-word
   topic).
3. Add the two header lines and the verbatim original text.
4. Insert a 1-line marker quote-block in the truth doc at the
   original location:
   ```markdown
   > Superseded YYYY-MM-DD — earlier reading of <topic>
   > moved to [`smp_history.md#H-YYYY-MM-DD-<slug>`](smp_history.md#H-YYYY-MM-DD-<slug>).
   > Current verdict: <one-line summary>.
   ```

Anchor IDs are **append-only** — never rename or reuse one.

---

## Sections

(Sections appear in source-truth-doc order. Within each section,
H3 blocks appear in the order they were originally located in the
truth doc, NOT in chronological order of the move.)

## From `smp_hw_diag.md`

### H-2026-04-30-7d-schematic-recovered-banner

**Moved from** [`smp_hw_diag.md` §Step 7 / D — X21 LO ALC sanity check, "SCHEMATIC RECOVERED" banner](smp_hw_diag.md#step-7--a21-bias--a211-comparator-state-measure-dc-voltage-only-if-step-4-shows-x75-dead-with-inputs-present) **on** 2026-04-30.
**Superseded by:** §7D.0 "Current verdict" subsection in `smp_hw_diag.md`. Technical content (device IDs, push-pull topology) restated as plain truth there; this banner is preserved as the original supersession announcement for FA traceability.

> ⚠ **SCHEMATIC RECOVERED 2026-04-30** — sheet 02/02 of A211 var.02
> (drawing 1035.8840.01) is filed at
> [`rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg`](rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg).
> The schematic confirms the §7D part identifications and locks in
> several open hypotheses by inspection:
>
> - **V3 = MRF3866-B** (NPN), **V4 = MRF5160-B** (PNP) — drawn as a
>   **complementary RF stage** with the doubled emitters tied to the
>   ±15 V rails through the per-chip 3R92 (3866 → −15 V; 5160 → +15 V)
>   and the doubled collectors going through **RF chokes (L41 / L43,
>   470 nH each)** to the opposite-polarity ±15 V supply rails. The
>   collectors meet at the X21-side AC-coupling network through the
>   100 Ω summing resistors and feed the LO into the casing. **This
>   is a class-AB push-pull RF power-output stage** with the BFG97
>   acting as **pre-driver** (V2 base-drives the commoned MRF3866 /
>   MRF5160 base node), not the collector-modulated AGC actuator the
>   §7D γ topology had inferred. The §7G "Device-rating anomaly"
>   open question is RESOLVED in favour of the power-amp reading;
>   §7F doubler-location is RESOLVED separately (see §7F banner).
> - **V50, V60 = AT-42085-B** (Avantek/HP NPN Si bipolar, "420"
>   top-mark confirmed by manufacturer datasheet — f_T 8 GHz,
>   8 V / 35 mA class-A bias, P1dB ≈ +20.5 dBm @ 1 GHz; the §7F
>   cascade-amp ID is locked. *Earlier "GaAs FET" identification
>   in this doc was a transcription error against the actual
>   Avago/HP AT-42085 datasheet — corrected 2026-04-30.*).
> - **V61, V62 = HSMS-2800-B** (Avago Schottky pair driven by
>   V50/V60 and forming the **frequency doubler**). The third on-PCB
>   "A0" SOT-23 is the DIAGSAMP rectifier on the X21 RF tap; all
>   three "A0" footprints on the board are HSMS-2800. The §7F
>   doubler-location open question is RESOLVED — see §7F banner.
> - **V2 = BFG97-B** (already known) — drawn as the LO pre-driver
>   feeding the V3/V4 push-pull pair; collector goes to +15 V via
>   collector-load choke L70 and a small base-divider biases the
>   pair into class-AB.
> - **V75 = MAR-8** (the §7G `A08`/MSA-0885 part — schematic confirms
>   the IF post-amp identity).
> - **N80-E = LP365M-L**, **N90-B = OP97FS-B** (already known per §7G).
>
> **Verdict supersession (per user decision 2026-04-30):** the §7D
> D.3 "mirror-rail latch-up" verdict (Table D rows 1, 4a) is
> **fully SUPERSEDED** — the in-circuit "−14.72 V on 3866 pin 6/7"
> and "+14.47 V on 5160 pin 6/7" readings are the expected DC paths
> through the L41 / L43 collector chokes (DCR a few Ω) plus the
> 100 Ω summing R plus the per-chip 3R92, **not** silicon C-E
> latch-up. **Chips are presumed alive pending Step D.5 / Step 8a
> RF validation** (see [`smp_next.md`](smp_next.md) Decision gate). All §7D
> γ "collector-modulated AGC" framing in the analysis below is also
> superseded by the push-pull power-amp reading; the historical
> analysis is retained verbatim as the FA record. The rebuild is on
> hold — D.5 + 8a together close the silicon question.

### H-2026-04-30-7d-deeper-schematic-reread

**Moved from** [`smp_hw_diag.md` §Step 7 / D, "DEEPER SCHEMATIC RE-READ" banner](smp_hw_diag.md#step-7--a21-bias--a211-comparator-state-measure-dc-voltage-only-if-step-4-shows-x75-dead-with-inputs-present) **on** 2026-04-30.
**Superseded by:** §7D.0 "Current verdict" subsection in `smp_hw_diag.md` (corrections 1 + 3 restated as positive truth there; correction 2 retained as `§7D.2 Open question — DIAGSAMP / W216.10 schematic-not-visible`). This banner is preserved as the original three-correction announcement for FA traceability.

> ⚠ **DEEPER SCHEMATIC RE-READ 2026-04-30 — three corrections on top
> of the banner above.** A line-by-line trace of the LO-AMPLIFIER and
> CONTROL-/BIAS-C blocks on
> [`A211_var02_schematic_sheet_02_02.jpg`](rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg)
> overturns three claims in the banner above:
>
> 1. **Bias-network topology (corrects the "doubled collectors driven
>    through L41 / L43 chokes to opposite ±15 V rails" line).** The
>    L41 / L43 470 nH chokes are **base-bias RFCs**, not collector
>    chokes. On the schematic each choke sits between a ±15 V rail and
>    one of the V3 / V4 base nodes, in series with R43 / R44 100 Ω.
>    The R40 / R41 3R92 emitter resistors tie the V4 / V3 emitter
>    pours **directly** to ±15 V (no choke in series). The two
>    collectors (V3 / V4 pins 2/3) are **tied together** and feed
>    **L45 54 nH + C49 10 P** as the output match, then exit the
>    LO-AMPLIFIER block to the right of the page (toward X21).
>    R43 / R44 100 Ω are therefore base-series isolation resistors,
>    **not collector summing resistors**. Consequence: the "≈ 105 Ω
>    C-E" coincidence in `smp_next.md` D.5 cannot be the choke + 100 Ω +
>    3R92 path on the **collector**; it is most likely a base-pin-to-
>    rail measurement (R44 + L43 DCR + R41 ≈ 100 + ~1 + 4 ≈ 105 Ω)
>    on a base pin. The push-pull / class-AB / chips-presumed-alive
>    verdict itself is unchanged — only the bias-network description
>    is wrong above.
> 2. **DIAGSAMP rectifier and W216.10 are not visible on this sheet
>    (corrects the "third A0 = DIAGSAMP rectifier on the X21 RF tap"
>    line).** The W216 connector on this sheet enumerates pins 1–9
>    only (`+15V / GND / GND / +7,5V / −15V / GND / GND / GND /
>    VARSAMP`); **W216.10 is absent from the W216 pinlist**. The only
>    HSMS-2800-B instances on this sheet are V61 and V62 inside the
>    FREQUENCY DOUBLER block (anti-parallel doubler pair across
>    L50 / L60 = 1 µH chokes). There is **no third "A0" SOT-23**
>    drawn on the V3/V4 collector tie / X21 output line. The X21 LO
>    output runs through L45 / C49 and exits the right edge of the
>    JPEG, which appears genuinely cropped at the column-9 right
>    margin (the comparator outputs of N80 also disappear past
>    x = 3968 px on the same edge). Most likely the DIAGSAMP
>    rectifier + W216.10 + the X21 connector itself live on that
>    off-image strip; less likely (but not falsified) the bench-
>    traced "A0 + 1002 + cap → W216.10" needs re-verification on
>    the unit. The bench-side identification of the SOT-23 "A0" on
>    the X21 RF tap as the DIAGSAMP rectifier is **downgraded to
>    provisional** pending a higher-resolution scan or a second look
>    at the right-margin strip; FA narrative below retained verbatim.
> 3. **LP365M comparator block is N.F. on this Var.02 (no contradiction
>    in the banner above, but invalidates downstream supervisor
>    text).** The Var.02 schematic marks the LP365M itself (`N80-E
>    LP365M-L`), the input-divider ladder R80–R85, and the ISET R109
>    274 K **all "N.F." (nicht bestückt / not fitted)**. The two top
>    divider resistors R102 100 K + R103 56 K2 and the −15 V leg
>    R86 100 K + R87 61 K9 + R88 3 K92 are still drawn populated.
>    On Var.02 there is therefore **no LP365M wired-OR fault node
>    to verify** in Step 8a, and the §7G supervisor / V85 / V89
>    crowbar analysis applies to a different variant. See the §7G
>    LP365M N.F. callout, the Step 7B note, and the Step 8a
>    "Supervisor handling" caveat below for downstream consequences.

### H-2026-04-30-7d-d0-d4-failure-chain-narrative

**Moved from** [`smp_hw_diag.md` Step 7 / D.0 + Table D + D.1-D.4 narrative](smp_hw_diag.md#step-7--a21-bias--a211-comparator-state-measure-dc-voltage-only-if-step-4-shows-x75-dead-with-inputs-present) **on** 2026-04-30.
**Superseded by:** the SCHEMATIC RECOVERED banner (H-2026-04-30-7d-schematic-recovered-banner above) + the new clean §7D.0 Current verdict in `smp_hw_diag.md`. The push-pull power-amp reading on the recovered schematic invalidates the entire complementary collector-modulated AGC narrative below (D.0 topology, D.1 Decision matrix, D.2 off-line confirmation, D.3 mirror-rail latch-up verdict, D.4 reconciliation). Bench gates D.5 + D.6 + Status are NOT migrated — they remain in `smp_hw_diag.md` as the active confirmation path. The pre-rebuild Table D row probes (5d-5g, 7a-7e) are also NOT migrated as ohm-check tasks since they are still useful pre-rebuild verifications, but they are reframed in the truth doc to reflect the bias-network correction (R43/R44 are base-series, not collector summing; L41/L43 are base RFCs, not collector chokes).

<details>
<summary>Click to expand the full superseded D.0-D.4 narrative (verbatim from <code>smp_hw_diag.md</code> as of 2026-04-30, ~463 lines)</summary>

Two Motorola SOIC-8 RF transistors sit on Side B at the lower edge
of the PCB, immediately adjacent to the **X21** brass casing pin.
**Part identification (under microscope, top-mark resolved):**
the chip on the −15 V-pour position is **MRF3866** (NPN RF, Case
751-05 Style 1; top mark `R4D ∥ 3866`); the chip on the +15 V-pour
position is **MRF5160** (PNP RF, SO-8 variant of the 2N5160 family;
top mark `R4N ∥ 5160`). The MRF3866 and MRF5160 are the SO-8
surface-mount derivatives of Motorola's classic TO-39 **2N3866 /
2N5160 complementary RF pair** (the 2N5160 datasheet explicitly
calls itself out as *"Designed for Use in Complementary Circuits
with 2N3866"*). Throughout the rest of the doc the chips are
referenced by their last-four part-number digits as **3866** (NPN)
and **5160** (PNP). They are **not in §7.1.7's bias loop** and
**not listed in the p.152 XY-list** (var.02 addition).

Topology bench-confirmed (revised after the §7D A0-trace, the
§7D pinout-trace sessions, and the part-ID resolution): the
**3866 / 5160 complementary pair** and the **DIAGSAMP rectifier**
are two **electrically distinct** sub-blocks that share only the
X21 RF tap node and the ±15 V supplies.

* **DIAGSAMP rectifier (passive, fully bench-traced):** SOT-23 "A0"
  Schottky single sits on the X21 RF tap with **anode (pin 3) on
  the X21 tap node and cathode (pin 1) hard to GND**; a 10 kΩ
  series isolation R `1002` taps off the same X21 node and feeds a
  shunt cap to GND, with the filtered DC node going straight to
  W216.10 (DIAGSAMP). No op-amp on the path. This is the readout
  monitored by §1 / §7C / §7.4.1 (spec band +7.5 … +11 V at W216.10
  in normal operation). Pin 2 of A0 is truly NC.
* **3866 / 5160 complementary pair (RESOLVED — collector-modulated
  AGC):** fed from a separate **capacitive tap off X21** through a
  three-element low-pass filter — series trim inductor L1 → shunt
  cap to GND → series trim inductor L2 — whose output node fans out
  to **all four base pins of both chips**: 3866 pin 2, 3866 pin 3,
  5160 pin 2, 5160 pin 3 (per the SO-8 Case 751-05 Style 1 pinout,
  pins 2 and 3 are the doubled base, externally tied together on
  the PCB). With the LO envelope applied common-mode to both base
  pins of each chip, the two chips operate as **single-ended
  envelope sense → collector-current modulation** stages, not as
  differential pairs. Each chip is then biased through the
  **four-pin emitter group** of the SO-8 RF package: **on each chip,
  pins 1, 4, 5, 8 are all bonded together via a copper pour under
  the package** (this is the standard Case 751-05 Style 1 multi-pin
  emitter for low-inductance grounding and thermal dissipation),
  and that pour is then pulled to one rail through a single 3R92 —
  **3866 emitter pour → −15 V** via 3R92 (NPN sitting on the
  negative rail); **5160 emitter pour → +15 V** via 3R92 (PNP
  sitting on the positive rail). The pin 1↔pin 5 short is part of
  this group (carried by a visible top-side trace and the pour
  underneath), as are pins 4 and 8. Each chip also carries its own
  cermet DC trim pot and ceramic RF trim cap, bulk-bypassed by the
  two large radial electrolytics on the left edge of the cluster.
  On each chip **pin 6 and pin 7 are tied together by a board-level
  trace** (the doubled collector of the SO-8 RF package), and the
  joined collector node leaves the chip through a small **LC filter
  network and a 100 Ω series resistor**, then both chips' joined
  collector outputs converge onto the **collector tab (pin 4) of a
  BFG97 wideband NPN RF transistor** (NXP, SOT-223; per the NXP
  datasheet pinout the SOT-223 BFG97 has pin 1 = emitter, pin 2 =
  base, pin 3 = emitter, pin 4 = collector — split-emitter package).
  Every pin on both chips is now bench-traced.

  **Standard-op-amp reading was TRIPLE-FALSIFIED prior to part-ID
  resolution; documented here for the FA record.** The earlier
  hypothesis that the R4D house mark sat on a SOIC-8 single op-amp
  was disconfirmed on three independent counts before the
  microscope-aided top-mark read identified the parts:
  (i) on the 5160 chip, pin 4 sits on +15 V (via the pour and 3R92),
      which cannot be the V− supply pin of any ±15 V op-amp;
  (ii) pin 6 ≡ pin 7 is hard-shorted on each chip — on a standard
       op-amp this would tie OUT directly to V+, instantaneously
       dumping the output stage's saturation current into the supply
       and destroying the part on power-up;
  (iii) the four-pin emitter-tie group (1, 4, 5, 8) all bonded to
        a per-chip pour and pulled to one rail through a single 3R92
        is incompatible with the standard offset-null + NC pin-8
        configuration of a single op-amp.
  All three were satisfied once the parts were re-identified as
  Motorola SO-8 Case 751-05 Style 1 RF transistors (pins 1/4/5/8 =
  doubled emitter on the rail-pour, pins 2/3 = doubled base on the
  LO sense node, pins 6/7 = doubled collector on the AGC drive node,
  with the 3866 NPN on −15 V and the 5160 PNP on +15 V completing a
  textbook complementary collector-modulated AGC).

  **Functional role — collector-modulated AGC of the BFG97 LO
  buffer.** With both chips sensing the LO envelope on their tied
  base nodes, the 3866 NPN modulates its collector current pulled
  *from* the BFG97 collector node (sourcing current down toward the
  −15 V rail through 100 Ω + LC), and the 5160 PNP simultaneously
  modulates its collector current sourced *to* the BFG97 collector
  node (pushing current up from the +15 V rail through the matching
  100 Ω + LC). The two collector currents sum at the BFG97 collector
  tab, jointly setting the BFG97's class-A operating point as a
  function of detected LO envelope — a textbook complementary
  push-pull AGC drive of an RF buffer's collector bias.

  **Actuator side — RESOLVED.** The "actuator" of the AGC loop is
  the **BFG97 LO-buffer collector**, not (as previously inferred)
  the §7F X50 input cascade-amp base-bias node (originally read as
  a GaAs gate-bias node; reidentified as NPN base-bias per recovered
  Var.02 schematic — see §7F). The X50 cascade-amp
  identification carried in §7F may still describe a separate
  upstream or downstream gain-control stage on this PCB, but the
  immediate destination of the 3866 / 5160 collector-summed output
  is the BFG97 RF NPN — bench-traced. The §7G pending-work list
  carries an item to verify the BFG97's bias network (collector-
  load inductor, base-bias divider, emitter resistors on its split
  pin 1 / pin 3) is intact, since a sustained 3866 / 5160 fault
  could have driven the BFG97 into saturation or cutoff and damaged
  its collector-supply network.

The 3R92 precision Rs (now confirmed as **two of them**, one per
chip in series between the emitter-tie pour and the rail, not on
the input/load path) supersede the earlier "3866 detector load"
reading of 3R92 — see Table D row 5 revised footnote.

Relevance to the X75-dead symptom: a dead 3866 / 5160 pair leaves
the **BFG97 LO buffer's collector bias undefined** (per the bench-
traced pin-6/7 → 100 Ω + LC → BFG97 pin 4 path, see §7D revised
topology above). With both chips internally shorted collector-to-
emitter (pin 6/7 ≡ pin 1/4/5/8), the BFG97 collector is alternately
pulled toward both ±15 V rails through the two 100 Ω resistors and
may rest near 0 V — well below the BFG97's required collector-
emitter operating voltage. The BFG97 then runs deeply in cutoff
(no LO buffering), X21 collapses, A212 is starved of LO, TP1910 /
X75 read dead *with §7.1.7 bias still reading nominal*. This is the
most common non-§7.1.7 reason for Step 7 A/B to pass while X75
stays dead, so Step 7D runs **before** Step 8. The exact mechanism
linking 3866 / 5160 failure → BFG97 collector collapse → X21 LO
collapse is now bench-supported but **not yet verified end-to-end**
— see §7G pending work for the BFG97 bias-network integrity check
(the sustained 3866 / 5160 fault current may also have damaged the
BFG97 itself or its collector-load components).

| # | Probe point (Side B, lower cluster) | Expected (nominal op) | Measured | Verdict |
|---|--------------------------------------|-----------------------|----------|---------|
| 1 | 3866 (NPN) pin 7 (joined collector node — pin 6 ≡ pin 7 per §7D γ trace; collector output of the NPN half of the complementary pair, summed with the 5160 PNP joined collector through 100 Ω + LC onto BFG97 collector) | nominal-op DC sits at whatever bias the BFG97 collector node requires (rail-mid range, set by the BFG97 collector load and the two 100 Ω summing resistors) | **−14.72 V** (pulled hard toward the −V rail) | **FAIL** — chip-internal collector ↔ emitter path inside the 3866 (NPN with pins 1/4/5/8 emitter on −15 V) pulled the joined pin 6/7 collector node hard toward −V through the silicon. The BFG97 collector then sees this −14.72 V through 100 Ω, summed with the 5160's +14.46 V through 100 Ω → BFG97 V_C ≈ −0.13 V (rail-killing for an NPN RF amp). The earlier "V+ supply path open" op-amp framing is **withdrawn** (pin 7 is not a supply pin in the SO-8 Case 751-05 Style 1 RF-transistor pinout). |
| 2 | 3866 (NPN) pin 4 (emitter pour group 1/4/5/8, on −15 V via 3R92 per §7D RF-transistor pinout) | local −V rail (≈ −15 V + I·3R92, mV-scale drop set by the 3866's quiescent emitter current) | **−15.24 V** | OK at the pin — pour↔−15 V path via 3R92 is intact. **Revised under §7D (β):** original "V− supply intact" op-amp verdict withdrawn — pin 4 is one of the four bonded emitter pins on the pour group, not a supply pin; the reading is diagnostic of the emitter-rail tie. |
| 3 | 3866 (NPN) pin 6 (joined with pin 7 by board trace per §7D γ; same collector node) | reads identical to pin 7 (row 1) by construction — the two pins are externally shorted (doubled collector of the SO-8 RF package) | **−14.72 V** (= 3866 pin 7, by board-level short) | reads as expected — the equality of pin 6 and pin 7 is **not fault evidence**; it is the design-intent SO-8 RF pinout. Fault evidence is the pin-7-pulled-toward-−V reading (row 1), not the pin 6 ≡ pin 7 equality. |
| 4 | 5160 (PNP) pin 6 (joined with pin 7 by board trace per §7D γ; same collector node) | reads identical to pin 7 (row 4a) by construction | **+14.46 V** (= 5160 pin 7, by board-level short) | reads as expected — same reframing as row 3, doubled-collector SO-8 RF pinout. |
| 4a | 5160 (PNP) pin 7 (joined collector node — same role as row 1 but on the PNP half, pulled toward +V) | nominal-op DC same as row 1 (BFG97 collector bias point) | **+14.47 V** (pulled hard toward the +V rail) | **FAIL** — chip-internal collector ↔ emitter path inside the 5160 (PNP with pins 1/4/5/8 emitter on +15 V) pulled the joined pin 6/7 collector node hard toward +V through the silicon. The complementary depression on the 3866 and elevation on the 5160 is the textbook **mirror-rail latch-up** signature expected when both halves of the complementary NPN/PNP pair latch simultaneously to their respective emitter rails. |
| 4b | 5160 (PNP) pin 4 (emitter pour group 1/4/5/8, on +15 V via 3R92 per §7D RF-transistor pinout) | local +V rail (≈ +15 V − I·3R92, mV-scale drop set by the 5160's quiescent emitter current) | **+15.09 V** | OK at the pin — pour↔+15 V path via 3R92 is intact. **Revised under §7D (β):** original "V− supply path open + internal V+↔V− short drags pin 4 up to pin 7 + Vbe" op-amp verdict **withdrawn** — pin 4 is hard-tied to +15 V via the emitter pour by design, so +15.09 V is the expected healthy reading. The "B4 − B7 = +0.62 V = one Vbe" coincidence falls away as fault evidence (the internal-collector-emitter-short hypothesis still survives on rows 1 / 4a and §D.2 evidence, but loses this anchor). |
| 5a | 3866 (NPN) pin 1 / 4 / 5 / 8 (emitter pour group, biased to −V via the per-chip 3R92 — read any one of the four pins, results identical) | a few tens of mV positive of the local −V rail (≈ −15 V + I·3R92, where I is the 3866's quiescent emitter current) | covered by row 2 (pin 4 read = −15.24 V) | reading establishes that the −V → 3R92 → pour → emitter-tie group bias path is intact; deviation by more than a few hundred mV implies open 3R92, broken pour, or chip ESD damage |
| 5b | 5160 (PNP) pin 1 / 4 / 5 / 8 (emitter pour group, biased to +V via the per-chip 3R92 — read any one of the four pins, results identical) | a few tens of mV negative of the local +V rail (mirror of 5a, set by the 5160's quiescent emitter current) | covered by row 4b (pin 4 read = +15.09 V) | mirror of 5a |
| 5c | V across each 3R92 (3866 pour ↔ −15 V rail; 5160 pour ↔ +15 V rail) | small drop, mV-scale, set by each chip's quiescent emitter current | TBD | confirms each chip is drawing the expected emitter current; ≈ 0 V drop indicates an open 3R92 or a dead chip pulling no current |
| 5d | 3866 pour ↔ −15 V rail (chips-out, ohm across the 3R92) | ≈ 3.92 Ω | TBD | non-3R92 reading (OL or grossly off-value) implies the 3R92 has fused open or the pour-to-rail trace has cracked; either case **must** be repaired before fitting fresh silicon |
| 5e | 5160 pour ↔ +15 V rail (chips-out, ohm across the 3R92) | ≈ 3.92 Ω | TBD | mirror of 5d |
| 5f | 3866 pour ↔ 3866 footprint pin 1, 4, 5, 8 (chips-out, ohm to each of the four pins) | sub-ohm short to all four | TBD (visual: pour bonds visible from top) | non-zero on any of the four implies a lifted pad / cracked bond — must be repaired before fitting fresh silicon |
| 5g | 5160 pour ↔ 5160 footprint pin 1, 4, 5, 8 (chips-out, ohm to each of the four pins) | sub-ohm short to all four | TBD (visual: pour bonds visible from top) | mirror of 5f |
| 5 | (legacy "V across the ≈ 3R92 precision R") | — | — | **Superseded** by 5a–5g per §7D revised topology — there are now **two** 3R92s, each in series between the per-chip emitter pour and one rail (3866 pour↔−15 V; 5160 pour↔+15 V), neither in the input/load path the original row was probing. Treat the original row as historical context only. |
| 6 | DC at the X21 brass pin (DMM only — **no SA until Step 8 with the ≥30 dB / ≥1 W pad**) | clean DC offset; AC-coupled detectors read ≈ 0 V, DC-coupled read tens of mV | ≈ 0 V | consistent with dead loop (no useful info on its own — RF must reach SA via Step 8 to confirm LO presence/absence at X21) |
| 7a | 3866 footprint pin 6 ↔ pin 7 (chips-out, ohm) | sub-ohm short (board-level doubled-collector trace per §7D γ) | TBD (visual: top-side trace) | non-zero implies a lifted pad / cracked bond on the pin 6 / pin 7 trace — must be repaired before fitting fresh silicon |
| 7b | 5160 footprint pin 6 ↔ pin 7 (chips-out, ohm) | sub-ohm short (board-level doubled-collector trace per §7D γ) | TBD (visual: top-side trace) | mirror of 7a |
| 7c | 3866 joined pin 6/7 collector node → BFG97 collector tab (pin 4) — through the 100 Ω series R and LC filter (chips-out, ohm; expect to read the 100 Ω plus DCR of the LC) | ≈ 100 Ω + small inductor DCR (a few Ω) | TBD | open implies a fused 100 Ω, broken LC inductor, or cracked trace between the 3866 collector and the BFG97 collector summing node — NPN-side collector-modulated AGC drive lost |
| 7d | 5160 joined pin 6/7 collector node → BFG97 collector tab (pin 4) — through the 100 Ω series R and LC filter (chips-out, ohm) | ≈ 100 Ω + small inductor DCR (a few Ω) | TBD | mirror of 7c — PNP-side AGC drive lost if open |
| 7e | BFG97 collector (pin 4 / tab) → +V rail through its collector-load inductor (chips-out, ohm) | a few Ω (inductor DCR), with whatever pull-up R sits in parallel | TBD | open inductor leaves the BFG97 starved of collector supply regardless of 3866 / 5160 state; this is a likely **secondary failure** if the 3866 / 5160 fault drove sustained collector current through the inductor and fused it. **Inspect at rebuild even if the 3866 / 5160 fault is the primary diagnosis.** |

**D.1 Decision matrix** — read after Table D is filled. **Note (per
§7D revised topology):** the original cascade A→B op-amp reading is
withdrawn; the 3866 (NPN) and the 5160 (PNP) are a complementary
collector-modulated AGC pair, not a cascade, and the per-output
"buffer / error amp" verdicts no longer apply. The matrix below
covers what can still be inferred from the collector-node and
emitter-pour readings under the resolved RF-transistor pinout.

| 3866 (NPN) pin 7 / 4 (#1, #2) | 5160 (PNP) pin 7 / 4 (#4a, #4b) | Verdict |
|-------------------------------|---------------------------------|---------|
| pin 7 at the BFG97-collector bias point, pin 4 clean −V rail | pin 7 at the BFG97-collector bias point, pin 4 clean +V rail | both chips' emitter rails intact and neither collector node railed; if pin 5a/5b also healthy, the 3866 / 5160 pair is plausibly alive — **Step 8** to check downstream RF/IF |
| pin 7 depressed toward V−, pin 4 clean −V rail | pin 7 elevated toward V+, pin 4 clean +V rail | the rail-mirror pattern observed on this unit — both chips dead with internal collector ↔ emitter shorts pulling each collector node toward its own emitter rail. **Proceed to §7E rebuild.** |
| pin 7 at bias point, pin 4 clean on one chip | the other chip showing the rail-mirror pattern | only one half of the complementary pair dead — same rebuild path applies; replace both the 3866 and the 5160 anyway (the surviving chip likely degraded by the same trigger event, and the complementary pair must be matched at rebuild). |
| both pin 4 (emitter pour) = 0 V on both chips | — | both per-chip emitter rails dead globally → trace upstream supply rail (likely shared with N90 supply path) before any silicon work |

**D.2 Off-line confirmation (instrument OFF, DMM diode-test mode)** —
re-probe with the A211 unpowered to separate "loop railed because input
is wrong" from "silicon is physically dead":

| Device | Probe pattern | Healthy reading | This unit | Verdict |
|--------|--------------|-----------------|-----------|---------|
| A0 (SOT-23) | red on pin 3 (anode, X21 RF tap side), black on pin 1 (cathode, GND); pin 2 NC | Schottky: ≈ 0.23 … 0.35 V forward (3→1), OL reverse (1→3) — barrier-height bracket established on this PCB by two other "A0"-marked parts reading 0.234 V and 0.265 V forward in their own footprints | **0.34 V forward (3→1), OL reverse (1→3)** — clean Schottky behaviour; Vf elevated ~80 mV above the two healthy refs | **Bystander, mildly degraded at most** — per §7D revised topology A0 is on the passive DIAGSAMP rectifier with cathode hard to GND (no path to either the 3866 or the 5160 input network), so it has **no role** in the 3866 / 5160 cascade failure either as cause or as load. The ~80 mV Vf elevation vs the two on-board A0 reference footprints is real (the RC-shunt parallel-load explanation no longer applies — the reference footprints likely have similar passive networks) and is consistent with mild barrier degradation; the OL reverse reading rules out a hard reverse short but does **not** rule out elevated reverse leakage at the actual LO envelope swing (DMM diode test only forces ~2-3 V across the device, well below any plausible LO peak). A0 is **replaced** at rebuild as a precaution (cheap, already on the rework path) and **bench-tested standalone post-removal** to characterise the pre-rebuild detector state for FA record — see §7E rebuild step 2a (revised verdict bullets reframe this as bystander confirmation rather than trigger discrimination). |
| 3866 (NPN) | pin 7 (joined collector node = pin 6/7 collector summing node per §7D γ) ↔ pin 4 (emitter pour group 1/4/5/8, on −15 V via 3R92) — DMM red on pin 7 (collector), black on pin 4 (emitter) is the reverse-biased C↔E direction for an NPN | OL both directions on a healthy NPN — collector-emitter open in the absence of base drive, with the polarity-aware diode test seeing the bulk silicon, not the B-E or B-C junctions in isolation | low-resistance reading both directions | **FAIL — internal collector ↔ emitter path** through the 3866. The on-die C-E shunt is what pulls the joined pin 6/7 collector node toward −15 V (the emitter rail) (Table D row 1). The earlier "V+ ↔ V− supply-to-supply short" op-amp framing is **withdrawn** — pin 7 is the doubled collector and pin 4 is one of the four bonded emitter pins; the failure is C-E, not supply-to-supply. |
| 5160 (PNP) | pin 7 (joined collector node, same role as the 3866) ↔ pin 4 (emitter pour group 1/4/5/8, on +15 V via 3R92) — DMM red on pin 4 (emitter), black on pin 7 (collector) is the reverse-biased C↔E direction for a PNP (mirror of the 3866 polarity) | OL both directions on a healthy PNP | low-resistance reading both directions (≈ 140 Ω) | **FAIL — internal collector ↔ emitter path** through the 5160, mirror of the 3866. The 140 Ω reading is the on-die C-E path through the damaged silicon; this is what pulls the joined pin 6/7 node toward +15 V (the PNP emitter rail) (Table D row 4a). The earlier "internal supply-to-supply short, explains +15 V on −15 V rail at pin 4" verdict **withdrawn** under §7D (β/γ) — the +15 V on the 5160 pin 4 is the *healthy* PNP emitter-pour reading, not fault evidence. |

**D.3 Run verdict — this unit:**

> ⚠ **D.3 VERDICT FULLY SUPERSEDED 2026-04-30** by recovered
> schematic (sheet 02/02 of A211 var.02, drawing 1035.8840.01;
> filed at
> [`rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg`](rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg)).
> The schematic shows V3 (MRF3866) and V4 (MRF5160) as a class-AB
> push-pull power-output stage — the in-circuit "−14.72 V on 3866
> pin 6/7" and "+14.47 V on 5160 pin 6/7" readings (Table D rows 1
> and 4a) are the expected DC paths through the bias network of the
> push-pull stage, **not** an on-die C-E latch-up. (Bias-network
> topology corrected per the DEEPER SCHEMATIC RE-READ banner at
> the top of §7D: L41 / L43 470 nH chokes are **base-bias RFCs**
> in series with R43 / R44 100 Ω, R40 / R41 3R92 are emitter-to-
> rail directly, collectors are tied → L45 54 nH + C49 10 P
> output match → off-page right toward X21. The previous "doubled
> collectors driven through L41 / L43 chokes to opposite ±15 V
> rails" framing in this banner is **withdrawn** — the push-pull /
> chips-presumed-alive verdict itself is unchanged.) The chips are presumed alive pending the
> Step D.5 DMM cross-check + the Step 8a bench-PSU LO-chain RF
> validation; D.3 is demoted to a historical footnote in the FA
> record. The verdict text and analysis below are retained verbatim
> for traceability of the original reasoning, but **must not be
> acted on** as a rebuild trigger. See [`smp_next.md`](smp_next.md)
> Decision-gate section for the resolution path.

- ALC loop **catastrophically failed**. The two chip readings are
  **mirror-symmetric** to the emitter bias — every pin on the 3866
  (NPN) reads at or near its local pour-rail (−V via 3R92), every
  pin on the 5160 (PNP) reads at or near its local pour-rail (+V via
  3R92). Under §7D (β/γ) revised topology, **part of this mirror
  pattern is the expected healthy reading**: pins 1, 4, 5, 8 on each
  chip are hard-tied to the emitter pour-rail by design (the SO-8
  Case 751-05 Style 1 doubled-emitter pinout), and pins 6 ≡ 7 are
  tied together by board trace (the doubled-collector pinout, so the
  equality is design-intent, not a fault). The remaining fault
  evidence is on the **joined pin 6/7 collector node** of each chip:
  depressed ~30 V toward the −V rail on the 3866; depressed ~530 mV
  toward the +V rail on the 5160 (with a modest +0.62 V offset above
  the +V pour, distinguishing the 5160's C-E damage from a clean
  rail-glue). Both chips show the collector-to-emitter latch-up
  signature; both are dead by the symptom; the rebuild is still the
  right call but the *specific* fault-site list below has been
  retrimmed under (β/γ).
- Confirmed fault sites:
  1. **3866 (NPN) internal collector ↔ emitter latch-up** — joined
     pin 6/7 collector node pulled to local −V emitter pour
     (= −14.72 V) by a low-impedance internal C-E path through the
     silicon (D.2 3866 row). The original "V+↔V− internal short
     plus output↔V+ internal short" op-amp framing is **fully
     withdrawn** (no V+ or V− pin in the SO-8 RF-transistor pinout).
     Cascade-from-A-to-B mechanism remains withdrawn (the 3866 and
     the 5160 share an input node and an output summing node, not a
     serial signal path) — the 3866 and the 5160 failed by
     **independent but related** mechanisms (most likely a common
     upstream stress event — see trigger discussion).
  2. **+15 V supply path to the 3866 — WITHDRAWN** under §7D (γ).
     The previous "pin 7 = V+ supply, per-chip pi-filter fused
     open" op-amp framing is **removed**: pin 7 is the doubled
     collector node feeding the BFG97 collector summing junction,
     not a supply pin. The 3866's emitter rail is delivered through
     the four-pin emitter pour at −15 V via 3R92, not through any
     pin-7 leg. The pin-7 reading at −14.72 V is now diagnosed as
     *internal C-E damage* (site 1), not as *supply-path open*. The
     3R92 / pour emitter-bias path is intact (Table D row 2 =
     −15.24 V). No per-chip pin-7 filter element to replace.
  3. **5160 (PNP) internal collector ↔ emitter latch-up** — joined
     pin 6/7 collector node at +14.47 V (= +V pour −0.62 V), with
     ≈ 140 Ω internal C-E path (D.2 5160 row). Mirror of site 1.
     Same reframing: the original "V+↔V− internal short" op-amp
     framing is **withdrawn**; the +15.09 V on the 5160 pin 4 is
     the healthy PNP emitter-tie reading, not fault evidence. The
     530 mV depression on the joined collector node is not a
     supply-filter symptom but the small DC drop across the internal
     C-E damage path under whatever current the BFG97 collector
     network is sourcing into the summing junction.
  4. **−15 V supply path to the 5160 pin 4 — WITHDRAWN** under §7D
     (β). Pin 4 of the 5160 is on the +15 V emitter pour via 3R92
     by design (PNP emitter on the positive rail); there is no
     −15 V supply leg to the 5160 pin 4 to be open. The original
     "fuse-open on R4D-B's −15 V leg" rebuild item is **removed**
     from the parts/rework list.
  5. **BFG97 collector-network integrity — TO BE VERIFIED at
     rebuild (CONDITIONAL secondary fault site).** With both
     collector nodes latched to opposite rails through the silicon
     (3866 → −V, 5160 → +V), the BFG97 collector tab (pin 4) sees
     ±15 V applied through the two 100 Ω summing resistors, with the
     collector-load inductor sourcing/sinking whatever current the
     BFG97 +V rail (or its pull-up R) presents. Sustained operation
     in this condition can have fused open the BFG97's collector-
     load inductor or stressed the 100 Ω summing resistors.
     **Inspect and ohm-check the BFG97's collector-load inductor
     and the two 100 Ω resistors** before fitting fresh 3866 / 5160
     silicon — see Table D rows 7c/7d/7e and §7G pending work for
     the verification procedure.
  - **A0** — included in the rebuild as a precaution but **not** a
    confirmed fault site on the 3866 / 5160 failure path. Per §7D
    revised topology A0 is the passive DIAGSAMP rectifier (cathode
    hard to GND, no path to either chip's input network), so its
    in-circuit Vf elevation of ~80 mV vs the two on-board A0
    reference footprints is independent of the AGC failure — it
    indicates at most a mildly degraded DIAGSAMP detector. Bench-
    tested standalone post-removal in §7E rebuild step 2a for FA
    record.
- The fact that the OP97 (N90) next door still reads clean ±15 V on
  its supply pins confirms the global rails are healthy — the only
  surviving "open per-chip filter" hypothesis is on the BFG97
  collector-load inductor (site 5), not on any 3866 / 5160 emitter-
  pour leg (sites 2 and 4 both withdrawn).

**Trigger hypothesis — surviving candidates after the §7D input
trace and the part-ID resolution to MRF3866 / MRF5160**: the
original "cascade originating at A0" narrative is **withdrawn** (per
§7D revised topology A0 has no path to either chip's input network),
and the previously-leading "R4D-B set-point divider open inducing
integrator wind-up" candidate is also **withdrawn** — there is no
W216.1 → 5160 pin 3 set-point divider; pin 3 sits on the X21 RF tap
node along with the 5160 pin 2 and the 3866 pins 2 / 3 (the doubled-
base group of both SO-8 RF transistors), all through the cap +
L1-Cshunt-L2 LPF. Surviving candidates:

1. **Common-mode LO transient on the X21 input tap.** A high-energy
   transient on the X21 line (LO supply glitch, neighbouring-chain
   breakdown, oscillator going overdrive) couples through the cap
   tap and LPF onto the commoned base node, presenting a large
   common-mode voltage to both pin 2/3 base groups simultaneously.
   If the transient exceeds either chip's V_BE breakdown or
   absolute-max base-emitter spec, both can latch up C-E in a
   single event. This naturally produces the observed simultaneous
   double-failure with rail-mirror symmetry (the 3866 NPN latches
   toward its −V emitter pour, the 5160 PNP toward its +V emitter
   pour).
2. **Supply-rail transient.** A ±15 V glitch (simultaneous common-
   mode spike on both rails from A26, or a chassis-ESD coupling
   event) directly stresses both chips' base-emitter junctions into
   latch-up without any signal-path trigger. Distinguishing
   evidence: a degraded A0 reading (§7E step 2a) is a **mild
   positive indicator** — the same transient that latched the
   3866 / 5160 plausibly stressed A0 too, without A0 being on the
   AGC path.
3. **Pour / 3R92 emitter-bias path failure.** Per §7D revised
   topology, pins 1, 4, 5, 8 of each chip are bonded to a per-chip
   copper pour (the doubled emitter of the SO-8 RF package) and the
   pour is pulled to one rail through a single 3R92. If that 3R92
   opens, or the pour-to-rail trace cracks, or the chip-internal
   bond to any of the four emitter pins is disturbed (e.g. by an ESD
   strike on any of pins 1/4/5/8), the emitter floats — and given
   that the emitter-tie sets the standing collector current of the
   stage, the chip's collector node goes to an undefined state,
   plausibly latching the C-E junction on first transient. This
   would normally take one chip out, not both, unless both 3R92s
   share a common failure mode (manufacturing batch defect, both
   stressed in the same supply event). **Pre-rebuild ohm check on
   both 3R92s AND the pour↔pin 1/4/5/8 bonds on each footprint
   (§7E-bench A3 revised, rows 5d–5g) is the discriminator.**
4. **Trim inductor open → floating bases.** L1 or L2 in the input
   LPF opens → both pin 2/3 base groups float → V_BE undefined on
   first leakage current → latch-up. Same caveat: this would
   normally take both chips down (since they share the input node),
   which fits the observed symptom. **Pre-rebuild continuity check
   on L1 and L2 (§7E-bench A3 revised) is the discriminator.**
5. **BFG97 collector-network short / load fault — REVERSE-CASCADE
   trigger.** Per §7D (γ) the joined pin 6/7 collector outputs of
   both chips sum onto the BFG97 collector tab through 100 Ω + LC.
   If the BFG97 collector is shorted to ±15 V (BFG97 internal C-E
   breakdown, collector-load inductor shorted to a rail, decoupling
   cap internally shorted, or a stray solder bridge across the
   collector-load network), the resulting hard rail forced onto the
   100 Ω summing node back-drives both chips' collectors with the
   full ±15 V rail through 100 Ω — well above the safe V_CE reverse-
   bias of either RF transistor. This back-drive can latch both the
   3866 and the 5160 simultaneously even without an X21-input or
   supply-rail transient. **Discriminator: pre-rebuild ohm check on
   the BFG97 collector to ±15 V and to GND (Table D row 7e); the
   collector should read finite (inductor DCR + pull-up R) to one
   rail, OL to the other, with no rail short. The 100 Ω summing
   resistors should both read close to nominal (Table D rows 7c/7d
   minus a few Ω of inductor DCR).**

The cascade-effect mechanism is then:

1. Common stress event (per #1 / #2 / #5 above) latches both chips
   simultaneously — internal C-E paths form in both, pulling each
   chip's joined pin 6/7 collector node hard to that chip's
   emitter-pour rail (3866 → −V, 5160 → +V).
2. Both collector nodes now drive the BFG97 collector tab through
   their respective 100 Ω summing resistors with opposite-rail DC
   (3866 ≈ −14.7 V, 5160 ≈ +14.5 V) → BFG97 collector parked at
   ≈ (3866·0.5 + 5160·0.5) ≈ −0.1 V (or wherever the collector-load
   inductor's resting current sets it), which is well below the
   BFG97's required V_CE for class-A operation.
3. BFG97 deeply in cutoff → no LO buffering → X21 LO collapses →
   casing comb gen starved → X75 / TP1910 dead. **DIAGSAMP also
   reads dead** not because the rectifier is broken (per §7D revised
   topology it's passive and intact), but because A0 has no LO
   envelope to rectify when X21 has collapsed.
4. **Possible secondary damage:** sustained operation in this
   condition can fuse the BFG97 collector-load inductor or stress
   the 100 Ω summing resistors — verify at rebuild per Table D row
   7e and §7G pending work (BFG97 bias-network integrity check).

- Failure chain to symptom: **trigger = common-mode LO transient OR
  supply-rail transient OR pour/3R92 failure OR LPF inductor open
  OR BFG97 collector-network fault (discriminated by §7E-bench A3
  revised + §7E step 2a + Table D rows 7c–7e) → both 3866 and 5160
  latch C-E to their respective emitter pours → joined pin 6/7
  collector outputs back-drive the BFG97 collector summing node to
  ≈ 0 V → BFG97 deep-cutoff → LO drive at X21 collapses → A212
  starved of LO → X75 / TP1910 dead and the passive DIAGSAMP
  rectifier delivers ≈ 0 V through its intact A0 + 1002 + cap
  network because there is no upstream LO to rectify** — all this
  with §7.1.7 bias still reading nominal. DIAGSAMP recovery is
  automatic once the rebuild restores LO at X21; no DIAGSAMP-
  specific repair is needed.
- Action: **repair before any further RF probing**. Do **not**
  advance to Step 8 (SA on X21) until A0, the 3866 and the 5160 are
  replaced AND the BFG97 collector-network integrity is verified
  intact (Table D rows 7c/7d/7e) AND Step 7E passes — a dead
  detector, unpowered AGC pair, or fused BFG97 collector-load
  inductor will all mimic an LO-chain fault on the SA and waste a
  probing session.

**D.4 Re-measurement under instrument off (full diode-mode junction sweep,
in-circuit) — D.2 / D.3 verdict CHALLENGED, NEEDS RECONCILIATION.** A
later bench session re-probed both chips under DMM diode mode (instrument
off) and read **healthy junction signatures** on the 3866 and *mostly*
healthy on the 5160:

```
+-------+-------+--------------+--------------------------------------+
| Chip  | Junc. | Reading      | Interpretation                       |
+-------+-------+--------------+--------------------------------------+
| 3866  | B-E F | 0.68 V       | normal NPN B-E Vf                    |
| 3866  | B-E R | OL (or 1.9 V | DMM open-circuit V; intermittent     |
|       |       | intermittent)| 1.9 V = X21 LPF cap-tap charging     |
| 3866  | B-C F | 0.68 V       | normal NPN B-C Vf                    |
| 3866  | B-C R | OL           | normal                               |
+-------+-------+--------------+--------------------------------------+
| 5160  | B-E F | 0.7 → 1.0 V  | junction Vf with series-cap charging |
|       |       | rising       | through the in-circuit network       |
| 5160  | B-E R | 1.9 V        | DMM open-circuit V = effective OL    |
|       |       |              | with cap-charge transient            |
| 5160  | B-C F | 0.7 V        | normal PNP B-C Vf                    |
| 5160  | B-C R | 1.9 V        | DMM open-circuit V = effective OL    |
+-------+-------+--------------+--------------------------------------+
```

C-E re-measurement on **both chips: 105 Ω in both directions** (vs the
earlier "low-Ω" 3866 reading and "≈ 140 Ω" 5160 reading recorded in
Table D rows 1 and 4a / D.2). The 105 Ω value is **suspiciously close
to the in-circuit external network sum**:

```
  pin 7 (C) ─ 100 Ω summing R ─ BFG97 col tab ─ L (DCR few Ω) ─ +V rail
  pin 4 (E) ─ 3R92 (3.92 Ω) ─── ±V rail
                            external ≈ 100 + few + 3.92 ≈ 105 Ω
```

**Reading-by-reading reconciliation:**

- **3866 — junctions read fully alive in all four directions.** B-E and
  B-C both forward at 0.68 V, both reverse at OL. This is **not** the
  signature of a damaged BJT. Diode-mode 0.0 V + continuity on C-E with
  no junction Vf rules out silicon C-E latch (a real C-E latch would
  *not* leave B-E and B-C reading as healthy junctions in 9 cases out
  of 10). 105 Ω in C-E almost certainly = the external network, not
  silicon damage.
- **5160 — B-C reads alive both directions, B-E shows a charging-cap
  signature on forward Vf (0.7 V settling upward to 1.0 V).** This is
  consistent with junction Vf + series cap (the X21 LPF cap-tap on the
  base side, or bypass caps on the emitter pour) charging through the
  junction at the DMM's constant-current diode-mode test current. **Not
  a damaged junction by itself.** Reverse readings of 1.9 V = the DMM's
  open-circuit voltage with cap charge transients, equivalent to OL.

**Interpretation:** the §7D Table D rows 1 / 4a and D.3 fault-site
verdicts (3866 + 5160 internal C-E latch-up) are **not supported by
the diode-mode evidence** captured in this re-measurement session. Both
chips may be **alive**; the original "low-Ω C-E both directions" ohm
reading was likely seeing the external 100 Ω + LC + 3R92 network, not
silicon damage. **D.3 is now flagged as PROVISIONAL pending the
external-network cross-check below.**

</details>

### H-2026-04-30-7f-alc-actuator-hypothesis-superseded

**Moved from** [`smp_hw_diag.md` §Step 7F header banner (X50 / V50 V60 LO cascade amp)](smp_hw_diag.md#step-7f--x50--v50v60-lo-cascade-amp-bench-tracing-side-b-optional-during-rebuild) **on** 2026-04-30.
**Superseded by:** H-2026-04-30-7d-schematic-recovered-banner (above) + the new clean §7D.0 in `smp_hw_diag.md`. The push-pull power-amp reading on the recovered schematic places the AGC actuator at the BFG97 LO-buffer collector summing junction, not the X50 cascade-amp gate. The §7F section retains the AT-42085 NPN cascade bench-trace as a correct description of an upstream LO-chain stage; only the "ALC actuator hypothesis" framing is moved here.

> ⚠ **§7F ALC-actuator hypothesis SUPERSEDED by §7D (γ).** The
> original premise of this section — that R&S close the X21 LO ALC
> loop by varying the **gate bias of the X50 cascade amp**, with
> the 5160 (then "R4D-B") pin 6 driving an actuator transistor onto
> the 1501 → Node B path — is **withdrawn**. The §7D γ trace shows
> the AGC actuator is the **BFG97 LO-buffer collector** (joined
> 3866 / 5160 pin 6/7 collector outputs sum onto the BFG97 collector
> tab through 100 Ω + LC), not the X50 cascade-amp gate. The X50
> cascade-amp topology bench-traced below remains a correct
> description of an upstream LO-chain stage and is retained for
> reference; the "ALC actuator hypothesis" subsection and its
> Node B / P2 / U1–U3 readings are **historical FA record** and
> should not be acted on as a rebuild discriminator. Use Table D
> rows 7c/7d/7e (BFG97 collector network) as the actuator-path
> verification instead.

### H-2026-04-30-7f-gaas-fet-id-superseded

**Moved from** [`smp_hw_diag.md` §Step 7F "420 MMIC identification" banner](smp_hw_diag.md#step-7f--x50--v50v60-lo-cascade-amp-bench-tracing-side-b-optional-during-rebuild) **on** 2026-04-30.
**Superseded by:** schematic-confirmed AT-42085-B NPN Si bipolar identification (current truth in §7F.0 of `smp_hw_diag.md`). The bench-trace observations originally collected under the GaAs FET reading are retained verbatim in the §7F "Bench-traced observations (retained for reconciliation)" subsection, since they remain useful as raw data even after the device class was corrected.

> ⚠ **Earlier "discrete 4-lead GaAs FET / PHEMT" identification
> SUPERSEDED 2026-04-30 by schematic.** The bench-trace data below
> was originally read as a GaAs FET cascade with shared negative-rail
> gate bias (Avantek ATF-13135 / ATF-13284 / ATF-10135 candidates).
> That reading is **withdrawn** — the schematic identifies
> AT-42085-B NPN Si bipolar. Bench observations are retained verbatim
> below for reconciliation: the solder-blob GND on pin 4 of the left
> chip is **consistent with NPN emitter** under the schematic ID
> (AT-42085 standard pinout puts Emitter on a corner pin); the
> −10.6 V open-circuit divider calculation, however, **does not
> reconcile with NPN base biasing** (V_BE wants ≈ +0.7 V, not
> −10.6 V). **OPEN: device-class / pin-mapping reconciliation** —
> either the bench-traced 3570 / 1500 / 1001 divider corresponds to
> a different schematic net than was assumed (R-values mismatch with
> the schematic R49 / R59 expected on this leg), or the pin-1-to-
> silkscreen indexing was rotated on the bench trace. To be cleared
> at the next bench session by DMM diode-test on V50 in-circuit +
> R-value sweep on the divider against schematic R49 / R59 (see
> action items in [smp_next.md](smp_next.md)).


### H-2026-05-05-a08-msa0885-superseded

**Moved from** [`smp_hw_diag.md` §7G A08 bench-confirmed-contents bullet](smp_hw_diag.md) **on** 2026-05-05.
**Superseded by:** MAR-8 identification per recovered schematic (V75 = MAR-8), confirmed by Step 10a VNA S21 measurement 2026-05-05 (passband +31.4 … +31.55 dB at 10–80 MHz matches MAR-8 datasheet ~32 dB at 100 MHz; falsifies MSA-0885 ~22.5 dB).

**Superseded / retracted:**

The following MSA-0885 identification and associated gain figures appeared
in `smp_hw_diag.md` §7G A08 bullet (authored 2026-04-29) and propagated to
the A21 connector-interface table (X75 row), the symptom paragraph, Step 9,
Step 10 config 2 expected gain, Step 10a expected gain, and the §7G
sourcing block. All instances have been swept to MAR-8 / +32 dB as of
2026-05-05.

Original §7G part-ID paragraph (verbatim):

> Marking decode (Avantek/HP house code via the qsl.net `on7pc` MMIC
> marking-cross-reference table — row reads literally
> `MAR-8 ∥ MSA0885 ∥ A08 ∥ Blue`): **`A08` = Avantek MSA-0885**, a
> low-noise silicon bipolar Darlington gain block, equivalent to
> **Mini-Circuits MAR-8** (and drop-in successor MAR-8A+). This is
> **not** an INA-series part — INA marking convention is the 3-digit
> part-number prefix (INA-03184 = `031`, INA-10386 = `103`), so the
> `A08` mark is uniquely Avantek MSA. **Specs:** DC – 1 GHz BW,
> ~22.5 dB gain @ 100 MHz, ~+12.5 dBm P1dB, ~3.5 dB NF,
> unconditionally stable

Original sourcing paragraph (verbatim):

> **Sourcing if ever needed:** like-for-like MSA-0885 / MSA-0885-BLK is
> NOS only (rfparts.com, jotrin, datasheetarchive brokers); modern
> drop-in is **Mini-Circuits MAR-8A+** (HBT, same micro-X pinout,
> **same recommended bias point of 36 mA / 7.8 V — drops in on the
> existing 195 Ω bias R without modification**, DC – 1 GHz, ~31 dB
> gain at 100 MHz — ~8–10 dB hotter than the original, budget into
> the X70 → X75 padding); **MAR-6+** (~20 dB at 100 MHz) matches the
> original MSA-0885 gain more closely if the extra MAR-8A+ gain is
> undesirable.

The MSA-0885 identification was inferred from the Avantek house-code
cross-reference (`A08` top-mark → MSA-0885) and the bias-point match
(I_d 36.9 mA / V_d 7.8 V). Both inferences remain factually correct —
MSA-0885 and MAR-8 share the same Avantek house code and the same
recommended operating point — but the gain figure (~22.5 dB for
MSA-0885 vs. ~32 dB for MAR-8) discriminates between them, and the
Step 10a bench S21 at +31.5 dB matches MAR-8 only. The recovered
schematic (drawing 1035.8840.01, sheet 02/02) explicitly labels V75
as MAR-8, confirming the bench finding.


## From `smp_next.md`

### H-2026-04-30-open-question-schematic-supersession

**Moved from** [`smp_next.md` §Open question, Schematic-driven supersession quote-block](smp_next.md#open-question) **on** 2026-04-30.
**Superseded by:** Branch (b) of the open question (chips alive; "≈ 105 Ω" is base-pin-to-rail = R44 + L43 DCR + R41 ≈ 105 Ω). §7D D.3 fully SUPERSEDED in `smp_hw_diag.md`; §7F doubler-location and §7G push-pull-vs-detector RESOLVED. D.5 + Step 8a remain the bench verifications.

> ✓ **Schematic-driven supersession 2026-04-30 — branch (b) is the
> heavy favorite by inspection.** Recovered schematic (sheet 02/02
> of A211 var.02; filed at
> [`rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg`](rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg))
> shows V3 (MRF3866) and V4 (MRF5160) as a class-AB push-pull
> RF power-output stage. Bias-network detail (per the §7D DEEPER
> SCHEMATIC RE-READ banner in `smp_hw_diag.md`, 2026-04-30):
> **L41 / L43 470 nH are base-bias RFCs** in series with R43 / R44
> 100 Ω from ±15 V to the V3 / V4 base nodes; **R40 / R41 3R92
> emitter resistors tie the V3 / V4 emitter pours directly to
> ∓15 V** (no choke in series); the V3 / V4 collectors are tied
> together and feed L45 54 nH + C49 10 P → off-page → X21. The
> "≈ 105 Ω" reading on the bench is therefore **not** a C-E path
> through "choke + 100 Ω + 3R92" (no such collector path exists);
> it is most plausibly a base-pin-to-rail measurement (R44 + L43
> DCR + R41 ≈ 100 + ~1 + 4 ≈ 105 Ω) on a base pin. §7D D.3 has
> been **fully SUPERSEDED** in `smp_hw_diag.md` per user decision
> 2026-04-30, and the chips-alive verdict still stands; only the
> circuit-rationale of the "105 Ω" coincidence has shifted from
> collector-network to base-network. The §7F doubler-
> location and §7G push-pull-vs-detector open questions are
> **RESOLVED** by the same schematic — see resolved banners in
> `smp_hw_diag.md`. **D.5 + Step 8a together remain the bench
> verifications** that close the chips-alive verdict on this
> instrument; the rebuild rationale that called for pulling the
> two MRF chips is dropped.

### H-2026-04-30-d5-revised-collector-vs-base-bias

**Moved from** [`smp_next.md` §Decision gate — D.5 cross-check, Revised banner](smp_next.md#decision-gate--d5-cross-check-instrument-off-ohm-mode-5-min) **on** 2026-04-30.
**Superseded by:** Revised D.5 probe table immediately below (probes built on the corrected base-bias topology: L41 / L43 = base-bias RFCs, R43 / R44 100 Ω = base-feed resistors).

> **Revised 2026-04-30** to match corrected bias topology — see the
> §7D DEEPER SCHEMATIC RE-READ banner in `smp_hw_diag.md`. The
> previous table's "BFG97 col tab → ±15 V via collector-load L" /
> "3866 / 5160 pin 7 → BFG97 col tab via 100 Ω" probes were built
> on the wrong "L41 / L43 = collector chokes, 100 Ω = collector
> summing R" reading and are withdrawn.

## From `smp_a21_modernization.md`

### H-2026-04-26-original-drop-in-constraint

**Moved from** [`smp_a21_modernization.md` §Module envelope, "Original drop-in constraint" block + 4 bullets](smp_a21_modernization.md) **on** 2026-04-30.
**Superseded by:** [`smp_a21_modernization.md` §Architecture decision (2026-04-26): lateral carrier topology](smp_a21_modernization.md#architecture-decision-2026-04-26-lateral-carrier-topology). New chassis built around the compound FR-4 + carrier-extension outline (~82 D × 100 H mm); X211 stays on Rogers; daughter mounts laterally on a carrier extension over a Samtec ERM8/ERF8 BTB.

**Original drop-in constraint (superseded)** — the original design
intent was to fit the new module inside the existing 57 × 116 × 23 mm
grey case. That constraint was relaxed when the design moved to a
new chassis built around the compound FR-4 + carrier-extension
outline (see *Architecture decision (2026-04-26): lateral carrier
topology*). The original measurements are still useful as the
**neighbour-slot envelope** the new chassis has to live inside:
≤ 57 mm in D, ≤ 116 mm in H, and ≤ ~31 mm in W (23 mm original +
≥ 8 mm free headroom on one face). The four bullets below predate
the lateral-carrier decision; references to a stacked daughter, SMP
bullets, and X211 migration to the FR-4 main are **superseded** —
specifically: the FR-4 outline is compound, X211 stays on Rogers,
and the daughter mounts laterally on a carrier extension. The
bullets are kept for context on how the W / D / H budgets were
originally reasoned about:

- **FR-4 main board outline** — the placeholder ~80 × 120 mm target
  (Bare-board fab table and Bucket E) **exceeds the envelope on the
  depth axis** (80 mm vs 57 mm clear) and is marginal on the vertical
  axis (120 mm vs 116 mm clear). Maximum usable main-board core
  outline is ≈ **55 × 114 mm** after allowing ~1 mm clearance per edge
  inside the casing, plus an **8 × 28 mm W216 tab** projecting at one
  end of a long edge (matching the original A211). Layout must be
  re-floorplanned against this footprint before fab — see Open Items.
- **Z-stack relaxed** — with ≥ 31 mm W available, the FR-4 main
  (1.6 mm) + 5–6 mm board gap + Rogers daughter (0.51 mm) + SMP bullet
  + standoffs + shield-can lid clears with > 20 mm of slack. The earlier
  worry about fitting the stack inside the original 23 mm casing
  thickness is moot. The W headroom also opens the option of taller
  through-hole parts (electrolytic bulk caps, larger LDO heatsinks,
  TO-252 / TO-263 packages on the AVA-drain LDO) without forcing them
  off-module. The 7 mm SMB pocket lives on the **opposite** W face
  from the new daughter/Rogers stack, so SMB body height does not
  interact with the two-board sandwich.
- **Connector edge geometry inherited from A211** — the W216 tab,
  X50 SMB, and X75 SMB cluster on one long (116 mm) edge of the new
  FR-4 main (the "I/O face"), with the W216 tab projecting 8 × 28 mm
  at one end of that edge. **X211 (3.5 mm RF in)** migrates from the
  now-deleted milled microwave casing onto **the same long (116 mm)
  edge** of the FR-4 main at **H ≈ 88 mm** (28 mm in from the opposite
  short end from the W216 tab), axis along D, parallel to the SMB
  cluster — this preserves the original chassis cable routing height
  for X211 while consolidating all I/O on a single face. A new chassis
  cutout in the grey case long D-face is required at H = 88 mm. The RF
  then crosses to the Rogers daughter via an SMP bullet hop.
- **Rogers daughter (25 × 40 mm) fits well inside the freed grey
  case interior**, sited adjacent to the X211 launch on the long
  edge so the bullet hop is short. (The original milled casing
  footprint of 40 × 60 mm is no longer relevant as a daughter
  outline constraint, since the milled casing is being deleted and
  its volume is not used by the new PCB.)

### H-2026-04-26-connectors-substrate-shielding-banner

**Moved from** [`smp_a21_modernization.md` §Connectors, substrate, shielding intro banner](smp_a21_modernization.md) **on** 2026-04-30.
**Superseded by:** [`smp_a21_modernization.md` §Architecture decision (2026-04-26): lateral carrier topology](smp_a21_modernization.md#architecture-decision-2026-04-26-lateral-carrier-topology) + BOM Bucket F table. Board-to-board interconnect is **1× Samtec ERM8/ERF8 20-pin vertical-mate BTB + 4× M2 brass standoffs (L = 7 mm)**; shielding is **Laird BMI-S-205-F + BMI-S-205-C** two-piece SMD cans.

> **Superseded by *Architecture decision (2026-04-26): lateral
> carrier topology* (lines 108–172) and the BOM Bucket F table.**
> The board-to-board interconnect rows in the table below (SMP
> bullets, SMP-MSSB jacks, FTS/CLM 2×3 header, M2.5 standoffs) are
> all replaced by **1× Samtec ERM8/ERF8 20-pin vertical-mate BTB +
> 4× M2 brass standoffs (L = 7 mm)**. The shielding row was retro-
> fitted in place to **Laird BMI-S-205-F + BMI-S-205-C** two-piece
> SMD cans. The X211 / X50 / X75 / W216 / substrate rows remain
> current. Historical SMP / FTS-CLM rows are retained below for
> context only — do not source against them.

## From `smp_diag.md`

### H-2026-04-30-next-actions-item-1-superseded

**Moved from** [`smp_diag.md` §Next actions, banner over item 1](smp_diag.md#next-actions) **on** 2026-04-30.
**Superseded by:** [`smp_hw_diag.md` §7D DEEPER SCHEMATIC RE-READ banner](smp_hw_diag.md#step-7--a21-bias--a211-comparator-state-measure-dc-voltage-only-if-step-4-shows-x75-dead-with-inputs-present) and the four-test bench decomposition in [`smp_next.md` Status section](smp_next.md).

> ⚠ **NEXT-ACTIONS ITEM 1 SUPERSEDED 2026-04-30** by recovered A211
> schematic (sheet 02/02 of A211 var.02, drawing 1035.8840.01;
> filed at
> [`rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg`](rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg)).
> The two "Motorola R4D SOIC-8 op-amps" called out in the original
> next-action paragraph are not op-amps — they are **MRF3866 (V3,
> NPN)** and **MRF5160 (V4, PNP)** RF transistors wired as a
> class-AB **push-pull LO power-output stage**. Bias network per
> the recovered schematic: **L41 / L43 (470 nH) are base-bias RFCs**
> in series with R43 / R44 100 Ω from each ±15 V rail to the V3 / V4
> base nodes; **R40 / R41 (3R92) emitter resistors tie the V3 / V4
> emitter pours directly to ∓15 V** (no choke in series); collectors
> are tied together and feed L45 54 nH + C49 10 P to X21. The
> "mirror-symmetric pinned-to-rail" readings and the "fused-open
> per-chip supply filter" narrative are the **expected DC paths
> through this bias network**, not silicon failure / fused-filter
> signatures. (Bias-network detail corrected per `smp_hw_diag.md`
> §7D DEEPER SCHEMATIC RE-READ banner 2026-04-30; the earlier
> "doubled collectors driven through L41 / L43 chokes" framing in
> this banner is **withdrawn** — the push-pull / chips-presumed-
> alive verdict is unchanged.) The §7D D.3 verdict in
> [`smp_hw_diag.md`](smp_hw_diag.md) is **fully SUPERSEDED**;
> chips are presumed alive pending Step D.5 DMM cross-check + Step
> 8a bench-PSU LO-chain RF validation. **The MC34071DR2G silicon-pull
> rebuild is on hold.** New next action is the four-test bench
> decomposition tracked in [`smp_next.md`](smp_next.md) Status section:
> (1) D.5 — DMM cross-check, ~5 min; (2) Step 10a — IF chain on
> bench, ~15 min; (3) Step 8a — LO chain on bench, ~30 min, gated
> on D.5; (4) Step 8b — milled casing standalone, ~30 min; (5) sys
> — `--a21-probe` after reassembly. If a silicon-pull eventually
> turns out to be required, the resolved sourcing pair is
> **MRF3866 / MRF5160 like-for-like** *or* **NTE2511 / NTE2512**
> (NTE TO-39 direct cross-references for 2N3866 / 2N5160 — sustained
> current production at TME / Newark, eliminates the SO-8 / TO-39
> NOS-channel risk; datasheet
> <https://www.tme.eu/Document/5321375d488a24e92c8cfb7f10d897a0/nte2511.pdf>).
> The §2 narrative below is retained verbatim for FA traceability.

### H-2026-04-30-tp1605-wrong-sign-retracted

**Moved from** [`smp_diag.md` §Per-module status A9 sub-section](smp_diag.md#per-module-status) **on** 2026-04-30.
**Superseded by:** A9 module verdict — multi-path DAC behaviour within zero-scale tolerance; QC=128 latch hypothesis retracted; 6199 board variant has no V240/V250 (see current A9 narrative in `smp_diag.md`).

**Superseded / retracted:** earlier TP1605 "wrong sign" and
TP1603 offset diagnoses retracted (multi-path DAC; within zero-scale
tolerance). QC=128 "power-up latch" hypothesis retracted — the
fresh-boot capture shows it is live. 6301-spec false-FAILs on TP1604 /
TP1606 / TP1609 / TP1610 / TP1611 and the "missing VA10.5 collector
supply to V240/V250" hypothesis are void (6199 board has no V240/V250).

### H-2026-04-30-step-7d-failure-chain-superseded

**Moved from** [`smp_diag.md` §Per-module status A21/A211 sub-section, §2 STEP 7D banner](smp_diag.md#per-module-status) **on** 2026-04-30.
**Superseded by:** [`smp_hw_diag.md` §7D DEEPER SCHEMATIC RE-READ banner](smp_hw_diag.md) and [H-2026-04-30-next-actions-item-1-superseded](#h-2026-04-30-next-actions-item-1-superseded). Chips presumed alive (V3 = MRF3866 NPN + V4 = MRF5160 PNP push-pull) pending Step D.5 + Step 8a bench validation. The wrong narrative immediately below the original banner location in `smp_diag.md` is **retained in-place for FA traceability** per the original banner instruction.

> ⚠ **§2 STEP 7D FAILURE-CHAIN NARRATIVE BELOW IS SUPERSEDED
> 2026-04-30** by recovered A211 schematic — see top-of-file
> banner over Next-actions item 1, and `smp_hw_diag.md` §7D D.3
> SUPERSEDED banner. Headline: the "two dead R4D op-amps + two
> fused-open per-chip supply filters + stressed A0 detector"
> failure chain reads instead as the **expected DC behavior of a
> healthy class-AB push-pull RF power stage** (V3 = MRF3866 NPN +
> V4 = MRF5160 PNP), with the bias network per the recovered
> schematic: L41 / L43 470 nH base-bias RFCs in series with
> R43 / R44 100 Ω from ±15 V to the base nodes; R40 / R41 3R92
> emitter resistors directly to ∓15 V; collectors tied → L45 / C49
> output match → X21. The A0 SOT-23 in the middle compartment is
> bench-traced as the DIAGSAMP envelope rectifier (HSMS-2800-B per
> family ID — V61 / V62 in the FREQUENCY DOUBLER block are two
> further HSMS-2800 instances drawn on the schematic; the third
> rectifier on the X21 RF tap is bench-traced but **not visible**
> on the available JPEG, almost certainly off the right margin of
> sheet 02/02 — see `smp_hw_diag.md` §7D DEEPER SCHEMATIC RE-READ
> banner items 2 and 3, plus item 1 for the bias-network correction).
> Chips presumed alive pending Step D.5 + Step 8a bench validation.
> Text retained for FA traceability.

### H-2026-04-30-a7-step-synth-marginal-retired

**Moved from** [`smp_diag.md` §Per-module status A21 narrative](smp_diag.md#per-module-status) **on** 2026-04-30.
**Superseded by:** A7 re-measured all-in-spec against the authoritative band-2 p.115 ranges (see current §3 A7 narrative in `smp_diag.md`).

**Superseded / retracted:** "A7 step-synth marginal → A21 cascade"
hypothesis was retired when A7 re-measured all-in-spec against the
authoritative band-2 p.115 ranges (see §3).

### H-2026-04-30-tp1802-sign-inversion-retracted

**Moved from** [`smp_diag.md` §Per-module status A10 sub-section](smp_diag.md#per-module-status) **on** 2026-04-30.
**Superseded by:** TP1802 verdict — positive per §7.4.2 `U1 = 8…12 V` and in spec on this unit (see current A10 narrative table in `smp_diag.md`).

**Superseded / retracted:** earlier "TP1802 sign-inversion / summing-
stage" diagnosis was a mis-binding of the p.163 formula's `V1` — TP1802
is positive per §7.4.2 `U1 = 8…12 V` and in spec on this unit. The
band-1 p.108 / band-2 p.168 TP-table entry giving TP1802 = `−12…−0.8 V`
is either an OCR artefact or refers to a tap upstream of a buffer
inversion; §7.4.2 is treated as the measurement-procedure authority.
Spec-window bugs in `smp_diag.py` / `smp_test.py` TP1802 checks are
follow-up cleanup (details below).

### H-2026-04-30-att-reseat-helps-retired

**Moved from** [`smp_diag.md` §Per-module status A19 attenuator narrative](smp_diag.md#per-module-status) **on** 2026-04-30.
**Superseded by:** A19 40 B section verdict — deterministic ID-line pull-to-ground, not intermittent (see current A19 narrative table in `smp_diag.md`).

**Superseded / retracted:** earlier "reseat helps, regresses"
intermittency theory is retired — the reseat only "helped" because
preceding operations left the attenuator at 0 dB (40 B in THRU); any
subsequent high-att use drove 40 B back into ATT and TP1914 back to
ground.

### H-2026-04-30-tp0305-and-a7-marginality-retired

**Moved from** [`smp_diag.md` §Per-module status A8/A7 narrative](smp_diag.md#per-module-status) **on** 2026-04-30.
**Superseded by:** A8 6a/6b current narrative in `smp_diag.md` — TP0305 in spec at manual's test condition (`:FREQ 1 GHz`), A7 re-measured all-in-spec, A8 boot err 221 reclassified as separate sub-loop intermittent.

**Superseded / retracted:**

- "TP0305 = 11.24 V is below spec" retired — the 12–20 V window
  applies at `:FREQ 1 GHz`, not at preset. At 1 GHz the reading is
  17.54 V (in spec).
- "A7 reference marginality drives the buffer-VCO intermittency"
  retired now that §3 A7 re-measures all-in-spec.
- Earlier "A8 OK" classification in the `## Modules OK` section is
  partially superseded: standard DDS sweep still passes, but the boot
  err 221 is on a separate sub-loop not covered by that test.

## From `smp_fan.md`

*(no entries — `smp_fan.md` contains no superseded readings or
historical narrative as of the 2026-04-30 migration. The single
"recovered" hit on regex scan was a corpus-availability note, not
a superseded reading.)*

