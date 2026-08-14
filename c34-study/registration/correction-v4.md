# C34 registration correction v4 (2026-08-13)

**Scope:** adds **non-adjudicating reporting only**, in response to the M4
non-executor audit of the sealed order gate (`727f293`). Authored pre-outcome:
no policy run exists, no smoke call has been made, and no answer from any arm
has been observed. Where this document and v3, v2 or the 2026-08-12
registration conflict, this document governs.

**What this correction does NOT change:** no threshold, no floor, no salt, no
model pin, no verdict-map clause, no prediction, no scoring rule, no corpus
membership, and no criterion of adjudication. The frozen question set is **not
re-frozen** and not edited. The primary verdict is computed on all 120
confirmatory questions exactly as registered. Zero provider calls.

Following v3 G4's discipline of saying precisely what did and did not change:
this correction adds three **annotations** over the committed question set and
one **reporting requirement** on the adjudicator's output. It enters no
deviation-ledger entry, because it alters nothing that adjudicates.

## Why this exists

The M4 audit passed every registered criterion (~665 mechanical checks, zero
failures) and then found four properties of the frozen question set that the
registration's own machinery does not gate on. The most consequential:
**three confirmatory gold answers are so unspecific that the frozen scoring
rule cannot fail them.** Under normalized substring containment, question
q014's gold answer `0` scores correct for any answer containing the digit zero,
and that string occurs in all 141 corpus files.

The questions are frozen and stay frozen. What this correction buys is that
the study **reports the defect with its magnitude** rather than leaving it for
a reader to discover, and does so under a rule fixed before any outcome exists.

## H1 — the mechanical degeneracy flag

**Annotation `scoring_degenerate`.** Computed over the 120 confirmatory
questions from the committed artifacts alone — `questions-2026-08-13.json`,
`corpus-snapshot/`, `corpus-manifest.json` — using the harness's existing
`normalize()` (lowercase, whitespace-collapsed) and `strip_frontmatter()`. No
judgment, no human selection, no field that does not already exist.

A confirmatory question is flagged iff **any** of:

- **F1 — corpus ubiquity.** `normalize(gold)` occurs in the stripped body of
  **≥ 71 of the 141** snapshot files (a majority of the corpus).
  *Rationale:* a gold string present in most corpus documents carries no
  localizing information, so a policy can satisfy it without locating
  anything, and an arbitrary wrong answer drawn from corpus vocabulary is
  likely to contain it.
- **F2 — cross-answer collision.** `normalize(gold_i)` is a substring of
  `normalize(gold_j)` for some other confirmatory question `j ≠ i` (equality
  included). *Rationale:* the frozen scoring rule cannot distinguish question
  i's answer from question j's, so answering i with j's answer scores correct.
  One collision is sufficient proof; no threshold is required.
- **F3 — length floor.** `len(normalize(gold)) ≤ 2`. *Rationale:* at one or
  two characters the gold is a token fragment and containment is near-certain
  in any non-trivial answer. Stated independently of F1/F2 because it is the
  cleanest expression of the failure and it generalizes to a re-run on a
  different corpus, where ubiquity counts would differ.

### The flagged set, enumerated

**8 of 120 confirmatory questions (6.7%)**, with the conditions each trips:

| id | conditions | ubiquity | len | gold answer |
|---|---|---|---|---|
| q014 | F1+F2+F3 | 141/141 | 1 | `0` |
| q023 | F1+F2+F3 | 87/141 | 2 | `19` |
| q037 | F1+F2+F3 | 140/141 | 1 | `3` |
| q058 | F2 | 11/141 | 4 | `0.0%` |
| q076 | F2 | 3/141 | 36 | `the patterns exist and are queryable` |
| q077 | F2 | 3/141 | 36 | `the patterns exist and are queryable` |
| q129 | F2 | 4/141 | 4 | `0.80` |
| q138 | F2 | 13/141 | 3 | `0.9` |

