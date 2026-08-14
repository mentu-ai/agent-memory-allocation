---
id: c9
name: pattern-crystallization-utility
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/frameworks/cir-memory-as-infrastructure.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/frameworks/dcos-semantic-coordination.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/frameworks/participatory-epistemic-interfaces.md.txt
  - Workspaces/mentu-physics/foundational/blueprint/docs/core-concepts/cognitive-archaeology.md.txt
verdict: null
---

# C9 - Pattern crystallization utility

## Claim

Repeated epistemic traces become more useful when compressed into certified pattern
signals. A crystallized pattern should be cheaper and more effective to retrieve,
inject, and act on than a loose bundle of its raw source signals.

This is the empirical residue of the old CIR/DCOS/participation framework language:
"pattern crystallization," "recursive reflection," "template evolution," and
"cognitive archaeology." It does not assert that pattern creation itself is
intelligence. It asks whether the created patterns become useful in later work.

## Origin

The core-concepts/frameworks corpus repeatedly describes a loop:

1. record epistemic signals;
2. cluster or interpret repeated traces;
3. crystallize reusable patterns/templates;
4. feed those patterns back into future orchestration and cognition.

The live CIR already performs step 3: it writes `crystallize` signals of kind
`pattern`, with `source_ids` linking back to source clusters. C9 tests whether step 4
exists as measured utility rather than aspiration.

## Operationalization

**Datasets**:

- `~/.mentu/cir.db`, read-only:
  `signals` rows where `op='crystallize' AND kind='pattern'`, their `source_ids`,
  timestamps, verification state, and any downstream relation/exposure signals.
- `~/.mentu/training/cir-run-outcomes.jsonl`, read-only:
  `injected_signal_ids`, `used_signal_ids`, `ignored_signal_ids`,
  `unproven_signal_ids`, `success`, `steps_ok`, `steps_total`, `duration_ms`,
  `total_cost`, `recipe`, and `started_at`.

**Unit**:

- Primary: crystallized pattern signal.
- Secondary: run exposure to at least one crystallized pattern.

**Predeclared predictor**:

- Pattern maturity: source cluster size, age, verification state, and whether the
  pattern has a stable source cluster in `source_ids`.
- Pattern exposure: run outcome row contains the pattern id in `injected_signal_ids`
  or a successor field that explicitly records pattern injection.

**Outcomes**:

- **Selection utility**: crystallized patterns are selected/injected in later runs.
- **Use utility**: exposed patterns appear in `used_signal_ids` or a successor
  measured-use field.
- **Outcome utility**: exposed-and-used pattern runs have higher step ratio, success,
  or lower duration/cost than matched raw-source exposure runs.
- **Compression utility**: pattern exposure supplies fewer signals/bytes than a raw
  source bundle while preserving or improving outcome utility.

**Controls**:

- recipe;
- run class;
- post-crystallization age;
- source cluster size;
- C1b footer/usage attribution regime;
- C2 friction week;
- C8 coherence load once recipe manifest identity exists.

## Predictions (stated 2026-06-19, before C9 verdict analysis)

- **P1**: After pattern exposure is wired, crystallized patterns are selected more
  often than size-matched raw source clusters for repeated recipes.
- **P2**: Runs that use crystallized patterns show equal or better step ratio than
  matched runs exposed only to raw source signals.
- **P3**: Pattern exposure reduces context volume per useful run compared with raw
  source-bundle exposure.
- **P4**: Large-source patterns without later selection/use are storage artifacts,
  not cognitive infrastructure.

## Falsification criteria

- Patterns are created but rarely selected or injected after they are eligible ->
  **revised** as archival compression, not runtime utility.
- Patterns are selected but not measured as used -> **instrument insufficient** until
  the C1b usage channel can see them.
- Pattern exposure has no advantage over raw source exposure after controls ->
  **refuted** as a utility claim.
- Benefit exists only for one recipe family or temporal cycle -> **revised** as a
  local template effect, not a general crystallization mechanism.

## Gate

C9 may produce a verdict only when all are true:

- at least 1,000 crystallized pattern signals;
- at least 95% of crystallized patterns have non-empty `source_ids`;
- at least 5 days of crystallization span;
- at least 50 runs after the first crystallized pattern exposure;
- at least 30 runs with crystallized pattern ids in `injected_signal_ids` or an
  equivalent pattern-exposure field;
- at least 10 runs with measured pattern use;
- C1b footer/usage attribution is mature enough to distinguish non-use from
  non-observation.

The current substrate clears pattern creation and source-linkage gates, but not
pattern exposure or measured-use gates.

Current readiness run (2026-06-19): `analyses/c9-pattern-crystallization-utility/analyze.py`
found 6,214 certified crystallized patterns spanning 5.2 days, with 6,214/6,214
patterns carrying source clusters and zero malformed `source_ids`. No crystallized
pattern ids appear in run outcome injection/use arrays. C9 is therefore `INSTRUMENT
INSUFFICIENT` for verdict work today.

## Known limitations

- Current pattern signals are often machine clusters with sparse summaries and no
  asserted confidence. Utility must be proven downstream; certification alone is not
  enough.
- Large recurring temporal jobs can dominate source clusters. Recipe and temporal
  cycle controls are mandatory.
- A pattern can be useful to observability without being useful to run execution. C9
  concerns runtime/retrieval utility only.
- This conjecture is downstream of C1b. If usage attribution cannot see pattern use,
  C9 cannot render a verdict.
