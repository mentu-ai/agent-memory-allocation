# Referee report B2 v2 — Measurement-validity re-review (confirmation pass)

*Adversarial re-review of `paper/return-base-rate-paper.md` (Draft **v1.2**, 2026-07-04),
against the prior B2-validity findings (`docs/referee/B2-validity.md`) and the author's
resolution claims (`docs/escalations/2026-07-04-return-base-rate-B2.md`).*
*Lens: measurement validity only. Report-only — no file but this report was written.
Numbers frozen: discrepancies flagged, nothing recomputed. No new citations. `~/.mentu` untouched.*
*Frozen cross-checks used as fixed textual context (not re-derived): `corpus/conjectures/c25-return-intervention.md`,
`applications/2026-07-01-return-funnel-and-footer-root-cause.md`.*

---

## Summary of dispositions

| ID | Prior severity | Status | One-line |
|---|---|---|---|
| B1 | blocker | **RESOLVED** | "accessed" = `access_count>0`, engine-written, model-independent |
| M1 | major | **PARTIAL** | headline denom fixed to "trust-state rows"; "signals" still names two populations, no population map |
| M2 | major | **RESOLVED** | multiplicative claim dropped; organic/per-row vs experimental/per-run stated; weakest-link bound is valid |
| M3 | major | **RESOLVED** | pattern non-reuse demoted to "floor", symmetric with Stage 2 |
| M4 | major | **RESOLVED** | "instrumented return" scoping in abstract + §8; target construct named downstream |
| M5 | major | **RESOLVED** | misplaced footer weakened to "emission, not use"; diagnostic *bounds* not resolves |
| m6 | minor | **RESOLVED** | "feature-class" and the 2026-06-15T02:57:24Z fix defined at use |
| m7 | minor | **RESOLVED** | per-metric-class pooling rules stated |
| m8 | minor | **PARTIAL** | both counts now defined, but 91-vs-24 relationship still not stated |
| m9 | minor | **NOT-RESOLVED** | the two "24"s (context_used all-time vs injected arm) still not disambiguated |
| m10 | minor | **PARTIAL** | Fig 1b reframed to the numerator (good), but tests *temporal* not *definitional* robustness |
| m11 | minor | **NOT-RESOLVED** | randomization mechanism still undescribed |
| m12 | minor | **RESOLVED** | 2026-07-02T18:43:00Z declared a third boundary with no-pool rule |
| n1 | nit | **RESOLVED** | 1,846 parenthetical removed |
| n2 | nit | **RESOLVED** | residual 1 chain break characterized (non-content-hash → session boundary) |
| n3 | nit | **PARTIAL** | unhashed rows characterized; analysis-exposure statement still absent |
| n4 | nit | **RESOLVED** | 2026-06-15T02:57:24Z precise timestamp now used at first mention |

**Counts: RESOLVED 11 / PARTIAL 4 / NOT-RESOLVED 2.**

---

## Prior findings — detail

### B1 (blocker) — headline numerator operational definition + instrument fidelity → **RESOLVED**
§3 Stage 0 now defines the access event and asserts its fidelity in one clause:
> "91 / 409,404 trust-state rows (**0.0222%**) were ever accessed after capture, where 'accessed' is a recorded access against the row in the operational store (`access_count > 0`), written by the engine independent of any model output".

Both halves of B1 are met: the predicate is operational (`access_count > 0`, exact store field/table implied) **and** the silent-failure concern from §5 is pre-empted — "written by the engine independent of any model output" is precisely the model-token-independence the prior report demanded. The abstract's headline is now on "trust-state rows," not "signals." Resolved.

### M1 (major) — population hygiene → **PARTIAL**
Headline denominator is now unambiguous ("trust-state rows," 409,404), the orphan 424,304 is gone, and §3 explicitly separates the ledger from the store base:
> "The ledger's 12,129 signals (§2) are a distinct population and are not the base for this rate."

