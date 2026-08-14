# The Mentu Instrument

*Founding provenance map. Compiled 2026-06-10 from a five-target audit of the live
Mentu ecosystem. This document is what makes the corpus empirical: every conjecture's
operationalization must name sources listed here.*

## What the instrument is

Mentu is a locally-run autonomous execution runtime that treats knowledge work as
durable epistemic chains: observations become obligations, obligations require
evidence, and evidence is hash-chained, trust-scored, and append-only. Five components
generate data:

| Component | Location | Role | Liveness (2026-06-10) |
|---|---|---|---|
| Data home | `~/.mentu/` | All operational records | Hot — written minutes ago |
| mentu-engine | `~/Desktop/mentu-complete/` | Ledger, sequences, gates, recipes | Active — last commit same day |
| mentud daemon | `mentu-core-workspace/children/spine/mentu-daemon` | Sentinels, governance, experiments, ANE | Running (uptime hours) |
| api-server | `mentu-core-workspace/children/spine/api-server` | Hosted gateway; Neon Postgres persistence | Deployed (Fly.io `mentu-api`); last commit May 23 |
| mentu-mcp | `mentu-complete/mentu-mcp` | MCP aggregation + perception; usage telemetry | v0.4.1, built Jun 8 |

A structural fact worth recording: the engine's `EpistemicSignal` type — `semantic`
(entities/intent/domain), `trust` (confidence, verification chain, decay half-life),
`trace` (causal depth, parents/children), typed `relations`
(cites/extends/contradicts/refines), merkle `hash`/`prevHash` — implements, nearly
field-for-field, the Epistemic Signal Schema specified in the 2025 corpus
(`epistemic-main/engine/foundations/cir-memory-as-infrastructure.md`). The instrument
was built before the theory layer was reconnected to it.

## Primary data stores (`~/.mentu`)

| Store | Type | Size / count | Date range | Schema sketch |
|---|---|---|---|---|
| `audit.jsonl` | JSONL | 48MB / ~379K events (growing) | 2026-03-09 → live | `type` (rpc/scheduler/lifecycle), `actor`, `method`, `status`, `durationMs`, `timestamp` |
| `ledger.jsonl` (root) | JSONL | 586 entries¹ | 2026-03-23 → 2026-06-08 | `op` (capture/annotate/commit/claim/close/submit), `payload.kind`, `semantic.{domain,entities}`, `trust.{confidence,chain}`, `workspace`, `ts`, `actor`, `hash` |
| `.mentu/ledger.jsonl` (nested) | JSONL | 1,721 entries | 2026-05-31 → live | same + `syncScope` |
| `cir.db` | SQLite (schema v14) | 3.1GB | live (WAL active) | tables: `signals`, `trust_state`, `trust_events`, `contradictions`, `patterns`, `interpretations`, `relations`, `embeddings_vec` (576-dim), `trust_profiles`, `evaluation_gate`, `sync_queue`, `dream_queue` |
| `commitments/` | JSON per commitment | 46MB / 11,885 files | 2026-03-08 → **2026-04-09 (stale)**² | `id` (cmt_*), `state` (committed/cancelled/claimed/released/closed), `created_at`, `updated_at`, `title`, `tags` (incl. `sequence:` refs), `actor` |
| `file-history/` | daily snapshot dirs | 324MB / 80 days | rolling | per-file timestamped snapshots + `.meta.json` provenance |
| `training/` | JSONL ×34 | ~86MB / ~247K rows | mixed | incl. `cir-run-outcomes.jsonl` (see below), `epistemic-trust.jsonl`, `sft-instruction-pairs.jsonl` |
| `sentinel-state/` + `sentinel-logs/` | JSON + logs | 15MB / ~3,900 files | live | 6 sentinels: socket-watchdog, cpu-watchdog, embedding-drift, cir-contradiction-drift, canary-regression-watch, daemon-health; heartbeat ≈60s |
| `recipes/` | JSON | 13MB / 2,420 files | live | multi-step sequences; per-step model, timeout, permission mode |
| `agent-audit.jsonl` | JSONL | 86 entries | 2026-04-24 → 2026-06-08 | `agentId`, `intent`, `result`, `durationMs`, `prevHash` |
| `sequence-history.jsonl` | JSONL | 403 runs | 2026-04-21 → **2026-04-26 (stale)** | `name`, `startedAt`, `completedAt`, `status`, `okCount`, `totalSteps` |
| `cir-pending/` | JSONL staging | small, live | live | `capture.jsonl` (file_change), `agent-hook.jsonl` (command_exec, session_stop), `mentud.jsonl` (daemon signals) |

