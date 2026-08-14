# B2v2 — Confirmatory re-referee (statistics lens), revised paper v1.2

*Re-audit of the 16 prior stats findings (`docs/referee/B2-stats.md`) against
`paper/return-base-rate-paper.md` draft **v1.2** (2026-07-04), cross-checked
textually against the resolution claims (`docs/escalations/2026-07-04-return-base-rate-B2.md`),
the amended conjecture (`corpus/conjectures/c25-return-intervention.md`,
`## Amendment 1`), and the funnel/root-cause application doc. Report-only. Frozen
numbers are cross-checked for internal consistency and flagged, never recomputed.*

**Counts: RESOLVED 13 · PARTIALLY-RESOLVED 2 · NOT-RESOLVED 1.**

---

## Per-finding disposition

### F1 (blocker) — P1 compared incommensurable units (per-row *access* vs per-run *use*)
**STATUS: RESOLVED.** §6 rewrites P1 onto a single per-run unit for both arms:
> "We compare like with like on the *per-run* unit. The primary outcome is the
> per-run return rate — the fraction of feature-class runs where a prior signal
> is offered *and* used (`use_rate > 0` with a positioned footer). The
> pre-intervention baseline ... is 0/244 (0.0%) for organic runs and 6/289
> (2.08%) including the forced-injection experiment ... the post-intervention
> per-run return rate exceeds the experiment-inclusive baseline of 2.08%, with
> the post arm's one-sided 95% Wilson lower bound clearing that threshold, and
> the *organic* per-run rate becomes detectably >0 ... (The 0.0222%
> per-trust-state-row access rate is the Stage-0 descriptive statistic, not the
> P1 comparator; the earlier per-row '≥10×' two-proportion formulation compared
> incommensurable units and is superseded — see the C25 amendment.)"

C25 `## Amendment 1` ratifies the same (dated 2026-07-05, pre-gate, verdict
null; original predictions preserved as audit trail). Both arms are now per-run;
the two-proportion test is dropped for the Wilson-lower-bound rule. The
access≠use conflation at the primary-hypothesis level is gone. **Coherence
check passes: baseline and post are the same rate on the same unit.**

### F2 (major) — headline rate denominator-dependent; "robust" check omitted the moving denominator; "signals" vs "rows" mislabel
**STATUS: RESOLVED.** Two sub-defects both fixed.
- Mislabel fixed: the abstract now reads "Only 91 of **409,404 trust-state
  rows** (0.0222%)" (was "signals"); §3 consistently says "trust-state rows."
- The denominator objection is met by a principled reframing rather than by
  adding 91/12,129. §3: "The binding quantity is the numerator, and it is
  invariant ... the accessed count is *still exactly 91* ... so the rate is
  stable across every denominator we can form (0.0232% ... 0.0222% ... 0.0210%
  on the later snapshot's 433,155 trust-state rows, 0.0203% against all 447,709
  signals) ... **The ledger's 12,129 signals (§2) are a distinct population and
  are not the base for this rate.**"

The "accessed" event is defined on trust-state rows (`access_count > 0`), so the
numerator is a trust-state-row count that cannot be divided by the 12,129 ledger
signals; the paper now says so explicitly and reports four denominators spanning
0.0203–0.0232% (all 10⁻⁴), including the largest. The misleading "robust to the
choice of denominator" sentence (two denominators 3.6% apart) is gone.

### F3 (major) — "ever accessed" is right-censored; no exposure adjustment
**STATUS: PARTIALLY-RESOLVED.** The bias is now disclosed in §8:
> "The Stage-0 rate is also right-censored: signals captured near the snapshot
> had less exposure time to be accessed than older ones, which biases the pooled
> ever-accessed rate downward; we report it as a pooled base rate and do not
> correct for exposure here."

