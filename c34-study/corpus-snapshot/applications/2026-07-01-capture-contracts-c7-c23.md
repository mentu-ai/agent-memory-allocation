# Capture-contract register — verdict-blocked conjectures C7–C23 (2026-07-01)

Every conjecture C7–C23 is `status: operationalized`, `verdict: null` — the analysis logic exists (`analyses/<c>/analyze.py`) but no verdict can be rendered because the live Mentu instrument does not yet emit a required signal. This register states, for each, the **capture contract**: the specific signal the instrument must emit, where it should land, and how the analysis reads it back. It is the forward specification that turns each 'INSTRUMENT INSUFFICIENT' into a testable conjecture.

Compiled by the science harness (Claude Fable 5) from the frozen conjecture text, cross-checked against the live `cir.db` schema and `cir-run-outcomes.jsonl` fields. Contracts are specifications only — **nothing here is written into Mentu**; implementing a contract is engineering work, and each lands as an `instruments/` doc when built (see the existing `instruments/2026-06-19-c22-*.md` for the house pattern).

## ⚠️ Live-emission audit (2026-07-01, supersedes the blocker classification below)

A direct read of the live `cir.db` signals table (118 distinct signal kinds,
read-only) after the specs were drafted shows the **instrument is substantially
more built-out than the frozen conjecture text implied.** The per-conjecture
"required signal" and "current state" fields below were extracted from the
conjectures, which were written weeks earlier; several of the gaps they describe
have since been closed by emission. Corrected status:

| conj | contract status vs live emission | live evidence |
|---|---|---|
| C7 | **EMITS but does NOT JOIN** — corrected after running the live analysis | `handle_snapshot` (131,299) + `handle_return_event` (2) + `handle_use_event` (59) all emit, BUT the existing `analyze.py` reports **matched handles 0, orphans 61** — the return/use events do not join to any snapshot by `handle_id`, and the first-seen feature gate FAILs. Readiness `data_insufficient`. Real gap: a **join key** between return/use events and the first-seen snapshot, plus far more return volume. Not "satisfied" — see correction note. |
| C22 | **EMITS; analysis needs a doc tree I can't reach** — partly verified | `operational_surface_snapshot` (687), `operational_surface_observation` (312), `operational_surface_event` (1) confirmed in live `cir.db`. The existing `analyze.py` additionally scans a source-doc tree (`Workspaces/mentu-physics/...`) outside my grant, so I could not run its verdict path end-to-end. Emission is real; the matched-cohort + 8-week window remains the accrual gate. |
| C14 | **emitting** — contract/gate telemetry live | `step_contract` (192), `semantic_gate_eval` (148), `gate_decision`/`gate_submission` (15 each). Data accrual. |
| C9, C15, C18, C19, C20, C23 | **PARTIAL** — the signal kind emits but at small n or lacks one label | `pattern` (1,847), `compilation` (10), `file_snapshot` (464), `ratchet` (26)+`evolve_regression` (13), `approval` (3), `review_commit` (5). Mostly data-accrual + one missing sub-field. |
| C10, C13, C16, C17, C21 | **CHECK** — likely computable from existing fields | `content_digest`/`semantic_hash` on snapshots; `embedding` (2,967); `relations` (41,633, typed cites/corrects/refines/synthesizes); `relevance_verdict` (74). |
| **C11** | **GENUINELY MISSING (code gap)** — no measurement→action closure edge | `relations` has only `cites`/`corrects`/`refines`/`synthesizes`; no `measurement-caused-action` / `action-resolved-measurement` edge type. This is the one real, bounded engineering gap. See C11 note below. |
| C12 | **BLOCKED on C1b return** — no code fills it until return happens | `trust_events` reuse (`context_used`) = 24 lifetime. |

**Bottom line:** the dominant blocker across C7–C23 is **data accrual, not missing
instrumentation.** Most conjectures cannot render a verdict yet because the
relevant signals are too few (returns, reviews, compilations, approvals) or the
pre-registered observation window/cohort has not elapsed — not because the
engine fails to emit. Building more emission would add fields no analysis can yet
consume. The one contract that is a true code gap is **C11** (a measurement→action
closure relation type); every other unblock is either "wait for runs" or "write
the dormant `analyze.py` against signals that already exist."

### Correction: the existing `analyze.py` files already consume these signals

