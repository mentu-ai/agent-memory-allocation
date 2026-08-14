# Referee report B2 — Measurement-validity lens

*Adversarial review of `paper/return-base-rate-paper.md` (Draft v1.1, 2026-07-04).*
*Lens: measurement validity only. Report-only. Numbers frozen — discrepancies flagged, nothing recomputed.*
*Cross-checks used as fixed context (not re-derived): `external-critique-audit-2026-07-02.md`,
`corpus/conjectures/c25-return-intervention.md`, `applications/2026-07-01-return-funnel-and-footer-root-cause.md`.*

---

## Blocker

### B1 — The headline numerator has no operational definition, and its instrument is self-impeached
- **Claim attacked:** The entire paper's headline, that return is "effectively zero," rests on the predicate *"ever accessed after capture,"* which is never operationally defined. What event marks a trust-state row as "accessed"? A non-null last-read timestamp? An access counter > 0? Membership in a `context_used` join? A referee cannot judge whether "91" is correct — or whether the access channel silently drops events the way §5 proves the *use* channel does — without the definition. This is not a peripheral quantity; it is the binding numerator of the paper.
- **Severity:** blocker
- **Exact quoted line:** "Only 91 of 409,404 signals (0.0222%) were ever accessed after capture" (Abstract); and §3 Stage 0: "91 / 409,404 signals (**0.0222%**) were ever accessed after capture … the numerator (91 accessed signals) is the binding quantity".
- **Proposed fix:** Add one paragraph in §2 or §3 defining the *access event* operationally: the exact field/table/predicate in the trust-state store that flips a signal to "accessed," when the engine writes it, and — critically, given §5 — evidence that this channel does *not* have a silent-failure mode analogous to the footer channel (e.g., that access is written deterministically by the engine, not conditionally on a model-emitted token). Until "accessed" is defined and its instrument's fidelity established, the headline number is unassessable.

---

## Major

### M2 — The "multiplicative funnel" does not compose: incommensurable units and two different regimes
- **Claim attacked:** Stage 0 is measured per **signal/trust-state row** (n=409,404) in the *organic, no-experiment* world; Stages 1–3 are measured per **run** (n=24/21) inside a *forced-injection experiment*. These are different units on different populations under different conditions. A signal that was never organically accessed (Stage 0 denominator) is not the same object that flows into an injected run (Stage 1–3 denominator), so the stages cannot be multiplied and the inference that Stage 2/3 gains are "capped by the 10⁻⁴ organic-offer rate at Stage 0" does not follow — it compares an organic-world rate to experiment-world rates. Figure 1 compounds this by plotting "signal counts across the funnel on a log axis" when Stages 1–3 are runs, not signals.
- **Severity:** major
- **Exact quoted line:** "The funnel is multiplicative: even a large improvement at Stage 2 or 3 is capped by the 10⁻⁴ organic-offer rate at Stage 0." (§3); and Figure 1 caption: "Signal counts across the funnel on a log axis".
- **Proposed fix:** Either (a) recast the "funnel" as what it is — a panel of related-but-non-composable metrics from two regimes (organic vs experimental), dropping the multiplicative-cap language and the single-axis signal-count figure; or (b) re-express every stage on one common denominator and unit (e.g., per-run through a single pipeline) so the stages genuinely compose. State explicitly that Stage 0 is organic and Stages 1–3 are the injection experiment.

### M3 — "true zero" (pattern non-reuse) and "floor" (Stage 2) are a double standard on the same silently-failing instrument
- **Claim attacked:** Stage 2 is correctly downgraded to a "floor, not a measurement" because the trace-emission instrument is silent for half the arm (§5). Pattern non-reuse rests on the *same* class of instrument — detection of a trace when reuse occurs — yet is elevated to a "true zero, distinct from a measurement gap." The only justification offered is that "the patterns exist and are queryable," which establishes that patterns *could* be returned, not that a return *would be detected* if it happened. Given §5 demonstrates this instrument routinely fails to record use that occurred, calling one result a floor and the other a true zero is internally inconsistent.
- **Severity:** major
- **Exact quoted line:** "no evidence that crystallized patterns are selected or used in later runs — a true zero, distinct from a measurement gap: the patterns exist and are queryable; they are simply not returned into subsequent work." (§4)
- **Proposed fix:** To keep the "true zero," name the *reliable* detection channel for pattern selection (e.g., an engine-written crystallize→select edge that does not depend on a model-emitted token) and show it lacks the failure mode of the footer channel. If no such channel exists, demote "true zero" to "no *detected* reuse," symmetric with the Stage-2 floor.