And the F3 tail-risk ("censoring-deflated baseline eases the ≥10× P1 bar") is
dissolved because P1 no longer uses 0.0222% as its comparator (F1).
**What still fails:** the proposed exposure-matched robustness cut (rate
restricted to signals ≥30/≥60 days old, or a K–M access curve) was not added, so
the magnitude of the downward bias is still unquantified. Note the paper leaves
unused mitigating evidence on the table: its own numerator-invariance finding
(91 accessed unchanged as the store grew 409,404→433,155 over ~5 extra days)
shows newly-aged rows did not convert to accessed — a weak empirical argument
that the censoring bias is small, never connected to §8.

### F4 (major) — pattern "true zero" not held to the Stage-2 measurement standard; abstract/body inconsistent
**STATUS: RESOLVED.** "true zero" is removed and demoted to a floor, consistently
across abstract, body, and Figure 2b. §4:
> "We report this as a floor rather than a confirmed zero: the reuse-detection
> channel is the same class of model-trace instrument shown to fail silently at
> Stage 2 (§5), and the C9 readiness gate ... is not yet met ... whether they
> are ever returned into subsequent work cannot be settled until an
> engine-written selection edge, independent of model output, is in place."

Abstract now reads "show no detected downstream reuse"; Fig 2b caption "none
show *detected* downstream reuse — a floor." Terminology is aligned. (But see
Regression R1: "true zero" reappears for a *different* quantity.)

### F5 (major) — "underpowered" asserted, never quantified
**STATUS: RESOLVED.** §3 Stage 3 now quantifies:
> "a difference of ~2 pp. At n=24/21 the minimum detectable effect at 80% power
> is on the order of ±35 pp, so the arms are uninformative about lift; per our
> preregistered gate this validates the instrument rather than measuring the
> effect."

The MDE (≈±35 pp) — the load-bearing quantification — is present and "arms are
uninformative about lift" carries the interval's content. The explicit 95% CI on
the difference ([−27,+31] pp) from the proposed fix is not stated, but the MDE
substantiates "underpowered," which was the finding.

### F6 (minor) — decay "0 boosted" tautological given the never-accessed stratum
**STATUS: RESOLVED.** "0 boosted / nothing ever drifts upward" is removed from
both body and caption. §4: "By construction this stratum is unreinforced — so
the informative quantity is the magnitude and monotonicity of decay, not the
absence of upward drift, which the filter guarantees." Fig 2a caption matches.

### F7 (minor) — "three independent findings" are views of one mechanism
**STATUS: RESOLVED.** §4: "Three corpus findings — **not statistically
independent, since non-return is their common cause**, but distinct measurements
— point the same way." "Independent" is negated and its cause named.

### F8 (minor) — Wilson lower-bound guard under-specified
**STATUS: RESOLVED.** §6 now states one-sidedness, the bounded quantity, and the
threshold: "the post arm's **one-sided 95% Wilson lower bound** clearing that
threshold [2.08%]" and, for the organic leg, "(Wilson lower bound >0)." The
composite ambiguity is removed because the two-proportion test is dropped
(Amendment 1: "The two-proportion test is replaced by the Wilson-lower-bound
decision"). The decision rule is now a stated conjunction: post per-run LB >
2.08% AND organic per-run LB > 0.

### F9 (minor; escalate) — "~16% of runs" unsourced, non-reconciling
**STATUS: RESOLVED (in the paper).** The figure is removed; §3 Stage 1 now reads
"Injection is almost entirely experiment-driven, not organic return."
**What still fails (out of paper scope):** the frozen sources still carry it —
c25 line 42 ("only ~16% of runs receive any injection") and the application doc
line 37. Flagged per the numeric-mismatch rule; the escalation (B4) already
records this as author cleanup of the frozen docs.

### F10 (minor) — 217,629 vs 409,404 trust-state totals unreconciled
**STATUS: RESOLVED.** §4 reconciles them as different snapshots: "the C3/C3a
decay analysis is computed on an earlier corpus snapshot, 2026-06-10, with
217,629 trust-state rows, and is not pooled with the 2026-06-29 funnel
snapshot." (n=1,964 remains to confirm at final proof per escalation B6; not a
stats-lens blocker.)

