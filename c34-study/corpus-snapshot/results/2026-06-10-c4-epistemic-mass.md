# Result — C4 epistemic mass (first test)

**Date**: 2026-06-10
**Conjecture**: `corpus/supported/c4-epistemic-mass.md` (moved from
`corpus/conjectures/` by this result)
**Analysis**: `analyses/c4-epistemic-mass/analyze.py` (read-only; deterministic —
verified identical across two runs; censoring horizon taken from the data, not
the clock)
**Pre-registration**: P1–P3 frozen at `c81f500`.

## Verdict: SUPPORTED — with the mechanism revised in the stronger direction

Heavier workflows fail more and change less. Both halves of the claim held, and
the proposed mechanism (pure compounding) was refuted in favor of something
stronger: weight degrades *per-step* performance, not just total survival.

## Dataset digest

420 runs with step counts (2026-05-17 → 2026-06-10), 79 recipes. Heavy bucket
(7+ steps) is 178 runs, dominated by one recipe (`ane-fortress`, 166) — so all
inference leans on the sensitivity table and per-recipe association, as the
conjecture's "holding purpose constant" caveat required.

## P1 — failure rises with weight: SUPPORTED

| weight | runs | success | per-step p̂ |
|---|---|---|---|
| 1 | 181 | 63.0% | 0.630 |
| 2–3 | 40 | 42.5% | 0.406 |
| 4–6 | 21 | 23.8% | 0.284 |
| 7+ | 178 | **0.0%** | 0.016 |

Monotone in every view: pooled, **excluding the dominant heavy recipe**
(7+ still 0/12, per-step p̂ 0.235), and per-recipe — Spearman
ρ(weight, success rate) = **−0.421** across 39 recipes with ≥3 runs
(−0.392 excluding `ane-fortress`). The falsification criterion (flat or
inverted) does not fire anywhere.

## P2 — per-step success constant: REFUTED (stronger alternative confirmed)

The frozen prediction said per-step success should be roughly constant, with
failure compounding as p^n — and explicitly flagged the alternative: "if
per-step success *also* degrades with weight, that is a stronger, more
interesting result." It does, steeply: 0.630 → 0.406 → 0.284 → 0.016 per step.
Heavy workflows are not light workflows chained together; their individual
steps are worse. Cross-sectional data cannot separate the two candidate
explanations — heavier recipes attempt harder steps (ambition confound), or
long chains degrade their own execution context as they run. Both are
testable later; the constant-p model is dead either way.

## P3 — heavier recipes change more slowly after failure: SUPPORTED, in an extreme form

Using recipe-hash transitions (from 862 recipes' `recipe_version` records, 464
transitions) as the modification clock:

| weight | failing runs | modified after failure | median hours | never modified |
|---|---|---|---|---|
| 1 | 67 | 72% | 0.2 | 28% |
| 2–3 | 23 | 30% | 34.2 | 70% |
| 4–6 | 15 | 73% | 0.9 | 27% |
| 7+ | 178 | **2%** | 0.2 | **98%** |

The pre-registered reversal criterion ("heavy recipes get fixed faster →
revised: attention follows mass") does not fire — the opposite of reversal.
But the honest reading is starker than "slower": heavy failing workflows are
not modified *at all*. The mechanism is inertia-as-abandonment-in-place.

**The zombie pipeline.** `ane-fortress` (8 steps) ran ~166 times over 25 days
— roughly every 3–4 hours — failed every single time, and received
approximately zero modifications. It neither succeeds, nor stops, nor changes.
That is epistemic mass made visible: the heaviest object in the system is the
one nothing acts upon. (Flagged to Mentu engineering: fix it or unschedule it;
either ends the waste. It is also quietly polluting baselines — it alone
accounts for 40% of all runs in the outcome dataset.)

## Scope and limits

- Weight and recipe identity are confounded; the per-recipe ρ and the
  sensitivity exclusion carry the inference, and both hold.
- P3's modification clock has run-cadence resolution, and abandoned recipes are
  censored, not "slow" — for the heavy bucket the distinction collapses, since
  the recipe kept running.
- All data is pre-regime-boundary (the 2026-06-10 instrument change affects
  injection, not step structure).

## Relation to the rest of the corpus

C4 closes a triangle with C2 and C3: heavy things fail per-step (C4), failing
heavy things are not maintained (C4-P3, C2's stall in another guise), and
unmaintained things decay (C3a). The system's entropy story is coherent across
three independent measurements — what's missing everywhere is the
counter-force, which is exactly what C1b is testing.
