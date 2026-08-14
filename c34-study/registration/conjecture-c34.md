---
id: c34
name: public-curation-vs-search-replication
status: tested
registered: 2026-08-12
lineage:
  - corpus/supported/c29-curation-vs-search-sufficiency.md          # parent; SUPPORTED 2026-07-19, untouched by this registration
  - results/2026-07-19-c29-curation-vs-search-sufficiency.md        # the adjudicated result this study replicates in public
  - analyses/c29-curation-vs-search-sufficiency/DESIGN.md           # D1–D6 design decisions carried forward verbatim except where named
  - analyses/c29-curation-vs-search-sufficiency/adjudicate.py       # the frozen thresholds reused here
  - paper/agent-memory-allocation/DISPOSITION-2026-08-12.md         # §D1 mis-routing, §B1 asymmetric P3, §A5 unfrozen measure — the three defects this design repairs
  - paper/agent-memory-allocation/paper-v1.2.md                     # §6.5, §7 Limits (b/b′), §Invitation — the staked prediction
  - paper/agent-memory-allocation/repro-kit/DEMONSTRATOR-ADDENDUM-2026-08-12.md  # the underpowered demonstrator this study supersedes
  - docs/PLAN-hardening-and-retest-2026-08-12.md                    # Phase-H rules 1–6, esp. rule 6 (hash-freezing is not archiving)
  - docs/BUILD-c34-public-curation-vs-search-replication-v1.md
  - instruments/2026-08-12-c34-public-corpus-replication-instrument.md
verdict: revised
result: results/2026-08-14-c34-public-curation-vs-search-replication.md
tracking:                      # machine-updated by observatory beats only
  last_beat: 2026-08-12
  note: "registered before any harness code, corpus snapshot, question set, or provider call; public corpus only; adjudicates ONLY on run records produced after the question-freeze commit; C29's verdict, thresholds, runs and effect table are untouched"
---

# C34 — Curation-vs-search sufficiency, replicated in public at power

## Claim

C29's finding holds on a **public, releasable corpus at adjudicating power**:
associative search over raw content followed by full reads (**B**
grep-then-read) matches or beats curated layered disclosure (**C**
index-then-hydrate) on answer accuracy, at a token cost within the registered
bound; and the curated index pays for its cheap tier with a **localization
deficit** — it routes the policy to the wrong document, or to no document,
more often than associative search does, and the answers issued without
hydrating the gold file are overwhelmingly wrong.

The mechanism clause is stated in the corrected form the parent study's
disposition established. C29's manuscript first read C's deficit as *premature
stopping* (answering from the digest tier). The run records refuted that
reading: of the 49 questions where C never read the gold file, **44 read at
least one file — the wrong one**, and C issued *more* Read events than B (192
vs 174) while locating the gold file on *fewer* questions (53 vs 82)
(`DISPOSITION-2026-08-12.md` Block 1). C34 therefore predicts and instruments
**mis-routing**, not stopping, and measures the two apart on every question in
both arms.

## What this study is for

C29 is adjudicated `supported`, and its evidence is 408 committed run records
over a corpus that is **85% third-party client material and cannot be
released**. The public artifact that ships in its place — the 16-question
`repro-kit/` demonstrator — falls below C29's own frozen scored-question floor
and, run through the committed adjudicator, returns `INSTRUMENT INSUFFICIENT`.
It adjudicates nothing, its frozen P3 fails and reverses on it, and it is not
an independent replication: its 17 documents are the English half of C29's own
corpus (`DEMONSTRATOR-ADDENDUM-2026-08-12.md`; paper §7 Limits (b′)).

C34 is the **release-blocking successor**: a study a reader can re-run in full,
on documents the reader holds in full, at a question count that clears the
frozen floor with margin. It buys three things the demonstrator cannot — power,
public re-runnability, and a corpus that ships with the paper — and it buys
**none** of a fourth: it does not remove the single-operator bound (see Known
limitations). On adjudication its result enters *Agent Memory Allocation* v2 at
claim-site prominence, whatever the result is.

## Non-amendment declaration

This registration amends nothing. C29's frozen claim, predictions,
falsification criteria, verdict, effect table, run records and results document
stand exactly as adjudicated, and no analysis registered here can move them.
The `repro-kit/` demonstrator record and its 2026-08-12 addendum likewise stand
unchanged; C34 supersedes the demonstrator's *role* in the public bundle
without editing its artifacts (essay 2026-08-12, lesson 6: supersede, never
amend).

