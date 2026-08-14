# Instrument note — C31 pilot revision 4 serializes future-history sanitation

**Date:** 2026-07-26

**Failure observed:** 2026-07-26, during the first formal credential-free
preparation attempt under pilot revision 3

**Predecessor adapter commit:**
`16a552ce6800479814b7c579e31187647f80947b`

**Predecessor instrument bundle:**
`3c83b906bb60cbded100ae88ad3afcd628a836d14879e3b72358c7cc09e48be2`

**Disposition:** public-setup instrument failure; no pilot cell started

## What failed

The first reserved task (`pdm-project_pdm-3281`) completed its frozen public
dataset setup and was sealed as revision-3 prepared image
`sha256:ee3894068caa449616b123e38114c279e86c1862a3bace8594b5d51a99eaa74e`
under build key
`20baf45595292fd114cf9f785b02ea45dcecc78adab7bbe38ab991f25e3dcd4b`.
During the next reserved task (`openai_openai-agents-python-1843`), the
future-history sanitation shell exited with status 128. That shell included
remote/ref deletion, reflog expiration, and foreground Git garbage collection;
because the failing adapter did not preserve stderr, the failed substep is not
identified. The adapter stopped immediately and removed that setup container.
Because preparation did not complete all four tasks, it wrote no runtime
manifest. It created no pilot-run directory, credential preflight, model
request, patch, or evaluation artifact.

The PDM image contains public setup bytes only. Its build key is bound to the
revision-3 adapter source and therefore cannot satisfy revision 4's prepared
image identity. After its provenance and sealed setup commit were inspected,
the stale tag and image were removed before this revision was committed.

The failing adapter did not retain Git's captured stderr in its raised
diagnostic. A credential-free reproduction using the same immutable task
image, base commit, and setup commands completed when the sanitation steps
were inspected individually. That evidence is insufficient to name the exact
status-128 cause. An automatic-maintenance or lock race is a plausible
mechanism, not a measured finding.

## Registered repair

This note registers **C31 pilot instrument revision 4** before another formal
preparation attempt. The repair changes future-history sanitation mechanics
only:

- disable Git automatic garbage collection, automatic maintenance, and
  detached background collection before any ref mutation;
- reset the index to the detached base while preserving public setup changes
  in the working tree, so staged future-only objects cannot remain reachability
  roots;
- remove configured remotes, then delete every remaining ref through one
  `git update-ref --stdin` transaction rather than one process per branch or
  tag;
- expire all reflogs and run one foreground `git gc --prune=now`;
- require the original detached base `HEAD` and clean base index to remain
  unchanged and require remotes, refs, reflogs, and unreachable objects all to
  be empty; and
- preserve a bounded public stderr/stdout diagnostic if sanitation fails.

The repair neither changes repository content presented to the model nor
introduces a retry of a pilot cell. It makes the already-registered exclusion
of post-base repository history mechanically serialized and auditable.

This is a new content-derived instrument bundle and pilot revision, not a
retry. Formal preparation and all 16 pilot cells must use the revision-4 commit
and bundle.

## Frozen design remains unchanged

- `estimand_unchanged: true`
- `claim_unchanged: true`
- `predictions_unchanged: true`
- `thresholds_unchanged: true`
- `arms_unchanged: true`
- `task_population_unchanged: true`
- `pilot_tasks_unchanged: true`
- `run_order_unchanged: true`
- `model_ids_unchanged: true`
- `effort_and_fallback_unchanged: true`

Pilot outputs remain non-verdict-bearing and may validate only the registered
instrument mechanics.