C7–C23 each already have an `analyze.py` + `test_analyze.py` (uncommitted working-
tree work). Running them read-only against live data (`MENTU_CIR_DB` / HOME shim
to the granted mount) shows they are **already wired to the live signal kinds** —
they are not stubs waiting to be written. So the useful action was **not** to
author new dormant analyses (that would duplicate existing work) but to run them
and record what they report:

- **C7**: runs; readiness **`data_insufficient`**. Strict CIR rows: exposures
  131,299; **return events 2; use events 59; matched handles 0; orphans 61.**
  The first-seen feature gate FAILs ("ledger lacks predictor snapshots"). So the
  real C7 gap is sharper than "add a snapshot" — the snapshots exist in bulk, but
  the return/use events **do not join to them by `handle_id`** (0 matched, 61
  orphaned), and the minimum substrate gate (≥5,000 query-derived handles, ≥20-day
  span) is not met. Corrected blocker: **missing join key + accrual**, not
  first-seen-snapshot-absent.
- **C22**: its `analyze.py` reads the live `operational_surface_*` signals (687/
  312/1, confirmed) but also scans a markdown source tree under
  `Workspaces/mentu-physics/…` that is outside the harness's host grant, so its
  full verdict path could not be run here. Emission verified; verdict run deferred
  to an environment with that grant.

This is why no new `analyze.py` was written for C7/C22 this pass: the analyses
exist and are correct; the blockers are join/accrual/access, not authoring.

### C7 join bug found and fixed; other analyses scanned for the same class

Running C7's analysis exposed a real bug — **in the epistemics `analyze.py`, not
the engine.** `handle_return_event`/`handle_use_event` emit a *plural* `handle_ids`
list (one event surfaces several handles), but the join read only the *singular*
`handle_id` and fell back to `signal_id`, so every outcome was orphaned (matched
0). Fixed by expanding the list; live result went `data_insufficient → ready`.
Distinct matched handles rose **0 → 52**, and orphaned outcome rows dropped
**61 → 7** (these are different units — matched *handles* vs orphan outcome
*rows* — so they do not sum; the 7 remaining orphans are zero-padded test IDs).
A regression test using the real plural shape was added (the existing fixtures
used the singular shape, which is why the suite never caught it); it fails on the
old code and passes on the fix. The fix and its test are committed directly in
`analyses/c7-handle-mediated-returnability/` (the change lives in the tracked
`analyze.py`); a standalone diff was also archived as the `c7-analyze-join-fix.patch`
workspace artifact for reference.

**Scan of the other signal-joining analyses for the same silent-zero pattern
(all read-only against live `cir.db`):**

| conj | join | verdict |
|---|---|---|
| C9 | pattern `mem_*` ids ∩ run-outcome id-arrays | **CLEAN.** Field names correct, arrays non-empty; intersection is a *true* 0 — none of 1,846 crystallized patterns has ever been injected/used in a run. That is the real finding (patterns crystallize but never return), not a bug. Honest INSTRUMENT INSUFFICIENT. |
| C10 | signals→outcomes by `run_id` | **CLEAN.** Join lands at 86.7% (842/971). Gate fails only on span (<56 days). |
| C14 | measurement-kind counts | **CLEAN.** Correct kinds (`semantic_gate_eval` 148, `gate_decision` 15); honest NOT-READY on contract fields. |
| C21 | `relations` table | **CLEAN join**, but errors later scanning a markdown source tree outside the harness host grant (same access limit as C22). |
| C23 | `run_id` sets over sequence history + outcomes | **CLEAN.** Joins land (5,777 total sequence-history rows, of which 2,585 terminal; 833 unique runs); honest FAIL on `review_commit ≥ 200` (only 5). |

**Conclusion:** C7 was the only silent-zero join defect. Every other analysis
either joins correctly (and its "insufficient" is a genuine accrual gate) or is
limited by a source-doc grant, not by a coding error.

## Original ground-truth check (from spec drafting; partially superseded above)

