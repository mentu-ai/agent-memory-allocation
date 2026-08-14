# Foundational ideas audit - 2026-06-19

## Scope

Read-only audit of the supplied mentu-physics files:

- `mentu-identity/genesis-profiles/README.md`
- `mentu-identity/genesis-profiles/genesis-profile-1.md`
- `constitutional-intelligence/cost-of-coherence.md`
- `epistemic-escape-velocity.md`
- `ideas-for-memory.md`
- `principles-laws-structural-imperatives.md.txt`
- `threshold-of-epistemic-activation.md`

No predecessor files were edited. Live data checks used direct reads of
`~/.mentu/training/cir-run-outcomes.jsonl`, `~/.mentu/cir.db`, and local recipe
manifests.

## Decision

Admit **C8 coherence dividend**:
`corpus/conjectures/c8-coherence-dividend.md`.

The old "cost of coherence" thesis becomes a measurable claim: guardrails and
verification should impose immediate overhead, then reduce downstream failure/rework
once recipes mature. The constants, critical-temperature equation, and inevitability
claims are dropped.

The first readiness analyzer is in
`analyses/c8-coherence-dividend/analyze.py`. Its current expected state is
`INSTRUMENT INSUFFICIENT`: the run-outcome corpus has enough volume and span, but
historical runs do not yet carry recipe manifest hashes, so current manifests cannot
be safely used as historical predictors.

Live readiness digest from 2026-06-19:

- run rows: 629;
- distinct recipes: 168;
- run span: 33.1 days;
- all minimum size/span gates: pass;
- manifest identity gate: fail at 0.0%;
- verdict tables: suppressed by design.

## Dispositions

| Idea | Disposition | Why |
|---|---|---|
| Cost of coherence | **Admitted as C8** | Has a clean operational residue: upfront guardrail overhead vs downstream reliability dividend. |
| Threshold of epistemic activation | **Folded into C8 gates** | Useful as readiness language, but too broad as a standalone claim. Activation becomes "do not analyze until exact manifest identity exists." |
| Epistemic escape velocity | **Already metabolized by C6; constants remain excluded** | The self-sustaining growth shape is covered by C6. Escape rhetoric remains parked. |
| Genesis Profile | **Not admitted separately** | Strong product/identity concept, but no live profile-event telemetry yet. It may become a person/profile-layer analogue of C7 once genesis profiles are actually used. |
| Ideas for memory / local CIR | **Instrument lineage, not new claim** | Much of it already exists as Mentu CIR, recipe outcomes, and Crawlio LACS. The scientific move is testing outcomes, not reasserting architecture. |
| Principles/laws/structural imperatives | **Partially metabolized** | C1-C8 now cover the measurable residues: return, friction, entropy, mass, boundary, compounding, handles, and coherence cost. The remaining law-suite constants stay excluded. |

## Next push

Persist recipe manifest identity into run outcomes:

- `recipe_manifest_hash`;
- recipe manifest path;
- recipe manifest hash algorithm/version;
- optional immutable run bundle hash;
- guardrail-load components computed at recipe commit time.

Once that exists, C8 can graduate from readiness to a controlled verdict analysis.
