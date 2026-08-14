# Instrument note — C1b eligibility accounting and the first randomized outcome

**Date**: 2026-06-11 (same day as packet 2026-06-11; written by a second beat
invocation — see F4 for provenance).
**Follows**: `observatory/packets/2026-06-11.md`, interpretation item 3
(watch: arm/eligibility accounting gap — "2 eligible runs all-time but only
1 arm recorded").
**Method**: read-only direct file inspection of
`~/.mentu/training/cir-run-outcomes.jsonl` (per the observer-effect rule; no
`mentu` CLI/MCP paths touched).

## Summary

The packet's open accounting gap is resolved, today, with evidence: it is not
an in-flight run. One of the two "eligible" runs predates the deployed
randomizing binary and can never accrue an arm. The eligibility gauge
permanently overcounts by exactly one; the effective randomized-eligible rate
is **1/18 post-regime runs**, not 2/18. The single accrued arm's outcome
record also shows the randomization path working end-to-end in production —
with one recording caveat to confirm before readout.

## Findings

### F1 — The eligibility/arm gap decomposed (packet item 3 resolved)

The two post-regime-boundary runs with non-empty briefs:

| run | time (UTC) | brief | arm |
|---|---|---|---|
| `cua-parity-w3` | 2026-06-10T12:28Z | 6 injected signals (exhaust, old pool) | none — pre-deployment binary |
| `run_rce2e_1781131206` | 2026-06-10T22:40Z | 748 B, 1 distilled signal selected | `withheld` |

`cua-parity-w3` started 9 minutes after the 12:19Z regime boundary but on the
old binary (beat #0 already called it "the old regime's last gasp"); its
record has no `randomization_arm` and never will. The collector's eligibility
counter (non-empty brief prepared) therefore includes one run that can never
enter the experiment. Until `collect.py` is amended to require
`randomization_arm` present (a code change outside beat powers, left to the
maintainer), read the digest's "eligibility" line as an upper bound that is
exactly one high.

### F2 — The first randomized outcome record, examined

`run_rce2e_1781131206` (recipe `rce2e`): brief prepared (748 bytes,
`selected_signal_count` 1, query 28 ms) → coin assigned **withheld** →
`cir_verdict: withheld`, `training_label: cir_withheld_failed` → run outcome
`warn`, steps 0/1, success false, 31 s. The randomization chain works
end-to-end in production: brief built, arm assigned, injection withheld,
counterfactual size recorded, outcome labeled. Two caveats:

1. **No `withheld_signal_ids` field in the outcome record.** The design
   (C1b prerequisite 3) says withheld runs record the counterfactual IDs;
   the JSONL record carries the counterfactual only as
   `selected_signal_count`/`brief_bytes` (`injected_signal_ids` is `[]`).
   The primary analysis (arm × success) is unaffected and P3 stratifies by
   recipe family only — but if any readout analysis wants per-signal
   counterfactuals, confirm the IDs are recoverable from `cir.db` before the
   gate opens. [watch]
2. **The recipe name `rce2e` reads as an E2E exercise of this very path**,
   not organic work. The frozen criterion is mechanical (`randomization_arm`
   set → counts), so the run counts; recorded for transparency. If C1b
   plumbing tests recur they remain visible as the `rce2e` stratum, which the
   pre-registered Mantel–Haenszel combination already isolates per recipe.

### F3 — Timing reconciliation

The arm surfaced in today's digest but accrued 2026-06-10T22:40Z — after
beat #0's hand-collected 20:22Z digest. Daily deltas in the digest are
collection-window deltas, not calendar-day counts (same artifact as today's
packet's C3 reconciliation: 11 → 48 = +37 against "+36 today").

### F4 — Provenance: a duplicate beat dispatch

Two beat invocations fired for 2026-06-11. One collected a digest at
06:13:02Z (handed to the agent writing this note); a parallel invocation
collected at 06:15:07Z, then wrote and committed the day's packet and
tracking updates (`e387f21`) while this one was mid-verification. The canon's
one-packet-per-day rule held because this invocation checked for an existing
packet before writing; the committed packet stands untouched (no retroactive
edits — this dated note carries the marginal evidence instead, per the
corrections rule). Two observatory consequences: (a) the temporal executor's
`epistemics-daily-beat` job double-fired and should be checked before
tomorrow's beat; (b) duplicate beats double the observatory's
self-instrumentation write load (packet item 7's contamination class).