Where C34's criteria differ from C29's frozen criteria, the difference is
named as a change, with its reason, in **§Registered deviations from C29**,
following the C33 v2/v3/v4 correction discipline. Nothing is changed silently
and nothing is changed after data exist: this registration precedes the harness,
the corpus snapshot, the question set, and every provider call.

## Operationalization (frozen at registration)

### 1. Corpus — public, rule-selected, and snapshotted

**Eligibility rule R (frozen).** A file is an eligible corpus member at the
snapshot commit `S` iff all of the following hold:

1. it is git-tracked in the `epistemics` repository at `S`;
2. its path ends in `.md`;
3. its path is at the repository root, or under one of `applications/`,
   `corpus/`, `docs/`, `essays/`, `instruments/`, `lineage/`, `observatory/`,
   `results/`;
4. its size is ≥ 2,000 bytes;
5. it passes the client-content audit with **zero flags** — no token of the
   frozen third-party token set appears (case-insensitive substring) and the
   frozen Spanish-marker regex matches fewer than 20 times. The token set and
   regex are copied **verbatim** from `paper/agent-memory-allocation/
   sensitivity_audit.py` into the study's own `corpus_rule.py`, so the rule is
   self-contained in the public bundle and needs no withheld file to re-run;
6. its path does not contain `c29` or `c34`, and it is not under
   `analyses/c34-public-curation-vs-search-replication/`.

Clause 3 excludes `paper/` (which holds the manuscript under test, the
withheld-corpus audit, and the demonstrator) and `analyses/` (which holds the
harnesses). Clause 6 removes every document *about* this study or its parent
conjecture from the corpus the study measures. Clause 5 mechanically excludes
the five repository files that carry client tokens or Spanish operational
density, including C29's own conjecture file.

**Provenance and releasability.** The existing public corpus is 17
operator-owned English methodology documents from `docs/`, `docs/escalations/`,
`docs/referee/` and `essays/`, audited free of third-party content on
2026-07-20 (`repro-kit/public-corpus.txt`). Rule R extends **from exactly that
family**: same repository, same author, same license position, same audit,
same language. Every added document is releasable on the same terms as the
original 17, and clause 5 is the mechanism that guarantees it.

**Enumeration at registration** (read-only, this commit): rule R yields
**142 files, 1,179,391 bytes**, rejecting 3 candidates on size, 5 on the
client-content audit (including C29's own conjecture file, which names the
client workspace) and 4 on self-reference. This is an empirical enumeration of a
surface we control, taken before the rule is frozen (Phase-H rule 3). The
repository grows, so `S` will yield at least this many.

**Floor:** if rule R yields fewer than **135** files at `S`, the study stops
before any generation call and reports the count; no clause of R is relaxed to
reach the floor. **Ceiling:** if rule R yields more than **170** files at `S`,
the corpus is a salted subsample of exactly 170 drawn by `c34-corpus-v1:`, so
that the generation and digest-authoring sub-ceilings below bind; the full
eligibility log is committed either way. Between 135 and 170 the corpus is every
eligible file — no sampling, and therefore no selection to defend.

**Snapshot, not a manifest** (Phase-H rule 6 — hash-freezing is not archiving).
Before any question is authored, the complete bytes of every eligible file are
copied into `analyses/c34-public-curation-vs-search-replication/corpus-snapshot/`
preserving relative paths, and committed, alongside `corpus-manifest.json`
(path, size, sha256 per file) and the rule-R evaluation log for every candidate
considered, including rejections and the clause that rejected them. All policy
runs execute against a sandbox assembled **from the snapshot**, hash-verified
per file, never from the live tree. C26/C27/C28 were hash-frozen and are now
permanently non-re-derivable because 1,996 of 2,337 manifested transcripts were
deleted by harness rotation (§X1). This study's corpus cannot suffer that,
because its corpus is committed.

### 2. Question set

**Contract (carried from C29 D4).** One factual question per eligible corpus
file, whose answer is an **exact contiguous string from the body**, 3–15 words,
generator-labeled `lookup` or `synthesis`, with per-question provenance (source
path, generation-input sha256). Before freezing, the harness mechanically
validates that the normalized answer string occurs in the source body;
non-occurring candidates are dropped and counted. One regeneration pass is
permitted for dropped files, then the yield is reported as it stands.

