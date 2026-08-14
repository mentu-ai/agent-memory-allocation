# Agent Memory Allocation — release bundle

*Tiers and Policies of Effective Agent Memory* — Rashid Azarang, Independent
Researcher · Mentu. Preprint, 2026-08-14.
DOI [10.5281/zenodo.21938413](https://doi.org/10.5281/zenodo.21938413).

## What is here

| File | What it is |
|---|---|
| `agent-memory-allocation.pdf` | the preprint, typeset (31 pp) |
| `agent-memory-allocation.html` | the same text as a single self-contained page |
| `paper-v2.md` | the canonical markdown the two renders are built from |
| `fig1_tier_gradient.png`, `fig2_c29_policies.png` | the two figures |
| `references.bib` | full BibTeX for the reference list |
| `CHANGES-v1.1.md`, `CHANGES-v1.2.md`, `CHANGES-v2.md` | what changed between drafts, itemized |
| `c34-study/` | the C34 public replication in full — corpus snapshot, frozen questions, harness, adjudicator, run records, results |

## On the filenames

The paper is a preprint with no public version number. Three filenames here
still carry the internal draft numbering used in the `epistemics` research
repository that produced it: the canonical markdown (`paper-v2.md`) and the
change documents. They are kept as they are committed, so that a path cited
inside the paper resolves against a real file.

The lineage those names record: the text supersedes earlier drafts, whose own
texts stand unchanged in that repository as `paper-v1.md` and `paper-v1.1.md`.
Every difference between them is itemized in the `CHANGES-*.md` documents
shipped here. No frozen conjecture, analyzer, results document, or effect table
was altered in any revision.

## Where to start

`c34-study/` is the artifact a reader can check rather than take on trust: 141
releasable documents, 120 frozen questions, and a pre-registered replication
whose adjudicator replays byte-identically. Its own README explains how to
re-run it.
