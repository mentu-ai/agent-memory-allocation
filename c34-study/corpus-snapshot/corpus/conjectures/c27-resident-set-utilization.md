---
id: c27
name: resident-set-utilization
status: operationalized
registered: 2026-07-18
lineage:
  - docs/BUILD-agent-memory-allocation-v1.md
  - instruments/2026-07-18-claude-code-transcript-instrument.md
  - corpus/conjectures/c22-operational-surface-debt.md   # surface-debt sibling at the harness tier
verdict: null
result: null
tracking:                      # machine-updated by observatory beats only
  last_beat: 2026-07-18
  note: "registered at M0 of the agent-memory-allocation program; probe is M2.1 (cheapest first); corpus frozen at the M0 registration commit"
---

# C27 — Resident-set utilization (is the boot image mostly dead weight?)

## Claim

The boot-resident allocation of a modern agent harness is mostly unexercised. The
skill catalog — every listed skill's name and trigger description, paid into
context at every session start — follows a steep concentration law: a small head
of skills accounts for nearly all invocations, a majority of listed skills are
never invoked at all, and most sessions invoke none. The resident set is sized by
accretion (what has been installed), not by utilization (what gets used), and the
gap between the two is the harness-tier analogue of structural waste: attention
paid every session for capability that never fires.

This does not claim the listing is worthless — an uninvoked skill may still shape
behavior by existing in context (a visibility effect this instrument cannot see,
declared below). It claims the *invocation* distribution, the one measurable
utilization signal, is extremely concentrated.

## Origin

Registered from the agent-memory-allocation program (BUILD doc, 2026-07-18). The
motivating observation: the current harness lists on the order of 150 skills in
every session of this project, while informal experience suggests most sessions
invoke zero or one. Nobody in the context-engineering literature measures the
configured tier — window waste has a number (Mason 2026: 21.8%), org-structure
waste has a number (the EJIS structural-waste work), but boot-image waste has
none. C27 produces the first one, from 2,368 archived sessions.

## Operationalization

**Dataset**: manifest-listed session transcripts (instrument note 2026-07-18).
Signal: `Skill` tool_use events (skill name, session, timestamp) vs. the resident
catalog denominator.

**Denominator (in declared preference order)**:

1. Per-session catalog reconstructed from the transcript's own listing, when
   recoverable — the correct denominator.
2. Union catalog over the corpus window, flagged as biased (understates
   utilization for late-added skills); month cohorts partially compensate.
3. Neither recoverable → `instrument insufficient`.

**Measures**: ever-invoked fraction of the catalog (pooled and per project);
invocation concentration (share of invocations by top-5 skills; full rank curve);
per-session invocation count distribution; catalog-listing token overhead per
session (measured from reconstructed listings where available) and its share
attributable to never-invoked skills.

**Strata**: interactive vs headless sessions (headless reported separately,
never pooled); month cohort; project.

## Predictions (frozen 2026-07-18, before any probe exists)

- **P1 (dead majority)**: ≤15% of the catalog (union denominator; ≤20% under
  per-session denominators) is ever invoked across the frozen corpus.
- **P2 (concentration)**: the top-5 invoked skills account for ≥60% of all
  invocations.
- **P3 (quiet sessions)**: ≥60% of interactive sessions invoke zero skills.
- **P4 (waste share)**: never-invoked skills account for ≥70% of catalog-listing
  tokens paid across the corpus (computable only under denominator 1; otherwise
  reported as a bounded estimate with the bias direction stated).

## Falsification criteria

- Ever-invoked fraction >40%, or top-5 share <30% (utilization broad and flat)
  → **refuted**; the resident set is earning its keep and the "dead boot image"
  framing must be withdrawn from the paper.
- P1 holds under the union denominator but fails under per-session denominators
  → **revised**: concentration is an artifact of catalog growth, not of
  utilization behavior.
- No denominator recoverable (rule above) → **instrument insufficient**.

## Gate

Verdict only from `analyses/c27-resident-set-utilization/analyze.py`, committed
after the M0 registration commit, manifest-only inputs, deterministic re-run.
Coverage floors: ≥500 interactive sessions spanning ≥2 month cohorts and ≥10
projects. This is M2.1 — the cheapest probe, and it runs first.

## Known limitations

- Invocation is not the only value channel: a listed-but-uninvoked skill may
  still steer behavior by being visible in context (the model routes differently
  knowing a capability exists). This instrument cannot measure the visibility
  effect; the conjecture is scoped to invocation utilization and the paper must
  carry that scope note wherever P1–P4 are cited.
- Skill names occasionally change across harness versions; the analyzer must
  normalize renames it can detect from the corpus and report unresolvable ones.
- Headless runs may auto-invoke skills through recipes; that stratum measures a
  different policy and is reported separately by construction.
