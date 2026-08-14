# Return funnel decomposition + footer-channel root cause

*2026-07-01. Read-only baseline measurement + engine source trace. Non-verdict,
provenance-stamped. Positioning/diagnostic doc — not a corpus verdict; no gate
opened, nothing in `results/`, `supported/`, or `refuted/` is touched.*

## 1. Why this doc exists

The corpus's strongest empirical signal is a **negative** one: knowledge is
captured at enormous volume but almost never returned/reused. "Return ≈ 0" is not
one failure — it is the product of a **multiplicative funnel**, and each stage has
a different cause and a different fix. This doc freezes the baseline funnel from
live data and traces the one stage that is currently *unmeasurable* to its root
cause in the engine source.

## 2. The return funnel (baseline, read-only)

Provenance: `cir-run-outcomes.jsonl` sha256 `5c3085ef3ab512d8…`, 971 rows,
source mtime `2026-06-29T15:33:35Z`; `cir.db` read-only; semantics =
`observatory/collect.py` verbatim (post-footer-fix boundary `2026-06-15T02:57:24Z`,
`EXCLUDED_RUN_CLASSES = {fixture, smoke, infra}`, arms keyed on
`randomization_arm`, `cited` = `use_rate > 0`).

| Stage | Quantity | Value |
|---|---|---|
| **0 — Organic offer** | trust_state ever accessed | **91 / 409,404 = 0.0222%** |
|  | context_used events (all time) | 24 |
| **1 — Offer (post-fix feature arms)** | injected arm / withheld arm | 24 / 21 |
| **2 — Use-when-offered** | citing runs (`use_rate>0`) | **6 / 24 = 25%** |
|  | useful verdicts | 4 / 24 |
|  | **footer present (mfr<1.0)** | **8 / 24** |
|  | missing_footer_rate mean / median | **0.70 / 1.00** |
| **3 — Task-lift proxy** | injected success | 13 / 24 = 54% |
|  | withheld success | 11 / 21 = 52% |

**Reading the funnel.** Stage 0 is the dominant loss: the system essentially
never surfaces prior knowledge on its own — only ~16% of runs receive any
injection, and almost all of that is the experiment/infra injecting, not organic
return. Stage 2's headline "25% use-when-offered" is a **floor, not a
measurement**: the median `missing_footer_rate` is **1.00**, meaning for half the
injected runs the use-recording channel is *completely silent*. Stage 3 shows no
task-lift separation, but at n=24/21 it is underpowered and (per the C1b frozen
conjecture) validates the instrument, not P1.

## 3. Footer channel — root cause (engine source trace)

**Question:** why is `missing_footer_rate` median 1.00 even *after* the
2026-06-15 footer fix?

**Trace (all in `mentu-engine/Sources/MentuEngine/CIRContextBrief.swift`):**

- `parseUsage(from:injectedSignalIds:completionKeyword:)` (line 352) is the sole
  entry point. All three production callers pass a `completionKeyword`
  (`SequenceRunner.swift:5203`, `LoopRunner.swift:1974`,
  `CIRRecordUsageCommand.swift:78`); the main run path defaults it to
  `LOOP_COMPLETE` (`SequenceRunner.swift:3600`). So the keyword branch is always taken.
- With a keyword set, `parseUsage` calls `completionAdjacentUsageLine` (line 387),
  which accepts a footer **only if it is the single line immediately before the
  completion keyword** (`candidate = lines[index(before: completionIndex)]`,
  line 401). If that exact position does not hold, `parseUsage` returns
  `missing_footer` at lines 366–371 **and never falls through** to the
  whole-output scan the no-keyword path uses (lines 374–384).
- This is **intentional and tested.** The committed test `misplaced`
  (`Tests/MentuEngineTests/CIRContextBriefTests.swift:1553`) feeds
  `"CIR_USED: cir_a\nwork happened after the declaration\nLOOP_COMPLETE"` and
  **asserts `status == "missing_footer"`**. The `usageContract` instruction
  (line 425) tells the model the footer "must" be "the line immediately before
  your completion keyword." The strictness is an **anti-gaming guard**: it stops a
  model from scattering stray `CIR_USED:` lines mid-output to farm reuse credit.

