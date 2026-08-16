# Addendum to the public demonstrator record, 2026-08-12

**Corrects**: `DEMONSTRATOR-RESULT.md` (2026-07-21), which stands unchanged as
the original record per the repository's correction convention.
**Occasioned by**: `../EXTERNAL-REVIEW-2026-08-12.md` §B1, dispositioned in
`../DISPOSITION-2026-08-12.md`.
**Data**: unchanged. `effect-table-public.json` and `runs/` are the same
artifacts; nothing was re-run. What follows is recomputation from them.

## 1. The demonstrator does not adjudicate anything

Run against C29's frozen criteria in the order the committed adjudicator applies
them (`analyses/c29-curation-vs-search-sufficiency/adjudicate.py`), the floor is
checked first:

| frozen criterion | computation | outcome |
|---|---|---|
| floor: ≥100 scored per B/C/D | min = **16** | **FAIL** |
| P1 acc(B) ≥ acc(C) − 3pp | 0.6250 ≥ 0.5950 | pass |
| P2 tok(B) ≤ 2× tok(C) | 2,914,973 ≤ 6,168,036 | pass |
| P3 C wrong-stop ≥ B wrong-answer | **0.1875 ≥ 0.3750** | **FAIL, ratio 0.50** |
| P4 B ≥ 3×D and C ≥ 3×D | 8.08×, 8.55× | pass |

**Verdict under the frozen machinery: INSTRUMENT INSUFFICIENT
(scored-question floor).** The demonstrator adjudicates nothing, for or against.

## 2. The original record's "reproduces" claim is withdrawn

`DEMONSTRATOR-RESULT.md` states that the run reproduces "C incurs a wrong-stop
tax that B does not" and calls this "the paper's §4 lossy-semantics mechanism,
visible again." **That is withdrawn.** Applying C's own frozen wrong-stop rule
(incorrect **and** never read the gold file) symmetrically to both policies over
the 16 public questions:

| | non-hydrated | wrong-stop | localization (gold file read) | accuracy |
|---|---|---|---|---|
| B grep-then-read | 4/16 | **3/16 = 18.75%** | 12/16 | 10/16 = 62.5% |
| C index-then-hydrate | 4/16 | **3/16 = 18.75%** | 12/16 | 10/16 = 62.5% |

The two policies are identical on every one of these measures. **There is no
wrong-stop tax in this run.** Under frozen P3 as written (C's wrong-stop against
B's wrong-*answer* rate) the comparison does not merely fail to reproduce the
paper's magnitude, it reverses direction: 18.75% against 37.5%.

## 3. "B has no wrong-stop failure mode" is false

The original record explains B's zero by policy definition ("B, which always
reads"). Two facts contradict it. Under C's frozen rule B's wrong-stop rate is
18.75% here and 12.75% on the paper's 102-question corpus. And B is not
structurally always-reading: on the paper's corpus B answered with zero Read
events on 1 of 102 questions. The zero in the original table is an artifact of
the harness computing wrong-stop only for policy C
(`repro_kit.py`: `if p == "C"`), not a property of B.

## 4. The tie is a power result, not a corpus-dependence result

At 16 questions per arm, two-sided Fisher power to detect the paper's own effect
(72.55% against 47.06%) is **19.0%**, and the smallest resolvable count
difference is 5 questions (31.2 pp). B's 10/16 carries a Jeffreys 95% interval
of **38.3%–82.6%**, which contains the paper's 72.5%. This run provides **no
evidence against** the accuracy margin; it is uninformative about it.

The original record attributed the tie to corpus conditions, naming "English vs.
Spanish" among them. That explanation does not survive the paper's own data: on
the 102-question corpus the B-minus-C margin is **+29.4 pp on the 17 English
documents** (B 12/17, C 7/17) and **+24.7 pp on the 85 Spanish ones** (B 62/85,
C 41/85). The margin is *larger* in English. Since this demonstrator runs on
those same 17 English documents with the same pinned answerer, the difference
between +29.4 pp and 0 pp is question sampling and run-to-run variation at
n≈16, not language.

## 5. This is not an independent replication

The 17 documents here are the **English half of the paper's own C29 corpus**,
the same objects that also serve as C26 T2 members and as the paper's §6.4
zero-frontmatter census row. Same operator, same machine, same harness, same
documents, same answerer family, smaller question set. It is a subsample re-run.
The word "replication" has been removed from the paper's abstract accordingly.

## 6. What the run does show

One qualitative pattern appears in both runs and is worth stating at its true
strength: **C's non-hydrated answers are overwhelmingly wrong** (3 of 4 here,
47 of 49 in the paper). Note also that in both runs the non-hydrated questions
are mostly not cases of the policy stopping at the index. Here **all 4** read at
least one file, the wrong one; in the paper 44 of 49 did. The mechanism is
mis-routing by the authored index, not premature stopping. See the paper's §6.5
as revised in `paper-v1.2.md`.

## 7. What a replicator should report

Report the scored-question count against the frozen floor of 100 per policy, and
record per question whether the policy read the gold file. That single field is
what separates mis-routing from early stopping, and it is what this record and
the paper's v1.1 both misread in their own data.
