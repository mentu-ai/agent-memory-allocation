# C34 registration correction v5 (2026-08-14)

**Scope:** amends the self-containment clause of the corpus rule **for the
public bundle only**. Occasioned by the M8 release gate, which failed when the
bundle was assembled and the client-content audit was run over it — the first
time both had happened together. Decided by Rashid Azarang on the builder's
recommendation. Where this document and v4, v3, v2 or the 2026-08-12
registration conflict, this document governs.

**What does not change:** no threshold, floor, salt, model pin, prediction,
scoring rule, verdict-map clause, corpus membership, annotation set, or
adjudicated result. The verdict sealed at `c1627af` stands untouched. The
**in-repository canonical token list is unchanged**; only bundle copies differ.

## The conflict this resolves

Two registered requirements could not both hold, and the contradiction was
invisible until the bundle physically existed:

- **registration §1 clause 5** requires `corpus_rule.py` to carry the
  client-content audit token set **verbatim**, "so the rule is self-contained
  in the public bundle and needs no withheld file to re-run";
- **BUILD M8** requires that **no file in the assembled bundle fail the
  client-content audit**, run "over the assembled bundle as the last gate
  before release".

`corpus_rule.py` necessarily fails its own detector: it contains the tokens the
detector searches for. First assembly: 1,257 files, three failures, all of them
detector-definition sites in code. **Study data was entirely clean** — corpus
snapshot 0 of 141, run records 0 of 780, generation cache 0 of 295,
registration chain 0 of 7, results document 0.

## The decision

**The bundle's copies are redacted. The repository's are not.**

Three files differ between the repository and the bundle, and only these three:

| bundle path | what differs |
|---|---|
| `corpus_rule.py` | `CLIENT_TOKENS = []`, plus a redaction note and the sha256 of the canonical list |
| `tests/test_corpus_rule.py` | the one client-token literal in the smuggled-file dead run, replaced by a redaction marker |
| `tests/test_harness_lib.py` | the one client-derived literal in the forbidden-literals list, replaced by a redaction marker |

Nothing else in the bundle is altered from its committed form, and
`BUNDLE-MANIFEST.json` carries a sha256 for every shipped file so any
difference is detectable.

### The prove-same-rule property

The bundle's `corpus_rule.py` records:

    CLIENT_TOKENS_SHA256 = sha256(json.dumps(canonical_list,
                                             separators=(",", ":")).encode())

Anyone holding the canonical list — the operator, a referee under NDA, a
future maintainer — can recompute that digest in one line and prove the
bundle's rule is the same rule, without the bundle ever carrying the names.

## Why redaction costs the reader nothing they could have used

Registered here because it is the load-bearing reason, and it is checkable:

1. **Rule R is not re-runnable from the bundle regardless.** Its enumeration
   reads the git **tree** at `cb73654` through git plumbing (correction v2
   C-2.3). The bundle ships no git history, so the enumeration cannot run in
   it whether the tokens are present or absent. The self-containment clause
   was written to remove a dependency on one withheld file; it never removed
   the dependency on the repository itself.
2. **The audit's effect ships, in full.** `rule-R-evaluation-log.json` records
   every one of the 154 candidates with its accepting or rejecting clause, and
   — by a decision taken at M3 and now load-bearing — **hit counts rather than
   matched tokens**. A reader can see that five files were rejected on the
   audit, which five, and how many hits each carried, without the token set.
3. **What a reader can actually verify is untouched**: the 141-file corpus
   against its per-file hashes, the frozen question set with gold answers and
   generation provenance, the digest index, the harness, the adjudicator, all
   390 run records and attempt logs, the smoke audit, the effect table, and
   the byte-identical replay of the verdict.
4. **The alternative publishes three uninvolved people's names.** The token
   set is a curated enumeration of exactly the sensitive third-party
   identifiers; three of its ten entries are personnel names. They are not
   party to this study and gain nothing from its publication.

## Consequence for the bundle's test suite, stated rather than hidden

Redaction makes one dead run unexercisable in the bundle: the smuggled-file
test in `tests/test_corpus_rule.py` proves clause 5 rejects a file carrying a
client token, and with an empty token set there is no token to smuggle. In the
bundle that test **skips with an explicit reason** rather than passing
vacuously. A test that passes because it tested nothing is worse than a test
that says it could not run — that is the same failure class this study's
CONVENTIONS.md records as "a success signal that fires whether or not the work
happened is not a check."

The Spanish-density half of the same gate is unaffected and still runs: the
marker regex is a generic stopword list, identifies no third party, and is
**not redacted**.

Other suites in the bundle skip for reasons that predate this correction and
are properties of shipping a study outside its repository — the rule-R
enumeration needs the git tree, and the prompt-provenance suite compares
against C29's harness, which the bundle does not ship. The bundle README
states exactly which suites run, which skip, and why.

## What is registered by this correction

1. The self-containment clause of registration §1 clause 5 is **amended**: the
   rule ships self-contained in structure and in every element except the
   client-identifier list, which ships redacted with a verifying digest.
2. The BUILD M8 release gate stands **unweakened**. The audit is not modified,
   no file is exempted, and the gate must pass silently over the assembled
   bundle. It is the bundle that changed, not the gate.
3. The repository's canonical `corpus_rule.py`, its token list, and the two
   test files are **unchanged**, so every in-repository check continues to
   exercise the full rule.

## What this correction does not do

- It does not alter the adjudicated result, any prediction, or any figure in
  `results/2026-08-14-c34-public-curation-vs-search-replication.md`.
- It does not weaken, modify, or exempt anything from the client-content
  audit.
- It adds no deviation-ledger entry: D-1 … D-9 are unchanged, and nothing that
  adjudicates was touched.
- It authorizes no provider call. The study's provider work ended at M6;
  687 of 950 registered calls were spent and the retry reserve was never
  drawn on.
