---
id: c7
name: handle-mediated-returnability
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/heap/mentu-finder/epistemic-handles/epistemic-handle2.md
  - Workspaces/mentu-physics/foundational/blueprint/heap/mentu-finder/epistemic-handles/epistemic-handles.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/heap/mentu-finder/schema-handles-architecture/schema-handles-architecture.md
  - Crawlio-app/docs/BUILD-Local-Artifact-Capture-System.md
  - Crawlio-app/Sources/CrawlioCore/LACS/
verdict: null
tracking:                      # machine-updated by observatory beats only
  last_beat: 2026-07-13
  retention_regime: "2026-07-08 exhaust purge (instruments/2026-07-08-cir-exhaust-purge-regime-note.md): uncited handle_snapshot rows now live <=14 days with a 7-day trust half-life; cited (consolidated) handles persist. Returnability windows >14d are UNMEASURABLE for uncited handles from 2026-07-08 on; any C7 rate over a window spanning that date mixes two retention regimes — never pool."
  watch: [packets/2026-07-13.md]
---

# C7 - Handle-mediated returnability

## Claim

An artifact becomes more returnable when it has a rich epistemic handle: typed
identity, lineage, project or domain scope, tags, and a human-legible summary. Under
comparable age and artifact type, richer handles should be more likely than sparse
handles to be found again, used as parents, composed into derived artifacts, and
promoted out of ephemerality.

This does not claim that a handle is intrinsically meaningful. It claims that a
specific representational affordance creates measurable reuse. If the handle layer is
doing real work, richer anchors should predict later return.

## Origin

Mentu Finder treated "epistemic handles" as stable identity/trust/consent anchors for
semantic work: addressable references that can carry context, relationships,
provenance, and policy. Crawlio's Local Artifact Capture System (LACS) is the first
live substrate that materially resembles that idea. Its `EpistemicHandle` separates a
Soul (identity, type, hashes, parents, project, tags, domain, status) from a Body
(media, bytes, summary, metadata), writes a chain ledger, and maintains indices by
type, project, time, parent, tag, semantic hash, and domain.

The conceptual jump is therefore testable. Mentu Finder said handles should make
meaning addressable. Crawlio LACS lets this corpus ask whether addressability predicts
return.

## Current substrate digest (read-only, 2026-06-19)

Source: `~/Library/Application Support/Crawlio/lacs/`, read directly without editing
Crawlio.

- Handles parsed: 8,760; corrupt handle JSON: 0.
- Created range: 2026-05-21T05:55:28Z to 2026-06-19T05:30:17Z.
- Top artifact types: `crawlResult` 2,191; `kbEntryRef` 1,708; `record` 1,315;
  `derivedQuery` 1,120; `screenshot` 512; `domSnapshot` 509; `networkCapture` 362.
- Status counts: `ephemeral` 7,581; `forged` 1,179.
- Parent counts: 5,575 handles have no parent; 1,863 have one parent; 1,175 have
  three parents; several derived/query handles have large parent sets.
- Scope fields: 2,053 handles have a project id; 8,730 have a registrable domain.
- Ledger rows: 67,956. Top ops: `capture` 32,843; `expire` 29,631; `query` 3,191;
  `forge` 1,179; `compose` 1,112.
- Index rows: `by-parent` 91,968; `by-tag` 22,333; `by-domain` 8,970; primary
  handle-index families each have about 8,760 rows.

This is enough to admit the conjecture. It is not yet enough for a verdict, because
the analysis must avoid leaking post-capture mutations into the predictor.

## Operationalization

**Datasets**:

- Crawlio LACS handle JSON:
  `~/Library/Application Support/Crawlio/lacs/handles/*/handle.json`.
- Crawlio LACS ledger: `~/Library/Application Support/Crawlio/lacs/ledger/chain.log`.
- Crawlio LACS indices: `~/Library/Application Support/Crawlio/lacs/indices/*.jsonl`.
- Crawlio source is used only to interpret fields, not as evidence of effect.

**Unit**:

