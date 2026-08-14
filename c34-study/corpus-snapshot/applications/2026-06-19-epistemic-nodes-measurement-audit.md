# Epistemic nodes and measurement framework audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/heap/heap/epistemic-physics/epistemic-nodes/`
- `Workspaces/mentu-physics/foundational/blueprint/heap/heap/epistemic-physics/measurement-instrumentation-framework.md`

No predecessor files were edited.

## Decision

Admit **C14 measurement contract validity**:
`corpus/conjectures/c14-measurement-contract-validity.md`.

The audited material is full of physics language: epistemic mass, force,
acceleration, particles, quantum state, and F = M x A. Those claims are not admitted.
The retained empirical residue is measurement discipline: records that carry subject,
method, value, unit/scale, uncertainty/tolerance, calibration/reference,
evidence/lineage, timestamp, and verification should be more stable and useful than
bare labels or scalar scores.

## Live readiness digest

`analyses/c14-measurement-contract-validity/analyze.py` reads CIR read-only and scores
measurement-like signals:

- `verdict`
- `semantic_gate_eval`
- `gate_decision`
- `cir_run_outcome`
- `correction.judge`
- `prediction.judge`
- `relevance_verdict`

The live CIR substrate already has many measurement-adjacent affordances:
verification labels, asserted confidence, evidence/source references, trust chains,
and hash lineage. Verdict readiness is still blocked because explicit unit/scale,
uncertainty/tolerance, and calibration/reference fields are not present in enough
volume to model measurement-contract effects.

Readiness snapshot:

- measurement-like CIR signals: 8774;
- kind counts: `verdict` 6717, `correction.judge` 630, `prediction.judge` 619,
  `cir_run_outcome` 615, `semantic_gate_eval` 104, `relevance_verdict` 74,
  `gate_decision` 15;
- subject coverage: 8701;
- method coverage: 1738;
- value coverage: 5006;
- unit/scale coverage: 10;
- uncertainty/tolerance or confidence coverage: 7351;
- calibration/reference coverage: 4;
- evidence/lineage coverage: 7350;
- verification coverage: 8530;
- strong contracts (`score >= 6`): 269;
- weak contracts (`score <= 3`): 242.

## Dispositions

| Idea | Disposition | Why |
|---|---|---|
| Measurement precision, traceability, uncertainty, calibration | **Admitted as C14** | These are concrete contract fields that can be scored before outcomes. |
| Epistemic nodes as particles | **Lineage/vocabulary** | Useful metaphor for addressable units, but not a standalone empirical claim. |
| Schema handle as physics signature | **C14/C13 lineage** | Becomes valuable only if measurement contracts and semantic redundancy improve stability/recovery. |
| Constitutional node integration | **C14/C8 lineage** | Human approval, lineage, and compliance are treated as contract components or guardrails, not perfect constants. |
| Node laboratory interface | **C14 instrumentation lineage** | Gives the desired event shape: experiment, method, measurement, quality check, notebook entry. |
| F = M x A, quantum effects, exact thresholds | **Excluded** | No calibrated units or independent validation exist. |

## Next push

Add a `measurement_contract` envelope to CIR measurement-like signals:

- `subject`
- `method`
- `value`
- `unit_or_scale`
- `uncertainty_or_tolerance`
- `calibration_reference`
- `evidence_ids`
- `verification_protocol`
- `measured_at`

Then C14 can test whether contract completeness predicts fewer later corrections,
better prediction calibration, and more verified reuse.
