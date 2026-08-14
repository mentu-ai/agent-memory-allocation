---
id: c22
name: operational-surface-debt
status: operationalized
lineage:
  - Workspaces/mentu-physics/foundational/blueprint/ese/engineering/
verdict: null
---

# C22 - Operational surface debt

## Claim

Operational workflows spread across fragmented tools, dashboards, spreadsheets,
manual handoffs, and ambiguous sources of truth should incur higher failure,
rework, delay, onboarding cost, and trust loss than comparable workflows with
explicit operational-surface architecture: canonical records, mapped tool
dependencies, externalized logic, visible workflow state, and decision-linked
interfaces.

The claim is not that fewer tools are always better. It predicts that ungoverned
surface proliferation is costly when the workflow lacks source-of-truth boundaries,
integration ownership, failure visibility, and handoff discipline. A multi-tool
system with clear contracts, redundancy, and observability may outperform a
nominally consolidated system that hides complexity or overloads a single surface.

## Origin

The engineering corpus contains a coherent failure/remedy pair. The failure side is
named through Tool Zoo, Excessive Tooling Complexity, Spreadsheet Factory,
Operational Fog, Decorated Fragility, Tool Collapse Map, Toolification, and
Interface Illusion Audit. The remedy side appears in Source-of-Truth Architecture,
Workflow Assembly Line, Layer-Maturity Grid, System Autopsy, and Adaptive Engine.

C22 keeps the measurable residue: operational surfaces can be inventoried, mapped,
and linked to workflow outcomes. It does not admit a general anti-SaaS position, a
claim that dashboards are bad, or a claim that consolidation is intrinsically wise.

## Operationalization

**Datasets**:

- Future operational-surface exposure records:
  - `workflow_id`, `run_id`, `surface_snapshot_id`;
  - tool/interface/dashboard/spreadsheet/status surface inventory;
  - canonical record and source-of-truth map;
  - handoff count, manual copy/reconciliation count, integration count;
  - business-logic location: code, config, spreadsheet, prompt, person, document;
  - integration ownership, fallback path, observability, and error handling;
  - status visibility and freshness at each workflow stage;
  - surface maturity by Data, Logic, Interface, Orchestration, and Feedback layers;
  - tool-collapse-map outputs and interface-illusion findings;
  - whether the workflow is fragmented, consolidated, or contract-mapped multi-tool.
- Current partial surfaces:
  - `~/.mentu/cir.db` has `tool_failure`, `step_result`, and related run signals.
  - `~/.mentu/training/cir-run-outcomes.jsonl` has run outcomes, warnings, duration,
    cost, and run ids.
  - The engineering source tree has the conceptual vocabulary for failure modes and
    remedy patterns, but not verdict-grade exposure telemetry.

**Predeclared predictor**:

Operational-surface-debt score at workflow start:

- `0`: single or multi-surface workflow with canonical source of truth, explicit
  contracts, visible state, owned integrations, and fallback paths.
- `1`: minor fragmentation; tool boundaries are known and most state is visible.
- `2`: multiple surfaces and some manual handoffs, but canonical records and
  workflow ownership are mostly clear.
- `3`: repeated manual reconciliation, dashboard/interface uncertainty, weak
  integration ownership, or partially hidden business logic.
- `4`: tool zoo or spreadsheet-factory pattern: ambiguous source of truth, many
  manual moves, brittle integrations, and hero-dependent maintenance.
- `5`: operational fog or decorated fragility: critical status/logic lives in
  people's heads, dashboards hide uncertainty, failures are detected late, and
  collapse paths are unmapped.

**Outcomes**:

- workflow success/failure;
- tool failure, integration failure, timeout, retry, or fallback use;
- step warnings and failed auto-commit or verification gates;
- elapsed duration and cost;
- manual reconciliation, correction, revert, and duplicate-entry events;
- stale or conflicting status/source-of-truth observations;
- onboarding/recovery time after a key person or tool is unavailable;
- downstream trust/use of interfaces and dashboards;
- post-incident recurrence after a System Autopsy or similar diagnostic.

**Controls**:

- workflow size, step count, run class, workspace, and task type;
- baseline complexity and change frequency;
- C10 structure-debt controls for identity/schema/run boundaries;
- C11 measurement-action closure, because dashboards only matter if they route to
  response;
- C16 conditional activation selectivity, because irrelevant surface activation can
  masquerade as tool debt;
- C19 governed-evolution completeness for change windows;
- C21 typed context-network quality where relationships guide navigation or
  composition.

## Predictions (stated 2026-06-19, before C22 verdict analysis)

- **P1**: Higher operational-surface-debt scores will predict more `tool_failure`,
  warnings, failed steps, longer duration, and higher cost after size and run-class
  controls.
- **P2**: Source-of-truth clarity and visible workflow state will reduce rework and
  stale/conflicting status observations, especially in multi-tool workflows.
- **P3**: Dashboard/interface sophistication will help only when connected to fresh
  data, explicit business logic, and action paths; otherwise it will predict
  interface-illusion or decorated-fragility outcomes.
- **P4**: Hero-dependent workflows will be more brittle under key-person absence,
  retry, or tool-collapse simulations than workflows with documented ownership and
  fallback paths.
