# Escalation — Return-Base-Rate paper, B2 four-lens referee pass (2026-07-04)

> **STATUS 2026-07-04 (update): RESOLVED via read-only re-derivation.** The author
> authorized re-deriving from the instrument. A pinned `.backup` snapshot of
> `~/.mentu/cir.db` (sha256 `0b320d9d…`, `PRAGMA integrity_check = ok`) plus
> `instruments/2026-07-04-return-baseline-rederivation.py` reproduced the frozen
> experimental arms **exactly** (24/21/6) and resolved every blocker below. Key
> real findings: (1) the Stage-0 numerator is **invariant** — accessed = 91,
> context_used = 24 on the frozen as-of read AND on the post-intervention
> snapshot; only the denominator grows (409,404 → 433,155), rate stays ~10⁻⁴;
> (2) the "malformed" read was a live-file artifact — the snapshot is clean,
> distinct_accessed = 91; (3) the coherent per-run baseline is 0/244 organic
> (0.0%) / 6/289 experiment-inclusive (2.08%), so P1 was amended to the per-run
> unit (dated, pre-gate, verdict still null). Per-item disposition at the bottom.

**Trigger:** the B2 adversarial pass (4 report-only lenses: stats, field, measurement
validity, reproducibility) surfaced defects that live in **frozen artifacts** or in
**frozen numbers**, which per the constitution I do not edit. This file records them, the
exact reconciliation each needs, and who must act. No frozen file was modified.

Companion (safe prose fixes already applied to `paper/return-base-rate-paper.md`): see the
"Applied" list at the bottom. Reports: `docs/referee/B2-{stats,field,validity,repro}.md`.

**Verdict of the pass:** three of four lenses independently return *major revision / not yet
acceptable*. The negative result and its direction survive scrutiny; the qualitative claim
(instrumented return ≪ capture) holds. The gaps are in **frozen preregistration structure,
denominator/definition provenance, and data-availability** — not in the top-line rates,
which did not move under any check. **This paper is not arXiv-ready until the items below are
resolved by the author.**

---

## A. Blocker in a frozen artifact — requires a ratified C25 amendment (pre-gate, legitimate)

### A1. P1's baseline and post-outcome are on different units (stats-F1, validity-M2)
- **Where:** `corpus/conjectures/c25-return-intervention.md` — `baseline_frozen.organic_offer_accessed_pct: 0.0222` is a **per-trust-state-row access** rate (91/409,404). The **Design/Primary outcome** and **P1** define the post quantity as a **per-run offered-AND-used** rate (`use_rate>0` with positioned footer). The frozen "≥10×" comparison and "two-proportion test with the pre arm fixed at the frozen baseline" therefore compare incommensurable quantities (rows vs runs; accessed vs used).
- **Why it matters:** P1 is the primary preregistered endpoint. As frozen, its null is undefined and the "10×" ratio is not a coherent quantity. This also means the audit's access≠use point (#9) is unaddressed at the level of the primary hypothesis.
- **What must happen (author decision — legitimate now: verdict null, no post-data examined):** ratify a **dated C25 amendment** that puts baseline and post on the *same unit*. Two coherent options:
  1. Freeze a **per-run organic baseline** return rate (baseline runs where a prior signal was offered-and-used ÷ baseline runs) and compare the post per-run rate against *that*; keep 91/409,404 as the Stage-0 descriptive statistic only.
  2. Keep 0.0222% but restate P1 as a **one-sample** test of the post per-run rate against a fixed reference constant, and drop the "two-proportion" language (a two-proportion test on unequal units is invalid).
- **Constraint:** the frozen `c25` file is not edited by me. An amendment is an author/RAT action, recorded dated, *before* gate-open. The paper's §6 currently restates P1 faithfully to the frozen artifact; once the amendment lands, update §6 to match.

---

## B. Frozen-number / frozen-artifact discrepancies — flag, do not edit (numeric-mismatch rule)

