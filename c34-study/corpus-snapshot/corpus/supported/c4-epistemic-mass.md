---
id: c4
name: epistemic-mass
status: tested
lineage:
  - epistemic-main/canon/law-suites/epistemic-acceleration-newton.md
  - epistemic-main/canon/law-suites/newtonian-laws-of-epistemic-motion.md
verdict: supported
result: results/2026-06-10-c4-epistemic-mass.md
---

# C4 — Epistemic mass

## Claim

Structurally heavier workflows — more steps, deeper dependencies — fail more often
and change more slowly than lighter ones, holding purpose constant.

## Origin

The 2025 corpus's a = F/m: rate of change is inversely proportional to "epistemic
mass." Mass was polysemous there (complexity, structural debt, tool dependence,
cognitive overhead). Here it is defined operationally and narrowly: the measurable
weight of a workflow.

## Operationalization

**Datasets**:
- `~/.mentu/recipes/` (2,420 JSON): steps per recipe, per-step config (models,
  timeouts, phases) as weight measures.
- `~/.mentu/training/cir-run-outcomes.jsonl`: `recipe`, `steps_total`, `steps_ok`,
  `outcome`, `duration_ms` — failure rates by weight.
- `~/.mentu/file-history/`: edit timestamps of recipe files — change latency (time
  between edits, edits per unit of use).

**Measures**:
- Run failure rate as a function of `steps_total`; per-step success rate (is failure
  compounding ~p^n, or do heavy recipes fail disproportionately even per step?).
- Change velocity: for recipes with ≥N runs, time-to-first-modification after a
  failing run, by weight class.

## Predictions (stated 2026-06-10, before analysis)

- **P1**: Run failure rate increases with `steps_total`.
- **P2**: Per-step success is roughly constant across weight classes — i.e., heavy
  recipes fail mostly because failure compounds, not because individual steps are
  worse. (If per-step success *also* degrades with weight, that is a stronger,
  more interesting result.)
- **P3**: Heavier recipes are modified more slowly after failures than lighter ones.

## Falsification criteria

- Failure rate flat or decreasing with weight → **refuted** (would suggest heavy
  recipes are better-engineered, an interesting inversion).
- P3 reversed (heavy recipes get fixed faster) → **revised**: attention follows mass.

## Known limitations

Recipe weight correlates with task ambition; "holding purpose constant" is only
approximated by comparing recipes within the same domain/tag family. Gate design
(boundary checks) may truncate failures in ways that mask per-step rates.

## Result (2026-06-10): SUPPORTED — mechanism revised

P1 supported (success 63% → 0% monotone across weight buckets; per-recipe
ρ = −0.42, robust to excluding the dominant heavy recipe). P2's constant-p
mechanism refuted in the pre-flagged stronger direction: per-step success
itself degrades with weight (0.63 → 0.016). P3 supported in extreme form: 98%
of heavy failing runs never saw a recipe modification — inertia as
abandonment-in-place (the `ane-fortress` zombie pipeline: ~166 failures in 25
days, zero fixes). Full record: `results/2026-06-10-c4-epistemic-mass.md`.
