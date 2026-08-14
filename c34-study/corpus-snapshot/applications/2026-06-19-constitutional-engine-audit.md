# Constitutional engine audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/constitutional-engine/`
- `Workspaces/mentu-physics/foundational/blueprint/constitutional-engine/trust-engine/`

No predecessor files were edited.

## Decision

Admit **C16 conditional activation selectivity**:
`corpus/conjectures/c16-conditional-activation-selectivity.md`.

The audited material describes a full constitutional runtime: object model, modules,
composition grammar, conditional activation, rationalizer, epistemic tuning, and trust
engine. The retained empirical claim is narrower: primitives and context records
activated through explicit runtime predicates should be more useful, less irrelevant,
and less likely to violate trust boundaries than unconditional or retrieval-only
activation.

## Dispositions

| Idea | Disposition | Why |
|---|---|---|
| Conditional activation runtime | **Admitted as C16** | Gives typed state, relationship, temporal, contextual, and trust predicates that can be scored before outcomes. |
| Trust engine authority thresholds | **C16 mechanism, future C17 candidate** | Strong idea, but needs prediction/outcome-calibrated trust logs before becoming a separate conjecture. |
| Rationalizer structural conscience | **C16/C8 lineage** | Runtime approve/modify/reject decisions become activation decisions and guardrail outcomes, not proof of guaranteed safety. |
| Epistemic tuning / conductor | **C16 lineage** | Invocation constructs can be treated as conditional activation predicates over context and user state. |
| Module inheritance/composition grammar | **C15/C13 lineage** | Useful for compiler-readiness and semantic redundancy; separate verdict needs composition outcome logs. |
| Epistemic object model and primitive taxonomy | **Vocabulary/lineage** | Clarifies units, but is not itself a falsifiable claim without lifecycle outcomes. |
| "Constitutional intelligence ecosystem" / "structural conscience" | **Excluded as verdict language** | Architecture rhetoric outruns current instrumentation. |

## Live readiness digest

`analyses/c16-conditional-activation-selectivity/analyze.py` checks both the source
folder and live Mentu telemetry.

Current snapshot:

- constitutional-engine source files scored: 18;
- source files with condition terms: 1;
- source files with trust terms: 12;
- activation mentions: 49;
- conditional/condition mentions: 147;
- source condition categories present: state, relationship, temporal, contextual;
- run outcome rows: 629;
- rows with required selection fields: 629;
- selected runs: 148;
- injected runs: 107;
- used runs: 0;
- context-helped runs: 0;
- total selected signals: 1345;
- total injected signals: 890;
- total used signals: 0;
- CIR activation-like proxy kinds: `semantic_gate_eval` 104, `gate_decision` 15,
  `gate_submission` 15, `gate_triggered` 2;
- exact candidate-level activation decision kinds: 0.

The source corpus has the right conditional vocabulary, and the live system has
aggregate selected/injected outcome rows. It does not yet log candidate-level
activation decisions, skipped/deferred candidates, condition expressions, or
condition-false outcomes. C16 therefore cannot produce a verdict.

## Next push

Add an `activation_decision` signal or equivalent append-only event:

- `candidate_id`
- `artifact_id`
- `condition_id`
- `condition_type`
- `condition_expression_hash`
- `condition_inputs_hash`
- `evaluation_result`
- `activation_decision`
- `reason`
- `thresholds`
- `dependency_ids`
- `run_id`
- `injected`
- `used`
- `outcome_id`
- `correction_or_missed_relevance_id`

Most important: log skipped/deferred candidates. Without false decisions, selectivity
cannot be tested.
