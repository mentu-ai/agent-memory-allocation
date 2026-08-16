# BUILD — CIR Substrate Hardening (post-exhaust-incident) v1

**Date:** 2026-07-08
**Depends on:** engine commit `7a3f85a` (fix(cir): reap machine exhaust by age; repair the silently-broken prune cascade) — the incident fix this build generalizes. Read its commit message first; it is the incident report.
**Executor:** claude-opus-4-8 implementing DIRECTLY from this doc — **not** compiled to recipes, `/scaffold` is not used. All judgment is pre-made here; where it could not be, the step says DIAGNOSE FIRST or HUMAN.
**Repos touched:** `mentu-complete` (engine `mentu-engine/`, mcp `mentu-mcp/`). One milestone (M6) has a declared side-effect on the `epistemics` repo's measurement regime — it requires a HUMAN-acknowledged instrument note, not epistemics code.

---

## 0. Scope & thesis

### 0.1 The incident this build generalizes

On 2026-07-08, `~/.mentu/cir.db` was found at 2.2 GB with 76% of its 468k
signals being machine exhaust: `handle_snapshot` (C7 returnability telemetry,
introduced 2026-06-19, 158,722 rows at ~8,300/day) and `temporal_result`
(197,778 rows). All of it was embedded (stale pre-`9862051` binaries kept
running the ungated backfill). The nightly reaper could not touch it — the
stale prune requires >90d AND <0.2 confidence and exhaust enters at default
confidence (2 of 356k rows matched) — and was ALSO silently dying on a missed
`evaluation_gate.correction_id` FK. On the bloated store, the runtime evidence
policy's recursive source-chain walk (which re-prepares the very large
generated `queryUsageDebt` SQL per provenance node; a live CPU sample showed
SQLite *parse* dominating) stalled recipe milestone transitions 10+ minutes.

`7a3f85a` fixed the instance: age-only exhaust reaping (>14d, provenance-cited
rows exempt), ineligible-embedding sweep, multi-space vec prune, the FK repair,
and a one-time purge (2.2 GB → 897 MB; the maintenance snapshot went from
minutes to 0.22 s).

### 0.2 The one-sentence goal

> Convert the instance fix into structural guarantees: new signal kinds
> default to the cheap tier (M2), maintenance proves it is effective instead
> of merely running (M3), accountability verdicts stop being recomputed from
> combinatorially-expanded SQL on every read (M4–M5), C7 telemetry stops
> polluting the knowledge substrate and spawning a process per handle (M6),
> and prune cascades / deployed binaries can no longer drift silently
> (M1, M7).

### 0.3 What this build is NOT

- **Not a re-litigation of `7a3f85a`.** Its behavior (exhaust kinds, 14d age,
  provenance exemption, sweep) is the baseline. Extend, don't rewrite.
- **Not a semantics change to accountability.** The `accountable*SQL`
  predicates in `CIRUsageMaintenancePolicy` (CIRStore.swift, ~lines 77–443)
  ARE the definition of accountable use/ignore/cool/doubt. M4 materializes
  them; it must be provably read-equivalent (dual-read gate), never a
  redefinition.
- **Not an epistemics analysis.** Where a milestone changes a measured
  quantity, the obligation is to STOP and flag for a dated instrument note in
  the `epistemics` repo (convention:
  `epistemics/instruments/2026-07-08-cir-exhaust-purge-regime-note.md`);
  writing epistemics corpus content is out of scope.

### 0.4 Invariants that govern every milestone

1. **The live db is production.** `~/.mentu/cir.db` (897 MB, post-purge) is
   live shared state used by concurrent runs and daemons. Tests operate on
   temp `MENTU_HOME` dirs only (`PathResolver` honors `MENTU_HOME`). For a
   realistic fixture, snapshot with `sqlite3 -readonly <db> "VACUUM INTO
   '<dest>'"` — NEVER `cp` a live WAL database (torn copies; this bit us in
   rehearsal). A consistent pre-purge snapshot exists at
   `~/mentu-home/cir.db.pre-exhaust-purge-20260708.bak` if bulk data is needed.
2. **Fail-open at runtime, loud in maintenance.** Runtime CIR paths (brief
   prep, ingest, usage recording) keep their fail-open contract. Maintenance
   paths do the opposite: a prune that collects candidates and deletes zero
   is a FAILURE (M3), not a success.
