---
id: c1b
name: return-as-intelligence-randomized
status: operationalized
lineage:
  - corpus/refuted/c1-return-as-intelligence.md
  - instruments/2026-06-10-return-loop-diagnosis.md
verdict: null
experiment_started: 2026-06-10T12:19Z
tracking:                      # machine-updated by observatory beats only
  last_beat: 2026-07-13
  beats: 21
  regime_boundary: 2026-06-15T02:57:24Z   # CIR_USED footer instrument fix (instruments/2026-06-15); pre-fix arms void, never pooled
  accrual: { injected: 24, withheld: 21 }   # POST-FIX feature-class arms — the live gate. 07-13 (beat #20; observatory dark 07-01..07-12): +0/+0 FOR 15 DAYS — ANOMALY: all 75 gap-span feature-class runs were COLD (selected_signal_count=0 AND brief_bytes=0); last eligible run 06-28T19:25:47Z (cir-positive-reuse-audit, injected). P(0/91 eligible under the prior 16.8% rate) ~ 5e-8 — channel broken or changed, cause unresolved read-only (grind starvation / post-purge pool contraction / recipe-mix shift; see packets/2026-07-13.md item 3). Prior: 06-30 +0/+0 flat; 06-29 +1/+0; 06-28 +2/+2 (first balanced accrual + first within-recipe contrast); 06-26 +3/+0 (first clean citations).
  accrual_prefix_void: { injected: 13, withheld: 6 }   # pre-fix arms, broken footer channel (missing_footer_rate=1.0); kept as a void ledger, NOT pooled
  eligibility: "post-fix feature-class runs: 45/359 prepared a non-empty brief (07-13: +91 denom since 06-30, +0 eligible — a 15-DAY DROUGHT; every gap-span feature run had ssc=0 and brief_bytes=0; last eligible 06-28T19:25:47Z). Eligible == armed (45). MECHANISM (06-25, confirmed 06-26..29): arming is gated on BRIEF NON-EMPTINESS, not recurrence — the 06-26 cir-positive-reuse-audit loop (3 COLD then 3 WARM with a monotonically growing recipe-keyed brief, ssc 2→3→4, armed AND cited AND succeeded) remains the canonical demonstration; recurrence neither necessary nor sufficient (VF3-callcapture recurred 5x, never armed). Gap-span no-brief families now include: crawlio-cockpit*, crawlio-safety*, crawlio-codex-fixes*, crawlio-workbench*, caw-*, ledger-first-outcome, tiny, cpdl-m0-contract (plus the earlier list: RECON, crawlio-zim, csp-crawl-embeddings, crawlio-web-engine-w*, crawlio-figma-result-w*, selector-forge-m*, VF3-callcapture, cal-m0/m1/m3)."
  gate: "post-footer-fix re-accrual: 45/300 feature-class arms (injected 24/150 = 16%, withheld 21/150 = 14%; combined 15%; digest binding min-arm 14%). F5 CLEARED — footer health 8/24 (mean mfr 0.70). 07-13 delta (vs 06-30): +0/+0 — ZERO ACCRUAL VELOCITY FOR 15 DAYS (anomaly, escalated in packets/2026-07-13.md item 3). At this rate the gate NEVER fills — needs eligible-run traffic (feature runs in domains with prior signals) or a dated re-design decision by the owner. Unchanged: citing 6, useful 4, inj success 13/24, wh 11/21. NEW REGIME BOUNDARY 2026-07-08 (CIR exhaust purge, instruments/2026-07-08-cir-exhaust-purge-regime-note.md): brief composition changes across it — pre/post use-when-offered rates are NOT comparable arms; cir.db context_used was re-based 24->15 by the prune cascade, so the '24 = 2+3+4+5+5+5' crosscheck is no longer re-derivable from cir.db (durable record = cir-run-outcomes.jsonl). STILL VALIDATES THE INSTRUMENT, NOT P1: recipe step prove-positive-reuse is purpose-built to reuse; P2 6/24 (25% < majority). Raw arm success near-even, underpowered, not a readout (rule 6). INFRA EXCLUSION stable at 109 armed ane-fortress (inj 55/wd 54), ~2.4x the 45 admitted arms, load-bearing. 'First wild useful' marker unchanged (06-26 05:31Z run)."
  watch: [instruments/2026-06-12-c1b-population-and-filter-change.md, instruments/2026-06-15-c1b-footer-measurement-fix.md, instruments/2026-07-08-cir-exhaust-purge-regime-note.md, packets/2026-06-29.md, packets/2026-06-30.md, packets/2026-07-13.md]
---