## The key outcome dataset: `training/cir-run-outcomes.jsonl`

One record per sequence run, recording whether prior knowledge (CIR context) was
injected and whether it helped. Verified fields (sampled 2026-06-10, 415 records):

`run_id`, `recipe`, `started_at`, `completed_at`, `duration_ms`, `outcome`
(`ok`/`fail`), `success`, `steps_ok`, `steps_total`, `steps_warn`, `total_cost`,
`cir_verdict` (`not_injected` / injected verdicts), `context_helped`,
`context_records`, `injected_count`, `injected_signal_ids`, `used_count`,
`used_signal_ids`, `use_rate`, `unproven_signal_ids`, `invalid_used_count`,
`contradiction_ids`, `missing_footer_count`, `missing_footer_rate`, `query_ms`,
`read_count`, `selected_signal_count`, `brief_bytes`, `surfaces` (per-surface
breakdown), `source_intent`, `training_label`.

This is the primary dataset for conjecture C1.

## Secondary stores

- **Neon Postgres (api-server)** — cross-device persistence: `cir_signals` (`ts`,
  `actor`, `workspace`, `kind`, `device_id`, `asserted_confidence`, `merkle_hash`),
  `recipe_runs` (`started_at`, `completed_at`, `outcome`, `week_bucket`),
  `training_signals` (adapter corrections; retrain threshold 200), `adapter_versions`,
  `webhook_deliveries`, `trigger_events`. Relevant to C5 (cross-device boundaries).
- **mentu-mcp telemetry** — per-call records (tool, server, `duration_ms`, `success`)
  appended non-blocking to its workspace ledger; CIR read-usage records (`query_ms`,
  `selected_signal_ids`, `source_intent`) written when memory is consulted. Relevant
  to C1 (when/why the system returns to memory).

¹ Counts in this table are point-in-time. The dated snapshots at the bottom of this
document (produced by `baseline_stats.py`) are canonical; where the founding audit's
agent-reported numbers disagreed with measurement (e.g., root ledger 1,586 vs the
measured 586), the measured value stands.

² Discovered during the C2 attempt (2026-06-10): the JSON snapshot store stopped
updating 2026-04-09 and 71% of its records never transition. Live commitment
lifecycle is event-sourced in `cir.db` `signals` (`op` + `commitment_id` + `ts` +
`workspace`) — but with caveats: only ~51% of commitment ids have a captured
`commit` op, ~65% are workspace-`unknown`, and cancelled/released states have no
terminal op. See `results/2026-06-10-c2-friction-to-production.md`.

## Data-quality caveats

1. `sequence-history.jsonl` stale since 2026-04-26 — sequence telemetry moved into
   `commitments/` (tags like `sequence:<name>`) and `cir-run-outcomes.jsonl`.
2. Schema drift mid-corpus: nested ledger added `syncScope`; ~43 ledger records have
   `op: null` (orphaned payloads).
3. `commitments/` contains a handful of `.tmp` files (partial writes); exclude from
   analysis.
4. `cir-run-outcomes.jsonl` itself records its own observability gaps
   (`missing_footer_count`: runs where the agent failed to report CIR usage) — treat
   `use_rate` as a lower bound.
5. `cir.db` is the richest store but its schema (14 migrations) is the source of
   truth; the JSONL mirrors lag it.