### B1. Figure-data denominators disagree with the paper body; robustness artifact carries a malformed-read (repro-M1, repro-M8, stats-F2)
- `paper/stage0_robustness.json` reports `robustness_rows` = **424,321** (all) and **409,768** (trust-state); the paper body quotes **424,304** and **409,404** (`frozen_denom`). Body's **424,304 matches neither** the live 424,321 nor any frozen field — it is an orphan.
- The same JSON contains `"distinct_accessed": "ERR:database disk image is malformed"` — one robustness measure failed on a corrupted read of the 2.1 GB store; undisclosed in the paper.
- **Reconciliation required (author):** pin **one** `cir.db` snapshot; run `PRAGMA integrity_check`; regenerate `stage0_robustness.json` from the clean snapshot; quote denominators in the paper *identical to the regenerated figure-data file*; disclose the malformed-read and confirm the headline figures come from the intact copy. The percentages round to the same values, so the headline survives — but the denominators must reconcile before posting.

### B2. `cir.db` figures (Stage 0, decay, patterns, contradictions) have no snapshot digest (repro-B2)
- The provenance block digests only `cir-run-outcomes.jsonl`. The store backing four of five findings has no sha256 / byte size / mtime / `user_version` / as-of instant, and it mutates as post-intervention runs accrue.
- **Required (author):** pin+digest the snapshot (see B1) and record its metadata; the paper's new *Data and code availability* section already commits to this — it must actually be produced before arXiv.

### B3. 98.97% chain-intact does not reconcile with 109 breaks (repro-m1)
- 109 breaks over ~11,105 links ≈ 99.02% intact, not 98.97% (which implies ~114–115 breaks). The break count, the intact-%, and the link denominator are mutually inconsistent as frozen.
- **Required (author):** re-derive on the pinned ledger snapshot; state the exact link denominator; make N-breaks and %-intact agree. Also characterize the **1** residual break currently absorbed into "almost all (108)".

### B4. "~16% of runs receive injection" has no derivation and doesn't reconcile (stats-F9)
- Appears in frozen `c25` and the funnel doc with no numerator/denominator; not derivable from the stated arms (24/45 = 53%). I removed the unsupported "~16%" phrasing from §3 (replaced with "almost entirely experiment-driven"), but the frozen sources still carry it.
- **Required (author):** either source the 16% (state its numerator/denominator) or drop it from the frozen docs.

### B5. Off-by-one: 1,847 patterns vs 1,846 crystallize operations (stats-F14, repro-m4)
- Unexplained +1. I removed "(1,846 crystallize operations)" from the paper §4 to avoid restating an unreconciled pair, keeping only the frozen 1,847.
- **Required (author):** confirm the two frozen counts and explain the +1, or reconcile to one count.

### B6. Decay stratum counts (n=1,964; 217,629) vs funnel total (409,404) (stats-F10, repro-M4)
- Resolved in the paper prose as a **different snapshot** (C3/C3a is the 2026-06-10 analysis, 217,629 rows; funnel is 2026-06-29, 409,404 rows) — this is source-supported (`results/2026-06-10-c3-epistemic-entropy.md`) and now stated in §4. **No frozen edit needed**; listed here for completeness. Confirm n=1,964 against the C3a source at final proof.

---

## C. Field-positioning fact to verify before posting (field-F4)

### C1. Wiese 2026 preregistration attribution
- The paper previously claimed Wiese 2026 (PLOS One, `10.1371/journal.pone.0339920`) "reports preregistered longitudinal LLM evaluations." Crossref title = "Human-anchored longitudinal comparison of generative AI with a bias-calibrated LLM-as-judge" — no preregistration in the record. **Applied fix:** §7 no longer attributes preregistration to Wiese; the freeze-predictions discipline is now framed as this paper's own commitment. If the author confirms Wiese *is* preregistered (registry/OSF id), the alliance can be reinstated with the registration cited; otherwise leave as-is.

---

## Applied in this pass (safe prose hardening — no frozen numbers touched)

