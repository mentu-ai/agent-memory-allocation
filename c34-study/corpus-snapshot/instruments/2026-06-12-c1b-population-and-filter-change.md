# Instrument note — C1b population widening, collector filter, and the end-of-experiment protocol

**Date**: 2026-06-12 (written from the engine-side repair session, not a beat
invocation; the next beat inherits these numbers).
**Follows**: `instruments/2026-06-11-c1b-eligibility-accounting.md` (F1
overcount, closed below) and packet 2026-06-11 interpretation item 2 ("the
arithmetic is the real news: at ~2 eligible runs/day, 150/arm is months away").
**Method**: engine-side audit + deployment (mentu-complete commits `f2add6f`,
`a33eec0`, `4f225f9`; engine redeployed and the temporal daemon restarted,
pid 7505), read-only inspection of `~/.mentu/training/cir-run-outcomes.jsonl`,
and one live probe run. collect.py changes verified read-only against the real
dataset. No frozen field of any conjecture file was touched.

## Summary

The experiment's accrual machinery was repaired on three axes, none of which
changes the treatment: (1) the randomization switch moved from a shell-local
env var to the engine feature flag `cir_randomize` in `~/.mentu/flags.json`,
so every dispatch surface — including launchd/temporal — can now arm runs;
(2) temporal-fired children regain CIR (the daemon's self-protective
MENTU_DISABLE_CIR* env vars are no longer inherited), opening the scheduled
population the prior arithmetic showed was structurally absent; (3) the
collector now excludes fixture/smoke/infra runs from arms and eligibility,
which zeroes the contaminated arm counts — 2 of the 3 arms ever recorded were
engine smoke tests. The gate restarts clean at 0/0. Selection and injection
logic are untouched: same coin, same hash, wider and cleaner population.
`REGIME_BOUNDARY` stays 2026-06-10T12:19:00Z. This note also pre-registers
the deferred selection-loosening trigger (F3) and the end-of-experiment
consolidation protocol (F4).

## Findings

### F1 — Population widening (deployment change, not treatment change)

Three structural reasons the gate was unreachable, now fixed in the engine:

- **The switch never reached scheduled dispatch.** `MENTU_CIR_RANDOMIZE=1`
  lived in `~/.zshrc`, so only interactive shells armed runs: 3 armed vs 38
  unarmed in the experiment's first 48h. The switch is now the engine feature
  flag `cir_randomize` (`~/.mentu/flags.json`, visible in the mentu-terminal
  settings UI) — the **single kill-switch**. The `.zshrc` export is retired.
  Env vars remain as test/escape overrides only: a PRESENT
  `MENTU_CIR_RANDOMIZE` decides in both directions; `MENTU_CIR_RANDOMIZE_ARM`
  still forces an arm. (Engine bonus fix: the flags.json array format the
  terminal writes was silently undecodable before — the engine ignored the
  whole file; it now parses both formats.)
- **Temporal children were structurally ineligible.** The daemon's launchd
  plist sets four `MENTU_DISABLE_CIR*` vars to keep the daemon's own loop off
  cir.db (the June WAL-writer wedge, since fixed at the root), and
  `fireFormula` passed the daemon env verbatim into every fired child — all
  23 temporal-fired post-regime runs had briefs disabled. Children now get a
  scrubbed environment (`TemporalRunner.childEnvironment`); the daemon
  process keeps its own protection.
- **Live proof**: with both env vars explicitly absent, a probe run
  (`flagprobe-smoke`) armed via the flag path (withheld, runId hash parity) —
  and self-filtered out of the experiment by its `run_class`.

Expected new scheduled population: `tls-release-discovery` (~4 formula
runs/day, feature-class), `tls-drift-reverify` (1 per 3 days), plus `mentu`
invocations inside command-mode children. Watch items for the next beats:
injected-arm scheduled runs pay prompt-cache misses (cost gauge), and
`~/.mentu/logs/temporal.log` for any wedge symptoms (none expected; root
cause fixed).

### F2 — Collector filter: arms and eligibility are feature-class only

`collect.py` now classifies every row (`run_class` field when present —
engine writes it since 2026-06-12 — else the engine's name heuristic plus an
`rcsleep*`→infra extension the engine misses) and excludes
{fixture, smoke, infra} from the arm partitions AND the eligibility pool. A
start-time guard closes the 06-11 note's F1 exact-one overcount
(`cua-parity-w3` started pre-boundary on the pre-deployment binary).

**The reset, stated plainly**: unfiltered arms were 1 injected / 2 withheld;
all three were plumbing tests (`rce2e`, `contract-smoke-warn`,
`contract-smoke-enforce`). Filtered arms are **0 / 0** — the widened
population starts from a clean slate. Current filtered eligibility: 0/2
post-regime feature-class runs.

### F3 — Pre-registered trigger for selection loosening (deferred Repair 3)

Loosening brief selection changes what "injected" means — a treatment change.
It stays frozen unless the trigger fires: **if filtered eligibility remains
below ~2 runs/day after 7 beats (≈ 2026-06-19), widen the brief recency
window 30→60 days and lower the confidence floor 0.35→0.30
(`CIRContextBrief.swift`), and stamp a NEW `REGIME_BOUNDARY` in collect.py**
so pre/post rows never pool. Until then, eligibility moves only through
population (F1) and the organic growth of the distilled pool.

### F4 — End-of-experiment protocol (pre-registered)

Ending C1b = setting `cir_randomize` to `enabled:false` in
`~/.mentu/flags.json`. Ending is **not** just stopping accrual — the teardown
consolidates the learnings into epistemics:

1. **Verdict**: write the readout against the frozen predictions P1–P3 into
   the C1b conjecture file's verdict field (the claim and predictions
   themselves stay untouched, per the constitution). A null or negative
   result is a result.
2. **Closing instrument note**: the final numbers (arms, per-arm success,
   use_rate, eligibility trajectory) plus the instrument lessons — what the
   experiment taught about brief relevance, eligibility, and population
   design, independent of the verdict.
3. **Substrate consolidation**: distill the lessons back into CIR as explicit
   signals (kind=learning/finding with provenance to the readout), so the
   memory system the experiment measured also remembers what was learned.
4. **Switch hygiene**: leave the flag present-but-disabled with its
   description pointing at the readout note, or remove it once consolidated.

The same protocol applies to early termination: an aborted experiment still
gets the closing note recording why it was stopped and what was learned.
