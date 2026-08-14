---
id: c8
name: coherence-dividend
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/constitutional-intelligence/cost-of-coherence.md
  - Workspaces/mentu-physics/foundational/threshold-of-epistemic-activation.md
  - Workspaces/mentu-physics/foundational/epistemic-escape-velocity.md
  - Workspaces/mentu-physics/foundational/principles-laws-structural-imperatives.md.txt
verdict: null
---

# C8 - Coherence dividend

## Claim

Coherence mechanisms have a measurable cost and a possible dividend. Recipes with
more predeclared guardrails should cost more up front, but after maturity they should
produce fewer repeat failures, fewer warning-heavy runs, and less downstream rework
than comparable low-guardrail recipes.

This is the empirical salvage of "the cost of coherence." It does not assert
constitutional thermodynamics, fixed sovereignty percentages, a critical temperature,
or inevitable escape velocity. It asks a narrower operational question: does explicit
verification structure pay back its overhead in the running Mentu system?

## Origin

The 2025 cost-of-coherence document argued that constitutional compliance imposes
initial computational overhead and later becomes performance advantage. The activation
threshold and escape-velocity notes gave the same shape in phase-transition language:
below the threshold, systems drain effort; above it, structure, memory, and recursive
checks make them self-sustaining.

The retained claim is modest. Guardrails are not presumed good. They must earn their
cost in observed outcomes.

## Operationalization

**Datasets**:

- `~/.mentu/training/cir-run-outcomes.jsonl`: `run_id`, `recipe`, `started_at`,
  `completed_at`, `duration_ms`, `total_cost`, `steps_ok`, `steps_total`,
  `steps_warn`, `success`, `outcome`, `run_health_label`.
- Recipe manifests, read-only, primarily under
  `/Users/rashid/Desktop/mentu-complete/.mentu/recipes/*.json`.
- `~/.mentu/cir.db`, read-only, for lifecycle signals and any future explicit
  violation/rework signals.

**Unit**:

- Primary: one recipe run.
- Secondary: `(recipe_family, week)` after enough repeated runs exist.

**Predeclared predictor**:

Coherence load is computed from the recipe manifest at run time. It is a static
manifest property, not an observed outcome. Components include:

- footprint contract: `expected_changes`;
- mechanical verification: `verify_requirements`;
- semantic verification: `semantic_assertion`;
- top-level human/approval gate fields;
- build/test command fields;
- explicit dependency sequencing (`depends_on`);
- explicit prerequisites (`requires`).

The analyzer may report current-manifest diagnostics, but verdict models must join a
run to the exact manifest hash or immutable run bundle that produced it. If the run
outcome row lacks a recipe manifest hash and no immutable historical manifest can be
reconstructed, C8 is `instrument insufficient`.

**Outcomes**:

- **Immediate cost**: duration per step, total cost per step, warning count.
- **Immediate reliability**: success, `steps_ok / steps_total`, warning-free success.
- **Downstream dividend**: fewer repeat failures for the same recipe within seven
  days, lower failure rate after the recipe has at least three prior runs, fewer
  violation/rework signals if those become available.

**Controls**:

- recipe family;
- step count;
- run class;
- created-day or week cohort;
- backend/model where available;
- prior recipe-run count;
- C2 friction week where available.

## Predictions (stated 2026-06-19, before C8 verdict analysis)

- **P1**: Higher coherence load increases immediate overhead: longer duration per
  step, higher total cost per step, or more warning-bearing runs in early executions.
- **P2**: After maturity, higher coherence load predicts fewer repeat failures and a
  higher `steps_ok / steps_total` ratio than lower-load recipes of comparable size.
- **P3**: The dividend is stronger for heavier recipes (`steps_total >= 5`) than for
  smoke tests or one-step probes.
- **P4**: If coherence load has only overhead and no downstream reliability benefit,
  the old "cost transforms into advantage" claim fails in this instrument.

## Falsification criteria

- High coherence load increases duration/cost but does not improve mature reliability
  or reduce repeat failures -> **refuted**.
- Apparent benefit disappears after controlling for step count, recipe family, or
  run class -> **revised** as recipe-shape selection, not coherence dividend.
- Current manifests cannot be linked to historical runs by hash/version -> **instrument
  insufficient**, no verdict.
- Benefit appears only for semantic gates while mechanical guardrails do not help, or
  vice versa -> **revised** into mechanism-specific subclaims.

## Gate

C8 may produce a verdict only when all are true:

- at least 300 run-outcome rows;
- at least 50 distinct recipes;
- at least 20 days of run span;
- at least 20 recipe families with three or more runs;
- at least 80% of analyzed run rows have an exact `recipe_manifest_hash`,
  `manifest_hash`, immutable run bundle hash, or equivalent reconstructable recipe
  version;
- the analyzer computes coherence load before looking at outcome deltas.

The current live corpus clears the size/span gates but not the manifest-hash gate.
That is a hard boundary.

Current readiness run (2026-06-19): `analyses/c8-coherence-dividend/analyze.py`
found 629 run rows, 168 distinct recipes, and 33.1 days of span. All minimum
size/span gates pass. The manifest identity gate fails at 0.0% because run outcomes
do not carry `recipe_manifest_hash` or an equivalent immutable run-bundle hash. C8 is
therefore `INSTRUMENT INSUFFICIENT` for verdict work today.

## Known limitations

- High-guardrail recipes may be harder tasks. Step count and recipe fixed effects are
  mandatory controls.
- Guardrails can create warning/failure events by detecting problems that low-guardrail
  recipes silently miss. C8 must separate detection from outcome harm.
- Current run outcomes do not expose backend/model for every run. If backend becomes a
  major confound, the analysis must wait for better telemetry.
- This conjecture is downstream of C2 and C4: friction and recipe mass can mimic or
  mask the coherence dividend.
