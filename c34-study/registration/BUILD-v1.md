# BUILD — C34 public curation-vs-search replication

**Date:** 2026-08-12
**Status:** registered; no harness code, no corpus snapshot, no question set,
no provider contact
**Conjecture:** `corpus/conjectures/c34-public-curation-vs-search-replication.md`
**Instrument note:** `instruments/2026-08-12-c34-public-corpus-replication-instrument.md`
**Study directory (to be created at M2):**
`analyses/c34-public-curation-vs-search-replication/`
**Parent:** C29, `corpus/supported/c29-curation-vs-search-sufficiency.md`
(untouched by this plan)

## 0. Objective

Produce public evidence for the paper's central experiment that a reader can
re-run in full: 120 frozen questions over a snapshotted public corpus, three
pinned policies, one deterministic adjudicator, one dated verdict — whatever
that verdict is. The study supersedes the 16-question `repro-kit/` demonstrator
as the paper's public evidence without editing a byte of it.

Registration is complete. Everything below is execution, and each milestone
ends in a verification step that a different pass performs read-only.

## 1. Standing rules this plan is bound by

From `docs/PLAN-hardening-and-retest-2026-08-12.md`:

1. **Dead-run rule** — every new gate lands with its constructed total failure
   in the same commit (M2 and M4 below).
2. **Green-review rule** — no fully-green result is believed until a non-author
   pass has tried to refute it (M1, M3, M5, M7).
3. **Enumerate-then-freeze rule** — no freeze pins the behavior of a surface we
   do not control without enumeration or a budgeted reality probe. The corpus is
   ours and was enumerated at registration (142 files); the provider is not
   ours, so model availability and schema acceptance are bought with two
   budgeted calls at M5 rather than assumed.
4. **Denominator rule** — every zero ships with its denominator and its
   `not_exercised` / `zero_events` status.
5. **Cost-of-knowledge ledger** — each milestone records what it cost, in
   provider calls against the registered sub-ceilings.
6. **Hash-freezing is not archiving** — M3 snapshots the corpus into committed
   storage. A manifest is not a freeze.

And from the constitution: verdicts come only from the frozen adjudicator;
negative and ambiguous findings are reported as-is; nothing in `results/`,
`corpus/supported/` or `corpus/refuted/` is edited.

## 2. Milestones

### M0 — register (done, this commit)

Three files: the conjecture registration with all frozen sections, the dated
instrument note, this plan. No code, no corpus, no questions, no provider
contact.

**Verify (M1).**

### M1 — verify the registration (read-only, non-author)

A pass that did not author M0 checks, mechanically where possible:

- every frozen section is present and internally consistent: claim, corpus rule
  R, question contract, policy definitions, the five predictions, the six named
  deviations, the total verdict precedence, the order gate, exposure rules,
  release binding, limitations;
- **P1 and P2 are byte-comparable to C29's frozen text**, and every deviation
  from C29 (D-1 … D-6) is named with a reason and none is silent — diff the
  registration's criteria against `corpus/supported/c29-…md` and
  `analyses/c29-…/adjudicate.py` and confirm the diff is exactly the six;
- the call-ceiling table sums to 927 against a stated ceiling of 950, and each
  sub-ceiling is reachable by the design it funds;
- rule R re-enumerates to ≥135 files read-only, and every file it admits passes
  the client-content audit with zero flags — **run the audit independently, do
  not trust the count in the registration**;
- rule R admits no file under `paper/` or `analyses/`, and no path containing
  `c29` or `c34`;
- C29's conjecture file, results document, effect table and run records are
  byte-identical to their state before M0;
- no provider call has been made.

Failure blocks M2 and is repaired by a dated correction, never by a silent edit.

### M2 — instrument and tests

Create the study directory. Implement, in one commit:

- `corpus_rule.py` — rule R, self-contained, with the audit token set and regex
  copied verbatim; emits the evaluation log with the accepting/rejecting clause
  per candidate;
- `harness_lib.py` — pinned model identities, `claude -p` invocation with
  `--no-session-persistence`, stream capture of `Read`/`Grep`/`Glob` events,
  token component separation, normalization and scoring, sandbox assembly with
  per-file hash verification, the global call counter and its durable ledger;
- `generate_questions.py` — frontmatter-stripped generation, mechanical answer
  validation, one regeneration pass, salted selection under
  `c34-confirmatory-v1:` and `c34-smoke-v1:`;
- `build_index.py` — mechanical frontmatter digest extraction, generator
  authoring for the remainder, authoring-cost ledger;
- `run_policies.py` — B, C, D; idempotent and resumable; one record per
  (question, policy); hydration record written for B and C alike;
- `adjudicate.py` — the frozen thresholds, the total verdict precedence, the
  effect table, and the non-adjudicating comparability block;
- `audit_smoke.py` — the smoke gate;
- tests and fixtures, **including every dead run** named in the instrument
  note's table.

**Verify (read-only, non-author).** Tests cover `supported`, `refuted`,
`revised` at each named reason, `instrument-insufficient` at each named cause,
and `void`. Each dead run fails its gate. The adjudicator is byte-deterministic
across two runs on the same fixtures. No question, no corpus snapshot and no
provider call exists yet. The commit contains no network call outside
`harness_lib`'s single pinned entry point.