# C1b — Return-as-intelligence, the fair test

## Claim

When the stored knowledge is distilled (not exhaust) and injection is randomized,
runs receiving injected prior knowledge succeed at a higher rate than runs denied
it, within the same recipe.

## Why this exists

C1 was refuted in its strong form *as instrumented*: agents received briefs and
honestly reported `CIR_USED: none`, because what was injected was operational
exhaust (see `instruments/2026-06-10-return-loop-diagnosis.md`). That refuted the
implementation, not the theory. The theory's fair test requires fixing what C1
exposed. This is the answer to "how would return-as-intelligence be proven true?"
— not by asserting it, and not by wanting it to be true, but by giving it the
strongest test it can survive.

## Instrument prerequisites (must land before any data counts)

1. **Distillation at capture**: injectable pool restricted to distilled,
   self-contained lessons (no `step_result` stdout tails; bodies survive
   truncation intact).
2. **Citeable reflections**: the distilled channel gets stable IDs valid in
   `CIR_USED`, closing the measurement blind spot at `CIRContextBrief.swift:603`.
3. **Within-recipe randomization**: for every eligible run, a recorded coin flip
   decides injection; the flip, not operator choice, determines the arm.
4. **Chain check**: one live run traced end-to-end (brief → prompt → footer →
   `used_signal_ids`) confirming a *deliberate* citation registers correctly.

## Design

- **Unit**: sequence run. **Arms**: injected vs withheld, randomized within
  recipe. **Primary outcome**: run success. **Secondary**: `steps_ok/steps_total`,
  `duration_ms`, `total_cost`, `use_rate` among injected.
- **Analysis**: success-rate difference with Fisher exact within recipe strata,
  combined across strata (Mantel–Haenszel); per the constitution, predictions and
  thresholds are frozen in this file before the first randomized run is examined.

## Predictions (frozen now, before any randomized data exists)

- **P1**: Pooled within-recipe success rate is higher in the injected arm.
- **P2**: Among injected runs, `use_rate > 0` in a majority (if distillation
  worked, agents will cite).
- **P3**: The effect, if present, concentrates in runs whose recipe family has
  prior failures recorded — return helps most where there is something to return.

## Falsification criteria

- Pooled effect ≈ 0 or negative across ≥150 runs/arm → **refuted**: distilled,
  randomized return does not improve outcomes in this system.
- P2 fails (agents still cite nothing) → instrument prerequisite 1 failed;
  result void, back to engineering.

## Power note

At baseline success ≈ 30%, detecting a +15pp effect at α=0.05 with 80% power
needs ≈ 150 runs/arm. At the observed rate (~16 outcome-recorded runs/day),
that is roughly 3 weeks of randomized operation.

## Instrument status (2026-06-10) — prerequisites LANDED, experiment LIVE

All four prerequisites shipped in `mentu-complete` branch
`feat/cir-c1b-randomized-return` (commit `dd43f96`), 40 tests green including
both E2E chain tests and the live controlled A/B eval:

1. ✅ Distillation at capture — brief evidence pool restricted to
   distilled-knowledge kinds (`step_result`/`verdict`/`commitment`/
   `recipe_version` removed; `reflection`/`learning` admitted);
   `CIRRuntimeEvidencePolicy` retained as second defense.
2. ✅ Citeable reflections — reflection IDs join `injectedSignalIds` and the
   usage contract; reflection confidence now derives from outcome quality
   (0.5 + 0.3·steps_ratio on pass, 0.4 on fail).
3. ✅ Within-recipe randomization — `MENTU_CIR_RANDOMIZE=1` assigns arms by
   FNV-1a hash parity of runId (deterministic, stateless). Withheld runs record
   the counterfactual (`withheld_signal_ids`) with clean usage aggregation;
   outcomes carry `randomization_arm` and a `withheld` verdict.
4. ✅ Chain check — E2E tests verify brief→prompt→footer→`used_signal_ids`
   registration; the controlled A/B eval exercised the path in a live run. The
   first wild `useful` verdict will be the definitive in-production confirmation.

**Deployment**: release binary signed and installed (`~/.local/bin/mentu`,
`~/.mentu/bin/*`) 2026-06-10; `MENTU_CIR_RANDOMIZE=1` active in `~/.zshrc`
(interactive runs) and the `ai.mentu` launchd environment (daemon-spawned runs;
verified in the running process). **Arms accrue from 2026-06-10T12:19Z.**

**Analysis gate**: do not analyze before ≥150 outcome-recorded runs per arm;
only runs with `randomization_arm` set count. Pre-2026-06-10 data is a
different instrument regime and must never be pooled with experiment data.
