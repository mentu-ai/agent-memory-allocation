# Reading More, Finding Less — release bundle

*Reading More, Finding Less: A Pre-Registered Anatomy of Progressive
Disclosure for AI Agents* — Rashid Azarang, Independent Researcher.
Preprint, 2026-08-16. DOI
[10.5281/zenodo.21960138](https://doi.org/10.5281/zenodo.21960138); the
concept DOI
[10.5281/zenodo.21938412](https://doi.org/10.5281/zenodo.21938412)
resolves to the current version.

## What is here

| File | What it is |
|---|---|
| `agent-memory-allocation.pdf` | the preprint, typeset (30 pp) |
| `paper.html` | the same text as a single self-contained page |
| `paper.md` | the canonical markdown the renders are built from |
| `fig1_misrouting.png`, `fig2_c29_policies.png` | the two figures |
| `references.bib` | full BibTeX for the reference list |
| `c34-study/` | the public replication in full: corpus snapshot, frozen questions, index, harness, adjudicator, run records, results, tests, registration chain, and `ORDER-PROOF.md` (the commit chain exported for bundle-only readers) |
| `repro-kit/` | the C29 public demonstrator: harness, 17 operator-owned English methodology documents, frozen public question set, reference result (see the paper's §10 and §8 Limits (b′) for what it does and does not establish) |

## One note on the corpus snapshot

`c34-study/corpus-snapshot/` contains the 141 documents the replication
measured, snapshotted at the byte and pinned in
`corpus-manifest.json`. Files inside it with configuration-sounding names
— `CLAUDE.md`, `AGENTS.md`, and similar — are **measured corpus
documents**, not configuration of this bundle: the frozen questions are
about them, the gold answers are substrings of them, and the adjudicator
recomputes generation-input hashes from them. Removing any of them breaks
the manifest, the questions, and the replay.

## Where to start

`c34-study/` is a complete empirical study you can re-run: 141 releasable
documents, 120 frozen confirmatory questions with gold answers, the
one-line-digest index (model-written under the committed prompt, as the
paper's §3 states), all 390 run records with per-attempt logs, the full
registration chain, and the harness, adjudicator, and test suite. Running
`python3 adjudicate.py --out <path>` reproduces the committed effect table
byte for byte (use `--out`; a bare invocation writes under the script's
internal date and the bundle's own leak gate will correctly reject the
uncommitted file). The study's tests run from a plain directory:
`python3 run_tests.py`. The paper's §4 anatomy derives from a withheld
production corpus and re-derives descriptively from this bundle's records
(§5); §5 re-derives from `c34-study/` entirely.