### M3 — corpus snapshot

Run rule R at the snapshot commit `S`; copy the full bytes of every eligible
file into `corpus-snapshot/` preserving relative paths; write
`corpus-manifest.json` and the evaluation log; commit.

**Verify (read-only, non-author).** File count ≥135 and recorded; every snapshot
file's sha256 matches its manifest entry and its source at `S`; every snapshot
file passes the client-content audit with zero flags — **re-run the audit over
the snapshot itself, not over the source tree**; no snapshot file's path
contains `c29` or `c34`; the evaluation log accounts for every candidate
considered, accepted or rejected, with its clause. No question exists yet.

### M4 — question freeze

Generate one candidate question per snapshot file; validate mechanically;
regenerate once for drops; apply the shortfall rule; salt-select 120
confirmatory and 10 smoke; build the digest index; commit questions, gold
answers, index, selection record and sha256 digests.

**Verify (read-only, non-author).** Every gold answer occurs verbatim in its
source file's body in the snapshot; every question carries provenance;
generation used stripped bodies (check the recorded generation-input hashes
against independently stripped bodies); confirmatory and smoke sets are disjoint
and reproduce exactly from the frozen salts; the yield branch taken matches the
registered shortfall rule; `runs/` does not exist. Provider calls to date are
within the generation, regeneration and digest sub-ceilings and are recorded in
the ledger.

**This is the order-gate boundary.** Any policy-run record dated before this
commit voids the run set.

### M5 — reality probe and excluded smoke

Two budgeted calls establish that the pinned answerer and generator resolve and
that the request schema is accepted (Phase-H rule 3 — the C33 lesson: 70 calls
died at the API boundary because no one had shown the real API a request).
Then run the 10 smoke questions × 3 policies and audit.

**Verify (read-only, non-author).** Every smoke call has nonzero input tokens
and a resolved model identity equal to the pinned identity; every smoke B and C
record carries a complete hydration record; the sandbox hash-verified; the
adjudicator ran end-to-end on smoke records; **two independent audit replays
produce identical artifacts**; the hollow-run dead fixture still fails the
audit. Smoke records are marked barred from adjudication in the records
themselves. If the probe or the smoke run reveals an instrument defect, repair
it, commit a dated correction, and run a **new** smoke set — a post-freeze
instrument change is a new regime.

### M6 — confirmatory pass

120 questions × 3 policies, resumable, retries only for the registered error
classes and only against the reserve, no scored answer ever re-rolled. Commit
run records.

**Verify (read-only, non-author).** Scored counts per policy against the ≥100
floor; error records classified and each retry accounted against the reserve;
zero scored answers re-rolled (check by record identity, not by assertion); the
call ledger within every sub-ceiling; no smoke question id present in the
confirmatory records.

### M7 — adjudicate

Run the frozen adjudicator twice; confirm byte-identical output; commit the
effect table and a new dated `results/2026-…-c34-public-curation-vs-search-replication.md`
once. Move the conjecture per the constitution: `supported` →
`corpus/supported/`, `refuted` → `corpus/refuted/`, `revised` /
`instrument-insufficient` → stays in `corpus/conjectures/` with `verdict` and
`result` set.

**Verify (read-only, non-author).** The verdict in the results document is the
adjudicator's string, unedited; every number in the document traces to the
effect table; each frozen prediction is reported with its measured value and its
adjudicating measure named; the non-adjudicating comparability block is present
(C29's asymmetric P3, both token measures, the regime split, first-read
precision, the mis-routed/true-stop decomposition); every zero carries its
denominator and status. **A `revised` or reversal outcome passes through
unchanged** — no threshold is revisited, no measure re-chosen, no question set
extended.

### M8 — import to paper v2

Import the machine result into *Agent Memory Allocation* v2 at claim-site
prominence: §6.5 beside C29's verdict, the abstract's C29 sentence, §7 Limits
(b′) where the demonstrator's superseded status is recorded, and §Data &
artifact availability where the public bundle is described. Assemble the public
bundle.

**Verify (read-only, non-author).** Every imported number is generated from the
committed effect table, not retyped; C29's own reported numbers are unchanged;
the demonstrator record and its addendum are unchanged; the bundle contains the
corpus snapshot, questions, gold answers, index, `corpus_rule.py`, harness,
adjudicator, tests, dead runs, all run records, smoke audit artifacts, effect
table and results document; **and the bundle contains no file that fails the
client-content audit** — run it over the assembled bundle as the last gate
before release.

## 3. Boundaries

- No compound spans M0→M2 or M4→M6. The registration commit, the question
  freeze and the confirmatory launch are manual scientific boundaries that an
  automatic chain must not cross.
- The 950-call ceiling is never raised. A required run that does not fit is an
  honest `instrument-insufficient`, not a budget amendment.
- The ≥100 scored-question floor is never lowered, and seen estimates from this
  study can never justify lowering it later.
- Index-plus-search — the arm C29's data actually motivate — is **not** in this
  study. It is a separate pre-registration and adding it here would confound the
  replication.
- The single-operator bound survives this study. A corpus authored by someone
  else is the next successor and is not claimed as an implication of this one.
