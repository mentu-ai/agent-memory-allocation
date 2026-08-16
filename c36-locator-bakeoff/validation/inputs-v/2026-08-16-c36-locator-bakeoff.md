---
id: c36-result
conjecture: corpus/conjectures/c36-fused-locator-localization.md
registration: instruments/2026-08-16-c36-locator-bakeoff-registration.md
date: 2026-08-16
verdict: revised
adjudicated_by: analyses/c36-locator-bakeoff/adjudicate_c36.py (frozen 706ccc6)
records: analyses/c36-locator-bakeoff/runs-c36/ + metrics-c36.json + adjudication-c36.json
---

# C36 result — locator bake-off: **revised**

Mechanical adjudication of the frozen predictions (registered 8604a09,
before any question existed) against the complete run records. n = 115
confirmatory questions (see pre-run correction); machine: macOS 26.3,
arm64, node v22.22.3, python 3.14.6.

## Predictions vs outcomes

| Prediction | Frozen threshold | Measured | Outcome |
|---|---|---|---|
| **P1** L2 − L0 localization | ≥ +5.0 pp | **+13.9 pp** (85.2% vs 71.3%) | **PASS** |
| **P2** L2 ≥ L1 | Δ ≥ 0 pp | **−7.8 pp** (85.2% vs 93.0%) | **FAIL** |
| **P3** Spanish-gold subset | ≥ +8.0 pp, n ≥ 25 | n = 0 | underpowered, not adjudicated |
| **P4** cost bounds | build ≤ 15,000 ms; +query ≤ 500 ms | 193.7 ms; +147.4 ms | **PASS** |
| **P5** downstream accuracy L2 ≥ L0 | Δ ≥ 0 pp | **+5.2 pp** (43.5% vs 38.3%) | **PASS** |

Verdict mapping (frozen): P1 pass with an adjudicated secondary (P2)
failing → **revised**. Interpretation changes nothing below.

## Localization, all arms (gold ∈ top-k, n = 115)

| Arm | @8 | @3 | @1 |
|---|---|---|---|
| L0 exact (baseline) | 71.3% | 60.9% | 43.5% |
| **L1 BM25 only** | **93.0%** | **84.3%** | **65.2%** |
| L2 fused (RRF60) | 85.2% | 73.0% | 53.9% |
| L4 FTS5 external control | 89.6% | 76.5% | 55.7% |

## What the numbers say

1. **The miss ceiling was substantially a ranking problem.** The parent
   studies left search's 19.6–25% miss rate unattributed; ranked lexical
   retrieval removes most of it here (L1 cuts L0's miss rate from 28.7%
   to 7.0%).
2. **Fusion — the framework's shipped default — is retired on this corpus
   class.** BM25-alone beats the fusion by 7.8 pp; folding in the exact
   leg's unranked, file-ordered matches degrades the ranked list. Per the
   pre-registered ablation registry ("RRF fusion: retire if fused ≤ best
   single"), the retirement is automatic. The redesign (BM25-primary
   default, exact leg as a fallback or rank-aware signal) is a design act
   taken outside this study, and any performance claim for it requires a
   fresh registration.
3. **The external control brackets the implementation.** Off-the-shelf
   FTS5 (89.6%) also beats both L0 and the fusion; our BM25 with
   per-language analyzers and field boosts adds +3.4 pp over it. "BM25 the
   idea" does most of the work; the implementation adds a real but modest
   margin; fusion subtracts.
4. **The program's anatomy replicates a third time.** Accuracy conditional
   on locating: 53.7% (L0) / 50.0% (L2). Accuracy without locating: 0.0% /
   5.9%. The downstream accuracy gain (+5.2 pp) is fully accounted for by
   localization — reaching the right document remains the binding stage.
   (Both scoring rules agree within 0.9 pp: boundary 43.5%/38.3%, C34 rule
   42.6%/38.3%; the rule choice did not drive any outcome.)

## Deviations and incidents, disclosed

- Confirmatory n = 115 (not the registered 120) and P3 subset empty: both
  recorded pre-run in `CORRECTION-2026-08-16-denominators-and-p3-power.md`;
  no rule was altered after yields were known.
- Two pre-run error-handling corrections to the harness (generator and
  Phase B), both dated, neither touching gates, thresholds, prompts,
  models, or salts.
- **Premature adjudication incident:** the adjudicator was executed once
  while Phase B was still writing (95/115 L2 records present). Its output
  was discarded, no verdict was recorded from it anywhere, and the frozen
  analyzer was not modified; the adjudication above ran on complete,
  verified-unique records. The incident is disclosed because the analyzer
  does not itself assert P5 denominator completeness — a defect to close
  in successor designs, recorded here rather than patched post hoc.
- Phase A wall-times include node process startup per locate call
  (~100 ms); P4's margins (77× on build, 3.4× on query) make this
  immaterial to any threshold.

## Successors this result motivates (no outcomes anticipated)

- Fusion redesign under fresh registration (rank-aware exact signal vs
  BM25-primary), on this corpus and the estate corpus.
- The Spanish-morphology mechanism test (P3's intent) registered on the
  private estate corpus, where the subset exists.
- PD-1 D3 revision: the shipped `fused` default is now evidence-contradicted
  on this corpus class; the design change is a dated decision in the PD-1
  lineage citing this result.
