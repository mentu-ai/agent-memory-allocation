# Result — C27 resident-set utilization (first probe run)

**Date**: 2026-07-18
**Conjecture**: `corpus/conjectures/c27-resident-set-utilization.md` (remains there;
`verdict: null` untouched)
**Analysis**: `analyses/c27-resident-set-utilization/analyze.py` (committed `17aaaab`
before any output; manifest-only inputs; deterministic re-run)
**Corpus**: `analyses/shared/transcript-manifest-2026-07-18.json` (frozen at M0
commit `4b86195`, 2026-07-18T22:04:39-06:00; 2,337 transcripts; 0 hash mismatches;
15 empty excluded; 1 program session excluded by rule)
**Effect table**: `analyses/c27-resident-set-utilization/effect-table-2026-07-18.json`

## Verdict: INSTRUMENT INSUFFICIENT — coverage floor

The gate requires ≥500 interactive sessions. The corpus contains **156**
(month cohorts: 2026-06 × 39, 2026-07 × 117; 20 projects — the other two floors
pass). No verdict is issued; the conjecture stays `operationalized`.

## Point estimates (NOT verdict-bearing; floor failed)

Reported for the record because the analyzer computes them mechanically; they
carry no adjudicative weight until a covered run:

| Frozen prediction | Threshold | Point estimate (n=156) | Direction |
|---|---|---|---|
| P1 ever-invoked share of catalog | ≤15% union / ≤20% restricted | **6.8%** union (17/251-scale), **9.6%** restricted | with P1 |
| P2 top-5 share of invocations | ≥60% | **62.5%** | with P2 |
| P3 interactive sessions invoking zero skills | ≥60% | **82.1%** | with P3 |
| P4 dead-listing token share | estimate only | **≈93%** of an est. ≈10.6k listing tokens/session | with P4's direction |
| Refutation triggers | >40% util or top-5 <30% | 9.6% / 62.5% | not triggered |

Denominator route: **union fallback**, as the instrument note anticipated —
per-session catalog reconstruction found listing blocks in only 2 of 2,337
transcripts (system prompts are not stored in session files). Both bias
directions were declared in the committed analyzer; the refutation check ran on
the restricted denominator where utilization reads highest.

## Instrument knowledge gained (the run's real yield)

1. **The transcript corpus is 93% machine.** 2,166 of 2,322 classified sessions
   are headless recipe runs (`agentName ^mentu-` or worktree/stdin dirs); only
   156 are interactive. The retroactive instrument measures a population in
   which the operator's own sessions are a 7% minority. Consequences: (a) the
   500-interactive floor is unreachable in this frozen corpus — at the observed
   rate (~156 per ~6 weeks) a covered corpus exists in roughly 3–4 months of
   accrual; (b) any future floor revision must be a dated amendment, never a
   silent lowering after seeing data (this doc records that the estimates were
   seen at n=156).
2. **Denominator 1 is permanently unavailable retroactively.** Per-session
   catalogs cannot be reconstructed from transcripts (2/2,337). Forward
   instrumentation that logs the resident catalog per session is the only path
   to the per-session denominator — a gauge for the M3 proposal, subject to the
   gauges-before-gates rule.
3. **The union catalog undercounts.** 15 distinct invoked names (44 events)
   matched no pre-freeze on-disk SKILL.md — dominated by `scaffold` (×10),
   `sequence` (×3), and harness built-ins (`loop`, `dataviz`, `init`,
   `artifact-design`). Both numerator and denominator exclude them
   symmetrically, but the catalog-source list in the manifest builder misses
   built-in and recipe-layer skills; a revised builder may add sources only as
   a dated amendment.
4. **Chain integrity held**: 0 of 2,337 prefix hashes mismatched — the frozen
   corpus is stable against post-freeze session resumption.

## Next actions

- M2.2 (C28 promotion-lane returnability) proceeds — its floors do not depend
  on the interactive stratum.
- C27 re-run when either (a) a future frozen corpus reaches 500 interactive
  sessions, or (b) a dated floor amendment is registered with justification
  independent of these point estimates.