- `cir.db` `signals` **has** a `run_id` column (the C22 run-id capture bridge landed). (The claim that snapshot/observation event-types are absent is **corrected above** — they emit: 687/312 rows.)
- `cir-run-outcomes.jsonl` carries **aggregate** exposure per run (`injected_signal_ids`, `used_signal_ids`, `selected_signal_count`, `missing_footer_count`, `use_rate`, …); per-handle first-seen attribution instead lives in `handle_snapshot` signals (see above), not the outcomes file.
- `trust_events` is dominated by `initial_computation` (199,123); genuine reuse events (`context_used`) number 24 — the return-dependent contracts (C9, C12) cannot fill until C1b makes return happen.

## Blocker-type summary

| blocker type | conjectures |
|---|---|
| missing-field | C9, C10, C11, C14, C18 |
| missing-event-type | C13, C15, C22, C23 |
| first-seen-snapshot-needed | C7 |
| missing-join-key | C8 |
| depends-on-C1b-return | C12 |
| missing-event-type, missing-join-key, first-seen-snapshot-needed | C16 |
| missing-field, missing-event-type | C17 |
| missing-event-type, missing-field, missing-join-key | C19 |
| missing-field, missing-event-type, missing-join-key, first-seen-snapshot-needed | C20 |
| missing-event-type; missing-field | C21 |

_Several conjectures are additionally downstream of **C1b return**: C12's primary blocker is depends-on-C1b-return, and C9 (listed under missing-field) also depends on C1b — their signals only populate once distilled return actually occurs, so C1b is their true unblock, not a new field. See each conjecture's "Downstream dependency" below._

## Capture contracts

### C7 — handle-mediated returnability

- **Measured quantity**: Whether handles with richer metadata (parents, projectID, domain, tags, summary) predict later reuse as parents, in queries, or in derived compositions.
- **Required signal**: First-seen snapshot of predictor fields (parents, projectID, registrableDomain, tags, body.summary) at or near handle creation, timestamped before any mutations.
- **Where written**: New snapshot store: lacs/snapshots/predictor-at-creation.jsonl, keyed by handle_id and creation_timestamp, or as ledger event type 'snapshot-predictor'.
- **How read back**: Join snapshot by handle_id to ledger outcome events (lineage-return, query-return, composition-return) after creation cutoff; filter ledger by operation timestamp >= snapshot timestamp.
- **Current state**: Live LACS has 8,760 mutable handle.json files and append-only ledger with 67,956 rows. Ledger lacks event timestamps on index rows (by-parent, by-tag, by-domain). No first-seen snapshot exists; current handle JSON reflects post-capture mutations.
- **Downstream dependency**: none
- **Blocker type**: first-seen-snapshot-needed

### C8 — coherence dividend

- **Measured quantity**: Whether recipes with higher coherence load (more guardrails, verification, gates) exhibit lower repeat-failure rates and better step success ratios after maturity, controlling for step count and recipe family.
- **Required signal**: recipe_manifest_hash or immutable run-bundle hash linking each run outcome in cir-run-outcomes.jsonl to its exact manifest version at execution time.
- **Where written**: cir-run-outcomes.jsonl as an additional field on each run-outcome row, or a join table keyed by run_id.
- **How read back**: Join run outcomes to recipe manifests by hash to compute coherence load (footprint contract, verify_requirements, semantic_assertion, gates, dependencies) as static predictor; correlate against duration, cost, steps_ok/steps_total, repeat failures within seven days.
- **Current state**: 629 run rows, 168 recipes, 33.1 days span exist and pass size/span gates. Manifest identity gate fails at 0.0%: run outcomes lack recipe_manifest_hash, immutable bundle hash, or reconstructable version. Analysis blocked.
- **Downstream dependency**: C2 (friction week), C4 (recipe mass) for control variables; no hard blocker conjecture dependency.
- **Blocker type**: missing-join-key

### C9 — pattern crystallization utility

- **Measured quantity**: Whether crystallized pattern signals are selected, injected, and used in later runs with measurable utility gains over raw source signal exposure.
- **Required signal**: Pattern id in `injected_signal_ids` or equivalent pattern-exposure field; pattern id in `used_signal_ids` or successor measured-use field in cir-run-outcomes.jsonl.
- **Where written**: cir-run-outcomes.jsonl: `injected_signal_ids` and `used_signal_ids` arrays must explicitly record crystallized pattern ids; cir.db: `signals` rows with `op='crystallize'` must have downstream relation/exposure signals.
- **How read back**: Join cir-run-outcomes.jsonl runs by pattern id presence in `injected_signal_ids` and `used_signal_ids`; correlate with pattern maturity and source cluster metadata from cir.db `signals` rows.
- **Current state**: 6,214 certified patterns created with valid source_ids; zero pattern ids appear in run outcome injection/use arrays. Pattern exposure and measured-use gates not cleared.
- **Downstream dependency**: C1b: footer/usage attribution must distinguish non-use from non-observation to enable pattern-use measurement.
- **Blocker type**: missing-field

