# B2 — Adversarial statistics / empirical-methods referee report

*Lens: empirical methods and statistics only. Numbers cross-checked textually (no
recomputation of frozen values, no database access) against
`corpus/conjectures/c25-return-intervention.md` and
`applications/2026-07-01-return-funnel-and-footer-root-cause.md`. Frozen-number
anomalies are flagged as discrepancies for escalation, not "fixed."*

Target: `paper/return-base-rate-paper.md` (draft v1.1, 2026-07-04).

---

## Findings

### F1 — The preregistered primary endpoint (P1) compares incommensurable quantities
**claim attacked:** the frozen primary test — post-intervention "return rate" vs the 0.0222% baseline "by at least an order of magnitude" via a two-proportion test.
**severity:** blocker
**exact quoted line:**
> **P1 (primary, frozen).** Building the organic-offer pathway raises the return rate to ≥10× the baseline organic-offer rate (0.0222%), with the post-arm's own 95% lower bound clearing that threshold (guarding against a single-run artifact) and a two-proportion test at α=0.05.

**why it fails:** The baseline 0.0222% is an *access* rate on *trust-state rows* (`91 / 409,404`, per `c25` `baseline_frozen.organic_offer_accessed_pct` = `trust_state accessed 91/409404`). The post-intervention "return rate" is defined in the same `c25` file as a *per-run* rate of a *different event*: "fraction of runs where a prior signal is *offered AND used* (`use_rate>0` with a positioned footer)." So the frozen two-proportion test puts a per-trust-state-row **access** proportion against a per-run **offered-AND-used** proportion. Different sampling units (rows vs runs) *and* different events (accessed vs used). A "10×" ratio between them is not a coherent quantity, and the two-proportion / Fisher test has no valid null because the two arms are not draws from a common population. This also means the paper never absorbed audit point #9 ("access ≠ use — the true return event is 'changed a future decision'"): the headline and the P1 baseline are still anchored on *accessed*, while the post arm is scored on *used*.
**proposed fix:** Redefine P1 so baseline and post are the *same rate on the same unit*. Concretely, freeze a per-run baseline "return rate" (runs in the read-only baseline where a prior signal was offered-and-used ÷ baseline runs) and compare the post-run rate against *that*; keep the 91/409,404 access figure as the Stage-0 descriptive statistic only, not as the P1 comparator. If the maintainers intend the row-based baseline to stand, state explicitly that P1 is a one-sample test of the post-run rate against a *fixed reference constant* 0.222%, and drop the "two-proportion" language (a two-proportion test on unequal units is invalid). Either way, add one sentence defining the numerator and denominator of the post "return rate" in the paper body — it is currently undefined in-text.

### F2 — The headline 0.0222% is denominator-dependent; the "robustness" check omits the denominator that moves it
**claim attacked:** that the ever-accessed rate is robust to denominator choice.
**severity:** major
**exact quoted line:**
> The rate is robust to the choice of denominator — 0.0214% against all 424,304 signals in the store, 0.0222% against trust-state rows — because the numerator (91 accessed signals) is the binding quantity, not the denominator (Figure 1b).

**why it fails:** The two denominators shown (424,304 and 409,404) differ by only 3.6%, so of course the rate barely moves — this demonstrates nothing. The scientifically load-bearing denominator is the *ledgered signal count* the paper itself introduces in §2 ("12,129 signals over 2026-03-31 → 2026-06-28"). Against 12,129 the ever-accessed rate is **91/12,129 = 0.75%** — 34× the headline and two orders of magnitude off "10⁻⁴." The paper's own framing ("captured knowledge is almost never reused") makes the ledgered signal the natural unit of "captured knowledge," not the 409,404 trust-state rows (which are an operational store that may carry many rows per signal). Choosing the largest denominator produces the most dramatic number, and the "robustness" sentence quietly excludes the small one. Separately, the numerator/denominator units are mislabeled: the prose says "91 of 409,404 **signals**" but 409,404 is trust-state **rows** (§2), while the ledger has 12,129 signals — the abstract's "91 of 409,404 signals" conflates the two.
**proposed fix:** Report the rate against all three denominators explicitly (12,129 ledgered signals → 0.75%; 409,404 trust-state rows → 0.0222%; 424,304 all store rows → 0.0214%), state which is the primary reported figure and *why* (define what a trust-state row is and why it, not the ledgered signal, is the correct base for "ever accessed"). Replace "robust to the choice of denominator" with an honest statement that the qualitative conclusion (return far below capture) holds across denominators while the point estimate spans 0.02%–0.75%. Fix the "signals" vs "rows" wording in the abstract and Stage 0.