6. Mixed actors: records come from autonomous runs, scheduled jobs, and interactive
   sessions; analyses should segment by `actor`/`source_intent` where it matters.
7. Injection is not randomized. CIR injection correlates with recipe, time period,
   and system maturity — every C1-style result is observational, and confounding must
   be addressed explicitly (per-recipe stratification at minimum).
   *(Mitigated post-regime-boundary by MENTU_CIR_RANDOMIZE — see below.)*
8. **Observer effect**: reading CIR through Mentu tooling writes `access_count`
   and reinforcement telemetry — the founding audit's agents produced the only 2
   `context_used` events in system history (`digest_ABBD0388-C07`, 2026-06-07).
   Corpus analyses must read `cir.db` via raw read-only SQLite, never via
   `mentu cir` / MCP paths, or they contaminate the quantities they measure.

## ⚠️ Regime boundary: 2026-06-10T12:19Z

The instrument changed on 2026-06-10 (mentu-complete `dd43f96`, deployed and
live): brief evidence pool became distilled-only, reflections became citeable,
reflection confidence became outcome-derived, and `MENTU_CIR_RANDOMIZE=1`
began assigning per-run arms. New fields: `randomization_arm` (run outcomes +
context usage), `withheld_signal_ids` (context usage); new verdict/labels:
`withheld`, `cir_withheld_success|failed`.

**Analyses must treat data before and after this timestamp as different
instruments.** Injection eligibility, brief content, and verdict semantics all
changed. C1's dataset (415 runs ending 2026-06-10) is pre-boundary; C1b's
dataset is post-boundary only.

## ⚠️ Regime boundary: protocol v2.2 (2026-07-05/06)

The instrument changed again on 2026-07-05/06: Mentu protocol spec v2.0 → **v2.2**
("protocol & ledger hardening", the ActiveGraph / arXiv:2605.21997 assimilation),
landed on `mentu-complete` main (`c013b64..e6d098b`, 2026-07-05) and deployed to the
engine binary and the live ledger. Full audit + boundary declaration:
`instruments/2026-07-06-protocol-v22-regime-boundary-and-impact.md`. Timeline: spec
landed `c013b64` (2026-07-05T22:14:43-06:00) → audit reconciliation `82deb5b`
(2026-07-05T23:27:58-06:00) → `lane_cutover` marker live 2026-07-06T05:13:24Z →
`steer_message` CIR-ingest deployed `949a018` (2026-07-06T08:54:43-06:00 =
2026-07-06T14:54:43Z UTC). **New signal kinds enter the substrate from these
timestamps; never pool kind-population or retrieval-pool metrics across this v2.2
boundary without declaring it.**

### New stores

- **`.mentu/cache/model-responses/`** — content-addressed response blobs for the
  engine's in-process model calls (**2 MB cap** per blob, with truncation markers
  when a response exceeds it), plus
  **`.mentu/cache/model-responses/manifests/<runId>.calls.jsonl`** — per-run call
  manifests (each call's request hash + blob digest).
- **`.mentu/mcp-telemetry.jsonl`** — **MCP tool-call rows moved here, out of
  `ledger.jsonl`** (from the `82deb5b` deploy onward). The rows are not gone, they
  relocated: any analysis that expected MCP telemetry in-ledger sees that lane
  **frozen at the cutover**, so pre-v2.2 in-ledger MCP counts are not comparable to
  post-v2.2 ledger counts. (This is why the founding "mentu-mcp telemetry" store
  above — appended to the workspace ledger — no longer describes the post-v2.2 lane.)

### New signal kinds (ledger / CIR)

| Kind | Meaning | Decay policy |
|---|---|---|
| `steer_message` | mid-run human steer text, recorded (full text) before injection at sequence-step and loop-beat boundaries; **CIR-ingested / embeddable / retrievable** from `949a018` | — |
| `model_call` / `tool_call` | content-addressed engine **in-process** calls (semantic gate, completion verifier) | **7-day** default half-life — same policy family as `temporal_result` |
| `call_lane` | run-level chain anchor over a run's calls (`manifest_sha256`) | — |
| `fork` | typed concurrency artifact carrying `prefix_head_hash` (lineage-anchored) | — |
| `session_anchor` | session boundary marker | — |
| `lane_cutover` | one-time hashed-lane cutover annotation (`ann_697E1D54-3DD`, 2026-07-06T05:13:24Z) | — |

### Chain semantics

Verification is now **canonical-ancestry** (a break is a *missing ancestor*), not
line-adjacency. The reference verifier this corpus uses —
`mentu-complete/protocol/tools/verify_ledger.py` — was reimplemented accordingly, and
the engine's own `mentu verify-ledger` now agrees with it (do not run the CLI here —
observer-effect rule; use the standalone script). **Name both versions so old numbers
stay interpretable:**

