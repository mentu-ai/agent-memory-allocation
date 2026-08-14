---
id: c15
name: compiler-invocation-readiness
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap/gemini/epistemic-matter.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap-june-2025/YAML-Design-Principles.md
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap-june-2025/constitutional-compiler.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap-june-2025/Compiler-Style-Guide.md
verdict: null
---

# C15 - Compiler invocation readiness

## Claim

Artifacts with an explicit compiler-invocation contract should be easier to parse,
validate, compose, and reuse than artifacts with ad hoc metadata or prose-only
identity. The contract includes at minimum: stable identity, title, creation time,
type, author, document type, epistemic status, roles, constitutional function, and
trust semantics. Enhanced contracts add relationships, evolution metadata, return
paths, and callable interface definitions.

This is the testable residue of the epistemic matter, YAML design, and constitutional
compiler material. It does not admit "constitutional compilation" as a new cognitive
physics. It asks whether compiler-callable structure actually improves operational
behavior.

## Origin

The audited files converge on one engineering thesis: a document becomes active
infrastructure when it has enough declared structure for a system to address it,
trust it, validate it, return to it, and invoke it. `epistemic-matter.md.txt` frames
this as a Handle with a Soul and Body. The YAML and compiler files frame it as staged
frontmatter that progresses from genesis identity to callable interfaces.

C15 keeps the measurable part: documents that satisfy a minimal invocation contract
should have better downstream outcomes than documents that do not.

## Operationalization

**Datasets**:

- First-seen artifact snapshots, read-only:
  - path, filename, content hash, frontmatter/YAML payload, timestamp first observed;
  - whether the artifact had Stage 0, Stage 1, and Stage 2+ fields at first sight.
- Compiler/validator logs:
  - parse success or failure;
  - schema validation result;
  - missing-field reports;
  - trust-boundary decisions;
  - relationship resolution result.
- Reuse and composition logs:
  - later references by id/path/handle;
  - inclusion in generated prompts, recipes, or memory briefs;
  - successful relationship traversal;
  - promotion into canonical stores or handles;
  - later corrections caused by ambiguous identity, trust, or function.

**Stage fields**:

- **Stage 0 identity**: `epistemic_id`, `title`, `created`, `type`.
- **Stage 1 compiler-callable minimum**: `author`, `document_type`,
  `epistemic_status`, `epistemic_roles`, `constitutional_function`,
  `trust_semantics`.
- **Stage 2+ enhanced capability**: relationship fields, evolution fields, interface
  definitions, return paths, usage modes, memory traces, or activation hooks.
- **Handle-soul equivalent**: `handle_id`, `timestamp`, `semantic_hash`, `type`,
  `author_key`, `status`.

**Predeclared predictor**:

Compiler invocation readiness at first observation:

- `0`: no parseable frontmatter/YAML contract;
- `1`: Stage 0 complete or handle-soul equivalent complete;
- `2`: Stage 0 and Stage 1 complete;
- `3`: Stage 0 and Stage 1 complete, plus at least one Stage 2+ capability.

**Outcomes**:

- parse success on first compiler pass;
- validation success without manual repair;
- later reuse by stable id or handle;
- successful composition with other artifacts;
- relationship traversal without orphan or alias correction;
- fewer later corrections attributed to identity, trust, or function ambiguity;
- higher downstream task success when the artifact is selected as context.

**Controls**:

- artifact type and size;
- workspace/repository;
- authoring cohort/week;
- artifact maturity age;
- C7 handle richness;
- C13 semantic redundancy score;
- C14 measurement-contract score when the artifact is itself a measurement.

## Predictions (stated 2026-06-19, before C15 verdict analysis)

- **P1**: Stage 1+ artifacts will have higher first-pass parse and validation success
  than artifacts with incomplete or ad hoc metadata.
- **P2**: Stage 2+ artifacts will be reused and composed more often than Stage 0-only
  artifacts after artifact type, age, workspace, and size controls.
- **P3**: Artifacts with explicit trust semantics will produce fewer later trust or
  permission corrections than artifacts with identity fields but no trust boundary.
- **P4**: Relationship fields will reduce orphan-reference and alias-repair events,
  but only when the referenced targets are themselves resolvable.
- **P5**: The C15 effect will partly overlap C7 and C13; it remains supported only if
  compiler readiness adds predictive value after controlling for handle richness and
  semantic redundancy.

## Falsification criteria

- Compiler-readiness score has no positive association with parse success, validation
  success, reuse, composition, or ambiguity reduction after controls -> **refuted**.
- The effect disappears after controlling for C7 handle richness and C13 redundancy ->
  **revised** as a handle/redundancy mechanism, not a distinct compiler-readiness
  effect.
- Stage 2+ metadata predicts worse outcomes because complexity creates repair burden ->
  **revised** toward a minimum-viable-contract claim.
- Any verdict that scores mature edited artifacts without first-seen snapshots is
  invalid, because metadata may have been added after successful reuse.

## Gate

C15 may produce a verdict only when all are true:

- field scoring rules are frozen before outcome modeling;
- at least 500 first-seen artifacts with parseable artifact snapshots exist;
- at least 100 artifacts satisfy Stage 1+ at first observation;
- at least 50 artifacts satisfy Stage 2+ at first observation;
- compiler validation logs exist for artifacts in scope;
- relationship resolution or orphan-reference outcomes exist;
- reuse/composition outcomes have at least 8 weeks of follow-up;
- C7 handle richness and C13 redundancy controls are available for the same artifacts.

The audited legacy files contain a rich design specification and examples. They are
not evidence that compiler-invocable structure works. The initial source-readiness
analyzer also found that the examples are distributed across progressive stages rather
than strict Stage 0 + Stage 1 + Stage 2+ complete specimens. C15 stays readiness-gated
until live artifact and invocation outcomes exist.

## Known limitations

- Metadata quality may be a proxy for human care. Control for author, workspace, age,
  and artifact class before attributing outcomes to compiler readiness.
- More structure can be harmful when it is premature or inconsistent. C15 predicts a
  minimum viable contract plus useful progressive enhancement, not maximal metadata.
- Some useful artifacts are intentionally informal. C15 should compare within artifact
  classes rather than punishing notes that were never meant to be invoked.
- C15 overlaps C7, C13, and C14. Its distinct claim is compiler-callable readiness:
  whether a declared invocation contract improves system behavior beyond handles,
  redundancy, or measurement discipline alone.