### F3 — "Ever accessed" is right-censored; no exposure-time adjustment
**claim attacked:** the 0.0222% base rate as an unbiased estimate of return propensity.
**severity:** major
**exact quoted line:**
> 91 / 409,404 signals (**0.0222%**) were ever accessed after capture; 24 `context_used` events exist in the entire history.

**why it fails:** "Ever accessed" pools signals with radically different exposure windows. A signal captured on 2026-03-31 had ~90 days to be accessed before the 2026-06-29 snapshot; one captured on 2026-06-28 had ~1 day. Recently captured signals are effectively guaranteed non-accessed and drag the pooled rate down — classic right-censoring. The paper contains no survival/exposure framing, no restriction to signals with a minimum exposure window, and no acknowledgment of the bias. The direction of the bias matters for the intervention: the 0.0222% baseline is the anchor for the "≥10×" P1 threshold, so a censoring-deflated baseline makes the preregistered bar artificially easy to clear.
**proposed fix:** Add an exposure-time robustness cut: report the ever-accessed rate restricted to signals captured at least N days before the snapshot (e.g. N=30 and N=60), or a Kaplan-Meier-style access curve. State whether the rate stabilizes once young signals are excluded. Add one sentence to §8 (Limitations) naming right-censoring and its downward bias, and confirm the P1 baseline is (or is re-derived on) an exposure-matched cohort.

### F4 — Pattern non-reuse "true zero" is not held to the measurement-validity standard the paper applies to Stage 2
**claim attacked:** that pattern non-reuse is a "true zero, distinct from a measurement gap."
**severity:** major
**exact quoted line:**
> We find no evidence that crystallized patterns are selected or used in later runs — a true zero, distinct from a measurement gap: the patterns exist and are queryable; they are simply not returned into subsequent work.

**why it fails:** The paper's central methodological virtue is skepticism about its own instrument — Stage 2 is explicitly downgraded to a "floor, not a measurement" because the use-recording channel is silent (§5). But pattern reuse is asserted as a *complete* null ("true zero") without demonstrating that the channel which would record pattern selection/use is any more reliable than the footer channel that failed at Stage 2. Absence of evidence (which the abstract correctly states: "show no evidence of downstream reuse") is being upgraded to evidence of absence ("true zero") in the body and Figure 2b ("a true zero, not a measurement gap"). If pattern-use recording shares the fragility that produced the Stage-2 floor, "true zero" is itself a floor. The two framings are also internally inconsistent (abstract = "no evidence"; §4 + figure = "true zero").
**proposed fix:** Either (a) demonstrate that pattern selection/use is recorded through an independent, validated channel — describe it and show it can register a positive when one exists (a calibration/positive-control) — and only then keep "true zero"; or (b) downgrade to "no evidence of reuse; if this channel is subject to the same silence as Stage 2, it is a floor," matching the abstract. Make the abstract and body use the same term.

### F5 — "Underpowered" (Stage 3) is asserted, never quantified
**claim attacked:** the Stage-3 no-separation claim and its "underpowered" characterization.
**severity:** major
**exact quoted line:**
> **Stage 3 — task-lift.** Injected success 13/24 (54%) vs withheld 11/21 (52%): no separation. At n=24/21 this is underpowered and, per our preregistered gate, validates the instrument rather than the effect.

