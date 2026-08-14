# Result — C2 friction-to-production (first test attempt)

**Date**: 2026-06-10
**Conjecture**: `corpus/conjectures/c2-friction-to-production.md` (remains there;
status unchanged)
**Analysis**: `analyses/c2-friction-to-production/analyze.py` (deterministic per
input; source is live, digest captured at run time)

## Verdict: INCONCLUSIVE — instrument mismatch

Neither the prediction nor the registered falsification criterion can be evaluated:
the commitment surface does not measure the construct the conjecture is about. The
conjecture stays `operationalized` with `verdict: null`, pending a revised
operationalization (C2 rev. 2, below). Per the corpus's own C1 lesson — *check that
the measuring chain closes before interpreting outcomes* — this attempt mostly
yielded instrument knowledge, which is recorded here.

## Pre-analysis deviation (documented)

The registered source, `~/.mentu/commitments/` (11,885 JSON files), failed its
measuring-chain check: stale since 2026-04-09 and 71% of records never transition
(`updated_at == created_at`). Substituted: `~/.mentu/cir.db` `signals` lifecycle
events (`op` ∈ commit/claim/submit/close/approve, with `commitment_id`,
`workspace`, `ts`) — live through the day of analysis. Measures were kept as
registered.

## What the instrument turned out to measure

- **5,845** commitments with a commit event (of 11,530 ids with any lifecycle
  event — partial capture), 2026-03-30 → 2026-06-10. 1,467 closed (25.1%).
- **Closes are machine-paced**: median close latency **2.4 minutes**; 94.1% close
  within an hour; 0.0% take more than 7 days. Cohorts bifurcate into
  instantly-closed and never-closed. "Latency" here measures sequence execution
  speed, not cognitive or organizational drag.
- **Stall conflates abandonment with friction**: cancelled/released commitments
  have no terminal op in this surface, so they appear identical to "stuck."
- **65% of commitments are workspace-`unknown`**, and that stratum's weekly series
  is constant — unmeasurable. Only 3 workspaces met the registered inclusion bar
  (≥30 commitments, ≥5 mature weeks).

## What the measurable remainder showed (for the record)

- Per-workspace (3 strata): rho(stall_t, closes_t+1) **uniformly positive**
  (+0.62, +0.26, +0.88; sign test p = 0.25) — the *opposite sign* of P1, with a
  mundane explanation: a week with a large pending cohort is followed by a week of
  many closes because the backlog clears. Backlog dynamics, not friction.
- Pooled across workspace-weeks: rho = **−0.435**, but driven entirely by
  total-abandonment weeks (stall = 1.00 → 0 next-week closes), i.e., activity
  cessation, not friction throttling production.
- Volume-normalized secondary: median rho −0.14, sign test p = 1.00 — null.

Three small strata, sign flipping with aggregation level, and a construct mismatch:
no reading of this supports *or* refutes the conjecture.

## C2 revised operationalization (to be frozen before next attempt)

1. **Segment actors**: exclude `workflow` auto-steps; keep human- and
   agent-initiated commitments where latency can carry friction meaning.
2. **Production surface**: weekly run successes from `cir-run-outcomes.jsonl`
   (and/or human-closed commitments), not machine close counts.
3. **Friction surface**: `audit.jsonl` per-method durations and error/retry rates
   per workspace-week, plus genuinely open commitment age.
4. **Inclusion bar**: ≥10 strata or the test is not attempted.
5. Predictions re-frozen in the conjecture file before the analysis runs.

## Verbatim analysis output

See `analyses/c2-friction-to-production/analyze.py`; output of record stored at
run time:

```
### Dataset digest
- Commitments with a commit event: **5845** (of 11530 ids with any lifecycle event)
- Date range: 2026-03-30 -> 2026-06-10 (live)
- Closed: 1467 (25.1%) | never-closed: 4378
- Close latency (h): median 0.04, share <1h 94.1%, share >7d 0.0%
- Workspaces: 135; 'unknown' share 65.2%

| workspace | n | weeks | rho(stall_t, closes_t+1) | rho(latency_t, closes_t+1) |
|---|---|---|---|---|
| unknown | 3814 | 10 | n/a (constant series) | n/a (constant series) |
| mentu-ane-ship | 433 | 5 | +0.62 | +0.30 |
| Crawlio-app | 175 | 6 | +0.26 | +0.54 |
| mentu-complete | 145 | 6 | +0.88 | +0.46 |

P1 stall->production: 3 workspaces | negative rho: 0 | positive: 3 | median rho: +0.62 | sign test p = 0.250
P2 latency->production: 3 workspaces | negative rho: 0 | positive: 3 | median rho: +0.46 | sign test p = 0.250
P3 pooled: Q1 19.0 / Q2 14.0 / Q3 19.0 / Q4 0.0 median next-week closes; pooled rho -0.435 (n=39)
Secondary (volume-normalized): 3 workspaces | negative: 2 | positive: 1 | median rho: -0.14 | p = 1.000
```