But the prior fix ("reserve 'signal' for ledger signals; add a population map") is only half-done. The word "signals" still names **two** populations: 12,129 ledger signals *and* the store total "all 447,709 signals" (§3). No population/unit/window table was added. The load-bearing ambiguity is fixed; a minor vocabulary overload survives on the robustness figure. Partial.

### M2 (major) — funnel composition → **RESOLVED**
The multiplicative claim and single-axis signal-count figure are gone. §3:
> "The stages are therefore related metrics from two regimes, not factors of a single product — we read them as a funnel because each is a necessary link in the same organic-return chain, not because they multiply."

and the cap is now a valid weakest-link *bound*, not a product:
> "it does not itself compose multiplicatively with the organic Stage-0 rate, because it is measured on a different unit and population."

Figure 1a caption now tags "Stage 0 is organic trust-state-row access; Stages 1–3 are per-run counts from the injection experiment." The bound "return ≤ offer" is logically sound (return is a subset of offer). Resolved.

### M3 (major) — true-zero / floor double standard → **RESOLVED**
§4 heading is now "**Pattern non-reuse (floor)**":
> "We report this as a floor rather than a confirmed zero: the reuse-detection channel is the same class of model-trace instrument shown to fail silently at Stage 2 (§5), and the C9 readiness gate … is not yet met."

Fig 2b caption matches ("a floor, since the reuse-detection channel is subject to the same silent failure demonstrated at Stage 2"). The instrument is now treated symmetrically across findings. Resolved.

### M4 (major) — construct validity / instrumented return → **RESOLVED**
Scoped in the abstract ("does captured knowledge get *instrumented* return — surfaced and reused through a recorded channel — *at all*?") and a dedicated §8 paragraph:
> "What we measure is *instrumented* return … the true target construct — that a prior signal *changed a later decision* — sits downstream of what the current instrument records."

Trace-free reuse (human-read, un-footered) is named out of scope. Resolved.

### M5 (major) — misplaced-footer over-claim → **RESOLVED**
The "used it but mis-formatted the proof" reading is gone from §5, replaced by:
> "an out-of-position `CIR_USED:` string proves the token was emitted, not that context was genuinely used … The diagnostic therefore bounds, rather than resolves, use-when-offered".

P2 in §6 is correspondingly conditional ("If the residual non-use is overwhelmingly *misplaced* … the historical loss was a measurement artifact"), not a claim of genuine use. Resolved.

### m6 (minor) — run-class filter → **RESOLVED**
§3 Stage 1: "feature-class runs (i.e. excluding `fixture`, `smoke`, and `infra` run classes) started after the 2026-06-15T02:57:24Z footer-fix boundary." Both terms defined at first use. Resolved.

### m7 (minor) — pooling rules → **RESOLVED**
§5: "Trace-credit metrics (use-when-offered, the footer diagnostic) are the metrics that respect these boundaries; access- and confidence-keyed metrics (Stage 0, decay) are continuous across the 2026-06-15 boundary." Decay pooling also stated in §4. Resolved. (See NEW-1 for the one boundary this rule is *silent* about in practice.)

### m8 (minor) — accessed (91) vs context_used (24) reconciliation → **PARTIAL**
Both are now operationally defined and it is clear the headline uses "accessed." But the prior ask — state whether `context_used` (24) is a subset/superset/orthogonal to `accessed` (91) — is still not answered. They appear side by side (§3) with no stated relationship. Partial.

### m9 (minor) — the two "24"s → **NOT-RESOLVED**
"24 `context_used` events … in the entire history" (Stage 0) and "24 runs were in the injected arm" (Stage 1) still share a value with no statement of whether they are the same set. Not addressed in the resolution ledger; unchanged. Not resolved.

### m10 (minor) — Fig 1b robustness axis → **PARTIAL**
The framing correctly shifted from denominator-robustness ("theatre") to the binding numerator: "The binding quantity is the numerator, and it is invariant." Good. But the specific ask — how 91 moves under *alternative access-event definitions* — is not shown; what is shown is invariance across *time/snapshots* under one fixed definition. Definitional robustness of the numerator remains untested (lower stakes now that `access_count>0` is pinned). Partial. (This same post-intervention-snapshot device is the seat of NEW-1.)

