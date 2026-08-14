# Orchestration, law-suites, and theoretical positions audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/docs/implementation/distributed-cognitive-orchestration/`
- `Workspaces/mentu-physics/foundational/blueprint/ese/canon/law-suites/`
- `Workspaces/mentu-physics/foundational/blueprint/ese/canon/theoretical-positions/`

No predecessor files were edited. Live checks used direct reads of
`~/.mentu/training/cir-run-outcomes.jsonl` and `~/.mentu/cir.db`.

## Decision

Admit **C10 structure debt**:
`corpus/conjectures/c10-structure-debt.md`.

The distributed orchestration docs and modal-layer law converge on a concrete claim:
monolithic or poorly bounded contexts create operational drag. The current instrument
shows enough structural identity debt to make this worth measuring: placeholder
workspaces, mixed attribution, ambiguous run-to-workspace labels, and missing recipe
manifest identity.

The first readiness analyzer is in `analyses/c10-structure-debt/analyze.py`, with
frozen identity rules in `analyses/c10-structure-debt/identity_rules.json`.

## Live readiness digest

`analyses/c10-structure-debt/analyze.py` reported:

- run rows: 629 across 2026-05-17T03:01:57+00:00 to
  2026-06-19T06:37:08+00:00, a 33.1 day span;
- run-signal join coverage: 620/629 (98.6%);
- run workspace statuses: mixed-placeholder 324, resolved 135, ambiguous-real
  101, placeholder-only 60, missing-signal 9;
- raw workspace labels are dominated by `default` (175566), `cir-pending`
  (25209), `unknown` (21529), and empty string (14383);
- recipe manifest identity is missing from all current run rows;
- verdict readiness: not ready because the 56-day longitudinal gate and the
  10 mature-workspace gate fail.

## Dispositions

| Idea | Disposition | Why |
|---|---|---|
| Bounded context pattern | **Admitted through C10** | Provides the clean causal story for structure debt: context pollution and unresolved boundaries should predict failure/drag. |
| IDE coordination MVP | **C10 instrumentation lineage** | Its message/handoff/changelog surfaces become future coordination-silence debt components. |
| Modal layer architecture | **C10 lineage, not standalone law** | The layer-balance claim becomes measurable as structural identity and integration debt. |
| Acceleration, mass, entropy, impedance law suites | **Already metabolized** | Covered by C2-C6 and C5; constants remain excluded. |
| Darwinian epistemic selection | **Parked** | Potentially maps to pattern/template survival later, but C9 must first expose pattern utility. |
| Wave, oscillation, quantum, relativistic suites | **Parked** | Still metaphor-heavy; no stable current measurement surface beyond C5/C6/C9. |
| Philosophy/systems/cybernetics positions | **Lineage/vocabulary** | Useful for framing; not direct empirical claims against the current instrument. |

## Next push

Keep the frozen identity rules stable, then add:

- exact recipe manifest hashes in run outcomes (shared with C8);
- explicit coordination/handoff signals for cross-workspace work;
- canonical workspace ids at signal ingest time;
- run-level workspace snapshot emitted once per sequence.

That turns structure debt from a diagnostic into a verdict-capable predictor.