- **Field positioning (field-F1/F2/F3/F5/F6):** replaced the incorrect "inject" verb with the class-split framing (systems *retrieve* from own stores; benchmarks *provide* a guaranteed-relevant corpus); reframed "assume return happened" → conditional-retrieval-quality vs our unconditional organic base rate; "track agent interactions" → "capture provenance and behavioral analytics"; scoped "the whole field"/"every retrieval benchmark" → "the memory-evaluation literature."
- **True zero → floor (stats-F4, validity-M3, repro-B3):** pattern non-reuse demoted to a floor (same silent-failure instrument class as Stage 2; C9 gate unmet), resolving the contradiction with §8; abstract and Fig 2 caption aligned.
- **Funnel composition (stats-F1-adjacent, validity-M2):** §3 now states Stage 0 is organic/per-row and Stages 1–3 are experimental/per-run; "multiplicative … capped" replaced by a weakest-link chain framing that does not claim the stages multiply. (The frozen `c25` still says "multiplicative funnel" — reconcile at the A1 amendment.)
- **Operational definitions (validity-B1, repro-M2/M3):** "accessed" = `access_count>0` (engine-written, model-independent); `context_used` = `event_type='context_used'`; "feature-class" = excludes {fixture,smoke,infra}; "post-measurement-fix" pinned to 2026-06-15T02:57:24Z.
- **Construct validity + censoring + single-system scoping (validity-M4, stats-F3, repro-M10):** new §8 paragraphs scoping the claim to *instrumented* return, naming trace-free reuse as out of scope, disclosing right-censoring of the Stage-0 rate, and naming the enabling conditions under which the base rate should transfer.
- **Power (stats-F5):** Stage 3 now states ~2 pp difference and MDE ≈ ±35 pp at n=24/21 (arms uninformative), replacing the bare "underpowered."
- **Misplaced-footer over-claim (validity-M5):** §5 weakened — an out-of-position `CIR_USED:` proves emission, not use; the diagnostic *bounds* rather than resolves use-when-offered.
- **Pooling / regime boundaries (validity-m7/m12):** §5 states which metric classes respect which boundaries and declares 2026-07-02T18:43:00Z as the third boundary.
- **Observatory-semantics overclaim (repro-M5/M6):** §2 scoped — run-outcome funnel counts use observatory semantics; the median missing-footer rate and the genuine-resolution contradiction count are analysis-specific and stated where they appear.
- **Data & code availability (repro-B1):** new section added (proprietary store; digests + scripts + figure-data JSONs released; pinned snapshot metadata) — contingent on B1/B2 above being executed.
- **Citations (repro-n1):** provenance now points at `applications/2026-07-04-citations-reverified.json` (11/11 verified against live arXiv API + Crossref today).
- **Figures:** redrawn from a committed reproducible source (`paper/figs.py`, validated house palette); fig4 stale "not yet shipped" corrected to "shipped 2026-07-02; gate closed pending accrual."

## Resolution ledger (2026-07-04)

- **A1 — RESOLVED.** C25 `## Amendment 1` (dated, pre-gate, verdict null) restates P1 on the per-run unit; paper §6 updated. Re-derived per-run baseline: organic 0/244 = 0.0%, experiment-inclusive 6/289 = 2.08%; post must clear 2.08% (Wilson LB) and organic must become detectably >0. The 0.0222% per-row rate is retained only as the Stage-0 descriptive statistic. Original frozen predictions preserved verbatim as the audit trail.
- **B1/B2 — RESOLVED.** Pinned snapshot (sha256 `0b320d9d…`, integrity_check ok). `stage0_robustness.json` regenerated from it (no malformed read; distinct_accessed = 91). Numerator 91 invariant across as-of (91/392,947 = 0.0232%), frozen read (91/409,404 = 0.0222%), snapshot (91/433,155 = 0.0210%), all-signals (91/447,709 = 0.0203%). Paper §3 + Fig 1b rewritten around numerator invariance; the orphan "424,304" is gone. Data & Code Availability + provenance now cite the real snapshot digest and the re-derivation instrument.
- **B3 — RESOLVED.** The 12,129-row checked-in ledger that produced the derived "98.97%" is not co-located (only a 6-line sample + `verify_ledger.py` remain in `mentu-complete/protocol/`), so the ambiguous percentage is dropped. Paper §2 now states the audit-confident counts: 100% content integrity (11,106/11,106), 109 link breaks (108 workspace-switch + 1 residual), no content-hash failures — consistent, no derived-% arithmetic to mismatch.
- **B4 (~16%) — RESOLVED (removed).** The unsourced "~16% of runs" is out of the paper (§3 says "almost entirely experiment-driven").
- **B5 (1,847 vs 1,846) — EXPLAINED.** The +1 is structural and persistent: kind=pattern exceeds op=crystallize by exactly one on the current snapshot too (2,004 vs 2,003) — a seed/non-crystallize pattern, not a counting artifact. The parenthetical count was removed from §4.
- **B6 (217,629 vs 409,404) — RESOLVED.** Different snapshots (decay = 2026-06-10 C3/C3a; funnel = 2026-06-29); stated in §4.
- **C1 (Wiese preregistration) — RESOLVED.** Attribution removed; freeze-predictions framed as this paper's own commitment.

