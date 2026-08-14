# Result — C28 promotion-lane returnability

**Date**: 2026-07-18
**Conjecture**: `corpus/refuted/c28-promotion-lane-returnability.md` (moved on this
verdict; registered same day at M0, commit `4b86195`)
**Analysis**: `analyses/c28-promotion-lane-returnability/analyze.py` (committed
before any output; manifest-only inputs; deterministic)
**Corpus**: `analyses/shared/transcript-manifest-2026-07-18.json` (frozen at M0;
2,337 transcripts; 453 memory files; 0 hash mismatches)
**Effect table**: `analyses/c28-promotion-lane-returnability/effect-table-2026-07-18.json`

## Verdict: REFUTED

Population (frozen definition: ≥30 days post-creation corpus, ≥10 eligible
same-project sessions): **157 files** — floor (≥100) passed.

| Frozen prediction | Threshold | Measured | Outcome |
|---|---|---|---|
| P1 ever re-read | ≥25% | **1.27%** (2 of 157) | fail |
| P2 median eligible-session read rate | ≥1% | **0.0%** | fail |
| P3 indexed ≥3× orphan | if ≥20 orphans (68 exist) | 2.25% vs 0.0% (ratio ∞, on n=2 readers) | technically pass; numerators too small to carry weight |
| P4 median rate <20% | bound | 0.0% | pass (vacuously) |
| **Refutation trigger** | ever ≤10% AND median ≤10×T3 (0.222%) | 1.27% and 0.0% | **fired** |

The two ever-re-read files (`feedback_re_citation_aggressive.md`,
`feedback_re_poll_over_subagents.md`, both in the Subtrace project) each had one
reader in 14 eligible sessions. Median first-recall latency (49.8 days) is an
n=2 statistic and carries no weight.

**What was refuted, precisely**: that promotion to the memory directory
produces later *explicit re-reads* (Read tool events) at rates orders of
magnitude above ambient. It does not. 451 of 453 promoted memory files were
never re-read by any eligible session in the frozen corpus. Capture-without-
return extends into the promotion lane itself.

## The channel caveat — recorded, not exculpatory

The conjecture's registered limitations *declared* that index-only recalls and
harness injection are invisible to this instrument and accepted the bias as
running against P1/P2. The refutation therefore stands under the frozen terms.
But the magnitude of the untested channel must be recorded: the analyzer
counted **18,780** non-tool transcript lines naming memory files (path echoes,
reminder-style injections, index content) against **2** tool reads. The
harness possesses an auto-recall channel (memory content can enter context as
system-reminder blocks without any Read event). Whether that channel delivers
*meaningful* returns is a different, registrable question — a successor
conjecture (injection-channel returnability, candidate c28b) would need an
instrument that parses reminder blocks and matches content hashes, not path
mentions. Named here as a candidate; not registered.

One honesty note: the conjecture's Origin cited a single motivating instance
(a commit-authorship memory read twelve days after writing). That instance
occurred in this program's own session — which the corpus rules exclude as
contaminated. The motivating example was, itself, the observer.

## Instrument knowledge

- 0 of 2,337 prefix hashes mismatched; corpus stable.
- Index membership was measured at freeze (drift over time not
  reconstructable) — with 2 readers total, no conclusion about the pointer
  mechanism survives either way.
- 296 of 453 memory files fell outside the population (young files or
  low-session projects); their exclusion is a coverage fact, not a verdict
  qualifier.

## Interpretation (does not change the verdict)

Under the allocation frame, T1's *explicit-read* return rate (ever ≈1.3%,
per-session median 0) sits far below the registered expectation and close
enough to ambient that C26's P1 ordering (T1 > T2 > T3 with order-of-magnitude
gaps) is now at genuine risk at the T1/T2 boundary — exactly what M2.3 will
adjudicate. The boot-manifest gauge (deployed today,
`instruments/2026-07-18-boot-manifest-gauge.md`) measures the residency side
going forward; the injection channel is the remaining unmeasured path.
