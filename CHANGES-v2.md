# Agent Memory Allocation — changes in v2 (2026-08-14)

**v2 = v1.2 plus the C34 public replication.** `paper-v1.2.md` is byte-frozen
and unedited (sha256[:16] `47c84aa9657172d6`); v2 begins from its exact bytes.

No result in v1.2 is retracted, softened, or restated. C29's verdict,
thresholds, effect table and run records are untouched. The demonstrator record
and its addendum are unchanged and unretracted. Everything below is an
addition, at the sites the v1.2 audit mapped.

## What C34 is

A pre-registered public replication of C29's curation-vs-search experiment,
registered 2026-08-12 before any harness code, corpus snapshot, question or
provider call existed. 141 releasable documents selected by a frozen mechanical
rule and snapshotted at the byte; 120 confirmatory questions; the same pinned
answerer; three criteria **deliberately harder** than C29's.

**Verdict `revised`**, machine reason
`headroom_not_established_on_marginal_tokens`. Adjudicator replays
byte-identical; floors 120/120/120; zero contamination findings.

| | C29 (private corpus) | C34 (public, at power) |
|---|---|---|
| accuracy margin, search over index | **+25.5 pp** (72.5% / 47.1%) | **+12.5 pp** (63.3% / 50.8%) |
| wrong-stop tax | 46.1% vs 27.5% (**asymmetric** rule) | 34.2% vs 18.3% (**symmetric** rule) |
| localization | 80.4% vs 52.0% (reported, not predicted) | 75.0% vs 62.5% (**predicted**, passes) |
| oracle headroom | pass on totals; **B fails on marginal**, measure unfrozen | **fail on marginal**, measure frozen in advance |
| verdict | supported | **revised** |

## The six claim sites changed

1. **Abstract.** The C29 sentence now carries the public replication beside it:
   +12.5 pp, the symmetric wrong-stop tax, the localization advantage, and the
   `revised` verdict with its orthogonal cause named.
2. **§6.5.** A new subsection reports C34 in full — the frozen prediction table
   with measured values, the verdict, and three consequences.
3. **Figure 2 caption.** Notes that the replication reproduces B's accuracy and
   localization advantages on a releasable corpus and fails P4 on marginal
   tokens.
4. **§7 Limits (b).** C29's scope conditions are recorded as surviving into
   C34, which buys power and public re-runnability but **not** operator
   diversity. Adds C34's own scope condition (below).
5. **§7 Limits (b′).** The demonstrator's *role* is superseded by C34; its
   record stands unchanged.
6. **Data & artifact availability.** Describes the public bundle and states the
   one redaction plainly.

## Three things v2 says that v1.2 could not

**The finding replicates, smaller, under stricter rules.** +12.5 pp on a
different corpus in the same direction, with the corpus, questions, answers,
harness and adjudicator shipped for re-running.

**The symmetric wrong-stop rule vindicates its own correction.** C29's original
P3 compared C's wrong-*stop* rate against B's wrong-*answer* rate — a subset
against a superset. On C34's data that asymmetric form reads C 34.2% against B
36.7%, making the curated index look *better*. The symmetric rule shows it
wrong-stopping at nearly twice B's rate. The original did not merely understate
the tax; on this corpus it would have reversed the reading.

**The defect v1.2 disclosed is exactly what failed.** §6.5 recorded that P4's
measure was unfrozen and that its outcome flipped with the choice, and set the
rule: freeze the measure with the threshold. C34 did so, chose marginal tokens
— the harder reading, the one C29's own B failed — and P4 failed again, at
1.84× and 2.73× against a 3× bar. A prediction that fails under a measure fixed
in advance is a finding. The same prediction passing under a measure chosen
afterward would have been an artifact.

## A methodological finding, added to the limitations

C34's question-generation prompt was **byte-identical** to C29's, pinned
precisely to keep the studies comparable. On the new corpus the same prompt
produced a **30% sub-three-word gold-answer rate against roughly 5%** on C29's,
with three of 120 confirmatory golds so unspecific that the frozen scoring rule
could not fail them.

Pinning a treatment string is necessary for comparability and **not sufficient**
for it. A replication carrying a generator prompt onto a new corpus should
measure the resulting question set's discriminating power before spending its
answering budget. C34 flags the affected questions mechanically and reports two
sensitivity analyses — excluding scoring-degenerate golds (n=112) and excluding
index-leaked golds (n=117). **Neither flips any prediction.**

## The bundle, and its one redaction

The public bundle ships the corpus snapshot with per-file hashes, the rule
evaluation log covering all 154 candidates, the frozen questions with gold
answers and provenance, the index, all 390 run records and attempt logs, the
smoke audit, the effect table, the results document, the full registration
chain, and the harness, adjudicator and tests. `adjudicate.py` reproduces the
committed effect table byte for byte.

One redaction, registered rather than silent: the corpus-selection rule's
client-identifier token list is withheld, three of its entries being personal
names of people not party to this study. The rule ships with the list emptied
and the canonical list's sha256 alongside, so it is provably the same rule, and
the rule's effect ships in full. The enumeration is not re-runnable from the
bundle regardless — it reads the git tree at `cb73654`, and no git history
ships. See `instruments/2026-08-14-c34-registration-correction-v5.md`.

## What did not change

- `paper-v1.2.md`: byte-frozen, sha256[:16] `47c84aa9657172d6`.
- C29's verdict, criteria, effect table and run records.
- The demonstrator record and its 2026-08-12 addendum.
- Every C26, C27, C28 and M2.4 result and its wording.
- The program scoreboard's existing entries; C34 joins as a fifth adjudicated
  conjecture with a `revised` verdict.