### m11 (minor) — randomization mechanism → **NOT-RESOLVED**
Still only "Under a within-recipe randomization experiment" (§3). The assignment unit and mechanism (how a run is assigned to injected vs withheld, blocking) are not described, so arm exchangeability cannot be assessed. Not resolved.

### m12 (minor) — 2026-07-02 boundary → **RESOLVED**
§5: "The intervention ship on 2026-07-02T18:43:00Z (commit `fb85d754`) is a third such boundary; no post-intervention data is pooled with the baseline reported here." The stale "before any offer pathway exists" framing is gone (§8 now: "shipped 2026-07-02 … after this baseline was frozen"). Resolved as *declared*. Whether the paper *honors* the rule is the subject of NEW-1.

### n1 (nit) — 1,847 vs 1,846 → **RESOLVED**
Parenthetical removed; §4 reports only "1,847 reusable patterns." (Resolution ledger B5 explains the +1 as structural.) Resolved.

### n2 (nit) — uncharacterized chain break → **RESOLVED**
§2: "108 of those coincide exactly with a workspace-context switch … with 1 residual break — none are content-hash failures, so they are session boundaries, not tampering." The residual is now characterized as benign. Resolved.

### n3 (nit) — unhashed-row analysis exposure → **PARTIAL**
§2 characterizes the 1,023 unhashed rows ("hook-authored annotations … an expected out-of-chain lane") but still does not state whether any funnel/decay/pattern/contradiction number is computed over them. (Structurally they cannot be — those analyses run on the operational store, not the ledger — but the paper does not say so.) Partial.

### n4 (nit) — date format → **RESOLVED**
The precise "2026-06-15T02:57:24Z" is used at first mention in §3 and §5. One later bare "2026-06-15 boundary" is acceptable shorthand after the full form. Resolved.

---

## Regressions / new validity issues introduced by the revision

### NEW-1 (MAJOR, fixable) — the post-intervention numerator-invariance device is not scoped in the paper as a baseline-stability check, and sits in tension with the paper's own 2026-07-02 no-pool rule
To answer m10/B1, §3 and Fig 1b now import a **post-intervention** snapshot into the baseline argument:
> §3: "on a pinned, integrity-checked snapshot taken 2026-07-04 (after this baseline was frozen), the accessed count is *still exactly 91* (distinct accessed 91; `context_used` still 24)".
> Fig 1b: "a pinned **post-intervention** snapshot (still 91)".

Two problems, both on the paper's own terms:

1. **No C25-scoping disclaimer in the paper.** The C25 amendment doc carries the exact guard this needs — "as of the 2026-07-04 snapshot (post-ship) `accessed` is still exactly 91 … reported here only as a baseline-stability check, **not** as a post-intervention result (the gate is closed)." The *paper* omits it. "Accessed still 91 two days after the offer pathway shipped" is, on its face, informative about whether the intervention moved the Stage-0 numerator; a reader of §3/Fig 1b alone can read it as a (null) early C25 signal. The paper does **not** anywhere *claim* it as a C25 result (good — no mis-claim), but it also does not *disclaim* it, and does not remind the reader the gate is at 0/150 so the snapshot carries negligible post-intervention exposure.

2. **Tension with the declared boundary.** §5 declares 2026-07-02 a hard boundary — "no post-intervention data is pooled with the baseline reported here" — and lists Stage 0 as continuous only across the *2026-06-15* boundary, saying nothing about 2026-07-02. But Stage-0 organic access is precisely the metric C25 intervenes on, so it must **not** be assumed continuous across 2026-07-02. Yet §3 folds post-intervention-snapshot rates (0.0210% on 433,155 rows; 0.0203% on 447,709 signals, both 2026-07-04) into the baseline robustness range alongside the pre-intervention 0.0222%. This is at least in tension with the paper's own strict freeze-before-results / no-pool discipline — the discipline that is one of the paper's headline strengths.

