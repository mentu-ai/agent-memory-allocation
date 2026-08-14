---
id: c3
name: epistemic-entropy
status: tested
lineage:
  - epistemic-main/canon/law-suites/second-law-of-epistemic-thermodynamics.md
  - epistemic-main/canon/law-suites/laws-of-epistemic-thermodynamics.md
verdict: revised
result: results/2026-06-10-c3-epistemic-entropy.md
tracking:                      # machine-updated by observatory beats only
  last_beat: 2026-07-13
  retest_gate: "91/100 detections or 35/60 detector-days — NEAREST GATE (9 detections or 25 days to open). +15 across the 07-01..07-12 dark gap, in two bursts: +5 on 07-02, +10 on 07-07 — both inside the CIR-grind window (burst-distress correlation now seen thrice, incl. 06-28's +6). Return gauge RE-BASED by the 2026-07-08 exhaust purge (instruments/2026-07-08-cir-exhaust-purge-regime-note.md): 86/161,935 ever accessed (was 103/397,497); context_used 24->15 (prune cascade deletes trust events attached to purged signals). cir.db gauges are retrospective-lossy across the boundary — never pool; durable ledger = cir-run-outcomes.jsonl."
  resolved: 2
  watch: [packets/2026-06-14.md, packets/2026-06-16.md, packets/2026-06-28.md, packets/2026-06-30.md, packets/2026-07-13.md]
---

# C3 — Epistemic entropy

## Claim

Without active maintenance, stored knowledge degrades measurably: trust confidence
decays in the absence of reinforcement events, contradictions accumulate faster than
they resolve, and resolution happens only through explicit counter-entropic work.

## Origin

The 2025 corpus's second law of epistemic thermodynamics — entropy increases unless
countered by ordered energy input — was among its most defensible analogies, because
it names observables: decay, contradiction, maintenance. The "irreversibility
threshold" constant is dropped (never derived); the decay and accumulation claims are
retained.

## Operationalization

**Datasets**:
- `~/.mentu/cir.db` (schema v14, read-only):
  - `trust_events`: every confidence change with cause (reinforcement, contradiction,
    decay), old/new values, timestamps.
  - `contradictions`: pairs, severity, `detected_at`, `resolved_at`.
  - `signals`: `reinforcement_score`, access counts, decay parameters.
- `~/.mentu/sentinel-logs/` + `sentinel-state/`: firing history of `embedding-drift`
  and `cir-contradiction-drift` sentinels (live entropy gauges).

**Measures**:
- Confidence trajectory of signals with zero reinforcement events vs. reinforced
  signals (does unmaintained confidence decline as the decay model says?).
- Contradiction detection rate vs. resolution rate over time; distribution of
  time-to-resolution.
- Whether resolution events coincide with explicit work (commitments, runs) rather
  than occurring spontaneously.

## Predictions (stated 2026-06-10, before analysis)

- **P1**: Unreinforced signals show monotonically non-increasing confidence;
  reinforced signals hold or recover.
- **P2**: Cumulative detected contradictions outpace cumulative resolved ones during
  periods of low maintenance activity.
- **P3**: Time-to-resolution is heavily right-skewed; a tail of contradictions never
  resolves.

## Falsification criteria

- Unreinforced signals hold confidence indefinitely (decay is configured but inert,
  or knowledge doesn't rot here) → **refuted** as stated; revise toward "decay is a
  policy, not a phenomenon."
- Contradictions resolve spontaneously at the same rate they appear → **refuted**.

## Known limitations

Decay may be *implemented* by the system (a half-life parameter exists in the
schema) — in which case P1 partly tests Mentu's bookkeeping, not nature. The honest
question is P2/P3: whether the *world* (contradictions, drift) degrades the corpus
faster than passive processes repair it. The analysis must separate mechanical decay
from evidence-driven confidence changes using `trust_events.cause`.

## Result (2026-06-10): REVISED — split

**Decay half of P1: SUPPORTED.** Unaccessed signals show a monotone age gradient
of confidence erosion (mean Δ −0.009 at 0–7d → −0.270 at >60d; 55% of >60d
signals decayed; zero boosted). Graduated narrowly as
`corpus/supported/c3a-mechanical-decay.md`.

**Reinforcement half of P1: untestable as of this test** — 98 of 217,629 signals
(0.045%) ever accessed; 2 reinforcement events in system history, both caused by
this corpus's own founding audit. Becomes testable when C1b makes return happen.

**P2/P3 (contradictions): INSUFFICIENT-EVIDENCE** — 11 contradictions total; the
detector is days old. **Re-test gate: ≥60 days of detector operation or ≥100
detected contradictions, whichever first.** Predictions P2/P3 remain frozen as
written above for that re-test.

Full record: `results/2026-06-10-c3-epistemic-entropy.md`.
