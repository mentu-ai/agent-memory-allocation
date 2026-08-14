# Instrument note — boot-manifest gauge (new forward instrument, 2026-07-18)

**Declares**: a per-session gauge of the configured resident set (T0 content,
T1 pointers), for the agent-memory-allocation program
(`docs/BUILD-agent-memory-allocation-v1.md`). Gauge, not gate: it measures;
it changes no behavior, sets no threshold.

## Motivation (from the C27 run, same day)

`results/2026-07-18-c27-resident-set-utilization.md` established that the
per-session catalog denominator is **permanently unrecoverable retroactively**
(system prompts are not stored in transcripts; listing blocks found in 2 of
2,337). This gauge closes that denominator forward: from its deployment on,
every session records what was resident at boot.

## Mechanism

- **Hook**: Claude Code `SessionStart`, user-level (`~/.claude/settings.json`),
  `async: true` (never blocks a session), failure-swallowing (a session must
  never be affected by its gauge). Deployed 2026-07-18, alongside the
  pre-existing mentu session-start hook (untouched).
- **Script**: canonical source `analyses/shared/boot_manifest_hook.py`;
  deployed copy `~/.claude/hooks/boot-manifest.py`. Pipe-tested on a
  synthesized payload before wiring (exit 0; valid line emitted).
- **Output**: `~/.claude/telemetry/boot-manifests.jsonl`, append-only,
  schema `boot_manifest.v1`: ts, session_id, source, cwd/slug; contract files
  (path, size, sha16) incl. one level of `@`-includes; memory index presence /
  size / entry count / file count; skill catalog (names, count, description
  chars).

## Observer-effect analysis

Reads disk only. Writes **only** to its own JSONL — never CIR, never LACS,
never any substrate this corpus measures. The gauge's output file is itself a
declared instrument source and is excluded from being evidence about anything
other than residency (it must never be read *by* sessions as context — if that
ever happens, the gauge becomes a co-intervention and this note must be
amended with a regime boundary).

## Declared limits

1. **Configured vs. actual residency**: the gauge reconstructs the resident
   set from disk sources. The harness's internal listing differs in bounded
   ways — description truncation (`skillListingMaxDescChars`, default 1536)
   and a listing budget (`skillListingBudgetFraction`, default 1% of context
   window) cap what is actually resident; built-in harness skills and
   deferred-tool listings are not on disk and are missed. Direction: the
   gauge *over*states resident description volume and *under*counts built-in
   entries. Both bounded, both declared here.
2. **Interactive-first**: headless mentu lanes have their own resident-set
   telemetry (brief injection ledger, C1b apparatus); this gauge completes
   the grid for the interactive stratum specifically.
3. **Forward-only**: nothing before 2026-07-18 is recoverable; the C27
   retroactive route remains union-denominator by necessity.
4. **First live line lands at the next session start** after deployment;
   until then the JSONL contains only the pipe-test line
   (`session_id: pipe-test-000`), which analyzers must exclude.

## Relation to frozen work

- C27 re-run may use this gauge's per-session denominators for sessions
  after 2026-07-18; pre/post-gauge sessions are different instrument regimes —
  never pool denominators across the boundary without stating it.
- C26's tier assignments (T0/T1 membership per session) may consume this
  source for post-gauge sessions.
- The gauge satisfies the BUILD's forward-instrumentation rule (gauges before
  gates): it ships before any threshold is recommended anywhere.
