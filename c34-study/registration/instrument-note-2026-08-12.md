# Instrument note — public-corpus curation-vs-search replication

**Date**: 2026-08-12 · **Serves**: C34 · **Mode**: public corpus, snapshotted,
three-arm retrieval comparison at adjudicating power

Written at registration, before harness code, before the corpus snapshot,
before any question, and before any provider call. It records what the
instrument measures, what it records per run, and — the point of this note —
**what the parent instrument could not see**.

## What the parent instrument could not see

C29's harness recorded `Read` and `Grep`/`Glob` events for both agentic arms,
but computed hydration only for policy C (`adjudicate.py`, `if p == "C"`). Two
consequences reached the manuscript and had to be withdrawn in v1.2:

1. **Mis-routing was invisible.** C's 49 non-hydrated questions were described
   as answers issued from the index tier. The run records say 44 of the 49 read
   at least one file — the wrong one — and C issued 192 Read events to B's 174
   while locating the gold file on 53 questions to B's 82. The mechanism is a
   localization deficit, not a stopping rule
   (`paper/agent-memory-allocation/DISPOSITION-2026-08-12.md` Block 1).
2. **B's wrong-stop rate read as structurally zero.** It is not: under C's own
   frozen rule B is 13/102 = 12.75% on the paper corpus and 3/16 = 18.75% on the
   public demonstrator, where C is also 18.75%. The zero was an artifact of the
   arm-conditional computation, and the demonstrator record's claim that "B,
   which always reads, has no wrong-stop failure mode" was withdrawn.

C34's instrument closes both by construction: every scored B and C run carries a
hydration record, and every derived measure is computed by the same code path
for both arms.

## Measurement surface

The corpus is the `epistemics` repository's own public, operator-authored
English documents, selected by the frozen rule R in
`corpus/conjectures/c34-public-curation-vs-search-replication.md` §1 and
**snapshotted in full** into
`analyses/c34-public-curation-vs-search-replication/corpus-snapshot/` before any
question is authored.

Rule R is mechanical end to end: git-tracked `.md`, in eight named directories
or the repository root, ≥2,000 bytes, zero flags from the frozen client-content
audit (token set and Spanish-density regex copied verbatim from
`paper/agent-memory-allocation/sensitivity_audit.py` into the study's
`corpus_rule.py`), path free of `c29` and `c34`. Read-only enumeration at
registration: **142 files, 1,179,391 bytes**; floor 135 at the snapshot commit.

Snapshotting rather than hash-manifesting is Phase-H rule 6, adopted the same
day this study was registered after 1,996 of 2,337 hash-manifested transcripts
were found deleted, leaving C26, C27 and C28 permanently non-re-derivable. A
manifest proves integrity only while the files exist. The corpus of this study
is committed bytes, and the sandbox every policy run executes against is
assembled from those bytes with per-file hash verification — never from the
live working tree.

## Experimental intervention

Three arms over one frozen question set, one pinned answerer, one sandbox:

- **B grep-then-read** — tools `Grep`, `Glob`, `Read`;
- **C index-then-hydrate** — tool `Read` only, plus a materialized index of
  every corpus file (relative path + one-line digest);
- **D oracle-approx** — the gold file's content, no tools, single turn.

What varies across B and C is the *locator*: associative search over raw content
versus an authored digest index. Everything else — model, corpus bytes,
question, scoring rule, token accounting, sandbox — is held fixed. D bounds
minimal-sufficient cost at file granularity and is an approximation, not a
ceiling.

C29's flat-load arm A is not run: its 100,000-character dump reached 4 of 102
files, its attainable ceiling was 3.9%, and no frozen prediction references it
(registration deviation D-1).

## Recorded fields

Per run record, for every question × policy:

- question id, policy, gold relative path, gold answer, question type;
- pinned model requested and **model identity resolved by the provider**;
- final `ANSWER:` line and normalized-containment score;
- uncached input, cache-creation, cache-read and output tokens; derived total
  and marginal token counts; provider-reported cost, recorded but not used
  comparatively (C29's cost column could not be reconstructed from list prices
  and was withdrawn from the manuscript);
- turns, wall duration, error flag and error class;
- **hydration record, for B and C alike**: ordered `Read` paths; ordered
  `Grep`/`Glob` invocations with patterns; `read_count`; `first_read_path`;
  `located`; `first_read_is_gold`; `zero_read`;
- global call-counter position at dispatch.

Per study: the rule-R evaluation log for every candidate file with its accepting
or rejecting clause; `corpus-manifest.json` (path, size, sha256); the frozen
question set with per-question provenance (source path, generation-input
sha256); the digest index with per-entry provenance (frontmatter-extracted vs
generator-authored) and the generator token cost; the salted-selection record;
the smoke audit artifacts; and the call ledger by sub-ceiling.

## Derived measures

Computed by one code path for B and C: accuracy, error rate, localization rate,
first-read precision, non-hydrated rate, **wrong-stop rate** (incorrect and
gold file never read), mis-routed rate (incorrect, not located, ≥1 read) and
true-stop rate (incorrect, zero reads). The last two are the fields that
separate the two mechanisms the parent study confused, and they are the fields
the manuscript's §Invitation asks every replicator to record.

## Contamination and hygiene rules

Carried from C29 D6, with the snapshot rule added:

1. The question set is frozen by committed sha256 **before any policy run**;
   any policy-run record predating that commit voids the run set, with no
   partial salvage.
2. `--no-session-persistence` on every call: the study writes no transcript
   into any future corpus.
3. The sandbox is assembled from the committed snapshot, outside every measured
   substrate. Nothing writes to CIR, LACS, Mentu's database, or any workspace.
   No Mentu data is read at all, so the observer-effect rule is satisfied
   without further ceremony.
4. The generator receives frontmatter-stripped bodies only, by mechanical strip
   in committed code, so "generation did not use the summary layers" is provable
   by construction.
5. The orchestrating session authors no question, no digest and no answer. It
   may fix harness code before runs; it may never edit questions, digests or
   answers after the freeze commit.

## Failure modes this instrument must catch, and the dead runs that prove it

Phase-H rule 1: each gate ships with a constructed total failure it must catch,
in the same commit.

| gate | dead run it must fail |
|---|---|
| smoke audit | a hollow run in which every provider call is rejected before inference (zero input tokens, `is_error`), which C33's first pilot produced and its auditor passed |
| smoke audit | a run whose resolved model identity differs from the pinned identity |
| adjudicator | a fixture where every C answer is correct and no gold file was read — localization 0 with wrong-stop 0, neither collapsing into the other |
| adjudicator | a fixture with a missing hydration record on a scored B run, which must produce `instrument-insufficient`, not a silent zero |
| adjudicator | a fixture below the 100-scored floor, which must return `instrument-insufficient` before any prediction is evaluated |
| corpus snapshot | a file mutated after snapshot, which must fail sandbox hash verification |

Every zero this instrument reports carries its denominator and its
exercised-status (Phase-H rule 4): `not_exercised` and `zero_events` are
distinct outcomes and are labeled as such in the effect table.

## Cost of knowledge

Recorded per Phase-H rule 5, for the benefit of future designs. What produced
this instrument note: one external adversarial review, one disposition of 41
findings by a non-author agent, and the recomputation of 408 committed run
records — from which the mis-routing decomposition, the symmetric wrong-stop
rule, the unfrozen-measure defect in P4 and the starved flat-load arm all fell
out. None of it cost a provider call. The lesson is priced accordingly: the
fields that would have prevented the manuscript's two withdrawn claim sites were
already being recorded and simply were not computed for both arms.