### C10 — structure debt

- **Measured quantity**: Association between structural identity debt (missing/ambiguous workspace, placeholder labels, missing recipe manifest hash) and operational outcomes (success rate, step ratio, closure latency, repeat failures).
- **Required signal**: Workspace identity field, recipe_manifest_hash or equivalent immutable recipe identifier, coordination/handoff event records for cross-workspace runs in signals table.
- **Where written**: cir-run-outcomes.jsonl (recipe manifest identity fields); cir.db signals table (workspace, coordination/handoff records); analyses/c10-structure-debt/identity_rules.json (frozen rules).
- **How read back**: Join cir-run-outcomes by run_id to signals.run_id; group by (workspace, week) for primary unit; apply frozen identity rules to classify debt; correlate debt index with success, steps_ok/steps_total, closure latency.
- **Current state**: cir-run-outcomes.jsonl and cir.db signals exist with run_id, workspace, recipe, success, steps; missing: recipe_manifest_hash or recipe_version_hash fields; missing: explicit coordination/handoff signals for cross-workspace work.
- **Downstream dependency**: C2 (friction surfaces), C5 (boundary impedance), C8 (coherence load); C10 gate requires C2 available; C4 (recipe manifest identity) prerequisite for recipe_manifest_hash.
- **Blocker type**: missing-field

### C11 — measurement–action closure

- **Measured quantity**: Whether measurement events that close into explicit causal relations to downstream actions show lower recurrence, shorter closure latency, and better reliability than measurements without traceable response contracts.
- **Required signal**: Explicit closure relation type or signal-body field in cir.db relations table indicating measurement caused/responded to/resolved/escalated action; one of: measurement-caused-action, action-responded-to-measurement, action-resolved-measurement, action-escalated-measurement.
- **Where written**: cir.db relations table with source_id (measurement signal), target_id (action event), relation_type (closure edge type), or extended signals.body field with closure_relation metadata.
- **How read back**: Join signals.run_id to relations.source_id (measurement) and target_id (action event); filter by explicit closure relation_type before computing latency and recurrence by measurement_family and recipe_family.
- **Current state**: cir.db signals and relations exist; measurement events (semantic_gate_eval, verdict, etc.) and action proxies (git_commit, step_closure, etc.) are logged. No explicit causal closure edge field or relation type documenting measurement→action causation exists yet.
- **Downstream dependency**: C2 (friction surface) and C10 (structure debt) required as controls; verdict blocked until both available for same window.
- **Blocker type**: missing-field

> **C11 is the one genuine code gap (verified against live `cir.db`, 2026-07-01).**
> The `relations` table is free-form TEXT `relation_type` (no schema migration
> needed) and already carries a rich vocabulary in engine code —
> `cites, corrects, refines, synthesizes, supports, extends, contradicts,
> questions, implements, supersedes`. What is absent is any **measurement→action
> closure edge**: nothing links a measurement signal (`verdict`,
> `semantic_gate_eval`, `relevance_verdict`, `contradiction`) to the action it
> triggered (`git_commit`, `step_closure`, `correction`, `submission`).
>
> **Why this is not implemented blind here:** emitting a closure edge requires
> deciding *when* a measurement "caused" an action — a run-flow semantics
> decision. Writing edges on a wrong heuristic pollutes a 41k-row relations table
> that other conjectures (C21) read. The clean path is a **narrow, explicit
> rule**: when a step's own contract/gate produces a measurement AND that same
> step closes with an action in the same `run_id` within the step boundary, emit
> `relation_type = "measurement-closed-by-action"` with `source_id` = measurement
> signal, `target_id` = action signal, `strength` = 1.0. Same-step, same-run only
> — no cross-step inference. This is bounded, testable (the engine already builds
> and its test suite runs green here), and additive (new type value, existing
> column). It is the recommended first engine capture-contract to implement, but
> it needs a decision on the exact trigger step before code lands — flagged for
> the maintainer rather than guessed.

