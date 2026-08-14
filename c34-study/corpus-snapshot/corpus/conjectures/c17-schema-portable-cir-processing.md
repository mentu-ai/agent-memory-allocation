---
id: c17
name: schema-portable-cir-processing
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/docs/archived/references/readme-epistemic-engine.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/archived/references/readme-infraos.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/archived/references/readme-ese.md
  - Workspaces/mentu-physics/foundational/blueprint/docs/archived/references/readme-ese.md.txt
verdict: null
---

# C17 - Schema-portable CIR processing

## Claim

A configurable CIR processor should be able to transform heterogeneous repositories
and file types into useful knowledge records with high coverage, bounded cost, and
comparable downstream utility without building a bespoke processor for every codebase
or tenant.

This is the testable residue of the archived ESE, infraOS, and Epistemic Engine
reference READMEs. It does not admit production-readiness, market-size, consciousness,
or "any codebase" claims. It asks whether schema-portable processing actually works
across different repositories and schemas when measured per file, per batch, and per
downstream use.

## Origin

The archived references repeatedly claim Universal CIR processing, schema-agnostic
configuration, 100% file coverage, 97% cost savings, multi-tenant zero-migration
enhancement, and external-first evaluation. C17 keeps only the empirically meaningful
part: portability across heterogeneous source material, with explicit coverage and
cost accounting, must predict useful knowledge records rather than just more processed
files.

## Operationalization

**Datasets**:

- Repository processing manifests, future:
  - `batch_id`, `repo_id`, `tenant_id`, `schema_id`, `schema_version`;
  - repository language/file-type inventory before processing;
  - per-file path, extension, bytes, hash, processable flag, skip reason;
  - parser/processor used, model/provider used, tokens, dollars, duration;
  - output strategy (`frontmatter`, `sidecar`, `json_twin`, `database_only`);
  - processing status, validation status, embedding status, relation count.
- Outcome and quality surfaces:
  - downstream retrieval/use events;
  - human correction or rejection;
  - validation failures;
  - duplicate/low-value record detection;
  - task outcomes when processed records are selected as context.
- Current partial surfaces:
  - `~/.mentu/training/cir-run-outcomes.jsonl` has run-level `total_cost`,
    duration, selected/injected/use fields;
  - CIR currently has `file_snapshot` signals, but not full Universal CIR batch
    manifests.

**Predeclared predictor**:

Schema-portability discipline at processing time:

- `0`: ad hoc processing, no schema id, no coverage denominator, no per-file cost;
- `1`: schema id present, but no complete per-file manifest;
- `2`: per-file manifest with status, skip reason, duration, and cost;
- `3`: level 2 plus validation, embedding, relation, and output artifact ids;
- `4`: level 3 plus downstream retrieval/use/correction outcomes.

**Outcomes**:

- file coverage: processed or explicitly skipped over total eligible inventory;
- accepted-record rate after validation and human correction;
- cost per accepted record and cost per later-used record;
- processing success by file type, repo, schema, and tenant;
- downstream retrieval/use and verified task contribution;
- tenant isolation incidents or cross-tenant leakage;
- latency and retry burden.

**Controls**:

- file type, file size, binary/text classification;
- repository size and language mix;
- schema complexity;
- model/provider;
- tenant tier or resource limits;
- C15 compiler invocation readiness of produced artifacts;
- C13 semantic redundancy of produced records;
- week/cohort.

## Predictions (stated 2026-06-19, before C17 verdict analysis)

- **P1**: Schema-portable processing with per-file manifests will achieve higher true
  coverage than ad hoc processing because skipped files are counted explicitly instead
  of disappearing.
- **P2**: Cost per accepted record will be lower for reusable schema-portable
  pipelines than for bespoke per-repository processing after file-type and model
  controls.
- **P3**: Success rates will vary materially by file type; any "any codebase" verdict
  that hides file-type failure modes is invalid.
- **P4**: Higher coverage alone will not predict utility unless produced records are
  validated, embedded, and later retrieved or used.
- **P5**: Multi-tenant or zero-migration claims are supported only if tenant identity,
  isolation checks, and resource/cost attribution are logged per batch.

## Falsification criteria

- Schema-portable discipline has no positive association with coverage, accepted-record
  rate, cost per accepted record, downstream use, or lower correction rate after
  controls -> **refuted**.
- Apparent cost savings come from lower quality, lower coverage, missing validation,
  or omitted model/provider costs -> **refuted**.
- Benefits hold only for one repo or one schema family -> **revised** as local
  processor effectiveness, not schema portability.
- Any verdict based on aggregate run cost without per-file denominators is invalid.

## Gate

C17 may produce a verdict only when all are true:

- scoring rules are frozen before outcome modeling;
- at least 20 repository processing batches exist;
- at least 5 distinct repositories and 5 distinct primary file ecosystems exist;
- at least 10,000 file-level manifest rows exist;
- each row has schema id, status, skip reason when skipped, duration, token/cost,
  validation status, and output artifact id when produced;
- at least 1,000 produced records have retrieval/use/correction follow-up;
- at least one baseline exists: ad hoc, bespoke, or prior processor cohort;
- at least 8 weeks of follow-up exist;
- C13 and C15 scores can be computed for produced artifacts.

Current Mentu data has run-level cost and file snapshots, but not Universal CIR
per-file processing manifests or cross-repo utility outcomes. C17 is therefore
readiness-gated.

## Known limitations

- "Coverage" can be gamed by creating low-quality records for every file. Use accepted
  records and later-used records, not raw processed count alone.
- Cost comparisons must include model calls, retries, validation, embedding, storage,
  and human repair where available.
- Heterogeneous repositories are not interchangeable. File type and repo controls are
  required before making portability claims.
- External-first evaluation from the references is important, but it is treated as
  measurement discipline under C14 unless deployment/user-access probes become a
  separate outcome surface.