**Fix (one clause, no new data):** lift the amendment doc's scoping into §3 and the Fig 1b caption — state that the 2026-07-04 snapshot is used only to show numerator *stability* under denominator growth, that the C25 gate is closed (0/150) so it carries no post-intervention signal, and that it is not evidence about C25. Severity major because it touches the paper's central methodological claim and its headline numerator; trivially fixable.

### NEW-2 (minor) — "single pinned snapshot" provenance does not match the reported headline counts
Data & Code Availability: "The `cir.db`-derived figures (Stage 0, patterns, contradictions) are computed against a single pinned snapshot" (sha256 `0b320d9d…`, 2026-07-04). But the reported headline values are the **frozen 2026-06-29** counts — 409,404 trust-state rows, 1,847 patterns, 76 contradictions — which differ from that 2026-07-04 snapshot's counts (433,155 rows; per resolution ledger B5, 2,004 patterns; a larger contradiction stock). The re-derivation instrument reconstructs the as-of-2026-06-29 state from the pinned snapshot, which reconciles this — but the paper does not explain that the "single pinned snapshot" is queried *as-of* an earlier instant, so the availability statement reads as inconsistent with the numbers it backs. Flagging per the numeric-mismatch rule; recommend one sentence clarifying the as-of reconstruction.

### NEW-3 (minor) — two undistinguished 2026-06-29-era denominators
§3 cites "0.0232% as-of the frozen instant" and "0.0222% at the frozen read" as if distinct baseline denominators. Per the resolution ledger these are 91/392,947 and 91/409,404 — two ~2026-06-29 denominators differing by ~16,000 rows, with no explanation in the paper of why "as-of instant" and "frozen read" differ. All rates are 10⁻⁴ so the headline is unaffected, but the two-denominator distinction is opaque. Flag only.

### Regression checks that came back clean
- **Decay-snapshot reconciliation (217,629 @ 2026-06-10 vs 409,404 @ 2026-06-29):** §4 states the two are different snapshots and are not pooled; decay is a within-snapshot stratified analysis, so the snapshot gap does not invalidate it. No new defect. Clean. (Resolution ledger's "confirm n=1,964 at final proof" remains a pending author check, not a defect.)
- **Numerator-invariance as a *statistical* claim:** the "rate stable across every denominator" argument is a sound order-of-magnitude robustness point given a tiny fixed numerator. No new statistical problem beyond the scoping issue in NEW-1.
- **Internal arithmetic spot-checks (flag-only, not recomputed):** 11,106 + 1,023 = 12,129 (§2); 108 + 1 = 109 breaks (§2); 244 organic + 45 arms (24+21) = 289 (§6 P1); 2 + 74 = 76 contradictions (§4) — all internally consistent as written.

---

## Overall verdict

On the measurement-validity axis the revision is a substantial pass: the blocker is fully resolved (the headline numerator now has an operational definition *and* a model-independence argument that neutralizes the §5 silent-failure concern), and all five prior majors except population hygiene are resolved — the multiplicative funnel is recast as a valid weakest-link bound, the true-zero/floor double standard is gone, the construct is honestly scoped to "instrumented return," and the misplaced-footer over-claim is weakened to emission-not-use. Eleven of seventeen prior items are fully resolved; four are partial (residual "signals" overload with no population map; 91-vs-24 relationship unstated; Fig 1b tests temporal not definitional robustness; unhashed-row exposure unstated) and two minor items are untouched (the two "24"s, the randomization mechanism).

The one thing the revision introduced that a hostile referee will seize on is NEW-1: to demonstrate numerator invariance, §3 and Figure 1b pull a **post-intervention** (2026-07-04) snapshot into the baseline and report "accessed still exactly 91" without the baseline-stability-only / not-a-C25-result scoping that the C25 amendment doc itself carries — and that sits in tension with the paper's own hard rule that no post-intervention data is pooled with the baseline, on the very metric (Stage-0 access) the intervention targets. It is not a mis-claim and it is fixable with one imported clause, but until it is scoped, the paper's strongest asset (its freeze-before-results discipline) is self-undercut in the section that carries its headline number. No new data is required for any item.