- **P5**: The relationship between tool count and outcome will be non-linear:
  contract-mapped multi-tool workflows can outperform over-consolidated or hidden
  single-surface workflows.

## Falsification criteria

- Operational-surface-debt score has no positive association with failure, rework,
  delay, cost, stale status, or trust loss after controls -> **refuted**.
- Tool count alone explains outcomes as well as the richer surface-debt score ->
  **revised** toward a simpler tool-count/complexity claim.
- Consolidated workflows perform no better, or worse, than matched fragmented
  workflows after source-of-truth, ownership, and observability controls ->
  **revised** toward contract quality rather than consolidation.
- A verdict that excludes failed workflows, skipped/fallback tool paths, invisible
  manual handoffs, or stale dashboard/status observations is invalid.

## Gate

C22 may produce a verdict only when all are true:

- scoring rules are frozen before outcome modeling;
- at least 1,000 workflow or run exposures have per-run operational-surface
  inventories;
- at least 300 high-fragmentation and 300 contract-mapped or consolidated workflows
  exist as matched comparison cohorts;
- exposure records include tool/interface/dashboard/spreadsheet inventory, source of
  truth, handoff count, manual reconciliation count, integration ownership, fallback
  path, observability, and status freshness;
- at least 200 failure/rework/stale-status/correction outcomes are linked to prior
  surface snapshots;
- tool-collapse and interface-illusion diagnostics are recorded for a representative
  sample, including negative findings;
- at least 8 weeks of follow-up exist;
- C10/C11/C16/C19/C21 controls are computable for exposed workflows.

Current data has tool-failure signals and run outcomes, but tool-failure rows are not
yet linked to run outcomes by run id. The C22 score rules are now frozen, but there
are still no live post-instrumentation exposure rows, source-of-truth freshness
records, manual-handoff denominators, diagnostic findings, matched cohorts, or
surface-to-outcome causal links. C22 is therefore readiness-gated.

## Instrumentation notes

- 2026-06-19: `Desktop/mentu-complete` gained a run-id capture bridge:
  `mentu cir capture --run-id`, `MENTU_RUN_ID` export from sequence steps, hook
  substrate forwarding, and MCP capture forwarding. This should make future
  lifecycle/tool-failure CIR rows joinable to run outcomes, but does not backfill
  existing rows or satisfy the surface-inventory gate. See
  `instruments/2026-06-19-c22-run-id-capture-bridge.md`.
- 2026-06-19: `Desktop/mentu-complete` gained a sequence-start
  `operational_surface_snapshot` signal with schema
  `c22.operational_surface_snapshot.v1`. It records run/workflow linkage, MCP/tool
  inventory, separated interface/dashboard/spreadsheet inventories, workflow
  structure, expected-change declarations, source-of-truth paths, freshness, fallback
  behavior, observability level, fragmentation class, score inputs, and a static
  manual-reconciliation risk estimate. These inventories are recipe-scan inferences,
  not runtime-observed usage or human reconciliation counts. See
  `instruments/2026-06-19-c22-operational-surface-snapshot.md`.
- 2026-06-19: the same instrumentation gained a step-exit
  `operational_surface_observation` signal with schema
  `c22.operational_surface_observation.v1`. It scans step output at the boundary for
  output-derived interface/dashboard/spreadsheet/manual-reconciliation evidence,
  stores hashes and extracted/sanitized references rather than raw output, and links
  each observation to `run_id`, workflow, and step label. This is stronger than
  recipe-only exposure, but still not direct UI, browser, or clipboard telemetry.
- 2026-06-19: MetaMCP gained direct child-tool surface events:
  `operational_surface_event` with schema `c22.operational_surface_event.v1`.
  The child-manager emits a best-effort event at the actual
  `child.client.callTool` boundary for success/failure and retry attempts. Events
  record server, tool, outcome, duration, attempt, sanitized argument/result/error
  metadata, surface-kind classifications, and `MENTU_RUN_ID`/workflow/step linkage
  when available. This observes actual MCP tool invocation metadata, but still not
  internal browser/UI/clipboard actions performed by the child tool.
- 2026-06-19: C22 scoring rules were frozen as
  `c22.surface_debt_score.v1` in
  `analyses/c22-operational-surface-debt/scoring.py`. Sequence-start snapshots are
  the only pre-outcome exposure predictor. Step-exit observations and direct MCP
  tool-call events are scored as runtime pressure and explicitly excluded from the
  exposure model. This satisfies the scoring-rule freeze gate, but not the exposure
  volume, outcome-linkage, diagnostic, cohort, control, or follow-up gates. See
  `instruments/2026-06-19-c22-surface-debt-score-v1.md`.

## Known limitations

- Tool fragmentation often follows complexity rather than causing it. Baseline task
  complexity and run class must be controlled.
- Strong teams may both build better architecture and get better outcomes for reasons
  outside the surface map. Matched cohorts and change windows matter.
- Some manual handoffs are deliberate safety controls. The score penalizes hidden,
  unaudited, or reconciliation-heavy handoffs, not human judgment itself.
- Interface quality can be a remedy or a liability. C22 treats dashboards as
  decision surfaces whose value depends on truth, freshness, and action linkage.
