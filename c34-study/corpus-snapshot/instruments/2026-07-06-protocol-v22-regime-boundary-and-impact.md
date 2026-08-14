# 2026-07-06 — Protocol v2.2 (ledger & protocol hardening): regime boundary + impact audit

*Instrument note (same class as `2026-06-15-c1b-footer-measurement-fix.md`). Documents a
measurement-regime change originating upstream in the instrument (the Mentu engine +
protocol), audits its impact on open conjectures and in-flight papers, and declares the
boundary. Touches no frozen prediction, verdict, or result.*

## What changed upstream

Mentu protocol spec v2.0 → **v2.2** ("protocol & ledger hardening", the ActiveGraph /
arXiv:2605.21997 assimilation), landed on `mentu-complete` main 2026-07-05/06 and
deployed (engine binary + live ledger markers). Sources of truth:
`mentu-complete/protocol/CHANGELOG.md` (v2.2 entry), the audit
`.mentu/audits/activegraph-log-primacy-2026-07-05/REPORT.md`, and the execution log
`docs/context/CONTEXT-protocol-ledger-hardening.md`. Public spec:
`github.com/mentu-ai/protocol` @ `0390a03`.

Instrument-relevant changes:

1. **Chain semantics corrected** — verification is now canonical-ancestry (break =
   missing ancestor), not line-adjacency; forks are typed non-fatal concurrency
   artifacts; the fork root cause (per-symlink append locks) is FIXED; the genesis/
   import anchor is recognized; `verify_ledger.py` (the reference verifier this corpus
   uses) reimplemented accordingly, and the engine's own `mentu verify-ledger` now
   agrees with it.
2. **`lane_cutover` marker live** on the shared ledger at **2026-07-06T05:13:24Z**
   (`ann_697E1D54-3DD`): the 1,023 unhashed hook-lane rows are grandfathered; unhashed
   rows after the marker are chain violations. All known unhashed writers migrated
   (hook scripts → hashed `--ledger-anchor` path; **MCP telemetry rows moved out of
   `ledger.jsonl` into `.mentu/mcp-telemetry.jsonl`**).
3. **Invariant 6 — Inputs Are Events**: mid-run steer messages are recorded as hashed
   `steer_message` ledger signals (full text) BEFORE injection, at sequence-step and
   loop-beat boundaries; and (since 949a018) steer_message is **CIR-ingested and
   embeddable** — retrievable into future briefs.
4. **Execution call lane**: `model_call`/`tool_call` content-addressed signals for the
   engine's IN-PROCESS model calls (semantic gate, completion verifier) with response
   blobs under `.mentu/cache/model-responses/` + per-run manifests; run-level
   `call_lane` chain anchor (`manifest_sha256`); CIR half-life 7d for the per-call
   kinds. **Coverage boundary: step agents run as child processes and are OUT of
   lane** — their calls (and therefore brief consumption) remain unrecorded.
5. **Verification-replay** (`mentu runs replay [--strict]`, `E_REPLAY_DIVERGED`) and
   **fork lineage anchoring** (`fork` signals carrying `prefix_head_hash`).
6. **Projections discipline**: step resume/fork reuse is content-keyed
   (`StepStatus.cacheKey`); reuse-by-label is non-conformant.

## The regime boundary

```json
{
  "boundary": "protocol_v2.2",
  "spec_landed": "2026-07-05T22:14:43-06:00 (c013b64) .. 2026-07-05T22:49:41-06:00 (e6d098b)",
  "lane_cutover_ts": "2026-07-06T05:13:24Z",
  "audit_reconciliation": "2026-07-05T23:27:58-06:00 (82deb5b)",
  "steer_cir_ingest_deployed": "2026-07-06T08:54:43-06:00 (949a018)",
  "note": "New signal kinds (steer_message, model_call, tool_call, call_lane, fork, session_anchor, lane_cutover) enter the substrate from these timestamps. steer_message is embeddable and retrievable from 949a018 deploy onward. MCP telemetry rows leave ledger.jsonl from 82deb5b deploy onward. Never pool kind-population or retrieval-pool metrics across this boundary without declaring it."
}
```

## Obligations (per this corpus's constitution)

1. **C25 co-intervention declaration.** `steer_message` entering the embeddable pool is
   a NEW potential return channel landing INSIDE the C25 accrual window (gate 0/150,
   analyzer dormant). It does not modify the C7 handle-offer mechanism P1 measures, but
   it changes the retrievable-content population. Expected magnitude today: ~zero
   (steering is rare; zero steer_message signals exist at boundary time). Discipline:
   declared here, like the already-noted C1b-withheld-arm dilution — when the gate
   opens, the analyzer should report steer-derived offers separately if any exist.
   The frozen predictions and falsification rule are untouched.
