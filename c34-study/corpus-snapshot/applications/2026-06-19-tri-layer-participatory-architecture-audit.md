# Tri-layer and participatory architecture audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/heap/heap/architecture/tri-layer-cognitive-architecture.md`
- `Workspaces/mentu-physics/foundational/blueprint/heap/heap/architecture/tri-layer-cognitive-system.md`
- `Workspaces/mentu-physics/foundational/blueprint/heap/heap/architecture/unified-cognitive-architecture-foundation.md`
- `Workspaces/mentu-physics/foundational/blueprint/heap/heap/architecture/raw-content/cognitive-infra/participatory-intelligence.md`

No predecessor files were edited.

## Decision

Admit **C13 semantic redundancy resilience**:
`corpus/conjectures/c13-semantic-redundancy-resilience.md`.

The architecture docs make many strong claims about five semantic layers,
constitutional memory, node-as-word, self-healing discovery, and exponential
intelligence. The admitted residue is narrower: artifacts with aligned identity
across multiple independent semantic surfaces should be easier to recover, retrieve,
reuse, and validate than artifacts with identity concentrated in one surface.

Participatory intelligence is not admitted as its own conjecture here. Its strongest
role is lineage for the same claim: intelligence emerges at interaction surfaces, so
interface quality and recovery routes matter.

## Live readiness digest

`analyses/c13-semantic-redundancy-resilience/analyze.py` inventories the architecture
directory itself. It reports layer coverage and redundancy scores only; it does not
claim outcome support.

The readiness snapshot reported:

- text artifacts scored: 19;
- path/domain layer present: 8;
- semantic filename layer present: 4;
- frontmatter present: 5;
- handle identity present: 10;
- twin handle present: 9;
- schema reference present: 14;
- node reference present: 9;
- relationship metadata present: 11;
- triple-complete artifacts: 2;
- five-layer-complete artifacts: 1;
- high-redundancy artifacts (`score >= 5`): 7;
- low-redundancy artifacts (`score <= 2`): 7.

Verdict readiness is blocked because the current corpus lacks:

- first-seen artifact snapshots;
- reuse or recovery outcomes;
- partial-information retrieval/recovery trials.

## Dispositions

| Idea | Disposition | Why |
|---|---|---|
| Triple semantic redundancy | **Admitted as C13** | Direct measurable claim: independent identity surfaces should improve recovery and reuse. |
| Five semantic layers | **C13 lineage** | Useful as the layer inventory for redundancy scoring; not accepted as a law. |
| Progressive YAML ladder | **C13 instrument feature** | May become one redundancy surface; effect must be measured, not assumed. |
| Node-as-word | **C13/C9 lineage** | Useful for identity gravity and pattern reuse; outcome belongs in C13 if recovery improves, C9 if patterns outperform raw sources. |
| Independent handles | **Already metabolized by C7** | Rich handle identity is already a returnability conjecture. |
| Schema handles | **C13/C10 lineage** | Schema handles matter when they reduce ambiguity or improve recovery; otherwise they are just metadata. |
| Participatory intelligence | **Lineage/vocabulary** | Frames interfaces as sites of intelligence, but current instrument cannot test social co-construction directly. |
| Exponential intelligence claims | **Excluded from C13** | Rhetorical unless translated into measured reuse/recovery gains. |

## Next push

Instrument first-seen artifact snapshots with:

- path/domain;
- semantic filename parse;
- frontmatter digest;
- handle URI/ref;
- schema domain/ref;
- node reference;
- relationship metadata;
- content hash.

Then add partial-information recovery trials: hide one surface at a time and measure
whether the artifact can still be retrieved, validated, and reused.
