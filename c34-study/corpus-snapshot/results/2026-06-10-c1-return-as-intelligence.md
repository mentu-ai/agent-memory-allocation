# Result — C1 return-as-intelligence

**Date**: 2026-06-10
**Conjecture**: `corpus/refuted/c1-return-as-intelligence.md` (moved from
`corpus/conjectures/` by this result)
**Analysis**: `analyses/c1-return-as-intelligence/analyze.py` (deterministic;
verified identical across two runs)
**Pre-registration**: predictions P1–P4 and falsification criteria committed at
`c81f500`, before this analysis was first executed.

## Verdict: REFUTED (strong form), as instrumented

The pre-registered criterion — *"use_rate ≈ 0 for the large majority of injected
runs (injection is theater) → refuted in its strong form, regardless of P1"* —
fired unambiguously: **0 of 54** injected runs recorded any use of injected
context. The weak directional form (P1) is **insufficient-evidence**: the success
delta favors injection (42.6% vs 30.5%) but is not significant (p = 0.086) and the
two arms share no common support — not one recipe has ≥3 runs in both arms, so the
delta cannot be separated from recipe mix.

## Dataset digest

- `~/.mentu/training/cir-run-outcomes.jsonl` — **415 runs**, 2026-05-17 →
  2026-06-10, 77 distinct recipes.
- Injected (`injected_count > 0`): 54 runs. Not injected: 361.
- `cir_verdict` distribution: `not_injected` 361, `unproven` 39, `ignored` 15,
  **`proven` 0**.
- Mean `missing_footer_rate` 0.091 — under-reporting exists but cannot explain a
  0/54 usage count.

## Findings against the pre-registered predictions

**P1 (injected runs succeed more)** — *directionally consistent, not established.*
23/54 (42.6%) vs 110/361 (30.5%); odds ratio 1.69; Fisher exact two-tailed
p = 0.0858. Confounding unresolved: the not-injected arm is dominated by
`ane-fortress` (164 runs, median 25s, near-zero cost) while the injected arm is
long experimental runs (median 602s). These are different populations.

**P2 (used context helps more)** — *untestable.* Zero runs have
`context_helped = true`. There is no "helped" stratum to compare.

**P3 (injection is actually used)** — **failed, 0/54.** And decisively so: a
follow-up check confirmed every injected run received a non-empty brief (median
2,262 bytes; none zero), yet `used_count` sums to **zero** across all 54 runs.
Knowledge was delivered and never once cited.

**P4 (injection is not costly)** — *fails at face value, but confounded.* Median
cost $2.77 (injected) vs $0.00 (not injected); attribution to injection is
impossible given the disjoint recipe populations.

## What this means

1. **The return loop is open, not closed.** The CIR pipeline selects signals,
   composes briefs, and delivers them into runs — and then nothing comes back:
   no usage citations, no `proven` verdicts, no `context_helped` flags, in 25 days
   of telemetry. As instrumented today, injection is delivery without consumption.
   The 2025 corpus asserted return-as-intelligence as a foundational principle;
   the first measurement of an actual implementation shows the return half of the
   loop is not happening (or not being attributed).

2. **Two live explanations, both actionable.** Either (a) agents genuinely ignore
   the injected briefs — in which case brief placement/format is wrong — or
   (b) agents use them but the usage-attribution contract (`CIR_USED` footers →
   `used_signal_ids`) fails silently beyond the measured 9% footer loss. The
   per-run data cannot distinguish these; a handful of manual transcript reads
   against injected runs would.

3. **The conjecture is refuted as-implemented, not retired as an idea.** A
   successor (C1b) is warranted only after the loop is closed: usage attribution
   verified end-to-end, and ideally injection randomized within-recipe so the
   arms share support. Until then, any "memory makes runs better" claim about
   this system is unsupported.

## Threats to validity

- Observational data; injection correlates with recipe, run length, and period.
- `use_rate` depends on agent self-report via footers (9.1% known loss) — but the
  delivered-brief check rules out "nothing was injected" as an explanation.
- `context_helped` and `cir_verdict` are produced by Mentu's own eval gate
  (recently shipped "CIR Wave 2"); zero `proven` verdicts may partly reflect a
  young verdict pipeline. That does not rescue the conjecture: it means the
  system cannot currently demonstrate that return helps, which is the claim.

## Verbatim analysis output

```
## C1 analysis output

### Dataset digest
- Records: **415** | date range: 2026-05-17T03:01:57Z -> 2026-06-10T10:12:06Z
- Distinct recipes: 77
- cir_verdict distribution: ignored: 15, not_injected: 361, unproven: 39
- injected_count>0 vs cir_verdict!=not_injected agreement: 415/415
- mean missing_footer_rate (usage under-reporting): 0.091

### P1 — success by injection status
- Injected:     23/54 succeed (42.6%)
- Not injected: 110/361 succeed (30.5%)
- 2x2 table [[23,31],[110,251]] | odds ratio: 1.69 | Fisher exact two-tailed p = 0.0858

### P2 — steps_ok/steps_total by context_helped (injected runs only)
- context_helped=true: n=0 (no step data)
- context_helped=false: n=54, mean steps ratio 0.532, median 0.536, success 42.6%

### P3 — was injected context used? (injected runs only)
- use_rate>0: 0/54 (0.0%)
- use_rate mean 0.000, median 0.000
- (lower bound: usage under-reported when footers missing)

### P4 — cost and duration by injection status
- injected: median cost 2.7697 (mean 8.4398), median duration 602s
- not injected: median cost 0.0000 (mean 0.1220), median duration 25s

### Confounder check — per-recipe success deltas (recipes with >=3 runs per arm)
- No recipe has >=3 runs in both arms; per-recipe inference not possible.
- Aggregate result may reflect recipe mix (Simpson's risk is UNRESOLVED).

### Recipe mix by arm (top 8 per arm) — for reading the confounder
- injected: E3-expr-version (7), openai-smoke (6), subcanvas-notion-parity-canvas-e2e (5), reporter-atlas-local-engine (2), E4-loop-rotation (2), VF1-exprmap (2), ara-desktop-harden (2), b084418d (1)
- not injected: ane-fortress (164), ant-recon-refresh (18), board-onramp-demo (10), t1-ui-good (6), t1-ui-bad (6), t1-http-good (6), t1-http-bad (6), t1-metric-good (6)
```

Supplementary check (jq, injected runs only): `{n: 54, brief_bytes_zero: 0,
brief_bytes_median: 2262, used_count_total: 0, unproven: 39, ignored: 15}`.

> **Addendum (same day)**: recommendation 1 was executed. The diagnosis
> (`instruments/2026-06-10-return-loop-diagnosis.md`) resolved the ambiguity in
> "What this means" §2: the attribution chain is sound and agents comply — the
> failure is substrate content (operational exhaust injected as evidence). The
> fair test is specified in `corpus/conjectures/c1b-return-as-intelligence-randomized.md`.

## Recommendations carried forward

1. **To Mentu engineering**: verify the brief→prompt→footer→`used_signal_ids`
   chain end-to-end on one live run; the loop's instrumentation or its consumption
   is broken, and this dataset cannot say which.
2. **To this corpus**: draft C1b only after (1); require within-recipe common
   support, ideally randomized injection.
3. **To C2–C5**: this result raises the bar — every operationalization must check
   that its measuring chain actually closes before interpreting outcomes.
