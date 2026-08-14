# Instrument note — C31 pilot revision 5 rebuilds a shallow base repository

**Date:** 2026-07-26

**Failure observed:** 2026-07-26, during the first formal credential-free
preparation attempt under pilot revision 4

**Predecessor adapter commit:**
`50ee8dce4574f8a7ccdc2cd6b925c549b208d213`

**Predecessor instrument bundle:**
`639f261266f1c6a7ae7485ac3f502804744a75a8fb383c76870c2f1a7b1c66e9`

**Disposition:** public-setup instrument failure; no pilot cell started

## What failed

The first reserved task (`pdm-project_pdm-3281`) completed its frozen public
dataset setup and was sealed as revision-4 prepared image
`sha256:b428fef57648273632975b818c63f1b6078cbf8f1a20f738fe94795e6b2f33f1`
under build key
`c97d756f378975f2c87a37c4cefc4655af3c94bd07da37241b12f334bc7b7a5c`.
During the next reserved task (`openai_openai-agents-python-1843`), revision
4's foreground Git repack failed with:

```text
fatal: unable to read 5ec33aa586724ebea569a66c88a4fb89f60ca2d7
fatal: failed to run repack
```

The adapter stopped and removed the setup container. Because preparation did
not complete all four tasks, it wrote no runtime manifest. It created no
pilot-run directory, credential preflight, model request, patch, or evaluation
artifact.

A credential-free reproduction on a fresh copy of the same immutable OpenAI
task image, checked out at the exact frozen base but without dataset setup,
again failed during full repacking, this time on object
`7f72ff41c4e40532e7b8bf77b78a61668a89372c`. The published repository can
check out the frozen base commit and tree, but its larger object store is not a
reliable input to an in-place full repack. The varying unreadable object also
rules out the revision-4 staged-index mechanism as a sufficient explanation.

The PDM image contains public setup bytes only. Its build key is bound to the
revision-4 adapter source and therefore cannot satisfy revision 5's prepared
image identity. After its provenance and sealed setup commit were inspected,
the stale tag and image were removed before this revision was committed.

## Registered repair

This note registers **C31 pilot instrument revision 5** before another formal
preparation attempt. Instead of pruning the published repository's full object
store in place, the repair reconstructs its Git metadata from the exact frozen
base:

- reset the source index to the detached base while preserving public setup
  worktree content;
- hash the complete non-Git worktree before and after metadata replacement;
- initialize a new same-filesystem repository and fetch the exact detached
  base over local `file://` transport with `--no-tags --depth=1`;
- retain only filesystem-relevant safe `core.*` settings and require the
  original 40-hex base commit, its shallow boundary, and its checked-out index
  to agree exactly;
- expire reflogs, delete any fetched refs transactionally, prune the new
  self-contained object store, and require no remote, ref, reflog, unreachable
  object, or traversable pre-base commit to remain;
- replace the old `.git` directory, remove both the old metadata and temporary
  rebuild worktree, and re-run every invariant against the installed metadata;
  and
- retain bounded public diagnostics and integration tests proving that future
  commits, tags, remote refs, reflogs, and staged-only blobs become unreadable
  while setup worktree bytes remain unchanged.

A credential-free live probe on the immutable OpenAI task image passed these
checks: `HEAD` and `.git/shallow` both named
`f3cac173055e180752167d0327a241240a2248a2`; `git rev-list HEAD` exposed only
that commit; the published image's later head was unreadable; and no ref,
remote, reflog, unreachable object, or temporary rebuild directory remained.
The probe used no dataset setup, credential, model request, or pilot artifact.

An ancestry-preserving local fetch of the same base was also tested before this
revision was committed in immutable image
`tgloaguen/planbenchx86_openai_openai-agents-python@sha256:83654915eb83be4cbb367aa34a5ce8060dcc96acf573a512b14dfae7ce45d141`.
It failed because the published partial clone could not supply promisor object
`edd0d898b48dcf1f9209b13a3eca341b0dcf4889`; `git upload-pack` aborted with
status 128. The disposable probe left no image or file artifact and used no
dataset setup, credential, or model request.

The depth-1 rebuild intentionally removes model-visible history before the
frozen base. The exact base commit and complete post-setup worktree remain
unchanged, and one prepared image is shared across both models and both
allocation arms for each task. The truncation is therefore symmetric and does
not alter the registered placement contrast, but it is a revision-5
task-environment boundary and limits external comparison with stock AGENTBench
repository execution.

This is a new content-derived instrument bundle and pilot revision, not a
retry. Formal preparation and all 16 pilot cells must use the revision-5 commit
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
