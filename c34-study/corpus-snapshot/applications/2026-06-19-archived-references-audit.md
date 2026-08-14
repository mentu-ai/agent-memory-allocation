# Archived references audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/docs/archived/references/readme-epistemic-engine.md.txt`
- `Workspaces/mentu-physics/foundational/blueprint/docs/archived/references/readme-infraos.md.txt`
- `Workspaces/mentu-physics/foundational/blueprint/docs/archived/references/readme-ese.md`
- `Workspaces/mentu-physics/foundational/blueprint/docs/archived/references/readme-ese.md.txt`

`readme-ese.md` and `readme-ese.md.txt` are identical. No predecessor files were
edited.

## Decision

Admit **C17 schema-portable CIR processing**:
`corpus/conjectures/c17-schema-portable-cir-processing.md`.

The archived references are product/platform READMEs with strong claims: Universal
CIR, schema-agnostic processing, 100% coverage, 97% cost savings, multi-tenant
zero-migration deployment, and external-first evaluation. The admitted claim is
narrower: a configurable CIR processor should work across heterogeneous repositories
and schemas only if per-file coverage, cost, validation, and downstream utility prove
it.

## Dispositions

| Idea | Disposition | Why |
|---|---|---|
| Universal CIR / schema-agnostic processing | **Admitted as C17** | Portability across repos, schemas, and file types is measurable with per-file manifests and outcomes. |
| 97% / 84% cost savings | **C17 outcome, not accepted claim** | Cost savings need full per-file denominator, model/provider costs, validation cost, and accepted-record utility. |
| 100% file or embedding coverage | **C17 coverage metric** | Coverage is useful only when skipped files are counted and produced records are validated. |
| Multi-tenant zero-migration infraOS | **C17 control/outcome** | Tenant id, isolation, resource attribution, and cross-tenant leakage checks can be measured, but are absent here. |
| External-first evaluation protocol | **C14/C11 lineage** | Strong measurement discipline, but not distinct enough for a new conjecture until deployment probes become outcome-linked. |
| Production/market/consciousness claims | **Excluded** | These are not supported by the local instrument and are not needed for the empirical residue. |

## Live readiness digest

`analyses/c17-schema-portable-cir-processing/analyze.py` checks the archived sources
and current Mentu telemetry.

Current source snapshot:

- source files: 4;
- unique content digests: 3;
- Universal CIR term hits: 30 across 2 files;
- schema-portability term hits: 5 across 1 file;
- coverage term hits: 7 across 3 files;
- cost term hits: 32 across 4 files;
- multi-tenant term hits: 41 across 4 files;
- zero-migration term hits: 7 across 1 file;
- external-first / false-positive evaluation term hits: 14 across 2 files.

Current live substrate:

- run outcome rows: 629;
- rows with `total_cost`: 629;
- total recorded run-level cost: 1303.843830;
- median run-level cost: 0.000000;
- rows with `duration_ms`: 629;
- median duration: 47291 ms;
- CIR `file_snapshot` signals: 275;
- exact per-file Universal CIR manifest rows: 0.

This is enough to prove the predecessor corpus had a measurable portability/economics
claim. It is not enough to test the claim. C17 needs repository processing manifests,
file-level cost/coverage records, validation outcomes, and later retrieval/use or
correction events.

## Next push

Add a `cir_processing_file_result` or equivalent event:

- `batch_id`
- `repo_id`
- `tenant_id`
- `schema_id`
- `schema_version`
- `path`
- `extension`
- `bytes`
- `content_hash`
- `processable`
- `status`
- `skip_reason`
- `processor`
- `model_provider`
- `tokens`
- `cost`
- `duration_ms`
- `validation_status`
- `embedding_status`
- `relation_count`
- `output_artifact_id`
- `downstream_use_ids`
- `correction_ids`

Without the coverage denominator and skipped-file records, Universal CIR remains a
product claim rather than a scientific result.