### F11 (minor) — Stage-2 floor omits the conditional (channel-working) rate and the upper companion
**STATUS: NOT-RESOLVED.** §3 Stage 2 still presents only the one-sided floor:
> "this 25% is a **floor, not a measurement**: the median missing-footer rate is
> 1.00 — for at least half the injected arm the use-recording channel is
> entirely silent (§5)."

**What still fails:** the informative conditional use-when-offered (6 of the 8
runs with a positioned footer = 75%, with its selection caveat) and the honest
bracket [25%, 92%] are absent from the paper, and the 8/24 "footer present"
figure is no longer stated anywhere, so a reader cannot reconstruct them. The
finding was minor and the omission is non-contradictory, but it is unaddressed —
neither the paper nor the resolution ledger touches F11.

### F12 (minor) — "backlog grows / accumulate faster than retired" asserted from a stock, not a flow
**STATUS: RESOLVED.** The flow claim is dropped and explicitly downgraded to a
stock statement. §4: "The stock of open contradictions dominates resolutions —
the corpus holds the tension rather than retiring it. **(We report a stock, not
a detection-vs-resolution flow over time.)**"

### F13 (minor; assessment) — multiple-comparison exposure
**STATUS: PARTIALLY-RESOLVED.** The substantive recommendation (FWER controlled
by a single frozen primary) is met structurally: §6 labels P1 primary, P2
"(mechanism, frozen)", P3 "(locus, frozen)". **What still fails:** the one
recommended explicit sentence — that the §4 corroborating findings are
descriptive, not hypothesis tests, so no multiplicity correction is applied — was
not added. Lowest-stakes item; F13 asserted no defect requiring a fix.

### F14 (nit; escalate) — 1,847 patterns vs 1,846 crystallize operations off-by-one
**STATUS: RESOLVED (in the paper).** The "(1,846 crystallize operations)"
parenthetical is removed; §4 states only "1,847 reusable patterns," so no
off-by-one is presented. The escalation (B5) explains the +1 as structural (a
seed/non-crystallize pattern; kind=pattern exceeds op=crystallize by one on the
current snapshot too). Frozen-count confirmation is an author item, not a
paper-internal inconsistency.

### F15 (nit) — one hash-chain break unexplained under a tamper-evidence claim
**STATUS: RESOLVED.** §2 now completes the accounting and drops the mismatched
"98.97%": "109 are breaks and 108 of those coincide exactly with a
workspace-context switch ... with **1 residual break** — none are content-hash
failures, so they are session boundaries, not tampering." The residual break is
explicitly categorized (not a content-hash failure), which is the integrity point
that matters, and the B3 arithmetic mismatch is dissolved by removing the
derived percentage.

### F16 (nit) — "for half the injected arm ... silent" understates the ~two-thirds fraction
**STATUS: RESOLVED.** §3 changes "for half" to "**for at least half** the
injected arm the use-recording channel is entirely silent." This is now a correct
lower bound entailed by median missing-footer-rate = 1.00, so the statement is no
longer an understatement presented as the actual fraction. The exact ~two-thirds
(16/24) is not stated, but the paper deliberately no longer exposes the 8/24
"footer present" count, so "at least half" is the correct available claim.

---

## Regressions — new defects, inconsistencies, or numbers introduced by the edits

**R1 (moderate — new internal inconsistency, touches the primary endpoint).**
The F4 fix purges "true zero" for pattern non-reuse *because* the reuse channel
is a "model-trace instrument shown to fail silently at Stage 2." But the F1
amendment reintroduces the phrase for a different quantity: §6 calls the organic
per-run baseline **0/244 a "true-zero baseline"** and Amendment 1 says "the
*organic* baseline is a true zero (0/244)." The organic per-run rate is
"offered *and* used (`use_rate > 0` with a positioned footer)" — its *used* leg
rides the very footer channel the paper elsewhere treats as floor-only. The
inconsistency is defensible on the merits (pre-intervention organic offer ≈ 10⁻⁴,
so 0/244 is offer-limited, not footer-silence-limited, and the footer floor
cannot bite when nothing was offered) — but the paper never states that
reconciliation, so two structurally similar zeros get opposite labels ("floor"
vs "true zero") within one paper that makes measurement-instrument skepticism its
signature. One sentence in §6 explaining why the organic zero is offer-limited
(hence "true") while the pattern zero is a floor would close it.

