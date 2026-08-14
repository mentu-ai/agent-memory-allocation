# Instrument note — C1b run-class exclusion: every arm to date is a smoke test

**Date**: 2026-06-12 (same day as packet 2026-06-12, beat #2; written at commit
time, before the beat's commit).
**Follows**: `instruments/2026-06-11-c1b-eligibility-accounting.md` (F1, F2);
`observatory/packets/2026-06-12.md` interpretation items 1–2.
**Method**: read-only direct file inspection of
`~/.mentu/training/cir-run-outcomes.jsonl` (observer-effect rule; no `mentu`
CLI/MCP paths touched), plus inspection of the uncommitted working-tree diff
to `observatory/collect.py` found at commit time.

## Summary

At commit time the beat found an uncommitted maintainer revision to
`observatory/collect.py` whose comment cites an "instrument note 2026-06-12"
that did not yet exist; this is that note. The revision excludes
fixture/smoke/infra run classes from C1b arm and eligibility gauges and adds a
start-time regime guard. Raw verification confirms its premise and sharpens
it: **every arm ever recorded — four by 20:12Z today — is a smoke-class engine
test. Organic arms accrued: zero.** Today's digest headline ("first injected
arm") was an engine plumbing exercise, not organic work. The note also
corrects a timing error in yesterday's F1.

## Findings

### F1 — All four arms are smoke-class

All rows in `cir-run-outcomes.jsonl` with `randomization_arm` set, as of
2026-06-12 ~20:15Z (447 rows total):

| run | time (UTC, completed) | recipe | arm | success | use_rate | cir_verdict | class |
|---|---|---|---|---|---|---|---|
| `run_rce2e_1781131206` | 06-10 22:40:37 | rce2e | withheld | no | 0 | withheld | smoke (heuristic: "e2e") |
| `run_contract-smoke-warn_1781257284` | 06-12 09:42:01 | contract-smoke-warn | injected | yes | 0 | ignored | smoke (explicit) |
| `run_contract-smoke-enforce_1781257335` | 06-12 09:42:53 | contract-smoke-enforce | withheld | no | 0 | withheld | smoke (explicit) |
| `run_flagprobe-smoke_1781295099` | 06-12 20:12:10 | flagprobe-smoke | withheld | yes | 0 | withheld | smoke (explicit) |

Notes:

- The collector comment says "2 of the first 3 arms" — that counts only
  explicit `run_class` fields. Under the revision's own name heuristic the
  `rce2e` arm is smoke-class too, and so is the fourth arm: **4 of 4**.
- The engine began writing an explicit `run_class` field on outcome rows
  today (3 rows ≥ 2026-06-12 carry `run_class: smoke`; all earlier rows null)
  — an engine-side instrument change observed, not made, by this beat.
- The fourth arm (`flagprobe-smoke`, withheld, success) completed 71 s after
  the digest's 20:10:58Z collection, so today's digest counted 3 arms.
- The day's "first injected arm" (`contract-smoke-warn`): success with
  `use_rate` 0 and `cir_verdict: ignored`. As a smoke exercise it cannot
  speak to P2 (organic citation) either way; packet item 1's watch remains,
  but with no organic injected run yet in existence, its subject is empty.

### F2 — Timing correction to yesterday's F1

Yesterday's note stated `cua-parity-w3` "started 9 minutes after the 12:19Z
regime boundary." Raw record: `started_at` 2026-06-10T11:38:21Z — **41
minutes before the boundary** — `completed_at` 12:28:08Z. The earlier note
conflated completion with start. The collector revision's start-time guard
(`started_at >= REGIME_BOUNDARY` for the eligibility pool) is therefore the
mechanically correct exclusion for this run, and the "permanent overcount by
one" reading of the legacy gauge stands for a different reason than F1 gave:
the run started pre-boundary on the pre-deployment binary.

### F3 — Expected gauge discontinuity at the next digest

Under the revised collector, tomorrow's digest will read approximately:

- arms: injected 0, withheld 0 (today: 1 and 2) — a **reclassification, not
  data loss**; the four smoke arms remain in the JSONL.
- eligibility: 0/2-ish post-regime *feature-class* runs (the only
  feature-class post-boundary runs to date, `mt-computer-use-panel` and
  `assimilate-vscode`, both had empty briefs). The denominator drops from 28
  because ane-fortress(9), rcsleep*(10), e2e/smoke recipes, and the
  pre-boundary-start run are excluded.

The experiment's true state, on the revised gauge: **zero eligible organic
runs and zero organic arms in 2.5 days of operation.** Eligibility was already
the experiment's clock (packets #0–#2); it is now unambiguously so.

### F4 — Open constitutional tension: gate countability of smoke arms

The conjecture's frozen analysis gate reads "only runs with
`randomization_arm` set count." The collector revision narrows the *gauge* to
feature-class runs. These now disagree: raw 4/300 vs organic 0/300. Posture:

- The revision changes gate *timing* signals only; the frozen analysis and
  its pre-registered per-recipe Mantel–Haenszel stratification are untouched
  (smoke recipes form their own strata and are isolatable at readout —
  yesterday's F2 caveat 2 anticipated exactly this).
- Whether smoke-class arms count toward the 150/arm gate and the pooled
  effect must be settled by a dated maintainer amendment **before** the gate
  opens — not decided at analysis time, and not by a beat. Until then, beat
  tracking carries both gauges side by side.

### F5 — Provenance

The collect.py revision was found uncommitted in the working tree at this
beat's commit step (repo was clean at beat start per the dispatch snapshot;
authorship outside beat observation). It compiles (`py_compile` clean). Per
the beat's standing commit instruction it is committed alongside this note,
which resolves the dangling "instrument note 2026-06-12" reference in its
comments. Writing collector code remains outside beat powers; this beat wrote
none.
