---
id: c36
name: fused-locator-localization
status: tested
registered: 2026-08-16
lineage:
  - corpus/supported/c29-curation-vs-search-sufficiency.md            # parent finding: search beats curated disclosure; search's own miss ceiling left unattributed
  - corpus/conjectures/c34-public-curation-vs-search-replication.md   # the public replication whose corpus snapshot and instrument family this study reuses
  - results/2026-08-14-c34-public-curation-vs-search-replication.md   # seen-set baselines (context only; adjudicate nothing here)
  - instruments/2026-08-16-locator-bakeoff-question-regeneration-intent.md  # the question protocol (gates G1-G6) this registration binds
  - instruments/2026-08-16-c36-locator-bakeoff-registration.md        # the full frozen design
  - paper/agent-memory-allocation/paper-v3.5.md                       # the published anatomy this study extends (intent §2.4: the winning arm's unattributed ceiling)
verdict: revised
result: results/2026-08-16-c36-locator-bakeoff.md
tracking:                      # machine-updated by observatory beats only
  last_beat: 2026-08-16
  note: "registered with predictions frozen BEFORE question generation (tightening of the regeneration intent's G5 order); adjudicates only on run records over the fresh question set; C29/C34 verdicts, thresholds and runs untouched"
---

# C36 — Does a fused ranked-lexical locator raise localization over plain search?

## Claim

On the frozen C34 public corpus (141 documents, snapshot commit
`cb736542a2bfc96a230e8bb9b605d11ff0b87d86`), a fused locator — BM25 with
per-language analyzers reciprocal-rank-fused with hardened exact search,
behind the pinned D4 tool contract — **localizes the gold document more
often than plain exact search under the identical contract**, at acceptable
index cost. This is the constructive converse of C29/C34: those studies
attributed the curated arm's failure to mis-routing; this one tests whether
the *winning* arm's own unattributed miss ceiling (19.6–25% of questions)
is reducible by ranking and morphology, as the C29 miss decomposition
predicts (dominant miss profile: same-language Spanish; cross-lingual only
3/20).

## Frozen predictions (staked 2026-08-16, before any question exists)

All predictions are arm-vs-arm deltas on the same fresh confirmatory set
(n = 120), so they are robust to difficulty shifts between question sets.
Localization = gold document present in the arm's k = 8 hit list.

- **P1 (primary).** L2 (fused) localization exceeds L0 (exact leg, same
  contract) by **≥ +5.0 percentage points**.
- **P2.** L2 localization ≥ L1 (BM25-only) localization (fusion never
  costs localization; Δ ≥ 0.0 pp). If it fails, RRF is retired per the
  ablation registry.
- **P3 (mechanism).** On the subset of questions whose gold document is
  Spanish-language, L2 − L0 ≥ **+8.0 pp**. Adjudicated only if the subset
  has n ≥ 25; otherwise recorded as underpowered and not adjudicated.
- **P4 (cost bound; makes "acceptable cost" mechanical).** Median cold
  index build over the pinned snapshot ≤ **15,000 ms** (5 runs, machine
  recorded), AND median added per-query wall time of L2 over L0 ≤
  **500 ms**.
- **P5 (downstream, directional).** Answer accuracy of the same
  search-then-read policy under L2 ≥ under L0 (Δ ≥ 0.0 pp). A localization
  gain with an accuracy loss is a mechanism finding, reported as such.

## Falsification criteria (mechanical)

- **Refuted** if (L2 − L0) ≤ 0.0 pp on the confirmatory set — the
  framework's locator does not earn its existence (intent §9, clause 1),
  and that is the result.
- **Supported** if P1, P2 and P4 all pass, AND P3 passes or is
  underpowered, AND P5 passes.
- **Revised** otherwise (including: P1 lands in (0, +5.0) pp; P1 passes
  but any adjudicated secondary fails).

Adjudication is by the frozen analyzer committed in
`analyses/c36-locator-bakeoff/` before any arm runs; interpretation never
changes the verdict.

## Scope conditions

One corpus class (a frontmattered operational documentation corpus, es/en
bilingual), one contract (D4: k = 8, 240-char snippets), one harness
family, arm-vs-arm deltas only. Nothing here claims generality beyond that
class; the external control L4 (off-the-shelf SQLite FTS5 behind the same
contract) is descriptive, staked by no prediction, and exists to separate
"our BM25 implementation" from "BM25 the idea."