**Generation exposure (carried from C29 D3).** The generator receives
**frontmatter-stripped bodies only**, by the committed mechanical strip, so
"generation did not use the summary layers" remains provable by construction
rather than asserted. The generator is a different model from the answerer. The
orchestrating session authors no question, no digest, and no answer.

**Selection and split.** From the validated pool, exactly **N = 120**
confirmatory questions are drawn by a frozen salt, `c34-confirmatory-v1:`
(sha256 of salt + question id, ascending, first 120); then exactly **10** smoke
questions are drawn from the remainder by `c34-smoke-v1:`. Salts are fixed here,
before any question exists, and never depend on outcomes. Shortfall rule,
frozen:

- validated ≥ 130 → N = 120 confirmatory, 10 smoke;
- 115 ≤ validated < 130 → 10 smoke, confirmatory = validated − 10 (≥ 105),
  recorded as a shortfall with its exact number;
- validated < 115 → **stop before any policy run**; seal
  `instrument-insufficient`, reason `question_yield_shortfall`.

The ≥100 scored-question floor never moves under any branch.

**Why N = 120.** The frozen floor is ≥100 *scored* questions per policy for B,
C and D. Scored counts fall below N only through unrecovered errors. C29
recorded 95 error records across 408 runs (71 provider session-limit refusals,
24 subprocess timeouts) and recovered all of them to **0 errors** under its
committed retry rule. N = 120 leaves 20 questions (16.7%) of headroom against a
residual-error risk that the parent study drove to zero, and it fixes the
provider-call arithmetic in advance. On power: at 120 per arm, two-sided
two-proportion power against C29's own B-vs-C margin (72.5% vs 47.1%) is
**98.4%**, and 80% power is reached at an **18.0 pp** difference (around a 60%
baseline); at the bare floor of 100 the same figures are 96.2% and 19.7 pp.
These are design statistics only — adjudication is against the frozen point
thresholds, never against a p-value — and they are recorded here so that a null
is interpretable:
at this N a failure of P1 or P3′ is informative rather than merely underpowered,
which is exactly what the 16-question demonstrator (19.0% power) could not
offer.

**Freeze.** `questions-<date>.json` and `index-<date>.json`, with their sha256
digests, are committed **before any policy run**. Any policy run whose record
predates that commit voids the run set with no partial salvage (C29's frozen
contamination rule, carried verbatim).

### 3. Policies — three arms, symmetrically instrumented

Same answerer model, same pinned version, same token accounting, same sandbox.

- **B grep-then-read**: agentic in the sandbox; tools `Grep`, `Glob`, `Read`;
  instructed to search, read hits, answer.
- **C index-then-hydrate**: agentic in the sandbox; tool `Read` only; prompt
  carries the materialized index (per file: relative path + one-line digest —
  the file's own frontmatter `summary`/`description`/`title` where mechanically
  extractable, else a generator-authored one-liner). Instructed to consult the
  index, hydrate the fewest files necessary, answer. Authoring cost is recorded
  and reported both amortized and unamortized.
- **D oracle-approx**: the answerer given exactly the gold file's content, no
  tools, single turn. Bounds minimal-sufficient cost from above at file
  granularity. **D is an approximation, never a ceiling** — on C29's own data a
  subset of C exceeded it.

**A (flat-load) is not run.** See deviation D-1.

**Per-question hydration record (frozen; the §D1 repair).** For B and C alike,
every run record carries: the ordered list of `Read` file paths; the ordered
list of `Grep`/`Glob` invocations with their patterns; `read_count`;
`first_read_path`; `located` (any recorded read path ends with or contains the
question's gold relative path — C29's committed hydration rule, unchanged);
`first_read_is_gold`; and `zero_read`. These fields are what separate
mis-routing from stopping, and C29's harness recorded them for C only. Recording
them for both arms is what makes the symmetric rules below computable.

**Derived measures, computed identically for B and C:**

