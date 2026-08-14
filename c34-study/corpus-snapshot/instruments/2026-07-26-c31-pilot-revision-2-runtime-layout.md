# Instrument note — C31 pilot revision 2 repairs Claude Code runtime attestation

**Date:** 2026-07-26

**Failure observed:** 2026-07-26, during credential-free public runtime
preparation

**Predecessor adapter commit:**
`33dcc4fa72c716964adc1247b7645784bf7fc544`

**Predecessor instrument bundle:**
`66e4aa483015d10fc4182b8a789956a9a4a5cf2ce4c9e5585470655bfe29c162`

**Disposition:** mechanical instrument failure; no pilot cell started

## What failed

The first prepared-image build stopped at its pre-setup runtime attestation.
The sealed adapter expected
`/usr/local/lib/node_modules/@anthropic-ai/claude-code/cli.js`, but the pinned
Claude Code 2.1.220 npm distribution has no such file. Its declared launcher is
`bin/claude.exe`, backed by the pinned
`@anthropic-ai/claude-code-linux-x64` optional package.

The failure occurred before repository setup, credential-file access, OAuth
preflight, model execution, patch production, or evaluation. No pilot run
directory, prepared-task image, or runtime manifest was created. The failed
container was removed. The cached public derived image and pinned builder image
contain no credential.

## Registered repair

This note registers **C31 pilot instrument revision 2** before another
preparation attempt. The repair:

- replaces the obsolete JavaScript entry-point expectation with the exact
  native-package layout declared by Claude Code 2.1.220;
- pins and verifies the linux-x64 optional-package integrity and native binary
  hash;
- materializes one deterministic root-owned launcher symlink instead of a
  duplicate executable copy;
- attests the launcher target, both native executable locations, both package
  manifests, and the loader/shared-library closure used by the executable;
- requires executable byte identity in capture and independent pilot
  validation; and
- adds regression tests for launcher or executable drift.

This is a new instrument bundle and therefore a new pilot revision, not a
same-bundle retry. Preparation and all 16 pilot cells must use the revision-2
commit and content-derived bundle.

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