3. **Provenance exemption is untouchable.** Signals cited in any derived
   signal's `source_ids` are never pruned (2,471 derived signals, avg fan-out
   43). Nothing in this build may weaken that.
4. **Backward compatibility.** Schema migrations are additive
   (`CIRStore.currentSchemaVersion`, currently 15 at CIRStore.swift:624).
   A v15 db opens under v16+ with a lossless migration; no field of an
   existing row is reinterpreted.

---

## 1. Executor constitution

1. **Branch discipline.** All work on `main`. Conventional commits, no
   `Co-Authored-By`, never amend, never force. One commit per milestone
   minimum. The tree may carry unrelated WIP (dashboard/fleet files) from
   other sessions — stage ONLY your own files, by explicit path.
2. **Build discipline.** Iterate with `cd mentu-engine && swift build`; run
   `swift test --filter <relevant>` before each milestone commit and one full
   `swift test` before M7. Release install ONCE, in M7, via
   `cd mentu-engine && make install` (cat-not-cp + codesign; see Makefile).
   For `mentu-mcp`: `npm test` in `mentu-mcp/` for M6.
3. **Line-number caveat.** File:line references are as of `7a3f85a`.
   Re-locate every symbol by grep before editing; do not trust line numbers.
4. **No live-db writes outside M7's verification.** Read-only inspection of
   the live db is allowed (`sqlite3 -readonly`). The one sanctioned live
   operation is M7's post-install `mentu cir compact --dry-run` smoke check.
5. **Escalation triggers** (stop, write an escalation note into
   `docs/context/CONTEXT-cir-substrate-hardening.md`, do not proceed):
   (a) M4's dual-read comparison finds ANY mismatch between materialized and
   predicate-derived verdicts on real data; (b) a change would alter which
   events count as accountable (semantics, not representation); (c) M6's
   routing would make C7 returnability unmeasurable rather than
   differently-measured; (d) any migration that cannot round-trip a v15 db.

---

## 2. Milestones

Execution order: **M1 → M2 → M3 → M4 → M5 → M6 → M7** (serial). M1 first
because it is a pure test that then guards every later cascade edit. M4 is
the largest and lands mid-build so its dual-read soak (M4.4) can run while
M5–M6 proceed. M7 is last: single release install + drift guard.

---

### M1 — Schema-derived prune-cascade completeness test

**Why.** The stale prune died for weeks on `evaluation_gate.correction_id
REFERENCES signals(id)` — a child table added after the cascade was written.
`7a3f85a` fixed that instance by hand. The class fix is a test that derives
the FK graph from the schema itself, so the NEXT table added with a
`REFERENCES signals(id)` breaks CI, not production.

**M1.1** New test file
`mentu-engine/Tests/MentuEngineTests/CIRPruneCascadeCompletenessTests.swift`.
Build a temp-`MENTU_HOME` store (existing test helpers show the pattern —
grep `MENTU_HOME` under `Tests/`), then:
- Enumerate every table with an FK to `signals` at runtime:
  `SELECT name FROM sqlite_master WHERE type='table'` + `PRAGMA
  foreign_key_list(<table>)`, collecting tables where any FK's target table
  is `signals`.
- Insert one signal plus one referencing row into EVERY such table (generic:
  fill NOT NULL columns with type-appropriate dummies; the FK column gets the
  signal id).
- Force the signal to be prune-eligible for BOTH prunes and run
  `pruneStaleSignals` and `pruneExhaustSignals` (for exhaust, use kind
  `temporal_result`, ts older than the window, uncited).
- Assert both complete without throwing AND the signal row is gone.
  With `PRAGMA foreign_keys=ON` this fails loudly the moment a new
  referencing table is missing from a cascade.

**M1.2 — DIAGNOSE FIRST.** Confirm whether the store connection enables
`PRAGMA foreign_keys` (grep `foreign_keys` in CIRStore.swift). If it is OFF,
the FK failure seen in production came through a different path (likely a
`defer_foreign_keys`/trigger nuance or it is ON) — record the actual
mechanism in the context doc, and make the test enable `PRAGMA
foreign_keys=ON` on its own connection so the guarantee holds regardless.

**Footprint:** new test file; possibly a small test-visibility annotation on
the two prune functions (keep `internal`, tests import `@testable`).

**Verification:** `swift test --filter CIRPruneCascadeCompleteness` green;
temporarily commenting out the `evaluation_gate` delete line makes it RED
(prove it catches the original bug — do this locally, do not commit the red
state).