**why it fails:** A statistics referee will not accept "underpowered" without a number. The 2-point difference (54% vs 52%) carries a 95% CI on the difference of roughly **[−27 pp, +31 pp]** (normal approx, SE ≈ 0.149) — i.e. the data are consistent with a large lift *or* a large harm, which is the actual content of "no separation." At n=24/21 and a ~52% base, the minimum detectable effect at 80% power / α=0.05 is on the order of ±35 pp. None of this is stated, so "no separation" reads as evidence of no effect rather than absence of evidence.
**proposed fix:** Replace with a quantified sentence, e.g.: "Injected 13/24 (54%) vs withheld 11/21 (52%); the difference is +1.8 pp (95% CI [−27, +31] pp). At this n the minimum detectable effect at 80% power is ≈±35 pp, so the arms are uninformative about lift — per the preregistered gate this validates the instrument, not the effect." This turns an assertion into a defensible power statement.

### F6 — Decay's "0 boosted" is largely tautological given the stratum definition
**claim attacked:** "0 boosted / nothing ever drifts upward" as independent corroborating evidence.
**severity:** minor
**exact quoted line:**
> Among signals never accessed after capture, effective confidence declines monotonically with age and *nothing ever drifts upward*: mean effective−asserted confidence is −0.270 at >60 days, with 55.0% of >60-day signals decayed and 0 boosted (n=1,964 in that stratum; 217,629 trust-state rows overall).

**why it fails:** The stratum is "signals *never accessed* after capture." If boosting requires reinforcement, and reinforcement requires access, then "0 boosted" in the never-accessed stratum is entailed by construction, not discovered — the paper concedes as much one sentence later ("Confidence decays exactly as configured because the reinforcement that would counter it almost never happens"). Presenting a mechanical consequence of the filter (and repeating it in the Figure 2 caption, "0 boosted in every stratum") as an empirical asymmetry overstates the corroboration.
**proposed fix:** Reframe: "By construction this stratum is unreinforced, so the informative quantity is the *magnitude and monotonicity* of decay (−0.270 at >60 days, 55.0% decayed), not the absence of boosts, which the filter guarantees." Drop or caveat "0 boosted in every stratum" in the caption.

### F7 — The three corroborating findings are called "independent" but are views of one mechanism
**claim attacked:** independence of the three corroborating channels.
**severity:** minor
**exact quoted line:**
> The base rate is not an artifact of one metric. Three independent corpus findings point the same way (Figure 2).

**why it fails:** Decay, pattern non-reuse, and contradiction backlog are not statistically independent — the paper itself says the decay result is "the same non-return, seen from the confidence side." Non-return is the common cause of all three, so agreement among them is expected and does not multiply the evidence the way "independent" implies. This is a mild garden-of-forking-paths / pseudo-replication concern.
**proposed fix:** Replace "three independent corpus findings" with "three complementary views of the same non-return" (or "three distinct metrics"), and drop any implication that concordance provides independent confirmation.

### F8 — The Wilson-score lower-bound guard is under-specified
**claim attacked:** that the guard is described precisely enough to reproduce/adjudicate.
**severity:** minor
**exact quoted line:**
> validation caught a real defect, where a single lucky used run cleared a naive significance test against the 409k-row baseline; we fixed it with a Wilson-score lower-bound guard on the order-of-magnitude claim.

**why it fails:** The description omits three things a referee needs: (1) one-sided vs two-sided — "95% lower bound" (P1) could be the lower limit of a 90% two-sided interval or a one-sided 95% bound; (2) the exact quantity bounded and the threshold it must clear (presumably the Wilson 95% LB of the post-arm return proportion must exceed 0.222%); (3) the composite decision rule — P1 requires *both* the LB clearing the threshold *and* a two-proportion test at α=0.05, so the combined type-I behavior and the tie-break/AND semantics should be stated. The anecdote also usefully reveals that the two-proportion test against a ~fixed tiny baseline is nearly degenerate (any 1–2 returns "clear" it), which is why the Wilson LB is doing the real work — worth saying plainly.
**proposed fix:** State: "The primary decision requires the one-sided 95% Wilson lower bound of the post-arm return proportion to exceed 0.222% (10× baseline); the two-proportion test at α=0.05 is a secondary corroborating check. Because the baseline is estimated on a very large n, the two-proportion test is near-degenerate against it, so the Wilson lower bound is the binding guard." (Also depends on resolving F1 — the bounded proportion must be on the same unit as the baseline.)

