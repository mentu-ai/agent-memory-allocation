---
id: c16
name: conditional-activation-selectivity
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/constitutional-engine/conditional-activation-runtime-logic.md
  - Workspaces/mentu-physics/foundational/blueprint/constitutional-engine/module-inheritance-composition-grammar.md
  - Workspaces/mentu-physics/foundational/blueprint/constitutional-engine/constitutional-engine-rationalizer.md
  - Workspaces/mentu-physics/foundational/blueprint/constitutional-engine/epistemic-tuning.md
  - Workspaces/mentu-physics/foundational/blueprint/constitutional-engine/trust-engine/trust-engine-architecture-v2.md
verdict: null
---

# C16 - Conditional activation selectivity

## Claim

Epistemic primitives, handles, modules, and context records activated through explicit
runtime predicates should be more useful and less harmful than primitives activated
unconditionally or by coarse retrieval alone. A predicate may be state-based,
relationship-based, temporal, contextual, or trust-calibrated. The expected benefit is
better selectivity: fewer irrelevant activations, fewer unsafe activations, and higher
downstream use among activated records.

This is the testable residue of the constitutional-engine material. It does not admit
"constitutional intelligence" or "structural conscience" as a proven architecture.
It asks whether explicit activation conditions improve the operational behavior of
context selection and module invocation.

## Origin

The audited folder describes a runtime where handles, nodes, modules, objects,
constructs, rationalizer decisions, and trust-engine decisions are activated only when
their conditions are satisfied. The strongest empirical question is not whether this
architecture is profound. It is whether conditional activation beats always-on or
retrieval-only activation.

## Operationalization

**Datasets**:

- Activation decision logs, future:
  - `candidate_id`, `artifact_id`, `condition_id`, `condition_type`;
  - condition expression and version;
  - inputs inspected by the evaluator;
  - evaluation result (`true`, `false`, `unknown`, `error`);
  - reason, threshold, and matched evidence;
  - activation decision (`activate`, `skip`, `defer`, `escalate`);
  - run id, recipe, workspace, timestamp.
- Run/context outcome logs:
  - `~/.mentu/training/cir-run-outcomes.jsonl` aggregate fields:
    `selected_signal_count`, `injected_count`, `used_count`, `context_helped`,
    `injected_signal_ids`;
  - future candidate-level linkage from activation decisions to injected records,
    read/use footers, and run outcomes.
- CIR, read-only:
  - activation/condition/rationalizer/trust decision signals when present;
  - relations from activation decision to candidate, condition, run, and outcome.

**Condition classes**:

- **State**: constitutional state, precedent count, trust score, semantic boundary
  stability.
- **Relationship**: related primitive active, relationship trust, semantic coherence,
  precedent consistency.
- **Temporal**: precedent age, activation sequence, trust stability, semantic evolution
  continuity.
- **Contextual**: context match, trust-network consensus, semantic-context coherence,
  precedent-context compatibility.

**Predeclared predictor**:

Activation specificity at candidate-evaluation time:

- `0`: no logged condition; activated by retrieval/coarse selection only;
- `1`: condition exists but is prose-only or untyped;
- `2`: typed condition with logged true/false result;
- `3`: typed condition with dependency, trust, precedent, and semantic-coherence
  evaluation;
- `4`: typed condition with prior calibration history and candidate-level outcome
  feedback.

**Outcomes**:

- activated candidate is injected into context;
- injected candidate is read or cited by footer/use telemetry;
- activated candidate contributes to verified/proven outcome;
- activation is later corrected as irrelevant, unsafe, stale, or over-permissive;
- skipped candidate is later judged as a missed relevant item;
- run outcome quality and rework rate.

**Controls**:

- retrieval score or semantic similarity;
- artifact type and age;
- workspace and recipe family;
- C7 handle richness;
- C13 semantic redundancy score;
- C15 compiler invocation readiness;
- risk class or trust boundary;
- week/cohort.

## Predictions (stated 2026-06-19, before C16 verdict analysis)

- **P1**: Typed condition activations will have higher used-after-injection rates than
  retrieval-only activations after retrieval score, workspace, recipe, and artifact
  controls.
- **P2**: Typed skip decisions will reduce irrelevant or unsafe injections without
  increasing later missed-relevance corrections beyond the predeclared tolerance.
- **P3**: Relationship and contextual conditions will improve composition/run outcomes
  more than state-only conditions for multi-artifact tasks.
- **P4**: Trust-calibrated conditions will reduce permission/trust-boundary corrections,
  but only if false/deferred decisions are logged; activated-only telemetry is
  insufficient.
- **P5**: Condition specificity remains predictive only if it adds value beyond C7,
  C13, and C15 controls.

## Falsification criteria

- Conditional activation has no positive association with use, verified outcome,
  lower correction rate, or lower irrelevant injection after controls -> **refuted**.
- The effect disappears after controlling for retrieval score or handle richness ->
  **revised** as retrieval/handle quality, not conditional activation.
- Typed conditions reduce injection volume but increase missed-relevance corrections
  materially -> **revised** as over-filtering.
- Verdict analysis that only observes activated candidates is invalid. False/skipped
  candidates are required, or the selectivity claim cannot be tested.

## Gate

C16 may produce a verdict only when all are true:

- condition scoring rules are frozen before outcome modeling;
- at least 1,000 candidate-level activation evaluations exist;
- at least 300 activated and 300 skipped/deferred candidate decisions exist;
- condition expression, type, evaluation result, decision, and reason are logged;
- activated and skipped candidates are linked to run/context outcomes;
- missed-relevance or correction events exist for skipped candidates;
- at least 8 weeks of follow-up exist;
- C7, C13, and C15 controls are available for the same artifacts.

Current Mentu run outcomes expose aggregate selected/injected/use fields, but not
candidate-level condition evaluations or skipped candidates. C16 is therefore a
readiness-gated conjecture, not a verdict.

## Known limitations

- Conditional activation can look better simply by activating easier or safer records.
  Controls for retrieval score, risk class, artifact type, and workspace are required.
- A skipped candidate is invisible unless the system logs skipped candidates. This is
  the main instrumentation risk.
- More selective activation may reduce exploration. Missed-relevance corrections must
  be part of the outcome surface.
- Trust-engine and rationalizer claims are treated here as activation mechanisms. They
  should become separate conjectures only if trust predictions, authority levels, and
  outcome-calibrated trust updates are logged independently.
