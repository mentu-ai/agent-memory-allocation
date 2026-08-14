# Result — C3 epistemic entropy (first test)

**Date**: 2026-06-10 (analysis run 18:49Z)
**Conjecture**: `corpus/conjectures/c3-epistemic-entropy.md`
**Analysis**: `analyses/c3-epistemic-entropy/analyze.py` (read-only on `cir.db`;
deterministic per database state; signal ages computed against run time)
**Pre-registration**: predictions P1–P3 frozen in the conjecture file at commit
`c81f500`, before any trust or contradiction data was examined.

## Verdict: REVISED — decay component SUPPORTED; contradiction component returns to operationalized

## Dataset digest

232,181 signals (152,958 with decay half-lives configured); 217,629 trust-state
rows. `trust_events`: 95,985 `initial_computation`, 175 `context_unproven`,
64 `context_ignored`, **2 `context_used`** (ever). `contradictions`: **11 rows
total**, 2 resolved.

## P1 — decay: SUPPORTED (cross-sectionally, as faithfully-applied policy)

Effective confidence erodes with age for unmaintained signals, exactly as a
half-life model predicts, and **nothing ever drifts upward**:

| age (unaccessed signals) | n | mean Δ (effective − asserted) | decayed | boosted |
|---|---|---|---|---|
| 0–7d | 20,336 | −0.009 | 1.6% | 0 |
| 7–30d | 65,380 | −0.010 | 1.9% | 0 |
| 30–60d | 60,675 | −0.026 | 5.0% | 0 |
| >60d | 1,964 | **−0.270** | **55.0%** | 0 |

The pre-registered refutation criterion — "unreinforced signals hold confidence
indefinitely (decay is configured but inert)" — **does not fire**. Decay is
real and applied (via periodic recomputation: ~23,700 trust rows have been
recomputed since write; coverage is partial and strongly age-correlated).

Scope honesty, per the conjecture's own caveat: this validates that *Mentu's
entropy bookkeeping operates and is monotone* — a cross-sectional age gradient
plus zero observed boosts, not a longitudinal trace of individual signals. The
narrow claim graduates to `corpus/supported/c3a-mechanical-decay.md`.

## P1's other half — reinforcement: INSUFFICIENT, and the number is itself a finding

Reinforcement barely exists: **98 of 217,629 signals (0.045%) have ever been
accessed**; 139 carry any reinforcement score; **2 `context_used` events in
system history — both for `digest_ABBD0388-C07`, reinforced on 2026-06-07 by
this corpus's own founding audit agents reading CIR context.** The only
counter-entropic events on record were caused by the investigation itself.

Combined with C1 (0/54 briefs cited) this completes the picture from the other
side: Mentu's memory is **write-only in practice** — 232K signals in, ~0.05%
ever read back. Entropy has no opponent in this system yet.

## P2 / P3 — contradictions: INSUFFICIENT-EVIDENCE (instrument too young)

11 contradictions across 232K signals (47 per million). The two April
detections were both resolved in ~27 hours; the other nine were all detected
**today** (during the day's runs) and are hours old. The contradiction detector
itself shipped days ago (CIR Wave 2). Direction is consistent with P2
(9 detected, 0 resolved in the current period) but one day of a days-old
detector supports no inference. Re-test gated on: ≥60 days of detector
operation or ≥100 detected contradictions, whichever comes first.

## Interpretation for the corpus

The entropy conjecture splits cleanly:

1. **Decay (supported)**: unmaintained knowledge in this system measurably
   loses effective confidence with age, monotonically, with zero spontaneous
   recovery. The second law's first half has empirical footing here.
2. **Counter-entropy (the real finding)**: the system performs almost no
   maintenance work to oppose decay — not because maintenance fails, but
   because *return barely happens* (0.045% access rate). C1b's distilled,
   citeable, randomized injection is therefore also the intervention that makes
   C3's reinforcement half testable: if return starts happening, reinforcement
   events will exist to study.
3. **Contradiction dynamics**: parked until the detector matures.

## Observer-effect caveat (added to the instrument map)

Analyses that read CIR through Mentu tooling write `access_count`/reinforcement
telemetry — the founding audit visibly did. This corpus's own scripts read
`cir.db` via raw read-only SQLite precisely to avoid contaminating the
quantities they measure. Keep it that way.

## Verbatim analysis output

Stored alongside; reproduce with `python3 analyses/c3-epistemic-entropy/analyze.py`.
Key lines: overall 5,685/148,356 decayed (3.83%); recomputation 193,911/217,629
untouched since write; `context_used` events: `digest_ABBD0388-C07` ×2
(0.9 → 0.9, 2026-06-07).
