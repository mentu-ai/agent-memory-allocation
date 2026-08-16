# C34 — curation vs search, replicated in public at power

This bundle is a complete empirical study you can re-run. It ships the corpus
it measured, the questions it asked, every answer it received, the code that
scored them, and the verdict that came out — including the part that failed.

**Verdict: `revised`**, machine reason
`headroom_not_established_on_marginal_tokens`.

## What the verdict means

The study asked whether **associative search over raw content** (grep, then
read the hits) matches or beats **curated layered disclosure** (an authored
index, then hydrate the few files it points to). Five predictions were frozen
before any data existed. Four passed and one failed, and the one that failed
is the one the verdict word names.

| Prediction | Result | Figures |
|---|---|---|
| **P1** accuracy parity | **PASS** | search 63.3% (76/120) vs index 50.8% (61/120) — search **+12.5pp** |
| **P3′** symmetric wrong-stop tax | **PASS** | index wrong-stops on 34.2% of questions vs search 18.3% (120 each) |
| **P5** localization advantage | **PASS** | search locates the right file on 75.0% vs index 62.5%; of answers given without ever opening the right file, 84.0% were wrong (63/75) |
| P2 token order | PASS | total(search) 21.99M ≤ 2× total(index) 16.94M |
| **P4** headroom vs oracle | **FAIL** | on marginal tokens, search/oracle 1.84× and index/oracle 2.73×, both under the registered 3× bar |

**Read this carefully, because the verdict word and the finding point in
different directions.** The curation-vs-search question — the thing the study
was built to answer — replicated. Search beat curation on accuracy, on
localization, and on the wrong-stop tax. The verdict is `revised` because a
*fifth, orthogonal* prediction about token headroom against a single-document
oracle arm did not hold on the harder of two possible measures, which the
registration deliberately chose in advance precisely because it was harder.

Reporting that as the verdict rather than burying it is the point. The
registration committed, before any data existed, to publishing whatever came
out.

## What you can re-run

```
python3 run_tests.py            # the full offline suite
python3 adjudicate.py --out /tmp/replay.json
diff effect-table-2026-08-14.json /tmp/replay.json     # must be empty
```

The adjudicator is deterministic over the committed run records. Re-running it
reproduces `effect-table-2026-08-14.json` byte for byte; that is the study's
central reproducibility claim and it takes about a second to check.

`run_tests.py` runs 193 tests here and reports 8 skips. The skips are honest
and explained below — nothing is broken.

## What is in the bundle

| path | what it is |
|---|---|
| `corpus-snapshot/` | the 141 documents measured, in full, at the byte |
| `corpus-manifest.json` | sha256 for every corpus file |
| `rule-R-evaluation-log.json` | all 154 candidates with the clause that accepted or rejected each |
| `questions-2026-08-13.json` | the 141 frozen questions with gold answers and generation provenance |
| `selection-2026-08-13.json` | the salted 120-confirmatory / 10-smoke split |
| `index-2026-08-13.json` | the authored index that policy C consulted |
| `runs/` | 390 run records + per-attempt logs (360 confirmatory, 30 excluded smoke) |
| `effect-table-2026-08-14.json` | the adjudicator's output — every figure above traces here |
| `RESULTS.md` | the dated results document |
| `registration/` | the full chain: conjecture, instrument note, BUILD plan, corrections v2–v5, erratum |
| `*.py`, `tests/` | corpus rule, harness, adjudicator, smoke audit, and the test suite |
| `CONVENTIONS.md` | two working rules this study paid for |
| `BUNDLE-MANIFEST.json` | sha256 for every file in this bundle |

## Three honest caveats

**1. The client-identifier list is redacted.** The corpus-selection rule
excludes any file mentioning third-party client identifiers. That token list
is withheld here — three of its entries are personal names of people not party
to this study. `corpus_rule.py` ships with `CLIENT_TOKENS = []` and the sha256
of the canonical list, so anyone holding the original can prove in one line
that this is the same rule. The rule's *effect* ships in full: the evaluation
log records every accepted and rejected file with its clause and hit counts.
Registered in `registration/correction-v5.md`.

**2. Rule R's enumeration cannot run here.** It reads the `epistemics` git
tree at commit `cb73654`, and no git history ships. What you can verify is
the corpus itself — 141 files against their hashes — and the complete record
of which candidates were accepted and why.

**3. Eight tests skip, for three reasons.** One because the redacted token
list means the smuggled-file dead run has no token to smuggle (it skips rather
than passing vacuously — a test that passes because it tested nothing is worse
than one that says it could not run). Five because they need the git work
tree. Two because they compare against repository files that do not ship: the
parent study's harness and the source of the audit rule.

## Known limitations of the study itself

Carried from the registration, not softened here:

- **Single operator.** Same author, repository, machine and answerer as the
  parent study. What this replication buys is power, public re-runnability and
  a corpus you can hold in full — not operator diversity.
- **Naming consistency plausibly favors search.** This repository's filenames
  are unusually descriptive of their contents, which is the condition under
  which grep is strongest.
- **The index has no search tool.** The comparison is an authored index
  against grep as *sole locators*. It says nothing about an index used
  alongside search, which is the arm the data actually motivate and which is
  deliberately deferred to a separate study.
- **The oracle arm is an approximation** at file granularity, not a true
  ceiling. P4 reads against that approximation.
- **The question set has measured imperfections**, flagged mechanically and
  reported: 8 of 120 confirmatory golds are scoring-degenerate, 3 index
  digests contain their own answer, 1 gold lies outside the slice the
  generator saw. Both sensitivity analyses — excluding the degenerate golds,
  and excluding the leaked ones — flip no prediction. See
  `registration/correction-v4.md`.
- **A methodological finding worth carrying forward**: the question-generation
  prompt was byte-identical to the parent study's, and produced a 30%
  sub-three-word gold rate on this corpus against ~5% on the parent's. Pinning
  a prompt is necessary for comparability and not sufficient for it. Measure
  your question set's discriminating power before spending an answering budget.

## Provenance

Corpus snapshot from `epistemics` at `cb73654`. Answerer
`claude-haiku-4-5-20251001`, generator `claude-sonnet-5`, both pinned before
any call. 687 of 950 registered provider calls spent; the 150-call retry
reserve was never drawn on; the confirmatory pass returned zero errors. Every
milestone was gated in commit order — registration, instrument, corpus
snapshot, question freeze, excluded smoke, confirmatory, adjudication — and
each was audited by a party that did not execute it.

## Adjudicator usage note

Invoke the adjudicator as documented: `python3 adjudicate.py --out
effect-table-replay.json` (any path outside the study directory works). A
bare `python3 adjudicate.py` writes its output under the script's internal
date constant (`effect-table-2026-08-13.json`) — byte-identical content
under a different name — which the bundle's own leak gate then correctly
rejects as an uncommitted artifact. That is the gate working, not a
corruption.