| measure | definition |
|---|---|
| accuracy | normalized containment of the gold string in the final `ANSWER:` line |
| error rate | 1 − accuracy |
| localization rate | `located` / scored |
| first-read precision | `first_read_is_gold` / scored |
| non-hydrated rate | `not located` / scored |
| **wrong-stop rate** | incorrect **and** not `located`, / scored |
| mis-routed rate | incorrect and not `located` and `read_count` ≥ 1, / scored |
| true-stop rate | incorrect and `zero_read`, / scored |

Token accounting (frozen, from the parent harness): **total tokens** =
uncached input + cache-creation + cache-read + output; **marginal tokens** =
uncached input + cache-creation + output. Both are reported for every arm;
each frozen prediction names which one it is adjudicated on.

### 4. Models and budget

**Answerer (all policies):** `claude-haiku-4-5-20251001`.
**Generator (questions + digests):** `claude-sonnet-5`.
Both via `claude -p`, `--no-session-persistence` on every call, exactly as
C29 pinned them. Pinning the parent's models is what makes C34 comparable to
C29 rather than merely adjacent.

If the pinned answerer is unavailable at run time, the study does **not**
substitute silently: it either seals `instrument-insufficient` with reason
`pinned_answerer_unavailable`, or a dated correction registers the closest
available model, states the difference, and precedes every confirmatory call.
Availability is established at the two-call reality probe below, not assumed
(Phase-H rule 3).

**Registered global provider-call ceiling: 950 calls**, with non-transferable
sub-ceilings:

| purpose | arithmetic | calls |
|---|---|---|
| reality probe (model availability + schema acceptance) | 1 generator + 1 answerer | 2 |
| question generation | 1 per eligible file, cap | 170 |
| regeneration pass for dropped files | cap | 45 |
| digest authoring for C's index | 1 per file lacking an extractable frontmatter digest, cap | 170 |
| excluded smoke set | 10 questions × 3 policies | 30 |
| confirmatory pass | 120 questions × 3 policies | 360 |
| retry reserve (registered error classes only) | non-transferable | 150 |
| **total** | | **927** |

Ceiling 950; 23 calls of slack. Unused sub-ceilings are never reassigned. The
counter is checked and durably recorded before every call. If the ceiling is
reached before the confirmatory pass completes, the study seals
`instrument-insufficient` with reason `registered_budget_exhausted`; the ceiling
is never raised, and no threshold is relaxed to fit the remaining budget.

**Retry semantics (carried from C29, tightened).** Only records flagged as
errors may be retried, and only for registered infrastructure classes: provider
session-limit refusal, transport failure before any assistant content, and
subprocess timeout. **A scored answer is never re-rolled.** Every retry is
counted against the reserve and recorded with its class. Any retry rule change
must be committed before the retried pass, as C29 committed its 420→900 s
timeout amendment pre-verdict.

**Excluded smoke set (C33-style).** The 10 smoke questions run all three
policies (30 calls) and are audited before any confirmatory call. Smoke
questions are permanently barred from adjudication, from every denominator, and
from the effect table. The smoke audit must verify, mechanically: nonzero input
tokens on every call (no request rejected at the API boundary), the resolved
model identity equals the pinned identity on every call, a hydration record
present for every B and C run, the corpus sandbox hash-verifying against the
snapshot, and the adjudicator running end-to-end on the smoke records. Per
Phase-H rule 1 the audit ships with its **dead runs**: a constructed hollow run
(all calls rejected before inference, zero tokens) that the audit must fail, and
an adjudicator fixture in which every C answer is correct while no gold file was
read, which must yield localization 0 and wrong-stop 0 without either being
mistaken for the other.

## Predictions (frozen 2026-08-12, before any harness code, corpus snapshot, question, or provider call)

- **P1 (accuracy parity)** — carried verbatim from C29: `acc(B) ≥ acc(C) − 3
  percentage points`.
- **P2 (token order)** — carried verbatim from C29, on **totals**, as C29's
  text names: `total tokens(B) ≤ 2 × unamortized total tokens(C)`.
- **P3′ (symmetric wrong-stop tax)** — `wrong-stop rate(C) ≥ wrong-stop
  rate(B)`, both computed under the identical frozen rule: **incorrect AND the
  gold file was never read**. See deviation D-2.
- **P4 (headroom vs the oracle approximation)**, on **marginal tokens**:
  `marginal(B) ≥ 3 × marginal(D)` and `marginal(C) ≥ 3 × marginal(D)`. See
  deviation D-3.
