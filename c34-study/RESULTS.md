# C34 — public curation-vs-search replication: adjudicated verdict (2026-08-14)

**VERDICT: REVISED** — reason `headroom_not_established_on_marginal_tokens` (the adjudicator's string,
unedited). Produced by the frozen adjudicator over the confirmatory records
sealed at 7b95e02: two replays, byte-identical at
`e73c072fcf1c29d699d998dc5d87f726a76dc4583bd6d6e9d05c5af7ce46c83b`.
Authorized by Rashid Azarang (typed authorization naming 7b95e02, 2026-08-14).
This document is immutable once committed.

## The headline, at equal prominence with the verdict (registered: v2 C-12)

The curation-vs-search question — the study's stake — REPLICATED. The verdict
word is `revised` for a reason orthogonal to it (P4 headroom, below).

| Prediction | Result | Figures (population named) |
|---|---|---|
| **P1 accuracy parity** | **PASS** | acc(B) 63.3% (76/120) vs acc(C) 50.8% (61/120): B **+12.5pp** above C, against a −3pp parity band |
| **P3′ symmetric wrong-stop tax** | **PASS** | wrong-stop C 34.2% ≥ B 18.3% (both over 120 scored; ties pass; the SYMMETRIC rule per D-2) |
| **P5 localization advantage** | **PASS** (both conjuncts, adjudicating) | localization B 75.0% vs C 62.5% (of 120 each); pooled non-hydrated answers incorrect 63/75 = 84.0% ≥ 80%, denominator 75 ≥ floor 20, status observed |
| P2 token order (totals) | PASS | total(B) 21.99M ≤ 2× total(C) 16.94M |
| **P4 headroom (marginal tokens)** | **FAIL — the verdict's sole cause** | marginal B/D **1.84×**, C/D **2.73×**, both below the registered 3× bar |

failed_predictions: ['P4']. Floors: B 120/120, C 120/120,
D 120/120 scored — all above the ≥100 floor. Contamination findings: zero.
Records adjudicated 360; barred (smoke) 30; snapshot cb736542a2bfc96a230e8bb9b605d11ff0b87d86.

## What P4's failure is, and is not (registered in v4 F4's anticipation)

P4 was registered on MARGINAL tokens (D-3) — deliberately the harder reading,
under which the parent's own B would have failed at 2.85×. The replication
returns exactly the anticipated outcome: the agentic arms' marginal cost does
not clear 3× headroom over flat-load. On TOTALS (non-adjudicating, reported
per D-3): B/D 7.56×, C/D 5.82× — would pass. The failure is a statement about
marginal-token headroom against a single-document oracle arm, not about
curation vs search, which is adjudicated by P1/P3′/P5 and replicated.

## Sensitivity rows (non-adjudicating; registered in v4 H4)

Excluding scoring-degenerate golds (n=112) and excluding index-leak golds
(n=117): **neither row flips any prediction** (`predictions_flipped: []` in
both). The v4-flagged imperfections are real and immaterial to every outcome.

## The D-2 vindication (comparability statistic, non-adjudicating)

Under C29's original ASYMMETRIC P3 — C's wrong-stop rate against B's
wrong-ANSWER rate — this data would read C 34.2% vs B 36.7%: **C would have
looked better than B.** Under the registered symmetric rule, C wrong-stops at
nearly twice B's rate (34.2% vs 18.3%). The asymmetric original did not merely
understate the tax; on this corpus it would have reversed the reading.

## Other registered figures

- Fisher exact p (acc B vs C, non-adjudicating): 0.0676 at n=120/arm — the
  +12.5pp margin clears the frozen parity band decisively but is not
  conventionally significant as a superiority test; the registered criterion
  is the parity band, and no superiority claim is made.
- Flat-load D: 80.0% accuracy (96/120) at 8,992 marginal tokens/question —
  the single-document arm remains the accuracy-and-cost ceiling, as designed.
- C's authoring cost: 3,945,524 index tokens (32,879/question amortized;
  100% generator-authored per H6, vs the parent's 52%).
- H5 (registered methodological observation) stands: the byte-identical
  generator prompt produced a 30% sub-3-word gold rate on this corpus vs ~5%
  on the parent's — question-set discriminating power must be measured, not
  assumed, when a prompt crosses corpora.

## Relation to the parent (C29) and the paper

C29 (private client corpus): B +25.5pp, supported. C34 (public corpus, at
power, symmetric rules, harder P4): B +12.5pp, P1/P3′/P5 replicated, verdict
revised on marginal-token headroom. Per the registration's release binding,
this result enters Agent Memory Allocation v2 at claim-site prominence
exactly as adjudicated: the replication carries the curation-vs-search
finding onto a corpus any reader can re-run, and carries the P4 headroom
failure with it, unhidden. The entire study — corpus snapshot, questions,
gold, index, harness, adjudicator, run records, this document — ships in the
public bundle.
