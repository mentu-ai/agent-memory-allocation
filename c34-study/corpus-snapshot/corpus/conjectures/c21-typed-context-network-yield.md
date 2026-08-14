---
id: c21
name: typed-context-network-yield
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/operating-system/epistemic-infrastructure-for-post-agent-intelligence.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/How Context Modules Help.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/Structuring Recursive.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/engine/Structuring Relationships.md
verdict: null
---

# C21 - Typed context-network yield

## Claim

Context modules connected by explicit, typed, quality-maintained relationships should
produce better navigation, composition, transfer, reuse, and maintenance outcomes than
isolated modules, untyped links, or citation-heavy relation graphs.

The claim is not that more links are better. It predicts that relationship type,
directionality, context dependency, interaction guidance, topology, and health checks
matter. Over-connected or poorly specified networks should perform worse than sparse,
meaningful networks.

## Origin

The audited files describe context modules as bounded knowledge units, then move from
module-level structure to network-level relationships and recursive evolution maps.
The strongest new residue is the relationship taxonomy: dependencies,
complements, refinements, translations, tensions, sequence relations, simultaneous
application relations, topology patterns, health checks, bottleneck/orphan detection,
and evolution trajectory monitoring.

C21 keeps that as a network-navigation and composition hypothesis. It does not admit
"post-agent intelligence" or collective intelligence as achieved.

## Operationalization

**Datasets**:

- Future context-network relationship snapshots:
  - `network_snapshot_id`, `artifact_id`, `module_id`;
  - edge `source_module_id`, `target_module_id`, `relationship_type`;
  - directionality, strength, context dependency, interaction mode;
  - boundary interaction and assumption compatibility;
  - application guidance, sequence recommendations, composition guidelines,
    potential conflicts;
  - topology features: degree, cluster, bridge score, centrality, redundancy,
    orphan/bottleneck flags;
  - relationship quality ratings: semantic accuracy, utility, currency,
    completeness, consistency;
  - relationship source: author-declared, inferred, user-confirmed, usage-derived;
  - relationship changes over time with reason and validation status.
- Current partial surfaces:
  - `~/.mentu/cir.db` has a `relations` table with typed edges, currently dominated
    by `cites` and `extends`.
  - The epistemics corpus has lineage frontmatter and textual C-number references, but
    little explicit context-network relationship metadata.
  - `~/.mentu/training/cir-run-outcomes.jsonl` has run outcomes, but no explicit
    relationship-navigation exposure/use telemetry.

**Predeclared predictor**:

Typed-context-network completeness score at exposure time:

- `0`: isolated artifact or no edge.
- `1`: untyped link/citation only.
- `2`: basic relation type and direction.
- `3`: relation type, direction, strength, and context dependency.
- `4`: above plus interaction guidance, assumptions/boundaries, and topology metrics.
- `5`: above plus relationship quality assessment and downstream navigation/use links.

**Outcomes**:

- successful navigation from one module/artifact to a useful related module;
- relationship traversal used in context selection, prompt construction, or result
  synthesis;
- downstream read/use/citation or proven contribution after relationship exposure;
- composition success and later reuse;
- translation success across boundaries;
- correction/revert caused by misleading, stale, missing, or over-broad relations;
- orphan/bottleneck resolution and reduced search/rework time.

**Controls**:

- artifact type, size, workspace, and age;
- relation type and source;
- graph degree, centrality, and cluster;
- query/task class and boundary class;
- C7 handle richness;
- C13 semantic redundancy;
- C15 compiler invocation readiness;
- C16 conditional activation selectivity;
- C19 governed-evolution completeness.

## Predictions (stated 2026-06-19, before C21 verdict analysis)

- **P1**: Typed relationships with guidance and quality metadata will have higher
  downstream use and lower correction rates than untyped citations.
- **P2**: Translation and bridge relationships will help most on cross-boundary tasks,
  while dependency/prerequisite relationships will help most on learning or sequential
  implementation tasks.
- **P3**: Network topology will have a non-linear effect: orphan and bottleneck modules
  hurt navigation, but indiscriminate high-degree linking also reduces utility.
- **P4**: Relationship health checks should reduce stale or misleading traversals over
  time.
- **P5**: If the apparent benefit disappears after C7/C13/C15/C16/C19 controls, the
  claim should be revised toward handle/redundancy/compiler/activation/governance
  quality rather than context-network topology.

## Falsification criteria

- Typed context-network completeness has no positive association with navigation use,
  composition success, transfer, downstream utility, or lower relation-caused
  corrections after controls -> **refuted**.
- Unstructured citations perform as well as typed relationships on utility per review
  cost -> **revised** toward a simpler citation-network claim.
- High relation density predicts worse outcomes after controls -> **revised** toward an
  optimal-sparsity claim.
- A verdict that excludes failed traversals, skipped edges, orphan modules, stale
  relations, or over-connected modules is invalid.

## Gate

C21 may produce a verdict only when all are true:

- scoring rules are frozen before outcome modeling;
- at least 5,000 relationship exposures are logged, including skipped/non-selected
  candidate edges;
- at least 1,000 typed context-network relationships exist across at least 10 declared
  relationship types;
- at least 500 untyped/citation-only matched relationships exist as comparison cohort;
- relationship records include direction, strength, context dependency, interaction
  guidance, topology metrics, and quality/currency assessment;
- exposures link to navigation, context selection, read/use/citation, composition,
  correction/revert, and search/rework outcomes;
- at least 4 weeks of follow-up exist;
- C7/C13/C15/C16/C19 controls are computable for exposed artifacts.

Current data has many CIR relations, but not context-network relationship envelopes,
topology snapshots, exposure denominators, or outcome links. C21 is therefore
readiness-gated.

## Known limitations

- Relationship-rich artifacts may be higher quality for other reasons. Controls for
  handle richness, redundancy, compiler readiness, activation selectivity, and
  governance are mandatory.
- Relationship taxonomies can become decorative. Only relationships exposed to
  navigation/composition or maintenance decisions count toward verdict data.
- Sparse networks may look weak early because their value appears at boundary-crossing
  moments. Outcome classes must separate routine retrieval from cross-domain transfer.
- The network can harm users through over-connection. Relation density is modeled as a
  risk, not merely a benefit.
