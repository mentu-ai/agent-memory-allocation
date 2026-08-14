# C25 — Return intervention: gate-triggered frozen analysis result (2026-08-12)

**Verdict: INDETERMINATE** — adjudicated mechanically by the frozen analyzer
`analyses/c25-return-intervention/analyze.py` against the pre-registered
criteria (preregistered 2026-07-01T21:30Z), ratified by Rashid Azarang
2026-08-12 (typed decision in the primary session). This document is
immutable once committed.

## Gate event

The gate (condition 1: organic-offer pathway shipped 2026-07-02T18:43:00Z;
condition 2: ≥150 post-intervention runs) was found OPEN at 949
post-intervention runs during a publication-readiness audit on 2026-08-12 —
the observatory beat had been dormant since 2026-07-13 (then 59/150). The
frozen analyzer was run per constitutional rule 5; its complete output
follows verbatim.

## Analyzer output (verbatim)

# C25 — Return intervention (proposed verdict)

**PROPOSED VERDICT: INDETERMINATE** — Return rose above baseline but not by the frozen order-of-magnitude margin at alpha; more accrual or a larger effect needed.

- **P1 (primary)**: post return rate 0.1054% vs baseline 0.0222%; ≥1 order-of-magnitude rise: False; p=0.0875; supported: False
- **P2 (mechanism)**: use-when-offered 50.0000% (used 1, misplaced 0, absent 1); use>0: True; loss mostly misplaced-not-absent: False
- **v2.2 co-intervention**: steer-derived offers 0/2 (steer_message embeddable 2026-07-06; reported separately, not pooled into P1/P2)

*n*: 949 post-intervention runs, 2 offered, 1 used. alpha=0.05.
*Provenance*: input `006f3ee035da2645…`, 2026 rows, source mtime 2026-08-04T18:09:48Z, run 2026-08-12T22:24:00Z.

*This is a PROPOSED verdict for human ratification (AGENTS.md rules 2 & 3). It writes nothing; freezing the result is a constitutional act.*

## Reading (interpretation; changes nothing above)

The intervention raised organic return ~4.7× above the frozen baseline
(0.1054% vs 0.0222%) but did not meet the pre-registered
order-of-magnitude-at-alpha bar (p=0.0875): real signal, short of the
registered success criterion. The offer pathway fired only twice in 949 runs
(1 used) — the binding constraint remains offer scarcity, consistent with the
return-base-rate paper's Stage-0 diagnosis. The two accrual-window
co-interventions (protocol v2.2 steer_message 2026-07-06; CIR exhaust purge
2026-07-08) are disclosed per the tracking block; steer-derived offers are
reported separately (0/2) and were not pooled.