### C12 — translation bottleneck

- **Measured quantity**: Whether attrition across the selection-injection-brief-use-attribution chain predicts lower run reliability, reuse success, and fewer downstream corrections.
- **Required signal**: Translation-stage event sequence: selected_signal_count, injected_count, read_count, missing_footer_count, used_count, invalid_used_count, unproven_signal_ids per run_id.
- **Where written**: ~/.mentu/training/cir-run-outcomes.jsonl, extended with per-stage transition flags and debt component markers.
- **How read back**: Join by run_id; compute debt subsets (selected-not-injected, injected-not-used, missing-footer, invalid-used); stratify outcome comparison by debt presence.
- **Current state**: Fields selected_signal_count through unproven_signal_ids exist in cir-run-outcomes.jsonl. Gap: post-footer-fix C1b randomized window (300+ rows) and 8-week maturity not yet available; C5 boundary classes and C10 structure debt controls incomplete.
- **Downstream dependency**: C1b (footer instrumentation fix), C5 (boundary-impedance classification), C10 (structure debt identity control).
- **Blocker type**: depends-on-C1b-return

### C13 — semantic redundancy resilience

- **Measured quantity**: Success rate of artifact retrieval and reuse when one or more identity surfaces are missing, corrupted, or ambiguous, controlling for artifact type, age, domain, and workflow maturity.
- **Required signal**: First-seen artifact snapshots (path, filename, frontmatter, handle references, schema references, node references, relationships, content hash) and reuse/recovery events (retrieval attempts, citations, derivations, validation results, repair actions).
- **Where written**: CIR/LACS artifact lifecycle store with dual tables: artifacts-first-seen (immutable snapshot at capture) and artifacts-reuse-events (timestamped retrieval, citation, derivation, and recovery outcomes).
- **How read back**: Join reuse-events to first-seen by artifact_id; compute redundancy score from first-seen snapshot before analyzing outcome association; stratify by control variables (type, age, domain, cohort).
- **Current state**: Source architecture documents exist; blueprint/heap/ is readable. Missing: automated first-seen snapshots from live Mentu/CIR captures, post-snapshot reuse event logs, and partial-information retrieval trials. Readiness inventory possible; verdict blocked on 500+ artifacts + 8 weeks history.
- **Downstream dependency**: C7 handle richness, C10 structure debt, C12 translation-stage identity loss (required as controls; C13 verdict depends on their availability).
- **Blocker type**: missing-event-type

### C14 — measurement-contract validity

- **Measured quantity**: Whether measurement events with explicit contracts (subject, method, value, unit/scale, uncertainty, evidence, calibration, verification) produce lower correction rates and better downstream reliability than weak-contract measurements.
- **Required signal**: Contract component metadata in signals: explicit unit/scale field, separate uncertainty/tolerance/confidence value, calibration/reference standard name, evidence_ids/trust_chain presence, verification_state beyond label.
- **Where written**: cir.db signals table: new columns for unit_scale, uncertainty_margin, calibration_reference, or enriched signals.body JSON with contract_components object.
- **How read back**: Per-signal contract score (0–8 points, one per component); join signals to later correction/verdict rows by run_id and signal timestamp; compare correction rates by contract strength tier.
- **Current state**: CIR substrate has confidence values, verification labels, evidence_ids, trust_chain, hash lineage. Missing: explicit unit/scale metadata (50 events needed), uncertainty/tolerance budgets (100 events), calibration/reference standards (10 events).
- **Downstream dependency**: None stated; orthogonal to C2, C10, C11 but uses them as controls.
- **Blocker type**: missing-field

### C15 — compiler-invocation readiness