**Completion keyword:** `M1_CASCADE_GUARD_COMPLETE`

---

### M2 — Fail-closed kind taxonomy in the ingest policy

**Why.** `handle_snapshot` recreated the 2026-06-10 failure mode in nine days
because every defense was an explicit kind list and a NEW kind defaulted to
full-citizen treatment (kept forever, never decayed, unreapable). Flip the
default: unknown = cheap tier.

**M2.1** In `CIRIngestPolicy` (mentu-engine/Sources/MentuEngine/
CIRIngestPolicy.swift), introduce an explicit registry of KNOWN
first-class kinds — start from `embeddableKinds` (line ~48) plus
`accountabilityKinds` plus the kinds with bespoke handling
(`consolidation`, `anomaly_detected`, `agent_crash`,
`elicitation_declined`, `steer_message`, `context_consumed`, and the
`prediction.*` prefix family). Then change the two defaults:
- `defaultHalfLifeDays(forKind:)` (line ~185): a normalized kind that is
  neither in the first-class registry nor already listed returns **7**, not
  nil. Known first-class kinds keep nil (no forced decay).
- `ageOnlyPrunableExhaustKinds` (added in `7a3f85a`, line ~46): becomes a
  computed policy: a kind qualifies for age-only reaping when it is NOT
  first-class AND NOT an accountability kind. Keep `handle_snapshot` and
  `temporal_result` as guaranteed members (regression pin).
  `CIRCompact` already threads `--exhaust-kinds` through; its default should
  now resolve from this policy (grep `parsedExhaustKinds` in
  CIRCommand.swift).

**M2.2** Emit visibility, not silence: the first time a given unknown kind is
ingested in a process lifetime, log one warning line (`Logger`, subsystem
`com.mentu.engine`) naming the kind and the applied defaults. No signal
emission (that would be exhaust about exhaust).

**M2.3** Tests in `CIRIngestPolicyTests.swift`: unknown kind → half-life 7 +
age-only-prunable; every registry kind → unchanged behavior (table-driven
over the full current kind census — pull the list from this doc's §0.1 db
kinds or from the existing test fixtures).

**Footprint:** `CIRIngestPolicy.swift`, `CIRCommand.swift` (default wiring),
`CIRIngestPolicyTests.swift`.

**Verification:** `swift test --filter CIRIngestPolicy` green; a synthetic
kind `made_up_kind_xyz` ingested into a temp store gets half-life 7 and is
collected by `pruneExhaustSignals` once >14d (test constructs the ts).

**Completion keyword:** `M2_FAILCLOSED_TAXONOMY_COMPLETE`

---

### M3 — Maintenance effectiveness telemetry + scheduled-skip repair

**Why.** Two silent failure modes coexisted: (1) the reaper "succeeded"
nightly while matching 2 of 356k rows — nothing compared reaped vs added;
(2) `--scheduled` skips when a writer is in flight (CIRCommand.swift,
`passiveCheckpoint` block ~1370), and on a machine with always-on writers a
skip streak can be indefinite. Make both measurable and bounded.

**M3.1 — Metrics line.** At the end of every `cir compact` run (scheduled and
manual), append one JSON line to `$MENTU_HOME/ops/cir-maintenance-metrics.jsonl`
(create dir; this is an ops file, deliberately OUTSIDE the CIR db — recording
maintenance into the substrate being maintained is the self-pollution
anti-pattern): `{ts, mode, skipped, db_bytes, wal_bytes, signals_total,
per_kind_top10, exhaust_deleted, stale_deleted, ineligible_embeddings,
duration_ms}`. Counts come cheap: `SELECT kind, COUNT(*) ... GROUP BY kind
ORDER BY 2 DESC LIMIT 10` post-prune.

**M3.2 — Net-growth tripwire.** After writing the line, read the last 7
entries; if `signals_total` grew monotonically across all of them AND total
exhaust deleted over the window is 0, ingest ONE `anomaly_detected` signal
(kind is already accept-listed as an anomaly worth keeping — see the comment
in `CIRIngestPolicy.telemetryKinds`) with a body naming the top-growing kind.
`anomaly_detected` is first-class (M2 registry) so it is retained.

