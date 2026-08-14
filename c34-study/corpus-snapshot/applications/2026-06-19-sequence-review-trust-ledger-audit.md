# Sequence-review trust ledger audit

Source audited: `/Users/rashid/.mentu/skill-library/.claude/skills/sequence-review/SKILL.md`

## Decision

Admit as **C23 - Review trust calibration**.

The strong idea is not "a reviewer can aggregate trust." It is:

> A citation-gated, fresh-context review of a completed sequence should produce a
> trust forecast that is calibrated against later recipe reliability better than
> mechanical run-success baselines alone.

This is distinct from C16 and C20. C16 tests whether trust-calibrated activation
conditions improve selection. C20 tests human participation at semantic boundaries.
C23 tests whether review commitments become calibrated predictive measurements.

## What the skill gets right

- It separates the executor from the reviewer with fresh context.
- It requires an explicit target run id and forbids "latest run" fallback.
- It requires citations before a review enters the trust ledger.
- It treats review output as a schema-gated artifact rather than narrative.
- It aggregates over runs instead of trusting one review in isolation.

## Current substrate gap

The skill assumes a durable `~/.mentu/sequence-history.jsonl` substrate and a
`review_commit` signal stream. Mentu has adjacent pieces, but the path is not yet a
verdict-grade instrument:

- `SequenceHistoryWriter` in `mentu-engine` is currently a logger stub, not the
  canonical append-only sequence history writer.
- `~/.mentu/training/cir-run-outcomes.jsonl` is a stronger existing run-outcome
  substrate than the skill's history file.
- `TrustAggregator` scores actors from ledger actions, but this is not calibrated to
  future recipe outcomes.
- `review_commit` rows, if present, must be joined to target runs and then to later
  same-recipe outcomes before any trust score becomes scientific evidence.

## Evolved telemetry contract

C23 needs three separated streams:

1. **Target run substrate**: terminal run record with explicit `run_id`, recipe,
   workspace, started/completed timestamps, status, step counts, cost, run class, and
   mechanical trust proxy.
2. **Review commitment**: `kind=review_commit`, target `run_id`, reviewer run id,
   verdict, rating, rubric scores, error tags, and citations to step-status, ledger
   lines, or CIR signal ids.
3. **Outcome follow-up**: later same-recipe run outcomes, release/rework/revert events,
   recurrence of error tags, and human overrides.

The reviewer rating is a prediction. It should be evaluated with Brier score,
calibration bins, and next-run / next-3-runs reliability, then compared with mechanical
baselines such as step success ratio, prior recipe success rate, and run class.

## Product implication

Build `sequence-review` as a reviewer workflow only after the read model exists. The
first safe product primitive is a read-only evaluator:

```bash
mentu sequence review-ledger --output json
```

or, in the science repo:

```bash
python3 analyses/c23-review-trust-calibration/analyze.py
```

The evaluator should say `instrument_waiting` until there are enough review commits and
later outcomes. Averages are allowed as diagnostics, not verdicts.

## Lessons for Mentu

- A trust score without calibration is a confidence display, not evidence.
- Citation gates are necessary but not sufficient; citations prove grounding, not
  predictive validity.
- The target invariant is scientifically important: accidental latest-run resolution
  contaminates the dataset.
- Review events should be excluded from pre-outcome exposure models for other
  conjectures unless they are explicitly the predictor under test.