## Confirmation pass (2026-07-05) — re-refereed v1.2 + closed the two ready-gaps

A second four-lens pass (`docs/referee/B2v2-{stats,field,validity,repro}.md`) re-audited
the revised paper and hunted regressions. Outcome: field 7/7 resolved; stats 13R/2P/1NR;
validity 11R/4P/2NR; repro 17R/3P/1NR. All prior blockers confirmed resolved. **Gap #1
(decay) closed** (`paper/return-base-rate-decay-verification-2026-07-05.md`): frozen figures
match the authoritative 2026-06-10 source exactly, and the finding corroborates on the live
snapshot (negative Δ every bucket, 0 boosted). **New regressions the pass caught, all now
fixed:**
- **repro-R2 (major):** Figure 4 still rendered the superseded "≥10×" P1 → regenerated to the
  per-run baseline (0/244; 6/289=2.08%) and Wilson-LB predictions.
- **repro-R1 (major):** provenance over-attributed the pattern/contradiction counts to the
  pinned snapshot (which gives 2,004 / 81) → §4 + provenance now attribute 1,847 / 76 / 2 / 74
  to the frozen 2026-06-29 read, with the snapshot-growth note (2,004 patterns; 81 detected;
  resolutions still 2) mirroring the Stage-0 invariance treatment.
- **stats-R1 (moderate):** "true zero" reintroduced for organic 0/244 → reworded to an
  *offer-limited* zero (distinct from the footer-channel floor) in §6 and the C25 amendment.
- **stats-R3 / repro-R4 / stats-F3 / F13 / F11 / fig2a-R3:** access-continuity across the
  2026-07-02 boundary stated (§5); P1 baseline source corrected to the outcomes JSONL (§6);
  numerator-invariance connected to the censoring bound + descriptive-vs-inferential note (§8);
  conditional use-when-offered [25%,92%] added (§3); fig2a "0 boosted" annotation demoted.
- **stats-R4:** C25 amendment now records that "multiplicative funnel" is superseded by the
  weakest-link framing (frozen-doc reconciliation).
Residual known-minors (non-blocking, documented): validity-m8 (91-vs-24 relationship),
validity-m11 (randomization mechanism undescribed), repro-M7 (ledger integrity inherently
un-recomputable by outsiders given proprietary data), n2 (companion arXiv id pending upload).

## Remaining before arXiv
- **C25 `## Amendment 1` — RATIFIED by author 2026-07-05** (pre-gate; verdict null).
- **arXiv LaTeX package — BUILT** at `paper/arxiv/return-base-rate/` (self-contained `.tex` + `figs/` + `00-ARXIV-SUBMISSION.md` metadata + `return-base-rate-arxiv.tgz`; verified to compile from a clean extraction). Abstract 1,570 chars (limit 1,920); primary cs.SE, cross-list cs.AI; license CC BY 4.0 [human confirm].
- **Human-only steps left:** (1) arXiv endorsement for cs.SE; (2) confirm license; (3) insert the companion ECX arXiv id in §7 (coordinated pair); (4) upload the tarball + submit. ECX (Paper 3) needs its own arXiv package built for the same-week coordinated post.
