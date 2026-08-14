# CHANGES — paper v1 → v1.1 (2026-08-12)

Source of the work order: the publication-readiness audit banked at
`orchestration-prompts/audit-memalloc-findings-2026-08-12.md` (verdict: no
blocks-posting; seven fix-before-posting findings F1–F7; six notes). This
revision applies only those items.

`paper-v1.md` is untouched (sha256 `92b1c0401aa042fcfb536ca119619a62629b49b497fb678dd098703854552556`,
unchanged and git-clean after this work). `paper-v1.1.md` was created from its
exact bytes and edited. No file under `corpus/`, `results/`, `analyses/`, or
`repro-kit/` was read-modified; every fix below corrects the *paper's*
paraphrase of a source, never a source.

Each finding was re-verified against its cited source before the edit; the
verification is stated with the disposition. Two audit items were applied with a
correction to the audit's own wording (F4, F6), noted inline.

Rebuild of `paper-v1.html` / `.tex` / `.pdf` is **pending, deliberately
deferred** to after Stage 2 (external Operon re-review of v1.1), since further
edits are likely and building now would be waste. The three built artifacts on
disk therefore still render v1.

---

## Findings

### F1 — demonstrator caveat missing at 2 of 4 claim sites · FIXED

**Verified:** the caveat is carried in the abstract ("*supported* on this
corpus; a public replication reproduces the wrong-stop mechanism but not the
accuracy margin") and in §7 Limits (b), and is absent from both §6.5 claim
sites: the results/prediction tables and the Figure 2 caption.

**Edit 1 — after the §6.5 prediction table (new paragraph, before Figure 2):**

> These outcomes are the result **on this corpus**. The released kit's public
> demonstrator reproduces the wrong-stop mechanism but not the accuracy margin
> at its own scale (§7 Limits (b)).

**Edit 2 — Figure 2 caption.**
Before: `… C's position is paid for with wrong-stops — 47 of its 49 index-only
answers were wrong.*`
After: `… C's position is paid for with wrong-stops — 47 of its 49 index-only
answers were wrong. Measured on this corpus; the public demonstrator reproduces
the wrong-stop mechanism but not the accuracy margin (§7 Limits (b)).*`

The audit's suggested pointer "see §7b" was rendered as "§7 Limits (b)": the
paper has no §7b, and (b) is the limits item that carries the demonstrator.

### F2 — wrong denominator in the honesty passage · FIXED

**Verified at source before editing.** `repro-kit/effect-table-public.json`
records for policy C: `non_hydrated: 4`, `wrong_stop_rate: 0.1875`, `scored:
16`. `repro-kit/DEMONSTRATOR-RESULT.md:20-22` reads "C answered 4/16 from the
index tier without hydrating, and 3 of those were wrong". The paper's "3 of 16
index-trusted answers wrong" implies sixteen index-trusted answers; there were
four. The audit's reading is correct.

**Edit — §7 Limits (b).**
Before: `… reproduces the flat-load and oracle bounds and C's wrong-stop tax
(3 of 16 index-trusted answers wrong; B has no such failure mode) but **not**
the +25.5 pp accuracy margin …`
After: `… reproduces the flat-load and oracle bounds and C's wrong-stop tax
(C answered 4 of the 16 questions from the index without hydrating and 3 of
those 4 were wrong, an 18.75% wrong-stop rate over the question set; B has no
such failure mode) but **not** the +25.5 pp accuracy margin …`

Both denominators now appear at the claim site: 3 of 4 index-trusted answers
wrong, which is 18.75% of the 16-question set.

### F3 — synthesis claim carried no n at the claim site · FIXED

**Verified:** the 81/21 split appears in §6.5's setup and §7 Limits (b) but not
at the regime-map sentence. The effect table's `qtype_split` is
`{lookup: 81, synthesis: 21}`, and the reported rates reconcile with those
denominators (0.714 × 21 = 15; 0.381 × 21 = 8).

**Edit — §6.5 regime map.**
Before: `B beats C on lookup (72.8% vs 49.4%) *and* on synthesis (71.4% vs
38.1%) — the hypothesized regime where hierarchy helps synthesis questions does
not appear in this data.`
After: `B beats C on lookup (72.8% vs 49.4%, n=81) *and* on synthesis (71.4% vs
38.1%, n=21) — the hypothesized regime where hierarchy helps synthesis questions
does not appear in this data. The synthesis arm is underpowered at 21 questions
and carries correspondingly less weight than the lookup arm.`

### F4 — headless zeros reported bare · FIXED (with one corrected number)

**Verified against `analyses/c26-residency-determined-return/effect-table-2026-07-18.json`:**
headless stratum `T1_memory` 8/453 = 0.0177, `T1_skills` 0/161, `T2` 0/102;
`strata_sessions.headless` = **2,176**. The audit's recommended clause said
"2,016 headless sessions"; that figure appears in no source. 2,176 is the
analyzer's count and is corroborated by the results doc's caveat 2 ("2,176/160
vs 2,166/156"). The finding's substance (denominators plus exercised-status)
is applied; the audit's numeral is rejected as a transcription error.

Exercised-status: both zeros are `zero_events`, not `not_exercised` — the tiers
were in scope and measured across the headless stratum, and no read events
occurred.

**Edit — §6.3.**
Before: `Headless stratum, reported and never pooled: T1 memory 1.77%, skills
0%, T2 0%.`
After:

> Headless stratum, reported and never pooled: T1 memory 1.77% (8 of 453),
> skills 0% (0 of 161), T2 0% (0 of 102), across 2,176 headless sessions; these
> are measured zeros (`zero_events`), not unexercised tiers.

### F5 — C28 orphan zero lost its denominator and its mechanical outcome · FIXED

**Verified against `analyses/c28-promotion-lane-returnability/effect-table-2026-07-18.json`:**
`indexed_in_population: 89`, `orphans_in_population: 68`, `population: 157`,
`indexed_ever_frac: 0.0225`, `orphan_ever_frac: 0.0`,
`predictions.P3_indexed_ge_3x_orphan: true`. The results doc records P3 as
"technically pass; numerators too small to carry weight". The paper reported the
percentages, the two-reader caveat, and "no weight either way", but dropped both
denominators and the mechanical pass.

**Edit — §6.2.**
Before: `The indexed-vs-orphan contrast (P3) read 2.25% vs 0.0% on two total
readers — no weight either way.`
After: `The indexed-vs-orphan contrast (P3) read 2.25% (2 of 89 indexed) vs
0.0% (0 of 68 orphans), which technically passes P3 on two readers in total and
carries no weight either way.`

### F6 — empty-validation-slot null was unbounded · FIXED (bounded to what the record supports)

**Verified:** the abstract's "empty validation slot" claim rests on the §3 table
cells reading "none documented" for MemGPT/Letta and Pichay, and neither the
paper nor `references.bib` states a search procedure, a version, or a date for
that reading. `references.bib`'s MemGPT entry (`packer2023memgpt`) carries no
version field and there is no Letta documentation entry at all. The finding
holds.

The audit's recommended wording named "arXiv:2310.08560 **v3**". That version
is not recorded anywhere in the repository and could not be verified here
without external contact, so it is **not** asserted. What the record does
support is the reading date: the references note states refs 1–8 were verified
against their primary sources on 2026-07-22. The fix uses that date and names
the scope instead of a version.

**Edit — §3, observation 1.**
Before: `**The validation column is empty for both published systems.** The
frame predicts a policy slot that MemGPT and Pichay simply do not fill. We read
this as a finding about the systems …`
After: `**The validation column is empty for both published systems.** The
frame predicts a policy slot that MemGPT and Pichay simply do not fill. The null
is bounded by the reading behind this table and no wider: no validation policy
appears in the MemGPT paper (arXiv:2310.08560), the Letta documentation, or
Pichay (arXiv:2603.09023) as read on 2026-07-22; a later revision or an
undocumented mechanism would move the cell. We read this as a finding about the
systems …`

### F7 — artifact repository never stated as unpublished · FIXED

**Verified against `SENSITIVITY-AUDIT.md:42-46`:** "Nothing has left the
machine … all client content is local-only … The client content sits in
committed git *history*, however — a clean public release cannot be a `git
push` of this repo; it must be a curated artifact." The paper's Data &
artifact availability section refers throughout to "the `epistemics` research
artifact" and to private artifacts "available under appropriate confidentiality
terms", but nowhere states that the repository itself is not published.

**Edit — Data & artifact availability, end of Confidentiality boundary.**
Added after "No part of the client corpus is released with this paper.":

> The `epistemics` repository itself is **not published**: client content sits
> in its committed git history, so no release here can take the form of
> publishing the repository. Artifacts are released individually: the paper, its
> figures, and `repro-kit/` publicly, and anything else only under appropriate
> confidentiality terms.

---

## Notes

### N1 — totals-vs-marginal token inversion visible only in the P2 row · FIXED

**Verified against the C29 effect table:** `tokens_total` A 4,925,937 /
B 19,476,827 / C 13,841,268 / D 2,132,139; B/C = 1.407, which is the 1.41×
figure the P2 row cites. The §6.5 policy table reported marginal tokens only,
so a reader met "1.41× totals; B cheaper on marginal" with no totals anywhere.

**Edit — §6.5 policy table:** added a **Total tokens** column (A 4.93M,
B 19.48M, C 13.84M, D 2.13M). C's amortized total (15.15M) is not added, since
P2's frozen threshold is stated against C's *unamortized* tokens and the
authoring charge already appears in the Cost column.

### N2 — C28 P4 quote truncated without an ellipsis · FIXED

**Verified against `corpus/refuted/c28-promotion-lane-returnability.md:70-73`:**
the frozen P4 ends "…promotion buys reachability, not omnipresence. (This bound
protects the tier model: if memory files behaved like T0, the T1 tier definition
would be wrong.)" The paper dropped the parenthetical silently, under §5's
"wording exact" claim.

**Edit — §5.3:** appended the paper's own elision marker (used already in §5.1
and §5.4) rather than lengthening the quoted block: `… promotion buys
reachability, not omnipresence. […]"`. The frozen source is untouched.