**Conclusion: this is a measurement-contract gap, not a parser bug.**
`missing_footer` conflates two distinct events that the instrument cannot
currently separate:
- **(a) absent** — the model emitted no `CIR_USED:` line anywhere; vs.
- **(b) misplaced** — the model emitted one, but not in the contracted position.

We cannot compute a true use-when-offered rate because we cannot tell (a) from (b).
Loosening the parser to accept any-position footers would *fix the rate* but
**break the anti-gaming guard and the committed `misplaced` test** — so that is
the wrong fix.

## 4. The minimal recording change (proposed, Phase 2)

Add a **diagnostic sub-signal that decomposes `missing_footer` into `absent` vs
`misplaced`, without changing credit or adjudication.** Concretely: when the
strict completion-adjacent line is absent, additionally scan the whole output for
any `CIR_USED:` line and record a diagnostic flag (e.g.
`footer_present_unpositioned`) on the usage record. The `UsageProof.status` stays
`missing_footer`, so `adjudicateUsage` (which keys credit on `status == "used"`)
is untouched, the anti-gaming guard holds, and the `misplaced` test still passes.

This is additive and testable, and it is exactly what makes use-when-offered
*measurable*: with the decomposition, "the model ignored offered context" (absent)
becomes distinguishable from "the model used it but mis-formatted the proof"
(misplaced) — the mechanistic split the whole memory-benchmark literature cannot
make because it forces gold memory into context.

**Not being changed (would need explicit maintainer sign-off):** the credit
contract itself (whether a misplaced footer *should* earn use credit). That is a
policy question about the instrument's gaming-resistance, left to the maintainer.

## 5. What this licenses downstream

- The **base-rate paper** can report Stage 0 and the decay/pattern-reuse findings
  today — they are gate-open and do not depend on the footer channel.
- The **return-intervention preregistration** names the footer diagnostic fix as
  a declared regime boundary (like the 2026-06-15 footer fix), so pre- and
  post-diagnostic use rates are never pooled across the discontinuity.

## 6. Regime boundary

*Declared 2026-07-01T21:19Z. This section is the formal boundary marker the
preregistration (§5) forward-referenced; it is a provenance note, not a verdict.*

The diagnostic decomposition proposed in §4 has been implemented and committed to
the engine.

- **Engine commit:** `dbef5dfd52166b7ddedb44d2f0cf47ac0e1002e4` (mentu-complete,
  branch `main`, authored `2026-07-01T21:18:39Z`),
  `fix: decompose missing_footer into absent vs misplaced (diagnostic)`.
- **What changed:** `CIRContextBrief.parseUsage`, on the completion-keyword path,
  now additionally scans the whole output for any `CIR_USED:` line when the strict
  completion-adjacent footer is absent, and records the result on a new
  diagnostic flag. The per-usage record in `cir-context-usage.jsonl` now emits
  an additive, Optional, backward-compatible field **`footer_present_unpositioned`**
  (`nil` on pre-diagnostic records; `true` = a footer exists but is misplaced;
  `false` = genuinely absent). `UsageProof.status` stays `missing_footer` in both
  cases, so credit, `adjudicateUsage`, and the anti-gaming guard (the committed
  `misplaced` test) are all unchanged.
- **The boundary (hard rule).** `2026-07-01T21:18:39Z` (the engine commit) is a
  declared regime boundary for the footer/use-recording channel, exactly like the
  `2026-06-15T02:57:24Z` footer fix. **Use-when-offered rates MUST NOT be pooled
  across this boundary.** Pre-diagnostic runs record only `missing_footer`, which
  conflates *absent* (model ignored offered context) and *misplaced* (model used
  it but mis-formatted the proof); those two events are separable only from
  `footer_present_unpositioned`, which does not exist before this commit. Any
  use-when-offered estimate that spans the boundary silently mixes an unmeasurable
  denominator with a measurable one and is invalid.
- **Scope.** Diagnostic only. Credit/adjudication semantics are unchanged, so
  `used`-keyed metrics (task-lift, adjudicated-use) are continuous across the
  boundary and may be pooled; only the *decomposition* of `missing_footer` is new.
