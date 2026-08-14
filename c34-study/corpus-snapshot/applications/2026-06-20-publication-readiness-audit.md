# Publication readiness audit - 2026-06-20

## Scope

Read-only audit of publication readiness for the 2025 ESE source trees named by
Rashid:

- `Workspaces/epistemic-main/engineering/`
- `Workspaces/epistemic-main/science/`
- `Workspaces/epistemic-main/canon/`

No predecessor files were edited. No Mentu CLI or MCP CIR path was used. Current
readiness checks used direct file reads and the frozen analyzers in this repository,
which read Mentu data through raw read-only SQLite or direct JSONL/file reads.

## Publication rule

This corpus should not publish anything as real unless it satisfies one of these
statuses:

| Status | Publication label | Requirement |
|---|---|---|
| Measured result | Empirical result | Frozen claim, measurement procedure, and computed result from real Mentu data. |
| Operationalized conjecture | Live conjecture | Frozen claim, prediction, gate, falsification criteria, and named data source; no verdict language. |
| Engineering doctrine | Design pattern / operator doctrine | A practical prescription or diagnostic pattern, explicitly not presented as empirically validated unless linked to a measured result. |
| Lineage | Historical / theoretical lineage | Useful ancestor text, clearly labeled as legacy framing rather than current truth. |
| Hold | Not publishable as current canon | Law, formula, threshold, clinical/psychological claim, consciousness claim, physics analogy, or certainty claim without measurement. |

Default rule: old documents do not publish as current canon merely because they say
`canonical`. Their current status is determined by the 2026 constitution.

## Inventory snapshot

Source files audited: **490**

| Tree | Files |
|---|---:|
| `engineering/` | 103 |
| `science/` | 309 |
| `canon/` | 78 |

Frontmatter/status shape:

- 485 files are `epistemic_status: draft`.
- 46 files are `type: law`.
- 147 files are `type: core-concept`.
- 94 files are `type: framework`.
- 49 files are `type: field-declaration`.
- 47 files are `type: pattern`.

Automated risk markers across the old trees:

| Marker | Files |
|---|---:|
| Evidence/measurement language | 339 |
| Certainty language | 205 |
| Formula, threshold, coefficient, or constant language | 182 |
| Law language | 143 |
| Physics metaphor language | 99 |
| Psychological/clinical label language | 21 |

These markers are not verdicts. They identify files that need a publication wrapper,
rewrite, or hold decision before release.

## Current empirical spine

These are publishable now as measured results, with their limits intact:

| Claim | Publication status | Why |
|---|---|---|
| C1 return-as-intelligence, strong form | Publish as **refuted result** | Injected knowledge was delivered but not measurably used; the strong return loop failed as instrumented. |
| C3a mechanical decay | Publish as **supported narrow result** | Decay machinery produces the predicted monotone population signature for unaccessed signals. |
| C4 epistemic mass | Publish as **supported result with revised mechanism** | Heavier workflows fail more often and change more slowly; per-step degradation, not pure constant-p compounding, is the mechanism. |

These results can carry a public science canon because they have analyses and real
Mentu data behind them.

## Live conjectures, not verdicts

The following can be published only as open conjectures or measurement programs:

| Claim | Current gate state from 2026-06-20 checks |
|---|---|
| C2 friction-to-production | Accruing under revised operationalization; current results are not a clean verdict. |
| C5 boundary impedance | Operationalized; normalization design exists; no verdict analysis yet. |
| C6 epistemic compounding | Operationalized; must wait for C2 rev. 2 gate: at least 8 post-regime weeks and 10 mature strata. |
| C7 handle-mediated returnability | Size gate passes; first-seen handle snapshots/outcome telemetry insufficient. |
| C8 coherence dividend | Size gate passes; recipe manifest identity missing from historical run outcomes. |
| C9 pattern crystallization utility | Not ready; measured pattern substrate currently has 0 crystallized patterns. |
| C10 structure debt | Not ready; 33.9 days observed, but needs 56 days and mature workspace cohorts. |
| C11 measurement-action closure | Not ready; explicit measurement-response closure edges are 0. |
| C12 translation bottleneck | Not ready; post-footer-fix rows are 45/300 and C5 boundary classes are missing. |
| C13 semantic redundancy resilience | Not ready; source redundancy exists, but first-seen snapshots/recovery outcomes are absent. |
| C14 measurement contract validity | Not ready; unit/scale and calibration/reference metadata are insufficient. |
| C15 compiler invocation readiness | Not ready; no compiler-callable specimens, validation logs, or reuse follow-up. |
| C16 conditional activation selectivity | Not ready; candidate-level activation decisions and skipped/deferred cases are absent. |
| C17 schema-portable CIR processing | Not ready; per-file manifests, processing batches, coverage denominators, and downstream utility are absent. |
| C18 intent-density capture advantage | Not ready; capture modality, consent, quality, and capture-to-return linkage are absent. |
| C19 governed evolution stability | Not ready; exact governed-evolution events and governance/maturity/tension metadata are absent. |
| C20 participatory alignment yield | Not ready; exact participation events, attention cost, semantic handshakes, and outcome linkage are absent. |
| C21 typed context-network yield | Not ready; relation taxonomy, quality/currency metadata, exposure denominators, and outcome linkage are absent. |
| C22 operational surface debt | Not ready; 69 snapshots and 29 observations exist, but outcome-linked surface telemetry is far below verdict scale. |
| C23 review trust calibration | Not ready; 5 review commits exist, but the gate needs 200 with later outcome linkage. |

## Engineering publication decision

The engineering tree is the closest to public release, but not as empirical science.
It should publish as an **engineering doctrine and diagnostic manual** after light
status wrapping.