### F9 — The "~16% of runs" figure has no stated denominator and does not reconcile with the arm counts
**claim attacked:** the Stage-1 offer-reach statistic.
**severity:** minor (frozen-number provenance — escalate)
**exact quoted line:**
> Even offered injection reaches only ~16% of runs, and almost all of that is the experiment, not organic return.

**why it fails:** No denominator is given for "~16% of runs," and it is not derivable from the stated arm sizes (injected 24 / withheld 21 → 24/45 = 53%, not 16%). The same undefined 16% appears in `c25` and the application doc without a source. A referee cannot tell what population "runs" refers to (feature-class runs? all 971 outcome records?).
**proposed fix:** State the numerator and denominator explicitly (e.g. "X injected runs of Y feature-class runs = 16%"). If the underlying counts are frozen, escalate to confirm the 16% against its source rather than restating it.

### F10 — 217,629 vs 409,404: unreconciled trust-state-row denominators
**claim attacked:** cross-section consistency of the trust-state store between the funnel and the decay analysis.
**severity:** minor
**exact quoted line:**
> mean effective−asserted confidence is −0.270 at >60 days, with 55.0% of >60-day signals decayed and 0 boosted (n=1,964 in that stratum; 217,629 trust-state rows overall).

**why it fails:** Stage 0 uses 409,404 trust-state rows; the decay finding says 217,629 "overall." The paper never explains why the same store has two different totals (different snapshot? rows with both asserted and effective confidence only? a filtered subset?). Unexplained denominator shifts within one dataset invite doubt about which cut underlies which headline.
**proposed fix:** Add one clause reconciling the two counts (e.g. "217,629 rows carry both an asserted and an effective confidence and are eligible for the decay computation, of the 409,404 total"). If the difference is a snapshot mismatch, say so.

### F11 — The Stage-2 floor omits the informative conditional rate and its upper companion
**claim attacked:** the "25% is a floor" presentation.
**severity:** minor
**exact quoted line:**
> Of 24 injected runs, 6 cite prior evidence (`use_rate > 0`) and 4 produce a "useful" verdict. But this 25% is a **floor, not a measurement**: the median missing-footer rate is 1.00 — for half the injected arm the use-recording channel is entirely silent (§5).

