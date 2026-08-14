---
id: c24
name: failure-driven-retirement
status: operationalized
lineage:
  - observatory/packets/2026-06-18.md   # attention-allocation candidate crystallized (beat #7)
  - observatory/packets/2026-06-19.md   # appearance 2/3
  - observatory/packets/2026-06-20.md   # appearance 3/3 → operationalized (canon guard 4)
  - corpus/refuted/c1-return-as-intelligence.md   # orchestration-layer counter-case to return
verdict: null
result: null
detector_born: 2026-06-20
tracking:                      # machine-updated by observatory beats only
  last_beat: 2026-07-13
  beats: 12
  cohort: "non-fixture zombie cohort (>=30 consecutive failures, 0 successes). Current: ane-fortress (386 runs / 0 success / max streak 386 / 0 version changes / 2026-05-17 -> 2026-06-28T16:51:26Z). 07-13 (beat #20; observatory dark 07-01..07-12): FIFTEEN days silent — but the wind-down/retirement read is now CONFOUNDED by the executor-health incident: the watchdog's last_evaluation froze at 06-26T14:37:59Z (still frozen today), the daily beat went dark from 07-01, and the CIR grind stalled scheduled lanes until the 07-08 purge (instruments/2026-07-08-cir-exhaust-purge-regime-note.md). Other lanes kept producing runs (76 completions 07-01..13), so the executor was not fully dead — but silence spanning the incident window carries NO C24 signal either way (attention reallocation vs scheduler stall not separable read-only) — HELD OPEN. DISCRIMINATING DATUM (post-recovery): if ane resumes after the daemons restart on the fixed binary -> the silence was stall, not retirement; sustained absence under a confirmed-healthy scheduler (watchdog re-evaluating) -> genuine retirement candidate. P1's >=150-consecutive-failure threshold stays CROSSED at 386/0/None (qualitative only). POST-PACKET FOLLOW-UP (07-13 ~14:00 local, read-only registry check): the discriminating datum has STARTED ACCRUING — both daemons restarted TODAY on current code (temporal 09:20 on engine f0ad9e9, per its own startup version print; mentud 12:48 with all subsystems incl. fortress initialized), the temporal daemon is healthily evaluating 28 schedules, and ane-fortress STILL did not run. Registry facts: ~/.mentu/recipes/ane-fortress.json has schedule:null and NO ~/.mentu/temporal-state/ entry exists — ane was never temporal-scheduled; its driver was mentud's fortress lane (launchd ai.mentu.fortress + mentud fortress subsystem). So the silence under a confirmed-healthy scheduler is now ONE day long; scheduler-stall is losing ground as the explanation, but one healthy day is not yet a retirement declaration — keep observing. Cadence history 06-23..30 = 32,47,21,5,5,2,0,0 (P2 whipsaw illustration stands). Note: ane-fortress was brief-injected (ssc 7) yet 100%-failed — per-run knowledge return does nothing for an unfixable recipe (bonus illustration, not a readout). Contrast (retired-fast) cohort unchanged: E3-expr-version (7 fails, last 06-08), subcanvas-notion-parity-canvas-e2e (5, last 05-18), observer-bridge (4, last 06-09)."
  cointervention: "2026-07-14 CROSS-DRIVER FAILURE TRIPWIRE pre-registered (instruments/2026-07-14-run-horizon-intervention-preregistration.md + marker). DIAGNOSE-FIRST finding that reshapes C24's reading: the TEMPORAL lane ALREADY reallocates attention (TemporalRunner circuit breaker, threshold 3 consecutive failures -> skip+notify+TTL recovery) — so C24's 'orchestration ignores failure history' is FALSE for temporal-scheduled recipes. ane-fortress reached 386 only because it ran on a NON-temporal lane (schedule:null, no temporal-state) that lacks the breaker. The intervention adds a detection-only tripwire at the universal outcome seam (CIRRunOutcomeRecorder) emitting anomaly_detected on >=10 consecutive failures / 0 successes, any driver. Regime boundary: pre-intervention baseline (ane-fortress 386/0, manual detection) frozen; post-marker zombie DETECTION is mechanized — never pool pre/post detection-latency. Frozen predictions/verdict untouched. Detection only; enforcement of external drivers is outside engine control."
  gate: "23/90 detector-days (born 2026-06-20); accelerator: 1/3 distinct non-fixture recipes at >=30 consecutive failures (ane-fortress only). Gate opens at 90 detector-days OR >=3 such recipes. NOTE: P1's numeric threshold (>=150 failures) is crossed (386) but does NOT itself open the gate. NOTE 2 (2026-07-14): C24's mechanism is now known to be PARTIALLY PRESENT already (temporal circuit breaker) — the open question narrows to non-temporal lanes, which the tripwire above addresses by detection."
  watch: [observatory/packets/2026-06-28.md, observatory/packets/2026-06-29.md, observatory/packets/2026-06-30.md, observatory/packets/2026-07-13.md]
---

