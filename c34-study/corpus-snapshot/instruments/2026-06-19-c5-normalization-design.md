# Instrument note - C5 boundary-impedance normalization design

**Date**: 2026-06-19.
**Follows**: `corpus/conjectures/c5-boundary-impedance.md` and the 2026-06-19
audit finding that C5 is blocked on normalization design, not on data.
**Method**: read-only schema and shape audit only: `sqlite3 -readonly
~/.mentu/cir.db`, direct reads of `~/.mentu/training/cir-run-outcomes.jsonl`, and
direct ledger samples. No Mentu CLI or MCP paths were used. No C5 result was
computed, no verdict surface was touched, and no frozen prediction or falsification
field was edited.

## Summary

C5 must not compare "signals used" against "all signals in CIR." Most signals were
never plausible candidates for a given consumer, so that denominator would turn
selection bias into a false impedance coefficient.

The normalization rule is:

> A signal is an opportunity only when it was available before the consumer event,
> had a resolved origin workspace, had a resolved consumer workspace, and either
> was actually exposed to the consumer or was in the same time-local semantic
> opportunity set as the consumer's act.

This creates two analysis surfaces, to be reported separately and never pooled:

1. **Primary: exposure-conditional run reuse.** Of the CIR signals actually exposed
   to a run, are native-workspace signals cited at a higher rate than cross-workspace
   signals?
2. **Secondary: availability-matched citation reuse.** Among prior, semantically
   similar signals available to a citing signal, are native-workspace candidates used
   more often than cross-workspace candidates?

The primary surface is cleaner because exposure is recorded directly. The secondary
surface is broader, but must rely on semantic matching and therefore carries more
diagnostic burden.

## Source fields

Use only read-only sources:

- `~/.mentu/training/cir-run-outcomes.jsonl`: `run_id`, `started_at`,
  `completed_at`, `recipe`, `injected_signal_ids`, `used_signal_ids`,
  `missing_footer_rate`, `surfaces`.
- `~/.mentu/cir.db` `signals`: `id`, `ts`, `workspace`, `kind`, `run_id`,
  `asserted_confidence`, `verification`, `source_ids`, `parent_ids`.
- `~/.mentu/cir.db` `relations`: `source_id`, `target_id`, `relation_type`,
  `created_at`.
- `~/.mentu/cir.db` `embeddings`: `signal_id`, `vector`, `dimension`, `model`,
  `embedding_space`.
- `~/.mentu/cir.db` `trust_events`: `signal_id`, `new_confidence`, `ts`.
- Root and nested `ledger.jsonl` may be used for workspace identity audit only, not
  as an outcome source.
- Neon/API cross-device data is a future, separately-labelled stratum. Do not mix it
  into the local workspace analysis unless the extraction path is documented with the
  same read-only discipline and a dated instrument note.

## Workspace identity

Boundary classification is invalid unless both sides resolve.

Canonicalization rules:

1. Trim whitespace; convert absolute workspace paths to their basename.
2. Compare canonical names case-insensitively.
3. Treat `unknown`, `default`, `cir-pending`, and the empty string as unresolved.
   They are excluded from C5 denominators, not counted as cross-boundary.
4. For run consumers, derive the consumer workspace from `cir.db.signals` rows with
   the same `run_id`. If rows include an ephemeral recipe/milestone workspace and one
   stable co-observed workspace, use the stable workspace. If more than one stable
   workspace remains, exclude the run as ambiguous.
5. Emit an exclusion table. If unresolved or ambiguous workspace identity removes
   more than 40% of otherwise eligible opportunities, C5 reports "instrument identity
   insufficient" and no verdict is adjudicated.

Boundary labels:

- `native`: canonical origin workspace equals canonical consumer workspace.
- `cross`: both resolve and differ.
- `unresolved`: either side fails to resolve; excluded from denominator and reported.

## Primary surface - exposure-conditional run reuse

Unit: `(run_id, exposed_signal_id)`.

Eligibility:

1. `started_at >= 2026-06-15T02:57:24Z`, the C1b footer-fix boundary. Before that,
   signal-level `used_signal_ids` is known to be a broken measurement channel.