- Primary: one handle lifecycle, observed from creation through the analysis cutoff.
- Secondary: handle-week, if the ledger and indices can support time-sliced outcomes.

**Predeclared predictor**:

Anchor richness at or near handle creation. Score one point each for:

- non-empty `parents`;
- non-empty `projectID`;
- non-empty `registrableDomain`;
- non-empty `tags`;
- non-empty `body.summary`.

Rich handles are `anchor_score >= 3`. Sparse handles are `anchor_score <= 1`.
`status` is not part of the predictor because promotion is an outcome.

**Outcomes**:

- **Lineage return**: later use as a parent by another handle.
- **Query return**: inclusion as a parent of a `derivedQuery` handle or a ledger
  `query`/`derivedQuery` operation.
- **Composition return**: inclusion in `compose`, `diff`, `discover`, or other
  derived artifacts when those operations are present.
- **Promotion**: transition from `ephemeral` to `forged` or `canonical`, measured
  only if transition timing can be reconstructed without leakage.

**Controls**:

- artifact type;
- handle age;
- registrable domain;
- project id, when present;
- created-day cohort;
- source operation (`capture`, `forge`, `query`, `compose`) where reconstructable.

**Required temporal guardrail**:

Predictor features must come from a first-seen snapshot. If the current handle JSON is
the only source for a feature and that feature can mutate after creation, it cannot be
used for a verdict model. The analysis may report this as an instrument gap, but it
must not silently treat current mutated metadata as original metadata.

## Predictions (stated 2026-06-19, before C7 analysis)

- **P1**: Rich handles have higher later lineage return than sparse handles after
  controlling for artifact type, age, domain, and created-day cohort.
- **P2**: Rich handles are overrepresented among handles returned by
  `derivedQuery`/query artifacts compared with their base rate in the same artifact
  type and age cohorts.
- **P3**: Handles with both lineage (`parents`) and semantic surface (`tags` or
  `summary`) have higher composition return than handles with only one of those
  surfaces.
- **P4**: If promotion timing is reconstructable, richer handles promote out of
  ephemerality more often than sparse handles after controls.

## Falsification criteria

- Richness has no positive association with lineage, query, or composition return
  after controls -> **refuted**.
- Any positive association disappears when controlling for artifact type or domain ->
  **revised** as workflow concentration, not handle-mediated returnability.
- The analysis cannot reconstruct first-seen predictor features -> **instrument
  insufficient**, no verdict. The next action would be a LACS snapshot/instrumentation
  fix, not a weaker analysis.
- Promotion is positive but lineage/query/composition are not -> **inconclusive**,
  because promotion can reflect policy rather than return.

## Gate

C7 may produce a verdict only after its deterministic analyzer can produce a frozen
first-seen feature snapshot before outcome comparison. The live substrate already
clears the minimum size gate: at least 5,000 handles, at least 500 query-derived
handles, at least 500 compose operations, at least 20 days of span, and zero corrupt
handle JSON in the read-only digest.

Do not run an ad hoc association test from the shell and backfill the conjecture
afterward. First effect table must come from committed analysis code.

Current readiness run (2026-06-19): `analyses/c7-handle-mediated-returnability/analyze.py`
passes the size gate but reports `INSTRUMENT INSUFFICIENT` for verdict work. The
reason is structural: the ledger lacks predictor snapshots, and `by-parent`,
`by-tag`, and `by-domain` index rows lack event time. This is a hard boundary, not a
statistical inconvenience.

## Known limitations

- LACS uses mutable handle JSON plus append-only indices. Without first-seen snapshots,
  current metadata can leak future reparenting or tag updates into the predictor.
- Crawlio activity is clustered by domain and workflow. A domain that receives more
  work can create both richer handles and more later returns. Domain and cohort
  controls are mandatory.
- Query-derived handles can have very large parent sets; those parent rows may measure
  broad retrieval rather than meaningful reuse. Report query return separately from
  composition return.
- Every LACS artifact already has a handle. The measured contrast is rich vs sparse
  handle anchoring, not handle vs no-handle, unless a separate raw-artifact control is
  introduced later.