# C24 — Failure-driven retirement (does orchestration reallocate attention away from persistently-failing recipes?)

## Claim

Mentu's recipe orchestration does not incorporate accrued failure history into
scheduling. A recipe that fails persistently — a long unbroken consecutive-failure
streak with zero successes — continues to be scheduled at undiminished cadence and is
never automatically retired or version-corrected. Failure-driven attention
reallocation is **absent** for scheduled (non-interactive) runs: the system does not
"return" its own failure ledger into the decision of what to run next.

## Why this exists

This is the orchestration-layer counter-case to return-as-intelligence (C1/C1b). C1
asked whether stored knowledge is returned *into agent runs*; C24 asks whether the
system returns *its own outcome history* into *scheduling*. It crystallized from the
observatory's zombie watch: `ane-fortress` has run **257 times with 0 successes**
(every run failed; max consecutive-failure streak = 257) from 2026-05-17 through
2026-06-19, with **zero recipe_version changes** and undiminished cadence — never
retired, never repaired, continually rescheduled. The attention-allocation candidate
appeared in three consecutive packets (beats #7–#9, 2026-06-18/19/20); per canon
guard 4 it is operationalized here rather than left in limbo. The constitution's bar
for entry — a conceivable measurement procedure — is met (read-only analysis of the
outcome ledger), so this is operationalized, not excluded.

## Operationalization

**Dataset**: `~/.mentu/training/cir-run-outcomes.jsonl` (read-only; observer-effect
rule). Fields used: `recipe`, `completed_at`, `success`, `recipe_version`,
`run_class`.

**Population**: all **non-fixture, non-smoke** recipes — i.e., exclude deliberate-
failure fixtures where "retirement" is meaningless (`run_class` in {fixture, smoke},
or name matching `-bad` / `-false` / `smoke` / `-test` / `e2e` / `-probe`). The
population **deliberately includes infra/cron-scheduled recipes** (e.g.
`ane-fortress`): the scheduled class is exactly where decoupling is hypothesized.
Note this is the inverse of C1b's infra exclusion — infra pollutes a success-rate
A/B, but it is the *primary subject* of an attention-allocation claim.

**Per-recipe measures** (chronological by `completed_at`): total runs, total
successes, max consecutive-failure streak, distinct `recipe_version` values, daily
cadence (runs/day) across the streak, last-run date. A recipe is **retired** if it
records no run for ≥14 days.

**Zombie** = non-fixture recipe with consecutive-failure streak ≥30 and 0 successes.

## Predictions (frozen now, before any analysis)

- **P1 (unbounded persistence)**: ≥1 non-fixture recipe reaches ≥150 consecutive
  failures with 0 successes and 0 `recipe_version` changes while still scheduled —
  the orchestration layer does not bound failure accrual.
- **P2 (cadence decoupling)**: For the zombie cohort, scheduling cadence in the
  deep-failure phase (streak >30) is **not lower** than in the early phase (first 10
  failures); there is no negative correlation between cumulative failures and
  subsequent daily run count. Failures do not throttle scheduling.
- **P3 (no in-streak repair)**: Zero `recipe_version` changes and zero successes
  occur *within* a zombie streak before its eventual termination — the system
  abandons (stops scheduling) rather than repairs in place; it never modifies a
  persistently-failing recipe.

## Falsification

If non-fixture failing recipes are systematically throttled or repaired as failures
accrue — cadence declines monotonically with accrued failures across the cohort, OR
`recipe_version` changes appear mid-streak, OR the longest non-fixture failure streak
stays bounded well below 150 because retirement is prompt — then **refuted**:
orchestration *does* exhibit failure-driven attention reallocation, and
`ane-fortress` is an isolated scheduling bug rather than a structural blind spot.

## Analysis gate

Do not analyze before **90 detector-days** (detector born 2026-06-20), OR until
**≥3 distinct non-fixture recipes** have crossed the ≥30-consecutive-failure
threshold (whichever first). At the gate a frozen `analyses/c24-failure-driven-retirement/analyze.py`
adjudicates P1–P3 mechanically against the pre-registered thresholds above. The
retired-fast contrast cohort (recipes that stopped after a handful of failures)
serves as the comparison even if the zombie cohort remains n=1.

## Honest caveats (recorded at operationalization, not adjudication)

- The zombie cohort is currently **n=1** (`ane-fortress`); most failing non-fixture
  recipes in the historical ledger retired quickly (E3-expr-version after 7 fails,
  subcanvas after 5, observer-bridge after 4). The population-level direction is
  therefore **open** — the data may show ane-fortress is the rule (decoupled
  scheduled class) or the exception (an isolated bug). P2/P3 discriminate which.
- `ane-fortress` carries no `recipe_version` field (vers=None throughout), so P3's
  in-place-repair test is partly degenerate for this subject; it is adjudicated as
  "no repair observed," with the contrast cohort carrying the discriminating weight.
- No verdict or readout is permitted before the gate (constitution rule 5).
