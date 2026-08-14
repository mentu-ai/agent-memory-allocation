# OKF projection — a read-only graph + retrieval lens over the corpus

**Date**: 2026-06-13
**Follows**: the engine's `okf project` (mentu-complete `13bfe8b`), applied to this corpus.
**Method**: `mentu okf project /Users/rashid/Desktop/epistemics --out ~/Desktop/epistemics-okf`,
then the pure OKF tools (`validate`, `lint`, `context`, `suggest-links`) over the *derived*
bundle. Read-only throughout: the projector reads the corpus filesystem and writes only
`--out`; it never opens `~/.mentu/cir.db` and `okf ingest` is never run.

## Summary

The corpus carries its entire knowledge graph inside domain frontmatter (`lineage`, `result`,
`parent`) and in no body links, so a generic OKF reader sees a pile of typeless, unlinked
files. `okf project` derives a parallel OKF bundle that exposes that latent graph (lineage →
`extends`, result → a `# Citations` link, verdict/status → `x-mentu.trust.level`) and assigns
a `type` from the directory, **without touching the corpus**. The bundle is a regenerable
view; the corpus stays the source of truth, in its own constitution-governed schema.

## What the lens is

A one-way projection `corpus → OKF bundle`. It lets the corpus be navigated and queried with
the OKF tools (graph health via `lint`, evidence packs via `context`, edge proposals via
`suggest-links`) while the falsificationist source is left exactly as written.

## Purity and non-mutation (why this is safe to run on the corpus)

- **Non-mutation.** `okf project` writes only `--out`. The corpus git tree was clean after
  every run (`git -C epistemics status --porcelain` empty). Verified.
- **Observer-effect.** `~/.mentu/cir.db` was byte-identical (same mtime and size,
  `3309121536`) across `project` + `validate` + `lint` + `context` + `suggest-links`. The
  projector has no CIR write path (source: `OKFProjector.project` is pure). `okf ingest` and
  `okf lint --cir` are **forbidden against the live db** here: they would inject `okf_concept`
  signals and read-access telemetry into the very substrate C1b / C3 measure.
- **Lossless.** The original frontmatter is preserved verbatim beneath the derived OKF fields.
  The `tracking:` inline flow-maps (which the OKF YAML subset cannot model) survive byte-exact,
  because the projector reads them only to extract `id` / `lineage` / `verdict` and re-emits
  the source block unchanged.

## The mapping

`dir → type`, `id → x-mentu.id`, `lineage`/`parent → extends`, `result → # Citations`,
`verdict`/`status → x-mentu.trust.level` (refuted 0.2, revised 0.5, supported 0.9; else the
status map). External lineage (e.g. `epistemic-main/…`, the 2025 ESE corpus, roughly 43% of
references) does not resolve to a bundle path, so it is **not** an edge; it is preserved in the
kept frontmatter text.

## Caveats and intended automation

- The derived bundle is a **view**. Regenerate it; never hand-edit it as if it were a source.
- Densifying edges proposed by `suggest-links` that point at frozen files (e.g. a back-ref onto
  `corpus/refuted/c1-…`) must live in the projection or a mutable index, never be written into
  the frozen source. `--apply` is not run against this corpus.
- **Intended automation (deferred):** a read-only daily observatory beat that regenerates
  `epistemics-okf/`. It must stay pure (filesystem read + side-dir write only); no `ingest`,
  no `--cir`. Until then the projection is run on demand.
