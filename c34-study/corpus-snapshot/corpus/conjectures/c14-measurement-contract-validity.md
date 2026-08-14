---
id: c14
name: measurement-contract-validity
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap/epistemic-physics/measurement-instrumentation-framework.md
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap/epistemic-physics/epistemic-nodes/README.md
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap/epistemic-physics/epistemic-nodes/node-physics-measurement.md
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap/epistemic-physics/epistemic-nodes/constitutional-node-integration.md
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap/epistemic-physics/epistemic-nodes/node-laboratory-interface.md
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap/epistemic-physics/epistemic-nodes/schema-handle-evolution.md
verdict: null
---

# C14 - Measurement contract validity

## Claim

Measurements with explicit contracts should produce more stable and useful later
judgments than measurements that only emit scalar scores or labels. A measurement
contract includes, at minimum: subject, method, value, unit or scale, uncertainty or
tolerance, evidence/lineage, calibration or reference standard, timestamp, and
verification status.

This is the salvageable core of the epistemic-physics measurement and node-laboratory
material. It does not accept the asserted physics constants, physical units, quantum
effects, or F = M x A as established law. It asks whether measurement discipline
itself predicts better downstream epistemic behavior.

## Origin

The audited files repeatedly demand measurement precision, calibration, uncertainty,
traceability, reproducibility, human approval, and constitutional verification. The
old framing overreaches by declaring epistemic mass, force, acceleration, and perfect
compliance thresholds before empirical grounding. C14 keeps the part that can be
tested inside Mentu: richer measurement records should be more reliable than weaker
measurement records.

## Operationalization

**Datasets**:

- `~/.mentu/cir.db`, read-only:
  - `signals.kind`, `signals.ts`, `signals.body`, `signals.summary`;
  - `signals.asserted_confidence`, `signals.verification`;
  - `signals.evidence_ids`, `signals.source_ids`, `signals.trust_chain`;
  - `signals.hash`, `signals.prev_hash`, `signals.merkle_hash`, `signals.run_id`.
- Future outcome surfaces:
  - later `correction`, `correction.judge`, `prediction.judge`, and `verdict` rows;
  - run outcomes and repeat failures for measurements tied to runs.

**Measurement-event candidates**:

- `verdict`
- `semantic_gate_eval`
- `gate_decision`
- `cir_run_outcome`
- `correction.judge`
- `prediction.judge`
- `relevance_verdict`

**Contract components**:

- **Subject**: measurement identifies a run, commitment, evidence target, source, or
  explicit object in body.
- **Method**: measurement records a method, adapter, metric, evaluator, gate,
  protocol, or deterministic procedure.
- **Value**: measurement records a numeric value, boolean outcome, label, or verdict.
- **Unit/scale**: measurement states the unit, scale, denominator, or bounded range.
- **Uncertainty/tolerance**: measurement states uncertainty, tolerance, confidence
  interval, error margin, precision, or measurement confidence separate from the
  asserted value.
- **Calibration/reference**: measurement names a reference standard, baseline,
  calibration, cohort, or comparator.
- **Evidence/lineage**: measurement records evidence ids, source ids, trust chain, or
  hash-chain lineage.
- **Verification**: measurement records a verification state beyond a bare label.

**Predeclared predictor**:

Measurement contract completeness at event time. One point for each component above.
Strong contracts are `score >= 6`; weak contracts are `score <= 3`.

**Outcomes**:

- later correction/reversal of the measured claim;
- disagreement between prediction and observed outcome;
- later verified reuse of the measurement;
- recurrence suppression for a measured failure/warning;
- downstream run reliability when tied to a `run_id`.

**Controls**:

- measurement kind;
- workspace;
- run class or recipe family;
- week/cohort;
- C2 friction;
- C10 structure debt;
- C11 closure edges when available.

## Predictions (stated 2026-06-19, before C14 verdict analysis)

- **P1**: Strong-contract measurements will have lower later correction/reversal
  rates than weak-contract measurements after kind and cohort controls.
- **P2**: Prediction/evaluation measurements with explicit uncertainty or tolerance
  will have better calibration against later outcomes than measurements with only a
  point label.
- **P3**: Measurements with evidence/lineage and verification status will be reused
  more often than unverified, lineage-poor measurements.
- **P4**: The advantage of strong contracts will be largest for semantic gates and
  prediction judgments, where natural-language evaluation is otherwise fragile.

## Falsification criteria

- Contract completeness has no positive association with stability, calibration,
  reuse, or recurrence suppression after controls -> **refuted**.
- Effects disappear after controlling for measurement kind -> **revised** as kind
  confounding.
- Effects only track structure debt or workspace maturity -> **revised** as
  instrumentation maturity, not measurement-contract validity.
- Any verdict that treats labels like `machine_verified` as enough without unit/scale
  and uncertainty checks is invalid.

## Gate

C14 may produce a verdict only when all are true:

- contract scoring rules are frozen before outcome modeling;
- at least 300 measurement events in scope;
- at least 100 events include explicit uncertainty/tolerance or calibrated confidence;
- at least 50 events include unit/scale metadata;
- at least 10 events include calibration/reference metadata;
- at least 8 weeks of later correction/reuse/outcome history exist;
- contract score is computed before outcome comparison.

The current CIR substrate has many measurement-like events, confidence values,
verification labels, evidence/source references, trust chains, and hash lineage. It
does not yet have enough explicit units, uncertainty budgets, or calibration/reference
standards for a verdict.

## Known limitations

- More complete measurement contracts may be used on higher-stakes work. Control for
  measurement kind, recipe family, workspace, and cohort before claiming benefit.
- A complete contract can still be wrong. C14 predicts better stability and calibration,
  not truth by formatting.
- Some useful measurements are qualitative. They still need an explicit scale,
  uncertainty/tolerance, or review protocol to be comparable.
- This overlaps C11 but is distinct: C11 asks whether measurements cause response;
  C14 asks whether measurement records themselves are well-formed enough to be trusted.