- **P5 (localization advantage)** — the prediction the manuscript publicly
  stakes on replication: `localization rate(B) > localization rate(C)`, **and**
  among non-hydrated answers pooled across B and C, ≥80% are incorrect. See
  deviation D-5.

Non-adjudicating quantities reported alongside, for comparability with C29 and
for the next reader: C29's asymmetric P3 as originally frozen (C's wrong-stop
rate vs B's wrong-*answer* rate); P2 and P4 on the measure each is *not*
adjudicated on; the `lookup`/`synthesis` regime split; first-read precision;
the mis-routed / true-stop decomposition; per-arm error rates with Fisher exact
p-values; and C's authoring cost amortized and unamortized.

## Registered deviations from C29's frozen criteria

Each is a change from the parent study's frozen design, named here with its
reason, before any C34 data exist.

**D-1 — the flat-load arm A is dropped.** *Reason:* C29's A was budget-starved,
not informative. Its 100,000-character dump reached **4 of 102 corpus files**
and contained the gold string for 4 of 102 questions, so its attainable ceiling
was 3.9% and it scored 3 (§A13). The manuscript's reading of A has been
withdrawn and A supports no claim about flat loading. No frozen prediction in
C29 or C34 references A: P1–P3 concern B and C, P4 and the floor concern B, C
and D. Dropping A therefore changes no adjudication and saves 120 provider
calls. A corrected flat-load arm would need a budget scaled to the corpus, which
is a different experiment and is not registered here.