- **verifier v1** (line-adjacency semantics): the pre-v2.2 classifier. Numbers
  computed under it — e.g. the return-base-rate draft's "109 chain breaks" — are
  interpretable only as v1 output.
- **verifier v2** (canonical-ancestry semantics, 2026-07-05): the current reference.
  On the *same bytes*, v1's 109 "breaks" decompose into **0 missing-ancestor breaks +
  62 typed concurrency forks + 1 genesis/import anchor**; content integrity is
  unchanged.

Forks are typed **non-fatal** concurrency artifacts, and their root cause (per-symlink
append locks) is **fixed** upstream (`c013b64`). The `lane_cutover` marker is live at
**2026-07-06T05:13:24Z**: the 1,023 unhashed hook-lane rows before it are
grandfathered; any unhashed row *after* it is a chain violation. Verification-replay
(`mentu runs replay --strict`, `E_REPLAY_DIVERGED`) and `fork` lineage anchoring
(`prefix_head_hash`) also arrive with v2.2.

### Data-quality caveats (delta from the founding list)

9. **Steered runs are now visible.** Pre-v2.2 a human could steer a run mid-flight
   with no durable record — an unrecorded co-input confounding outcome attribution.
   `steer_message` signals make steering mechanically stratifiable/excludable for
   every per-run outcome analysis (C2, C6, C24, C1b). Declared as the C25
   co-intervention watch: `instruments/protocol-v22-cointervention-marker.json`.
10. **Fork ancestry is verifiable.** `fork` signals carry `prefix_head_hash`, so
    forked runs masquerading as independent cohort members are cryptographically
    detectable (C1b cohort hygiene).
11. **The call lane covers ONLY the engine's in-process calls.** Step agents run as
    child processes and are OUT of lane; their calls — and therefore brief
    *consumption* — remain unrecorded. **C1b's Stage-2 footer-instrumentation problem
    is unchanged**; v2.2 does not close it. The child-agent lane is the named
    follow-up, not a shipped capability.

## Baseline snapshot

Run `python3 instruments/baseline_stats.py` to append a dated snapshot below.

<!-- BASELINE SNAPSHOTS -->

### Snapshot 2026-06-10T11:19:34Z

| Store | Count | First ts | Last ts |
|---|---|---|---|
| audit.jsonl | 379072 | 2026-03-09T04:13:51Z | 2026-06-10T11:19:29Z |
| ledger.jsonl (root) | 586 | 2026-03-23T06:41:00Z | 2026-06-08T08:33:13Z |
| ledger.jsonl (nested) | 1721 | 2026-05-31T05:34:54Z | 2026-06-09T05:15:32Z |
| training/cir-run-outcomes.jsonl | 415 | 2026-05-17T10:15:19Z | 2026-06-10T10:27:32Z |
| sequence-history.jsonl | 403 | ? | ? |
| agent-audit.jsonl | 86 | 2026-04-24T21:28:39.195Z | 2026-06-09T01:49:29.409Z |
| commitments/ (excl. .tmp) | 11885 | | |
| recipes/ | 2414 | | |
| file-history/ (day dirs) | 80 | | |
| sentinel-logs/ | 3911 | | |
| cir.db | 3.31 GB | | |
