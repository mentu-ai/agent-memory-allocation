# Epistemic computer audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/epistemic-computer/`

No predecessor files were edited.

## Decision

Admit **C18 intent-density capture advantage**:
`corpus/conjectures/c18-intent-density-capture-advantage.md`.

The audited material imagines the Epistemic Computer as hardware, software,
coordinators, agent pipelines, ambient capture, and eventually a physical vessel for
Mentu. The admitted claim is narrower: capture channels with more human intent already
inside them should produce more returnable intelligence per unit cost and privacy
burden than broad passive capture, until passive capture proves otherwise.

## Dispositions

| Idea | Disposition | Why |
|---|---|---|
| Minimum viable signal / written word | **Admitted as C18** | Directly testable as intent-density: explicit notes/imports/highlights vs passive capture. |
| Coordinator / ambient listening hardware | **C18 comparison cohort** | Product vision becomes passive/semi-passive capture modalities, not proof of value. |
| Existing-device abstraction layer vs purpose-built hardware | **C18 lineage** | Becomes a source-quality and modality comparison, not a design verdict. |
| Universal capture across meetings, Slack, Gmail, files | **C18/C17 lineage** | C18 tests modality utility; C17 tests schema-portable processing. |
| Real-time agentic pipelines | **C16 lineage** | Activation/selectivity of live guidance is already covered by C16. |
| Trust Engine for agents | **C16/C7 lineage** | Strong product direction, but not a distinct claim here without trust-prediction logs. |
| Physical product design language | **Excluded as evidence** | Useful imagination, not measurable science. |

## Live readiness digest

`analyses/c18-intent-density-capture-advantage/analyze.py` checks source vocabulary and
local capture/run substrates.

Current source snapshot:

- source files: 8;
- source term counts: explicit text 72, ambient audio 115, visual sensors 26,
  device/hardware 270, privacy/consent 72, return-loop 144, intent/noise 8;
- source coverage: all 8 files contain explicit-text, ambient-audio,
  device/hardware, and return-loop language; 7 files contain privacy/consent
  language; 4 files contain visual-sensor language; 2 files contain explicit
  intent/noise language.

Current live substrate:

- capture archive files: 116;
- capture archive rows: 31,637, all with `op: capture`;
- dominant payload kinds: `file_change` 13,233; `classification` 13,193;
  `embedding` 4,538; `embedding.batch` 211;
- CIR capture-like kinds include `file_snapshot` and `document`;
- run outcome rows: 629, with `source_intent` present on 108 rows;
- run surfaces: `step_brief` 190, `pattern_promote` 119,
  `selector_evidence` 48;
- media relevance training rows: 8,480.

The blocker is structural: current records do not carry per-capture modality,
intent-density, consent/privacy scope, fidelity/quality metrics, or capture-to-return
outcome links. The analyzer found 0 per-capture modality rows, 0 consent/privacy
rows, 0 quality/fidelity rows, and 0 exact `capture_event` CIR signals. The substrate
has capture activity, but not the metadata needed to test capture-channel advantage.

## Next push

Add a `capture_event` or equivalent event:

- `capture_id`
- `modality`
- `source_app_or_device`
- `capture_mode`
- `intent_level`
- `consent_scope`
- `privacy_level`
- `retention_policy`
- `raw_bytes_or_duration`
- `quality_metrics`
- `processing_cost`
- `produced_signal_ids`
- `produced_handle_ids`
- `selected_run_ids`
- `used_outcome_ids`
- `correction_ids`
- `privacy_objection_ids`

Most important: record both high-intent captures and passive captures with the same
denominators. Without passive denominators and privacy outcomes, hardware/ambient
capture remains a product dream rather than a scientific result.