2. `injected_signal_ids` is non-empty.
3. Consumer workspace resolves through `signals.run_id`.
4. Every exposed signal exists in `signals`, has a resolved origin workspace, and was
   created at or before the run start.
5. Strict primary rows require `missing_footer_rate == 0`. A lower-bound sensitivity
   analysis may include `0 <= missing_footer_rate < 1`, but `missing_footer_rate == 1`
   is never treated as proof of non-use.

Outcome:

- `used = exposed_signal_id in used_signal_ids`.

Estimator:

- Report native and cross use rates over exposed signals.
- The adjudication estimate is within-run: only runs with at least one native and one
  cross exposure contribute to the paired comparison.
- Also report all clean exposed opportunities descriptively, clustered by run, so the
  corpus can see whether the paired subset is representative.

Readiness gate:

- At least 30 strict-clean mixed-boundary runs, or
- at least 100 strict-clean exposed opportunities in each boundary class across at
  least 10 mixed-boundary runs.

If the gate is not met, the output is a readiness report, not a C5 verdict.

## Secondary surface - availability-matched citation reuse

Unit: `(source_signal_id, candidate_signal_id)`.

For each source signal that creates one or more `relations` of type `cites`,
`supports`, `extends`, `refines`, or `corrects`:

1. Resolve the source workspace from `signals.workspace`.
2. Build a candidate pool of prior signals with embeddings, resolved workspaces,
   eligible content kind, and `signal.ts <= source.ts`.
3. Exclude candidates created by the same run as the source signal, candidates whose
   only workspace is unresolved, and candidates newer than the source.
4. Rank candidates by semantic similarity to the source signal, not by global corpus
   frequency.
5. Keep a fixed local neighborhood: the top `K` candidates per embedding space,
   stratified by kind family and age bucket. The initial implementation should test
   `K in {20, 50, 100}` as a sensitivity suite.
6. `used = relation(source_id, candidate_id)` exists.

Estimator:

- Compare native vs cross use within each source signal's matched candidate
  neighborhood.
- Include source fixed effects; a candidate is compared only to other candidates that
  were plausible for the same source act.
- Report sensitivity across `K`, embedding model/space, age buckets, kind whitelist,
  and alias maps.

This surface can support or weaken the primary surface, but it should not overrule a
clean primary result unless the mismatch is explained mechanically.

## Confidence at point of use

P2 must compare confidence at use time, not today's recomputed trust state.

For a used signal:

1. Use the latest `trust_events.new_confidence` for that `signal_id` with
   `trust_events.ts <= use_time`.
2. If no such event exists, fall back to `signals.asserted_confidence`.
3. Do not use current `trust_state.effective_confidence` unless its
   `last_recomputed <= use_time`; otherwise it leaks future evidence into the use.
4. Report missing-confidence rows separately. They do not become zero confidence.

For run reuse, `use_time = completed_at`. For relation reuse, `use_time =
relations.created_at` when present, otherwise the source signal timestamp.

## Fail-closed guardrails

The future `analyze.py` must stop with a readiness or instrument report instead of a
verdict when any of these trip:

- pre-footer-fix run rows are needed to reach the primary gate;
- `missing_footer_rate == 1` rows materially change the run-level direction;
- unresolved/ambiguous workspace identity exceeds 40% of eligible opportunities;
- native or cross class has fewer than 100 strict-clean opportunities;
- the paired/matched subset reverses the all-exposure descriptive direction;
- confidence-at-use cannot be reconstructed for more than 30% of used signals;
- primary and secondary surfaces disagree in sign and no mechanical reason is found.

These are not ways to rescue C5. They are ways to prevent a false verdict from an
instrument whose identity, exposure, or attribution channel is not yet adequate.

## Implementation checklist

The future analysis should be built in this order:

1. Pure guardrail helpers and fixture tests: workspace canonicalization, run workspace
   resolution, footer-boundary eligibility, confidence-at-use reconstruction.
2. Dataset digest only: source counts, exclusion counts, strict-clean primary gate
   progress, secondary candidate-pool progress.
3. Primary exposure-conditional estimator.
4. Secondary availability-matched estimator.
5. Sensitivity suite and null checks.
6. Mechanical adjudication against C5 predictions and falsification criteria only
   after the readiness gates pass.

Until step 6, every output is a design/readiness artifact, not a C5 result.