### M4 — Construct validity: "return" is measured only where the engine writes a trace; the target construct is two layers above what is measured
- **Claim attacked:** Return/reuse is operationalized entirely by engine-emitted traces (accessed rows, `context_used` events, `CIR_USED` footers). Reuse that leaves no trace — a human reading a signal in the ledger and acting on it, or a model using context without emitting a footer — is invisible by construction, so the claim is really "*instrumented* return ≈ 0." The program's own audit already establishes that access ≠ use and that the true return event is "changed a future decision" (external-critique-audit #9, adopted as a decision-linkage amendment). The paper measures at the access/footer layer, which sits below that target construct, and never lists this gap in §8 Limitations.
- **Severity:** major
- **Exact quoted line:** "does captured knowledge get returned and reused *at all*?" (Abstract) — operationalized only as "ever accessed," "context_used events," and the "`CIR_USED:` footer the model must emit" (§3, §5), with no limitation acknowledging trace-free reuse.
- **Proposed fix:** Add a construct-validity paragraph to §8: state that the measured construct is instrumented, engine-visible return, that trace-free reuse (human or un-footered) is out of scope, and that the target construct ("changed a future decision") is downstream of what is measured. Scope the headline accordingly (e.g., "instrumented return").

### M5 — "misplaced footer = used it but mis-formatted the proof" over-claims and reuses a token the anti-gaming guard deems untrustworthy
- **Claim attacked:** The absent/misplaced decomposition is credit-safe (the diagnostic grants no credit), and that anti-gaming rationale is sound. But P2 reads the *misplaced* count as behavioral evidence of genuine use ("used it but mis-formatted the proof"). A `CIR_USED:` string appearing anywhere proves only that the token was emitted, not that context was used — and an out-of-position `CIR_USED:` line is exactly what the guard exists to distrust ("a model could scatter stray `CIR_USED:` lines to farm reuse credit"). The same token is treated as untrustworthy gaming for credit and as evidence of genuine use for the P2 inference. The guard protects credit but not the measurement claim built on the diagnostic.
- **Severity:** major
- **Exact quoted line:** "This makes 'the model ignored offered context' distinguishable from 'the model used it but mis-formatted the proof'" (§5); paired with "a model could scatter stray `CIR_USED:` lines to farm reuse credit" (§5).
- **Proposed fix:** Weaken the interpretation of `footer_present_unpositioned` from "genuine use, mis-formatted" to "a use *claim* was emitted out of position — necessary but not sufficient evidence of use." Note that the P2 misplaced-vs-absent inference is gameable even though credit is not, and state what would corroborate genuine use beyond the presence of the token.

### M1 (population hygiene) — "trust-state rows" are relabeled "signals," and at least four populations are intermixed without a map
- **Claim attacked:** The paper uses "signals" for two different populations — 12,129 ledger signals and 409,404 trust-state rows — in adjacent sentences, and introduces a third store count (424,304) and a fourth for decay (217,629). The reader cannot tell which population each headline is computed on, and the headline denominator's identity ("signals" vs "trust-state rows") is ambiguous.
- **Severity:** major
- **Exact quoted line:** "an operational store of 409,404 trust-state rows … Only 91 of 409,404 signals" (Abstract); "0.0214% against all 424,304 signals in the store, 0.0222% against trust-state rows" (§3); "217,629 trust-state rows overall" (§4).
- **Proposed fix:** Fix the vocabulary: reserve "signal" for ledger signals and name trust-state rows consistently. Add a short population table in §2 mapping each reported number to its exact population, unit, and time window (ledger signals 12,129; trust-state rows 409,404; store signals 424,304; decay subset 217,629; run-outcomes 971; funnel runs 24/21). State why the decay subset (217,629) differs from the Stage-0 population (409,404).

