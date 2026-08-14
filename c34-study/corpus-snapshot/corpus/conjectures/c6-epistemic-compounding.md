---
id: c6
name: epistemic-compounding
status: operationalized
lineage:
  - epistemic-main/canon/foundational-documents/the-law-of-epistemic-acceleration.md
  - epistemic-main/science/cognitive-systems-evolution/core-concepts/intelligence-compounding-loop.md
  - observatory/packets/2026-06-14.md
verdict: null
tracking:                      # machine-updated by observatory beats only
  last_beat: 2026-07-13
  gate: "shares C2 rev.2's gate — CHECKED 2026-07-13: time arm MET (8.1/8 weeks) but the strata bar FAILED 1/10 under all readings (analyses/c2-friction-to-production/gate_check.py; see c2 tracking). No C6 analysis permitted; waits."
  watch: [packets/2026-07-13.md]
---

# C6 - Epistemic compounding

## Claim

Epistemic production is partly state-proportional: a workspace or recipe family with
more accumulated verified production should, under comparable workload, generate more
subsequent verified production than an otherwise similar low-stock stratum.

This is the modest salvage of the old acceleration-law shape. It does not assert a
universal scalar `E(t)`, a multiplicative constant, or an escape-velocity threshold.
It asks whether the live Mentu system shows any measurable compounding: does prior
productive stock predict later productive output after volume and friction are
accounted for?

## Origin

The 2025 corpus asserted multiplicative epistemic acceleration:
`E(t+1) = E(t) * (1 + r * S * M * I)`. The 2026-06-14 weekly synthesis rejected the
formula as a law: its factors were not independently measured on a common scale, and
`E(t)` had no stable operational definition.

The retained shape is narrower and testable. If knowledge work compounds, prior
verified production should predict future verified production more than an additive
constant-rate model predicts. If it does not, the acceleration metaphor stays parked.

## Operationalization

**Datasets**:

- `~/.mentu/training/cir-run-outcomes.jsonl`, post-2026-06-10 regime only:
  `run_id`, `recipe`, `started_at`, `completed_at`, `success`, `steps_ok`,
  `steps_total`, `duration_ms`, `total_cost`, `source_intent`.
- `~/.mentu/cir.db` read-only: `signals` lifecycle rows for workspace attribution,
  verified evidence signals, and commitment close events; `relations` only for
  sensitivity checks, not the primary stock count.
- C2 rev. 2 friction surfaces: weekly run error rates, duration medians, and mature
  open-commitment age. C6 shares C2's friction definitions rather than inventing a
  second friction proxy.

**Units**:

- Primary stratum: `(recipe_family, week)` from post-regime run outcomes.
- Secondary stratum: `(workspace, week)` where workspace identity resolves from
  `cir.db.signals.run_id` or commitment lifecycle rows.

**Measures**:

- **Stock at week t**: cumulative verified production before the week. Primary stock
  is prior successful runs in the same recipe family, weighted by `steps_ok /
  steps_total` where available. Secondary stock uses prior close events and
  machine-verified evidence/verdict signals in the same workspace.
- **Production at week t+1**: successful runs, close events, and verified evidence
  signals in the next week, reported separately and in a predeclared composite only
  if all components agree in sign.
- **Workload controls**: run count, started commitments, median duration, total cost,
  and recipe family/workspace fixed effects.
- **Friction interaction**: C2 friction at week t. Compounding should weaken when
  stall fraction, error rate, or latency are high.

**Test**:

Compare a state-proportional model against an additive model on mature strata:

- state-proportional: `production_t+1 ~ log1p(stock_t) + workload + friction`
- additive baseline: `production_t+1 ~ workload + friction + stratum age`

The analysis should report effect direction, rank correlation, and whether the
state-proportional term improves out-of-sample weekly prediction over the additive
baseline. The exact estimator can be simple and deterministic; the contrast matters
more than the model family.

## Predictions (stated 2026-06-19, before C6 analysis)

- **P1**: `log1p(stock_t)` is positively associated with next-week verified
  production after controlling for workload and stratum age.
- **P2**: The association is stronger in low-friction weeks and weakens or reverses
  in high-friction weeks.
- **P3**: A state-proportional model predicts next-week production better than an
  additive constant-rate baseline in a majority of mature strata.

## Falsification criteria

- Prior stock has no positive association with next-week production after workload
  and age controls -> **refuted** as a live Mentu effect.
- A positive association exists but is fully explained by run volume, scheduling, or
  workspace age -> **revised** as production momentum rather than epistemic
  compounding.
- The effect appears only on one surface while the other production surfaces disagree
  in sign -> **inconclusive**, no verdict.

## Gate

Do not analyze before the C2 rev. 2 gate opens: at least **8 weeks** of post-regime
run outcomes and at least **10 strata** with **5 mature weeks** each. C6 deliberately
rides the same accrual clock as C2 because the central confound is friction.

If the gate fails on strata count, the conjecture waits. Do not lower the bar after
seeing partial data.

## Known limitations

- "Stock" is still a proxy. This conjecture does not claim to measure total
  knowledge, only prior verified production recorded by the instrument.
- Recipe scheduling can mimic compounding: a family that gets more attention can
  produce more simply because it is scheduled more often. Workload controls and
  fixed effects are mandatory.
- Workspace identity is noisy (`unknown`, `default`, path aliases). The secondary
  workspace surface must reuse the C5 identity guardrails where applicable.
- This conjecture is downstream of C2. If friction surfaces are not ready, C6 is not
  ready either.
