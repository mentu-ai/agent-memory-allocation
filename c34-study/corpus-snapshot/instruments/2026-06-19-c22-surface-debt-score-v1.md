# C22 surface-debt score v1 - 2026-06-19

## Purpose

Freeze the first operational-surface-debt scoring rules before C22 outcome modeling.

This satisfies the first C22 verdict gate in principle: scoring rules now exist as
versioned, deterministic code and can be applied to future `operational_surface_*`
payloads before any failure/rework/cost association is modeled.

## Implementation

Patched `Desktop/epistemics`:

- `analyses/c22-operational-surface-debt/scoring.py`
  - defines score schema `c22.surface_debt_score.v1`;
  - scores `c22.operational_surface_snapshot.v1` as the only pre-outcome exposure
    predictor;
  - scores `c22.operational_surface_observation.v1` and
    `c22.operational_surface_event.v1` as runtime pressure evidence only;
  - marks runtime pressure scores `excluded_from_exposure_model: true`;
  - records factor ids, point contributions, protections, evidence tier, and notes.
- `analyses/c22-operational-surface-debt/analyze.py`
  - reports structured surface signal counts;
  - opportunistically scores any scorable CIR bodies from
    `operational_surface_snapshot`, `operational_surface_observation`, and
    `operational_surface_event`;
  - prints score distribution, pre-outcome score rows, runtime pressure rows, and
    the active score schema.
- `analyses/c22-operational-surface-debt/test_scoring.py`
  - locks contract-mapped multi-surface systems as low-debt when source of truth,
    fallback, inventories, and contracts are present;
  - locks fragmented/manual/spreadsheet/dashboard systems as high-debt;
  - verifies direct tool-call events are runtime pressure, not exposure predictors.

## Score Semantics

Snapshot scoring is the C22 exposure variable:

- score range: `0..5`;
- score source: `pre_outcome_exposure`;
- evidence tier: `sequence_start_snapshot`;
- factors include fragmented multi-surface structure, high interface count,
  dashboard pressure, spreadsheet-factory pressure, manual reconciliation,
  undeclared change contracts, implicit handoffs, missing source-of-truth map,
  missing fallback path, and weak observability;
- protections include source-of-truth map, fallback path, separated inventories,
  MCP health, fully declared expected changes, contract-mapped multi-surface class,
  and single-surface class.

Observation and event scoring is not the C22 exposure variable:

- score source: `runtime_pressure_not_pre_outcome_exposure`;
- evidence tiers: `step_exit_output_scan` and `direct_tool_call_metadata`;
- runtime pressure may include failed tool calls, retries, slow calls, output-derived
  manual reconciliation, spreadsheet evidence, or dashboard evidence;
- these records are useful for outcome and mechanism analysis, but not for assigning
  the pre-run predictor.

## Verification

- `python3 -m unittest discover -s analyses/c22-operational-surface-debt -p 'test_*.py'`
  passed: 9 tests.
- `python3 analyses/c22-operational-surface-debt/analyze.py` passed against the live
  substrate and reported:
  - score schema `c22.surface_debt_score.v1`;
  - 0 structured C22 surface rows in the current CIR database;
  - readiness PASS for frozen scoring rules;
  - readiness FAIL for exposure-volume, outcome-linkage, diagnostic, cohort, and
    control gates.

## Scientific Status

This is not a C22 verdict.

The score is frozen before outcome modeling, but the live dataset still has no
post-instrumentation `operational_surface_snapshot`, `operational_surface_observation`,
or `operational_surface_event` rows. Future Mentu runs can now produce scored exposure
records; C22 still needs 1,000 scored exposure rows, matched cohorts, outcome linkage,
diagnostic samples, controls, and follow-up before verdict analysis.