**M3.3 — Skip bound.** In the `--scheduled` path, replace silent skip with:
retry `passiveCheckpoint` for up to 60 s (sleep 5 s between attempts); if
still busy, write the metrics line with `skipped: true` and exit 0 as today.
Then the tripwire naturally catches chronic skipping: 7 consecutive
`skipped:true` lines with zero deletions is exactly the M3.2 condition
(extend the M3.2 predicate: skip-streak ≥ 7 also fires).

**M3.4** Tests: metrics line schema (temp MENTU_HOME, run compact, parse the
line); tripwire predicate as a pure function over 7 synthetic entries
(extract it as a testable static).

**Footprint:** `CIRCommand.swift` (compact), possibly a small
`CIRMaintenanceMetrics.swift` helper, tests.

**Verification:** `swift test` for the new tests; on a temp store, two
compact runs produce two well-formed JSONL lines; `jq` parses them.

**Completion keyword:** `M3_EFFECTIVENESS_COMPLETE`

---

### M4 — Materialized accountability verdicts (the kernel fix)

**Why.** Every read of usage debt re-derives accountability by expanding
`CIRUsageMaintenancePolicy.accountable*SQL` — hundreds of lines of nested
`EXISTS`/`json_each` predicates — into SQL that SQLite must re-PARSE on every
call (the live CPU sample was parse-dominated), inside a recursive provenance
walk. The purge removed the amplifier (db size); the O(nodes × giant-parse)
cost is still there and returns as the db grows. Fix: compute each trust
event's accountability class ONCE, at write time, and make reads a column
filter.

**M4.1 — Schema v16.** Add nullable column `accountable_class TEXT` to
`trust_events` (values: `context_used | context_ignored | context_cooled |
doubt | contradicted | none`; NULL = not yet classified). Migration bumps
`currentSchemaVersion` 15 → 16 (follow the existing migration pattern —
grep `schema_version` / migration blocks in CIRStore.swift). Additive only
(Invariant 0.4).

