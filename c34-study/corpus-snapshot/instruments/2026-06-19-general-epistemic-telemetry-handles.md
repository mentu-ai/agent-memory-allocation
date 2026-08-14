# General epistemic telemetry handles - 2026-06-19

## Purpose

Generalize the C22 telemetry lesson across the full epistemics corpus.

The recurring blocker across C7, C9, C11, C13-C22 is not one missing metric. It is
missing typed exposure metadata at capture time: first-seen snapshots, conjecture
ids, evidence roles, capture boundaries, score schemas, evidence tiers, and explicit
separation between pre-outcome predictors and runtime/outcome-adjacent pressure.

## Implementation

Patched `Desktop/mentu-complete`:

- `mentu-mcp/` (`metamcp@0.4.1`)
  - adds a shared TypeScript epistemic telemetry helper matching the engine-side
    `mentu.epistemic_handle.v1` contract;
  - adds the MCP tool `cir_capture_signal` so MetaMCP itself can capture typed
    LARCS/CIR/conjecture evidence without relying on a child server to know the
    Mentu CLI shape;
  - removes the hardcoded TypeScript CIR kind allow-list in favor of structural
    kind validation, so C7-C22 and later conjectures can add instruments without
    editing MetaMCP each time.
- `mentu-engine/Sources/MentuEngine/EpistemicTelemetry.swift`
  - introduces `mentu.epistemic_handle.v1`;
  - normalizes conjecture ids, evidence roles, evidence tiers, capture boundaries,
    score schemas, score sources, and exposure-model inclusion/exclusion;
  - emits queryable CIR domain tags such as `conjecture:c7`,
    `evidence_role:first_seen_exposure`, `capture_boundary:artifact_create`, and
    `exposure_model:included`;
  - emits entity tags such as `handle:<id>`, `artifact:<id>`, `run:<id>`,
    `workflow:<id>`, and `step:<label>`.
- `mentu-engine/Sources/MentuEngine/CIRCommand.swift`
  - adds forward-compatible `mentu cir capture` flags:
    `--conjecture`, `--evidence-role`, `--evidence-tier`, `--capture-boundary`,
    `--score-schema`, `--score-source`, `--exclude-from-exposure-model`,
    `--handle-id`, and `--artifact-id`;
  - stores the metadata in existing `SemanticContext.domain` and `entities`, avoiding
    a Merkle-breaking `EpistemicSignal` schema change.
- `mentu-mcp/src/cir-client.ts`
  - adds optional capture metadata so TypeScript producers can pass the same
    conjecture/evidence/handle tags through the CLI bridge;
  - exposes `buildCIRCaptureArgs` for testable, non-spawning validation of the
    exact `mentu cir capture` argv used by MetaMCP.
- `mentu-engine/Sources/MentuEngine/OperationalSurfaceSnapshot.swift` and
  `mentu-mcp/src/operational-surface-event.ts`
  - now include `epistemic_handles` payloads as examples of the shared contract.
- `Desktop/Crawlio-app` LACS/LARCS producers
  - `ArtifactStore.capture` now emits `handle_snapshot` with `--conjecture c7`,
    `--evidence-role first_seen_exposure`, `--handle-id`, and
    `--score-source pre_outcome_exposure` at handle creation;
  - local LACS API, Swift Crawlio MCP tools, recrawl resolution, diff/discover,
    body reads, lineage, investigation, and promoted-tool execution now emit
    `handle_return_event` or `handle_use_event` as post-exposure observations
    excluded from the exposure model;
  - the TypeScript `@crawlio/mcp` aggregator can now pass the same capture metadata
    through its CIR client and emits `handle_use_event` for `recrawl_urls` handle
    arguments/targets.

## Implications

This is the substrate-level lesson from the audits:

- C7/LARCS: every handle needs first-seen snapshots and later return/use events tied
  to `handle:<id>` and `conjecture:c7`.
- MetaMCP/CIR: `cir_capture_signal` is now the practical capture path for these
  handles when the active surface is `metamcp`, including Crawlio/LARCS-style
  handle snapshots.
- C9: pattern exposure and later reuse should be captured separately.
- C10: structure-debt predictors need run/workspace/schema identity fields before
  later failures are observed.
- C11/C14: measurements need explicit measurement-to-action or calibration/reference
  tags, not just metric text.
- C13/C15: artifact maturity/redundancy/compiler-readiness scores need first-seen
  artifact snapshots before reuse outcomes.
- C16: activation decisions need candidate-level `activated`, `skipped`, and
  `deferred` captures before outcomes.
- C19/C20: governance and participation contracts need change-time exposure records,
  not post-hoc summaries.
- C21: relationship/navigation exposures need typed context-edge denominators.
- C22: operational-surface snapshots/events now use the same generic handle layer.

## Scientific Status

This is telemetry hardening, not a verdict.

It does not prove any conjecture. It makes future data less ambiguous by ensuring the
running system can say, at capture time, what conjecture a signal informs, what role
it plays, whether it belongs in the pre-outcome exposure model, and which handle,
artifact, run, workflow, or step it refers to.
