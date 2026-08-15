# Reading More, Finding Less — release bundle (attribution-corrected text)

*Reading More, Finding Less: A Pre-Registered Anatomy of Mis-Routing in
Curated Agent Retrieval* — Rashid Azarang, Independent Researcher. Preprint,
2026-08-15. This version's DOI is
[10.5281/zenodo.21958917](https://doi.org/10.5281/zenodo.21958917); all
versions resolve from concept DOI
[10.5281/zenodo.21938412](https://doi.org/10.5281/zenodo.21938412). The
immediate predecessor (DOI
[10.5281/zenodo.21947917](https://doi.org/10.5281/zenodo.21947917)) is
superseded on the related-work attribution corrected in `CHANGES-v3.1.md`;
the tier-program version of record is DOI
[10.5281/zenodo.21938413](https://doi.org/10.5281/zenodo.21938413).

## What is here

| File | What it is |
|---|---|
| `agent-memory-allocation.pdf` | the preprint, typeset (22 pp) |
| `paper-v3.1.html` | the same text as a single self-contained page |
| `paper-v3.1.md` | the canonical markdown the renders are built from |
| `fig1_misrouting.png`, `fig2_c29_policies.png` | the two figures |
| `references.bib` | full BibTeX for the reference list |
| `CHANGES-v1.1.md` … `CHANGES-v3.1.md` | what changed between drafts, itemized |
| `c34-study/` | the C34 public replication in full — corpus snapshot, frozen questions, harness, adjudicator, run records, results |

## On the filenames

The paper is a preprint with no public version number. Filenames carry the
internal draft numbering of the `epistemics` research repository that
produced it, kept as committed so that a path cited inside the paper resolves
against a real file. No frozen conjecture, analyzer, results document, or
effect table was altered in any revision. `CHANGES-v3.1.md` records the
attribution correction that produced this version, with the base digest of
the deposited predecessor and every claim site that changed.

## Where to start

`c34-study/` is the public replication at power: 141 releasable documents
snapshotted at the byte, 120 frozen confirmatory questions with gold answers,
the authored index, all run records, and the harness, adjudicator, and test
suite. Re-running `adjudicate.py` reproduces the committed effect table byte
for byte. The paper's §4 anatomy re-derives from the C29 records whose
committed hashes the paper cites; §5 re-derives entirely from `c34-study/`.
