# 2026-07-06 — C25 co-intervention amendment (reporting-only, gate still closed)

*Instrument/amendment note. Discharges Obligation 1 of the protocol v2.2 impact
audit (`instruments/2026-07-06-protocol-v22-regime-boundary-and-impact.md`). Touches
no frozen prediction, falsification rule, threshold, verdict, or result. The C25 gate
is CLOSED (6/150 post-intervention runs at write time); this lands before it can open,
per the corpus discipline of declaring instrument changes before readouts.*

## What changed upstream

Protocol v2.2 (engine `949a018`, deployed 2026-07-06T14:54:43Z) made `steer_message`
a **CIR-ingested, embeddable** signal kind: mid-run human steer messages are now
retrievable into future briefs. That is a NEW retrievable-content class landing INSIDE
the C25 accrual window — a potential return channel distinct from the C7 handle-offer
mechanism P1 measures. Expected magnitude today is ~zero (zero `steer_message` signals
exist in `cir.db` at boundary time).

## What was added

1. **Machine-readable marker** — `instruments/protocol-v22-cointervention-marker.json`
   (same shape as `c25-intervention-marker.json`): conjecture `c25`, `cointervention_at`
   = 2026-07-06T14:54:43Z (the `949a018` commit time in UTC), `trigger_type`
   `steer_message_embeddable_v22`.
2. **Reporting-only analyzer amendment** — `analyses/c25-return-intervention/analyze.py`
   gains `_steer_derived_offer_stats()` and one report line: among post-intervention
   **offered** runs, how many were offered ≥1 signal of kind `steer_message`
   (`steer-derived offers: k/n`), plus a `v22_cointervention` block in the `--json`
   output. Steer-derived offers are reported **separately, never pooled** into P1/P2.

## Diagnosis outcome: DISTINGUISHABLE

The offer row (`training/cir-run-outcomes.jsonl`) exposes `injected_signal_ids` (a list
of signal ids) but no kind field. The ids join read-only against `cir.db`'s
`signals.kind` (verified: a probe of live injected ids resolved to kinds `step_result`,
`correction.perceive`; `idx_signals_kind` makes the join cheap; `steer_message` count =
0 today). Because the kind is recoverable via a read-only join, steer-derived offers are
**distinguishable** — so this is a code amendment, not escalation (b). The join runs
`mode=ro` on `cir.db` (observer-effect rule honoured: no `mentu` CLI, no MCP CIR path).

## Why reporting-only, and byte-equivalence

The block is computed ONLY on the gate-open path (`_steer_derived_offer_stats` is called
after adjudication inputs are fixed; the `v22_cointervention` key is added only to the
gate-open return; the render line is emitted only in the gate-open branch, after the
GATE-NOT-OPEN early return). It feeds **no** verdict input. Proven mechanically: the
pre-edit analyzer (git HEAD) and the amended analyzer produce **byte-identical**
GATE-NOT-OPEN output (both `--json` and markdown) against a frozen input, run-timestamp
normalized; `git diff` shows +77 insertions, 0 deletions. If `cir.db` is unavailable the
block degrades to `null` / `n/a` and never raises. New unit tests assert: the dormant
result gains no key; the count is correct via the read-only join; and the verdict + P1/P2
inputs are identical with and without a `steer_message` population present.

**Predictions, falsification, thresholds, and the gate untouched.** The frozen baseline
(organic offer 0.0222%), the ≥150-per-arm gate, the ≥10× order-of-magnitude test, alpha,
and the falsification rule are unchanged. This wiring changes no prediction, statistic,
or gate constant — only what is reported when the gate opens.