- **Measured quantity**: Whether artifacts with explicit compiler-invocation contracts (Stage 0/1/2+ frontmatter) have higher parse success, validation success, reuse frequency, and composition success than artifacts without such contracts.
- **Required signal**: First-seen artifact snapshots with parsed frontmatter/YAML payload; compiler validation logs (parse result, schema validation, missing-field reports); reuse/composition logs (later references by id, successful relationship traversal, corrections attributed to identity/trust/function ambiguity).
- **Where written**: First-seen snapshots in artifact metadata store (e.g., artifacts.db or artifact-snapshots.jsonl); compiler validation outcomes in compiler-logs.jsonl; reuse/composition events in relationship-resolution.jsonl or composition-logs.jsonl.
- **How read back**: Join first-seen snapshots to compiler logs by artifact_id/path; join reuse/composition logs by artifact_id to track later references and correction events; stratify by readiness_stage (0, 1, 2, 3) at first observation.
- **Current state**: Design specification and examples exist in audited legacy files (epistemic-matter.md, YAML-Design-Principles.md, constitutional-compiler.md, Compiler-Style-Guide.md). Live Mentu instrument does not yet emit first-seen artifact snapshots with frozen stage-field scoring, compiler validation logs with structured parse/validation outcomes, or reuse/composition logs with orphan-reference and correction events.
- **Downstream dependency**: C7 (handle richness), C13 (semantic redundancy), C14 (measurement-contract score); C15 verdict requires controls for all three to isolate distinct compiler-readiness effect.
- **Blocker type**: missing-event-type

### C16 — conditional activation selectivity

- **Measured quantity**: Whether conditional activation of epistemic primitives produces higher use rates, fewer irrelevant injections, and lower correction rates than retrieval-only activation, controlling for retrieval score and artifact properties.
- **Required signal**: Candidate-level activation decision logs: candidate_id, condition_id, condition_type, evaluation result (true/false/unknown/error), activation decision (activate/skip/defer/escalate), plus linkage to run outcomes and use/correction telemetry.
- **Where written**: ~/.mentu/training/cir-run-outcomes.jsonl extended with candidate-level records; CIR signals table with activation decision relations.
- **How read back**: Join activation decisions to injected_signal_ids and use footers by candidate_id and run_id; match skipped candidates to missed-relevance or correction events by run/context.
- **Current state**: Aggregate fields exist (selected_signal_count, injected_count, used_count, context_helped). Candidate-level condition evaluations, skipped/deferred decisions, and missed-relevance telemetry for skipped candidates do not exist.
- **Downstream dependency**: C7 (handle richness), C13 (semantic redundancy), C15 (compiler readiness) required as controls; verdict blocked until these are available.
- **Blocker type**: missing-event-type, missing-join-key, first-seen-snapshot-needed

### C17 — schema-portable CIR processing

- **Measured quantity**: Whether schema-portable CIR processing achieves higher coverage, lower cost-per-accepted-record, and measurable downstream utility across heterogeneous repositories compared to ad hoc or bespoke processing.
- **Required signal**: Per-file processing manifest: schema_id, status, skip_reason, duration, tokens, cost, validation_status, embedding_status, output_artifact_id; downstream retrieval/use/correction events linked to produced records.
- **Where written**: cir-run-outcomes.jsonl extended with per-file rows; new signals table or nested array for batch-level manifests and downstream outcome linkage.
- **How read back**: Join by batch_id and file_path to aggregate coverage and cost denominators; join produced artifact_id to downstream use/retrieval events; group by schema_id, file_type, repo_id for stratified analysis.
- **Current state**: Run-level cost and file_snapshot signals exist in cir-run-outcomes.jsonl; per-file manifest (status, skip reason, cost, validation, artifact id) missing; downstream retrieval/use outcomes not yet instrumented.
- **Downstream dependency**: C13 (semantic redundancy scoring) and C15 (compiler readiness) required for produced artifact quality evaluation; no dependency on other conjectures for gate.
- **Blocker type**: missing-field, missing-event-type

### C18 — intent-density capture advantage

