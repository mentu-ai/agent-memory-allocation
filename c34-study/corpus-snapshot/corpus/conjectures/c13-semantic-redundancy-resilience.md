---
id: c13
name: semantic-redundancy-resilience
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap/architecture/tri-layer-cognitive-architecture.md
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap/architecture/tri-layer-cognitive-system.md
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap/architecture/unified-cognitive-architecture-foundation.md
  - Workspaces/mentu-physics/foundational/blueprint/heap/heap/architecture/raw-content/cognitive-infra/participatory-intelligence.md
verdict: null
---

# C13 - Semantic redundancy resilience

## Claim

Artifacts whose identity is redundantly encoded across independent semantic layers
should be more resilient to ambiguity, damage, retrieval drift, and later reuse than
artifacts whose identity is carried by only one surface. Path/domain, semantic
filename, frontmatter, independent handle, schema handle, node reference, and
relationship metadata should act as partially independent recovery routes.

This is the empirical residue of the tri-layer/unified cognitive architecture
material. It does not assert that more metadata is always better. It asks whether
multi-surface identity improves recovery and returnability after controlling for
artifact type, age, domain, and workflow intensity.

## Origin

The architecture files propose five semantic layers plus constitutional memory:
semantic filenames, YAML frontmatter, independent handles, node directories, schema
handles, and project-level precedent/trust records. The participatory-intelligence
essay adds the interface claim: intelligence emerges at the interaction surfaces
between agents, contexts, and knowledge structures. C13 keeps the testable core:
redundant semantic surfaces should improve robustness and reuse.

## Operationalization

**Datasets**:

- `Workspaces/mentu-physics/foundational/blueprint/heap/heap/architecture/`,
  read-only, for initial source-substrate inventory.
- Future artifact first-seen snapshots from Mentu/CIR or LACS:
  path, filename, frontmatter, handle references, schema references, node references,
  relationships, and content hash at capture time.
- Future reuse/recovery events from CIR/LACS:
  retrieval, citation/use, parent/child derivation, repair after missing field, and
  validation results.

**Unit**:

- Primary: one artifact lifecycle, frozen at first seen.
- Secondary: artifact-week when reuse/recovery events become dense enough.

**Predeclared predictor**:

Semantic redundancy score at first seen. One point each for:

- path or folder encodes domain/type;
- semantic filename encodes domain/type/slug/id;
- frontmatter exists;
- frontmatter or body carries stable handle identity;
- independent twin handle exists or artifact is itself a handle;
- schema handle is referenced or available for the artifact domain;
- node or node-candidacy reference exists;
- relationship metadata exists.

High redundancy is `score >= 5`. Low redundancy is `score <= 2`.

**Outcomes**:

- successful retrieval under partial query or missing-surface conditions;
- later use/citation as evidence;
- later parent/child derivation or composition;
- validation success after file movement or partial metadata loss;
- reduced C10 structure-debt classification for the associated run/workspace;
- reduced C12 translation-stage identity loss.

**Controls**:

- artifact type;
- artifact age;
- domain/workspace;
- capture cohort;
- source corpus;
- C7 handle richness;
- C9 pattern exposure/use telemetry;
- C10 structure debt.

## Predictions (stated 2026-06-19, before C13 verdict analysis)

- **P1**: High-redundancy artifacts will be retrieved and reused more often than
  low-redundancy artifacts after type, age, domain, and cohort controls.
- **P2**: High-redundancy artifacts will have lower recovery failure when one surface
  is missing or corrupted.
- **P3**: Redundancy across independent surfaces will outperform equivalent metadata
  volume concentrated in one surface.
- **P4**: The benefit will be strongest for cross-domain and cross-workspace reuse,
  where C10 identity debt and C12 translation debt are otherwise high.

## Falsification criteria

- Semantic redundancy score has no positive association with retrieval, reuse, or
  recovery after controls -> **refuted**.
- Any effect disappears after controlling for handle richness -> **revised** as C7
  handle-mediated returnability, not independent redundancy.
- Any effect disappears after controlling for workspace/domain maturity -> **revised**
  as maturity confounding.
- The analyzer cannot reconstruct first-seen redundancy before outcomes -> **instrument
  insufficient**, no verdict.

## Gate

C13 may produce a verdict only when all are true:

- redundancy scoring rules are frozen before outcome modeling;
- first-seen artifact snapshots exist for at least 500 artifacts;
- at least 8 weeks of post-snapshot reuse/recovery history exist;
- at least one partial-information retrieval or recovery trial is recorded;
- C7 handle richness and C10 structure debt controls are available;
- the analyzer computes redundancy score before inspecting outcomes.

The current source corpus can support a readiness inventory but not a verdict.

## Known limitations

- Richer artifacts may simply be more important artifacts. Importance must be
  controlled through type, domain, age, and source workflow.
- Redundancy can become contradiction if surfaces disagree. C13 predicts resilience
  only for aligned redundancy, not noisy duplication.
- Some fast-capture artifacts should remain low metadata. The claim is not that
  every artifact deserves full constitutional treatment.
- C13 overlaps C7, C10, and C12. Its distinct claim is independent recovery through
  multiple aligned identity surfaces.
