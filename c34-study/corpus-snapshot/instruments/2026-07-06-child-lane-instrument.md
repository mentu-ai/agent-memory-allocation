# 2026-07-06 — Child-agent call lane: a structural brief-consumption channel (C1b)

*Instrument note (same class as `2026-06-15-c1b-footer-measurement-fix.md` and
`2026-07-06-protocol-v22-regime-boundary-and-impact.md`). Declares a new
measurement channel landing on an OPEN conjecture before it carries load.
Touches no frozen prediction, verdict, or result.*

## What changed upstream

Protocol v2.2 wiring milestone **W1** (mentu-complete, engine commit shipping
today) adds the **child-agent call lane**. A sequence step runs its agent as a
CLI child process, so until now the engine's call lane (M3) recorded only the
engine's own in-process leaf calls (semantic gate, completion verifier) — the
child's calls, and its consumption of the injected CIR brief, were invisible
(the M3 "coverage boundary"). W1 closes this by a boundary-compatible route:

- At **step exit**, the engine harvests the child's Claude Code session
  transcript (`~/.claude/projects/<sanitized-cwd>/<uuid>.jsonl`) into
  `model_call` records tagged lane `child_transcript` (reconstructions, not wire
  captures — `mentu runs replay` prints the in-process / child split).
- It emits **one `context_consumed` signal per step** recording, of the CIR-brief
  signal ids offered into that step (`PreparedBrief.injectedSignalIds`, already
  recorded at injection): `in_context` = how many appear in the child's request
  context (the offer actually reached the model), `echoed` = how many the child
  reproduced in its output (evidence of active use).
- **No network interception.** Backends without an accessible transcript
  (codex, gemini, shell) stay out of lane. Linkage is **correct-or-abstain**:
  a transcript is harvested only when exactly one links to the step by
  modification window; on zero or multiple matches the step is skipped, so a
  concurrent or parent session is never mis-attributed.

## Why this matters for C1b (the instrument gain)

C1b Stage-2 ("use-when-offered") has been blocked on a MEASUREMENT problem: use
is observable only through a model-emitted footer, whose median missing-footer
rate is 1.00 in the injected arm — for at least half the arm the channel is
silent (see `2026-06-15-c1b-footer-measurement-fix.md`). `context_consumed` is a
**structural** channel for the same quantity: it reads the transcript the model
actually produced, not a footer the model had to remember to emit. It does not
depend on model cooperation.

This is the substrate half of the H8 `context_offered` / `context_consumed`
edge pair, and the first channel that measures brief consumption at the wire
(transcript) level rather than by self-report.

## Obligations (per the corpus constitution)

1. **Do NOT retire the footer.** Run both channels and compare. The footer is
   the pre-registered C1b instrument; `context_consumed` is a new, independent
   estimator of the same construct. Divergence between them is itself data
   (it quantifies the footer's silence bias). Retiring the footer now would
   break continuity across the regime boundary.
2. **Never pool the two silently.** A future C1b readout that mixes
   footer-derived and transcript-derived use rates must declare which rows came
   from which channel — the same discipline as the C1b run-class and
   footer-fix boundaries.
3. **Regime boundary.** `context_consumed` signals begin at the W1 engine
   deploy (2026-07-06; marker `child-lane-cointervention-marker.json`). No
   `context_consumed` row predates it; do not backfill.
4. **Coverage is partial and honest.** Only Claude-Code-backed steps with an
   unambiguously-linkable transcript are covered. The denominator for any
   transcript-derived use rate is those steps, NOT all injected runs — state it
   explicitly at readout.

## What this does NOT change

Frozen C1b predictions, falsification criteria, verdict, and the footer-based
analysis are untouched. C25's offer/handle-return mechanism is unchanged; this
note declares the co-intervention for completeness (marker filed) but W1 adds a
measurement channel, not an intervention on the offer path. No `results/`,
`corpus/supported/`, or `corpus/refuted/` file is touched.