**D-2 — P3 is made symmetric.** *Reason:* C29's frozen P3 compares C's
wrong-stop *rate* against B's wrong-*answer* rate — a subset against a superset,
so it is close to unfalsifiable in the direction it was written (external review
§A2; disposition Block 1 "A symmetric P3, which the paper should have
reported"). The asymmetry also produced the demonstrator's most misleading
claim: `DEMONSTRATOR-RESULT.md` recorded B's wrong-stop rate as structurally
zero, when it is zero only because the harness computed wrong-stop under
`if p == "C"`. Under the symmetric rule B's rate is **12.75%** on C29's corpus
and **18.75%** on the demonstrator's, where C's is **18.75%** — identical. The
original asymmetric comparison is **acknowledged, retained and reported** as a
non-adjudicating comparability statistic; only the adjudicating form changes.

**D-3 — P4 names its measure, and the measure is marginal tokens.** *Reason:*
C29's P4 named no measure and its outcome flips with the choice: on totals
9.1× and 6.5× (pass), on marginal tokens **2.85× for B** (fail). The
manuscript recorded this as a defect in method and the rule the program owes
itself — *freeze the measure with the threshold* (§6.5, §A5). Marginal tokens
are the policy-attributable measure: cache reads are 90.0% of B's total against
29.7% of A's, and that overhead is nested-CLI system-prompt cost that differs by
arm for reasons unrelated to policy, as the parent harness notes where it
separates the components. Registering P4 on marginal tokens is the **harder**
reading — it is the one under which C29's own B would have failed — which is
the direction that cannot be outcome-shopping. Totals are reported alongside,
non-adjudicating.

**D-4 — the verdict map is made total.** *Reason:* C29's adjudicator emits
`PARTIAL — HELD OPEN` for combinations it does not classify, which is not one of
the corpus's admissible verdicts. C34 registers a complete precedence (below) so
that every reachable outcome maps to `supported`, `refuted`, `revised`,
`instrument-insufficient`, or `void`, with a machine reason. No threshold
changes; only the mapping of threshold outcomes to verdict words.

**D-5 — P5 is added.** *Reason:* it is the prediction the manuscript stakes on
replication in §Invitation, and the mechanism C34 exists to test in public.
Adding it makes `supported` strictly harder to reach than under C29's frozen
set. This is an addition, not a change to any inherited criterion.

**D-6 — hydration records are required for both arms.** *Reason:* the §D1
finding. C29 recorded reads for both arms but computed hydration only for C, so
the manuscript could not tell mis-routing from stopping and read it wrong at two
claim sites. Under C34 a missing hydration record on any scored B or C run is a
floor failure, not a footnote.

Everything else is carried unchanged: the answerer and generator identities,
`--no-session-persistence`, the sandbox-outside-every-measured-substrate rule,
the exact-substring question contract, the mechanical answer validation, the
normalized-containment scoring rule, the frontmatter-strip generation rule, the
gold-file hydration rule, the ≥100 scored-question floor, the contamination-voids
-the-run rule, the amortized/unamortized authoring-cost reporting, and P1 and P2
verbatim.

## Falsification and adjudication (frozen)

Mechanical, by `analyses/c34-public-curation-vs-search-replication/adjudicate.py`,
committed before the first policy run and operating only on committed run
records plus the frozen question set. First matching clause wins.

1. **void** — question-set contamination discovered (the generator saw digest
   or index content; any policy-run record predates the question-freeze commit).
   The run set is void; regenerate under a new dated harness. **No partial
   salvage.** (C29's frozen rule.)
2. **instrument-insufficient** — any of: fewer than 100 scored questions for any
   of B, C, D; a corpus-snapshot hash mismatch; a missing hydration record on
   any scored B or C run; a resolved model identity differing from the pinned
   identity on any scored call; the question-yield shortfall branch
   (`validated < 115`); rule R yielding fewer than 135 files at `S`; or the
   registered call ceiling exhausted before the confirmatory pass completes.
   Machine reason names which.
3. **refuted** — `acc(C) − acc(B) > 3 pp` **and** amortized total tokens(C)
   ≤ 0.5 × total tokens(B). Curation dominates: the paper must present layered
   disclosure as the superior policy wherever layers exist. (C29's frozen
   refutation trigger, verbatim.)
4. **supported** — P1 ∧ P2 ∧ P3′ ∧ P4 ∧ P5 all pass, with the floors met.
5. **revised** — every other outcome, with a machine reason enumerating each
   failed prediction. Named single-failure reasons:
   - P1 fails without triggering clause 3 → `accuracy_reversal_without_cost_dominance`
   - P2 fails, or total(B) > 5 × total(C) → `search_accurate_but_token_profligate`
   - P3′ fails → `no_wrong_stop_tax_at_power`
   - P4 fails → `headroom_not_established_on_marginal_tokens`
   - P5 fails → `localization_advantage_not_reproduced`

**A B–C tie, or a reversal, is a reportable finding — not a study failure.**
The demonstrator, at n = 16, showed B and C identical on accuracy (10/16 each),
on localization (12/16 each) and on symmetric wrong-stop (3/16 each). At n = 120
that pattern is resolvable, and if it is what the public corpus produces then
`revised` with reason `no_wrong_stop_tax_at_power` or
`localization_advantage_not_reproduced` is the honest verdict, it enters
*Agent Memory Allocation* v2 at claim-site prominence beside C29's supported
verdict, and it says something the field does not currently know: that the
parent result is corpus-conditional. This registration commits to publishing
that outcome as the result. Interpretation never changes a verdict.

## Gate

**Hard order gate**, proven by commit timestamps (the C25 / run-horizon /
C29 pattern), in this sequence:

1. **registration** — this file, the instrument note, the BUILD plan. No code,
   no corpus, no questions, no provider contact.
2. **verification** — an independent read-only pass over the committed
   registration (Phase-H rule 2, the green-review rule).
3. **instrument** — harness, adjudicator, tests, and their dead runs, committed
   together (Phase-H rule 1). No questions, no corpus snapshot.
4. **corpus snapshot** — full file bytes + manifest + rule-R evaluation log,
   committed. Before any question exists.
5. **question freeze** — questions, gold answers, index, salted-selection
   record and sha256 digests, committed. Before any policy run.
6. **excluded smoke** — 10 questions, 3 policies, audited; two independent
   audit replays must produce identical artifacts.
7. **confirmatory** — 120 questions, 3 policies.
8. **adjudication** — the frozen adjudicator run twice, byte-identical, its
   effect table and a new dated results document committed once.

**Coverage floors:** ≥100 scored questions for each of B, C and D; rule R
yielding ≥135 files at `S`; hydration records on 100% of scored B and C runs;
one resolved model identity per pinned model across the entire study; the corpus
sandbox hash-verifying byte-exact against the committed snapshot on every run.

A post-freeze change to the harness, the policies, the scoring rule or the
adjudicator creates a new regime and requires a new dated correction and a new
disjoint smoke set. Since C34's corpus is public and its questions are generated
from it, the C33 pilot-cohort disjointness ruling does not apply here: no
identity is held out for exposure reasons.

## Exposure rules (lighter than C33, and explicitly so)

The corpus is public. Its documents may be read by any model at any time, and
their exposure is not accounted, tracked or budgeted. There is no held-out
identity, no cohort disjointness requirement, and no exposure ledger for corpus
files. This is stated rather than left implicit because the sibling C33 study
carries the opposite regime and a reader moving between them should not have to
infer which applies.

What is protected is narrower and is protected absolutely:

1. The frozen question set and its gold answers are authored by the generator
   from corpus bodies and are thereafter shown to **no model** except the
   answerer during registered runs. They are not shown to the orchestrating
   session's model as material to reason from, not used to author digests, and
   not used to author the index.
2. The generator sees frontmatter-stripped bodies only. It never sees the
   digest index it helps produce alongside a question it authored for the same
   file, and digest authoring and question generation are separate committed
   passes.
3. The 10 smoke questions **are** exposed to the answerer before the
   confirmatory pass. They are disjoint from the 120 by frozen salt and
   permanently barred from every denominator, table and verdict.
4. The orchestrating session authors no question, no digest and no answer, and
   may fix harness *code* before runs but may never edit questions, digests or
   answers after the freeze commit.

## Release binding

**Purpose, registered:** on adjudication this study's result enters *Agent
Memory Allocation* v2 **at claim-site prominence, whatever it is** — beside
C29's verdict in §6.5, in the abstract's C29 sentence, and in §7 Limits (b′)
where the superseded demonstrator's status is recorded. The v2 import is
mechanical from the committed effect table; no number is retyped.

**The entire study ships in the public bundle**: the corpus snapshot (full file
bytes), `corpus-manifest.json` and the rule-R evaluation log, the frozen
question set with gold answers, the digest index, `corpus_rule.py`, the harness,
the adjudicator and its tests and dead runs, every smoke and confirmatory run
record, the smoke audit artifacts, the effect table, and the dated results
document.

**Shipping it violates no confidentiality**, by construction and not by review:
rule R clause 5 admits only files that pass the client-content audit with zero
flags; clause 3 excludes `paper/` and `analyses/`, where the withheld material
and the withheld-corpus harness live; the sandbox is assembled solely from the
snapshot, so no unaudited file can enter a prompt; and no Mentu database, CIR
record, transcript, memory file or client workspace path is on any path this
study touches. The study reads repository files and calls a model. It reads no
measured Mentu substrate, so the observer-effect rule is satisfied trivially,
and `--no-session-persistence` means it writes no transcript into any future
corpus.

## Known limitations (frozen)

- **The single-operator bound is not removed.** Same author, same repository,
  same machine, same harness family, same answerer as C29. What C34 buys is
  power, public re-runnability and a corpus a reader can hold in full. Operator
  diversity is a different study — a corpus authored by someone else, ideally
  with different naming conventions — and it is named here as the next
  successor, not smuggled in as an implication of this one.
- **Naming consistency plausibly favors grep**, exactly as in C29: this
  repository's filenames are unusually descriptive of their contents, which is
  the condition under which associative search is strongest. This is an
  external-validity bound to state, not a reason to soften a prediction.
- **Self-reference.** The corpus is the program's own methodology corpus,
  including sibling conjecture registrations and dated results documents. Rule R
  clause 6 removes documents about C29 and C34 specifically, but the corpus
  still describes the program that runs the experiment. This affects all arms
  identically, and D bounds the comprehension component.
- **One answerer at one capability tier.** A stronger answerer might extract
  more from digests; C31 owns that question and this study does not touch it.
- **C has no search tool.** As in C29, the comparison is an authored index
  against grep as **sole locators**; it says nothing about an index used
  *alongside* search. The disposition names index-plus-search as the successor
  the C29 data motivate; adding it here would confound the replication, so it is
  explicitly deferred and not registered.
- **The tested C is a two-tier realization** — path plus one-line digest, then
  the full body — not the four-layer ladder the parent claim's prose describes.
  Carried from C29 D1 and stated before the questions exist.
- **D is an approximation** at file granularity and is not a ceiling; P4's ≥3×
  reads against that approximation, not against true optimality.
- **Generated questions skew toward locatable facts.** The `lookup`/`synthesis`
  split is reported and, as in C29, the synthesis arm will be the smaller one
  and carries correspondingly less weight.
