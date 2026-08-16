# Correction (2026-08-16, post-generation, pre-run): denominators and P3 power

Recorded after question generation and BEFORE any arm run. No localization
or accuracy number of any arm existed when this was written.

## 1. Confirmatory n = 115, smoke n = 0

The registration pinned 120 confirmatory + 10 smoke. The corpus, under the
G3 gates, yields **115** accepted questions from 141 documents (one per
document, max 3 attempts): 26 documents exhausted their attempts and are
excluded, counted, and listed in `generation-log-c36.json`. Gate
rejections across all attempts: length 75, failable-multidoc 59, verbatim
46, non-degenerate 45, failable-in-question 2; provider errors 0.

The frozen split rule (salted order, first 120 confirmatory, next-salt 10
smoke) applied verbatim to the actual yield assigns all 115 to
confirmatory and none to smoke. That output is adopted as-is. No question
was re-generated, no attempt limit was raised, and no selection rule was
altered after the yield was known — a denominator harvested to meet a
registered target would be worth less than an honest 115. The smoke set's
harness-shakeout purpose is already covered by the 18 freeze tests, which
include live arm smoke.

All predictions are arm-vs-arm deltas with percentage thresholds;
denominators enter only through power, and n = 115 vs 120 changes no
threshold and no adjudication rule.

## 2. P3 is underpowered at n = 0, by the registered guard

The P3 subset rule (gold documents carrying a `lang: es` frontmatter tag,
mechanical, fixed at generation time) yields an **empty subset**: the C34
public snapshot carries no such tags. The conjecture's n ≥ 25 guard
therefore fires and **P3 adjudicates nothing** — recorded as underpowered,
exactly as pre-registered. The Spanish-morphology mechanism claim (D3
basis: the private estate corpus is 83% Spanish) is untestable on this
public corpus and belongs to a successor registered on the estate corpus.
The `supported` verdict path already treats underpowered P3 as
non-blocking ("P3 passes or is underpowered"); nothing changes.

## 3. Incidental finding, reported as-is

The gate-rejection profile is itself evidence for the program's
instructed-vs-enforced claim: the same generator model under the same
frozen prompt, when mechanically gated, needed 2+ attempts on a large
share of documents and still failed 26 of 141 entirely. The per-gate rates
ship in `generation-log-c36.json`; the raw candidate cache (`gen-cache/`)
is committed so every gate decision is replayable.
