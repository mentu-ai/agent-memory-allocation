# Mentu Finder / Crawlio LACS audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/heap/mentu-finder/`
- `Crawlio-app/`
- `~/Library/Application Support/Crawlio/lacs/`

No Crawlio or mentu-finder files were edited. Crawlio's working tree is dirty and was
treated as user-owned. Live LACS data was read directly from disk.

## What survived the audit

Mentu Finder's strongest idea is not the broad "semantic filesystem" language. The
part that survived contact with a live system is narrower: an epistemic handle is a
stable, typed, addressable anchor that can carry identity, lineage, scope, tags,
summary, and trust/status.

Crawlio's LACS implements enough of that shape to make the idea testable:

- `EpistemicHandle` has a Soul/Body split.
- `ArtifactStore` captures, forges, canonicalizes, expires, reparents, queries, and
  verifies chain integrity.
- `HandleQuery` exposes type, project, parent/child, tag, semantic hash, summary,
  status, domain, and paging constraints.
- `IndexDatabase` writes JSONL indices for type, project, time, parent, tag,
  semantic hash, and domain.
- `ChainLedger` records append-only operations and hash links.

The result is not merely a memory metaphor. It is a local return substrate.

## Live substrate digest

Source: `~/Library/Application Support/Crawlio/lacs/`.

- Handles parsed: 8,760; corrupt handle JSON: 0.
- Created range: 2026-05-21T05:55:28Z to 2026-06-19T05:30:17Z.
- Top artifact types: `crawlResult` 2,191; `kbEntryRef` 1,708; `record` 1,315;
  `derivedQuery` 1,120; `screenshot` 512; `domSnapshot` 509; `networkCapture` 362.
- Status counts: `ephemeral` 7,581; `forged` 1,179.
- Parent distribution: 5,575 handles with no parents; 1,863 with one parent; 1,175
  with three parents; multiple derived/query handles have large parent sets.
- Scope: 2,053 handles have a project id; 8,730 have a registrable domain.
- Ledger rows: 67,956. Top operations: `capture` 32,843; `expire` 29,631;
  `query` 3,191; `forge` 1,179; `compose` 1,112.
- Index rows: `by-parent` 91,968; `by-tag` 22,333; `by-domain` 8,970.

## Decision

Admit **C7 handle-mediated returnability** as an operationalized conjecture:
`corpus/conjectures/c7-handle-mediated-returnability.md`.

The admission is deliberately modest. It does not assert that handles create meaning.
It asks whether richer handles predict later return, composition, query inclusion, or
promotion after controls.

The first readiness analyzer is also in place:
`analyses/c7-handle-mediated-returnability/analyze.py`. Its 2026-06-19 live run
passes the substrate size gate and then correctly blocks verdict analysis as
`INSTRUMENT INSUFFICIENT`: LACS has enough handles, query artifacts, compose ops, and
span, but it does not yet expose first-seen predictor snapshots for mutable fields.

## What was not admitted

- **Schema handles as directory intelligence**: promising, but Crawlio's live LACS
  store measures artifact handles, not directory-level schema inheritance.
- **Linguistic constructs and cognitive primitives**: still mostly conceptual.
  Current data does not expose primitive extraction quality or downstream cognitive
  benefit.
- **Semantic Finder as UI thesis**: product-direction material, not yet a corpus
  claim. It may become testable if UI search sessions are logged with handle returns.

## Next push

Add first-seen handle snapshots or timestamped mutable index events in Crawlio. Until
then, the correct C7 state is `instrument insufficient`, not "run a weaker analysis."
