# smp_next.md — A21 / A211 next-bench-session tracker

Companion to `smp_hw_diag.md`. Captures the single open question that
blocks the next decision (rebuild vs. hunt elsewhere) and the minimum
probe set that resolves it. Full context, history, and reconciliation
narrative live in `smp_hw_diag.md` §7D.4 / §7D.5 / §7D.6.

> **Historical / superseded content** is moved to
> [`smp_history.md`](smp_history.md). Inline supersession markers in
> this doc point to specific anchors there. The doc body itself
> always reflects current truth.

## Open question

Is the **105 Ω C-E reading** on both MRF3866 and MRF5160:

  (a) on-die silicon C-E latch-up (original §7D D.3 verdict), **or**
  (b) the in-circuit external network sum (100 Ω summing R + collector-
      load L DCR + 3R92), with both chips actually **alive**?

> Superseded 2026-04-30 — full schematic-driven supersession quote-block
> moved to
> [`smp_history.md#H-2026-04-30-open-question-schematic-supersession`](smp_history.md#h-2026-04-30-open-question-schematic-supersession).
> Current verdict: branch (b) is the heavy favourite — chips alive; "≈ 105 Ω"
> is base-pin-to-rail = R44 + L43 DCR + R41 ≈ 105 Ω. §7D D.3 fully SUPERSEDED
> in `smp_hw_diag.md`; §7F / §7G open questions RESOLVED. D.5 + Step 8a
> remain the bench verifications; rebuild silicon-pull on hold.

Diode-mode junction sweep already done (§7D.4) reads **healthy
junctions** on the 3866 and **mostly healthy** on the 5160 (B-E forward
shows series-cap charging signature, not a damaged junction). That
points strongly toward (b), and is now corroborated by the schematic
above.

**Resolution path (revised 2026-04-30):** D.5 (DMM cross-check)
remains the cheapest sanity sweep before powering the LO chain on
the bench — it confirms the choke + 100 Ω + 3R92 network reads as
expected per the schematic. **Step 8a** (bench-PSU LO-chain RF test,
board out) is the next direct RF validator: a clean X21 spectrum at
8a end-to-end settles the silicon question by exclusion. D.5 + 8a
together close §7D D.3 in the "chips alive" direction; the rebuild
silicon-pull is on hold.

## Decision gate — D.5 cross-check (instrument off, ohm mode, ~5 min)

> Superseded 2026-04-30 — full "Revised D.5 probes" banner moved to
> [`smp_history.md#H-2026-04-30-d5-revised-collector-vs-base-bias`](smp_history.md#h-2026-04-30-d5-revised-collector-vs-base-bias).
> Current verdict: D.5 probe table below uses the corrected base-bias
> topology (L41 / L43 = base-bias RFCs; R43 / R44 100 Ω = base-feed Rs).

```
+---+-----------------------------------------+-----------+----------------------------+
| # | Probe                                   | Expected  | Tells us                   |
+---+-----------------------------------------+-----------+----------------------------+
| 1 | V3 pin 1/4/5/8 (3866 emitter pour)      |  ~3.92 Ω  | confirms R41 3R92 emitter  |
|   |   → −15 V rail                          |           | tie to −15 V is intact     |
| 2 | V4 pin 1/4/5/8 (5160 emitter pour)      |  ~3.92 Ω  | confirms R40 3R92 emitter  |
|   |   → +15 V rail                          |           | tie to +15 V is intact     |
| 3 | V3 pin 6/7 (3866 base node)             |  ~101 Ω   | confirms R44 100 Ω +       |
|   |   → −15 V rail                          |           | L43 470 nH base-bias path  |
| 4 | V4 pin 6/7 (5160 base node)             |  ~101 Ω   | confirms R43 100 Ω +       |
|   |   → +15 V rail                          |           | L41 470 nH base-bias path  |
| 5 | V3 pin 2/3 (3866 collector tie)         |  sub-Ω    | confirms collectors are    |
|   |   ↔ V4 pin 2/3 (5160 collector tie)     |           | board-tied as drawn        |
| 6 | V3 pin 2/3 collector tie                |    OL     | confirms collectors are    |
|   |   → +15 V rail (and same to −15 V)      |           | NOT DC-tied to either rail |
|   |                                         |           | (output match is L45 → C49 |
|   |                                         |           | DC-block to off-page X21)  |
| 7 | V3 pin 6/7 base ↔ V4 pin 6/7 base       |  ~few kΩ  | confirms inter-base tie    |
|   |   (across R42 4K75 + L40 / L42 39 nH)   |           | network is intact          |
+---+-----------------------------------------+-----------+----------------------------+
```

Outcome branches:

```
+--------------------------+------------------------------------------+
| Cross-check result       | Action                                   |
+--------------------------+------------------------------------------+
| All as expected          | §7D D.3 superseded; silicon likely ALIVE.|
|                          | DEFER rebuild step 2. Re-open trigger    |
|                          | hunt elsewhere on A21 (BFG97 stage,      |
|                          | OP97 N90, X21 LPF, §7G monitor block,    |
|                          | comparator-input divider stub — see      |
|                          | next-bench-trace plan below).            |
| Probe 1 / 2 off          | Open R40 / R41 3R92 emitter resistor     |
|                          | (or cracked emitter pour bond). Repair   |
|                          | before fitting fresh silicon.            |
| Probe 3 / 4 off          | Open base-bias path (L41 / L43 470 nH    |
|                          | choke open, R43 / R44 100 Ω blown, or    |
|                          | base-pin pad lifted). Repair before      |
|                          | fitting fresh silicon.                   |
| Probe 5 off              | Collector-tie trace cracked. Repair      |
|                          | before fitting fresh silicon.            |
| Probe 6 reads few Ω      | Short across L45, C49 fused leaky, or    |
|                          | downstream X21-side network shorted to   |
|                          | rail. Trace before powering up.          |
| Probe 7 OL               | R42 / L40 / L42 inter-base network open. |
|                          | Investigate before re-powering.          |
| All as expected BUT 5160 | Proceed to D.6 desolder of 5160 only     |
|   B-E persistently odd   | for out-of-circuit confirmation.         |
+--------------------------+------------------------------------------+
```

### Bench results — 2026-05-03 (D.5 PASSED)

In-circuit DMM ohm sweep, instrument off, casing on. All seven probes
land on the "all as expected" branch above; chips alive, bias network
intact, output match DC-blocked as drawn.

```
+---+--------------------------------------+----------+--------------+--------+
| # | Probe                                | Expected | Measured     | Verdict|
+---+--------------------------------------+----------+--------------+--------+
| 1 | V3 emit pour (pin 1/4/5/8) → −15 V   | ~3.92 Ω  | 5.3 Ω        | PASS   |
| 2 | V4 emit pour (pin 1/4/5/8) → +15 V   | ~3.92 Ω  | 5.4 Ω        | PASS   |
| 3 | V3 base node (pin 6/7)    → −15 V    |  ~101 Ω  | 102.6 Ω      | PASS   |
| 4 | V4 base node (pin 6/7)    → +15 V    |  ~101 Ω  | 102.3 Ω      | PASS   |
| 5 | V3 pin 2/3 ↔ V4 pin 2/3 (collectors) |  sub-Ω   | 0.2 Ω        | PASS   |
| 6 | V3 pin 2/3 collector tie  → ±15 V    |   OL     | OL           | PASS   |
| 7 | V3 pin 6/7 ↔ V4 pin 6/7 (inter-base) |  ~few kΩ | 2.64 kΩ      | PASS   |
+---+--------------------------------------+----------+--------------+--------+
```

Notes:

- Probes 1 / 2 read ≈ 5.3-5.4 Ω vs. the 3.92 Ω expected — DMM lead
  offset ≈ 1.4 Ω accounts for the difference; the resistors themselves
  are healthy and the emitter pour-to-rail bond is intact.
- Probes 3 / 4 land within 1.5 % of the 101 Ω schematic prediction
  (R43 / R44 100 Ω + L41 / L43 470 nH DCR) — base-bias path on both
  chips intact.
- Probe 5 = 0.2 Ω confirms the V3 / V4 collectors are commoned on the
  copper as drawn; probe 6 = OL confirms the L45 / C49 output match
  is the only DC path off that node (no rail short).
- Probe 7 = 2.64 kΩ matches the ~few kΩ band predicted by R42 4K75 +
  L40 / L42 inter-base network.

**Verdict:** §7D D.3 silicon-latch-up hypothesis is bench-falsified at
the ohm-cross-check level. The MRF3866 / MRF5160 push-pull pair are
**alive**; bias network around them (R40 / R41 3R92, R43 / R44 100 Ω,
L41 / L43 470 nH, R42 4K75, L40 / L42 39 nH, L45 / C49 output match)
is intact. Silicon-pull rebuild (§7E step 2) is **formally on hold**.
The remaining open question on the LO-amp half is settled by RF
validation only — Step 8a (out-of-casing, board on bench) or Target 4
(in-instrument R65 split-test) closes it by exclusion.

> **Doc-bug flagged for follow-up — pin-numbering convention.** Two
> conventions coexist in `smp_hw_diag.md` for V3 / V4 (MRF3866 /
> MRF5160 in SO-8):
>
> - **Convention A** (this D.5 table; §7D D.0 line ~784 paragraph
>   "Collector output: pins 2 / 3 of each SO-8"; bench-confirmed by
>   probes 5 + 6 above): **pin 2/3 = collector**, **pin 6/7 = base**,
>   pin 1/4/5/8 = emitter pour.
> - **Convention B** (part-bind table at `smp_hw_diag.md` L1201-1202;
>   §7G post-rebuild expectation tables L1455-1461; Table D rows
>   7a-7e narrative L985 / L992 / L1004-1017 / L1117-1144):
>   **pin 2/3 = base**, **pin 6/7 = collector**, pin 1/4/5/8 = emitter
>   pour.
>
> The D.5 readings discriminate decisively in favour of Convention A:
> probe 5 (V3 pin 2/3 ↔ V4 pin 2/3 = 0.2 Ω) and probe 6 (V3 pin 2/3 →
> ±15 V = OL) only fit a DC-blocked output node, which the schematic
> places on the **collectors** via L45 / C49 — i.e. on the pin 2/3
> pair under Convention A. Under Convention B those probes would land
> on the base group, which is DC-tied to the rails through R43 / R44
> + L41 / L43 (≈ 101 Ω, not OL) and would show ≈ 200 Ω cross-chip
> through the inter-base R42 path (not 0.2 Ω). The bench data is
> internally consistent with itself and with the recovered schematic
> only under Convention A.
>
> Convention B is therefore presumed to be a stale carry-over from
> the pre-2026-04-30 part-bind work that assumed the standard
> Motorola Case 751-05 Style 1 datasheet pinout without bench
> verification. Cleanup is **non-blocking** — neither the rebuild
> decision nor any downstream bench step depends on which convention
> the doc body uses, only on the bench data itself. Queued as
> follow-up: confirm the chip-silkscreen pin-1 marker against the
> probed pad on a future bench session, then sweep `smp_hw_diag.md`
> to land on a single convention.

## D.6 confirmation by desolder (optional, only if D.5 ambiguous)

Pull **5160 only** (smaller, the chip with the ambiguous B-E reading,
cheaper to risk on rework). Re-run full Tier B junction battery
out-of-circuit:

```
PNP (5160) healthy out-of-circuit  (SO-8 Case 751-05 Style 1:
  E = pins 1/4/5/8 quad-bonded, B = pins 2/3, C = pins 6/7)
+-------+--------------+--------------+-------+
| Test  | Red          | Black        | Read  |
+-------+--------------+--------------+-------+
| B-E F | E (1/4/5/8)  | B (2 or 3)   | ~0.65 |
| B-E R | B (2 or 3)   | E (1/4/5/8)  |  OL   |
| B-C F | C (6 or 7)   | B (2 or 3)   | ~0.65 |
| B-C R | B (2 or 3)   | C (6 or 7)   |  OL   |
| C-E   | E (1/4/5/8)  | C (6 or 7)   |  OL   |
| E-C   | C (6 or 7)   | E (1/4/5/8)  |  OL   |
+-------+--------------+--------------+-------+
```

Plus bond sanity (1↔4↔5↔8 < 0.5 Ω, 2↔3 < 0.5 Ω, 6↔7 < 0.5 Ω).

**If 5160 reads clean OOC:** §7D D.3 fully overturned. Reflow 5160
back, leave 3866 in place, hunt elsewhere.

**If 5160 reads damaged OOC (C-E short or B-E open):** D.3 confirmed
for the 5160; re-evaluate the 3866 separately (most likely also pull
it given they failed as a complementary pair).

## RF probes — doubler location + 3866/5160 role

**Vehicle (revised 2026-04-29):** these probes are now folded into
**Step 8a** (bench-PSU LO chain, board out) — easier access with the
PCB on the bench than in-instrument, and runnable **before** the §7E
rebuild. The original "post-rebuild, in-instrument" variant is the
fallback if any 8a probe reads ambiguous (or as a final end-to-end
sanity check after reassembly).

Two open questions previously added to `smp_hw_diag.md` 2026-04-29 are
both **RESOLVED 2026-04-30** by the recovered schematic:

- **§7F Doubler location (H) — RESOLVED.** Schematic locates the
  discrete doubler in the FREQUENCY DOUBLER block: V50 + V60 (both
  AT-42085-B NPN Si bipolar) drive the **V61 + V62 (HSMS-2800-B
  Schottky pair)** that performs the actual 2f generation; the
  cascade and the diode pair sit upstream of the BFG97 base node.
  Candidate (a) is confirmed in spirit (the 420 cascade is the
  doubler drive), with the explicit 2f generation in V61 / V62
  rather than in the BJT base-drive nonlinearity. Candidates
  (b)/(c)/(d) are falsified.
- **§7G Device-rating anomaly (H) — RESOLVED.** Schematic confirms
  the MRF3866 / MRF5160 pair is the **class-AB push-pull LO
  power-output stage** driving X21 (combined ≈ 2 W envelope matches
  the +26…+30 dBm spec), with the BFG97 (V2) wired explicitly as
  the pre-driver. The §7G γ collector-modulated AGC topology is
  withdrawn.

The bench checks below were originally framed to discriminate
between the AGC and power-amp readings; with the topology now
resolved by the schematic, they are downgraded to **bring-up sanity
checks for Step 8a** rather than topology disambiguators.

### Bench checks (single most informative first)

| # | Probe                                                       | Tool     | Discriminates                                                                                                            |
|---|-------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| 1 | DC V across 3R92 on each chip (3866 pour ↔ −15 V; 5160 pour ↔ +15 V) **= Step 8a procedure step 7** | DMM      | 4–40 mV ⇒ detector duty (AGC reading stands). 200–800 mV ⇒ class-AB power-output duty (power-amp reading wins).         |
| 2 | SA at X21 brass pin — **= Step 8a SA capture** (board out, bench PSU); in-instrument Step 8 is the post-rebuild fallback | SA       | Centre at 220 MHz ⇒ doubling done upstream of X21 (falsifies §7F (d)). Centre at 110 MHz ⇒ §7F (d) confirmed.           |
| 3 | SA at BFG97 collector tab (low-cap probe; bench during 8a, or in-instrument post-rebuild) | SA       | Level ≪ X21 ⇒ flow is BFG97 → 3866/5160 → X21 (power-amp). Level ≈ X21 minus small loss ⇒ inverse flow (AGC).           |
| 4 | SA at RIGHT 420 collector output (low-cap probe; bench during 8a, or in-instrument post-rebuild) | SA       | 220 MHz dominant ⇒ §7F (a) confirmed (420 cascade IS the doubler). 110 MHz dominant ⇒ doubler is downstream.        |
| 5 | SA at 3866 / 5160 commoned base node (low-cap probe; bench during 8a, or in-instrument post-rebuild) | SA       | Clean fundamental at −10 to 0 dBm ⇒ power-amp drive. < −20 dBm with rectification products ⇒ envelope sense tap.        |
| 6 | A08 (MAR-8) pin-4 DC + pin-1 RF-trace in X75 compartment | DMM + SA | **DONE 2026-04-29 (✓ ✓):** role (i) active IF post-amp CONFIRMED. Step 10a S21 2026-05-05 confirms MAR-8 gain (+31.5 dB). |

### Outcome interaction

Probe 1 is decisive on §7G and re-prioritizes the §7F probe order:

- **Power-amp reading (probe 1 reads 200–800 mV):** §7D γ "RESOLVED"
  header downgrades to "leading hypothesis" pending probe 3. §7F (a)
  — 420 cascade as doubler — moves to top of doubler-location list
  (the doubling has to sit upstream of the BFG97 base if the BFG97
  is the pre-driver). Run probe 4 next.
- **AGC reading (probe 1 reads 4–40 mV):** §7D γ verdict stands as
  resolved. Run probes 2 and 4 to localize the doubler; §7F (c)
  (BFG97 in compression) stays viable.

## Sourcing — already in §7E Replacements

If the bench validation eventually requires a silicon-pull (which
the §7D D.3 SUPERSEDED banner currently argues against), the
co-primary substitute pairs are:

- **2N3866** (NPN, TO-39) — user has on hand. Leg-dress to SO-8 Case
  751-05 Style 1 (1/4/5/8=E, 2/3=B, 6/7=C).
- **2N5160** (PNP, TO-39) — Jotrin / Radio741 NOS, see §7E line ~1112.
- **NTE2511** (NPN, TO-39) — NTE direct cross for 2N3866, sustained
  current production at TME / Newark, eliminates NOS-channel risk.
  Datasheet: <https://www.tme.eu/Document/5321375d488a24e92c8cfb7f10d897a0/nte2511.pdf>.
- **NTE2512** (PNP, TO-39) — NTE direct cross for 2N5160, the
  explicit complementary partner of NTE2511; same sourcing channels.

NTE pair listed alongside the 2N pair at equal priority — pick
whichever Co-primary lands in stock first.

## Files / sections to read on session resume

- `smp_hw_diag.md` §7D D.4 (lines ~852–968) — re-measurement findings,
  cross-check table, decision matrix.
- `smp_hw_diag.md` §7D Table D rows 1, 4a (lines 653–654) — original
  "FAIL" verdicts now flagged provisional.
- `smp_hw_diag.md` §7E rebuild steps 2 / 2a — formally on hold per
  D.5 PASS 2026-05-03; reopen only if Step 8a / Target 4 RF
  validation falsifies the chips-alive verdict.
- `smp_hw_diag.md` §7F "Doubler location — OPEN QUESTION (H)"
  (~line 1788, end of §7F before §7G heading) — 4-candidate
  hypothesis table for the missing discrete doubler.
- `smp_hw_diag.md` §7G "Device-rating anomaly vs. resolved-AGC
  role — OPEN QUESTION (H)" pending-work bullet (~line 2433) —
  BFG97-pre-driver / 3866-5160-push-pull-power-output alternative
  reading + 3 discriminating bench checks.
- `smp_hw_diag.md` §7G bench-confirmed-contents bullet on the
  **A08 / MAR-8 MMIC in the X75 middle compartment** (~line 2248)
  — MAR-8 per schematic V75, role (i) IF post-amp confirmed,
  sourcing (MAR-8A+ / MAR-6+).
- `smp_hw_diag.md` **Step 8a** (~line 2802) — bench-PSU LO chain,
  board out, no casing. Most direct §7D D.5 RF validator.
- `smp_hw_diag.md` **Step 8b** (~line 2955) — milled-casing
  standalone, A211 disconnected. Independent of every other step.
- `smp_hw_diag.md` **Step 10a** (~line 3141) — bench-PSU IF chain,
  board out, +15 V only. ~15 min, runnable before §7E rebuild.

## Status

```
[x] D.5 cross-check (7 probes, ~5 min) — PASSED 2026-05-03.
    All seven readings on the "all as expected" branch:
    1) 5.3 Ω, 2) 5.4 Ω, 3) 102.6 Ω, 4) 102.3 Ω, 5) 0.2 Ω, 6) OL,
    7) 2.64 kΩ. See "Bench results — 2026-05-03 (D.5 PASSED)"
    subsection above for per-probe verdicts and the pin-naming
    reconciliation note.
[-] D.6 desolder 5160 + OOC re-probe — NOT REQUIRED (D.5
    unambiguous; 5160 B-E reading already explained as series-cap
    charging signature in §7D.4).
[x] Update §7D D.3 verdict in smp_hw_diag.md
    (SUPERSEDED 2026-04-30 by recovered schematic; chips
    bench-confirmed alive 2026-05-03 by D.5 cross-check. Silicon-
    pull rebuild formally on hold; reopen only if Step 8a or
    Target 4 RF validation falsifies the chips-alive verdict.)
[ ] Decide: proceed with rebuild step 2, or pivot to elsewhere-hunt
    — D.5 PASS lands on "pivot": rebuild step 2 stays on hold,
    next bench action is Step 8a or Target 4 (RF validation of
    the LO-amp half of the chain).
[ ] Probes 1–5 — folded into Step 8a (bench, board out). Run during
    8a's procedure step 7 (DC across 3R92) and 8a's SA capture
    (X21 / BFG97 collector / 420 collector / commoned base nodes).
    Post-rebuild in-instrument variant is the fallback only if any
    8a probe reads ambiguous.
[x] Probe 6 — A08 (MAR-8) DC + RF-trace — done 2026-04-29
[x] Update §7F / §7G / Step 9 / Step 10 / connector-interface
    in smp_hw_diag.md — done 2026-04-29, gain figures corrected
    to MAR-8 (+32 dB) 2026-05-05
[x] Update A21-connector-interface paragraph (smp_hw_diag.md
    top, X70/X75 rows + symptom paragraph): X70 → X75 path is
    L72 + A08, not passive — done 2026-04-29
[x] Correct §7G A08 bullet bias-R topology: 2 × 392 Ω in
    parallel (R_eff 196 Ω, ~133 mW per R), trace bench-confirmed
    end-to-end W216.1 → 2 × 392 || → A08 pin 4 — done 2026-04-29
[x] Add bench-session sequencing callouts to Step 8a / 8b / 10a
    (smp_hw_diag.md): runnable before §7E rebuild; 8a is the
    most direct §7D D.5 RF validator — done 2026-04-29
[ ] **Bench session — 4-test decomposition** (added 2026-04-29).
    Two-hour bench session, fully reversible, no soldering;
    closes every signal path on the A21 with a single localized
    pass/fail per stage. Order:
    [x] (1) D.5 cross-check — DMM only, ~5 min, instrument off.
        PASSED 2026-05-03; per "Bench results" subsection above.
    [x] (2) Step 10a — IF chain on A211 — PASSED 2026-05-05.
        Board out, +15 V bench PSU on W216.1; +15 V steady-state
        I = 105 mA (vs. pre-revision "≈ 37 mA A08-only"
        expectation — superseded). VNA −30 dBm at port 1, 10 dB
        attenuator on port 2 thru-cal de-embedded; |S21| passband
        10–80 MHz flat at +31.41 / +31.531 / +31.553 dB
        (M1 / M3 / M2), L72 notch at M4 = −39.482 dB @ 103.04 MHz,
        far stopband M5 = −56.481 dB @ 240 MHz. Maps to outcome
        row "Passband ≥ +28 dB, L72 notch in place" → A08
        + L72 + DC-block caps + 2×392 Ω + +15 V trace + GND bond
        all healthy. **X70 → X75 on-A211 IF path EXONERATED.**
        See smp_hw_diag.md §Step 10a "Run results — this unit"
        for trace shape and marker table.
    [ ] (3) Step 8a — LO chain on A211 — ~30 min, board out,
        ±15 V + +7.5 V on bench, X50 driven from bench source,
        SA + ≥30 dB / ≥1 W pad on X21. smp_hw_diag.md §Step 8a
        (added 2026-04-29). D.5 PASS 2026-05-03 lands on the
        "alive" branch — gating cleared, run when convenient.
        Pass also settles §7D D.3 / §7F doubler-location /
        §7G push-pull-vs-detector by exclusion.
    [ ] (4) Step 8b — milled casing standalone — ~30 min,
        casing on bench, A211 disconnected, biases on X72 / X95
        / X96 from bench PSUs, +28 dBm LO at casing-side X21,
        0 dBm RF at X211, IF read at X70. smp_hw_diag.md
        §Step 8b (added 2026-04-29). Independent of all above;
        can run any time once casing is unmated.
    [ ] (5) sys — `--a21-probe` after reassembly. The single
        verdict cell in the 4-test outcome matrix that decides
        between "done", "Step 11 territory", "casing", or
        "rebuild incomplete".
[ ] Re-read band-3 p.145 §7.1.5 / §7.1.6 + p.146 §7.4.2 to
    nail down the §7.4.2 +27 dB gain attribution (A212 alone
    vs. A212 + A08 combined chain) — closes the remaining
    A08-related doc gap; non-blocking for the rebuild path
[x] Doc-correction sweep A08 = MAR-8 — done 2026-05-05;
    history in [smp_history.md H-2026-05-05](smp_history.md#h-2026-05-05-a08-msa0885-superseded).
[ ] Schematic re-read open items 2026-04-30 — see
    "Comparator inputs + X21 last stage" planning block below.
    [ ] Find the still-fitted N80 input-divider stub destination
    [ ] Trace the X21 last stage past L45/C49 (off-image strip)
    [ ] Resolve the VARSAMP divider mismatch (R30 = 8K25 read?)
[ ] X95 / X96 / V95 / R98 bias-network re-trace 2026-04-30 — see
    "Target 3 — X95 / X96 bias-network topology re-trace" planning
    block below. Triggered by bench findings 2026-04-30 that
    contradict the §7C Table B / §7B layout-list wording.
    [ ] Locate R98 (sub-Ω SMD) on the +V_unreg → BUZ71-D path
    [ ] Identify the two "4F" SOT-23s on the X95 fan-out
    [ ] Decide α (4F = V85/V89 cascade-amp pair) vs β (4F = bias
        generator pair upstream of cascade amp)
    [ ] Search for V95 ("A0" SOT-23) upstream of the X95 brass pin
    [ ] Coordinated §7C / §7B edit pass once trace is complete
[ ] R65 in-instrument LO-chain probe 2026-05-03 — see
    "Target 4 — R65 in-instrument LO-chain probe" planning block
    below. In-circuit X50 → X21 stage-by-stage validator using
    R65 (0R jumper at the doubler/LO-amp boundary) as a clean
    lift-and-restore patch point. Competes with Step 8a as the
    next major LO-chain validator; pick whichever fits the next
    bench session.
    [ ] Stages 0–2: pre-flight + R49 + V60 collector probes
    [ ] Stage 3: lift R65, hard-coax tap on doubler-side pad
    [ ] Stage 3b (optional): re-flow R65 to V2 side, bench-inject
        +0 dBm @ 220 MHz, capture X21
    [ ] Stages 4–5: R67 V2-side + BFG97 collector + V3/V4 collector
    [ ] Re-flow R65 across both pads when done
    [ ] Coordinated `smp_hw_diag.md` Step 4 / §7D D.3 / §7E edit
        pass once Stage-N verdict lands
[ ] Target 5 — §7F doubler topology + AT-42085 pinout rewrite
    (drafted 2026-05-03 from V50-vs-V60 visual inspection +
    schematic re-read; holding pending bench DMM confirmation
    of V50 pin 3 → GND sub-Ω). See "Target 5 — §7F frequency-
    doubler topology + AT-42085 pinout rewrite" planning block
    below.
    [ ] DMM confirm V50 pin 3 → GND sub-Ω (closes visual ID)
    [ ] DMM confirm V60 pin 3 → GND finite (RFC + back-side rail)
    [ ] Decide repair direction (deblob V50 vs accept disable)
    [ ] Coordinated smp_hw_diag.md §7F edit pass once gate clears
```

## Comparator inputs + X21 last stage — next bench-trace targets

Two areas of the recovered Var.02 schematic still need bench
follow-up (added 2026-04-30, deferrable until the next time the
A211 is out of the casing for any reason — none of these gate the
4-test bench session above).

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

These two bench-trace targets are **deferrable** — they do not
gate the 4-test bench session and they do not block any rebuild
decision. Best run **opportunistically** the next time the A211
is out of the casing (e.g. immediately after Step 8a with the
board on the bench). Both targets together should take ~20 min
of DMM work plus whatever time the schematic re-scan needs.

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

Sequencing: Target 3 is **deferrable** like Targets 1 & 2 — the
§7C bias chain reads in spec, X95 / X96 are within tolerance, and
no fault depends on this. Best run in the same out-of-casing
opportunity window as Targets 1 & 2, after Step 8a. Estimated
~30 min for probes 1–6 + ~5 min for probes 7 + 8. The coordinated
doc edit pass (table at the bottom) is intentionally batched to
avoid thrashing `smp_hw_diag.md` with partial-information edits as
findings come in piecewise.


### Target 4 — R65 in-instrument LO-chain probe (tracker only)

Added 2026-05-03; **full procedure, decision matrices, and risks
live in [`smp_hw_diag.md` Step 4-X50](smp_hw_diag.md#step-4-x50--in-instrument-x50--x21-lo-chain-probe-sa--low-cap-probe-planned-2026-05-03)**.
This entry is the cross-doc tracker only — see Status block
above for the run checklist.

In-instrument, in-circuit alternative to Step 8a that localises the
X50 → X21 LO-chain failure stage by stage, without pulling A211
from the casing or wiring bench PSUs to W216. R65 is the 0 Ω
jumper at the FREQUENCY DOUBLER ↔ LO AMPLIFIER boundary on sheet
02/02; lifting one end gives a clean, reversible hard break — R67
121 Ω is the series match into V2 BFG97 base, R66 750 Ω is the
shunt that completes the V2 input divider.

Sequencing vs the existing planning entries here:

- **Target 4 vs Step 8a:** mutually exclusive next-bench-session
  candidates for the same LO-chain question. Pick Target 4 to keep
  A211 in-instrument; pick Step 8a for the most thorough silicon-
  question closure with the board out. A pass at Step 4-X50
  Stage 5 closes §7D D.3 / §7F doubler-location / §7G push-pull-
  vs-detector by exclusion the same way Step 8a does.
- **Target 4 vs Targets 1, 2, 3:** Target 4 leaves A211 mounted,
  so it does *not* fold the out-of-casing DMM trace items
  (Targets 1/2/3) into the same session. If Target 4 runs first
  and resolves the LO-chain question, A211 may never come out of
  the casing — re-evaluate whether the Targets 1/2/3 doc-cleanup
  work is still worth the unmate.


### Target 5 — §7F frequency-doubler topology + AT-42085 pinout rewrite

Added 2026-05-03 from user-led visual inspection of V50 vs V60 +
re-read of `rs_smp_corpus/volumes/band-3/figures/A211_var02_schematic_sheet_02_02.jpg`
zone A (FREQUENCY DOUBLER block). Bench-confirmed 2026-05-03:
DMM probes 1 + 2' PASS, probe 2 invalidated and replaced (see
decision-gate block below). **Bench gate electrically / visually
CLEARED.** Per user instruction 2026-05-03 ("hold"), all §7F
doc edits in `smp_hw_diag.md` remain on hold pending either the
deblob + re-test outcome OR the Target 4 (R65) baseline +
post-deblob delta — whichever the user runs first (sequencing
note below).

#### Findings to land in §7F

```
+---+----------------------------------------------------------------+
| # | Finding                                                        |
+---+----------------------------------------------------------------+
| 1 | AT-42085-B pinout (85-mil plastic / SOT-86 4-lead) is          |
|   |   pin 1 = Base                                                 |
|   |   pin 2 = Emitter                                              |
|   |   pin 3 = Collector                                            |
|   |   pin 4 = Emitter                                              |
|   | (B-E-C-E ordering, both emitter pins on the package, both      |
|   | on the GND pour). Per schematic, both V50 and V60 base pins    |
|   | are fed from the −15 V rail through their respective input     |
|   | divider networks — consistent with NPN run on a −15 V supply   |
|   | (emitter pour to −15 V, collector pulled to GND through the    |
|   | on-board RFC).                                                 |
+---+----------------------------------------------------------------+
| 2 | V50 / V60 / V61 / V62 are a **single push-push frequency-      |
|   | doubler stage**, not a two-stage cascade NPN amplifier. Two    |
|   | AT-42085-B NPN drive transistors in **parallel** off the X50 / |
|   | FSTEP input via separate base-bias networks, each collector    |
|   | driving an HSMS-2800-B Schottky diode (V61 above V50, V62      |
|   | above V60); diode tied terminals form the combiner node;       |
|   | combiner → BPF (C53 / R65 / L65 / L66 / C68 / C66 / L70 —      |
|   | values to be transcribed off the schematic at rewrite time,    |
|   | tuned to 2 × f_FSTEP) → V2 BFG97 base.                         |
+---+----------------------------------------------------------------+
| 3 | V60 input network: V60 base is fed from the **same** X50 /     |
|   | FSTEP drive as V50, NOT cascade-coupled from V50 collector.    |
|   | Path: X50 input → C50 → R50 → R60 (series-R network) → V60     |
|   | base. The "RIGHT chip pin 1 RF-grounded, bias-control input"   |
|   | reading in the existing §7F architecture paragraph is wrong.   |
+---+----------------------------------------------------------------+
| 4 | V50 pin 3 (collector) has a **solder-blob parallel-short to   |
|   | GND across L50** on this unit (visually identified 2026-05-03, |
|   | see `A211_patch.jpg` — blob beside L50, L50 physically present |
|   | and intact, V50-vs-V60 asymmetric: V60 pin 3 has L60 only, no  |
|   | equivalent blob). Electrical consequence:                      |
|   |   DC — benign. V50 collector is DC-grounded through L50 RFC    |
|   |        by design (sub-Ω DCR); the blob adds a parallel sub-Ω  |
|   |        path that is electrically silent at DC. Both V50 and    |
|   |        V60 pin 3 read sub-Ω to GND in DMM ohms mode in normal  |
|   |        operation (bench-confirmed 2026-05-03). No supply-      |
|   |        current pathology, no rail trip — invisible to all      |
|   |        DC checks.                                              |
|   |   RF — fatal. L50 1 µH normally presents ≈ j0.65 to j0.74 kΩ  |
|   |        to the collector across the FSTEP fundamental band      |
|   |        (103-117 MHz), and ≈ j1.29 to j1.47 kΩ at the X21       |
|   |        doubled output (206-234 MHz). The blob bypasses this    |
|   |        with ≈ 0 Ω at all frequencies, RF-grounding the         |
|   |        collector and killing the V50 doubler-leg drive into    |
|   |        V61.                                                    |
|   | V50 contribution to V61 → 0; combiner sees only V62's half-    |
|   | wave-rectified output; doubler 2 × f_FSTEP component drops by  |
|   | exactly 6 dB from the balanced case (Fourier coefficients:     |
|   | half-wave 2/(3π) vs full-wave 4/(3π) of V_peak). Spectrum      |
|   | stays clean at the BFG97 base — the doubler-output BPF         |
|   | rejects the leaked fundamental that no longer cancels by       |
|   | symmetry.                                                      |
+---+----------------------------------------------------------------+
| 5 | L50 / L60 ID: **1 µH ±10% chip RFCs**, body marking            |
|   | "S+T 102K" (Sagami / Sumida-class encoding: 10 × 10² nH =      |
|   | 1000 nH = 1 µH; K = ±10% tolerance). Schematic L50 = L60 =     |
|   | 1 µH confirmed by marking decode 2026-05-03. Topology: shunt   |
|   | RFC from collector pin 3 to GND on each leg, providing DC      |
|   | return + RF isolation (≈ j0.65-0.74 kΩ across the 103-117 MHz  |
|   | FSTEP band, j1.29-1.47 kΩ at the X21 206-234 MHz output).      |
|   | Cap interpretation falsified by sanity check — a 1 nF cap      |
|   | shunt to GND would RF-ground both collectors by design,        |
|   | killing the doubler before any blob is even on the board.      |
+---+----------------------------------------------------------------+
```

#### Decision gate — bench results 2026-05-03

```
+----+----------------------------------------------------------+--------------+
| #  | Bench probe (instrument off, casing on)                  | Result       |
+----+----------------------------------------------------------+--------------+
| 1  | DMM ohm V50 pin 3 → chassis GND. Expected sub-Ω.         | PASS         |
+----+----------------------------------------------------------+--------------+
| 2  | DMM ohm V60 pin 3 → chassis GND. Originally expected     | INVALIDATED  |
|    |   finite (RFC DCR through L60 to back-side rail).        |              |
|    |   Actual: also sub-Ω. Re-interpretation: L60 is a 1 µH   |              |
|    |   chip RFC with sub-Ω DCR (finding 5 above), so both     |              |
|    |   pin 3's read sub-Ω in normal operation. Probe 2        |              |
|    |   cannot discriminate "blob short" from "healthy RFC";   |              |
|    |   replaced by visual gate 2' below.                      |              |
+----+----------------------------------------------------------+--------------+
| 2' | Visual asymmetry (replaces probe 2): V50 has anomalous   | PASS         |
|    |   solder blob beside L50 going from pin 3 to GND pour;   |              |
|    |   V60 has L60 only, no blob. L50 and L60 both physically |              |
|    |   present, intact, identical body and marking            |              |
|    |   (`A211_patch.jpg`).                                    |              |
+----+----------------------------------------------------------+--------------+
| 3  | DMM diode test V50 + V60 in-circuit (12 probe combos,    | PASS         |
|    |   B-E fwd, B-E fwd, B-C fwd, all 3 reverse, both C-E     |              |
|    |   directions on both emitter pins, E-E tie). Bench       |              |
|    |   2026-05-03: V50 readings match V60 within DMM          |              |
|    |   resolution on every probe combo. Forwards 0.78 V       |              |
|    |   (junction + series-R from in-circuit bias network),    |              |
|    |   reverses 1.68-1.92 V (effectively OL = DMM diode-mode  |              |
|    |   OCV ceiling), C-E (red C) 1.5 V (also OL through       |              |
|    |   external path), E-C (red E) 0.72 V (B-C junction       |              |
|    |   forward-biased via the −15 V rail → bias chain → base  |              |
|    |   → BC → collector path; bonus: confirms bias chain      |              |
|    |   intact at low Ω on both devices), E-E tie 0 Ω.         |              |
|    |   V50 silicon fully intact, matched to V60 reference;    |              |
|    |   blob has not back-stressed the device — deblob alone   |              |
|    |   predicted to restore V50 leg fully.                    |              |
+----+----------------------------------------------------------+--------------+
```

Gate status (2026-05-03): probes 1 + 2' + 3 PASS; probe 2
invalidated and superseded. **Bench gate fully CLEARED — V50
silicon confirmed intact, deblob alone predicted to restore the
V50 leg.** Doc edits to `smp_hw_diag.md` remain HELD per user
instruction 2026-05-03 ("hold") pending either (i) the deblob +
re-test outcome below, or (ii) Target 4 R65 baseline + post-
deblob delta (see sequencing note below). With probe 3 PASS, the
"deblob alone insufficient ⇒ V50 silicon damaged" branch in the
supplementary step is closed off as a low-probability outcome.

**Optional supplementary step before rewriting** — deblob V50
pin 3 and re-test X75 with `--a21-probe`:

- X75 returns ⇒ V50 blob was the entire root cause; rewrite
  §7F with the doubler topology + the blob-as-disable history;
  blob status = "removed 2026-05-XX, X75 restored".
- X75 stays dead but BFG97 base SA level rises by ~6 dB ⇒
  blob was a contributor only; second fault somewhere down-
  stream of BFG97; rewrite §7F as above and open a new
  follow-up on the residual fault.
- X75 stays dead and BFG97 base SA level doesn't rise ⇒ V50
  silicon also damaged; deblob alone insufficient; rewrite
  §7F as above and add a V50 silicon-replacement sub-task.

#### Sequencing — Target 4 (R65 probe) before deblob

Considered 2026-05-03 (user, "thinking probing R65 first"): run
**Target 4** (R65 in-instrument LO-chain probe; full procedure
in `smp_hw_diag.md` Step 4-X50) **before** deblobbing V50 pin 3.
Rationale:

- Target 4 captures a calibrated baseline of the LO drive at the
  FREQUENCY DOUBLER ↔ LO AMPLIFIER boundary with the blob in
  place — specifically the V2 BFG97-base SA level and spectral
  shape at 2 × f_FSTEP — before any irreversible rework.
- Deblob + re-run of the same Target 4 capture then yields a
  directly measurable delta. Finding 4 above predicts a clean
  **+6 dB rise** on the 2 × f_FSTEP component (half-wave →
  full-wave Fourier coefficient ratio), with the spectrum
  otherwise unchanged. That delta is the single cleanest test
  of the doubler-half-disabled hypothesis.
- Outcome map (Target 4 with blob → deblob → Target 4 again):
    pre-deblob spectrum already clean and ~6 dB low vs nominal
      ⇒ finding 4 corroborated even before the rework; deblob
      with high confidence.
    pre-deblob spectrum dead at BFG97 base ⇒ V50 leg is not the
      only contributor (residual fault upstream of doubler, or
      V62 leg also dead). Deblob still useful but expect partial
      restoration only; widen the search.
    post-deblob delta = +6 dB ± 1 dB ⇒ finding 4 vindicated; if
      X75 still dead, residual fault is downstream of BFG97 base
      (V2 amp, BPF, or X21 / X75 path).
    post-deblob delta significantly < +6 dB ⇒ V50 silicon also
      damaged (probe 3 above) or L50 itself altered by the
      blob-removal; re-evaluate before further rework.
- Alternative: run probe 3 (DMM diode test on V50 in-circuit)
  alongside the pre-deblob Target 4 capture. Both are non-
  invasive, ~5 min each, and together strongly constrain the
  deblob outcome before committing to the rework.

If Target 4 is run before deblob, the supplementary step above
becomes "Target 4 (post-deblob) re-capture" rather than a
standalone X75 retest, and the three-outcome branch maps onto
the delta-measurement outcomes here.


#### Specific edits proposed for `smp_hw_diag.md` §7F

```
+---+-----------------------------------------------------------+
| # | Edit (held per user "hold" instr.; bench gate cleared)    |
+---+-----------------------------------------------------------+
| 1 | Lines 1580-1595 (Bench-traced observations bullets):      |
|   |   replace the "pin 4 is solder-blob-grounded" reading     |
|   |   with the corrected "pin 3 (collector) is solder-blob-   |
|   |   grounded on V50 only; V60 pin 3 unblobbed". Drop the    |
|   |   pin-4-as-emitter framing and the "originally ruled out  |
|   |   the Darlington class" anchor — the schematic confirms   |
|   |   the AT-42085-B ID directly, no longer relies on the     |
|   |   blob observation. Drop the "provisional GaAs-FET        |
|   |   pinout (now superseded)" bullet — fully closed by the   |
|   |   resolved B-E-C-E pinout in finding 1 above.             |
+---+-----------------------------------------------------------+
| 2 | Lines 1597-1605 (Architecture paragraph): replace the     |
|   |   "two-stage cascade NPN bipolar amplifier" framing with  |
|   |   "push-push frequency doubler — two parallel AT-42085-B  |
|   |   NPN drive transistors (V50, V60), each driving an       |
|   |   HSMS-2800-B Schottky (V61, V62), Schottky outputs       |
|   |   combined at the BPF input feeding V2 BFG97 base". Drop  |
|   |   the "RIGHT chip pin 1 RF-grounded, bias-control input"  |
|   |   reading — V60 pin 1 is active RF input from the same    |
|   |   X50 drive, fed via C50 / R50 / R60. Drop the "inter-    |
|   |   stage section is not yet bench-traced" framing — there  |
|   |   is no inter-stage section in a parallel-doubler         |
|   |   topology.                                               |
+---+-----------------------------------------------------------+
| 3 | Lines 1607-1623 (Bench-traced DC divider paragraph +      |
|   |   V_B = −10.6 V calculation): the divider net being       |
|   |   modelled is one of the two parallel base-bias networks  |
|   |   (V50-side or V60-side) feeding −15 V to a single base   |
|   |   pin, not a cascade-amp gate-bias node feeding two       |
|   |   chips. Re-derive the expected V_B against the schematic |
|   |   R49 / C57 / R59 (V50-side) or C50 / R50 / R60 (V60-     |
|   |   side) values once the schematic R-values are            |
|   |   transcribed. The "−10.6 V is not a valid NPN base-bias  |
|   |   point" caveat resolves to "the divider feeds a high-Z   |
|   |   base; static V_B equals the divider mid-point, and DC   |
|   |   bias is set by the larger −15 V → R → base network on   |
|   |   the schematic-confirmed side, not by the X50-side       |
|   |   divider".                                               |
+---+-----------------------------------------------------------+
| 4 | Lines 1625-1835 (ALC-actuator hypothesis withdrawn,       |
|   |   back-side rail discovery, regulator block, P-sequence,  |
|   |   distributed-rail sketch): much of this is constructed   |
|   |   on the cascade-amp + actuator framing. Re-read against  |
|   |   the parallel-doubler topology: the back-side             |
|   |   distributed rail at 61R9 / pins 2-3 is now the          |
|   |   **emitter pour rail at −15 V** (pin 2 and pin 4 both    |
|   |   E on the corrected pinout, both on the same pour). The  |
|   |   "pin 2/3 cluster on a regulated rail in the −1 to −3 V  |
|   |   window" reading is wrong — pin 2 is E (on −15 V via     |
|   |   3R92-class R), pin 3 is C (on the doubler-side trace to |
|   |   V61 / V62, GND-blobbed on V50 only). Strike the         |
|   |   regulator-block / V_rail framing; the P-sequence rows   |
|   |   that depended on it (P2, P3, P6, P7, P8) need rewriting |
|   |   against the corrected emitter-rail / collector-trace    |
|   |   reading. The ALC-actuator hypothesis stays withdrawn    |
|   |   (already done under §7D γ); no further action there.    |
+---+-----------------------------------------------------------+
| 5 | Lines 1777-1796 (Pinout interpretation flagged            |
|   |   unresolved (H)): replace with the resolved pinout       |
|   |   table (B-E-C-E per finding 1 above). Strike the dual-   |
|   |   gate / cascode / VVA candidate list — all falsified by  |
|   |   the AT-42085-B schematic ID + bench-confirmed pinout.   |
|   |   The "pin 4 LEFT = GND (solder-blob short)" survival     |
|   |   bullet is also wrong — the GND-blobbed pin is pin 3,    |
|   |   not pin 4.                                              |
+---+-----------------------------------------------------------+
| 6 | Lines 1910-1944 (AT-42085 → AG303-86G substitution        |
|   |   sketch table): correct the pin-mapping column. Pin 2 =  |
|   |   E (already roughly right); pin 3 = **C** (not "(one of  |
|   |   two)"); pin 4 = **E** (not "Collector through RFC to    |
|   |   +VR15-P"). Re-derive the rework-needed column against   |
|   |   the corrected pinout: the R_bias / DC-block / RFC-keep  |
|   |   advice shifts from pin 4 to pin 3, and the AG303 bias   |
|   |   sense (single-supply, current-driven via output-pin     |
|   |   bias-R) needs re-checking against the negative-supply   |
|   |   AT-42085 topology on this board (the AG303-86G is       |
|   |   spec'd from a positive supply; substitution onto a      |
|   |   negative-supply pad pattern requires either flipping    |
|   |   the rail or fitting a level-shift, neither documented   |
|   |   in the current sketch).                                 |
+---+-----------------------------------------------------------+
| 7 | New §7F sub-section: "V50 collector GND-blob — disabled   |
|   |   doubler half (visual ID 2026-05-03, electrical confirm  |
|   |   YYYY-MM-DD)". Describes the visual identification, V50- |
|   |   vs-V60 asymmetry, electrical consequence (−6 dB on      |
|   |   doubler 2 × f_FSTEP component, fundamental rejected by  |
|   |   the BPF, X75 dead by amplitude collapse OR amplitude +  |
|   |   secondary downstream fault per the supplementary step   |
|   |   outcome), and the repair-direction taken. Cross-        |
|   |   reference Target 5 in `smp_next.md` for the bench-      |
|   |   confirmation history.                                   |
+---+-----------------------------------------------------------+
| 8 | History pointer: move the superseded "two-stage cascade   |
|   |   NPN amplifier" architecture paragraph + the GaAs-FET    |
|   |   pinout fragments + the regulator-block P-sequence to    |
|   |   `smp_history.md` under a new anchor                      |
|   |   `H-2026-05-XX-7f-cascade-vs-doubler-topology-           |
|   |   superseded`. Same pattern as the                         |
|   |   `H-2026-04-30-7f-gaas-fet-id-superseded` anchor used    |
|   |   for the previous round of §7F supersession.             |
+---+-----------------------------------------------------------+
```

#### Cross-doc impact (other sections touched by the rewrite)

```
+---+-----------------------------------------------------------+
| # | Cross-doc edit                                            |
+---+-----------------------------------------------------------+
| a | §7B layout list V50 / V60 entries: update pinout from     |
|   |   any cascade-amp framing to push-push doubler-drive +    |
|   |   B-E-C-E pinout. Cross-reference V61 / V62 as the        |
|   |   Schottky combiner pair (not separate stages).           |
| b | §7D D.0 / D.5 references to "420 cascade" → "doubler      |
|   |   drive pair". The D.5 cross-check itself is on V3 / V4   |
|   |   (MRF3866 / MRF5160), unaffected by the §7F rewrite.     |
| c | §7E rebuild bill-of-materials AT-42085 → AG303-86G        |
|   |   substitution (cross-referenced from §7F line 1881):     |
|   |   re-evaluate substitution feasibility under the          |
|   |   corrected negative-supply topology + B-E-C-E pinout     |
|   |   (see edit 6 above).                                     |
| d | Step 8a / Step 4-X50 / Target 4 procedure docs: any       |
|   |   "V60 collector SA capture" probe points are correct as  |
|   |   written (V60 collector = V60 pin 3 on the un-blobbed    |
|   |   leg, RF-active); "V50 collector SA capture" probes      |
|   |   need a caveat that V50 pin 3 is GND-shorted on this     |
|   |   unit and will read 0 RF regardless of upstream drive.   |
+---+-----------------------------------------------------------+
```

