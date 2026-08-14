# Changes from draft v1.1 to draft v1.2 (2026-08-12)

**Base**: `paper-v1.1.md`, unchanged, sha256
`7d7a5c088a9a79c6f11e6cadbb8480ec7a9c46aec75e978d101478f69871f984`. v1.2 was
built from those exact bytes. `paper-v1.md` and `paper-v1.1.md` are untouched.

**Driver**: `EXTERNAL-REVIEW-2026-08-12.md`, dispositioned finding by finding in
`DISPOSITION-2026-08-12.md` (41 findings: 19 accepted, 11
accepted-with-modification, 8 rejected-with-arithmetic, 3 deferred).

**What did not change.** No frozen conjecture file, committed analyzer, results
document, or effect table was altered. No verdict was re-adjudicated. C29
remains SUPPORTED, C28 REFUTED, C26 and C27 INSTRUMENT INSUFFICIENT. Every
numerical change below re-reports a quantity the committed artifacts already
contained, or adds a descriptive statistic computed from committed run records
by read-only scripts held outside `analyses/`. The em-dash count fell from 163
to 150; none were introduced.

---

## The four changes that alter what the paper claims

### R1. §6.5 mechanism: mis-routing replaces early stopping

v1.1 read C's 49 non-hydrated answers as the policy trusting the digest and
stopping ("the digest tier almost never sufficed, and the policy trusted it
anyway"; Figure 2: "47 of its 49 **index-only** answers were wrong"). The
committed run records contradict this. **Of those 49 questions only 5 involved
reading no file at all; 44 read at least one file, the wrong one.** C issued
192 Read events to B's 174 and located the gold file on 53 of 102 (52.0%)
against B's 82 of 102 (80.4%).

Added at the claim site: the hydration decomposition (index-only 2/49 = 4.1%;
located 46/53 = 86.8%, Jeffreys CI 75.8–93.9), the selection control showing the
split is not question difficulty (D scores 81.1% and 83.7% across it, Fisher
p = 0.80), and the bound on the early-stopping successor arm (at most 5
questions, maximum attainable C accuracy 51.0%). "Index-only" and "trusted it
anyway" are removed. The headline result is unchanged: B beats C by 25.5 pp.

### R2. §6.5 and Figure 2: "D is the ceiling" removed; the A arm invalidated

On the 53 questions where C located the gold file, C scores 46 and D scores 43,
so a subset of C exceeds D. The excess is not significant (McNemar exact
p = 0.51) and the cause is mechanical: there C holds the gold file plus the
index plus other reads, while D holds the gold file alone truncated at 60,000
characters. The frozen conjecture already called D an approximation; only v1.1's
prose called it a ceiling.

Arm validation for A, newly computed and previously absent: **the 100,000-char
flat-load dump reaches 4 of the 102 corpus files**, and the gold answer string is
present for 4 of 102 questions. A's attainable ceiling was 3.9%; it scored 3 of
102, i.e. 3 of the 4 it could answer. "The naive full-dump (A) is useless" is
removed from Figure 2; A is now reported as a budget-bounded baseline supporting
no claim about flat loading.

### R3. §6.3, §7, abstract, Figure 1: the C26 inversion is re-scoped

v1.1 asserted that "the T1-vs-T2 comparison is internally consistent because
both sides use the same definition." **Withdrawn as a non-sequitur.** Identical
definitions do not equalize differential exposure to the channel a definition
admits, and here the exposure is grossly unequal: 73.5% of T2 objects were
edited during the measurement window against 9.5% of T1 memory files.

New diagnostic table in §6.3 (declared as a diagnostic, adjudicating nothing):
21 of 23 exercised T2 files are exercised only by sessions that also wrote them;
91 of 93 recoverable T2 read events are edit-linked; excluding the edit channel,
T2 falls to 2 of 102 and T1 to 0 of 453. The bound is stated explicitly, and it
is severe (see R4). The T2/T3 contrast survives untouched; the T1-versus-T2
inversion does not survive as a statement about allocation tier.

### R4. New Limit (g): the frozen transcript corpus no longer exists

Discovered while testing R3. **1,996 of the 2,337 transcripts in the frozen
manifest have been deleted; 341 survive and all 341 verify byte-exact against
their frozen prefix hashes.** All memory, workspace, and skill files survive.
C26, C27, and C28 are no longer re-derivable from their own manifests. C29 is
unaffected, its evidence being its own 408 committed run records. Recorded with
the generalizable lesson: hash-freezing proves integrity, not availability.

---

## Demonstrator and reproduction record

### R5. §7 Limits (b′), abstract, §Release shape, §Invitation

v1.1 said at four sites that the public demonstrator "reproduces the wrong-stop
mechanism but not the accuracy margin." **Withdrawn at all four.** Recomputed
against the frozen criteria: the demonstrator is below C29's 100-question floor,
so the committed adjudicator returns INSTRUMENT INSUFFICIENT and it adjudicates
nothing; within that, **frozen P3 fails and reverses** (C wrong-stop 18.75%
against B wrong-answer 37.5%, ratio 0.50); and under C's rule applied
symmetrically, **B and C are identical at 3/16 = 18.75%** with identical
localization. Power at n=16 is 19.0%; B's 10/16 interval is 38.3–82.6% and
contains 72.5%. "Replication" is removed from the abstract: the 17 documents are
the English half of the paper's own corpus.

New: `repro-kit/DEMONSTRATOR-ADDENDUM-2026-08-12.md`, a dated correction.
`DEMONSTRATOR-RESULT.md` stands unchanged per the correction convention.

### R6. §6.5: the corpus-language map, which withdraws v1.1's explanation

New table. B minus C is **+29.4 pp on the 17 English documents** and **+24.7 pp
on the 85 Spanish**. The margin is larger in English, so language does not
explain the demonstrator's tie; question sampling at n≈16 does.

---

## Claim-site repairs

### R7. Denominators and missing quantities

- **§6.5**: C's error rate added (52.9% against B's 27.5%, Fisher p = 0.0003),
  the comparison the abstract made and the paper never reported.
