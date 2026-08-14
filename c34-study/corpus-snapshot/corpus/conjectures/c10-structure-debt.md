---
id: c10
name: structure-debt
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/docs/implementation/distributed-cognitive-orchestration/essay-bounded-context-pattern.md
  - Workspaces/mentu-physics/foundational/blueprint/docs/implementation/distributed-cognitive-orchestration/multi-repo-coordination/ide-coordination-mvp-approach.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/canon/law-suites/azarang-law-of-modal-layer-architecture.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/ese/canon/theoretical-positions/systems-theory-evolution.md.txt
verdict: null
---

# C10 - Structure debt

## Claim

Unresolved or poorly bounded structural identity predicts operational drag. Runs and
workspace-weeks with ambiguous workspace identity, placeholder labels, cross-boundary
mixing, or missing immutable recipe identity should later show lower success, worse
step ratios, slower closure, or more repeat failures than structurally clean peers.

This is the empirical residue of the bounded-context and modal-layer material. It
does not assert that all boundaries are good. It asks whether unresolved boundaries
and identity debt make autonomous work measurably worse.

## Origin

The distributed-cognitive-orchestration docs describe the monolithic context problem:
large undifferentiated AI contexts conflate domains, break repository boundaries, and
create coordination overhead. The modal-layer law says knowledge-system failures can
often be localized to layer imbalance and poor integration. The retained claim is
operational: when the instrument cannot tell what workspace, recipe version, or
boundary a run belongs to, future work should be more failure-prone.

## Operationalization

**Datasets**:

- `~/.mentu/training/cir-run-outcomes.jsonl`, read-only: `run_id`, `recipe`,
  `started_at`, `success`, `outcome`, `steps_ok`, `steps_total`, `duration_ms`,
  `total_cost`, and any future recipe manifest identity fields.
- `~/.mentu/cir.db`, read-only: `signals.run_id`, `signals.workspace`,
  commitment lifecycle rows, and future coordination/handoff signals.
- `analyses/c10-structure-debt/identity_rules.json`: frozen identity rules, written
  before verdict analysis.

**Unit**:

- Primary: `(workspace, week)`.
- Secondary: one run, for run-level debt diagnostics.

**Predeclared debt components**:

- **Workspace placeholder debt**: workspace is missing, empty, `unknown`, `default`,
  or `cir-pending`.
- **Workspace ambiguity debt**: a single run is associated with multiple canonical
  non-placeholder workspaces.
- **Mixed-placeholder debt**: a run has one real workspace plus placeholder labels,
  indicating partial attribution.
- **Alias debt**: multiple raw workspace labels collapse to one canonical label under
  the frozen identity rules.
- **Recipe identity debt**: run outcome lacks `recipe_manifest_hash`,
  `manifest_hash`, `recipe_hash`, `recipe_version_hash`, or `run_bundle_hash`.
- **Coordination silence debt**: future component; cross-workspace work has no
  explicit handoff/coordination signal in the relevant window.

**Outcomes**:

- run success and warning/failure outcome;
- `steps_ok / steps_total`;
- next-week close count and close latency from commitment lifecycle rows;
- repeat failure rate for the same recipe/workspace within seven days.

**Controls**:

- recipe family;
- step count;
- week/cohort;
- C2 friction week;
- C8 coherence load once recipe manifest identity exists;
- boundary class from C5 where applicable.

## Predictions (stated 2026-06-19, before C10 verdict analysis)

- **P1**: Higher structure-debt index predicts lower next-week production and run
  reliability after workload controls.
- **P2**: Workspace ambiguity and mixed-placeholder debt have stronger negative
  association in multi-step or cross-repo recipes than in one-step smoke tests.
- **P3**: Alias debt and placeholder debt weaken C5 boundary-impedance estimates; C5
  effects should sharpen after excluding or controlling high-debt rows.
- **P4**: If explicit coordination/handoff signals later exist, they should reduce
  the penalty of cross-workspace work.

## Falsification criteria

- Structure debt has no negative association with next-week production or run
  reliability after controls -> **refuted**.
- Association exists only because high-debt rows are harder/heavier recipes -> **revised**
  as recipe-mass confounding.
- Debt predicts observability problems but not operational outcomes -> **revised** as
  instrumentation debt, not structure debt.
- Identity rules are changed after effect inspection -> verdict invalid; reset the
  conjecture with a new frozen rules version.

## Gate

C10 may produce a verdict only when all are true:

- identity rules are frozen before outcome modeling;
- at least 8 weeks of run outcomes;
- at least 10 canonical workspaces with 5 mature weeks each;
- at least 300 run rows;
- at least 80% of run rows join to at least one CIR signal by `run_id`;
- the analyzer computes the debt index before outcome comparison;
- C2 friction surfaces are available for the same window.

The current corpus has enough rows and run-signal join coverage, but not enough
longitudinal span for a verdict.

## Known limitations

- Some debt is an observability artifact. A run can succeed while the instrument
  mislabels its workspace. C10 must distinguish outcome drag from attribution drag.
- Placeholder labels are widespread in historical data. Early estimates may be driven
  by one regime's logging behavior rather than underlying coordination quality.
- Cross-workspace work is sometimes healthy. The debt is unresolved or uncoordinated
  crossing, not boundary crossing itself.
- This conjecture overlaps C5 and C8 but is not identical: C5 tests transfer across
  boundaries; C8 tests guardrail cost/dividend; C10 tests structural identity and
  boundary hygiene.
