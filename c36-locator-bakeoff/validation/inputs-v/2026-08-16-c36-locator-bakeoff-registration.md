---
id: c36-locator-bakeoff-registration
conjecture: corpus/conjectures/c36-fused-locator-localization.md
status: registration
date: 2026-08-16
author: Rashid Azarang
binds:
  - instruments/2026-08-16-locator-bakeoff-question-regeneration-intent.md
tracking: {}
---

# C36 registration — the locator bake-off design, frozen

Everything an arm needs is pinned here or explicitly deferred to the
harness-freeze commit in `analyses/c36-locator-bakeoff/`, which must exist
**before any question is generated and before any arm runs**. The
predictions and falsification criteria live in the conjecture document and
are already frozen; this document fixes the design that makes them
adjudicable.

## 1. Corpus (G1)

The C34 public snapshot, verbatim: 141 documents, 1,162,998 bytes,
manifest `analyses/c34-public-curation-vs-search-replication/corpus-manifest.json`,
snapshot commit `cb736542a2bfc96a230e8bb9b605d11ff0b87d86`. Every arm and
the question generator read the snapshot copy, never the live estate. Any
hash mismatch at run time aborts the run (the C29 drift lesson: 32/102
documents had drifted when re-verified).

## 2. Arms

| Arm | Locator | Status |
|---|---|---|
| **L0** | `mentu-nav locate --retriever=exact` — the H1-hardened exact leg | baseline |
| **L1** | `--retriever=bm25` — ranked lexical, per-language analyzers | run |
| **L2** | `--retriever=fused` — RRF(k=60) over L0+L1's legs | primary |
| **L3** | cross-lingual dense | **not run**; D3 trigger unfired. This study's cross-language subset measurement can fire it for a successor; recorded, not staked |
| **L4** | SQLite FTS5 (unicode61, porter/en, no es stemmer) behind the same k=8 contract via a thin adapter frozen in the analysis dir | descriptive external control |

The tool contract is identical across arms (intent §8 condition 1): k = 8,
snippet ≤ 240 chars, same `read_range`, same answerer, same prompts, same
scoring rule, same adjudicator. **The single variable per comparison is the
locator composition.** The published C34 rg-harness numbers (75.0%
localization on the *seen* set) are context, not a baseline: L0 is
re-measured fresh under this contract. mentu-navigator's commit is recorded
at harness freeze; any navigator change after this registration is a
recorded deviation.

## 3. Questions (G2–G3, bound verbatim)

Fresh set per the regeneration protocol
(`instruments/2026-08-16-locator-bakeoff-question-regeneration-intent.md`):
frozen `Q_PROMPT` wording, 8,000-char input bound, mechanical acceptance
gates (verbatim / length 3–15 validated not instructed / failable /
non-degenerate / leak), rejection log and per-gate acceptance rates shipped.
**120 confirmatory + 10 smoke** by salted split, same mechanism as C34,
salt drawn at generation and committed. Generation model and operator
prompt pinned at harness freeze.

**Blindness tightening, recorded:** the regeneration intent's G5 froze
predictions after question generation (step 5 after step 4). This
registration freezes them **before** (they are already in the conjecture
document, and no question exists at this commit). Stricter is permitted;
this note is the record.

## 4. Scoring rule (G4 decision, taken now)

The **word-boundary variant** of normalized substring containment is the
adjudicating rule (closes the q073 false-positive class); the C34 rule is
computed alongside and reported descriptively for comparability. Both are
implemented in the frozen analyzer; the `failable` generation gate uses the
adjudicating rule.

## 5. Measures, reported per arm

- Localization: gold ∈ top-8 (adjudicating); gold ∈ top-1 and top-3
  (descriptive).
- Downstream accuracy under the same search-then-read policy (P5).
- Marginal tokens; read events per question.
- Index build cost: median of 5 cold builds + peak RSS (P4), machine
  recorded.
- Per-query wall time per arm (P4).
- Spanish-gold and cross-language subsets, with denominators (P3 guard:
  n ≥ 25 to adjudicate).

## 6. What must exist before the first run (checklist)

1. `analyses/c36-locator-bakeoff/` with: harness, generator+validator,
   adjudicator (both scoring rules), L4 adapter, salts, machine record —
   committed, hash-pinned.
2. Generated question set, hash-pinned, gate rates recorded.
3. This registration and the conjecture document unchanged since this
   commit (any edit is a correction document, not an amendment).

## 7. Relation to the published paper

"Reading More, Finding Less" attributed the curated arm's failure to
mis-routing and left the search arm's own 19.6–25% miss ceiling
unattributed (its §8 names it; intent §2.4 decomposed it post-hoc). C36
tests whether that ceiling is reducible by ranking + morphology. Either
verdict feeds the program: **supported** gives PD-1 its evidence basis and
the paper's successor a constructive result; **refuted** bounds the
paper's "search wins" claim — if even a ranked, fused, per-language
locator cannot beat plain exact search on this corpus class, the miss
ceiling is not a ranking problem, and that is worth publishing at the same
prominence. The verdict is whatever comes out.
