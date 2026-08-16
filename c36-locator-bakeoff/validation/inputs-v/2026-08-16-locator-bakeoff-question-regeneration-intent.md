---
id: locator-bakeoff-question-regeneration-intent
status: intent
date: 2026-08-16
author: Rashid Azarang
purpose: >
  Regeneration protocol for the PD-1 locator bake-off question set (BUILD
  P4a). Fixes the two disclosed instrument defects of the C29/C34 question
  sets and restores blindness. No conjecture id is claimed here; the id is
  assigned at registration (BUILD B8).
grounded_in:
  - analyses/c34-public-curation-vs-search-replication/generate_questions.py (frozen Q_PROMPT, line 55-67)
  - paper/agent-memory-allocation/paper-v3.5.md §5 (defect disclosures)
  - mentu-navigator docs/build/BUILD-progressive-disclosure-v1.md §2 P4a
tracking: {}
---

# Locator bake-off — question regeneration protocol (intent)

## Why regeneration, restated once

The existing 141/120-question public set and the 102-question C29 set are
**seen**: their results are published (search localizes 75.0% / 80.4%), so
any threshold frozen against them is chosen by someone who knows what it has
to clear. Order proof is not blindness (INTENT-progressive-disclosure §8).
Numbers from the seen sets are pilot-only and are labelled inside any
artifact that carries them. The bake-off adjudicates only on a fresh set
generated under this protocol.

## The two defects this protocol closes

1. **Instructed, not enforced.** The frozen generator told the model
   "3-15 words" (`generate_questions.py` `Q_PROMPT`) and enforced nothing;
   30.0% of golds (36/120) violated it. The same generator's digest
   instruction ("max 140 characters") was breached on 128/141 documents.
   The lesson is general: *a constraint that exists only as an instruction
   to a model is not a constraint* — it is measured here as an error rate.
2. **Unfailable golds.** Three golds ("0", "19", "3" — q014/q023/q037)
   could not be failed under the committed scoring rule; two substring
   false positives (q073, gold hash inside a longer hash) were symmetric
   but real.

## Protocol

**G1 — Corpus.** The same frozen snapshot family as the prior studies; the
exact snapshot and its manifest hashes are pinned in the registration
document, not here. No document may change between generation and the last
bake-off run.

**G2 — Generation.** The frozen `Q_PROMPT` wording is reused verbatim (one
factual question; answer an exact contiguous string; lookup|synthesis
label), same 8,000-char input bound. Model and operator prompt are pinned
at registration.

**G3 — Mechanical acceptance gates, applied per candidate at generation
time (reject-and-regenerate, max 3 attempts per document, failures
logged):**

| Gate | Rule | Closes |
|---|---|---|
| verbatim | gold is an exact contiguous substring of the document body | (inherited from C34) |
| length | gold is 3–15 words under the committed tokenization, **counted by the validator**, not the model | defect 1 |
| failable | gold, normalized under the committed scoring rule, must NOT be a substring of the question text, and must occur in ≤2 corpus documents (so locating wrongly can actually fail) | defect 2 |
| non-degenerate | gold is not purely numeric/punctuation and not a frontmatter field value | defect 2 |
| leak | the document's one-line digest (if any arm uses digests) must not contain the gold | (inherited; index-leak class) |

Every rejection is recorded with its gate in the generation log; the
acceptance rate per gate ships with the registered set. If a document
exhausts its attempts, it is excluded and counted — never silently skipped.

**G4 — Scoring rule.** The registration freezes the scoring rule *before*
generation validation runs, because gate `failable` is defined in terms of
it. Registration-time decision, recorded there: keep the C34 rule
(normalized substring containment) for comparability, or adopt a
word-boundary variant closing the q073 class. Default: adopt the
word-boundary variant as the adjudicating rule and compute the C34 rule
alongside descriptively, so both comparability and the fix are preserved.

**G5 — Freeze order (blindness discipline).**
1. corpus snapshot pinned →
2. scoring rule frozen →
3. generator + validator committed →
4. questions generated and hash-pinned →
5. **predictions and retire-thresholds frozen** →
6. arms run (L0–L4 per BUILD P4b, tool contract pinned per D4) →
7. mechanical adjudication.

No number from steps 1–4 may be quoted as a result; the set's only
pre-registration statistics are the acceptance-gate rates (G3), which
describe the instrument, not the arms.

**G6 — Who runs it.** Generation and validation are scripted and committed
under the registration's analysis directory (`analyses/<id>/`) per the
constitution; the validator is the same class of artifact as
`adjudicate.py` — frozen before data, byte-replayable after.

## What this document is not

Not a registration: no conjecture id, no predictions, no thresholds. Those
freeze in the dated registration document that cites this protocol. The
registration may tighten any gate here; it may not loosen one without
recording the loosening as a deviation in the registration itself.
