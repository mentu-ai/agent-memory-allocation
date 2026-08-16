# BUILD — Run Horizon v1: behavioral failure prediction + early-abort/retirement policy

**Status**: ready for execution · **Prepared**: 2026-07-14 · **Owner**: Rashid Azarang
**Executor**: one engineering agent on `mentu-complete`, milestones in order, M0 → M1 → M2 (M3 deferred).
**Scientific companion**: the epistemics corpus (`~/Desktop/epistemics`) — this build is *coupled* to open
conjectures C24 (failure-driven retirement) and C1b (consumption channel); the coupling rules below are
constitutional, not advisory.

## Purpose

Silva, Tu & Monperrus (arXiv:2607.05188, 2026-07-06) show that a coding agent's internal state linearly
encodes properties of the evolving program and predicts them ~25 agent-steps ahead (probes, AUC ≤ 0.84,
transfer across benchmarks with ≤ 0.09 drop). Mentu cannot probe residual streams on its API-model lanes,
but it records the *behavioral* analogue per run — and it has the motivating pathology the paper lacks:
`ane-fortress` ran **386 consecutive failures with zero successes** and was never slowed, aborted, or
retired (epistemics C24, detector born 2026-06-20). This build creates:

1. **Run Horizon** — a per-step behavioral risk score with a measured prediction horizon (the black-box
   analogue of the paper's latent horizon), trained on the existing outcome ledger.
2. **The policy C24 documented as missing** — steering checkpoints for feature runs, early abort for
   infra/scheduled runs, and consecutive-failure cool-down/retirement for temporal schedules.

## Grounding (verified 2026-07-13/14, read-only)

- **Outcome ledger**: `~/.mentu/training/cir-run-outcomes.jsonl` — 1,065+ runs, per-run aggregates incl.
  `run_id`, `recipe`, `run_class`, `started_at/completed_at`, `success`, `outcome`, `steps_ok/warn/total`,
  `duration_ms`, `injected_count`, `read_count`, `use_rate`, `missing_footer_rate`, `brief_bytes`,
  `run_health_label`, `training_label`. Written by `CIRRunOutcomeRecorder.swift` (`steps_ok` at key 65,
  `record(...)` at ~180).
- **Per-step trail (retrospective)**: `cir.db` `signals` rows carry `run_id`, `commitment_id`, `op`
  (`commit/claim/close/submit/annotate`), `ts` — per-step commitments ("Step: …") give step start/close
  timestamps and stall gaps (verified on live runs). Plus `cir-read-usage.jsonl` (step-brief read
  telemetry) and per-workspace `.mentu/ledger.jsonl`.
- **Step execution seam**: `SequenceRunner.swift` (`SequenceStep` at ~114; already computes step results
  and emits read telemetry ~4131; `steer_message` channel exists — protocol v2.2, embeddable since
  2026-07-06).
- **Temporal seam**: `TemporalRunner.swift` + `~/.mentu/temporal-state/<name>.json` which ALREADY carries
  `consecutive_failures`, `history`, `run_count`, `last_run`, `next_run` — the retirement rule needs no
  new counter, only a policy over the existing one.
- **Training lane**: `Scripts/` + `requirements-training.txt` (numpy available); mentud has an MLX
  classifier lane (autoresearch sentinel-classifier) — NOT a dependency of this build.
- **Regime boundaries that constrain training data**: 2026-06-10 (randomization feature),
  2026-06-15T02:57Z (footer fix), 2026-07-08 (CIR exhaust purge — retrieval-pool change). Never pool
  naively across them; include regime flags or restrict windows.

## Executor constitution (hard rules)

1. Work on `main` of `mentu-complete`. Conventional commits. **Never** `Co-Authored-By`, never amend,
   never force-push. Stage only your own files by explicit path (unrelated WIP may be present).
2. **DIAGNOSE-FIRST**: every milestone opens by verifying its assumptions against the live substrate
   (read-only) and logging findings in `docs/context/CONTEXT-run-horizon.md` (force-add; `docs/` is
   gitignored). Deviations from this doc are allowed only toward safety and must be logged there.
3. Tests use a temp `MENTU_HOME` only; never touch the live home from tests. Snapshot live DBs with
   `VACUUM INTO`, never `cp`.
4. Training/analysis reads live data **read-only** (`sqlite3 -readonly` / Python `mode=ro`; append-only
   files by direct read). Never read through the `mentu` CLI (observer effect — same discipline as
   epistemics).
5. Runtime scoring is pure Swift (dot product over a JSON model artifact); no new runtime dependencies,
   no network, no Python at run time. Training is offline Python (numpy ok), deterministic seed.
6. All ledger/schema changes are **additive** — `observatory/collect.py` (epistemics) and existing
   consumers must parse old and new records unchanged.
7. **Epistemics coupling order (constitutional)**: M1's new fields need a dated *minor instrument note*
   in `epistemics/instruments/` (additive telemetry, no behavior change). M2 is a **declared
   intervention**: the pre-registration + marker (spec in M2.0) must be committed in the epistemics repo
   **before** any behavior-changing code merges in this repo. Commit timestamps are the proof.
8. Steering/abort messages contain **no CIR content** and never mention injected briefs (C1b protection).
9. Milestone gates are frozen below; failing a gate routes to its registered fallback — gates are never
   lowered after seeing data.
10. Kill-switch from day one: config flag `run_horizon.enabled` (default: M1 `shadow`, M2 `enforce` only
    after pre-registration) + env override `MENTU_RUN_HORIZON=off`.

---

## M0 — Retrospective horizon curve (read-only; ~1 session)

**Question**: how far ahead, and how well, does early behavioral telemetry predict final `success`?

- **M0.1 DIAGNOSE-FIRST — reconstructability census.** For every ledger run: can a per-step prefix be
  rebuilt from `cir.db` lifecycle signals (+ `cir-read-usage.jsonl`)? Report coverage (% runs with ≥ 3
  reconstructable steps) by run class, recipe family, and month. Also report label base rates
  (`success` ≈ 83% overall — class imbalance is real).
- **M0.2 Freeze the feature spec v1 *before* joining features to labels** (minimize analyst dof). Per
  prefix of k steps, behavioral features only — NO recipe identity: log step durations + inter-step
  gaps; warn ratio if derivable; CIR read/use event counts + timing; footer emissions; brief size;
  run class one-hot; steps-elapsed/steps-planned if available; regime flags (pre/post 2026-06-15 and
  2026-07-08). Spec goes in CONTEXT doc + `Scripts/run-horizon/features.md` in the same commit as the
  census, before training.
- **M0.3 Train + curve.** Logistic regression (numpy, seeded), standardized features. Splits: **temporal**
  (train < 2026-06-25 ≤ eval) with a family-overlap report; secondary family-disjoint split as
  robustness. Sweep prefix k = 1..15 and horizon h (predict end-of-run success from step ≤ k, i.e.
  h = steps_total − k). Report ROC-AUC **and** PR-AUC per (k), calibration plot, and the **horizon
  curve** (AUC vs. how many steps before the end the prediction is made) — the Mentu analogue of the
  paper's Figure.
- **M0.4 Deliverables.** `Scripts/run-horizon/{census.py,train.py,features.md}`; model artifact
  `~/.mentu/models/runhorizon-v0.json` (schema: `{version, trained_at, features:[...], means, stds,
  coefficients, intercept, eval:{auc_by_k, pr_auc_by_k, split}}`); results in the CONTEXT doc.

**Gate M0 (frozen)**: temporal-split eval ROC-AUC ≥ 0.70 at some k ≤ 5 with median horizon ≥ 3 steps,
and coverage ≥ 60% of post-2026-06-15 feature+infra runs.
**Registered fallback**: if coverage < 60% → M0 delivers the census + feature/logging spec only, and the
plan becomes **M1-first**: ship native per-step logging, accrue ≥ 300 prospective runs (~3–4 weeks at
current ~10/day), then train against the same gate. If coverage passes but AUC < 0.60 → stop after M1
(shadow telemetry is still worth having); M2 does NOT proceed on a sub-0.60 model — its per-recipe
retirement rule (which needs no model) may ship alone under M2's process.

## M1 — Live shadow scoring (observe-only; ~1 session)

- **M1.1** `RunHorizonScorer.swift`: loads newest `~/.mentu/models/runhorizon-v*.json`; per step boundary
  in `SequenceRunner`, computes the score from natively-collected features (must equal the frozen spec —
  feature parity test against `Scripts/run-horizon` on a fixture). Missing model ⇒ clean no-op.
- **M1.2** Ledger additions (additive): `risk_trajectory: [Double]`, `risk_model_version: String` in the
  outcome record; plus append-only `~/.mentu/training/run-horizon-steps.jsonl` (one line per step:
  run_id, step_idx, features, score) for retraining. Nothing is written into CIR signals; runs cannot
  read their own scores.
- **M1.3** Tests (temp home): scorer determinism; no-model no-op; overhead micro-bench; old-ledger
  parse-compat; epistemics `collect.py` smoke against a fixture ledger containing new fields.
- **M1.4** Epistemics: dated **minor instrument note** (`instruments/<date>-run-horizon-shadow-telemetry.md`)
  declaring the additive fields; no conjecture tracking changes required.

**Gate M1 (frozen)**: p50 scoring overhead < 5 ms/step and p99 < 25 ms; `risk_trajectory` present on 100%
of scored runs over a 3-day soak; **zero behavior deltas** (no branch of run control flow reads the score).

## M2 — Policy: steer / abort / retire (the C24 intervention; 1–2 sessions)

- **M2.0 Pre-registration FIRST (epistemics repo, before any code merge here).** Write and commit:
  - `instruments/<date>-run-horizon-intervention-preregistration.md` — frozen thresholds (θ_high, m,
    cool-down/retire counts — chosen from M0/M1 curves and stated with their derivation), frozen
    predictions (at minimum: (P1) maximum consecutive-failure streak for any scheduled recipe is capped
    at the retire threshold — the 386-style streak becomes impossible; (P2) wasted scheduled-run minutes
    per week fall ≥ 50% relative to the 2026-05-17→07-13 baseline; (P3) false-abort rate < 5%, measured
    by `revive`/override within 7 days; (P4) feature-run success rate does NOT decrease — steering must
    be non-harmful), falsification criteria, and the analysis window.
  - `instruments/<date>-run-horizon-intervention-marker.json` — machine marker with ship commit + UTC
    timestamp. **This date is a regime boundary**: C24's tracking is updated to record that its claim is
    now scoped *pre-intervention* and its re-read becomes a before/after natural experiment (mirror of
    the C25 pattern). C24's frozen predictions/verdict fields are NOT edited.
- **M2.1 Per-run policy** (SequenceRunner):
  - *Feature-class runs*: score > θ_high for m consecutive steps → **steering checkpoint** via the
    existing `steer_message` channel: a short, CIR-free note ("risk elevated at step N: recent steps
    slow/failing; consider narrowing scope or stopping") — never an abort.
  - *Infra/fixture/smoke and temporal-scheduled runs*: same trigger → **graceful abort**; new additive
    outcome value `aborted_early_risk` with the trajectory recorded; abort is logged, never silent.
- **M2.2 Per-recipe retirement** (TemporalRunner, model-independent): on `consecutive_failures ≥ 10` →
  cool-down (double the interval, flag `cooldown: true` in temporal-state); on `≥ 25` → **retire**
  (`retired: true`, skipped by eval loop, visible in `mentu temporal list`), emit one `anomaly_detected`
  CIR signal (deterministic id `run-horizon-retire-<name>`), and require explicit
  `mentu temporal revive <name>` to reinstate. Counters already exist; this is pure policy.
- **M2.3 Tests**: policy state machine (temp home); revive path; kill-switch; abort records outcome
  correctly; steering emits no CIR content (assert on message text); temporal retire/cool-down over a
  simulated failing schedule.
- **M2.4 Post-ship**: 7-day soak with `enforce` on infra/scheduled only; report against the
  pre-registered predictions in the CONTEXT doc; epistemics observatory picks up the boundary via the
  marker (beat tracking, not this executor).

**Gate M2 (frozen)**: pre-registration commit precedes code-merge commit (timestamps); all M2.3 tests
green; during the 7-day soak zero feature-run aborts and zero unexplained scheduler stalls; the retire
rule fires on a synthetic failing schedule in ≤ 25 evaluations.

## M3 — White-box probes on local-model lanes (deferred; research)

Replicate the paper's method inside Mentu where weights are open (MLX/LoRA lanes): capture hidden states
at step boundaries, train linear probes for the same labels, and compare the internal horizon against
M0's behavioral horizon. No gate; explicitly non-blocking; candidate for a standalone research note.
Reference: arXiv:2607.05188.

## Final verification battery

Full engine test suite green; `make install` + smoke (`mentu --version`, one live scored run showing
`risk_trajectory`); epistemics `observatory/collect.py` runs unchanged against the live home; old ledger
lines still parse; commit trail shows M2.0 preceding M2.1-2 merges.

## Risks (named)

- **Family leakage / ephemeral mix**: 219 recipe families, ~90% single-week — identity features are
  banned; splits are temporal with family-overlap reporting.
- **Regime drift**: the 2026-07-08 purge changed retrieval dynamics; regime flags are features, and the
  model version is stamped per run so post-purge retraining is clean.
- **Class imbalance** (~83% success): PR-AUC reported alongside ROC; thresholds set on precision at
  fixed recall, not raw score.
- **Decodability ≠ causality** (the paper's own caveat): the policy only needs prediction, not
  mechanism — but P4 (steering non-harm) is pre-registered to catch harmful feedback loops.
- **C1b/C25 contamination**: steering text is CIR-free; scores are invisible to runs; both protections
  are asserted in tests.