**R2 (minor — reproducibility wrinkle from the numerator-invariance reframing).**
The headline 0.0222% uses the frozen-read denominator 409,404 (tied to the
2026-06-29 outcomes snapshot), but the *pinned, released* `cir.db` snapshot
offered for verification (sha256 `0b320d9d…`, 2,271,764,480 bytes) has 433,155
trust-state rows and yields 0.0210%. A verifier running the published
re-derivation instrument on the published snapshot reproduces the numerator (91)
and the arms (24/21/6) but **not the headline percentage** — they get 0.0210%,
not 0.0222%. The paper is transparent (it lists both and rests the claim on
numerator invariance), so this is disclosed, not hidden; but the headline
number is not the one reproducible from the single artifact released to
reproduce it.

**R3 (minor — pooling-rule scope gap).** The numerator-invariance robustness
leans on a **post-intervention** snapshot (2026-07-04, after the declared
2026-07-02 intervention boundary): "on a pinned ... snapshot taken 2026-07-04
(after this baseline was frozen), the accessed count is *still exactly 91*."
§5's pooling rule, however, only explicitly declares access/confidence metrics
"continuous across the **2026-06-15** boundary" — it does not extend the
continuity statement to the 2026-07-02 intervention boundary that this
robustness read crosses. The intent is consistent (access is engine-written,
model-independent, not a trace-credit metric; Amendment 1 flags the 2026-07-04
read as "a baseline-stability check, **not** ... a post-intervention result"),
but a reader applying §5 literally sees a post-2026-07-02 read used inside a
pre-baseline robustness claim. Naming access-continuity across the intervention
boundary too would remove the ambiguity.

**R4 (flag only — paper vs frozen-source, per numeric-mismatch rule).** The
paper §3 now repudiates the multiplicative framing ("related metrics from two
regimes, not factors of a single product ... not because they multiply"), but
the frozen c25 (line 39) and application doc still describe a "multiplicative
funnel." Paper-internal consistency is fine (the weakest-link/bottleneck framing
is coherent and does not claim the stages multiply); the residual is a
paper-vs-frozen-source mismatch the escalation already earmarked ("reconcile at
the A1 amendment") and Amendment 1 did not touch. Flag for author reconciliation;
no recomputation.

**Positive consistency checks that pass.** The new per-run baseline reconciles
cleanly: 289 experiment-inclusive feature runs = 244 organic + 45 experiment
(24 injected + 21 withheld), and the 6 offered-and-used runs are the same 6/24
injected citers from Stage 2 — so 6/289 = 2.08% and 0/244 = 0.0% are mutually
consistent and consistent with the funnel. 6/289 = 2.076% rounds to 2.08% ✓. The
four Stage-0 rates are monotone in the denominator with the numerator fixed at 91
(0.0232 > 0.0222 > 0.0210 > 0.0203 as 392,947 < 409,404 < 433,155 < 447,709) ✓.
The dropped "2.6%" is simply absent (no surviving reference contradicts it) ✓.
The amended P1 is statistically coherent: both arms per-run, one-sided 95% Wilson
LB on the post proportion against a fixed 2.08% reference plus an organic LB>0
test, two-proportion test correctly removed ✓.

---

## Verdict

The blocker (F1) and both majors that had concrete fixes (F2, F4, F5) are
resolved; the amended P1 is statistically coherent with a single per-run unit on
both arms. Remaining stats-lens gaps are all minor: F3 discloses the censoring
bias but does not quantify it (PARTIAL), F11 still omits the conditional
use-when-offered rate (NOT-RESOLVED), and F13's optional descriptive-vs-inferential
sentence is absent (PARTIAL). The most consequential *new* item is R1 — the
reintroduced "true zero" for the organic 0/244 baseline sits in tension with the
paper's own demotion of pattern non-reuse to a floor, and closing it needs one
clarifying sentence, not a re-analysis. No new number contradicts another; the
new per-run baseline reconciles exactly with the frozen arms.