### N3 — all-green C29 plus an author-commissioned review · FIXED

**Verified:** `EXTERNAL-REVIEW-2026-07-22.md` records a review the author ran
through a separate harness (OPERON) and then re-verified; it is
author-commissioned. The standing green-review rule
(`docs/PLAN-hardening-and-retest-2026-08-12.md`, Phase H rule 2) holds that no
fully-green result is believed until a non-author adversarial pass fails to
refute it, and C29 is the program's only all-green result.

**Edit — §7, end of the meta-method paragraph:**

> One part of that discipline is not yet met here: the adversarial review this
> manuscript was hardened against was commissioned by the author
> (`EXTERNAL-REVIEW-2026-07-22.md`), so C29, the program's one all-green result,
> has not survived a refutation attempt by a reviewer with an independent stake.

### N4 — §3.1 hook-API null needed an access date · FIXED

**Verified:** §3.1 cites "[Claude Code hooks reference, accessed 2026-07-22]" at
the top of the paragraph, but the null ("no hook writes the durable store
directly") read as timeless.

**Edit — §3.1.** Before: `**Promotion is the exception**: no hook writes the
durable store directly;` After: `**Promotion is the exception**: no hook
documented at that access date writes the durable store directly;`

### N5 — C26 P3 arms sum to 101 against a T2 of 102 · FIXED

**Verified in `analyses/c26-residency-determined-return/analyze.py:267-271`:**
the frozen richness rule is "Rich >= 3, sparse <= 1" anchors, and a score of 2
lands in neither list (`(rich if s >= 3 else sparse if s <= 1 else []).append(p)`).
The effect table's `rich_n: 55` and `sparse_n: 46` therefore leave exactly one
mid-band T2 file out of both arms.

**Edit — §6.3,** after the 1.08 ratio sentence: `The frozen richness rule scores
rich at ≥3 anchors and sparse at ≤1, so one mid-band T2 file falls in neither
arm (55 + 46 = 101 of 102).`

### N6 — tension between refs 12 and 13 unnoted · FIXED (minimally)

**Verified only against the paper's own reference descriptions** (ref 12 "finds
retrieval dominant"; ref 13 probes "what final accuracy misses" in memory
utilization). The primary sources were not re-read here, so the added clause
asserts nothing beyond the tension already visible between the paper's two
descriptions.