- **§6.2**: "451 of 453" withdrawn; the count is reported on the registered
  population of 157 at both sites, with 296 files named as not yet eligible.
  Cross-reference added to §6.3's 43/453 as the same objects under a different
  frozen definition.
- **§6.2**: C28's P3 keeps its mechanical pass (the not-evaluable branch fires
  below 20 orphans; the corpus has 68) and gains Fisher p = 0.51 and the
  statement that the ratio is undefined at a zero orphan numerator.
- **§6.1**: the top-5 invocation total is given (**10 of 16 matched
  invocations**; one reassignment gives 56.3%, below the frozen floor), together
  with the 44 total invocation events, the 28 catalog-matching failures, and the
  47.7% all-events share. "Directionally with the predictions" is withdrawn for
  P2.
- **§6.1**: the listing-token estimator is named
  (`(len(name) + len(description)) / 4.0` over the 161-entry union catalog,
  `analyze.py:228`), satisfying the constitution's rule 6 at the claim site.
- **§6.3**: the P3 richness confidence interval (0.60–1.92, Fisher p = 0.83) and
  the P4 antecedent window (anywhere earlier in session, not immediate).
- **§1**: session totals reconciled. C26 2,176 + 160 + 1 unclassified = 2,337;
  C27 2,166 + 156 + 15 empty = 2,337. The §1 census figure of 2,368 is marked as
  a differently-ruled earlier raw count, and the residual 31-transcript gap is
  disclosed as not decomposed by any committed artifact.
- **§6.4**: the per-corpus superlative is **deleted**. On recoverable data the
  entire T2 exercise signal comes from the 66%-frontmattered corpus (23 of 85,
  27.1%) and none from the 0%-frontmattered one (0 of 17).

### R8. §6.5: metric ambiguity in P4 disclosed

