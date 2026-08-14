# C34 — working conventions

Two standing rules this study adopted after they were paid for. Both come from
real defects caught during the build, and both generalize past C34, so they are
written here where the next person to touch this code will find them rather
than buried in a commit message.

## 1. A scripted in-place edit asserts its replacement count

**Rule.** Any script that rewrites a file in place must assert how many
replacements it made and fail loudly on zero. Never print a success message
that fires whether or not the work happened.

```python
assert s.count(old) == 1, f"patch matched {s.count(old)} times"
s = s.replace(old, new)
```

**Why it exists.** During M2 a patch script called `str.replace()` twice and
then printed `"patched"` unconditionally. One replacement matched; the other
silently no-opped, because a previous edit had already changed the text its
search string was looking for. The tests went green, the leak gate stayed
clean, and a stale comment shipped to a committed file (finding S-2).

`str.replace()` returning its input unchanged on no match is silent by design.
An unconditional success print converts a failed edit into a reported success.
Applied to a comment it produced a documentation error. Applied to a
threshold, an operator, or an expected-flag tuple it would have produced a
wrong artifact that still passed every test.

**The class.** This is the same structural blindness as two other defects this
study hit: the F1 ubiquity denominator, which was computed against the wrong
population and still matched every expected flag set; and the flag enumeration
check itself, which was blind to that denominator error. In each case a check
existed, ran, and reported success while the thing it was meant to catch went
past. **A success signal that fires whether or not the work happened is not a
check.**

The rule earned its place immediately: the first script written after it was
adopted asserted its count, matched zero, and stopped — catching the exact
stale comment the rule was written about.

## 2. Recompute any reported figure from the population it names

**Rule.** When a document states a figure, recompute it from the population
that figure's own sentence names, and state that population. A percentage and
a fraction in the same sentence must be arithmetically consistent with each
other, not merely with the surrounding prose.

**Why it exists.** This broadens the standing lesson of
`instruments/2026-08-13-c34-correction-v4-erratum-1.md` (finding G-V4-1),
which recorded a narrower version: recompute a percentage from the fraction
beside it. Two instances in one registration chain made it a class rather than
an accident —

- **v3 G1** corrected v2 C-4, which carried pre-exemption counts against a
  post-exemption denominator: right numerator, wrong population.
- **G-V4-1** corrected v4 H6, which paired C29's *frontmatter* share (48%)
  with its *authored* numerator (53 of 102). The correct authored share is
  52%. Same shape: a figure computed over one population, reported against
  another.

A third near-instance was caught before it shipped: the C29 digest median was
stated as 174, the upper of two middle values at even n, where the median is
173.5 (G-V4-3). Naming the convention alongside the statistic is the same
discipline applied to a different kind of population question.

**Where this bites hardest.** Results documents and paper imports, which
report many paired shares in close succession, and where a reader has no way
to recompute without the underlying artifact. The M7 results document
therefore names the population for every figure it quotes, and every one of
them was verified against the committed effect table before the seal.

## Related, already registered elsewhere

- **Phase-H rule 1** (dead runs): every gate ships a constructed total failure
  it must catch, in the same commit. Rule 1 above is what happens when that
  discipline is applied to a *tool* rather than to a gate.
- **Correction v2 C-9** (order-annotated ledgers): record all matching clauses,
  not just the first, so a bucketing choice cannot hide a second reason.
- **Correction v4 H4**: the flag enumerations are computed and compared, and a
  mismatch raises rather than reports — a commitment that can drift silently
  is a comment.
