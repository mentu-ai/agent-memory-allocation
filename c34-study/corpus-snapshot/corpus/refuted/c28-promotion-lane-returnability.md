---
id: c28
name: promotion-lane-returnability
status: tested
registered: 2026-07-18
lineage:
  - docs/BUILD-agent-memory-allocation-v1.md
  - instruments/2026-07-18-claude-code-transcript-instrument.md
  - corpus/conjectures/c26-residency-determined-return.md   # supplies the tier definitions
  - paper/return-base-rate-paper.md                         # the T3 contrast (0.0222%)
verdict: refuted
result: results/2026-07-18-c28-promotion-lane-returnability.md
---

# C28 — Promotion-lane returnability (does the memory directory actually return?)

## Claim

Promotion works, and it works through pointer residency. A fact written to the
durable memory directory (`<project>/memory/*.md`) and indexed in the boot-loaded
`MEMORY.md` returns in later sessions at rates orders of magnitude above ambient
paged artifacts — because promotion buys a **resident pointer**, not because the
content is better. The promotion policy is the one working return lane in the
current allocation architecture: capture-without-promotion goes to T2/T3 and
effectively never returns; capture-with-promotion goes to T1 and does.

The corollary claim: memory files that lack an index line in `MEMORY.md` (orphans)
return at rates far closer to ambient T2 than their indexed siblings — same
directory, same content class, no pointer — which would isolate the pointer as the
active ingredient.

## Origin

Registered from the agent-memory-allocation program (BUILD doc, 2026-07-18). The
promotion lane is the harness's own answer to the return problem: 453 memory files
exist across 157 projects (census, instrument note), each written by a past session
that judged a fact durable. Whether that judgment pays — whether promoted facts are
ever recalled — has never been measured. One observed instance motivated the
conjecture: a commit-authorship memory written 2026-07-06 was read and obeyed by a
session twelve days later. C28 asks whether that is the norm or the exception.

## Operationalization

**Dataset**: manifest-listed transcripts + memory directories (instrument note
2026-07-18). For each memory file: creation time (git/birthtime/first mention),
whether `MEMORY.md` indexes it (and since when, where reconstructable), and every
later same-project session `Read` of it.

**Unit**: one memory file, observed from creation to corpus freeze; eligible
sessions = same-project sessions strictly after creation, excluding the session
that wrote it.

**Measures**: ever-re-read fraction (share of memory files read in ≥1 later
session); per-file subsequent-session read rate (median, with intervals); indexed
vs orphan contrast; recall latency (days from write to first re-read).

**Controls**: project session volume (a file in a busy project has more chances —
rates are per-eligible-session, and project is a covariate), file age, month
cohort, interactive/headless strata.

## Predictions (frozen 2026-07-18, before any probe exists)

- **P1 (the lane works)**: ≥25% of memory files with ≥10 eligible sessions are
  re-read at least once within the corpus window.
- **P2 (rate, commensurable with T3)**: the median per-file subsequent-session
  read rate is ≥1% — ≥45× the frozen T3 organic access baseline (0.0222%).
- **P3 (the pointer is the ingredient)**: indexed files are re-read at ≥3× the
  ever-re-read fraction of orphan files, given ≥20 orphans exist in the corpus;
  with fewer than 20 orphans this prediction is reported as not evaluable.
- **P4 (bounded, not resident)**: the promotion lane stays well below T0 — the
  median per-file session read rate is <20%; promotion buys reachability, not
  omnipresence. (This bound protects the tier model: if memory files behaved like
  T0, the T1 tier definition would be wrong.)

## Falsification criteria

- Ever-re-read fraction ≤10% and median rate ≤10× the T3 baseline → **refuted**:
  the promotion lane does not function as a return mechanism, and the paper's
  "promotion works via pointer residency" line must be withdrawn — with the
  allocation-tier frame (C26) then predicting the harness's memory feature is
  mostly ritual.
- The lane works but the indexed-vs-orphan contrast is absent (<1.5×) →
  **revised**: promotion works through some channel other than the pointer
  (e.g., content quality or recency), weakening C26's mechanism story.
- Creation times or index membership cannot be reconstructed deterministically →
  **instrument insufficient**.

## Gate

Verdict only from `analyses/c28-promotion-lane-returnability/analyze.py`,
committed after the M0 registration commit, manifest-only inputs, deterministic
re-run. Coverage floors: ≥100 memory files with ≥30 days of post-creation corpus
and ≥10 eligible sessions each. Below floor → `instrument insufficient`.

## Known limitations

- `MEMORY.md` content is itself boot-loaded: a fact short enough to live in the
  index line returns without any file read. Such index-only recalls are invisible
  to this instrument and would *understate* the lane's value — the bias direction
  is declared and runs against P1/P2, not for them.
- Re-read proves retrieval, not that the memory changed the session's behavior
  (instrument note limit 3).
- Memory files written and read by scheduled/headless lanes measure recipe
  policy, not recall; strata are mandatory.
- 453 files across 157 projects is thin per-project; pooled estimates carry
  project heterogeneity — intervals and per-project breakdowns are required
  outputs, not options.