**M4.2 — Write-time classification.** Wherever a trust event that the
predicates cover is inserted (`insertTrustEvent`, `insertTrustEventIfAbsent`,
`updateTrustEventConfidence` — grep call sites), evaluate the SAME predicate
SQL for just that row (a `WHERE te.rowid = last_insert_rowid() AND
<predicate>` probe, or refactor the predicate into a single-row query) and
stamp `accountable_class`. This keeps the predicate text as the single source
of truth — the column is a cache of its verdict, not a re-implementation.
NOTE the classification of an event can depend on its cause signal's body
(`cir_context_usage`), which is written BEFORE the trust event in
`CIRContextBrief.recordUsage` — verify order by reading that flow
(CIRContextBrief.swift ~1700–2160); if any path writes the cause after the
event, classify lazily (M4.3's backfill catches it).

**M4.3 — Backfill + repair job.** `cir compact` gains a bounded backfill:
classify up to N=20,000 NULL-class rows per run using the predicates
(oldest first). On the live db (~168k trust_events post-purge) full coverage
lands within ~9 nightly runs; manual `mentu cir compact` accelerates.

**M4.4 — Dual-read gate (the equivalence proof).** Add
`mentu cir verify-accountability [--sample N]`: samples N random classified
rows (default 5,000), re-evaluates the predicate SQL, compares to the column,
reports mismatches, exits non-zero on ANY. Run it on a temp copy of the live
db (VACUUM INTO snapshot) and on test fixtures. **Reads do not flip in this
milestone.** Escalation trigger (§1.5a) on any mismatch.

**M4.5 — Read flip, guarded.** Once M4.4 is clean: switch the hot readers —
`queryUsageDebt(signalIds:)` (CIRStore.swift:1272), the `event_counts` CTE in
`CIRContextBrief` candidate retrieval (~1030–1120), `CIRReranker`'s three
blocks (~700–1100), `countAccountableIgnoredEvents` /
`countAccountableUsedEvents`, `countUsageMaintenanceSignals` — to
`WHERE accountable_class = '<class>' OR (accountable_class IS NULL AND
<legacy predicate>)`. The NULL fallback keeps unclassified rows correct
during backfill; once M3's metrics show zero NULL rows, a later cleanup may
drop the fallback (out of scope here).

**Footprint:** `CIRStore.swift` (migration, classification, readers),
`CIRContextBrief.swift`, `CIRReranker.swift`, `CIRCommand.swift`
(verify-accountability, backfill), new tests
(`CIRAccountabilityMaterializationTests.swift`).

**Verification (mechanical):**
- `swift test` green including existing `CIRAccountabilityConformance*` and
  `CIRPositiveReuseAudit*` suites (they pin the semantics you must not move).
- `verify-accountability --sample 5000` exits 0 on a live-db snapshot.
- Timing probe: on the snapshot, time 200 sequential
  `queryUsageDebt(signalIds:)` calls (small test harness) before/after the
  flip; expect ≥5× improvement (parse cost gone).

**Completion keyword:** `M4_MATERIALIZED_VERDICTS_COMPLETE`

---

### M5 — Bounded source-chain eligibility walk

**Why.** `CIRRuntimeEvidencePolicy.sourceChainEligibleSignalIds`
(CIRRuntimeEvidencePolicy.swift:367) recurses per candidate with no reuse
across siblings, issuing `queryUsageDebt` + metadata + superseded queries at
every level. With 2,471 derived signals at avg fan-out 43 (max 996), one
brief can touch thousands of nodes. M4 makes each query cheap; M5 makes the
walk visit each node once.

**M5.1 — DIAGNOSE FIRST (semantics).** The cycle guard
(`visitingDerivedSignals`, lines 388–392) makes a node's verdict
PATH-DEPENDENT: a signal skipped because it appears on the current visiting
path could be eligible from a different root. Naive global memoization
changes results. Write two fixture graphs proving current behavior (a
diamond A→{B,C}→D and a cycle A→B→A) and pin them in tests BEFORE changing
anything.

**M5.2 — Safe memoization.** Within ONE top-level
`runtimeEligibleSignalIds` invocation, cache verdicts ONLY for nodes whose
entire subtree was evaluated without hitting the visiting-set guard (a
"clean" verdict). Nodes whose evaluation short-circuited on the guard are
NOT cached. Implement as an inout cache struct passed alongside
`visitingDerivedSignals`; public entry points construct it fresh (no
cross-call staleness).

**M5.3 — Batch the fan-out.** Inside `sourceChainEligibleSignalIds`, collect
ALL uncached first-level sources across the candidate set and issue ONE
`queryUsageDebt` / `querySignalMetadata` round for the batch before
recursing (per-level batching preserves per-candidate guard semantics —
recursion structure unchanged, only the queries coalesce).

**M5.4 — Depth/width tripwire.** Count nodes visited per top-level call; at
>10,000, stop expanding, treat unexpanded derived candidates as ineligible
(conservative direction — never grants eligibility it didn't prove), and log
one warning. Pin the constant in a `static let`.

**Footprint:** `CIRRuntimeEvidencePolicy.swift`, new
`CIRSourceChainWalkTests.swift`.

**Verification:** fixture-graph tests byte-identical verdicts pre/post
(diamond, cycle, and a 3-level chain with a debt-suppressed leaf);
`swift test` full CIR filter green; visited-node count on the diamond drops
from 6 to 4 (assert via injected counter).

**Completion keyword:** `M5_WALK_BOUNDED_COMPLETE`

---

### M6 — C7 telemetry off the hot path (and out of the substrate's face)

**Why.** `mentu-mcp` emits one `handle_snapshot` per handle via a synchronous
`execFileSync(mentu cir capture ...)` (cir-client.ts:115–131, emitter
c7-returnability.ts:56) and, in `captureCIRSignalWithEmbedding`
(cir-client.ts:189–203), a SECOND subprocess (`cir backfill-embeddings
--batch 1`) per capture. That is ~8,300 process spawns/day of telemetry
writing straight into the knowledge substrate — the self-pollution
anti-pattern plus a real latency tax on every MCP handle creation.

**M6.1 — Route through the pending drain.** The cross-surface path already
exists: producers append JSONL to `~/.mentu/cir-pending/` and the hourly
temporal `cir pending --ingest` drains through the ingest policy
(TemporalSeed.swift:126–137). Change mentu-mcp's `handle_snapshot` emission
to append to a per-session file
`~/.mentu/cir-pending/mcp-handles-<sessionid>.jsonl` (matching the drain's
expected line schema — read `CIRPendingCommand.swift` for the format)
instead of spawning `mentu`. Result: zero subprocess per handle, batch
ingest, taxonomy applied at drain time (post-M2 that means 7d half-life +
age-only reaping automatically).

**M6.2 — Delete the per-capture backfill.** Remove the `backfill-embeddings
--batch 1` subprocess from `captureCIRSignalWithEmbedding` (and the function
if it collapses into `captureCIRSignal`). Embedding backfill already runs
between engine steps (SequenceRunner.swift:4197–4210, gated) — per-capture
spawning is pure waste post-gate.

**M6.3 — C7 measurability check.** `CIRHandleReturnabilityEvaluator`
(engine) reads `handle_snapshot` signals. Confirm it reads from the CIR db
(not the pending files) and that hourly-batched arrival only shifts
event-time vs ingest-time. If the evaluator uses ingest timestamps for
returnability windows, switch it to the event's own `created_at` from the
body. If windows > 14 days are measured, that limit ALREADY moved in
`7a3f85a` — no new regime change from this milestone.
**HUMAN:** notify the epistemics owner that C7 telemetry becomes
hourly-batched (latency in signal availability, not semantics), referencing
`epistemics/instruments/2026-07-08-cir-exhaust-purge-regime-note.md`; a
one-line addendum there is their call. Escalation trigger §1.5c if
measurability would be lost outright.

**M6.4** Tests: mcp side — `npm test` unit for the pending-file writer
(schema, session scoping, fs failure = silent no-op preserving the fail-open
contract); engine side — a drain test ingesting a synthetic
mcp-handles file end-to-end into a temp store.

**Footprint:** `mentu-mcp/src/cir-client.ts`, `mentu-mcp/src/c7-returnability.ts`,
`mentu-mcp/src/__tests__/`, possibly `CIRPendingCommand.swift` (only if the
line schema needs a documented field), `CIRHandleReturnabilityEvaluator.swift`
(only per M6.3).

**Verification:** `npm test` green in mentu-mcp; engine drain test green;
grep proves no `execFileSync` remains in the handle-snapshot path.

**Completion keyword:** `M6_TELEMETRY_REROUTED_COMPLETE`

---

### M7 — Deployment drift guard + release

**Why.** The embedding gate landed in source on 2026-06-08 (`9862051`) and
was still being bypassed on 2026-07-08 by stale deployed binaries — a
30-day source-to-deployment gap nullified a data-policy fix. Make drift
visible and shrink it.

**M7.1 — Version stamp.** Embed the git short-hash at build time (SwiftPM
build-tool or a generated `EngineVersion.swift` refreshed by the Makefile
`build` target — pick the smallest mechanism that works offline). `mentu
--version` prints it. Every `cir compact` metrics line (M3.1) includes it —
maintenance history then shows exactly which binary did what.

**M7.2 — Daemon drift check.** `mentud` is a SEPARATE binary installed by
`scripts/install.sh` (not the engine Makefile) and runs for days.
DIAGNOSE FIRST: locate mentud's build source (grep the workspace; it is not
under `mentu-engine/`). Then implement the smallest honest check: on engine
startup of a long-lived command (`serve`/daemon paths), compare the
installed `~/.local/bin/mentu` stamp with the running process's own stamp;
if they differ, log a single loud warning ("installed engine is <hash>, this
process runs <hash> — restart to pick up policy changes"). Add a
`make install` epilogue line REMINDING about `launchctl kickstart` for
mentud (print, don't kickstart — killing a daemon mid-run is an operator
decision).

**M7.3 — Release.** Full `swift test`. `make install`. Smoke: `mentu
--version` shows the new stamp; `mentu cir compact --dry-run` on the live db
completes in seconds and prints the maintenance snapshot.

**Footprint:** `mentu-engine/Makefile`, version-stamp mechanism,
daemon-startup warning, `CIRCommand.swift` (metrics field).

**Verification:** stamp appears in `--version` and in a fresh metrics line;
full `swift test` green; dry-run smoke passes.

**Completion keyword:** `M7_DRIFT_GUARD_COMPLETE`

---

## 3. Acceptance (whole build)

1. All seven completion keywords reached, serially.
2. Full `swift test` + mentu-mcp `npm test` green at M7.
3. `verify-accountability` exits 0 on a live-db snapshot (M4.4) AND the
   read flip (M4.5) is active.
4. A synthetic unknown kind ingested on a temp store: half-life 7, reaped by
   age, never embedded, never spawns a subprocess (M2 + M6 jointly).
5. `$MENTU_HOME/ops/cir-maintenance-metrics.jsonl` accumulates one line per
   compact run, carrying the binary stamp (M3 + M7).
6. The epistemics owner has been notified for M6.3 (HUMAN step recorded in
   the context doc).
