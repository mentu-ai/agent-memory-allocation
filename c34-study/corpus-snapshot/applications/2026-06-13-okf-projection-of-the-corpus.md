# OKF projection of the corpus — what the lens found

*Date: 2026-06-13. Author: Claude (Opus 4.8). NOT corpus material — no verdicts. The corpus
was projected into an OKF bundle (read-only; corpus and `cir.db` untouched) and inspected with
the OKF tools. These are findings about the corpus's own structure, framed as one run. See the
instrument note `instruments/2026-06-13-okf-projection.md` for the method and safety proof.*

## What was done

`mentu okf project` derived `~/Desktop/epistemics-okf` (32 docs) from the corpus, then the pure
tools (`validate`, `lint`, `context`, `suggest-links`) inspected it. The corpus git tree stayed
clean and `cir.db` stayed byte-identical throughout.

## Findings (one run, 2026-06-13)

- **Conformance.** The raw corpus has no `type` field on any doc (its schema is domain-specific:
  `id` / `status` / `verdict` / `lineage`). Read as OKF it is 32 `type_missing`. The projection
  infers `type` from the directory, so the bundle has **0 type errors**.
- **Graph.** **27 of 32 docs are orphans** (no inbound links). The corpus's graph is real but
  sparse and one-directional: `lineage` points mostly external (the 2025 ESE corpus, roughly
  43% of references) or one-way, with few internal back-edges. The honest reading: the corpus
  has rigorous write and verdict discipline and **no graph or retrieval layer**. That gap is
  exactly what OKF contributes.
- **Retrieval.** `okf context "<return-loop question>"` assembled a real evidence pack: the C1b
  seed plus its lineage (the refuted C1 and the return-loop diagnosis). This is the corpus's
  first retrieval surface. (On mentu's own engine docs the same command assembled a 6-doc pack
  by relevance even though that bundle is 20/20 orphans, i.e. retrieval does not require a dense
  graph.)
- **Densification.** `okf suggest-links` (propose-only) proposes **10 edges** (2 back-refs, 8
  similarity), stable at `--max 200`. The 2 back-refs are correct and high-confidence (score 1):
  `corpus/refuted/c1-return-as-intelligence.md → c1b` and
  `instruments/2026-06-10-return-loop-diagnosis.md → c1b`.
  > An earlier ad-hoc run reported roughly 102 proposals. With the shipped binary and default
  > (and `--max 200`) flags the count is 10. The lower, reproduced number stands; the inflated
  > one is not used.

## Two disciplines this must respect

1. **Immutability.** The two correct back-refs would, if applied, edit
   `corpus/refuted/c1-return-as-intelligence.md` — a frozen file. They must live in the
   projection or a mutable index, never be written into the frozen source. `okf suggest-links
   --apply` is therefore not run against this corpus.
2. **Observer-effect.** Everything above used pure tools; `cir.db` was byte-identical
   throughout. `okf ingest` and `okf lint --cir` against the live db are forbidden here.

## A future-conjecture candidate (noted, not opened)

`okf context` is distilled, graph-structured retrieval over prior knowledge: a candidate
*implementation* of the return loop that C1 refuted as-instrumented and that C1b is now testing
under randomization. This is recorded as a candidate, not opened as a conjecture, and it **must
not be wired into the live run loop while C1b is accruing** — doing so would both contaminate
the experiment and trip the observer-effect. Revisit only after C1b reads out. What the
projection shows today is narrower and real: the corpus had no retrieval layer, and one can be
derived from it without altering it.
