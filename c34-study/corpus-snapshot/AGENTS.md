# epistemics — agent entry protocol

This is the empirical theory layer for Mentu. Read `README.md` (the
constitution) before any work. If you are here for the daily observatory beat,
read `observatory/CANON-observation-packet-v0.1.md` and follow it exactly.

## Hard rules (constitutional — no exceptions)

1. Claims enter as conjectures; they graduate only via a measurement procedure
   plus a result from real Mentu data. Predictions are frozen before analysis.
2. **Never edit**: frozen frontmatter fields (claim, predictions, falsification
   criteria, `verdict`, `result`), anything in `results/`, `corpus/supported/`,
   or `corpus/refuted/`. Corrections go in new dated documents.
3. Beats may: append observation packets, update `tracking:` frontmatter
   blocks, refresh the README status board, and commit.
4. **Observer-effect rule**: read Mentu data via raw read-only SQLite
   (`sqlite3 -readonly` / Python `mode=ro`) and direct file reads only. Never
   query through `mentu` CLI or MCP CIR paths — that writes access telemetry
   into the quantities this corpus measures.
5. Verdicts come only from gate-triggered frozen analyses
   (`analyses/*/analyze.py`), adjudicated mechanically against pre-registered
   criteria. Interpretation never changes a verdict.
6. Report negative and ambiguous findings as-is. The verdict is whatever comes
   out — that is the point of this repository.

## Daily beat (for the scheduled agent)

1. The dispatcher has already run `observatory/collect.py` — its digest is in
   your prompt. If not, run it yourself (read-only).
2. Write `observatory/packets/<today>.md`: digest verbatim, then
   Interpretation, Classifications (`note` / `conjecture-candidate` /
   `gate-event`), Tracking updates, and a one-line Status.
3. Update `tracking:` blocks on affected conjectures (C1b at minimum).
4. Sundays: add `## Weekly synthesis` — gate checks, README board refresh,
   and metabolize ONE un-salvaged 2025 idea per the canon.
5. If a gate opened (`gate-event`): run that conjecture's frozen analysis,
   write the dated results doc, adjudicate mechanically, move files per the
   constitution.
6. Commit with a descriptive message ending in the Codex trailer. Do not push.

## Layout

See `README.md`. Instrument provenance: `instruments/mentu-instrument.md`
(note the 2026-06-10 regime boundary — never pool pre/post data).