P2's frozen text names totals; **P4's names no measure**. On totals P4 passes at
9.1× and 6.5×; on marginal tokens **B is 2.85× and P4 fails for B**. Both
readings are printed. The verdict is not re-adjudicated; the ambiguity is
recorded as a method defect with the corrective rule (freeze the measure with
the threshold).

### R9. §6.5: token and cost columns

Cache-read share added per arm (A 29.7%, B 90.0%, C 82.2%, D 67.9%), which
accounts for the whole 4.8× effective-price spread the review flagged. **The
cost column is withdrawn from comparative use**: recorded `cost_usd` is
provider-reported and could not be reproduced from list prices.

---

## Positioning, lineage, and self-assessment

### R10. §2.2, §3, §8: the systems and pre-registration lineages

Added and independently verified on 2026-08-12 (arXiv API and Crossref; all
resolved): Smith 1982 and Denning 1968/1970 for the policy vocabulary, with an
explicit statement of what the frame adds beyond the cache axes; Liu et al. TACL
2024, Levy et al. 2024, BooookScore for §4's premises; Joren et al. 2024 as
**prior art for C\*(τ) and the wrong-stop framing**, narrowing §7's "first direct
measurement" claim; RAPTOR promoted from seed-flagged to nearest rival;
Agentless, SWE-agent, CAG, Xu et al. 2023; Mem0, MemoryBank, A-MEM, Generative
Agents, AIOS; Cockburn et al., Nosek et al., Chambers, Pineau et al., Ralph et
al., Ioannidis for the meta-method; both Aghajani et al. papers for §4 and §6.4.
References 14–38.

### R11. §3: observation 1 withdrawn; the load test demoted

MemoryBank's Ebbinghaus-inspired decay mechanism fills the validation cell in a
published system, so v1.1's inference that the empty column is "weak evidence
the slot is real: practice invented validation before theory named it"
**inverts and is withdrawn**. The abstract's wording is bounded to the two
systems named rather than retracted, because as written it names them.

"No residual column was needed" is demoted to a descriptive observation about an
author-run classification, with the reason stated: the author defined the rows,
filled the cells, and widened one definition during filling, so residual-free
coverage was not an outcome the test could have failed to produce. §7's
falsifying criterion is marked inert until a pre-committed version is run.

### R12. §7: the meta-method reframed as instantiation

"Treating systems claims the way clinical claims are treated" becomes a rigorous
*instantiation* against a named pre-registration literature. The green-review
status is updated honestly: C29 has now survived a refutation attempt and did
not survive it unchanged, but both reviews were commissioned by the author, so
the independent-stake condition remains unmet.

### R13. §7: practice implication re-scoped; new Limit (h)

"Retiring digest authoring for greppable corpora" is re-scoped: C had no search
tool, so the experiment compares an authored index against grep as **sole**
locators and does not test an index used alongside search. Limit (h) discloses
that the 17 epistemics documents serve simultaneously as C26 T2 objects, §6.4's
census row, C29's English arm, and the demonstrator's whole corpus.

---

## Not done, and why

1. **Reference 9 (the live hook documentation page)** is not replaced with an
   archival capture. The reviewer is right that a live URL with an access date
   is verifiable by nobody, and that §3.1's promotion null and §2.2's
   policy-push channel rest on it alone. Both are now marked unchecked in the
   References note. Replacing it needs an author-authorized fetch and a choice
   of archive.
2. **Mem0's update stage** is cited as adjacent rather than as a filled
   validation cell. Its abstract confirms consolidation but not add/update/delete
   reconciliation, and the body was not read. MemoryBank alone carries R11.
3. **The C26 deconfounded re-run** the review asks for is impossible: the
   transcripts are gone (R4). The diagnostic on the surviving 14.6% is reported
   with its bound, and the inversion is re-scoped rather than withdrawn, because
   withdrawing it would assert a deconfounded result the evidence cannot support
   either.
4. **The 31-transcript census gap** is disclosed, not reconciled.
5. **No successor conjecture is registered here.** The two this work generates
   (index-plus-search for C29; an immediate-antecedent mediation instrument for
   C26-P4) are pre-registrations under gauges-before-gates, not paper edits.