**why it fails:** Calling 6/24 a floor is directionally valid (the anti-gaming guard implies the channel produces false negatives, not false positives, so observed use ≤ true use). But the paper leaves the interval one-sided and drops the most informative pre-fix estimate: of the 8/24 runs whose channel actually worked ("footer present, mfr<1.0," per the application doc), 6 cited — a *conditional* use-when-offered of **6/8 = 75%** (with an obvious selection caveat that runs which positioned the footer may differ from those that didn't). The honest bracket is: true use-when-offered ∈ [6/24 = 25%, (6+16)/24 = 92%], with a channel-working point estimate of 75%.
**proposed fix:** Add: "Conditional on the recording channel working (8/24 runs with a positioned footer), 6 cited — 75%, though this cohort may be selected. The true use-when-offered lies in [25%, 92%]; we report 25% as the floor." This strengthens the section without loosening the credit contract.

### F12 — "Accumulate faster than they are retired" is asserted from a stock, not a flow comparison
**claim attacked:** the contradiction-backlog growth claim.
**severity:** minor
**exact quoted line:**
> Contradictions are surfaced but not retired — the corpus keeps the tension rather than resolving it, and the backlog grows.

**why it fails:** The evidence given is a *stock* (74 open, 2 resolved, resolution rate 2.6%, longest 21.5 days). "Accumulate faster than retired" / "the backlog grows" is a statement about *flows over time* (detection rate vs resolution rate) that is never shown as a time series. A high open-stock is consistent with growth, plateau, or a one-time burst followed by stasis. The claim may well be true but is not demonstrated.
**proposed fix:** Either show detection and resolution counts per unit time (even a two-point comparison), or soften to a stock statement: "the stock of open contradictions (74/76) dominates resolutions (2), and the oldest has stood 21.5 days" — dropping the unproven flow claim.

### F13 — Multiple-comparison exposure across the funnel and corroborating findings (assessment)
**claim attacked:** whether the paper's many reported quantities inflate false-positive risk.
**severity:** minor
**exact quoted line:**
> a two-proportion test at α=0.05.

**assessment:** Largely controlled, worth one sentence. Most funnel/corroborating quantities are *descriptive* (counts and rates), which do not incur multiple-testing penalties. The genuinely inferential claims are (a) the preregistered C25 primary endpoint with a single frozen primary hypothesis (good MC hygiene) and (b) the Stage-3 two-proportion comparison. The main residual MC-adjacent risk is rhetorical, not statistical: framing three co-caused metrics as "independent" corroboration (see F7). No formal correction is required, but the paper should say the descriptive metrics are not hypothesis tests and that C25's family-wise error is controlled by a single preregistered primary endpoint (P2/P3 secondary).
**proposed fix:** Add to §6 or §8: "The corroborating findings (§4) are descriptive, not hypothesis tests; the only frozen inferential endpoint is P1, with P2/P3 secondary, so no multiplicity correction is applied to the funnel decomposition."

### F14 — 1,847 patterns from 1,846 operations (unexplained off-by-one)
**claim attacked:** internal consistency of the pattern count.
**severity:** nit (frozen-number discrepancy — escalate)
**exact quoted line:**
> The system crystallized 1,847 reusable patterns (1,846 crystallize operations).

**why it fails:** 1,847 patterns from 1,846 operations is an unexplained off-by-one (one operation yielding two patterns, a seed pattern, or a counting artifact). Harmless to the argument but a referee will note it.
**proposed fix:** Add a half-clause explaining the +1, or escalate to confirm the two frozen counts.

### F15 — One hash-chain break is unexplained under a tamper-evidence claim
**claim attacked:** the integrity quantification (adjacent to the stats lens).
**severity:** nit
**exact quoted line:**
> The single global chain is 98.97% intact; the 109 breaks are almost all (108) workspace-context switches, not tampering.

**why it fails:** "almost all (108)" of 109 leaves exactly one break unaccounted for. For a chain offered as tamper-evidence, an unexplained break should be classified (benign cause vs unknown) rather than left in "almost all." Minor and outside the core statistics lens, but it is a quantitative integrity claim.
**proposed fix:** State the cause (or "cause unknown, under review") of the single residual break, so the integrity accounting is complete: 108 context-switch + 1 [category].

### F16 — "For half the injected arm ... silent" understates the actual fraction
**claim attacked:** the precision of the Stage-2 silence statement.
**severity:** nit
**exact quoted line:**
> the median missing-footer rate is 1.00 — for half the injected arm the use-recording channel is entirely silent (§5).

**why it fails:** Per the application doc, 8/24 runs have a positioned footer, so 16/24 ≈ 67% are fully silent — closer to two-thirds than half. "Half" is defensible as a floor implied by median=1.00, but it undersells the finding.
**proposed fix:** "for roughly two-thirds of the injected arm (16/24; median missing-footer rate 1.00) the channel is entirely silent."

---

## Overall verdict

The negative result is real and the qualitative claim — captured knowledge is returned at a rate far below the volume at which it is captured — survives scrutiny; the exclusions discipline and the pre-registration are genuine strengths. But three defects keep this below submission-grade as written. First (blocker, F1), the frozen primary endpoint P1 compares a per-trust-state-row *access* rate against a per-run *use* rate, so the "10×" threshold and two-proportion test are ill-defined and the paper has not absorbed the audit's access≠use point at the level of its own primary hypothesis. Second (major, F2), the headline 0.0222% is denominator-dependent — it is ~0.75% against the 12,129 ledgered signals the paper itself introduces — and the "robust to denominator" check only spans two denominators 3.6% apart, omitting the one that moves the estimate by 34×. Third (major, F3), "ever accessed" is right-censored with no exposure adjustment, biasing the base rate downward and easing the preregistered bar. Alongside these, the "true zero" pattern claim is not measurement-validated to the standard the paper rightly applies at Stage 2 (F4), and "underpowered" is asserted without the CI or MDE that would substantiate it (F5). None of these overturns the direction of the result, but each must be fixed — and F1 in particular before the C25 gate opens, since it is baked into a frozen artifact. Escalate the frozen-number items (F9 the unsourced 16%, F14 the 1,847/1,846 off-by-one) rather than editing them.
