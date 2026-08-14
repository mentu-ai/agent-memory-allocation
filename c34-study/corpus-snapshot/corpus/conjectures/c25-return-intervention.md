---
id: c25
name: return-intervention
status: conjecture
lineage:
  - corpus/refuted/c1-return-as-intelligence.md
  - corpus/conjectures/c1b-return-as-intelligence-randomized.md
  - applications/2026-07-01-return-funnel-and-footer-root-cause.md
verdict: indeterminate
result: results/2026-08-12-c25-return-intervention.md
preregistered: 2026-07-01T21:30Z
tracking:                      # machine-updated by observatory beats only
  regime_boundary: 2026-07-01T21:18:39Z   # footer-diagnostic engine commit dbef5dfd; use rates never pooled across this boundary
  baseline_frozen:
    organic_offer_accessed_pct: 0.0222     # trust_state accessed 91/409404 (read-only, 2026-06-29 outcomes snapshot)
    offer_arms: { injected: 24, withheld: 21 }
    use_when_offered_citing: 6             # use_rate>0, of 24 injected (a FLOOR: median missing_footer_rate=1.0 pre-diagnostic)
    footer_present: 8                       # of 24 injected
  intervention_arms: { pre: null, post: 949 }    # final at gate-triggered analysis (2026-08-12T22:08:40Z)
  intervention_at: 2026-07-02T18:43:00Z          # regime boundary — engine commit fb85d754 (Option A, C7 handle-return lane); never pool across it
  ship_doc: instruments/2026-07-02-organic-offer-pathway-ship.md
  gate: "OPENED (found 2026-08-12 at 949/150 post-intervention runs; beat dormant since 2026-07-13). Frozen analyzer run 2026-08-12T22:08:40Z; verdict INDETERMINATE ratified same day; see results/2026-08-12-c25-return-intervention.md. Accrual-window co-interventions disclosed there per the pre-registered note."
---

# C25 — Return intervention: does building the offer pathway raise return?

## Claim

The dominant loss in the knowledge-return funnel is **organic offer**, not
use-when-offered. When the system is changed to *surface relevant prior signals
into a new run on its own* (rather than only when an experiment injects them),
the return rate rises materially above the read-only baseline — and, with the
footer diagnostic (regime boundary `2026-07-01T21:18:39Z`) separating *absent*
from *misplaced* footers, use-when-offered becomes cleanly measurable for the
first time.

## Why this exists

The read-only baseline (`applications/2026-07-01-return-funnel-and-footer-root-cause.md`)
decomposes "return ≈ 0" into a multiplicative funnel:

- **Stage 0 — organic offer:** 91 / 409,404 signals (**0.0222%**) ever accessed;
  only ~16% of runs receive any injection, almost all experiment/infra-driven.
- **Stage 1 — offer:** 24 injected / 21 withheld post-fix feature arms.
- **Stage 2 — use-when-offered:** 6/24 cite (`use_rate>0`) — a **floor, not a
  measurement**, because median `missing_footer_rate = 1.00` (the channel is
  silent for half the arms).
- **Stage 3 — task-lift:** 13/24 vs 11/21 success — underpowered, no separation.

C1b tests Stage 2→3 (does *used* knowledge help?) and is instrument-validating at
current n. C25 tests the **upstream** intervention: build Stage 0, and measure
whether return rises. This is the question the read-only measurement made
answerable — and it is the causal claim behind the negative base-rate result.

## Instrument prerequisites (must land before any intervention data counts)

1. **Footer diagnostic** (LANDED, `2026-07-01T21:18:39Z`, engine commit
   `dbef5dfd`): `footer_present_unpositioned` decomposes `missing_footer` into
   absent vs misplaced, so use-when-offered is measurable. This is the regime
   boundary; pre-diagnostic use rates are never pooled with post.
2. **Organic offer pathway** (NOT yet shipped): the engine surfaces relevant
   prior signals into a new run without an experiment forcing injection — e.g.
   via the C7 handle-return lane and/or a C11 measurement→action closure edge.
   The exact trigger is an engineering decision recorded in a future instrument
   doc; until it ships, C25 stays a frozen conjecture with no intervention arm.
3. **Offer provenance**: every organically-offered signal is logged with why it
   was surfaced (the query/edge that produced it), so offer is countable
   independent of use.

## Design

- **Unit**: sequence run. **Arms**: pre-intervention (offer pathway off — the
  frozen read-only baseline) vs post-intervention (offer pathway on). **Primary
  outcome**: return rate = fraction of runs where a prior signal is *offered
  AND used* (`use_rate>0` with a positioned footer). **Secondary**: organic-offer
  rate (Stage 0), use-when-offered conditional on offer (Stage 2, now measurable),
  task success (Stage 3), and the absent-vs-misplaced split.
- **Analysis**: pre-vs-post difference in return rate, two-proportion test with
  the pre arm fixed at the frozen baseline; use-when-offered compared only
  *within* the post-diagnostic regime. Stdlib-only, matching the corpus (Fisher
  exact / two-proportion z from `math`), no scipy.
- Predictions and thresholds are frozen in this file before the offer pathway
  ships and before any post-intervention run is examined.

## Predictions (frozen now, before the offer pathway exists)

- **P1 (primary)**: Post-intervention return rate exceeds the frozen baseline
  organic-offer rate (0.0222%) by at least an order of magnitude — offer is the
  binding constraint, so building it moves return.
