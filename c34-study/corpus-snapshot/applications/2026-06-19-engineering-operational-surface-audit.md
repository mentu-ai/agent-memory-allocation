# Engineering operational surface audit - 2026-06-19

## Scope

Read-only audit of:

- `Workspaces/mentu-physics/foundational/blueprint/ese/engineering/`

No predecessor files were edited.

## Decision

Admit **C22 operational surface debt**:
`corpus/conjectures/c22-operational-surface-debt.md`.

The engineering corpus's strongest new testable mechanism is operational surface
architecture: how tools, dashboards, spreadsheets, workflow state, source-of-truth
records, integration ownership, and manual handoffs shape operational reliability.

## Dispositions

| Idea | Disposition | Why |
|---|---|---|
| Tool Zoo / excessive tooling / toolification | **Admitted as C22 motivation and predictor surface** | Becomes measurable through per-run tool inventory, integration count, ownership, fallback, and observability. |
| Spreadsheet Factory | **Admitted as C22 failure mode** | Becomes manual reconciliation, embedded-logic, duplicate-version, and source-of-truth ambiguity telemetry. |
| Operational Fog / Decorated Fragility | **Admitted as C22 high-debt states** | Keeps the measurable residue: hidden status, hero dependence, stale dashboards, and foundation/interface imbalance. |
| Tool Collapse Map / Interface Illusion Audit / System Autopsy | **Admitted as C22 diagnostic surfaces** | These become structured diagnostic findings that can be linked to later outcomes. |
| Source-of-Truth Architecture / Workflow Assembly Line / Adaptive Engine | **Admitted as C22 remedy variables** | These define canonical records, visible state, externalized logic, and feedback loops as measurable protections. |
| Status Architecture | **Parked outside C22** | This file is mainly about social position and implementation resistance; it may support a later adoption/status-threat conjecture, but it is not the main operational-surface claim. |

## Live readiness digest

`analyses/c22-operational-surface-debt/analyze.py` checks source vocabulary, CIR
signals, and run outcomes.

Current source snapshot:

- markdown files: 102;
- logical source lines: 16,041;
- top-level file distribution: cognitive-interfaces 51, epistemic-operations 26,
  recursive-intelligence 15, knowledge-orchestration 10;
- source term counts: tool sprawl 413, maturity/adaptive 381,
  workflow/orchestration 285, failure/dependency 131, interface illusion 97,
  spreadsheet/manual 87, operational fog 66, source-of-truth 54;
- source coverage: all required categories are present; tool-sprawl language appears
  in 51 files, workflow/orchestration in 63, maturity/adaptive in 72,
  source-of-truth in 21, interface-illusion in 30, spreadsheet/manual in 20,
  operational fog in 16, and failure/dependency in 34.

Current live substrate:

- C22 scoring schema: `c22.surface_debt_score.v1`;
- CIR signal rows: 267,536;
- `tool_failure` signals: 2,229;
- `step_result` signals: 6,588 across 2,119 run ids;
- `correction` signals: 215;
- `approval` signals: 3;
- `semantic_gate_eval` signals: 104;
- exact operational-surface event kinds: 0;
- structured C22 surface rows: 0 snapshots, 0 observations, 0 direct events;
- scored C22 surface rows: 0 pre-outcome exposure rows and 0 runtime pressure rows;
- run outcome rows: 629 across 612 run ids;
- run outcomes: 184 success rows, 445 failure rows, 391 warning rows, 414 total
  step warnings;
- all run outcome rows have duration and cost fields;
- run-outcome surface-term mentions are sparse: dashboard 5, tool 2, status 2;
- `tool_failure` signals currently have 0 run ids and 0 overlap with run outcomes.

The first scientific blocker, frozen scoring rules before outcome modeling, is now
closed by `analyses/c22-operational-surface-debt/scoring.py`. The remaining blocker
is structural: current records have tool failures and run outcomes, but tool
failures are not linked to run outcomes by run id. There are no live
post-instrumentation per-workflow surface inventories, source-of-truth freshness
records, manual-handoff denominators, tool-collapse/interface-illusion diagnostic
findings, matched fragmented-vs-contract-mapped cohorts, or surface-to-outcome
causal links.

## Next push

Add operational-surface exposure telemetry:

- `workflow_id`
- `run_id`
- `surface_snapshot_id`
- `tool_inventory`
- `interface_inventory`
- `dashboard_inventory`
- `spreadsheet_inventory`
- `source_of_truth_map`
- `handoff_count`
- `manual_reconciliation_count`
- `business_logic_location`
- `integration_count`
- `integration_owner`
- `fallback_path`
- `observability_level`
- `status_freshness`
- `layer_maturity_scores`
- `tool_collapse_findings`
- `interface_illusion_findings`
- `surface_debt_score`
- `fragmentation_class`
- `linked_outcome_ids`

Most important: record both the surfaces that were used and the surfaces that were
available but bypassed or manually reconciled. Without those denominators, C22 would
only rediscover generic tool failures.

## Follow-through

First instrumentation push landed in `Desktop/mentu-complete` on 2026-06-19:
`mentu cir capture --run-id`, `MENTU_RUN_ID` step export, hook substrate forwarding,
and MCP capture forwarding. This closes the first join-key gap for future data only.

Second instrumentation push landed the same day:
`operational_surface_snapshot` is emitted at Mentu sequence start with schema
`c22.operational_surface_snapshot.v1`. It records run/workflow linkage, MCP/tool
inventory, separated interface/dashboard/spreadsheet inventories, workflow
structure, expected-change declarations, source-of-truth paths, freshness, fallback
behavior, observability level, fragmentation class, score inputs, and a static
manual-reconciliation risk estimate.

The same push now also emits `operational_surface_observation` at step exit with
schema `c22.operational_surface_observation.v1`. It scans step output for
output-derived surface evidence, stores output hashes and extracted/sanitized
references rather than raw output, and links each observation to run id, workflow,
and step label.

MetaMCP now emits `operational_surface_event` with schema
`c22.operational_surface_event.v1` at the actual child MCP `callTool` boundary. It
records server, tool, outcome, duration, retry attempt, sanitized argument/result
metadata, error class, surface-kind classifications, and run/workflow/step linkage
when the Mentu runner supplied those env vars.

Third push: the deterministic score rubric is frozen as
`c22.surface_debt_score.v1`. Sequence-start snapshots are scored as the C22
pre-outcome exposure variable. Step-exit observations and direct MCP events are
scored only as runtime pressure and are explicitly excluded from the exposure model.

This still does not backfill the 2,229 existing `tool_failure` rows. It also does
not complete the C22 verdict gate: sequence-start inventories are recipe-scan
inferences, step-exit observations are output-derived rather than direct UI/browser/
clipboard telemetry, direct MCP events observe tool invocation metadata rather than
child-tool internals, the live CIR database has 0 structured C22 surface rows, and
business-logic location, integration ownership, diagnostic samples, matched cohorts,
controls, and follow-up windows remain open.
