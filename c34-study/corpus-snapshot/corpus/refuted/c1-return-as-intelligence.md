---
id: c1
name: return-as-intelligence
status: tested
lineage:
  - epistemic-main/canon/foundational-documents/the-law-of-epistemic-acceleration.md
  - epistemic-main/engine/foundations/cir-memory-as-infrastructure.md
  - epistemic-main/canon/foundational-principles/foundational-principles-of-ese.md
verdict: refuted
result: results/2026-06-10-c1-return-as-intelligence.md
---

# C1 — Return-as-intelligence

## Claim

Autonomous runs that receive injected prior validated knowledge (CIR context) succeed
at a higher rate than runs without injection — and injected knowledge that is actually
*used* helps more than knowledge that is merely injected.

## Origin

The 2025 corpus held "return as generation" as a foundational principle: revisiting
knowledge is generative, not mere retrieval, and is the mechanism by which intelligence
compounds. It was asserted, never tested; the principle lived inside a multiplicative
law (E(t+1) = E(t)·(1 + r·S·M·I)) whose parameters had no measurement procedure. This
conjecture extracts the testable core: does returning prior knowledge into new work
measurably improve outcomes?

## Operationalization

**Dataset**: `~/.mentu/training/cir-run-outcomes.jsonl` — one record per sequence run.

- **Injection status**: `cir_verdict` (`not_injected` vs any injected verdict) and
  `injected_count > 0`.
- **Usage**: `use_rate`, `used_count` (injected signals the agent actually cited),
  `context_helped` (run-level flag).
- **Outcome**: `outcome` (`ok`/`fail`), `success`, `steps_ok / steps_total`.
- **Cost**: `total_cost`, `duration_ms`.
- **Stratification**: per `recipe` (injection is not randomized; recipe difficulty is
  the obvious confounder).

Analysis: `analyses/c1-return-as-intelligence/analyze.py`. Significance via Fisher
exact test on the injected × success 2×2 table; per-recipe deltas reported to expose
Simpson's-paradox risk.

## Predictions (stated 2026-06-10, before any results were computed)

- **P1**: Success rate is higher for injected runs than for `not_injected` runs.
- **P2**: Among injected runs, those with `context_helped = true` show a higher mean
  `steps_ok/steps_total` than those with `context_helped = false`.
- **P3**: Injection is not dead weight: the majority of injected runs have
  `use_rate > 0`.
- **P4**: Injection does not impose a large cost penalty: mean `total_cost` of
  injected runs is within ~2× of non-injected runs.

## Falsification criteria

- P1 reversed (injected runs succeed *less*) with a Fisher exact p < 0.05 → **refuted**.
- `use_rate ≈ 0` for the large majority of injected runs (injection is theater) →
  **refuted** in its strong form, regardless of P1.
- P1 holds in aggregate but reverses within most recipe strata (Simpson's) →
  **revised**: the effect belongs to recipe selection, not to return.
- Cells too small for inference → **insufficient-evidence**; conjecture stays
  operationalized and waits for more runs.

## Known limitations

Observational data; injection correlates with system maturity and recipe mix over
time. `use_rate` is a lower bound (`missing_footer_count` records runs where usage
went unreported). A definitive test would randomize injection — noted as future work
if this analysis is promising.

## Result (2026-06-10)

**REFUTED (strong form), as instrumented.** The pre-registered criterion fired:
0/54 injected runs recorded any usage of injected context, despite every brief
being delivered non-empty (median 2,262 bytes). Zero `proven` verdicts, zero
`context_helped` runs. P1 was directionally positive (42.6% vs 30.5% success,
p = 0.086) but confounded — no recipe has runs in both arms. The return loop is
open: knowledge is delivered but never measurably consumed. A successor (C1b)
requires fixing the usage-attribution chain and within-recipe common support.
Full result: `results/2026-06-10-c1-return-as-intelligence.md`.