- **P2 (mechanism, measurable via the diagnostic)**: Once offer is organic and
  the footer diagnostic is live, use-when-offered (positioned-footer `use_rate>0`
  among offered runs) is **> 0** and separable from absent — i.e. the residual
  loss is *not* "model ignores everything," it is a mix of absent and genuine
  use. If instead post-diagnostic runs are overwhelmingly `footer_present_unpositioned`
  (misplaced, not absent), the loss was a *measurement* artifact, not behavior.
- **P3 (locus)**: Organic offer, when it fires, concentrates on runs whose recipe
  family has prior recorded outcomes to return — offer helps most where there is
  something to return (mirrors C1b P3).

## Falsification criteria

- Post-intervention return rate ≈ baseline (no material rise) across the gate
  sample → **refuted**: building organic offer does not raise return; the loss is
  downstream (model does not use what it is offered), not upstream.
- P2 shows post-diagnostic use is ~0 with footers overwhelmingly *absent* (not
  misplaced) despite organic offer → **refuted in the strong form**: the system
  offers but the model does not use — return is a use problem, not an offer problem.
- Offer pathway ships but organic-offer rate does not rise above baseline → the
  intervention did not take; back to engineering, result void (not a refutation
  of the claim).

## Analysis gate (frozen)

Do **not** compute a C25 verdict until BOTH hold:
1. the organic-offer pathway has shipped (a dated instrument doc records the
   engine commit and the trigger), establishing a post-intervention regime; and
2. ≥150 post-intervention runs have accrued with the offer pathway on and the
   footer diagnostic live (same per-arm discipline as C1b).

Until then C25 is a frozen conjecture: the analyzer (`analyses/c25-return-intervention/`)
stays dormant and prints GATE NOT OPEN. Pre-intervention data is the frozen
baseline above and is never pooled across the `2026-07-01T21:18:39Z` diagnostic
boundary. Per the constitution, this conjecture enters as a question, not a law;
the intervention must survive the strongest test it can be given, not be asserted.

---

## Amendment 1 — P1 unit correction (2026-07-04, pre-gate; verdict still null)

**Status: RATIFIED by author (Rashid Azarang), 2026-07-05.** Pre-gate amendment
(0/150 post-intervention runs; verdict null; no post-intervention data examined).

**Legitimacy.** This amendment is made *before* the analysis gate opens (0/150
post-intervention runs; verdict null; no post-intervention data examined). The
original predictions above are preserved verbatim as the audit trail; this
section supersedes P1's *comparison unit* only.

**Defect found (B2 referee pass, stats-F1 / validity-M2).** As frozen, P1
compares incommensurable quantities: the baseline `organic_offer_accessed_pct
= 0.0222%` is a **per-trust-state-row access** rate (91/409,404), while the
Design's primary outcome and P1 define the post quantity as a **per-run
offered-and-used** rate. Rows vs runs; accessed vs used. A "≥10×" ratio and a
two-proportion test across those units have no coherent null.

**Re-derivation (read-only, pinned snapshot).** `instruments/2026-07-04-return-baseline-rederivation.py`
on a `.backup` snapshot (`PRAGMA integrity_check = ok`; sha256 `0b320d9d…`,
2026-07-04) reproduces the frozen experimental arms **exactly** (injected 24,
withheld 21, offered-and-used 6) and derives the per-run baseline on the same
window (post-footer-fix `2026-06-15T02:57:24Z`, pre-intervention, feature-class):

- **per-run return rate, organic (non-experiment):** 0 / 244 feature runs = **0.0%**
- **per-run return rate, experiment-inclusive:** 6 / 289 feature runs = **2.08%**
  (the 6 offered-and-used runs are all in the forced-injection arm; no organic
  run ever offered-and-used a prior signal).

**P1 (amended, primary, frozen at this amendment).** With the organic-offer
pathway on, the **post-intervention per-run return rate** — fraction of
feature-class runs where a prior signal is offered AND used (`use_rate>0` with a
positioned footer) — exceeds the pre-intervention **experiment-inclusive**
per-run baseline of **2.08%** (6/289), with the post arm's own one-sided 95%
Wilson lower bound clearing 2.08%. The *organic* baseline is zero (0/244), and
this zero is **offer-limited** — no organic run offered a prior signal at all —
not a footer-channel floor like pattern non-reuse (the silent-use channel cannot
bite when nothing was offered); so the pathway must also make the organic per-run
return rate detectably `>0` (Wilson 95% lower bound `>0`). Both arms are now on
the per-run unit; the 0.0222% per-row access rate is retained only as the Stage-0
descriptive statistic, not as the P1 comparator. The two-proportion test is
replaced by the Wilson-lower-bound decision above (the per-row two-proportion
test was invalid across units).

**Framing note (supersedes "multiplicative funnel").** The "Why this exists"
section above and the root-cause application doc describe the funnel as
*multiplicative*. That wording is superseded: Stage 0 is an organic per-row rate
and Stages 1–3 are per-run experimental rates, so the stages do not literally
multiply. The correct reading is a weakest-link bound — organic offer at 10⁻⁴
caps organic return regardless of downstream use — which is what the paper now
states. No number changes; only the composition claim is corrected.

**Unchanged:** P2, P3, the falsification criteria, and the analysis gate (both
conditions) stand as frozen. Numerator invariance note: as of the 2026-07-04
snapshot (post-ship) `accessed` is still exactly 91 and `context_used` still 24
— reported here only as a baseline-stability check, **not** as a
post-intervention result (the gate is closed).
