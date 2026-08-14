# C22 operational surface snapshot - 2026-06-19

## Purpose

Second instrumentation push for **C22 operational surface debt**.

The run-id bridge made future CIR rows joinable to run outcomes. This push records a
structured, per-run exposure envelope at the sequence-start boundary so later C22
analysis can distinguish simple, fragmented, and contract-mapped multi-surface runs
before outcomes occur.

## Implementation

Patched `Desktop/mentu-complete`:

- `mentu-engine/Sources/MentuEngine/OperationalSurfaceSnapshot.swift`
  - adds schemas `c22.operational_surface_snapshot.v1` and
    `c22.operational_surface_observation.v1`;
  - builds canonical JSON for run id, workflow id, workspace, recipe surface,
    MCP/tool inventory, interface inventory, dashboard inventory, spreadsheet
    inventory, step/workflow structure, source-of-truth map, freshness, fallback
    behavior, observability level, fragmentation class, and score inputs;
  - adds a conservative static recipe-scan estimate for manual reconciliation risk
    while marking sequence-start `manual_reconciliation_observed` false;
  - adds step-exit output scanning that records output-derived dashboard,
    spreadsheet, interface, and manual-reconciliation indicators without storing raw
    output text.
- `mentu-engine/Sources/MentuEngine/SequenceRunner.swift`
  - emits `operational_surface_snapshot` immediately after MCP health caching and
    before step dispatch;
  - emits `operational_surface_observation` after step exits in DAG, wave,
    sequential, and canary-retry paths;
  - routes the signal through `CIRMemory.ingest(signal:runId:)`;
  - keeps capture best-effort: CIR or JSON failure never interrupts the sequence.
- `mentu-mcp/src/operational-surface-event.ts`
  - adds schema `c22.operational_surface_event.v1` for direct child MCP tool-call
    events;
  - records server, tool, outcome, duration, attempt, run/workflow/step env linkage,
    surface-kind classification, argument shape, result shape, and error class;
  - stores hashes and extracted/sanitized references only, not raw args, raw result
    content, URL query strings, or URL fragments.
- `mentu-mcp/src/child-manager.ts`
  - emits `operational_surface_event` at the actual `child.client.callTool`
    boundary for success, first-attempt failure, retry success, and retry failure.
- `mentu-mcp/src/cir-client.ts`
  - admits `operational_surface_event` as a valid MetaMCP CIR capture kind.
- `mentu-engine/Tests/MentuEngineTests/OperationalSurfaceSnapshotTests.swift`
  - verifies the snapshot schema, inventory counts, handoff/contract counts,
    fragmentation class, observability level, parseable canonical JSON, step-exit
    output scanning, sanitized URL handling, and raw-output non-storage.
- `mentu-mcp/src/__tests__/operational-surface-event.test.ts`
  - verifies direct tool-call event classification, sanitized URL handling, raw-arg
    non-storage, raw-result non-storage, and error-shape hashing.

## Captured Fields

The v1 payload includes:

- `run_id`, `workflow_id`, `workspace`, `project_root`;
- recipe-level transfer mode, run class, VM, tmux, sandbox, approval, secretless,
  and requirements;
- observed and declared MCP servers, MCP availability, step engines, Mentu MCP,
  cloud, VM, tmux, secretless, and sandboxed step counts;
- separated `interface_inventory`, including CLI, MCP, agent, web-target, and file
  surfaces inferred from the recipe;
- separated `dashboard_inventory`, including dashboard, status, admin, and console
  surfaces inferred from recipe URLs and labels;
- separated `spreadsheet_inventory`, including Google Sheets, spreadsheet references,
  and tabular files such as CSV/XLSX;
- `manual_reconciliation` static indicators, estimated count, indicator steps, and
  explicit `observed: false`;
- labels, step dirs, dependency edges, estimated handoffs, gates, forks,
  expected-change declarations, footprints, and shared steps;
- CIR/run-outcome/context source-of-truth paths;
- freshness stage and capture time;
- fallback behavior and no-mid-flight-interrupt policy;
- `fragmentation_class`, `observability_level`, and raw surface-debt score inputs.

The v1 step-exit observation payload also includes:

- schema `c22.operational_surface_observation.v1`;
- `run_id`, `workflow_id`, `step_label`, `stage: step_exit`;
- result status, loop completion, output bytes, cost, and duration;
- output-evidence hashes and character counts, with `raw_output_stored: false`;
- output-derived interface/dashboard/spreadsheet inventories;
- output-derived manual-reconciliation indicators and count source
  `step_output_scan_estimate`;
- an explicit limit: output mentions are not direct UI, browser, or clipboard
  telemetry.

The v1 direct surface-event payload also includes:

- schema `c22.operational_surface_event.v1`;
- actual child MCP server/tool invoked, outcome, duration, attempt, and route;
- run/workflow/step linkage from `MENTU_RUN_ID`, `MENTU_PIPELINE_NAME`, and
  `MENTU_STEP_LABEL` when present;
- surface classifications such as browser, dashboard, spreadsheet, repository, web,
  file, and manual-reconciliation surfaces;
- argument shape, sanitized URL/file references, and argument hash;
- result shape and result hash;
- error class and error hash for failures.

## Verification

- `swift test --filter OperationalSurfaceSnapshotTests` passed:
  3 Swift Testing tests.
- `npm run typecheck` passed in `mentu-mcp`.
- `npm run build && node dist/__tests__/operational-surface-event.test.js` passed:
  2 direct surface-event tests.

## Scientific Status

This is exposure telemetry, not a C22 verdict.

It satisfies the first structured `operational_surface_snapshot` requirement for
future Mentu sequence runs and gives C22 a pre-outcome surface record. It does not
backfill historical runs.

Follow-on scoring was frozen the same day as `c22.surface_debt_score.v1`; see
`instruments/2026-06-19-c22-surface-debt-score-v1.md`. Snapshot scores are the C22
pre-outcome exposure variable. Step-exit observations and direct MCP tool-call
events are runtime pressure evidence, not exposure predictors.

Remaining verdict blockers:

- sequence-start interface/dashboard/spreadsheet inventories are static recipe-scan
  inferences;
- step-exit inventories and manual-reconciliation counts are output-derived evidence,
  not direct UI, browser, or clipboard telemetry;
- direct MCP tool-call events observe actual child tool invocation metadata, but not
  direct UI/browser/clipboard interaction internals inside the child tool;
- business-logic location and integration owner are only partially represented;
- tool-collapse and interface-illusion diagnostics are not sampled;
- matched fragmented-vs-contract-mapped cohorts and follow-up windows do not yet
  exist.
