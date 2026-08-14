---
id: c31
name: capability-conditioned-resident-utility
status: operationalized
registered: 2026-07-26
lineage:
  - corpus/conjectures/c27-resident-set-utilization.md
  - results/2026-07-18-c27-resident-set-utilization.md
  - paper/agent-memory-allocation/paper-v1.md
  - docs/BUILD-c31-capability-conditioned-resident-utility-v1.md
  - instruments/2026-07-26-agentbench-context-allocation-instrument.md
verdict: null
result: null
tracking:
  last_beat: 2026-07-26
  note: "registered before adapter code or model runs; four-task/16-cell pilot validates the instrument only and is permanently barred from adjudication"
---

# C31 — Capability-conditioned resident utility

## Claim

Moving identical developer-provided repository guidance from
**boot-resident content** to **pointer-paged content** preserves task success
more closely for Claude Opus 5 than for Claude Opus 4.8. The utility of
resident guidance is therefore conditional on model generation: a model change
is an allocation-regime boundary, and residency policies cannot be inherited
across that boundary without remeasurement.

The content is held byte-identical across arms. Only its placement changes.
C31 therefore measures allocation rather than annotation richness, summary
quality, or curation effort.

## Origin

C27 found a highly concentrated skill-invocation distribution as seen, but its
coverage floor failed and its instrument explicitly could not measure the
visibility effect of resident-but-uninvoked guidance. C29 also used only one
answerer at one capability tier. C31 registers the missing counterfactual:
measure outcomes after changing residency while keeping guidance content,
tasks, tools, and evaluator fixed.

C31 does not amend C27. C27's original gate, predictions, and eventual verdict
remain untouched.

## Operationalization

**Population**: the 138 public AGENTBench instances at dataset revision
`82c4b95db706965e82736ef5fe8404be3c0f79ba`, executed through harness commit
`da299c4c6b14a9abad2ceef8c751f6c45c543656`. Four task ids are selected
mechanically across four repositories for a non-verdict-bearing pilot and
permanently excluded. The intended future adjudication population is the
remaining 134 tasks.

**Models**: `claude-opus-4-8` and `claude-opus-5`, both at explicit
`effort=high`, no fallback.

**Allocation arms**:

- `full_resident`: developer guidance remains in its auto-loaded file.
- `pointer_paged`: the byte-identical body moves to
  `.c31/full-guidance.md`; the auto-loaded file contains only the frozen
  pointer in the BUILD contract.

**Primary metric**: official AGENTBench task resolution.

**Secondary vector**: paid and uncached input tokens, output tokens, cost,
wall time, steps, tool calls, files touched, mechanically detectable rule
violations, resident-guidance tokens, and paged-body Read occurrence/step.
No weighted or self-assigned composite score is permitted.

**Regime**: exact model id × effort × harness commit × dataset revision ×
adapter commit × task-manifest hash × pointer-text hash. Any change creates a
new regime; regimes are never pooled.

## Predictions (frozen 2026-07-26, before adapter code or any model run)

- **P1 (advanced-model non-inferiority)**: for `claude-opus-5`, the
  pointer-paged task-resolution rate is no more than **5 percentage points**
  below the full-resident rate:
  `success(pointer) >= success(full) - 0.05`.
- **P2 (capability interaction)**: the full-resident minus pointer-paged
  resolution penalty is at least **10 percentage points larger** for
  `claude-opus-4-8` than for `claude-opus-5`.
- **P3 (residency reduction)**: the median per-task reduction in
  boot-resident guidance tokens under pointer paging is at least **80%**.

## Falsification and adjudication criteria

- P1, P2, and P3 all pass with coverage floors met → **supported**.
- P1 and P3 pass but P2 is positive and below 10 percentage points →
  **revised**: paging is non-inferior at the registered margin, but the
  capability-conditioned effect size is not supported.
- The Opus 5 pointer arm is more than 5 percentage points below full residency
  → **refuted**: advanced-model non-inferiority fails.
- The interaction is non-positive (the Opus 4.8 penalty is no larger than the
  Opus 5 penalty) → **refuted on capability conditioning**.
- P3 fails → **refuted on the intervention**: the registered pointer
  transformation did not materially de-reside the guidance.
- Fewer than 100 non-pilot tasks remain, official evaluator coverage is below
  95%, requested/resolved model identities drift, task or context hashes
  disagree, or arm identity cannot be proven → **instrument insufficient**;
  no verdict.

The committed analyzer also reports repository-stratified paired bootstrap
95% intervals and paired discordance counts. These quantify uncertainty; they
do not move the frozen point-estimate thresholds.

## Gate

Verdict only from
`analyses/c31-capability-conditioned-resident-utility/analyze.py`, committed
after this registration and before the first model run, operating solely on
the frozen non-pilot manifest.

Coverage floors:

- at least 100 evaluable non-pilot tasks per factorial cell;
- official evaluator coverage ≥95% in every cell;
- one resolved model identity per requested model across the entire run;
- verified context-body identity for 100% of started cells.

The four-task, 16-cell pilot may validate instrumentation only. Pilot task
success is never aggregated, compared, or admitted to adjudication.

## Known limitations

- AGENTBench covers Python repository tasks and 12 public repositories; it
  does not establish a universal task distribution.
- Official test resolution may not capture compliance value that does not
  change tests. Rule-violation outcomes are secondary and only mechanical.
- Pointer-arm Reads prove exposure, not use; the allocation contrast, not Read
  attribution, carries the causal estimand.
- Model id bundles many capability differences. C31 identifies a regime
  interaction, not its internal cause.
- One attempt per task/cell means stochastic run variance remains; task-level
  pairing and complete publication of negative results are the mitigation.
- The future 536 scored runs are not authorized by this registration session.