---

## Minor

### m6 — Run-class filter is never defined for the reader
- **Claim attacked:** Stage 1 states "post-measurement-fix, feature-class runs," but "feature-class" is undefined in the paper. The exclusion set (`EXCLUDED_RUN_CLASSES = {fixture, smoke, infra}`) lives only in the cross-check doc, not the paper. The filter is stated for Stage 1 and carried implicitly to Stages 2–3; other numbers state no filter.
- **Severity:** minor
- **Exact quoted line:** "24 runs were in the injected arm, 21 in the withheld arm (post-measurement-fix, feature-class runs)." (§3)
- **Proposed fix:** Define "feature-class" (= runs excluding fixture/smoke/infra) and "post-measurement-fix" (which fix — the 2026-06-15 boundary) at first use, and state the run-class filter for every run-level number.

### m7 — Pooling rules are declared for one channel and left unstated for the rest
- **Claim attacked:** The no-pool rule is asserted only for use-when-offered across the 2026-07-01 boundary. The paper is silent on whether Stage 0 (91/409,404, spanning 2026-03-31→2026-06-28), decay, pattern, and contradiction numbers pool across the 2026-06-15 footer fix. The lens question "are pooling rules stated and consistently applied to *every* number?" is answered no.
- **Severity:** minor
- **Exact quoted line:** "use-when-offered rates are never pooled across it, exactly as the earlier 2026-06-15 footer fix is treated." (§5)
- **Proposed fix:** State, for each reported number, whether it pools across each declared boundary and why that is valid (e.g., "accessed"/`used`-keyed metrics are continuous across 2026-06-15 per the cross-check doc §6; use-recording is not).

### m8 — Two numerators for "return" (accessed = 91 vs context_used = 24) are never reconciled
- **Claim attacked:** Stage 0 reports 91 accessed signals and, in the same bullet, 24 `context_used` events all-time. These are different instruments giving different counts of "return," and their relationship is unexplained. Which is the offer/return quantity?
- **Severity:** minor
- **Exact quoted line:** "91 / 409,404 signals (**0.0222%**) were ever accessed after capture; 24 `context_used` events exist in the entire history." (§3)
- **Proposed fix:** Explain how "accessed" (91) relates to "context_used" (24) — subset, superset, or orthogonal — and state which operationalizes organic offer for the headline.

### m9 — The two "24"s (context_used all-time vs injected arm) are not disambiguated
- **Claim attacked:** "24 context_used events exist in the entire history" (Stage 0) and "24 runs were in the injected arm" (Stage 1) share a value. If they are the same 24, then essentially *all* context_used events are the experiment (consistent with "almost all of that is the experiment"), and organic context_used ≈ 0 — a stronger, quantifiable claim the paper leaves implicit. If coincidental, that should be said.
- **Severity:** minor
- **Exact quoted line:** "24 `context_used` events exist in the entire history." (§3 Stage 0) vs "24 runs were in the injected arm" (§3 Stage 1).
- **Proposed fix:** State whether the two 24s are the same set. If so, report organic (non-experiment) `context_used` explicitly.

### m10 — Figure 1b tests robustness on the axis that does not matter
- **Claim attacked:** The "robust to the choice of denominator" argument checks 409,404 vs 424,304 (a ~4% denominator swing) while conceding "the numerator … is the binding quantity." The measurement risk is entirely in the numerator (what counts as accessed), which is exactly the axis left untested — robustness theater.
- **Severity:** minor
- **Exact quoted line:** "The rate is robust to the choice of denominator … because the numerator (91 accessed signals) is the binding quantity, not the denominator (Figure 1b)." (§3)
- **Proposed fix:** Replace or supplement the denominator-robustness check with a numerator-robustness check: how the 91 moves under alternative reasonable access-event definitions.

