# Organic-offer pathway — design proposal (C25 intervention arm)

*2026-07-01. Engineering design proposal for the C25 return intervention. This
is a **proposal**, not an implementation: it specifies the pathway whose shipping
would satisfy gate-condition (1) of the preregistered C25 conjecture. Nothing
here opens the gate, ships code, or touches a verdict. It exists so the trigger
choice is a concrete decision rather than an open question in the conjecture.*

## 0. Why this doc exists

C25 (`corpus/conjectures/c25-return-intervention.md`) freezes the intervention's
predictions before the intervention exists, and names its second instrument
prerequisite as future work:

> **Organic offer pathway** (NOT yet shipped): the engine surfaces relevant prior
> signals into a new run without an experiment forcing injection — e.g. via the
> C7 handle-return lane and/or a C11 measurement→action closure edge. The exact
> trigger is an engineering decision recorded in a future instrument doc.

This is that doc. It converts "an engineering decision" into three concrete,
comparable options with an acceptance contract, so the maintainer can pick one
and build it — at which point C25 gate-condition (1) is satisfied and the
post-intervention arm begins to accrue.

## 1. What the pathway must do (from C25, non-negotiable)

The frozen conjecture constrains the design. Any implementation MUST:

1. **Surface prior signals organically** — selected by the run's own context, not
   forced by an experiment's randomization arm. This is the whole point: Stage 0
   (organic offer, 0.0222%) is the binding constraint, not Stage 2.
2. **Log offer provenance** — every organically-offered signal is recorded with
   *why* it was surfaced (the query or edge that produced it), so **offer is
   countable independent of use**. Without this, the primary outcome (offered AND
   used) cannot be computed and the intervention is unmeasurable — the exact trap
   the baseline funnel fell into at Stage 2.
3. **Emit the positioned `CIR_USED:` footer contract unchanged** — the footer
   diagnostic (engine `dbef5dfd`, regime boundary `2026-07-01T21:18:39Z`) is
   prerequisite 1 and already landed. The offer pathway must not alter the credit
   contract or the anti-gaming guard; it only changes *what gets offered*, not
   *how use is proven*.
4. **Be a declared regime boundary of its own** — the ship date is recorded here
   and in the C25 frontmatter as `MENTU_C25_INTERVENTION_AT`; pre- and
   post-intervention return rates are never pooled, exactly as the footer boundary
   is treated.

## 2. Three trigger options

The engine already has two mechanisms that could carry organic offer. A third is
a purpose-built selector. They are not mutually exclusive, but the proposal is to
**ship exactly one first** so the intervention has a clean, attributable trigger.

### Option A — C7 handle-return lane (addressability-driven)

Surface prior signals that share a **stable handle** with the current run's
inputs. C7 (handle-mediated returnability) already establishes that signals carry
addressable handles (Crawlio LACS is the reference substrate); the offer step is:
at run start, look up signals whose handle matches an input handle of this run,
and offer the top-k by recency/confidence.

- **Pro**: reuses an existing, audited addressing scheme; offer provenance is
  trivially the matched handle. Narrow, testable, low blast radius.
- **Con**: only fires when the new run shares a handle with a prior one — high
  precision, low recall. May under-fire on runs that would benefit from
  *semantically* related but not *handle*-identical prior work.
- **Measurability**: excellent. Offer = "handle H matched"; the log is the handle.

### Option B — C11 measurement→action closure edge (outcome-driven)

Surface prior signals whose recorded **measurement** is relevant to the current
run's **action**. C11 (measurement-action closure) is currently blocked precisely
on the absence of explicit measurement-to-action edges; building the offer step as
that edge closes C11's gap and creates C25's trigger in one move.

- **Pro**: kills two blocked conjectures' shared dependency; offer is semantically
  motivated (this measurement bears on this action), so higher recall than handles.
- **Con**: requires defining the measurement→action relevance relation, which is a
  larger design surface than handle-matching; more ways to get the relevance wrong.
- **Measurability**: good, but the offer-provenance log must capture the *edge
  type* and the *relevance score*, not just an id, or offer becomes uncountable.

### Option C — purpose-built context selector (retrieval-driven)

A dedicated retrieval step at run start: embed the run's opening context, query
the signal store for nearest neighbours above a similarity floor, offer the top-k.
This is what the memory-systems literature (Mem0, A-MEM, MemGPT) actually builds;
it is the most general and the least grounded in the existing engine.

- **Pro**: highest recall; directly comparable to the field's systems; the
  intervention becomes "we added what everyone else assumes exists."
- **Con**: largest blast radius; introduces an embedding/index dependency the
  engine does not currently have; offer provenance is a similarity score whose
  threshold is a free parameter that must be frozen before accrual to stay honest.
- **Measurability**: good if the threshold and index are frozen at ship time and
  recorded; poor if the threshold is tuned while the post arm accrues.

## 3. Recommendation

**Ship Option A (C7 handle-return lane) first.** Rationale:

- It has the **smallest blast radius** and the **cleanest offer provenance** (a
  matched handle is self-documenting), which matters most for a preregistered
  intervention where offer must be countable independent of use.
- It reuses an **already-audited** addressing scheme rather than introducing a new
  embedding dependency whose free parameters threaten the freeze.
- If Option A ships and the post-intervention return rate rises ≥10× baseline
  (C25 P1), the intervention is supported with a mechanism that is easy to
  explain and hard to game. If it *under-fires* (offer rate barely moves because
  handle-identity is too strict), that is itself an informative result and
  motivates Option B or C as a follow-up intervention — a second frozen conjecture,
  not a mid-study parameter change.

Option B is the natural second intervention (it also retires C11's blocker).
Option C is the "match the literature" arm, best run last and with its similarity
threshold frozen in advance.

## 4. Acceptance contract (what "shipped" means for the gate)

Gate-condition (1) of C25 is satisfied when ALL of the following hold, recorded in
a dated ship doc:

1. The chosen trigger is live in the engine on the main run path (not behind an
   experiment flag), with a test that asserts it fires on a matching run and does
   not fire on a non-matching one.
2. Every organic offer writes a provenance record: `{run_id, offered_signal_id,
   trigger_type, trigger_key_or_score, ts}`. Offer count is derivable from these
   records alone.
3. The positioned-footer credit contract and the `footer_present_unpositioned`
   diagnostic are unchanged (verified by the existing regression tests).
4. `MENTU_C25_INTERVENTION_AT` is set to the ship timestamp; the C25 dormant
   analyzer (`analyses/c25-return-intervention/analyze.py`) reads it and begins
   counting post-intervention runs. The analyzer stays dormant until BOTH the
   marker is set AND ≥150 post-intervention runs accrue — it enforces this itself.

Until every item holds, C25 remains a frozen conjecture with `verdict: null` and
no intervention arm. This doc changes none of that; it only makes the build a
decision the maintainer can take.

## 5. What this doc deliberately does NOT do

- It does not implement any trigger, set `MENTU_C25_INTERVENTION_AT`, or modify
  the engine. Building is the maintainer's call; this is the menu.
- It does not change any frozen C25 prediction, threshold, or the gate. The
  predictions were frozen before this doc existed and stay frozen.
- It does not touch `results/`, `supported/`, or `refuted/`. No verdict is
  implied. The intervention's outcome is unknown and will stay unknown until the
  gate opens on real post-intervention data.
