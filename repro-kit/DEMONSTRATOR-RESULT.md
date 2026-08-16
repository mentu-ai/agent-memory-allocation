# Public demonstrator result (reference output)

Reference run of `repro_kit.py` over the 16 public questions
(`questions-public.json`, sha256[:16] `820352e5b0b4b147`) across the 17
operator-owned English documents. Answerer `claude-haiku-4-5` (pinned).
0 infrastructure errors; 16 scored per policy. **This is a demonstrator, not
the paper's result** — the paper (§6.5) used a withheld 102-question client
corpus whose committed hashes are the order proof.

| Policy | Accuracy | Total tokens | Wrong-stop |
|---|---|---|---|
| A flat-load | 12.5% | 0.73M | — |
| B grep-then-read | 62.5% | 2.91M | none |
| C index-then-hydrate | 62.5% | 3.08M | 18.75% (3/16 answered from index, wrong; 4 non-hydrated) |
| D oracle (gold file) | 81.25% | 0.36M | — |

## Honest reading (what reproduces, what doesn't, at n=16 English)

- **Reproduces:** the flat-load baseline is near-useless (A 12.5%); the oracle
  is the ceiling (D 81.25%); and **C incurs a wrong-stop tax that B does not**
  — C answered 4/16 from the index tier without hydrating, and 3 of those were
  wrong, while B (which always reads) has no wrong-stop failure mode. This is
  the paper's §4 lossy-semantics mechanism, visible again.
- **Does NOT reproduce at this scale:** the paper's headline **B-over-C
  accuracy gap (+25.5 pp)**. Here B and C *tie* at 62.5%. On 16 short,
  consistently-titled English methodology docs the curated index is good enough
  often enough to close the accuracy gap — exactly the corpus-dependence the
  paper flags as a limit (naming consistency, corpus size, English vs. Spanish,
  one answerer tier). The paper claims sufficiency for its corpus and reports
  these scope conditions; this demonstrator is consistent with them.

The direction that generalizes is the **wrong-stop tax** (curation's failure
mode), not a fixed accuracy margin. A reviewer running this kit should expect
that pattern, not the paper's magnitudes. Machine-readable summary:
`effect-table-public.json`.