### m11 — Randomization mechanism for the offer experiment is undefined
- **Claim attacked:** The Stage 1–3 arm comparison depends on "within-recipe randomization," but the assignment mechanism is never described, so the reader cannot assess whether arms are exchangeable or confounded by recipe/time.
- **Severity:** minor
- **Exact quoted line:** "Under a within-recipe randomization experiment, 24 runs were in the injected arm, 21 in the withheld arm" (§3).
- **Proposed fix:** One sentence on the randomization unit and mechanism (how a run is assigned to injected vs withheld, blocking within recipe).

### m12 — The 2026-07-02 intervention marker is not declared a regime boundary in the paper
- **Claim attacked:** The C25 file names the intervention commit (`fb85d754`, 2026-07-02T18:43:00Z) a regime boundary ("never pool across it"), but the paper reports the ship date without declaring the no-pool rule, and states the baseline is "before any offer pathway exists" — untrue at the 2026-07-04 draft moment (the pathway shipped 2026-07-02). No post-intervention data is analyzed, so no pooling violation occurs yet, but the boundary should be named for symmetry with 2026-06-15 and 2026-07-01.
- **Severity:** minor
- **Exact quoted line:** "This paper measures the return behavior that engine exhibits before any offer pathway exists" (§7); "the pathway shipped 2026-07-02" (Abstract/§6).
- **Proposed fix:** Declare 2026-07-02T18:43:00Z a third regime boundary with its no-pool rule, and rephrase to "measured over a window before the offer pathway shipped" rather than "before any offer pathway exists."

---

## Nits

### n1 — Pattern count vs operation count off by one
- **Severity:** nit
- **Exact quoted line:** "The system crystallized 1,847 reusable patterns (1,846 crystallize operations)." (§4)
- **Proposed fix:** One clause explaining the 1,847 vs 1,846 discrepancy (pre-existing pattern? one operation yielding two?).

### n2 — One chain break left uncharacterized
- **Severity:** nit
- **Exact quoted line:** "the 109 breaks are almost all (108) workspace-context switches, not tampering." (§2)
- **Proposed fix:** Characterize the remaining 1 break, since the integrity guarantee is load-bearing for the measurement substrate.

### n3 — Integrity check covers 91.6% of signals; analyses' exposure to unhashed rows unstated
- **Severity:** nit
- **Exact quoted line:** "11,106 carry a content hash … The 1,023 unhashed rows are all hook-authored annotations" (§2)
- **Proposed fix:** State whether any funnel/decay/pattern/contradiction number is computed over the 1,023 unhashed (unverifiable) rows.

### n4 — Date-format inconsistency for the earlier boundary
- **Severity:** nit
- **Exact quoted line:** "exactly as the earlier 2026-06-15 footer fix is treated." (§5) vs the cross-check doc's `2026-06-15T02:57:24Z`.
- **Proposed fix:** Use the precise timestamp for the 2026-06-15 boundary as for the others.

---

## Overall verdict

On the measurement-validity axis this paper is not yet acceptable, and the gap is fixable but load-bearing. The single blocker is definitional: the headline claim ("return ≈ 0") is built on an "ever accessed" predicate that is never operationally defined, and §5 independently proves that this engine's trace-emission instruments can fail silently — so the reader is asked to trust a numerator whose recording mechanism the paper itself has shown to be unreliable elsewhere. That unresolved tension propagates into the two sharpest internal-consistency problems: the "funnel" is presented as multiplicative and plotted as one signal-count axis, but Stage 0 is a per-signal organic rate while Stages 1–3 are per-run experimental rates, so the stages do not compose and the "capped by 10⁻⁴" inference does not follow; and pattern non-reuse is elevated to a "true zero" while the structurally identical Stage-2 measurement is (correctly) demoted to a "floor," a double standard on the same instrument. Underneath sits a construct-validity gap the program's own audit already acknowledges (access ≠ use ≠ decision-change) but the paper does not surface as a limitation, and a population-hygiene problem in which "trust-state rows" are relabeled "signals" across at least four intermixed populations. None of these require new data — they require operational definitions, a population/unit map, symmetric treatment of the instrument's reliability across findings, and honest scoping of the construct to "instrumented return." The preregistration discipline, the footer root-cause trace, and the regime-boundary machinery are genuine strengths; the measurement *reporting* around them is where the paper currently fails rigor.