q076 and q077 are distinct questions over distinct files
(`docs/referee/B2-stats.md` and `docs/referee/B2-validity.md`) that received
byte-identical gold answers; both remain individually answerable, but the
scoring rule cannot separate them.

### Disclosure: the rule was written after seeing the question set

It had to be — the question set is frozen and the audit is what surfaced the
problem. Three facts bound what that ordering can have bought:

1. **No outcome exists.** No policy has run. The flag cannot be
   outcome-informed, which is the class of move this corpus exists to prevent.
2. **The rule is mechanical.** It admits no per-question judgment, and any
   reader can recompute the flagged set from the committed bundle.
3. **F1's threshold is not knife-edged.** The confirmatory ubiquity
   distribution is sharply bimodal — median 1, with the next value below the
   flagged three at 19. F1 selects exactly {q014, q023, q037} for **every
   threshold from 20 through 87 inclusive**, a 68-wide plateau. The choice of
   "a majority, 71" therefore fixes no outcome that a neighbouring choice
   would have changed.

## H2 — `index_leak` is a separate annotation, not part of the flag

**Annotation `index_leak`:** `normalize(gold_i)` is a substring of
`normalize(digest)` for the question's own source file in
`index-2026-08-13.json`. **3 of 120: q014, q101 (`233,918`), q127 (`330`).**

It is kept **separate from `scoring_degenerate`** for three reasons, each of
which would make a merged flag uninterpretable:

- **Different mechanism.** F1–F3 concern the scoring rule's inability to
  separate right from wrong. `index_leak` concerns policy C's cheap tier
  containing the answer — treatment contamination, not scoring degeneracy.
- **Different symmetry.** The degeneracy flag is symmetric across B, C and D.
  `index_leak` is visible only to C, which alone receives the index.
- **Different direction.** `index_leak` raises `acc(C)`, lowers C's wrong-stop
  rate, and lowers the pooled non-hydrated incorrect fraction — each of which
  makes **P1, P3′ and P5 harder to pass**. It works against the study's own
  stake, which is the conservative direction. The degeneracy flag pushes P1
  and P3′ the easier way and P5(b) the harder way.

Only q014 carries both annotations.

## H3 — `outside_generation_slice` is a provenance note and excludes nothing

**Annotation `outside_generation_slice`:** `normalize(gold_i)` does not occur
in `normalize(stripped_body[:8000])` — the exact slice the generator was shown
under correction v2 C-4. **1 of 120: q131**, gold `0.80→0.73`, at normalized
offset 9,853 of 13,530 in `observatory/packets/2026-06-28.md`.

Cause, carried from C29 verbatim: `gen_one` validates containment against the
**full** body while prompting with `body[:8000]`, so a generator may emit a
string it was not shown that happens to occur later in the file.

**It is reported and excluded from nothing.** The question is answerable
exactly as the study intends — all agentic arms read whole files and D
receives up to 60,000 characters — so no measurement is affected. What is
unmet is the *provenance sentence*, and the correction is to state the caveat
rather than to drop a valid question.

## H4 — the non-adjudicating sensitivity table (reporting requirement)

`adjudicate.py` MUST emit, inside the existing `non_adjudicating` block and
labelled as non-adjudicating:

1. the three annotations above, per question id, with the conditions tripped;
2. `sensitivity_excluding_scoring_degenerate` — the **identical** computation
   over the 112 unflagged confirmatory questions: every per-policy statistic
   and every prediction outcome, so a reader can see whether any prediction
   turns on the flagged eight;
3. `sensitivity_excluding_index_leak` — the identical computation over the 117
   questions without the `index_leak` annotation;
4. for each row, its denominator and the delta against the primary result.

Binding constraints:

- **The verdict is the primary computation on all 120.** The sensitivity rows
  carry no verdict, move no threshold, and are never a tiebreak. If a
  sensitivity row disagrees with the primary result, **that disagreement is
  the finding and is reported as such** — it does not change the verdict.
  Interpretation never changes a verdict.