**Edit — §8, novelty claim (3).** Before: `retrieval-vs-utilization is
diagnosed in [12] and per-knowledge-point probing in [13] — but neither is
cross-tier (boot→store) nor pre-registered …` After: `retrieval-vs-utilization
is diagnosed in [12] and per-knowledge-point probing in [13], which pull in
different directions on whether retrieval or utilization is the binding stage —
but neither is cross-tier (boot→store) nor pre-registered …`

---

## Housekeeping edits (not audit items)

- **Version block.** The "Draft v1 — 2026-07-23. Preprint." line became "Draft
  v1.1 — 2026-08-12. Preprint; supersedes draft v1 (2026-07-23), whose text
  stands unchanged at `paper-v1.md`, with every difference itemized in
  `CHANGES-v1.1.md`." Required by the corpus rule that corrections are new
  dated documents.
- **Rewrapping.** Lines touched by the edits were rewrapped to the file's
  ~76-column convention; no line introduced by this revision exceeds 80
  columns. No em dash was introduced anywhere (the file's em-dash count moves
  155 → 154, the single removal being F5's rewritten clause).

## Nothing rejected

All seven findings and all six notes were verified and applied. Two audit
*wordings* were corrected in the process and are recorded above: F4's "2,016
headless sessions" (the analyzer says 2,176) and F6's "arXiv:2310.08560 v3"
(no version is recorded in the repository, so the fix states the reading scope
and date instead).

## Open for Stage 2

- External Operon re-review of `paper-v1.1.md`.
- `paper-v1.html` / `.tex` / `.pdf` rebuild, deferred until after that review.
- The audit's COULD-NOT-VERIFY list is unaddressed by this revision and stays
  open: the live `cir.db` schema claim (§1), references 1, 2, 4–9, and the
  existence of any non-author-commissioned adversarial pass (N3 now states the
  last of these in the paper itself).
