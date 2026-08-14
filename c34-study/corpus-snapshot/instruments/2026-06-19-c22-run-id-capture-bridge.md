# C22 run-id capture bridge - 2026-06-19

## Purpose

First instrumentation push for **C22 operational surface debt**.

The immediate blocker from the engineering audit was that live CIR had
`tool_failure` signals and run outcomes, but `tool_failure` rows carried no run id,
so they could not join to `cir-run-outcomes.jsonl`.

## Implementation

Patched `Desktop/mentu-complete` so future lifecycle and MCP CIR captures can attach
run ids:

- `mentu-engine/Sources/MentuEngine/CIRCommand.swift`
  - `mentu cir capture` now accepts `--run-id`;
  - capture routes the value into `CIRMemory.ingest(signal:runId:)`;
  - blank run ids normalize to nil;
  - concurrent-overflow pending files include a run-id-specific suffix, though the
    pending signal payload itself is still not a verdict-grade run-id envelope.
- `mentu-engine/Sources/MentuEngine/SequenceRunner.swift`
  - per-step agent/hook environment now exports `MENTU_RUN_ID`.
- `mentu-engine/Sources/MentuEngine/ProcessExecutor.swift`
  - forkpty and tmux paths backfill `MENTU_RUN_ID` from `config.recipeRunId` when
    callers did not provide it in step environment.
- `mentu-hooks/mentu_policy/substrate.py`
  - `capture_signal` and `cir_capture` append `--run-id` from explicit argument or
    `MENTU_RUN_ID`, `MENTU_RECIPE_RUN_ID`, `RUN_ID`;
  - legacy argv shape is preserved when no run id exists.
- `mentu-mcp/src/cir-client.ts`
  - `captureCIRSignal` appends `--run-id` from the same environment convention.

## Verification

- `python3 -m unittest discover -s tests -p 'test_supply_observe.py'` passed:
  35 tests.
- `swift test --filter CIRCaptureCommandTests` passed:
  1 Swift Testing test after building the engine target.
- `npm run typecheck` passed in `mentu-mcp`.

## Scientific Status

This is instrumentation, not evidence.

It does not backfill existing `tool_failure` rows, and it does not yet provide the
full C22 exposure envelope: per-workflow tool/interface/spreadsheet inventories,
source-of-truth freshness, handoff/reconciliation counts, tool-collapse diagnostics,
interface-illusion diagnostics, or matched fragmented-vs-contract-mapped cohorts.

It only closes the first join key: future CIR capture rows emitted inside a Mentu run
can now join to run outcomes by `signals.run_id`.

## Follow-up Instrumentation

Completed in `instruments/2026-06-19-c22-operational-surface-snapshot.md`:
Mentu now emits an `operational_surface_snapshot` signal at sequence start with:

- `run_id`
- `workflow_id`
- `tool_inventory`
- `source_of_truth_map`
- `handoff_count`
- `manual_reconciliation_count`
- `status_freshness`
- `integration_owner`
- `fallback_path`
- `observability_level`
- `fragmentation_class`

Remaining future work: separate `interface_inventory`, dashboard and spreadsheet
inventory, business-logic location, integration ownership beyond the runner default,
manual reconciliation counters, and diagnostic samples.
