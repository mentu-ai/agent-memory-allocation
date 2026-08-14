---
id: c12
name: translation-bottleneck
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/ese/science/cognitive-systems-evolution/laws/translation-bottleneck-law-canonical-source.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/science/cognitive-systems-evolution/laws/translation-bottleneck-law.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/science/knowledge-architecture/patterns/canonical-ids.md
  - Workspaces/mentu-physics/foundational/blueprint/ese/science/knowledge-architecture/frameworks/source-of-truth.md
verdict: null
---

# C12 - Translation bottleneck

## Claim

Cross-surface transformations lose usable meaning, and the weakest translation point
in a run constrains downstream usefulness. Runs where selected knowledge fails to
be injected, injected knowledge fails to be read or cited, cited knowledge is invalid,
or source identity cannot be preserved should show lower reliability and weaker reuse
than runs whose translation chain stays intact.

This is the operational version of the Translation Bottleneck Law. It drops the
unbounded "maximum intelligence" wording and keeps the measurable residue: meaning
must survive handoff between retrieval, brief, agent behavior, footer attribution,
outcome extraction, and later reuse.

## Origin

The science corpus describes translation organs, modal boundaries, translation debt,
semantic drift, and canonical identity. Mentu already exposes one concrete translation
chain through run outcomes:

`selected evidence -> injected context -> read/brief surface -> used footer -> outcome row`.

C12 exists to test whether attrition across that chain predicts worse downstream
outcomes once C1b and C5 have matured.

## Operationalization

**Datasets**:

- `~/.mentu/training/cir-run-outcomes.jsonl`, read-only:
  - `selected_signal_count`
  - `injected_count`
  - `read_count`
  - `brief_bytes`
  - `missing_footer_count`
  - `used_count`
  - `invalid_used_count`
  - `unproven_signal_ids`
  - `surfaces`
  - `outcome`, `success`, `steps_ok`, `steps_total`
- `~/.mentu/cir.db`, read-only, for later source identity, relations, and reuse.

**Translation stages**:

- **Selection**: candidate signals are selected for a run.
- **Injection**: selected knowledge enters a context surface.
- **Brief/read surface**: injected context is made available in a step brief or
  read surface.
- **Use attribution**: agent output cites or uses the injected material.
- **Validity**: cited/used material is proven, not invalid or unproven.
- **Outcome extraction**: the run outcome preserves enough identity to trace reuse.

**Debt components**:

- selected-but-not-injected;
- injected-but-not-used;
- missing footer after injection;
- invalid used signal;
- unproven used signal;
- surface absence for expected translation stages;
- identity loss that prevents source or workspace reconstruction.

**Outcomes**:

- run success and warning/failure outcome;
- `steps_ok / steps_total`;
- later reuse of the same signal or pattern;
- downstream contradiction/correction after purported use;
- boundary-transfer performance from C5.

**Controls**:

- recipe family;
- workspace;
- week/cohort;
- step count;
- C2 friction;
- C5 boundary class;
- C10 structure debt.

## Predictions (stated 2026-06-19, before C12 verdict analysis)

- **P1**: Runs with complete selection -> injection -> use attribution chains will
  have higher later reliability than runs with attrition at any stage.
- **P2**: Missing-footer and injected-but-unused debt will predict failure/warning
  more strongly for multi-step recipes than for one-step smoke tests.
- **P3**: Invalid or unproven used signals will predict later corrections or lower
  reuse more strongly than simple non-injection.
- **P4**: C5 boundary-impedance effects will sharpen when translation-debt rows are
  excluded or controlled.

## Falsification criteria

- Translation-stage attrition does not predict run reliability, reuse, or correction
  after controls -> **refuted**.
- Effects are entirely explained by recipe difficulty or workspace maturity ->
  **revised** as workload confounding.
- Missing-footer effects disappear after the C1b footer-fix cohort matures ->
  **revised** as historical instrument failure, not translation bottleneck.
- Any verdict produced before C1b post-fix gate and C5 controls mature is invalid.

## Gate

C12 may produce a verdict only when all are true:

- at least 300 post-footer-fix randomized C1b rows;
- all translation-stage fields are present in run outcomes;
- at least 8 weeks of post-footer-fix outcome history;
- C5 boundary classes are available for the same window;
- C10 structure debt can control identity loss;
- the analyzer computes translation debt before outcome comparison.

The current corpus has translation-stage fields and enough historical rows for
readiness diagnostics, but not a mature post-footer-fix randomized window.

## Known limitations

- Missing footers can mean instrumentation failure, not true non-use.
- Some selected signals should not be injected; selection attrition is not always bad.
- C12 overlaps C1b, but C1b tests randomized return; C12 tests stage-by-stage meaning
  preservation across the return chain.
- Cross-human translation and organizational translation are outside the current
  Mentu instrument unless they become explicit CIR signals.
