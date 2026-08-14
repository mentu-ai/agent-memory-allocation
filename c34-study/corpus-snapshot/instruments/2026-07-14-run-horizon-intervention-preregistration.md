# 2026-07-14 — Run Horizon cross-driver failure tripwire (C24 co-intervention pre-registration)

*Pre-registration in the C25 lineage: declares a substrate-level intervention that changes a quantity
an open conjecture (C24) measures, with predictions and falsification criteria frozen BEFORE the code
merges. Touches no frozen prediction, verdict, or result of any conjecture. Governing build doc:
`mentu-complete/docs/BUILD-run-horizon-v1.md` (+ its `CONTEXT-run-horizon.md`).*

## Why this exists

C24 (failure-driven retirement) asks whether Mentu's orchestration incorporates accrued failure
history into attention allocation. The founding case is `ane-fortress`: **386 consecutive failures,
0 successes**, never slowed or retired (detector born 2026-06-20).

DIAGNOSE-FIRST (2026-07-14, read-only) established three things:
1. The **temporal** lane already reallocates attention: `TemporalRunner` has a circuit breaker on
   `consecutiveFailures` (default threshold 3 — skip + notify + TTL auto-recovery).
2. `ane-fortress` evaded it because it ran on a **non-temporal lane** (recipe `schedule:null`, no
   temporal-state entry; external/now-defunct driver, silent since 2026-06-28).
3. The single universal seam every run passes through — `CIRRunOutcomeRecorder.record` — has **no
   cross-run failure tracking**. That is the gap.

## The intervention (detection-only)

At the universal outcome seam, track consecutive failures per recipe across all drivers. On
crossing the threshold, emit ONE `anomaly_detected` CIR signal (deterministic id, re-armed after a
success). **Detection-only**: the engine cannot unschedule an external driver, so this surfaces the
pathology (to the human and to the epistemics observatory) rather than enforcing a stop. Enforcement
in lanes the engine controls (temporal) already exists.

## Frozen parameters (before any code merges)

- **Threshold**: **10** consecutive failures with **0** interleaved successes for a given recipe.
  Rationale: above normal dev-iteration noise (3–5 failures is common and already covered by the
  temporal breaker's threshold 3), below C24's ≥30-failure zombie-cohort line — an early tripwire
  that catches a zombie *in formation*.
- **Idempotence**: at most one anomaly per recipe per failure-streak; the emit-flag resets on the
  next success. A streak that keeps growing past 10 does not re-emit.
- **Signal**: `kind=anomaly_detected` (already first-class per `CIRIngestPolicy`), id
  `run-horizon-streak-<recipe>-<streak_start_run_id>`, body naming the recipe, streak length, and
  last run id.

## Frozen predictions

- **P1 (coverage)**: every recipe that reaches 10 consecutive failures / 0 successes after the marker
  emits exactly one anomaly within one run of crossing the threshold.
- **P2 (specificity)**: no anomaly is emitted for any recipe whose last 10 runs contain ≥1 success
  (reset-on-success correctness).
- **P3 (C24 detection latency)**: post-marker, time-to-detection of a zombie drops from "a human
  notices in the daily beat" to "≤1 run after the 10th consecutive failure" — mechanized attention
  reallocation for the previously-unprotected lanes. (This is the C24-facing effect; enforcement of
  external drivers remains impossible, stated honestly.)
- **P4 (non-harm / C1b)**: the anomaly is not a context/footer/brief kind, so it never enters brief
  composition; C1b's offer and use-when-offered channels are unaffected. Steering/abort are NOT part
  of this intervention (deferred with the risk model — see below), so no run control-flow changes.

## Falsification

- P1 fails (a genuine ≥10/0 streak produces no anomaly) → the tripwire is broken.
- P2 fails (an anomaly fires for a recipe with a recent success) → the reset logic is broken; the
  mechanism is unsound and must be reverted.

## Deferred (recorded, not shipped)

The **model-dependent per-run steer/abort** (BUILD doc M2.1) is deferred: M0's horizon model does not
clear the frozen temporal gate on a non-monoculture population (the pass is carried by the
`ane-fortress` monoculture; de-confounded leave-family-out CV shows ROC 0.80–0.86 at k=3–5 — real but
not yet gate-passing on the required split). It waits for a clean prospective set, which accrues
automatically in `cir.db`. See `CONTEXT-run-horizon.md`.

## Regime boundary

`instruments/2026-07-14-run-horizon-intervention-marker.json`. C24's pre-intervention baseline
(`ane-fortress` 386/0, manual detection) is frozen; post-marker, zombie **detection** is mechanized —
never pool pre/post detection-latency in any C24 re-read. C24's frozen predictions/verdict are
untouched; only its `tracking:` block is annotated (as for C25).

## Addendum (2026-07-14, before code ship) — population clarification

The tripwire watches **feature and infra run classes only**. Deliberately-failing fixtures
(`fixture`/`smoke` classes — e.g. `t1-*-bad`, `pricing-buggy`, `*-false`) are excluded: their
failure is by design, not pathology, so a long failure streak there is expected and must not emit an
anomaly. This sharpens P2 (specificity) by defining the population precisely; it does not weaken any
prediction. `ane-fortress` classifies as `infra` and remains in scope. Run class is
`CIRRunOutcomeRecorder.classify(recipe:explicit:)`.