### Publish now, with design-status wrapper

These families are suitable for a v0 engineering canon if every page is labeled as
design doctrine, diagnostic vocabulary, or operational pattern rather than proven
law:

- `engineering/*/anti-patterns/`: especially operational fog, tool zoo, spreadsheet
  factory, decorated fragility, isolated knowledge islands, semantic drift.
- `engineering/*/diagnostics/`: interface illusion audit, tool collapse map, symptom
  grid, logic leak trace, system autopsy, operational eulogy.
- `engineering/epistemic-operations/patterns/`: workflow assembly line, recursive
  ingestion, closed-loop feedback, true clarity.
- `engineering/epistemic-operations/frameworks/instrumented-ese-lab-operating-model.md`
- `engineering/knowledge-orchestration/frameworks/recursive-publishing-engine.md`
- `engineering/knowledge-orchestration/frameworks/participatory-intelligence-field-guide.md`
- `engineering/cognitive-interfaces/frameworks/friction-ontology.md`
- `engineering/cognitive-interfaces/frameworks/layer-maturity-grid.md`
- `engineering/recursive-intelligence/patterns/return-path-engineering.md`

These are publishable because they are useful operator language and because C22 now
turns their empirical residue into a future test. Their public label must not imply
that C22 is already supported.

### Publish only as conjecture lineage

These contain important ideas but must be tied to current conjectures rather than
published as settled claims:

- Return-as-intelligence material -> C1 refutation plus C1b successor.
- Translation bottleneck material -> C12.
- Intelligence compounding / acceleration material -> C6.
- Structure debt / source-of-truth / operational surface material -> C10 and C22.
- Coherence, guardrail, and constitutional overhead material -> C8.
- Participatory intelligence material -> C20.

### Hold or rewrite before publication

Do not publish these as current engineering canon in their old form:

- `engineering/**/laws/*.md`
- `engineering/recursive-intelligence/laws/law-of-epistemic-acceleration-canonical.md`
- `engineering/recursive-intelligence/core-concepts/epistemic-escape-velocity.md`
- any file asserting formulas, thresholds, or law status without measured result.

They may be excerpted only as historical lineage or rewritten into conjecture form.

## Science publication decision

The science tree should publish as **measured results plus open research program**,
not as a mature science of laws.

### Publish now, with conjecture-status wrapper

These families can be public if they are clearly labeled as vocabulary, conjecture
lineage, or research-program material:

- Metric mirage and dashboard theater -> C11.
- Translation bottleneck -> C12.
- Structure debt -> C10.
- Friction-as-signal and friction-to-production language -> C2.
- Entropy/decay language -> only the C3a mechanical decay result is supported; the
  broader entropy/reinforcement theory remains open.
- Boundary/impedance language -> C5.
- Knowledge externalization, source-of-truth, and operational surface language ->
  C10/C22.

### Hold as not instrumented

Do not publish these as current science canon yet:

- `science/**/laws/*.md`, except as historical lineage to current conjectures.
- Thermodynamics, wave, oscillation, quantum, relativistic, field-dynamics, and
  impedance law suites in their formulaic form.
- Meta-cognitive architecture files using clinical, religious, political, or social
  system labels as explanatory architectures.
- Cognitive capacitance / breakthrough-cycle material until latent-holding telemetry
  exists.
- Any file whose main claim is a universal law, threshold, coefficient, escape
  velocity, or inevitable compounding dynamic.

The science tree has many publishable ideas, but most of them become real only when
presented as measurement-bound conjectures.

## Canon publication decision

The old `canon/` tree should not be published as current canon in its existing form.
It can be published only as one of:

1. **historical 2025 canon / lineage**;
2. **manifesto and field-framing**, clearly separated from empirical results;
3. **rewritten conjecture canon**, where each claim links to a current C-number,
   measurement procedure, gate, and result status.

### Publishable with strong wrapper

- Foundational field declarations can be excerpted as the origin story of ESE.
- The science/engineering distinction can be retained as organizing architecture.
- The field vocabulary can be retained where it does not assert measurement.

### Not publishable as current truth

- `canon/law-suites/*`
- consciousness scoring and five-threshold consciousness models;
- quantum/relativistic/thermodynamic/wave/oscillation law analogies;
- asserted constants or thresholds not fitted from data;
- self-reported platform metrics as validation.

This is the old corpus's main credibility boundary.

## First pass release shape

Recommended public v0:

1. **Empirical Results**
   - C1 refuted: return loop not closed as instrumented.
   - C3a supported: mechanical decay operates.
   - C4 supported: epistemic mass predicts drag/failure.

2. **Open Conjecture Register**
   - C1b-C23 with gates, blockers, and no premature verdicts.

3. **Engineering Doctrine**
   - Selected anti-patterns, diagnostics, and operator patterns from `engineering/`,
     explicitly labeled design doctrine.

4. **Lineage**
   - Carefully framed excerpts from `canon/` and `science/`, showing where each idea
     now lives in the empirical corpus or why it is held.

Do not release a book or site titled "laws of epistemic science" yet. Release a
truthful v0: **measured results, live conjectures, and engineering doctrine under
measurement**.

## Next evaluation pass

Starter file-by-file manifest:

- `applications/2026-06-20-publication-readiness-manifest.tsv`

It contains one row per audited source file and these columns:

- source path;
- old source type and epistemic status;
- proposed initial publication status;
- required edits;
- linked current conjecture/result;
- reason;
- risk markers.

The manifest is a first-pass triage, not final publication approval. No file should
enter a public bundle until its row has been manually reviewed and promoted to an
explicit release decision.
