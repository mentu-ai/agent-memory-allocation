# C34 correction v4 — erratum 1 (2026-08-13)

**Scope:** three factual corrections to `2026-08-13-c34-registration-correction-v4.md`,
raised as findings G-V4-1 … G-V4-3 by the non-author verification of that
correction (which passed 5/5 on substance). Per house discipline the committed
v4 is **not edited**; this dated note governs where the two differ.

**Nothing here changes** a threshold, floor, salt, model pin, verdict-map
clause, prediction, scoring rule, corpus membership, flag rule, flagged set, or
any conclusion of v4. All three are errors in *reported comparison figures* and
in one *directional sentence*. The flag sets — `scoring_degenerate` 8,
`index_leak` 3, `outside_generation_slice` 1 — are unaffected and stand as
enumerated.

## G-V4-1 — H6's C29 authored share was the frontmatter share

**v4 H6 said:** "C34's index is 100% generator-authored (141/141); C29's was
48% (53/102)."

**Correct:** C29's index was **52% generator-authored (53/102)**.

C29's 102 files split 53 authored / 49 frontmatter. 53/102 = 51.96% → 52%;
49/102 = 48.04% → 48%. The sentence paired the **frontmatter** percentage with
the **authored** numerator.

**Error class, recorded because it recurs.** This is the same
numerator-against-the-wrong-denominator-regime error that v3 G1 corrected in v2
C-4, where pre-exemption counts were carried against a post-exemption
denominator. Two instances in one registration chain make it a class, not an
accident. The standing lesson for this study's remaining documents: **when a
percentage and a fraction appear in the same sentence, recompute the percentage
from that fraction rather than from the surrounding prose.** The M7 results
document and the v2 paper import are where this class would do real damage,
since both report many paired shares.

The substantive point of H6 is untouched: C34 authored every digest while C29
authored roughly half, and the ~3× authoring-token gap (3,945,524 vs 1,307,300)
follows from that.

## G-V4-2 — H2's direction sentence overclaimed on P5

**v4 H2 said:** `index_leak` "raises `acc(C)`, lowers C's wrong-stop rate, and
lowers the pooled non-hydrated incorrect fraction — each of which makes **P1,
P3′ and P5 harder to pass**."

**Correct:** it makes **P1 and P3′ harder, and P5 harder through its P5(b)
conjunct, while P5(a) moves the other way.**

Worked through, since the sign matters:

| conjunct | effect of a leak | direction |
|---|---|---|
| P1 — `acc(B) ≥ acc(C) − 3pp` | raises `acc(C)` | harder |
| P3′ — `wrong-stop(C) ≥ wrong-stop(B)` | lowers C's wrong-stop | harder |
| P5(a) — `localization(B) > localization(C)` | C answers **without hydrating**, lowering `localization(C)` | **easier** |
| P5(b) — ≥80% of pooled non-hydrated answers incorrect | a leak-enabled non-hydrated answer is **correct**, lowering the incorrect fraction | harder |

**The conclusion of H2 stands unchanged.** P5 = P5(a) ∧ P5(b), so a conjunct
that gets harder can fail the conjunction regardless of the other moving the
easier way. `index_leak` therefore still works against the study's own stake on
every prediction it touches, and the reason for keeping it a separate
annotation — different mechanism, different symmetry, different direction from
`scoring_degenerate` — is if anything strengthened: it now demonstrably moves
two of P5's own components in *opposite* directions, which is exactly what
merging it into the degeneracy flag would have hidden.

## G-V4-3 — C29 digest median stated without its even-n convention

**v4 H6 said:** "C29 median 174".

**Correct: 173.5 exactly**, or "≈174" if a single figure is wanted.

C29's index has n = 102 digests — an even count — whose two middle values are
173 and 174, giving a true median of 173.5. The figure 174 is the upper of the
two middle values, which is what `sorted(L)[n//2]` returns. C34's n = 141 is
odd, so its stated median of 163 is exact and unaffected.

Per correction v2 C-10's discipline of naming the convention alongside any
statistic, future statements of either median name their convention.

The comparison H6 draws is unaffected: C34's digests are slightly *shorter*
than C29's (163 vs 173.5) with a similar share exceeding the prompt's
140-character request (91% vs 87%), so policy C's cheap tier here is not
systematically richer than the parent's.

---

For the verifier: all three corrections were recomputed from committed
artifacts before this note was written —
`analyses/c29-curation-vs-search-sufficiency/index-2026-07-19.json` (53 authored,
49 frontmatter, n=102, middle values 173 and 174) and
`analyses/c34-public-curation-vs-search-replication/index-2026-08-13.json`
(141 authored, 0 frontmatter, n=141, median 163).