- Both sensitivity denominators (112, 117) sit above the registered ≥100
  scored-question floor, so both are computable; this is a fact about these
  numbers, not a new floor, and neither row is ever floor-gated.
- The flagged sets are **computed** by the adjudicator from the committed
  artifacts, not hardcoded. The enumerations in H1–H3 are the frozen expected
  values: **a mismatch between the computed and enumerated sets is itself a
  failure** and must raise rather than proceed. This is what makes the
  enumeration above a commitment instead of a comment.
- The verdict-legibility requirement of v2 C-12 is unchanged: P1, P3′ and P5
  remain at top level beside the verdict word.

## H5 — registered methodological observation (destined for the paper)

Recorded here as a finding of the replication itself, pre-outcome:

> **Carrying a generation prompt verbatim across corpora does not carry its
> question quality.** C34's `Q_PROMPT` is byte-identical to C29's, pinned by
> correction v2 C-1 precisely to make the two studies comparable. On C29's
> corpus it produced **5%** sub-three-word gold answers and **zero** golds of
> two characters or fewer. On C34's corpus, the same prompt produced **30%**
> sub-three-word golds (36 of 120 confirmatory) and **three** of two
> characters or fewer. The corpora differ in kind: C29's was largely
> narrative client material, while C34's is this program's own methodology
> documents — dense with bare numerals, thresholds and status tables, which
> the generator preferentially extracted.

The implication for replication practice is the point: pinning the treatment
string is necessary for comparability and **not sufficient** for it. A
replication that carries a generator prompt verbatim onto a new corpus should
measure the resulting question set's discriminating power before spending its
answering budget, because the prompt's behaviour is corpus-conditional. This
enters *Agent Memory Allocation* v2 with the C34 result.

## H6 — comparability facts recorded (audit O-4)

Non-adjudicating, recorded so the C29/C34 comparison is read correctly:

- **C34's index is 100% generator-authored (141/141); C29's was 48%
  (53/102).** 32 corpus files carry a frontmatter block, but none carries a
  `summary`, `description` or `title` key — this repository's conjecture files
  use `id`/`status`/`lineage`/`verdict`/`tracking` — so the committed
  `digest_from_frontmatter` correctly yields nothing for all 141.
- **Authoring cost 3,945,524 tokens against C29's 1,307,300.** It falls
  entirely in policy C's authoring ledger and is already reported both
  amortized and unamortized, as registered.
- **Digest length parity.** C34 median 163 characters, 91% exceeding the
  `S_PROMPT`'s 140-character request; C29 median 174, 87% exceeding it. C's
  cheap tier is therefore **not** systematically richer than the parent's —
  this is faithful replication, not drift, and the 200-character truncation is
  C29's, carried verbatim.

## H7 — what this correction does not do

- It does **not** re-freeze, regenerate or edit the question set. The
  re-freeze option is before the author separately. If a re-freeze is ordered,
  this correction supersedes cleanly: H1–H3's enumerations are specific to the
  committed set and would be recomputed for the new one under the same rules,
  and H5's observation stands regardless, being about the prompt rather than
  about any particular question.
- It does not change P1, P2, P3′, P4 or P5, their measures, their thresholds,
  the ≥100 floor, the verdict precedence, the salts, the model pins, rule R,
  or the corpus.
- It adds no deviation-ledger entry. D-1 … D-9 are unchanged.
- It authorizes no provider call. M5 remains subject to its own
  authorization.

---

Arithmetic for the verifier: confirmatory 120; `scoring_degenerate` 8
(F1 3, F2 8, F3 3; union 8); `index_leak` 3; `outside_generation_slice` 1;
overlap degenerate∩leak = {q014}, all other pairwise overlaps empty; union of
all three annotations 11 of 120 (9.2%); sensitivity denominators 112 and 117,
both above the ≥100 floor; primary denominator unchanged at 120.
