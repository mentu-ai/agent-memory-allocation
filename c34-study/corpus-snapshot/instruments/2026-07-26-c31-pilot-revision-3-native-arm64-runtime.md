# Instrument note — C31 pilot revision 3 uses a native arm64 Claude runtime

**Date:** 2026-07-26

**Failure observed:** 2026-07-26, during the first formal credential-free
preparation attempt under pilot revision 2

**Predecessor adapter commit:**
`19ad6ec854030ed3f8077b6acd892570f2533149`

**Predecessor instrument bundle:**
`0ccbdfb509173f3ad15238458f71d43250bbce032cd406a34d33e32b70f4e4f1`

**Disposition:** host-architecture instrument failure; no pilot cell started

## What failed

Revision 2 correctly identified and attested the native Claude Code package,
but selected its linux-x64 executable to match AGENTBench's frozen amd64 task
images. On this arm64 Docker host, the x86-64 Bun executable can be routed
through an emulator that does not expose AVX. The formal pre-setup version
probe exited with status 139 before repository setup.

The failure occurred before credential-file access, OAuth preflight, model
execution, patch production, or evaluation. No pilot run directory,
prepared-task image, or runtime manifest was created. The failed container was
removed. Cached builder and derived-image layers contain public bytes only.

## Registered repair

This note registers **C31 pilot instrument revision 3** before another formal
preparation attempt. The final task image and all repository tools remain the
frozen linux/amd64 AGENTBench substrate. Only the Claude Code executable is
selected from the same-version linux-arm64 package so it runs natively on the
arm64 host.

The repair:

- pins the arm64 Node builder image, Claude native-package integrity, and
  native executable hash;
- retains the pinned amd64 Node runtime for repository tasks;
- copies the arm64 Claude package plus its exact loader/shared-library closure
  from the pinned arm64 builder into the otherwise amd64 task image;
- labels and attests the mixed-architecture boundary explicitly;
- attests both the amd64 task-tool closure and arm64 Claude closure before and
  after public setup;
- binds credential-bearing TLS to the frozen base CA bundle and an
  attested-empty root-owned certificate directory, preventing public setup
  from adding a second trust source; and
- adds regression tests for builder, architecture, package, executable, and
  loader and trust-store drift.

An instrument-development smoke test ran the repaired Claude Code 2.1.220
version probe successfully 20 consecutive times—ten direct container execs and
ten launches from the task shell—and confirmed that an unauthenticated status
probe returned `loggedIn: false`. This smoke test used no credential, task
setup, model request, or pilot artifact.

This is a new content-derived instrument bundle and pilot revision, not a
retry. Formal preparation and all 16 pilot cells must use the revision-3 commit
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
