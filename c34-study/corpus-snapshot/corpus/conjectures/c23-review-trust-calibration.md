---
id: c23
name: review-trust-calibration
status: operationalized
lineage:
  - /Users/rashid/.mentu/skill-library/.claude/skills/sequence-review/SKILL.md
verdict: null
---

# C23 - Review trust calibration

## Claim

Citation-gated, fresh-context reviews of completed Mentu sequence runs should produce
trust forecasts that are calibrated against later recipe reliability better than
mechanical run-success baselines alone.

The claim is not that a reviewer can assign "true trust" by inspection. The claim is
that review commitments, when grounded in mechanical evidence and later outcome-linked,
can become a predictive measurement layer for release and recipe-governance decisions.

## Origin

The `sequence-review` skill proposes a workflow:

`run -> reviewer sees mechanical evidence -> observation JSON -> schema gate -> ledger -> aggregate trust`

It has the right epistemic posture: fresh reviewer context, explicit run targeting,
closed review schema, required citations, and aggregation over many runs. C23 keeps
only the measurable residue. Review ratings are treated as forecasts, not verdicts
about reality until calibrated against future outcomes.

## Operationalization

**Datasets**:

- Sequence terminal records:
  - `run_id`, recipe, workspace, started/completed timestamps, status, total steps,
    passed/warned steps, duration, cost, run class, and mechanical trust proxy.
  - Current partial surfaces: `~/.mentu/sequence-history.jsonl`,
    workspace `.mentu/state/step-status/*.json`, and
    `~/.mentu/training/cir-run-outcomes.jsonl`.
- Review commitments:
  - CIR `signals.kind = review_commit`;
  - body JSON with `run_id`, recipe, reviewer id, verdict, rating, rubric scores,
    error tags, citations, narrative, and submitted timestamp;
  - future fields: `reviewer_run_id`, `target_history_hash`, `evidence_digest`,
    `fresh_context=true`, `target_resolution=explicit_run_id`.
- Follow-up outcomes:
  - later same-recipe sequence outcomes;
  - release, changelog, rework, revert, regression, or blocked-release decisions;
  - recurrence of review error tags in later runs;
  - human override or disagreement events.

**Predeclared predictor**:

Review-contract completeness at review time:

- `0`: no review commitment.
- `1`: review exists with verdict/rating but no citations.
- `2`: rating plus citations, but no closed error-tag/rubric schema.
- `3`: full schema with citations to verifiable artifacts.
- `4`: full schema plus mechanical evidence digest and explicit target-run hash.
- `5`: all above plus reviewer run id, fresh-context marker, and later outcome
  linkage metadata.

**Trust forecast**:

- Primary predictor: reviewer `rating` in `[0, 1]`.
- Secondary predictors: rubric vector, verdict, error tags, citation count/type,
  reviewer identity, and review-contract completeness.
- Baselines:
  - target run step success ratio;
  - prior same-recipe success rate;
  - run class and recipe family;
  - CIR usage verdict / run health label.

**Outcomes**:

- next same-recipe run succeeds or fails;
- next three same-recipe runs' success rate;
- later rework/reject/revert/regression event;
- release accepted/blocked;
- recurrence of error tags;
- downstream human override of review verdict.

**Controls**:

- recipe, workspace, run class, step count, duration, cost;
- prior recipe success rate and prior failure count;
- reviewer identity and review lag;
- C14 measurement contract validity;
- C16 conditional activation selectivity;
- C20 participation contract completeness;
- C22 operational surface debt.

## Predictions

- **P1**: Citation-gated review ratings will have lower Brier score for next same-recipe
  run success than mechanical step-success ratio alone.
- **P2**: Low ratings and `rework`/`reject` verdicts will predict higher failure,
  regression, or rework rates in the next three same-recipe runs.
- **P3**: Reviews with full schema, artifact citations, and explicit target hashes will
  be better calibrated than review rows with only narrative and rating.
- **P4**: Error tags will predict recurring failure modes better than undifferentiated
  average rating.
- **P5**: The reviewer signal will add value only if it remains predictive after prior
  recipe success rate, run class, and mechanical step success are controlled.

## Falsification criteria

- Review ratings do not improve calibration or discrimination over mechanical baselines
  after controls -> **refuted**.
- The signal disappears after controlling for recipe identity or prior recipe success
  -> **revised** as recipe-history summarization, not review trust.
- Citation-gated reviews are grounded but not predictive -> **revised** as audit
  provenance, not trust calibration.
- Any verdict that uses reviewer ratings without later outcome linkage is invalid.

## Gate

C23 may produce a verdict only when all are true:

- review-contract scoring rules are frozen before outcome modeling;
- at least 200 `review_commit` rows exist;
- at least 150 reviewed target runs link to terminal run records;
- at least 100 reviewed target runs have a later same-recipe outcome window;
- at least 50 negative or non-ship outcomes exist across reviewed runs;
- citations are machine-parseable and point at step-status, ledger, or CIR artifacts;
- explicit target-run ids are enforced and no latest-run fallback rows are admitted;
- reviewed and unreviewed matched control cohorts exist by recipe/run class;
- outcome windows cover at least 4 weeks.

Current Mentu has run-outcome and trust-state substrates, but the review-commit stream
and canonical sequence-history writer are not yet verdict-grade. C23 is therefore
readiness-gated.

## Known limitations

- Reviews are likely applied to more important or troubled runs, so naive averages are
  biased.
- A high rating may cause different downstream behavior, making prediction and
  intervention hard to separate.
- Reviewer identity and model version can drift.
- Citation count can be gamed. Citation validity and type matter more than volume.