- **Measured quantity**: Downstream utility and acceptance rate of captured records stratified by intent-density level, controlling for modality, processing cost, privacy burden, and handle/semantic richness.
- **Required signal**: Per-capture event record with modality, intent_level, consent_scope, quality_fidelity_metrics, produced_signal_ids, and linked outcomes (selection, injection, read/use, correction, deletion, privacy_objection).
- **Where written**: cir-run-outcomes.jsonl extended with capture_id, modality, intent_level, fidelity scores, and outcome_link references; or new capture-outcomes.jsonl with same schema.
- **How read back**: Join by capture_id to downstream selection and run-context injection events; aggregate by intent_level and modality; compute accepted-record rate and later-use rate per cohort and control group.
- **Current state**: Capture archives exist in ~/.mentu/cir-pending-archive/*capture*.jsonl; file_snapshot and document signals exist; cir-run-outcomes.jsonl logs aggregate selects/injects. Missing: per-capture intent_level labels, modality, quality metrics, consent scope, and explicit links to later read/use, correction, or privacy outcomes.
- **Downstream dependency**: C7 (handle richness), C13 (semantic redundancy), C15 (compiler invocation readiness), C16 (conditional activation selectivity) — used as controls, not blocking prerequisites.
- **Blocker type**: missing-field

### C19 — governed-evolution stability

- **Measured quantity**: Whether knowledge-module changes with explicit governance metadata (boundaries, assumptions, relationships, maturity, tensions, validation, feedback) produce lower drift/revert rates and higher downstream utility than matched unguided changes.
- **Required signal**: change_id, artifact_id, change_type, pre/post hashes, declared boundary/assumption/relationship/interface deltas, maturity dimension scores, governance_mode, tension labels, validation_gates, feedback_loops, authority_path, rollback_plan for each versioned knowledge-module change event.
- **Where written**: New table/document store: change-governance-events or cir.db governance_changes table, linked by artifact_id and change_id to artifacts and post-change outcomes.
- **How read back**: Join change_id to artifact_id; match governed vs. unguided changes by artifact type, size, change_type, and workspace; link outcome window (semantic gate, verify/build/test, correction/revert/drift) by artifact_id and timestamp post-change.
- **Current state**: Git history records diffs but lacks governance labels. CIR has recipe_version and step_contract but not knowledge-module change envelopes. cir-run-outcomes.jsonl records runs unlinked to governed changes. Conjecture corpus has frontmatter but no maturity/tension/governance metadata per change event.
- **Downstream dependency**: Depends on C7 (handle richness), C10 (structure debt), C13 (semantic redundancy), C15 (compiler readiness), C16 (activation selectivity), C17 (schema portability) as controls; requires outcome linkage.
- **Blocker type**: missing-event-type, missing-field, missing-join-key

### C20 — participatory alignment yield

- **Measured quantity**: Human participation at explicit semantic boundaries improves alignment, correction rates, trust calibration, and downstream utility per unit of human attention compared with autonomous or ad hoc execution.
- **Required signal**: participation_contract events with participation_id, run_id, trigger_source, candidate_options, human_action, attention_cost, semantic_state_before/after, downstream_outcome, correction/revert status, and trust_update.
- **Where written**: ~/.mentu/training/participation-contracts.jsonl or extended cir-run-outcomes.jsonl with participation_contract record type and outcome linkage.
- **How read back**: Join participation_contract.run_id to execution outcome; group by trigger_source and participation_type; correlate attention_cost with correction_rate and utility_outcome; stratify by C7/C13/C15/C16/C19 control scores.
- **Current state**: CIR has approval, correction, semantic_gate_eval kinds but not first-class participation contracts, semantic handshakes/diffs, lineage patches, attention budgets, or participation-to-outcome linkage. approvals.json records approvals without triggers or downstream tracking. cir-run-outcomes.jsonl has outcomes but no participation decision linkage.
- **Downstream dependency**: C7 (handle richness), C13 (semantic redundancy), C15 (compiler readiness), C16 (conditional selectivity), C19 (governed evolution) as control variables; C1/C9/C17 (CIR memory).
- **Blocker type**: missing-field, missing-event-type, missing-join-key, first-seen-snapshot-needed

### C21 — typed context-network yield

- **Measured quantity**: Association between typed context-network relationship completeness (0–5 scale) and downstream navigation success, composition utility, transfer outcomes, and correction rates after controlling for artifact quality factors.
- **Required signal**: exposure event: artifact_id, module_id, candidate_relationship_ids shown; selected_relationship_id or skip; downstream outcome within 4 weeks: navigation_success, context_selection_used, read/cite/reuse, composition_attempt, correction/revert, search_rework_time saved.
- **Where written**: cir-run-outcomes.jsonl extended with relationship_exposure records; cir.db relations table extended with completeness_score, quality_rating, context_dependency, interaction_guidance, topology_metrics, and relationship_source.
- **How read back**: Join exposure.selected_relationship_id to relations.id; group by relationship_type and completeness_score; link to outcome within artifact_id and 4-week follow-up window; cohort matched untyped citations separately.
- **Current state**: cir.db relations table exists with typed edges (cites, extends dominant); lineage and C-numbers in epistemics corpus but no relationship metadata envelopes. cir-run-outcomes.jsonl logs run outcomes; no exposure denominators, skipped-edge logging, or outcome linkage to specific relationship traversals.
- **Downstream dependency**: C7, C13, C15, C16, C19 (control covariates); no conjecture dependency.
- **Blocker type**: missing-event-type; missing-field (completeness_score, quality_rating, context_dependency, interaction_guidance, topology_metrics, relationship_source on relations; exposure event structure on outcomes; outcome linkage keys).

### C22 — operational surface debt

- **Measured quantity**: Association between operational-surface-debt score (fragmentation, source-of-truth clarity, integration ownership, observability) and workflow failure, rework, delay, cost, stale status, and trust loss after complexity/run-class controls.
- **Required signal**: operational_surface_snapshot (run/workflow start: tool inventory, source-of-truth map, handoff count, integration ownership, observability, fragmentation class, debt score) and operational_surface_observation (step-exit: interface/dashboard/spreadsheet evidence, manual-reconciliation markers) linked by run_id to tool_failure and step_result events; matched cohorts with 300+ high-fragmentation and 300+ contract-mapped workflows.
- **Where written**: ~/.mentu/cir.db signals table: operational_surface_snapshot.v1 and operational_surface_observation.v1 rows; cir-run-outcomes.jsonl enriched with surface-debt score and outcome linkage per run_id; matched-cohort manifest and diagnostic findings in analyses/c22-operational-surface-debt/.
- **How read back**: Join operational_surface_snapshot to cir-run-outcomes.jsonl by run_id; group tool_failure/step_result events by run_id and link to snapshot exposure; stratify by fragmentation class and source-of-truth clarity; control for C10/C11/C16/C19/C21 confounders.
- **Current state**: Snapshot and observation schemas frozen (v1); run-id capture bridge deployed; tool-failure rows exist but NOT yet joined to run outcomes by run_id. Zero live post-instrumentation exposure snapshots, surface inventories, manual-handoff counts, diagnostic findings, or matched cohorts. No surface-to-outcome causal linkage or follow-up data.
- **Downstream dependency**: C10 (structure-debt identity/schema/run boundaries), C11 (measurement-action closure), C16 (conditional activation selectivity), C19 (governed-evolution), C21 (typed context-network quality) — all required as controls.
- **Blocker type**: missing-event-type (no live operational_surface_snapshot/observation emissions yet; tool_failure rows lack run_id join key to run outcomes; no matched cohorts, diagnostic sample, or 8-week follow-up data collected)

### C23 — review-trust calibration

- **Measured quantity**: Whether reviewer ratings on sequence runs predict later same-recipe success or failure better than mechanical step-success baselines alone.
- **Required signal**: review_commit signal with run_id, recipe, rating [0,1], verdict, rubric scores, error tags, citations, submitted timestamp, and explicit target_run_id.
- **Where written**: CIR signals.kind=review_commit as JSON records; linked to cir-run-outcomes.jsonl by run_id and later same-recipe terminal outcomes.
- **How read back**: Join review_commit by run_id to sequence terminal records; match reviewed run to later same-recipe run outcomes within 4-week windows; aggregate by recipe and run class.
- **Current state**: Run-outcome substrate and trust-state substrates exist; review-commit stream and canonical sequence-history writer not yet verdict-grade. Schema incomplete.
- **Downstream dependency**: C14 (measurement contract), C16 (activation selectivity), C20 (participation contract), C22 (operational surface debt).
- **Blocker type**: missing-event-type

## How to use this register

1. Pick a contract whose blocker is a **missing-field** or **missing-join-key** — these are the cheapest to implement (extend an existing emit path) and unblock the most conjectures per unit work.
2. Implement the emit in the engine, land it as an `instruments/<date>-<c>-*.md` doc following the `Purpose / Implementation / Verification / Scientific Status` pattern.
3. Once the signal is live and accruing, write the conjecture's gate-triggered `analyze.py` verdict path (dormant until enough data), exactly as done for C1b and C3.
4. Defer the **depends-on-C1b-return** contracts (C9, C12) until C1b return is actually happening — no instrument change will fill them sooner.

_Specifications only. No live `.mentu` data and no Mentu source were modified to produce this register._