2. **Verifier version bump for the return-base-rate paper (§2).** Draft v1.2 reports
   "109 chain breaks, 108 coinciding with workspace switches" under the OLD
   adjacency-semantics verifier and argues statistically they are session boundaries.
   Under the corrected reference verifier the SAME bytes classify as **0 breaks + 62
   forks + 1 genesis/import anchor** — and the fork mechanism is now root-caused
   (per-symlink locks) and fixed, converting the paper's statistical argument into a
   mechanical one. The load-bearing number (100% content integrity, 11,106/11,106) is
   unchanged. Action before submission: update §2 to the corrected semantics (stronger
   story), or pin "verifier v1, adjacency semantics" as the instrument version. The
   underlying ledger bytes are untouched — this is instrument correction, not data
   change.
3. **Evidence-carrying-execution paper: verification anchors are stale.** Its
   `formal/invariant-spec.md` grounds invariants in `Ledger/Ledger.swift` file:line +
   source digests; commits c013b64/82deb5b/949a018 modified that file (K1's
   `validateCitation` shifted ~9 lines; `verify()` rewritten). Action: re-run the
   digest verification and re-ground file:lines. Opportunity: v2.2 is NEW paper
   material — the thesis ("evidence-carrying execution") now extends to the execution
   plane with mechanically-enforced primitives to cite: in-engine canonical-ancestry
   verification, Invariant 6 (inputs are events), strict replay with
   `E_REPLAY_DIVERGED`, chain-anchored call lanes, and the projections discipline.
4. **Provenance map updates** (`instruments/mentu-instrument.md`): add
   `.mentu/cache/model-responses/` (+ `manifests/`), `.mentu/mcp-telemetry.jsonl`
   (MCP rows NO LONGER in `ledger.jsonl`), the seven new signal kinds, and the new
   kind-scoped decay defaults (model_call/tool_call 7d — same policy family as
   temporal_result).

## Benefits by conjecture

- **Internal validity for every per-run outcome analysis (C2, C6, C24, C1b):**
  steered runs are now VISIBLE. Pre-v2.2, a human could steer a run mid-flight with no
  durable record — an unrecorded co-input confounding outcome attribution. Analyses
  can now stratify or exclude steered runs mechanically.
- **C11 (measurement-action closure):** `steer_message` IS a measurement→action edge —
  a human observed run state and acted, durably. The conjecture was blocked on
  "explicit measurement-to-action closure edges"; a new edge type now accrues.
- **Decision-level outcomes (external-critique adoption #9):** a brief-retrieved past
  steer that alters a later run is precisely "a return that altered a subsequent
  commitment" — the first substrate primitive matching the adopted definition.
- **C7 (handle-mediated returnability):** `request_hash` + content-addressed blobs are
  a new mechanically-stable handle class, and call-lane manifests are handle
  inventories whose first-seen snapshots come free — chain-anchored via
  `manifest_sha256`.
- **C22 (operational surface debt):** `mentu runs replay --json` emits per-run surface
  diagnostics (statuses for the run, content-keyed count, blobs resolved, anchor
  status) — new machine-readable inventory for the surface-debt score.
- **C23 (review trust calibration):** blocked on explicit target-run linkage;
  `call_lane`/`fork` anchors + per-run manifests strengthen run-identity plumbing.
- **C14 (measurement contract validity):** the call lane carries digests, size caps,
  and truncation markers — measurement metadata where none existed.
- **C3a (mechanical decay, supported):** kind-scoped half-lives now cover a second
  population (execution-lane kinds), broadening the decay-policy test surface.
- **C1b cohort hygiene:** fork ancestry is cryptographically verifiable
  (`prefix_head_hash`), so forked runs masquerading as independent cohort members are
  detectable.
- **The corpus's own instrument claim strengthens:** the README's "append-only,
  hash-chained" ledger had two documented weaknesses (109 apparent breaks; 1,023
  unhashed rows). Both are now typed, root-caused, and closed going forward — future
  §instrument sections get shorter and stronger.

## What v2.2 does NOT fix (honest boundary)

C1b's Stage-2 measurement problem stands. The call lane records only the engine's
in-process calls; step agents are child processes, outside it — so brief
*consumption* remains footer-instrumented (median missing-footer rate 1.00 in the
injected arm). The structural fix (recording the child agent's request content and
joining offered-signal ids against it) requires a child-agent lane, which v2.2
explicitly declined to attempt (no child-process interception). It is the named
follow-up, not a shipped capability.

## Risks (minor, bounded)

Substrate growth from new kinds is bounded (in-process calls only; 7-day decay; 2 MB
blob caps; GC named as follow-up). `steer_message` entering the embedding pool changes
retrieval-pool composition — declared above as the C25 co-intervention watch.
